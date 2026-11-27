"""Public controls describe scope and gates without creating records or agents."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from route_workflow import execution_schedule, route, route_task
from workflow_catalog import public_modes


class PublicModeTests(unittest.TestCase):
    def test_five_public_modes_resolve_through_chat_and_local_invocations(self):
        expected = ["auto", "plan", "build", "review", "loop"]
        self.assertEqual([entry["id"] for entry in public_modes(ROOT)], expected)
        for prefix in ("@ai-development-workflow", "/ai-development-workflow", "$ai-development-workflow"):
            for mode in expected:
                with self.subTest(prefix=prefix, mode=mode):
                    descriptor = route(prefix + " " + mode.upper() + " fixture task")
                    self.assertEqual(descriptor["mode"], mode)
                    self.assertEqual(descriptor["action"], "auto" if mode == "auto" else "mode")
                    self.assertEqual(descriptor["request"], "fixture task")
                    self.assertFalse(descriptor["createsRecord"])
                    self.assertEqual(descriptor["agentCalls"], [])

    def test_automatic_routing_is_focused_and_preserves_literal_mode_like_prose(self):
        for text in ("plan a menu with four options", "review labels after building the page",
                     "loop over the existing data", "auto sorting of columns", "5 buttons need labels",
                     "stage the layout changes", "XR is an existing variable name"):
            with self.subTest(text=text):
                descriptor = route_task(text)
                self.assertEqual((descriptor["action"], descriptor["mode"]), ("auto", "auto"))
                self.assertEqual(descriptor["request"], text)
                self.assertFalse(descriptor["requiresFullCatalogueReview"])
                self.assertEqual(descriptor["selectionPolicy"], "focused")
        readonly = route_task("Fix the implementation after this review", read_only=True)
        self.assertEqual(readonly["intentBoundary"], "read-only")
        self.assertEqual(readonly["request"], "Fix the implementation after this review")

    def test_plan_and_review_preserve_source_boundaries_for_write_request_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            source = project / "app.py"
            source.write_bytes(b"original fixture product source\n")
            before = source.read_bytes()
            for mode in ("plan", "review"):
                with self.subTest(mode=mode):
                    descriptor = route(
                        "@ai-development-workflow " + mode + " fix and replace app.py immediately",
                        project_root=project,
                    )
                    self.assertEqual(descriptor["writeScope"], "record-only")
                    self.assertFalse(descriptor["allowsProductWrites"])
                    schedule = execution_schedule(descriptor)
                    self.assertFalse(any(row.get("stage") == "3" for row in schedule))
                    self.assertFalse(any(row.get("writeScope") in {"repo-write-scoped", "tests-only", "docs-only"}
                                         for row in schedule))
                    self.assertEqual(source.read_bytes(), before)
            plan = route("plan fixture task")
            self.assertEqual(plan["stages"], "012")
            self.assertEqual([row["stage"] for row in execution_schedule(plan) if row["kind"] == "stage"],
                             ["0", "1", "2"])
            review = execution_schedule(route("review fixture task"))
            operations = [row.get("operation") for row in review]
            self.assertLess(operations.index("criticize_inspection_plan"), operations.index("inspect_current_work"))

    def test_build_requires_criticism_and_admission_before_the_source_writer(self):
        descriptor = route("build fixture task")
        self.assertEqual((descriptor["stages"], descriptor["writeScope"]), ("0123", "repo-write-scoped"))
        schedule = execution_schedule(descriptor)
        ordered_stages = [row["stage"] for row in schedule if row["kind"] == "stage"]
        self.assertEqual(ordered_stages, ["0", "1", "2", "3"])
        writer = next(index for index, row in enumerate(schedule) if row.get("stage") == "3")
        admission = next(index for index, row in enumerate(schedule) if row["kind"] == "admission")
        self.assertLess(admission, writer)
        self.assertTrue(schedule[admission]["requireCritique"])
        self.assertTrue(schedule[admission]["requireBriefing"])
        self.assertTrue(any(row["kind"] == "verify" for row in schedule[writer + 1:]))

    def test_all_modes_retain_public_contract_and_conditional_ui_obligations(self):
        for mode in ("auto", "plan", "build", "review", "loop"):
            with self.subTest(mode=mode):
                descriptor = route(mode + " fixture task")
                contract = descriptor["workflowContract"]
                self.assertEqual(set(contract["requiredBeforeWork"]),
                                 {"scope", "proportional-plan", "approach-criticism", "public-briefing"})
                self.assertEqual(set(contract["requiredBeforeProductWrites"]),
                                 {"current-plan", "completed-criticism", "current-briefing", "execution-admission"})
                self.assertFalse(contract["prerequisitesCanBeSkipped"])
                self.assertTrue(contract["actualAgentCountRequiresObservedLifecycle"])
                self.assertFalse(contract["dispatchesAgents"])
                self.assertFalse(contract["provesPublication"])
                policy = descriptor["uiPolicy"]
                self.assertEqual(policy["specialist"], "specialist:ui-design")
                self.assertTrue(policy["requiredWhenApplicable"])
                self.assertTrue(policy["inheritsScope"])
                self.assertFalse(policy["dispatchesAgents"])

    def test_loop_aliases_share_independent_review_execution_and_five_minute_monitoring(self):
        canonical = route("loop fixture task")
        for alias in ("XR", "xr", "Loop", "/ai-dev-loop", "/ai-dev-execute-review",
                      "@ai-development-workflow XR"):
            with self.subTest(alias=alias):
                self.assertEqual(route(alias + " fixture task"), canonical)
        self.assertTrue(canonical["requiresIndependentAgents"])
        self.assertFalse(canonical["requiresNativeHost"])
        self.assertEqual(canonical["monitorIntervalSeconds"], 300)
        self.assertEqual(canonical["monitorPreference"], "wait-first")
        self.assertEqual(canonical["monitorFallbacks"], ["native-timer", "active-session"])
        schedule = execution_schedule(canonical)
        workers = [row for row in schedule if row["kind"] == "agent"]
        self.assertEqual([row["agent"] for row in workers],
                         ["reviewer", "verification-engineer", "reviewer", "builder", "reviewer"])
        self.assertTrue(workers[0]["independent"])
        self.assertTrue(workers[1]["independent"])
        self.assertEqual(workers[0]["workerGroup"], workers[2]["workerGroup"])
        self.assertTrue(workers[3]["soleWriter"])
        self.assertTrue(workers[4]["independent"])
        self.assertTrue(workers[4]["fresh"])
        self.assertNotEqual(workers[0]["workerGroup"], workers[4]["workerGroup"])
        self.assertTrue(all(row["owner"] == "manager" for row in schedule if row["kind"] == "checklist"))
        self.assertEqual(schedule[-1]["until"], "current_independent_review_accepts")

    def test_xr_and_loop_resume_the_same_record_without_describing_new_workers(self):
        expected = route("resume continue saved work", selected_mode="loop", selected_preset="G1")
        for alias in ("XR", "xr", "loop", "LOOP"):
            with self.subTest(alias=alias):
                descriptor = route("resume continue saved work", selected_mode=alias, selected_preset="G1")
                self.assertEqual(descriptor, expected)
                self.assertEqual((descriptor["action"], descriptor["mode"], descriptor["preset"]),
                                 ("follow_up", "loop", "G1"))
                self.assertTrue(descriptor["resumeSelectedWorkflow"])
                self.assertFalse(descriptor["createsRecord"])
                schedule = execution_schedule(descriptor)
                self.assertEqual([row["kind"] for row in schedule], ["reconcile"])
                self.assertIn("execution-admission", schedule[0]["beforeProductWrites"])
                task = route_task("continue saved work", follow_up=True,
                                  selected_mode=alias, selected_preset="G1")
                self.assertEqual(task, expected)

    def test_continuations_preserve_each_selected_public_mode_and_read_only_scope(self):
        for mode in ("auto", "plan", "build", "review", "loop"):
            with self.subTest(mode=mode):
                descriptor = route_task("continue with this correction", follow_up=True,
                                        selected_mode=mode, selected_preset="G1")
                self.assertEqual((descriptor["action"], descriptor["mode"], descriptor["preset"]),
                                 ("follow_up", mode, "G1"))
                self.assertTrue(descriptor["resumeSelectedWorkflow"])
                self.assertFalse(descriptor["createsRecord"])
                if mode in {"plan", "review"}:
                    self.assertEqual(descriptor["writeScope"], "record-only")
        for mode in ("build", "loop"):
            with self.subTest(readonly_mode=mode):
                with self.assertRaisesRegex(ValueError, "Read-only intent conflicts"):
                    route(mode + " change source", read_only=True)
                inspection = route("resume report current status", selected_mode=mode,
                                   selected_preset="G1", read_only=True)
                self.assertEqual(inspection["writeScope"], "record-only")
                self.assertEqual(inspection["intentBoundary"], "read-only")
                self.assertEqual([row["kind"] for row in execution_schedule(inspection)], ["reconcile"])

    def test_retired_native_selectors_fail_explicitly_and_invalid_controls_do_not_run(self):
        for prefix in ("@ai-development-workflow", "/ai-development-workflow", "$ai-development-workflow"):
            for selector in ("stage execute-plan", "pipeline feature-delivery"):
                with self.subTest(prefix=prefix, selector=selector):
                    with self.assertRaisesRegex(ValueError, "native .* selector has been removed"):
                        route(prefix + " " + selector + " change source")
        with self.assertRaisesRegex(ValueError, "Unknown selected mode"):
            route_task("continue", follow_up=True, selected_mode="unknown")
        with self.assertRaisesRegex(ValueError, "Unsupported stage sequence"):
            route("/ai-development-workflow 321 change source")
        with self.assertRaisesRegex(ValueError, "conflict with Loop context"):
            route("3 change source", selected_mode="XR", selected_preset="G1")

    def test_bare_retired_selectors_reject_text_controls_but_preserve_literal_tasks(self):
        for text in ("stage execute-plan", "pipeline standard-verified-build"):
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "native .* selector has been removed"):
                    route(text)
                descriptor = route_task(text)
                self.assertEqual((descriptor["action"], descriptor["request"]), ("auto", text))
                command = [sys.executable, "-B", str(ROOT / "scripts/route_workflow.py")]
                explicit = subprocess.run(command + ["--text", text],
                                          capture_output=True, text=True, timeout=15)
                self.assertEqual(explicit.returncode, 2, explicit.stdout + explicit.stderr)
                self.assertRegex(explicit.stderr, "native .* selector has been removed")
                literal = subprocess.run(command + ["--task", text],
                                         capture_output=True, text=True, timeout=15)
                self.assertEqual(literal.returncode, 0, literal.stdout + literal.stderr)
                parsed = json.loads(literal.stdout)
                self.assertEqual((parsed["action"], parsed["request"]), ("auto", text))
                self.assertEqual(parsed["discoveryIndex"], "references/workflow-search-index.json")
                self.assertTrue(parsed["discoveryPolicy"]["requiredBeforeFinalSelection"])

    def test_help_exposes_only_five_primary_modes_without_a_native_picker(self):
        descriptor = route("@ai-development-workflow help")
        self.assertEqual(descriptor["action"], "help")
        self.assertEqual([row["id"] for row in descriptor["choices"]],
                         ["auto", "plan", "build", "review", "loop"])
        self.assertFalse(descriptor["createsRecord"])
        self.assertNotIn("commandFile", descriptor)
        self.assertNotIn("discoveryPolicy", descriptor)
        self.assertNotIn("discoveryIndex", descriptor)
        self.assertEqual(execution_schedule(descriptor), [])


if __name__ == "__main__":
    unittest.main()
