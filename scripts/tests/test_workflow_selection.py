"""Focused selection tests against the real catalogue, without dispatching work.

Existing-evidence references below are synthetic declarations used to test
structural prerequisites; they are not approval, review or execution receipts.
"""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from workflow_catalog import build_catalog, validate_selection
from route_workflow import route
from contract_fixture import declare_policy, fixture_assignment
from workflow_contract import pending_contract
from task_policy import ASSESSOR, PLANNER, UI_DIRECTOR, VISUAL_REVIEWER, PLAN_REVIEWER, CODE_REVIEWER


EXPECTED_RECIPES = {
    "reference-rebuild", "visual-correction", "design-system-rollout",
    "native-yaml-conversion", "asset-production", "motion-reconstruction",
    "media-library-extension", "content-site-delivery", "artifact-handoff", "plugin-evolution",
}


class FocusedSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = build_catalog(ROOT)
        cls.entries = {row["id"]: row for row in cls.catalog["entries"]}

    def selection(self, *ids, intent="implement", ui=False, specialists=(), evidence=()):
        mode = "build" if intent in {"implement", "docs"} else "plan" if intent == "plan" else "review"
        if len(ids) == 1 and ids[0] in {"mode:plan", "mode:build", "mode:review", "mode:loop"} and intent in {"implement", "docs"}:
            mode = ids[0].split(":")[1]
        if len(ids) == 1 and ids[0].lower() == "mode:xr" and intent == "implement":
            mode = "loop"
        contract = pending_contract(write_scope="docs-only" if intent == "docs" else "repo-write-scoped")
        declare_policy(contract, mode=mode)
        selected = contract["selection"]
        if mode in {"plan", "review"}:
            selected["phases"] = selected["phases"][:3]
            if mode == "plan":
                selected["delegation"]["assignments"] = [fixture_assignment("plan", PLANNER), fixture_assignment("critique", PLAN_REVIEWER, ["plan"])]
            else:
                selected["phases"] += [
                    {"id": "inspect", "title": "Inspect", "kind": "other", "operation": "inspect-current-source", "writeScope": "record-only", "owner": "specialist", "dependsOn": ["critique"]},
                    {"id": "countercheck", "title": "Check findings", "kind": "verify", "operation": "corroborate-findings", "writeScope": "record-only", "owner": "reviewer", "dependsOn": ["inspect"]},
                ]
                selected["delegation"]["assignments"] = [fixture_assignment("inspect", ASSESSOR), fixture_assignment("countercheck", CODE_REVIEWER, ["plan", "inspect"])]
        if ui:
            self.ui_assignments(selected)
        return {
            **{key: selected[key] for key in ("mode", "routing", "delegation", "reviewPolicy", "phases", "verificationContext")},
            "catalogueFingerprint": self.catalog["catalogueFingerprint"],
            "intent": intent,
            "request": "Exercise the requested fixture scope and selected prerequisites.",
            "reason": "Use only the operations necessary for this isolated structural test.",
            "chain": [{"id": identity, "why": "Required for the declared fixture outcome: " + identity}
                      for identity in ids],
            "specialists": list(specialists),
            "existingEvidence": [{"artifact": name, "record": "fixture:declared-" + name}
                                 for name in evidence],
            "uiContext": selected["uiContext"],
        }

    @staticmethod
    def ui_assignments(selected):
        selected["uiContext"] = {"applicable": True, "kind": "design", "reason": "The fixture explicitly develops a source-grounded UI specification."}
        assignments = selected["delegation"]["assignments"]
        selected["phases"].insert(1, {"id": "design", "title": "Design UI", "kind": "other", "operation": "design-ui", "writeScope": "record-only", "owner": "UI Director", "dependsOn": ["scope"]})
        next(row for row in selected["phases"] if row["id"] == "plan")["dependsOn"] = ["design"]
        assignments.append(fixture_assignment("design", UI_DIRECTOR, capabilities=["design-ui", "ui-design"]))
        for row in assignments:
            if row["phaseId"] in {"critique", "accept", "countercheck"}:
                row["independentFrom"].append("design")
            if "ui-design" not in row["capabilities"]:
                row["capabilities"].append("ui-design")
            if row["phaseId"] in {"accept", "countercheck", "critique"} and "review-ui" not in row["capabilities"]:
                row["capabilities"].append("review-ui")

    def valid(self, selection, catalog=None):
        result = validate_selection(selection, catalog or self.catalog)
        self.assertTrue(result["valid"], result["errors"])
        return result

    def invalid(self, selection, message, catalog=None):
        result = validate_selection(selection, catalog or self.catalog)
        self.assertFalse(result["valid"], result)
        self.assertTrue(any(message in error for error in result["errors"]), result["errors"])
        return result

    def test_compact_ordered_chain_needs_no_exhaustive_evaluation_rows(self):
        selection = self.selection("stage:plan-code", "stage:review-plan", "stage:execute-plan")
        self.assertNotIn("evaluated", selection)
        result = self.valid(selection)
        self.assertEqual(result["chain"], [row["id"] for row in selection["chain"]])
        self.assertEqual(result["checkedEntryCount"], 3)
        self.assertLess(result["checkedEntryCount"], result["catalogueEntryCount"])

    def test_legacy_catalogue_selection_is_readable_but_not_execution_admissible(self):
        legacy = self.selection("mode:plan", intent="plan")
        inspected = validate_selection(legacy, self.catalog)
        self.assertTrue(inspected["valid"], inspected["errors"])
        self.assertEqual(inspected["discoveryStatus"], "legacy-reconciliation-required")
        execution = validate_selection(legacy, self.catalog, execution=True)
        self.assertFalse(execution["valid"])
        self.assertTrue(any("before execution" in error for error in execution["errors"]))

    def test_optional_evaluated_records_keep_their_consistency_checks(self):
        selection = self.selection("mode:plan", intent="plan")
        selection["evaluated"] = [{"id": "mode:plan", "disposition": "selected",
                                   "reason": "Preserve a focused legacy decision row."}]
        self.valid(selection)
        selection["evaluated"][0]["disposition"] = "not-applicable"
        self.invalid(selection, "Chain/lens entry must be selected: mode:plan")
        selection["evaluated"] = [
            {"id": identity, "disposition": "selected" if identity == "mode:plan" else "not-applicable",
             "reason": "Synthetic full-catalogue compatibility declaration for " + identity}
            for identity in self.entries
        ]
        self.valid(selection)

    def test_evaluated_rows_cannot_waive_explicit_ui_applicability(self):
        variants = (None, [], [{"id": "mode:plan", "disposition": "selected",
                               "reason": "A retained optional evaluated row does not waive UI scope."}])
        for evaluated in variants:
            with self.subTest(evaluated=evaluated):
                selection = self.selection("mode:plan", intent="plan")
                if evaluated is not None:
                    selection["evaluated"] = evaluated
                self.valid(selection)
                selection.pop("uiContext")
                self.invalid(selection, "Selection needs uiContext applicability and reason")
                selection["uiContext"] = {"applicable": True, "kind": "design",
                                          "reason": "This fixture explicitly concerns a user interface."}
                self.invalid(selection, "UI scope requires the selected specialist:ui-design lens")
                selection["specialists"] = ["specialist:ui-design"]
                self.ui_assignments(selection)
                self.valid(selection)

    def test_execute_requires_both_plan_and_review_evidence(self):
        for evidence, missing in (((), "code.plan, plan.review"),
                                  (("code.plan",), "plan.review"),
                                  (("plan.review",), "code.plan")):
            with self.subTest(evidence=evidence):
                self.invalid(self.selection("stage:execute-plan", evidence=evidence),
                             "stage:execute-plan requires prior evidence: " + missing)
        self.valid(self.selection("stage:execute-plan", evidence=("code.plan", "plan.review")))

    def test_new_plan_invalidates_an_existing_review_before_execution(self):
        selection = self.selection("stage:plan-code", "stage:execute-plan",
                                   evidence=("plan.review", "execution.result"))
        self.invalid(selection, "stage:execute-plan requires prior evidence: plan.review")
        selection["chain"].insert(1, {"id": "stage:review-plan", "why": "Review the newly produced plan."})
        self.valid(selection)

    def test_plan_and_review_work_without_prior_execution_but_cannot_authorize_writes(self):
        for identity, intent in (("mode:plan", "plan"), ("mode:review", "review"),
                                 ("stage:review-code", "review")):
            with self.subTest(read_only=identity):
                self.valid(self.selection(identity, intent=intent))
                self.assertEqual(self.entries[identity]["writeScope"], "record-only")
                self.assertNotIn("execution.result", self.entries[identity]["requiresAll"])
        for intent in ("plan", "review"):
            for identity in ("stage:execute-plan", "mode:build", "mode:loop"):
                with self.subTest(intent=intent, writer=identity):
                    self.invalid(self.selection(identity, intent=intent,
                                                evidence=("code.plan", "plan.review")),
                                 "Intent does not permit repo-write-scoped: " + identity)

    def test_unknown_duplicate_and_unexplained_operations_fail_closed(self):
        self.invalid(self.selection("stage:not-an-operation"), "unknown entry ID")
        self.invalid(self.selection("stage:plan-code", "stage:plan-code"),
                     "chain contains duplicate ID stage:plan-code")
        selection = self.selection("mode:plan", intent="plan")
        selection["chain"][0]["why"] = ""
        self.invalid(selection, "chain[0] needs a nonempty reason")
        selection = self.selection("mode:plan", intent="plan")
        selection.pop("reason")
        self.invalid(selection, "Compact selection needs a reason")

    def test_neutral_instruction_change_invalidates_a_saved_catalogue_fingerprint(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git", "dist"))
            before = build_catalog(source)
            selection = self.selection("mode:plan", intent="plan")
            selection["catalogueFingerprint"] = before["catalogueFingerprint"]
            self.valid(selection, before)
            instruction = source / "workflows/stages/plan-code.md"
            instruction.write_text(instruction.read_text() + "\nSynthetic fixture-only source revision.\n")
            after = build_catalog(source)
            self.assertNotEqual(before["catalogueFingerprint"], after["catalogueFingerprint"])
            self.invalid(selection, "Catalogue fingerprint is missing or stale", after)
            selection["catalogueFingerprint"] = after["catalogueFingerprint"]
            self.valid(selection, after)

    def test_declared_or_explicit_ui_scope_requires_the_ui_design_lens(self):
        for identity in ("mode:plan", "stage:design-ui"):
            with self.subTest(identity=identity):
                selection = self.selection(identity, intent="plan", ui=True)
                self.invalid(selection, "UI scope requires the selected specialist:ui-design lens")
                selection["specialists"] = ["specialist:ui-design"]
                self.valid(selection)
        self.invalid(self.selection("stage:design-ui", intent="plan", ui=False),
                     "uiContext cannot exclude UI for explicit visual operations")

    def test_loop_xr_alias_is_canonical_and_auto_is_not_an_executable_chain_item(self):
        for identity in ("mode:loop", "mode:XR", "mode:xr"):
            with self.subTest(identity=identity):
                result = self.valid(self.selection(identity))
                self.assertEqual(result["chain"], ["mode:loop"])
        self.assertTrue(self.entries["mode:loop"]["requiresIndependentAgents"])
        self.invalid(self.selection("mode:auto"), "unknown entry ID")
        self.invalid(self.selection("mode:XR", "mode:loop"), "chain contains duplicate ID mode:loop")

    def test_all_ten_recipes_route_and_validate_with_only_neutral_dependencies(self):
        recipes = {row["id"].removeprefix("recipe:"): row for row in self.catalog["entries"]
                   if row["kind"] == "recipe"}
        self.assertEqual(set(recipes), EXPECTED_RECIPES)
        for removed in ("agents-pro-v2", "integrations/workflow-picker", "integrations/skill-selector"):
            self.assertFalse((ROOT / removed).exists(), removed)
        for identity, recipe in recipes.items():
            with self.subTest(recipe=identity):
                descriptor = route("/ai-development-workflow recipe " + identity + " fixture task")
                self.assertEqual((descriptor["action"], descriptor["id"]), ("recipe", identity))
                self.assertFalse(descriptor["requiresNativeHost"])
                self.assertEqual(descriptor["suggestedExpansion"], recipe["expansion"])
                selection = self.selection(*recipe["expansion"],
                                           ui="specialist:ui-design" in recipe["recommendedSpecialists"],
                                           specialists=recipe["recommendedSpecialists"])
                selection["evaluated"] = [{"id": recipe["id"], "disposition": "selected",
                                           "reason": "Preserve this complete recipe's required input bindings."}]
                self.valid(selection)
                for stage_id in recipe["expansion"]:
                    stage = self.entries[stage_id]
                    self.assertTrue(stage["instructions"].startswith("workflows/stages/"))
                    for relative in (stage["instructions"], *stage["profiles"]):
                        self.assertFalse(relative.startswith(("agents-pro-v2/", "integrations/")), relative)
                        self.assertTrue((ROOT / relative).read_text().strip(), relative)

    def test_partial_recipe_cannot_omit_its_required_ui_review_evidence(self):
        recipe = self.entries["recipe:reference-rebuild"]
        partial = [identity for identity in recipe["expansion"] if identity != "stage:review-ui-spec"]
        selection = self.selection(*partial, ui=True, specialists=recipe["recommendedSpecialists"])
        selection["evaluated"] = [{"id": recipe["id"], "disposition": "covered",
                                   "reason": "Synthetic partial recipe tests that required bindings remain enforced.",
                                   "coveredBy": partial}]
        self.invalid(selection, "stage:plan-code requires prior evidence: ui.spec.review")


if __name__ == "__main__":
    unittest.main()
