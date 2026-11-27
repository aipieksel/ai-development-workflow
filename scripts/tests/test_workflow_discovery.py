"""Task-aware resource discovery regressions."""
from pathlib import Path
import copy
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from route_workflow import route, route_task
from workflow_catalog import (
    DISCOVERY_SCHEMA,
    SEARCH_SCHEMA,
    build_catalog,
    build_search_index,
    search_resources,
    validate_discovery,
)


class WorkflowDiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = build_catalog(ROOT)
        cls.index = build_search_index(ROOT, cls.catalog)

    def ids(self, report, group):
        return [row["id"] for row in report["groups"][group]]

    def test_plugin_evolution_surfaces_recipe_and_domain_lenses(self):
        report = search_resources(
            "Improve a portable skill router from observed usage failures",
            self.index,
            refined_query="Python skill catalogue and package router; domain guidance is not applied",
        )
        self.assertIn("recipe:plugin-evolution", self.ids(report, "recipes")[:3])
        self.assertIn("specialist:plugins-mcp", self.ids(report, "specialists")[:3])
        self.assertIn("specialist:usage-learning", self.ids(report, "specialists")[:3])
        plugin = next(row for row in report["groups"]["specialists"]
                      if row["id"] == "specialist:plugins-mcp")
        self.assertTrue({"useWhen", "recipe-recommendation"} &
                        {match["field"] for match in plugin["matched"]})
        self.assertTrue(report["candidateOnly"])

    def test_visual_correction_surfaces_visual_recipe_and_lenses(self):
        report = search_resources(
            "Repair the wrong typography spacing and component states in the rendered page",
            self.index,
            refined_query="Existing design system page has incorrect typography spacing and visual component states",
        )
        self.assertIn("recipe:visual-correction", self.ids(report, "recipes")[:3])
        lenses = self.ids(report, "specialists")
        self.assertIn("specialist:ui-design", lenses)
        self.assertIn("specialist:design-system", lenses)

    def test_inspected_react_next_evidence_ranks_react_specialist_first(self):
        report = search_resources(
            "Fix the reported integration behavior and verify it",
            self.index,
            refined_query=("Inspected package.json and source evidence: Next.js React App Router, "
                           "server and client components, reusable component APIs, state-driven UI "
                           "and frontend rendering performance"),
        )
        specialist = report["groups"]["specialists"][0]
        self.assertEqual(specialist["id"], "specialist:react-frontend")
        self.assertTrue(specialist["matched"])
        self.assertTrue({"useWhen", "summary", "description"} &
                        {match["field"] for match in specialist["matched"]})

    def test_inspected_wordpress_woocommerce_evidence_ranks_wordpress_specialist_first(self):
        report = search_resources(
            "Fix the reported integration behavior and verify it",
            self.index,
            refined_query=("Inspected plugin headers and PHP source evidence: WordPress WooCommerce "
                           "plugin hooks, capabilities, nonces, REST integration, checkout order "
                           "lifecycle and order metadata"),
        )
        specialist = report["groups"]["specialists"][0]
        self.assertEqual(specialist["id"], "specialist:wordpress-woocommerce")
        self.assertTrue(specialist["matched"])
        self.assertTrue({"useWhen", "summary", "description"} &
                        {match["field"] for match in specialist["matched"]})

    def test_explicit_named_exclusions_do_not_promote_conflicting_lenses(self):
        baseline = search_resources("Maintain the WHMCS payment integration", self.index)
        excluded = search_resources(
            "Maintain the WHMCS payment integration, no WordPress or browser extraction work",
            self.index,
        )
        self.assertIn("specialist:whmcs", self.ids(excluded, "specialists"))
        self.assertNotIn("specialist:wordpress-woocommerce", self.ids(excluded, "specialists"))
        self.assertNotIn("specialist:browser-extraction", self.ids(excluded, "specialists"))
        self.assertEqual(excluded["excludedTerms"], ["browser", "extraction", "wordpress"])
        self.assertNotIn("specialist:wordpress-woocommerce", self.ids(baseline, "specialists")[:3])

    def test_index_is_deterministic_and_covers_every_eligible_reference_once(self):
        again = build_search_index(ROOT, build_catalog(ROOT))
        self.assertEqual(self.index, again)
        self.assertEqual(self.index["schema"], SEARCH_SCHEMA)
        reference_paths = [row["path"] for row in self.index["resources"]
                           if row["kind"] == "reference"]
        self.assertEqual(sorted(reference_paths), self.index["eligibleReferences"])
        self.assertEqual(len(reference_paths), len(set(reference_paths)))
        expected = sorted(path.relative_to(ROOT).as_posix()
                          for path in (ROOT / "references").glob("*.md")
                          if path.name != "workflow-index.md")
        self.assertEqual(sorted(reference_paths), expected)
        excluded = {row["path"] for row in self.index["excludedReferences"]}
        self.assertIn("references/workflow-index.md", excluded)
        self.assertIn("references/workflow-search-index.json", excluded)

    def test_empty_queries_and_unknown_groups_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "nonempty initial query"):
            search_resources("", self.index)
        with self.assertRaisesRegex(ValueError, "Unknown discovery kinds"):
            search_resources("plugin router", self.index, kinds=["unknown"])

    def test_auto_route_exposes_mandatory_candidate_only_discovery(self):
        routed = route_task("Improve this plugin router")
        policy = routed["discoveryPolicy"]
        self.assertTrue(policy["requiredBeforeFinalSelection"])
        self.assertTrue(policy["candidateOnly"])
        self.assertEqual(routed["discoveryIndex"], "references/workflow-search-index.json")
        self.assertEqual(routed["request"], "Improve this plugin router")

    def test_every_task_bearing_route_exposes_the_common_discovery_policy(self):
        descriptors = [
            route("G1 improve routing"),
            route("recipe plugin-evolution improve routing"),
            route_task("G1 remains literal task prose"),
        ]
        for descriptor in descriptors:
            with self.subTest(action=descriptor["action"]):
                self.assertEqual(descriptor["discoveryIndex"], "references/workflow-search-index.json")
                self.assertTrue(descriptor["discoveryPolicy"]["requiredBeforeFinalSelection"])
                self.assertTrue(descriptor["discoveryPolicy"]["candidateOnly"])

    def test_current_receipt_checks_paths_fingerprint_and_recipe_recommendations(self):
        selection = {
            "specialists": ["specialist:usage-learning", "specialist:plugins-mcp"],
            "evaluated": [{"id": "recipe:plugin-evolution", "disposition": "covered",
                           "reason": "Use the task-specific subset."}],
        }
        selected = []
        for identity in selection["specialists"]:
            resource = next(row for row in self.index["resources"] if row["id"] == identity)
            selected.append({
                "id": identity, "reason": "The inspected skill router uses this domain.",
                "instructionPaths": [resource["path"]], "assignment": "worker-1",
                "question": "Apply the domain contract to the inspected router.",
                "acceptance": ["The result shows a concrete domain-specific effect."],
            })
        query = "plugin router usage failures"
        refined = "Python skill catalogue router and package"
        report = search_resources(query, self.index, refined_query=refined)
        receipt = {
            "schema": DISCOVERY_SCHEMA, "initialQuery": query,
            "refinedQuery": refined,
            "indexFingerprint": self.index["indexFingerprint"],
            "matches": [{"id": row["id"], "score": row["score"]}
                        for rows in report["groups"].values() for row in rows],
            "selected": selected,
            "recipeRecommendations": [
                {"recipe": "recipe:plugin-evolution", "specialist": "specialist:usage-learning",
                 "disposition": "selected", "reason": "Usage failure is the supplied evidence."},
                {"recipe": "recipe:plugin-evolution", "specialist": "specialist:plugins-mcp",
                 "disposition": "selected", "reason": "The changed owner is a skill router."},
                {"recipe": "recipe:plugin-evolution", "specialist": "specialist:artifact-delivery",
                 "disposition": "not-applicable", "reason": "This fixture does not package or publish."},
            ],
        }
        self.assertEqual(validate_discovery(receipt, selection, self.index), [])
        stale = copy.deepcopy(receipt)
        stale["indexFingerprint"] = "stale"
        self.assertTrue(any("fingerprint" in error for error in
                            validate_discovery(stale, selection, self.index)))
        unsupported = copy.deepcopy(receipt)
        unsupported["schema"] = "unsupported"
        self.assertEqual(validate_discovery(unsupported, selection, self.index).count(
            "Unsupported discovery receipt schema"), 1)


if __name__ == "__main__":
    unittest.main()
