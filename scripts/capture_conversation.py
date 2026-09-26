#!/usr/bin/env python3
"""Preserve an explicitly resolved Codex message range; never infer scope."""
import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def capture(source, thread_id, start, end, *, message_lines=None, exclude_lines=(),
            start_time=None, timezone=None, date=None, last_assistant=False):
    if start < 1 or end < start:
        raise ValueError("invalid inclusive line range")
    if (timezone or date) and not start_time:
        raise ValueError("timezone/date require --start-time")
    messages = []
    identity = None
    with Path(source).open("rb") as stream:
        for number, raw in enumerate(stream, 1):
            if number > end:
                break
            event = json.loads(raw)
            if not isinstance(event, dict):
                raise ValueError("source event must be an object")
            payload = event.get("payload", {})
            if not isinstance(payload, dict):
                raise ValueError("source payload must be an object")
            if event.get("type") == "session_meta":
                identity = payload.get("id")
            if number < start:
                continue
            if (event.get("type") == "response_item" and payload.get("type") == "message"
                    and payload.get("role") in {"user", "assistant"}):
                messages.append({"line": number, "timestamp": event.get("timestamp"),
                                 "eventSha256": hashlib.sha256(raw).hexdigest(), "message": payload})
    if identity != thread_id:
        raise ValueError("source conversation identity does not match")
    if not messages or messages[0]["line"] != start or messages[-1]["line"] != end:
        raise ValueError("both boundaries must identify actual user/assistant messages")
    available = {m["line"] for m in messages}
    excluded = set(exclude_lines)
    if not excluded <= available or end in excluded:
        raise ValueError("exclusions must name actual messages and cannot exclude invocation")
    if sum((message_lines is not None, start_time is not None, last_assistant)) > 1:
        raise ValueError("choose only one message selector")
    messages = [m for m in messages if m["line"] not in excluded]
    if message_lines is not None:
        selected = set(message_lines) | {end}
        if not selected <= available or selected & excluded:
            raise ValueError("selection must name actual non-excluded messages")
        messages = [m for m in messages if m["line"] in selected]
    elif last_assistant:
        candidates = [m for m in messages if m["line"] < end and m["message"]["role"] == "assistant"]
        if not candidates:
            raise ValueError("no preceding assistant message")
        messages = [candidates[-1], messages[-1]]
    elif start_time:
        if not timezone:
            raise ValueError("--start-time requires --timezone")
        zone = ZoneInfo(timezone)
        clock = None
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                clock = datetime.strptime(start_time.upper(), fmt).time()
                break
            except ValueError:
                pass
        if clock is None:
            raise ValueError("time must be HH:MM or H:MM AM/PM")
        if date:
            datetime.strptime(date, "%Y-%m-%d")
        matches = []
        for m in messages:
            stamp = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("source timestamps must include timezone")
            local = stamp.astimezone(zone)
            if (local.hour, local.minute) == (clock.hour, clock.minute) and (not date or local.date().isoformat() == date):
                matches.append(m)
        if not matches:
            raise ValueError("no matching message time")
        messages = [m for m in messages if m["line"] >= matches[-1]["line"]]
    start = messages[0]["line"]
    return {"schema": "aiwd-conversation/v1", "threadId": thread_id,
            "source": str(Path(source).resolve()), "startLine": start, "endLine": end,
            "messageCount": len(messages), "messages": messages}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--thread-id", required=True)
    parser.add_argument("--start-line", type=int, required=True)
    parser.add_argument("--end-line", type=int, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--message-lines", type=int, nargs="+")
    parser.add_argument("--exclude-lines", type=int, nargs="+", default=[])
    parser.add_argument("--last-assistant", action="store_true")
    parser.add_argument("--start-time")
    parser.add_argument("--timezone")
    parser.add_argument("--date")
    args = parser.parse_args()
    try:
        data = capture(args.source, args.thread_id, args.start_line, args.end_line,
                       message_lines=args.message_lines, exclude_lines=args.exclude_lines,
                       start_time=args.start_time, timezone=args.timezone, date=args.date,
                       last_assistant=args.last_assistant)
        output = Path(args.output)
        encoded = (json.dumps(data, ensure_ascii=True, indent=2) + "\n").encode()
        if args.verify:
            if output.read_bytes() != encoded:
                raise ValueError("archive differs from the complete original message range")
        else:
            # Exclusive creation preserves prior evidence, including on repeated invocations.
            with output.open("xb") as stream:
                stream.write(encoded)
        print(json.dumps({"path": str(output.resolve()), "messages": data["messageCount"],
                          "sha256": hashlib.sha256(encoded).hexdigest(), "verified": args.verify}))
        return 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(str(error))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
