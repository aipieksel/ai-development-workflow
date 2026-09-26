from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "create_plan_record.py"


class CreatePlanRecordTests(unittest.TestCase):
    def test_rejects_escaped_task_root(self) -> None:
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as outside:
            root = Path(project)
            (root / "documents").symlink_to(Path(outside), target_is_directory=True)
            result = self.run_script(root)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(list(Path(outside).iterdir()), [])

    def run_script(self, root: Path, title: str = "Repair account flow"):
        return subprocess.run(
            ["python3", str(SCRIPT), "--project-root", str(root), "--title", title],
            text=True, capture_output=True, check=False,
        )

    def test_creates_complete_unique_records(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.run_script(root)
            second = self.run_script(root)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            one, two = json.loads(first.stdout), json.loads(second.stdout)
            self.assertNotEqual(one["recordPath"], two["recordPath"])
            record = Path(one["recordPath"])
            self.assertRegex(record.name, r"^\d{4}-\d{2}-\d{2}-\d{5}-repair-account-flow$")
            expected = {"record.json", "checklist.md", "fix-plan.md", "test-plan.md", "critique.md", "results.md"}
            self.assertEqual({path.name for path in record.iterdir()}, expected)
            self.assertEqual(json.loads((record / "record.json").read_text())["status"], "draft")
            self.assertTrue(all(path.stat().st_size > 40 for path in record.iterdir()))

    def test_rejects_empty_title(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(self.run_script(Path(temporary), "---").returncode, 2)

    def test_fresh_record_preserves_prior_open_and_complete_records(self) -> None:
        for status in ("blocked", "complete"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                first = self.run_script(root)
                self.assertEqual(first.returncode, 0, first.stderr)
                old = Path(json.loads(first.stdout)["recordPath"])
                metadata = json.loads((old / "record.json").read_text())
                metadata["status"] = status
                (old / "record.json").write_text(json.dumps(metadata))
                (old / "results.md").write_text("Prior attempt and evidence must remain unchanged.\n")
                before = {p.name: p.read_bytes() for p in old.iterdir()}
                second = self.run_script(root)
                self.assertEqual(second.returncode, 0, second.stderr)
                new = Path(json.loads(second.stdout)["recordPath"])
                self.assertNotEqual(old, new)
                self.assertEqual(before, {p.name: p.read_bytes() for p in old.iterdir()})
                self.assertEqual(json.loads((new / "record.json").read_text())["status"], "draft")


if __name__ == "__main__":
    unittest.main()
