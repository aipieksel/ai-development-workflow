"""Behavioral routing/admission regressions using synthetic worker evidence only."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from contract_fixture import declare_policy, refresh_contract, fixture_assignment, declare_returned_contributions, make_readonly_contract
from test_contract import fixture
from route_workflow import execution_schedule, route, route_task
from task_policy import ARCHITECT, ASSESSOR, FAST_ENGINEER, UI_DIRECTOR, VISUAL_REVIEWER, routing_requirements
from workflow_contract import briefing_binding, pending_contract, render_briefing, validate_contract


def decision(mode="build", impact="small-localized", **facts):
    routing = {"impact": impact, "affectedPages": ["settings"], "affectedFeatures": ["settings labels"],
               "changedSharedContract": False, "architectureOrMigration": False,
               "reason": "Synthetic inspection establishes the affected requested surface and consumers.",
               "evidence": ["fixture:owner-and-consumer-inspection"]}
    routing.update(facts)
    return {"mode": mode, "routing": routing,
            "uiContext": {"applicable": False, "kind": "none", "reason": "Synthetic backend-only scope."},
            "verificationContext": {"required": False, "triggers": [], "reason": "Synthetic single bounded validation."}}


class RoutingPolicyTests(unittest.TestCase):
    def test_small_auto_build_selects_existing_gb_with_three_real_worker_duties(self):
        descriptor = route_task("Change the inspected local label", decision=decision())
        self.assertEqual((descriptor["preset"], descriptor["resolvedMode"], descriptor["originMode"]), ("GB", "build", "auto"))
        self.assertEqual([row["agent"] for row in execution_schedule(descriptor) if row["kind"] == "agent"],
                         ["reviewer", "builder", "reviewer"])
        self.assertFalse(descriptor["taskPolicy"]["dispatchesAgents"])

    def test_small_plan_and_review_do_not_become_builds(self):
        for mode in ("plan", "review"):
            descriptor = route_task("A small request", decision=decision(mode))
            self.assertEqual(descriptor["mode"], mode)
            self.assertEqual(descriptor["writeScope"], "record-only")
            self.assertNotEqual(descriptor.get("preset"), "GB")
            self.assertTrue(any(row.get("agent") for row in execution_schedule(descriptor)))

    def test_cross_cutting_auto_build_selects_architect_before_plan(self):
        for facts in ({"affectedPages": ["home", "account"]},
                      {"affectedFeatures": ["accounts", "billing"]},
                      {"changedSharedContract": True}, {"architectureOrMigration": True}):
            with self.subTest(facts=facts):
                descriptor = route_task("A short task description", decision=decision(impact="cross-cutting", **facts))
                self.assertEqual(descriptor["preset"], "GA")
                schedule = execution_schedule(descriptor)
                architect = next(i for i, row in enumerate(schedule) if row.get("agent") == "architect")
                final_plan = next(i for i, row in enumerate(schedule) if row.get("kind") == "stage" and row.get("stage") == "1")
                self.assertLess(architect, final_plan)
                self.assertTrue(any(row.get("agent") == "builder" for row in schedule))

    def test_broad_declared_facts_cannot_be_classified_small_or_standard(self):
        for impact in ("small-localized", "standard"):
            with self.assertRaisesRegex(ValueError, "require cross-cutting impact"):
                routing_requirements("build", decision(impact=impact, changedSharedContract=True)["routing"])

    def test_unknown_impact_requires_actual_assessment_without_source_writes(self):
        descriptor = route_task("small quick simple change", decision=decision(impact="unknown", changedSharedContract=None))
        self.assertEqual(descriptor["routingStatus"], "assessment-required")
        self.assertNotIn("preset", descriptor)
        schedule = execution_schedule(descriptor)
        self.assertEqual([row.get("agent") for row in schedule if row["kind"] == "agent"], ["investigator", "reviewer"])
        self.assertFalse(any(row.get("writeScope") == "repo-write-scoped" for row in schedule))

    def test_scope_is_not_guessed_from_keywords_or_number_of_paths_in_request(self):
        descriptor = route_task("architect all pages migration one two three", decision=decision())
        self.assertEqual(descriptor["preset"], "GB")
        unresolved = route_task("one tiny label")
        self.assertIsNone(unresolved["resolvedMode"])
        self.assertEqual(unresolved["routingStatus"], "needs-source-grounded-decision")

    def test_quick_keeps_its_one_compact_record_with_fast_worker(self):
        descriptor = route("G0 local label", decision=decision())
        self.assertEqual(descriptor["action"], "quick")
        self.assertEqual(descriptor["preset"], "G0")
        self.assertEqual(descriptor["recordKind"], "checklist")
        self.assertTrue(any(row.get("agent") == "builder" for row in execution_schedule(descriptor)))
        self.assertEqual(descriptor["commandFile"], "commands/quick-task/ai-dev-quick-task.md")

    def test_read_only_commands_resolve_review_and_gpp_schedules_planner(self):
        for code in ("GAS", "GRC", "GDA", "GRS"):
            descriptor = route(code + " inspect", decision=decision("review", impact="standard"))
            self.assertEqual(descriptor["resolvedMode"], "review")
            self.assertTrue(any(row.get("agent") for row in execution_schedule(descriptor)))
        descriptor = route("GPP existing evidence", decision=decision("plan", impact="standard"))
        self.assertTrue(any(row.get("agent") == "architect" for row in execution_schedule(descriptor)))

    def test_auto_resolution_preserves_task_text_that_looks_like_controls(self):
        for text in ("--record output must remain literal", "G0 one route", "0 inspect", "recipe content-site-delivery"):
            descriptor = route_task(text, decision=decision())
            self.assertEqual(descriptor["preset"], "GB")
            self.assertEqual(descriptor["request"], text)

    def test_read_only_continuation_declares_review_and_preserves_build_or_loop_context(self):
        for mode in ("build", "loop"):
            descriptor = route("status", follow_up=True, selected_mode=mode, read_only=True,
                               decision=decision("review", impact="standard"))
            self.assertEqual(descriptor["resolvedMode"], "review")
            self.assertEqual(descriptor["selectedModeContext"], mode)
            self.assertEqual(descriptor["writeScope"], "record-only")
            self.assertEqual([row["kind"] for row in execution_schedule(descriptor)], ["reconcile"])

    def test_explicit_gb_cannot_waive_architect(self):
        descriptor = route("GB supplied work", decision=decision(impact="cross-cutting", changedSharedContract=True))
        self.assertEqual(descriptor["preset"], "GB")
        self.assertTrue(any(row.get("agent") == "architect" for row in execution_schedule(descriptor)))

    def test_all_entry_points_disclose_mandatory_workers_and_no_recursive_child_rule(self):
        for text in ("", "help", "auto", "G0 fix", "G1 fix", "GB fix", "GPL plan", "GPP plan", "0 capture", "2 criticize", "3 execute", "review inspect", "recipe plugin-evolution update"):
            with self.subTest(text=text):
                descriptor = route(text)
                self.assertTrue(descriptor["taskPolicy"]["requiresActualWorkers"])
                self.assertFalse(descriptor["taskPolicy"]["allowsSolo"])
                self.assertFalse(descriptor["taskPolicy"]["assignedChildrenRecurse"])
                self.assertEqual(descriptor["taskPolicy"]["missingDispatch"], "blocked")
                self.assertEqual(descriptor["taskPolicy"]["busyWorkers"], "wait-or-serialize")

    def test_explicit_mode_and_read_only_boundary_cannot_be_widened_by_decision(self):
        with self.assertRaisesRegex(ValueError, "explicit concrete mode"):
            route("plan inspect", decision=decision())
        with self.assertRaisesRegex(ValueError, "read-only boundary"):
            route_task("fix", read_only=True, decision=decision())

    def test_router_cli_consumes_host_decision_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "decision.json"
            source.write_text(json.dumps(decision()))
            result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/route_workflow.py"),
                                     "--task", "local label", "--decision", str(source)],
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["preset"], "GB")


class WorkerAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.record, self.data = fixture(Path(self.temp.name))
        self.contract = self.data["workflowContract"]

    def state(self, phase):
        return next(row for row in self.contract["progress"]["phases"] if row["id"] == phase)

    def refresh(self):
        return refresh_contract(self.record, self.data)

    def admit(self, **options):
        return validate_contract(self.record, self.data, **options)

    def architecture(self):
        selected = self.contract["selection"]
        selected["routing"] = decision(impact="cross-cutting", changedSharedContract=True)["routing"]
        selected["phases"].insert(1, {"id": "architecture", "title": "Architecture advice", "kind": "other",
            "operation": "inspect-owners-and-propose-contract", "writeScope": "read-only",
            "owner": "Architect", "dependsOn": ["scope"]})
        next(row for row in selected["phases"] if row["id"] == "plan")["dependsOn"] = ["architecture"]
        selected["delegation"]["assignments"].insert(0, fixture_assignment("architecture", ARCHITECT, capabilities=["design-architecture"]))
        for assignment in selected["delegation"]["assignments"]:
            if assignment["phaseId"] in {"critique", "accept"}:
                assignment["independentFrom"].append("architecture")
        self.contract["progress"]["phases"].insert(1, {"id": "architecture", "status": "complete", "ownerId": "fixture:architect",
            "authorIds": ["fixture:architect"], "evidence": ["fixture:architecture-result"], "workHash": None})
        self.contract["roster"]["workers"].append({"id": "fixture:architect", "role": "Architect", "status": "completed", "evidence": ["fixture:architecture-result"]})
        self.contract["roster"]["profiles"].append({"name": ARCHITECT, "ownerId": "fixture:architect"})
        self.contract["roster"]["assignments"].append({"assignmentId": "architecture", "workerId": "fixture:architect"})
        declare_returned_contributions(self.contract)
        self.refresh()

    def complete_implementation(self):
        for identity in ("execute", "verify", "accept"):
            self.state(identity).update(status="complete", ownerId="fixture:critic" if identity == "accept" else "fixture:executor",
                                        evidence=["fixture:result-" + identity])
        self.contract["progress"]["currentPhase"] = "accept"
        self.contract["progress"]["resultRevision"] = "fixture:stable-result-v1"
        declare_returned_contributions(self.contract)
        for worker in self.contract["roster"]["workers"]:
            worker["status"] = "completed"
        self.contract["roster"]["activeAgentCount"] = 1
        self.refresh()

    def test_valid_distinct_critic_and_executor_are_admitted(self):
        self.assertTrue(self.admit()["admitted"])

    def test_pending_template_never_implies_solo_or_admitted_mode(self):
        pending = pending_contract("GB")
        self.assertIsNone(pending["selection"]["mode"])
        self.assertEqual(pending["selection"]["delegation"]["policy"], "required")
        self.assertEqual(pending["selection"]["delegation"]["assignments"], [])
        self.data["workflowContract"] = pending
        with self.assertRaises(ValueError):
            self.admit()

    def test_auto_is_not_an_admitted_concrete_mode(self):
        self.contract["selection"]["mode"] = "auto"
        with self.assertRaisesRegex(ValueError, "Auto is only a selector"):
            self.admit()

    def test_no_solo_policy_even_for_trivial_or_user_requested_solo(self):
        for reason in ("The task is trivial", "The user requested solo"):
            self.contract["selection"]["delegation"].update(policy="solo", reason=reason)
            with self.assertRaisesRegex(ValueError, "no solo waiver"):
                self.admit()

    def test_zero_workers_profiles_and_planned_roles_cannot_count_as_dispatch(self):
        self.contract["roster"].update(workers=[], profiles=[], activeAgentCount=1,
            plannedWorkers=[{"role": "executor", "phaseIds": ["execute"]}])
        with self.assertRaisesRegex(ValueError, "actual actors"):
            self.admit()

    def test_coordinator_owned_implementation_does_not_satisfy_worker_assignment(self):
        self.state("execute")["ownerId"] = "fixture:coordinator"
        self.state("execute")["authorIds"] = ["fixture:coordinator"]
        self.refresh()
        with self.assertRaisesRegex(ValueError, "actual assigned workers"):
            self.admit()

    def test_profile_on_wrong_agent_cannot_satisfy_required_worker(self):
        self.contract["roster"]["profiles"] = [row for row in self.contract["roster"]["profiles"] if row["ownerId"] != "fixture:executor"]
        self.refresh()
        with self.assertRaisesRegex(ValueError, "apply the assigned bundled profile"):
            self.admit()

    def test_critic_cannot_be_execution_worker(self):
        self.state("execute")["ownerId"] = "fixture:critic"
        self.state("execute")["authorIds"] = ["fixture:critic"]
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "execute")["workerId"] = "fixture:critic"
        self.contract["roster"]["workers"][0]["status"] = "running"
        self.contract["roster"]["workers"][1]["status"] = "completed"
        self.contract["roster"]["profiles"].append({"ownerId": "fixture:critic", "name": self.contract["selection"]["delegation"]["assignments"][1]["profile"]})
        self.refresh()
        with self.assertRaisesRegex(ValueError, "independent duty shares|cannot provide independent criticism"):
            self.admit()

    def test_completed_or_failed_worker_cannot_own_in_progress_implementation(self):
        for status in ("completed", "failed"):
            self.contract["roster"]["workers"][1]["status"] = status
            self.contract["roster"]["activeAgentCount"] = 1
            self.refresh()
            with self.assertRaisesRegex(ValueError, "in-progress phase cannot be owned"):
                self.admit()

    def test_nominal_duplicate_or_planned_lifecycle_is_rejected(self):
        self.contract["roster"]["workers"].append(copy.deepcopy(self.contract["roster"]["workers"][0]))
        with self.assertRaisesRegex(ValueError, "distinct nonblank IDs"):
            self.admit()
        self.contract["roster"]["workers"].pop()
        self.contract["roster"]["workers"][1]["status"] = "planned"
        with self.assertRaisesRegex(ValueError, "actual running/completed/failed agents"):
            self.admit()

    def test_removing_worker_assignments_cannot_leave_valid_self_execution(self):
        self.contract["selection"]["delegation"]["assignments"] = []
        with self.assertRaisesRegex(ValueError, "at least two useful worker assignments"):
            self.admit()

    def test_complete_claim_requires_independent_acceptance(self):
        self.data["status"] = "complete"
        with self.assertRaisesRegex(ValueError, "completion requires every selected non-report phase"):
            self.admit()

    def test_sequential_completed_workers_remain_valid_with_one_active_coordinator(self):
        self.complete_implementation()
        self.data["status"] = "complete"
        self.assertTrue(self.admit()["admitted"])
        self.assertEqual(self.contract["roster"]["activeAgentCount"], 1)

    def test_same_executor_cannot_accept_its_result(self):
        self.complete_implementation()
        self.state("accept")["ownerId"] = "fixture:executor"
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "accept")["workerId"] = "fixture:executor"
        self.contract["roster"]["profiles"].append({"name": "agents/code-reviewer/agent.md", "ownerId": "fixture:executor"})
        self.refresh()
        with self.assertRaisesRegex(ValueError, "required independent duty shares"):
            self.admit()

    def test_policy_changes_invalidate_exact_review_binding(self):
        for field, value in (("mode", "loop"), ("originMode", "auto")):
            old = copy.deepcopy(self.contract["selection"])
            self.contract["selection"][field] = value
            with self.assertRaisesRegex(ValueError, "criticism does not cover the exact"):
                self.admit()
            self.contract["selection"] = old
        self.contract["selection"]["routing"]["reason"] += " New affected behavior discovered."
        with self.assertRaisesRegex(ValueError, "criticism does not cover the exact"):
            self.admit()

    def test_unknown_impact_cannot_admit_implementation(self):
        self.contract["selection"]["routing"] = decision(impact="unknown")["routing"]
        with self.assertRaisesRegex(ValueError, "unknown impact must be assessed"):
            self.admit()

    def test_architect_is_actual_complete_and_before_final_plan(self):
        self.architecture()
        self.assertTrue(self.admit()["admitted"])
        self.state("architecture")["ownerId"] = "fixture:coordinator"
        self.state("architecture")["authorIds"] = ["fixture:coordinator", "fixture:architect"]
        self.refresh()
        with self.assertRaisesRegex(ValueError, "actual assigned workers"):
            self.admit()

    def test_architect_name_or_future_assignment_cannot_replace_advice(self):
        self.architecture()
        self.state("architecture").update(status="pending", ownerId=None, evidence=[], workHash=None)
        with self.assertRaisesRegex(ValueError, "incomplete prerequisite"):
            self.admit()

    def test_architect_must_be_plan_dependency(self):
        self.architecture()
        next(row for row in self.contract["selection"]["phases"] if row["id"] == "plan")["dependsOn"] = ["scope"]
        with self.assertRaisesRegex(ValueError, "Architect advice must be a prerequisite"):
            self.admit()

    def test_small_build_requires_fast_executor_profile(self):
        self.contract["selection"]["routing"] = decision()["routing"]
        with self.assertRaisesRegex(ValueError, "require the complete Fast Builder"):
            self.admit()
        self.contract["selection"]["delegation"]["assignments"][1]["profile"] = FAST_ENGINEER
        self.contract["roster"]["profiles"].append({"name": FAST_ENGINEER, "ownerId": "fixture:executor"})
        self.refresh()
        self.assertTrue(self.admit()["admitted"])

    def test_coordinator_integration_is_covered_by_independent_acceptance(self):
        selected = self.contract["selection"]
        selected["phases"].insert(4, {"id": "integrate", "title": "Integrate specialist results", "kind": "execute",
            "operation": "integrate-reviewed-source", "writeScope": "repo-write-scoped",
            "owner": "coordinator", "dependsOn": ["execute"]})
        next(row for row in selected["phases"] if row["id"] == "verify")["dependsOn"] = ["integrate"]
        selected["delegation"]["assignments"][2]["independentFrom"].append("integrate")
        self.contract["progress"]["phases"].insert(4, {"id": "integrate", "status": "pending", "ownerId": None,
            "authorIds": [], "evidence": [], "workHash": None})
        self.refresh()
        self.assertTrue(self.admit()["admitted"])
        self.state("execute").update(status="complete", evidence=["fixture:specialist-result"])
        self.state("integrate").update(status="in-progress", ownerId="fixture:coordinator", authorIds=["fixture:coordinator"])
        declare_returned_contributions(self.contract)
        self.contract["progress"]["currentPhase"] = "integrate"
        self.refresh()
        self.assertTrue(self.admit()["admitted"])

    def test_external_only_publication_can_follow_real_preparation_and_acceptance(self):
        baseline = copy.deepcopy(self.data)
        for impact in ("standard", "small-localized"):
            with self.subTest(impact=impact):
                self.data = copy.deepcopy(baseline)
                self.contract = self.data["workflowContract"]
                selected = self.contract["selection"]
                selected["routing"] = decision(impact=impact)["routing"]
                preparation = next(row for row in selected["phases"] if row["id"] == "execute")
                preparation.update(kind="other", operation="inspect-prepared-publication-artifact", writeScope="read-only")
                if impact == "small-localized":
                    selected["delegation"]["assignments"][1]["profile"] = FAST_ENGINEER
                    self.contract["roster"]["profiles"].append({"name": FAST_ENGINEER, "ownerId": "fixture:executor"})
                selected["phases"].append({"id": "publish", "title": "Publish accepted artifact", "kind": "execute",
                    "operation": "publish-prepared-artifact", "writeScope": "external-write", "owner": "coordinator", "dependsOn": ["accept"]})
                self.contract["progress"]["phases"].append({"id": "publish", "status": "pending", "ownerId": None,
                    "authorIds": [], "evidence": [], "workHash": None})
                self.complete_implementation()
                self.state("publish").update(status="in-progress", ownerId="fixture:coordinator")
                self.contract["progress"]["currentPhase"] = "publish"
                self.refresh()
                self.assertTrue(self.admit()["admitted"])
                self.state("publish").update(status="complete", evidence=["fixture:publication-result"])
                self.data["status"] = "complete"
                self.refresh()
                self.assertTrue(self.admit()["admitted"])
                next(row for row in selected["phases"] if row["id"] == "publish")["dependsOn"] = ["execute"]
                with self.assertRaisesRegex(ValueError, "acceptance before every external write"):
                    self.admit()

    def test_mixed_build_and_publication_cannot_publish_before_independent_acceptance(self):
        selected = self.contract["selection"]
        selected["phases"].insert(4, {"id": "publish", "title": "Publish the implementation", "kind": "execute",
            "operation": "publish-current-result", "writeScope": "external-write", "owner": "coordinator", "dependsOn": ["execute"]})
        self.contract["progress"]["phases"].insert(4, {"id": "publish", "status": "in-progress", "ownerId": "fixture:coordinator",
            "authorIds": [], "evidence": [], "workHash": None})
        self.state("execute").update(status="complete", evidence=["fixture:execution-result"])
        self.contract["progress"]["currentPhase"] = "publish"
        with self.assertRaisesRegex(ValueError, "acceptance before every external write"):
            self.admit()
        publication = selected["phases"].pop(4)
        publication["dependsOn"] = ["accept"]
        selected["phases"].append(publication)
        self.complete_implementation()
        self.contract["progress"]["currentPhase"] = "publish"
        self.refresh()
        self.assertTrue(self.admit()["admitted"])

    def test_read_only_unknown_impact_requires_two_useful_contributors_at_completion(self):
        self.contract = make_readonly_contract(self.record, self.data, "review", complete=True)
        self.contract["selection"]["routing"] = decision("review", impact="unknown", changedSharedContract=None)["routing"]
        self.refresh()
        self.assertFalse(self.admit(require_product_write=False, completing=True)["admitted"])
        self.contract["contributions"] = [row for row in self.contract["contributions"] if row["workerId"] != "fixture:executor"]
        self.refresh()
        with self.assertRaisesRegex(ValueError, "lacks a useful current contribution"):
            self.admit(require_product_write=False, completing=True)

    def test_mechanical_ui_requires_full_expertise_and_rendered_acceptance(self):
        selected = self.contract["selection"]
        selected["uiContext"] = {"applicable": True, "kind": "mechanical", "reason": "The fixture applies an existing label to an existing rendered component."}
        with self.assertRaisesRegex(ValueError, "complete UI expertise"):
            self.admit()
        selected["delegation"]["assignments"][1]["capabilities"].append("ui-design")
        selected["delegation"]["assignments"][2]["capabilities"].append("ui-design")
        with self.assertRaisesRegex(ValueError, "rendered-result acceptance"):
            self.admit()
        selected["delegation"]["assignments"][2]["capabilities"].append("review-ui")
        self.refresh()
        self.assertTrue(self.admit()["admitted"])


if __name__ == "__main__":
    unittest.main()
