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

def fixture(root, suffix="first"):
    record = root / "documents/tasks/development" / ("2026-09-07-00001-" + suffix)
    record.mkdir(parents=True)
    for name in FILES:
        (record / name).write_text("# " + name + "\n\nActual plan content.\n")
    data = {
        "schema": "project-development-plan/v1", "contractVersion": 2,
        "projectRoot": str(root.resolve()), "recordPath": str(record.relative_to(root)),
        "status": "planned", "readiness": "ready", "blockers": [],
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
        for stage in ("planned", "criticized"):
            if stage == "criticized":
                self.data["critiqueOutcome"] = "revised"
                self.data["planRevision"] = 2
                write(self.record, self.data)
            result = subprocess.run([sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                                     "--project-root", str(self.root), "--record", str(self.record),
                                     "--stage", stage], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.record, self.data = load_record(self.root, self.record)
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
        result = subprocess.run([sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
                                 "--project-root", str(self.root), "--record", str(self.record),
                                 "--stage", "planned", "--resume"], capture_output=True, text=True)
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
        self.data["critiqueOutcome"] = "revised"
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
