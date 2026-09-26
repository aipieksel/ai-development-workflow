import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "capture_conversation.py"


class ConversationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "history.jsonl"
        self.output = self.root / "conversation.json"
        self.events = [
            {"type": "session_meta", "payload": {"id": "task-A"}},
            self.message("user", "All fields, including zero and false.\n"),
            {"type": "response_item", "payload": {"type": "function_call_output", "output": "not a message"}},
            self.message("assistant", "- Fields\n- Conditions\n- Optional redesign"),
            self.message("user", "0123 11:24 PM"),
            self.message("user", "Later correction"),
        ]
        self.save()

    def message(self, role, text):
        return {"type": "response_item", "timestamp": "2026-09-10T21:24:00Z",
                "payload": {"type": "message", "role": role,
                            "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}]}}

    def save(self):
        self.source.write_text("".join(json.dumps(e) + "\n" for e in self.events))

    def run_capture(self, *extra, start="2", end="5", thread="task-A"):
        return subprocess.run([sys.executable, str(SCRIPT), "--source", str(self.source),
                               "--thread-id", thread, "--start-line", start, "--end-line", end,
                               "--output", str(self.output), *extra], capture_output=True, text=True)

    def test_exact_inclusive_range_all_roles_no_tool_or_later_messages(self):
        self.assertEqual(self.run_capture().returncode, 0)
        data = json.loads(self.output.read_text())
        self.assertEqual(data["messageCount"], 3)
        self.assertEqual([m["line"] for m in data["messages"]], [2, 4, 5])
        self.assertEqual([m["message"] for m in data["messages"]], [self.events[i]["payload"] for i in [1, 3, 4]])
        self.assertEqual(self.run_capture("--verify").returncode, 0)

    def test_never_overwrites_archive(self):
        self.run_capture()
        before = self.output.read_bytes()
        self.assertEqual(self.run_capture().returncode, 2)
        self.assertEqual(self.output.read_bytes(), before)

    def test_removed_message_or_edited_quote_fails_verification(self):
        self.run_capture()
        original = self.output.read_bytes()
        for change in ("remove", "edit"):
            data = json.loads(original)
            if change == "remove":
                data["messages"].pop(1)
            else:
                data["messages"][0]["message"]["content"][0]["text"] = "All fields"
            self.output.write_text(json.dumps(data))
            self.assertEqual(self.run_capture("--verify").returncode, 2)

    def test_wrong_identity_or_nonmessage_or_missing_boundary_rejected(self):
        for kwargs in ({"thread": "task-B"}, {"start": "3"}, {"end": "99"}, {"start": "5", "end": "2"}):
            self.assertEqual(self.run_capture(**kwargs).returncode, 2)
            self.assertFalse(self.output.exists())

    def test_source_edit_fails_but_later_append_does_not_extend_range(self):
        self.run_capture()
        self.events.append(self.message("assistant", "New reply"))
        self.save()
        self.assertEqual(self.run_capture("--verify").returncode, 0)
        self.events[1]["payload"]["content"][0]["text"] = "Altered requirement"
        self.save()
        self.assertEqual(self.run_capture("--verify").returncode, 2)

    def test_recent_selection_excludes_old_topic_and_keeps_invocation(self):
        self.assertEqual(self.run_capture("--message-lines", "4").returncode, 0)
        data = json.loads(self.output.read_text())
        self.assertEqual([m["line"] for m in data["messages"]], [4, 5])
        self.assertEqual(self.run_capture("--message-lines", "4", "--verify").returncode, 0)

    def test_last_reply_excludes_summary_and_keeps_invocation(self):
        self.events.insert(4, self.message("assistant", "Compaction summary, not authored reply"))
        self.save()
        args = ("--last-assistant", "--exclude-lines", "5")
        self.assertEqual(self.run_capture(*args, end="6").returncode, 0)
        self.assertEqual([m["line"] for m in json.loads(self.output.read_text())["messages"]], [4, 6])
        self.assertEqual(self.run_capture(*args, "--verify", end="6").returncode, 0)

    def test_latest_time_across_dates_and_same_minute_is_inclusive(self):
        self.events[1]["timestamp"] = "2026-09-09T21:24:00Z"
        self.events[3]["timestamp"] = "2026-09-10T21:24:50Z"
        self.events[4]["timestamp"] = "2026-09-10T21:46:00Z"
        self.events[5]["timestamp"] = "2026-09-11T21:24:00Z"
        self.save()
        args = ("--start-time", "11:24 PM", "--timezone", "Africa/Johannesburg")
        self.assertEqual(self.run_capture(*args).returncode, 0)
        self.assertEqual([m["line"] for m in json.loads(self.output.read_text())["messages"]], [4, 5])
        self.assertEqual(self.run_capture(*args, "--verify").returncode, 0)

    def test_explicit_date_selects_older_matching_message(self):
        self.events[1]["timestamp"] = "2026-09-09T21:24:00Z"
        self.save()
        self.assertEqual(self.run_capture("--start-time", "23:24", "--timezone", "Africa/Johannesburg",
                                          "--date", "2026-09-09").returncode, 0)
        self.assertEqual(json.loads(self.output.read_text())["startLine"], 2)

    def test_latest_of_two_authored_messages_in_same_minute(self):
        self.events[1]["timestamp"] = "2026-09-10T21:24:02Z"
        self.events[3]["timestamp"] = "2026-09-10T21:24:50Z"
        self.events[4]["timestamp"] = "2026-09-10T21:46:00Z"
        self.save()
        self.assertEqual(self.run_capture("--start-time", "23:24", "--timezone", "Africa/Johannesburg").returncode, 0)
        self.assertEqual([m["line"] for m in json.loads(self.output.read_text())["messages"]], [4, 5])

    def test_no_match_and_invalid_selections_do_not_create_archive(self):
        cases = [("--start-time", "23:25", "--timezone", "Africa/Johannesburg"),
                 ("--start-time", "23:24"), ("--message-lines", "3"),
                 ("--exclude-lines", "5"), ("--last-assistant", "--message-lines", "4")]
        for args in cases:
            self.assertEqual(self.run_capture(*args).returncode, 2)
            self.assertFalse(self.output.exists())

    def test_excluded_automated_message_cannot_win_time_match(self):
        self.events[4]["timestamp"] = "2026-09-10T21:46:00Z"
        self.events.insert(4, self.message("user", "<skill>automated attachment</skill>"))
        self.save()
        self.assertEqual(self.run_capture("--start-time", "23:24", "--timezone", "Africa/Johannesburg",
                                          "--exclude-lines", "5", end="6").returncode, 0)
        self.assertEqual([m["line"] for m in json.loads(self.output.read_text())["messages"]], [4, 6])


if __name__ == "__main__":
    unittest.main()
