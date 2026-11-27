import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from plan_record import FILES, PLAN_FILES, digest, definition_hash, gate, load_record, select, request_hashes
from workflow_contract import (
    briefing_binding, pending_contract, render_briefing, review_binding,
    selection as contract_selection,
)
from contract_fixture import (declare_discovery, declare_policy, declare_review, refresh_contract,
                              normalize_fixture_assignments, make_readonly_contract)
from task_policy import ASSESSOR, EXECUTOR

def fixture(root, suffix="first", *, reviewed=True):
    record = root / "documents/tasks/development" / ("2026-09-07-00001-" + suffix)
    record.mkdir(parents=True)
    for name in FILES:
        (record / name).write_text("# " + name + "\n\nActual plan content.\n")
    data = {
        "schema": "project-development-plan/v1", "contractVersion": 2,
        "projectRoot": str(root.resolve()), "recordPath": str(record.relative_to(root)),
        "status": "planned", "readiness": "not_ready", "blockers": [],
        "planRevision": 1, "critiqueOutcome": "not_requested",
        "sourceBaseline": {"description": "Inspected fixture source"},
        "scope": {"in": ["Fix requested behavior"], "out": ["Deployment"]},
        "requestSources": [{"id": "S1", "role": "user", "origin": "Fixture user message",
                            "text": "Keep requester identity"}],
        "requirements": [{"id": "R1", "text": "Keep requester identity", "sources": ["S1"], "kind": "requested"}],
        "steps": [{"id": "P1", "requirements": ["R1"], "paths": ["app/dispatch.py"],
                   "change": "Preserve identity", "dependsOn": []}],
        "checks": [{"id": "T1", "requirements": ["R1"], "method": "Two requesters",
                    "expected": "Separate identities", "boundary": "Fixture only"}],
        "planHashes": {name: digest(record / name) for name in PLAN_FILES},
    }
    data["requestHashes"] = request_hashes(data)
    data["definitionHash"] = definition_hash(data)
    data["workflowContract"] = pending_contract()
    if reviewed:
        declare_review(record, data)
    write(record, data)
    return record, data

def write(record, data):
    (record / "record.json").write_text(json.dumps(data))

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record, self.data = fixture(self.root)

    def test_ready_plan(self):
        self.assertTrue(gate(*select(self.root), self.root))

    def test_missing_criticism_blocks_execution(self):
        self.data["critiqueOutcome"] = "not_requested"
        with self.assertRaisesRegex(ValueError, "every execution requires current criticism"):
            gate(self.record, self.data, self.root)

    def test_false_compatibility_flag_cannot_waive_criticism(self):
        self.data["critiqueOutcome"] = "not_requested"
        with self.assertRaisesRegex(ValueError, "every execution requires current criticism"):
            gate(self.record, self.data, self.root, require_critique=False)

    def test_incomplete_contract_review_blocks_legacy_ready_flag(self):
        self.data["workflowContract"]["review"]["status"] = "pending"
        with self.assertRaisesRegex(ValueError, "current criticism is incomplete or blocked"):
            gate(self.record, self.data, self.root)

    def test_missing_briefing_blocks_execution(self):
        self.data["workflowContract"]["briefing"]["status"] = "pending"
        with self.assertRaisesRegex(ValueError, "public briefing declaration is missing"):
            gate(self.record, self.data, self.root)

    def test_new_pending_contract_declares_current_discovery_fields(self):
        selected = pending_contract()["selection"]
        self.assertEqual(selected["selectionSchema"], "ai-development-workflow/selection-v2")
        self.assertEqual(selected["discovery"]["schema"], "ai-development-workflow/discovery-v1")
        self.assertEqual(selected["discovery"]["initialQuery"], "")

    def test_executor_cli_rejects_missing_or_stale_discovery(self):
        script = SCRIPTS / "resolve_plan_record.py"
        for defect in ("missing", "stale"):
            with self.subTest(defect=defect):
                data = copy.deepcopy(self.data)
                selected = data["workflowContract"]["selection"]
                if defect == "missing":
                    selected.pop("selectionSchema")
                    selected.pop("discovery")
                else:
                    selected["discovery"]["indexFingerprint"] = "stale"
                write(self.record, data)
                result = subprocess.run(
                    [sys.executable, str(script), "--project-root", str(self.root),
                     "--record", str(self.record), "--execution"],
                    capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("discovery", result.stderr)

    def test_discovery_is_bound_to_the_completed_review(self):
        declare_discovery(self.data["workflowContract"], "Review a different current workflow route")
        with self.assertRaisesRegex(ValueError, "criticism does not cover"):
            gate(self.record, self.data, self.root)

    def test_loop_and_xr_require_independent_criticism_even_with_self_permitted_policy(self):
        for value in ("loop", "LOOP", "XR", "xr", "mode:loop", "MODE:XR", " loop ",
                      "ai-dev-loop", "ai-dev-execute-review", "mode:ai-dev-loop"):
            with self.subTest(workflow=value):
                data = copy.deepcopy(self.data)
                contract = data["workflowContract"]
                contract["selection"].update(workflow=value, mode="loop", reviewPolicy="self-permitted")
                with self.assertRaisesRegex(ValueError, "writing work requires independent criticism"):
                    gate(self.record, data, self.root)

    def test_loop_accepts_a_current_synthetic_independent_review_declaration(self):
        contract = self.data["workflowContract"]
        contract["selection"].update(workflow="loop", mode="loop")
        refresh_contract(self.record, self.data)
        self.assertTrue(gate(self.record, self.data, self.root))

    def test_plan_and_review_contracts_reject_every_product_write_scope_in_any_late_phase(self):
        for field in ("workflow", "mode"):
            for value in ("plan", "review", "mode:plan", "MODE:REVIEW"):
                for phase_id in ("execute", "verify"):
                    for write_scope in ("repo-write-scoped", "tests-only", "docs-only", "external-write"):
                        with self.subTest(field=field, value=value, phase=phase_id, scope=write_scope):
                            contract = copy.deepcopy(self.data["workflowContract"])
                            for phase in contract["selection"]["phases"]:
                                if phase["id"] in {"execute", "verify"}:
                                    phase["writeScope"] = write_scope if phase["id"] == phase_id else "record-only"
                            # Delegate whichever source writer this case selects.
                            assignments = contract["selection"]["delegation"]["assignments"]
                            for assignment in assignments:
                                if assignment["phaseId"] == "execute":
                                    assignment["phaseId"] = phase_id
                                    if write_scope == "docs-only":
                                        assignment["capabilities"].append("update-docs")
                                elif assignment["phaseId"] == "accept":
                                    assignment["independentFrom"] = ["plan", phase_id]
                            if write_scope == "external-write":
                                # A legal publication has delegated preparation
                                # and independent acceptance before its writer.
                                selected = contract["selection"]
                                selected["phases"] = selected["phases"][:3] + [
                                    {"id": "prepare", "title": "Inspect artifact", "kind": "other",
                                     "operation": "inspect-prepared-artifact", "writeScope": "read-only",
                                     "owner": "specialist", "dependsOn": ["critique"]},
                                    {"id": "accept", "title": "Accept artifact", "kind": "verify",
                                     "operation": "accept-prepared-artifact", "writeScope": "read-only",
                                     "owner": "independent reviewer", "dependsOn": ["prepare"]},
                                    {"id": phase_id, "title": "Publish", "kind": "execute",
                                     "operation": "publish-accepted-artifact", "writeScope": write_scope,
                                     "owner": "coordinator", "dependsOn": ["accept"]},
                                ]
                                selected["delegation"]["assignments"] = [assignments[0],
                                    {"phaseId": "prepare", "profile": EXECUTOR, "independentFrom": []},
                                    {"phaseId": "accept", "profile": "agents/code-reviewer/agent.md", "independentFrom": ["plan", "prepare"]},
                                ]
                            normalize_fixture_assignments(contract)
                            contract_selection(contract)
                            contract["selection"][field] = value
                            with self.assertRaisesRegex(ValueError, "Plan and Review modes cannot authorize product writes"):
                                contract_selection(contract)
                            if write_scope == "repo-write-scoped":
                                data = {**self.data, "workflowContract": contract}
                                with self.assertRaisesRegex(ValueError, "Plan and Review modes cannot authorize product writes"):
                                    gate(self.record, data, self.root)

    def test_record_only_plan_and_review_contract_selections_remain_valid(self):
        for field in ("workflow", "mode"):
            for value in ("plan", "review", "mode:plan", "MODE:REVIEW"):
                with self.subTest(field=field, value=value):
                    data = copy.deepcopy(self.data)
                    concrete_mode = value.lower().removeprefix("mode:")
                    contract = make_readonly_contract(self.record, data, concrete_mode)
                    contract["selection"][field] = value if field == "workflow" else concrete_mode
                    actual, phases = contract_selection(contract)
                    self.assertEqual(actual[field], value if field == "workflow" else concrete_mode)
                    self.assertTrue({"scope", "plan", "critique", "report"} <= set(phases))
                    self.assertEqual({phase["writeScope"] for phase in phases.values()}, {"record-only"})

    def test_metadata_edit_invalidates_readiness(self):
        self.data["steps"][0]["change"] = "A different change"
        with self.assertRaisesRegex(ValueError, "metadata changed"):
            gate(self.record, self.data, self.root)

    def test_relative_record_uses_project_not_cwd(self):
        self.assertEqual(select(self.root, str(self.record.relative_to(self.root)))[0], self.record)

    def test_two_active_records_are_ambiguous(self):
        fixture(self.root, "second")
        with self.assertRaisesRegex(ValueError, "multiple active"):
            select(self.root)

    def test_blocked_explicit_cannot_bypass_gate(self):
        self.data["blockers"] = ["Missing credentials"]
        write(self.record, self.data)
        with self.assertRaisesRegex(ValueError, "blockers"):
            gate(*select(self.root, self.record), self.root)

    def test_does_not_skip_newer_blocked_record(self):
        record, data = fixture(self.root, "second")
        data["status"] = "blocked"
        write(record, data)
        with self.assertRaisesRegex(ValueError, "multiple active"):
            select(self.root)

    def test_missing_file_rejected(self):
        (self.record / "test-plan.md").unlink()
        with self.assertRaisesRegex(ValueError, "test-plan.md"):
            select(self.root)

    def test_malformed_metadata_rejected(self):
        (self.record / "record.json").write_text("[]")
        with self.assertRaisesRegex(ValueError, "incompatible"):
            select(self.root)

    def test_missing_requirement_coverage(self):
        self.data["requirements"].append({"id": "R2", "text": "Second outcome"})
        with self.assertRaisesRegex(ValueError, "unmapped"):
            gate(self.record, self.data, self.root)

    def test_dependency_cycle(self):
        self.data["steps"][0]["dependsOn"] = ["P1"]
        with self.assertRaisesRegex(ValueError, "cycle"):
            gate(self.record, self.data, self.root)

    def test_unknown_dependency(self):
        self.data["steps"][0]["dependsOn"] = ["P99"]
        with self.assertRaisesRegex(ValueError, "unknown"):
            gate(self.record, self.data, self.root)

    def test_plan_edit_invalidates_readiness(self):
        (self.record / "fix-plan.md").write_text("Changed the implementation")
        with self.assertRaisesRegex(ValueError, "plan changed"):
            gate(self.record, self.data, self.root)

    def test_review_revision_must_match(self):
        self.data.update(critiqueOutcome="ready", reviewedPlanRevision=0)
        with self.assertRaisesRegex(ValueError, "different plan revision"):
            gate(self.record, self.data, self.root)

    def test_review_edit_invalidates_readiness(self):
        self.data.update(critiqueOutcome="ready", reviewedPlanRevision=1,
                         critiqueHash=digest(self.record / "critique.md"))
        (self.record / "critique.md").write_text("New blocking finding")
        with self.assertRaisesRegex(ValueError, "critique changed"):
            gate(self.record, self.data, self.root)

    def test_legacy_readable_but_not_executable(self):
        self.data.pop("contractVersion")
        write(self.record, self.data)
        self.assertEqual(select(self.root)[1]["schema"], "project-development-plan/v1")
        with self.assertRaisesRegex(ValueError, "legacy"):
            gate(*select(self.root), self.root)

    def test_resume_explicitly_required(self):
        self.data["status"] = "executing"
        with self.assertRaisesRegex(ValueError, "resume"):
            gate(self.record, self.data, self.root)
        self.assertTrue(gate(self.record, self.data, self.root, resume=True))

    def test_root_mismatch(self):
        self.data["projectRoot"] = "/unrelated"
        with self.assertRaisesRegex(ValueError, "projectRoot"):
            gate(self.record, self.data, self.root)

    def test_symlink_document_rejected(self):
        target = self.root / "outside.md"
        target.write_text("outside")
        (self.record / "fix-plan.md").unlink()
        (self.record / "fix-plan.md").symlink_to(target)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            select(self.root)

    def test_record_outside_project_rejected(self):
        with tempfile.TemporaryDirectory() as other:
            record, _ = fixture(Path(other))
            with self.assertRaisesRegex(ValueError, "direct dated child"):
                select(self.root, record)

    def test_finalize_rejects_blockers_without_overwriting(self):
        self.data["blockers"] = ["Unresolved"]
        write(self.record, self.data)
        before = (self.record / "record.json").read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                                 "--project-root", str(self.root), "--record", str(self.record),
                                 "--stage", "planned"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.record / "record.json").read_bytes(), before)

    def test_finalize_then_criticize_then_execute(self):
        self.record, self.data = fixture(self.root, "unreviewed", reviewed=False)
        for stage in ("planned", "criticized"):
            if stage == "criticized":
                self.data["planRevision"] = 2
                declare_review(self.record, self.data, outcome="revised", finalized=False)
                write(self.record, self.data)
            result = subprocess.run([sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                                     "--project-root", str(self.root), "--record", str(self.record),
                                     "--stage", stage], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.record, self.data = load_record(self.root, self.record)
            self.assertFalse(json.loads(result.stdout)["executionAdmitted"])
            if stage == "planned":
                self.assertEqual(self.data["readiness"], "not_ready")
                with self.assertRaisesRegex(ValueError, "current criticism"):
                    gate(self.record, self.data, self.root)
            else:
                self.assertEqual(self.data["reviewedPlanRevision"], 2)
                self.assertTrue(gate(self.record, self.data, self.root))


    def test_invalid_collection_types_fail_cleanly(self):
        self.data["scope"] = {"in": True, "out": 42}
        with self.assertRaisesRegex(ValueError, "scope"):
            gate(self.record, self.data, self.root)
        self.data["scope"] = {"in": ["work"], "out": ["deploy"]}
        self.data["planHashes"] = []
        with self.assertRaisesRegex(ValueError, "planHashes"):
            gate(self.record, self.data, self.root)

    def test_resume_review_preserves_interrupted_status(self):
        self.data["status"] = "blocked"
        self.data["readiness"] = "blocked"
        write(self.record, self.data)
        (self.record / "checklist.md").write_text("# Checklist\n- [x] Verified first outcome\n")
        command = [sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                   "--project-root", str(self.root), "--record", str(self.record)]
        before = (self.record / "record.json").read_bytes()
        stale = subprocess.run(command + ["--stage", "planned", "--resume"],
                               capture_output=True, text=True)
        self.assertEqual(stale.returncode, 2)
        self.assertIn("fresh critique", stale.stdout)
        self.assertEqual((self.record / "record.json").read_bytes(), before)
        self.data["planRevision"] += 1
        declare_review(self.record, self.data, outcome="revised", finalized=False)
        write(self.record, self.data)
        result = subprocess.run(command + ["--stage", "criticized", "--resume"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record, data = select(self.root, self.record)
        self.assertEqual(data["status"], "blocked")
        self.assertTrue(gate(record, data, self.root, resume=True))

    def test_executor_cli_rejects_explicit_blocker(self):
        script = SCRIPTS / "resolve_plan_record.py"
        if not script.exists():
            script = SCRIPTS / "plan_record.py"
        self.data["blockers"] = ["No source evidence"]
        write(self.record, self.data)
        result = subprocess.run([sys.executable, str(script), "--project-root", str(self.root),
                                 "--record", str(self.record), "--execution"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("blockers", result.stderr)

    def test_completed_record_reopens_in_place_after_fresh_review(self):
        self.data.update(status="complete", critiqueOutcome="ready", reviewedPlanRevision=1,
                         critiqueHash=digest(self.record / "critique.md"), createdAt="2026-09-07T12:00:00Z")
        write(self.record, self.data)
        history = (self.record / "results.md").read_bytes()
        with self.assertRaisesRegex(ValueError, "status not eligible"):
            gate(self.record, self.data, self.root)
        self.data.update(status="planned", readiness="not_ready", planRevision=2)
        write(self.record, self.data)
        command = [sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                   "--project-root", str(self.root), "--record", str(self.record), "--stage"]
        stale = subprocess.run(command + ["planned"], capture_output=True, text=True)
        self.assertEqual(stale.returncode, 2)
        self.assertIn("fresh critique", stale.stdout)
        declare_review(self.record, self.data, outcome="revised", finalized=False)
        write(self.record, self.data)
        reviewed = subprocess.run(command + ["criticized"], capture_output=True, text=True)
        self.assertEqual(reviewed.returncode, 0, reviewed.stdout + reviewed.stderr)
        record, data = load_record(self.root, self.record)
        self.assertEqual(record, self.record)
        self.assertEqual(data["createdAt"], "2026-09-07T12:00:00Z")
        self.assertEqual(data["planRevision"], 2)
        self.assertEqual(data["reviewedPlanRevision"], 2)
        self.assertEqual((record / "results.md").read_bytes(), history)
        self.assertTrue(gate(record, data, self.root))

if __name__ == "__main__":
    unittest.main()
