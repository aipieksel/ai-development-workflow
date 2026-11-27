"""Real finalizer CLI regressions using explicitly synthetic review declarations.

These tests distinguish completed criticism from permission to mutate product
files. Fixture actors, inspection claims and public-message receipts are never
presented as real work; only disposable test records are finalized.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from contract_fixture import declare_policy, declare_review, refresh_contract, make_readonly_contract
from task_policy import ASSESSOR, PLANNER
from plan_record import gate, load_record
from test_contract import fixture, write
from workflow_contract import (
    briefing_binding, canonical_hash, render_briefing, review_binding, validate_contract,
)


class ReviewFinalizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def make_record(self, mode, suffix=None):
        record, data = fixture(self.root, suffix or mode, reviewed=False)
        declare_review(record, data, finalized=False)
        contract = data["workflowContract"]
        selected = contract["selection"]
        selected.update(workflow=mode, mode=mode, reason="Exercise the " + mode + " finalization boundary on a synthetic record.")
        if mode in {"plan", "review"}:
            make_readonly_contract(record, data, mode)
        refresh_contract(record, data)
        write(record, data)
        return record, data

    def cli(self, script, record, *arguments):
        environment = os.environ.copy()
        environment.update(PYTHONDONTWRITEBYTECODE="1", AIDW_LOG="off")
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / script), "--project-root", str(self.root),
             "--record", str(record), *arguments],
            env=environment, capture_output=True, text=True, timeout=15,
        )

    def finalize(self, record):
        return self.cli("finalize_plan_record.py", record, "--stage", "criticized")

    @staticmethod
    def record_bytes(record):
        return {path.relative_to(record).as_posix(): path.read_bytes()
                for path in record.rglob("*") if path.is_file()}

    def test_plan_and_review_criticism_finalize_without_admitting_execution(self):
        for mode in ("plan", "review"):
            with self.subTest(mode=mode):
                record, _ = self.make_record(mode)
                outcome = self.finalize(record)
                self.assertEqual(outcome.returncode, 0, outcome.stdout + outcome.stderr)
                result = json.loads(outcome.stdout)
                self.assertEqual((result["status"], result["readiness"]), ("criticized", "not_ready"))
                self.assertTrue(result["reviewValidated"])
                self.assertFalse(result["executionAdmitted"])
                _, saved = load_record(self.root, record)
                self.assertEqual((saved["status"], saved["readiness"]), ("criticized", "not_ready"))
                self.assertEqual(saved["reviewedPlanRevision"], saved["planRevision"])
                self.assertTrue(gate(record, saved, self.root, review_only=True))
                reviewed = validate_contract(record, saved, require_product_write=False)
                self.assertTrue(reviewed["reviewValidated"])
                self.assertFalse(reviewed["admitted"])
                with self.assertRaisesRegex(ValueError, "planning alone is not execution-ready"):
                    gate(record, saved, self.root)
                with self.assertRaisesRegex(ValueError, "no product mutation operation selected"):
                    validate_contract(record, saved)
                execution = self.cli("resolve_plan_record.py", record, "--execution")
                self.assertEqual(execution.returncode, 2, execution.stdout + execution.stderr)
                self.assertIn("planning alone is not execution-ready", execution.stderr)

    def test_a_forged_ready_flag_cannot_turn_record_only_criticism_into_execution(self):
        for mode in ("plan", "review"):
            with self.subTest(mode=mode):
                record, _ = self.make_record(mode)
                outcome = self.finalize(record)
                self.assertEqual(outcome.returncode, 0, outcome.stdout + outcome.stderr)
                _, saved = load_record(self.root, record)
                saved["readiness"] = "ready"
                write(record, saved)
                before = self.record_bytes(record)
                with self.assertRaisesRegex(ValueError, "no product mutation operation selected"):
                    gate(record, saved, self.root)
                execution = self.cli("resolve_plan_record.py", record, "--execution")
                self.assertEqual(execution.returncode, 2, execution.stdout + execution.stderr)
                self.assertIn("no product mutation operation selected", execution.stderr)
                self.assertEqual(self.record_bytes(record), before)

    def test_record_only_finalization_rejects_missing_or_stale_review_and_briefing_without_writes(self):
        cases = (
            ("missing-critique-file", "critique.md"),
            ("missing-critique-outcome", "record the actual critique outcome"),
            ("incomplete-criticism", "current criticism is incomplete or blocked"),
            ("stale-review-binding", "criticism does not cover the exact current plan/source/operations"),
            ("changed-plan-file", "criticism does not cover the exact current plan/source/operations"),
            ("missing-briefing", "public briefing declaration is missing"),
            ("stale-briefing-binding", "briefing is stale"),
            ("stale-briefing-text", "briefing text must contain the current complete required block"),
        )
        for mode in ("plan", "review"):
            for case, message in cases:
                with self.subTest(mode=mode, case=case):
                    record, data = self.make_record(mode, mode + "-" + case)
                    contract = data["workflowContract"]
                    if case == "missing-critique-file":
                        (record / "critique.md").unlink()
                    elif case == "missing-critique-outcome":
                        data["critiqueOutcome"] = "not_requested"
                    elif case == "incomplete-criticism":
                        contract["review"]["status"] = "pending"
                    elif case == "stale-review-binding":
                        contract["review"]["binding"]["planRevision"] = 0
                    elif case == "changed-plan-file":
                        plan = record / "fix-plan.md"
                        plan.write_text(plan.read_text() + "\nUnreviewed fixture change.\n")
                    elif case == "missing-briefing":
                        contract["briefing"]["status"] = "pending"
                    elif case == "stale-briefing-binding":
                        contract["briefing"]["binding"]["scopeHash"] = "0" * 64
                    elif case == "stale-briefing-text":
                        contract["briefing"]["text"] = "Synthetic stale briefing without the selected phases."
                    write(record, data)
                    before = self.record_bytes(record)
                    outcome = self.finalize(record)
                    self.assertEqual(outcome.returncode, 2, outcome.stdout + outcome.stderr)
                    self.assertIn(message, outcome.stdout + outcome.stderr)
                    self.assertEqual(self.record_bytes(record), before,
                                     "Failed finalization must preserve every saved record byte and file")

    def test_planning_and_review_only_flags_are_mutually_exclusive(self):
        record, data = fixture(self.root, "conflicting-flags")
        before = self.record_bytes(record)
        with self.assertRaisesRegex(ValueError, "planning and review-only validation are distinct stages"):
            gate(record, data, self.root, planning=True, review_only=True)
        self.assertEqual(self.record_bytes(record), before)

    def test_build_finalization_retains_explicit_execution_admission(self):
        record, _ = self.make_record("build")
        outcome = self.finalize(record)
        self.assertEqual(outcome.returncode, 0, outcome.stdout + outcome.stderr)
        result = json.loads(outcome.stdout)
        self.assertEqual((result["status"], result["readiness"]), ("criticized", "ready"))
        self.assertTrue(result["reviewValidated"])
        self.assertFalse(result["executionAdmitted"])
        _, saved = load_record(self.root, record)
        reviewed = validate_contract(record, saved, require_product_write=False)
        self.assertTrue(reviewed["reviewValidated"])
        self.assertFalse(reviewed["admitted"])
        self.assertTrue(validate_contract(record, saved)["admitted"])
        self.assertTrue(gate(record, saved, self.root))
        execution = self.cli("resolve_plan_record.py", record, "--execution")
        self.assertEqual(execution.returncode, 0, execution.stdout + execution.stderr)
        self.assertTrue(json.loads(execution.stdout)["executionAdmitted"])


if __name__ == "__main__":
    unittest.main()
