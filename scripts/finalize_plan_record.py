#!/usr/bin/env python3
"""Finalize a HUMAN/AGENT-reviewed plan; hashes do not establish correctness."""
import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from plan_record import load_record, gate, digest, definition_hash, seal_request_sources, PLAN_FILES

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--record", required=True)
    parser.add_argument("--stage", choices=["planned", "criticized"], required=True)
    parser.add_argument("--resume", action="store_true",
                        help="After reconciliation, refresh readiness without resetting interrupted status")
    args = parser.parse_args()
    try:
        record, data = load_record(args.project_root, args.record)
        interrupted_status = data["status"]
        if args.resume and interrupted_status not in {"executing", "blocked"}:
            raise ValueError("resume review requires an executing or blocked record")
        if not args.resume and data["status"] in {"executing", "complete"}:
            raise ValueError("cannot finalize executing or complete work; reconcile it first")
        if args.stage == "planned" and data.get("critiqueOutcome") != "not_requested":
            raise ValueError("previously reviewed plan requires fresh critique, not bypass")
        data["status"] = interrupted_status if args.resume else args.stage
        data["readiness"] = "ready"
        if args.stage == "criticized":
            if data.get("critiqueOutcome") not in {"ready", "revised"}:
                raise ValueError("record the actual critique outcome before finalizing")
            data["reviewedPlanRevision"] = data.get("planRevision")
            data["critiqueHash"] = digest(record / "critique.md")
        data["requestHashes"] = seal_request_sources(data)
        data["planHashes"] = {name: digest(record / name) for name in PLAN_FILES}
        data["definitionHash"] = definition_hash(data)
        data["updatedAt"] = datetime.now(timezone.utc).isoformat()
        gate(record, data, args.project_root, resume=args.resume)
        descriptor, pending = tempfile.mkstemp(prefix=".record-", dir=record)
        try:
            with os.fdopen(descriptor, "w") as stream:
                json.dump(data, stream, indent=2)
                stream.write("\n")
            os.replace(pending, record / "record.json")
        finally:
            if os.path.exists(pending):
                os.unlink(pending)
        print(json.dumps({"recordPath": str(record), "status": data["status"], "readiness": "ready"}))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(str(error))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
