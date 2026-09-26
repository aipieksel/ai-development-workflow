import copy
import json
import subprocess
import sys
import unittest

import test_contract
from test_contract import SCRIPTS, write
from plan_record import definition_hash, gate, request_hashes


class ScopeProvenanceTests(unittest.TestCase):
    setUp = test_contract.ContractTests.setUp

    def finalize(self):
        write(self.record, self.data)
        before = (self.record / "record.json").read_bytes()
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "finalize_plan_record.py"),
             "--project-root", str(self.root), "--record", str(self.record), "--stage", "planned"],
            capture_output=True, text=True,
        )
        return result, before

    def test_missing_provenance_readiness_rejected(self):
        self.data.pop("requestSources")
        with self.assertRaisesRegex(ValueError, "requestSources missing"):
            gate(self.record, self.data, self.root)

    def test_unknown_source_rejected(self):
        self.data["requirements"][0]["sources"] = ["S99"]
        with self.assertRaisesRegex(ValueError, "source references"):
            gate(self.record, self.data, self.root)

    def test_context_cannot_become_user_authority(self):
        self.data["requestSources"].append({"id": "C1", "role": "context", "origin": "Agent suggestion", "text": "Build identity platform"})
        self.data["requirements"][0]["sources"] = ["C1"]
        self.data["requestHashes"] = request_hashes(self.data)
        with self.assertRaisesRegex(ValueError, "needs a user source"):
            gate(self.record, self.data, self.root)

    def test_optional_requirement_not_executable(self):
        self.data["requirements"][0]["kind"] = "proposal"
        with self.assertRaisesRegex(ValueError, "proposals are not executable"):
            gate(self.record, self.data, self.root)

    def test_necessary_detail_needs_justification(self):
        self.data["requirements"][0]["kind"] = "necessary"
        with self.assertRaisesRegex(ValueError, "justification"):
            gate(self.record, self.data, self.root)

    def test_necessary_safeguard_can_pass(self):
        self.data["requirements"][0].update(
            kind="necessary", justification="The dispatch fixture uses requester identity to isolate private results."
        )
        self.data["definitionHash"] = definition_hash(self.data)
        self.assertTrue(gate(self.record, self.data, self.root))

    def test_policy_can_authorize_necessary_not_requested_detail(self):
        self.data["requestSources"].append({"id": "P1", "role": "policy", "origin": "AGENTS.md", "text": "Preserve identity"})
        self.data["requirements"][0]["sources"] = ["P1"]
        self.data["requestHashes"] = request_hashes(self.data)
        self.data["requirements"][0].update(kind="necessary", justification="Mandatory isolation policy.")
        self.data["definitionHash"] = definition_hash(self.data)
        self.assertTrue(gate(self.record, self.data, self.root))

    def test_policy_alone_cannot_replace_actual_request(self):
        self.data["requestSources"][0]["role"] = "policy"
        with self.assertRaisesRegex(ValueError, "actual user request"):
            request_hashes(self.data)

    def test_source_edit_fails_even_when_refinalizing(self):
        self.data["requestSources"][0]["text"] = "Also build a new identity platform"
        result, before = self.finalize()
        self.assertEqual(result.returncode, 2)
        self.assertIn("changed or removed", result.stdout)
        self.assertEqual((self.record / "record.json").read_bytes(), before)

    def test_source_removal_fails_when_refinalizing(self):
        self.data["requestSources"] = [{"id": "S2", "role": "user", "origin": "Later message", "text": "New task"}]
        result, before = self.finalize()
        self.assertEqual(result.returncode, 2)
        self.assertIn("changed or removed", result.stdout)
        self.assertEqual((self.record / "record.json").read_bytes(), before)

    def test_source_role_edit_fails_when_refinalizing(self):
        self.data["requestSources"][0]["role"] = "policy"
        result, _ = self.finalize()
        self.assertEqual(result.returncode, 2)

    def test_append_correction_retains_original_hash(self):
        original = copy.deepcopy(self.data["requestHashes"])
        self.data["requestSources"].append({"id": "S2", "role": "user", "origin": "Follow-up",
                                            "text": "Keep display names unchanged too."})
        self.data["requirements"][0]["sources"].append("S2")
        self.data["planRevision"] += 1
        with self.assertRaisesRegex(ValueError, "sources changed"):
            gate(self.record, self.data, self.root)
        result, _ = self.finalize()
        self.assertEqual(result.returncode, 0, result.stdout)
        updated = json.loads((self.record / "record.json").read_text())
        self.assertEqual(updated["requestHashes"]["S1"], original["S1"])
        self.assertIn("S2", updated["requestHashes"])
        self.assertTrue(gate(self.record, updated, self.root))

    def test_duplicate_and_malformed_sources_rejected(self):
        for sources in ([self.data["requestSources"][0]] * 2, [None], [], "source", [{"id": "S1"}]):
            with self.subTest(sources=sources), self.assertRaises(ValueError):
                request_hashes({"requestSources": sources})

    def test_bad_seal_type_does_not_overwrite(self):
        self.data["requestHashes"] = []
        result, before = self.finalize()
        self.assertEqual(result.returncode, 2)
        self.assertEqual((self.record / "record.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
