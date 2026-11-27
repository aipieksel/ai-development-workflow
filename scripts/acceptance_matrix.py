#!/usr/bin/env python3
"""Check declared acceptance coverage and revision-bound evidence; never execute work."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

EXPECTATIONS = "ai-development-workflow/acceptance-expectations/v1"
MATRIX = "ai-development-workflow/acceptance-matrix/v1"
KINDS = {"source", "visual", "interaction", "motion", "roundtrip", "content",
         "package", "delivery", "compatibility", "privacy", "test", "correction"}
CHECK_STATES = {"passed", "failed", "blocked", "not-run"}
OUTPUT_STATES = {"pending", "prepared", "delivered", "blocked"}
LIMITATIONS = [
    "Checks declared expectations, not the semantic completeness of the original request.",
    "Hashes bind files and output revisions; they do not prove observations or visual quality.",
    "Remote receipts are checked for identity/version consistency, not provider authenticity.",
    "Does not run commands, fetch URLs, render, import, publish, authorize, or certify a host.",
]


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def _constant(value):
    raise ValueError("Non-finite JSON value: " + value)


def parse_json(text):
    try:
        result = json.loads(text, object_pairs_hook=_object, parse_constant=_constant)
    except (RecursionError, OverflowError) as exc:
        raise ValueError("JSON nesting exceeds supported limits") from exc
    pending = [(result, 0)]
    while pending:
        value, depth = pending.pop()
        if depth > 64:
            raise ValueError("JSON nesting exceeds supported limits")
        if isinstance(value, dict):
            pending.extend((child, depth + 1) for child in value.values())
        elif isinstance(value, list):
            pending.extend((child, depth + 1) for child in value)
    return result


def _mapping(value, required, optional=(), label="Object"):
    if not isinstance(value, dict):
        raise ValueError(label + " must be an object")
    missing = set(required) - value.keys()
    unknown = value.keys() - set(required) - set(optional)
    if missing or unknown:
        raise ValueError(f"{label}: missing {sorted(missing)}; unknown {sorted(unknown)}")
    return value


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + " must be a nonblank string")
    return value


def _ids(value, label, *, empty=False):
    if not isinstance(value, list) or (not value and not empty):
        raise ValueError(label + " must be " + ("a" if empty else "a nonempty") + " list")
    for item in value:
        _text(item, label + " item")
    if len(set(value)) != len(value):
        raise ValueError(label + " contains duplicate IDs")
    return set(value)


def _rows(value, label):
    if not isinstance(value, list):
        raise ValueError(label + " must be a list")
    result = {}
    for row in value:
        if not isinstance(row, dict):
            raise ValueError(label + " row must be an object")
        identity = _text(row.get("id"), label + " ID")
        if identity in result:
            raise ValueError(label + " contains duplicate ID " + identity)
        result[identity] = row
    return result


def _same_ids(actual, expected, label):
    if set(actual) != set(expected):
        raise ValueError(f"{label} mismatch: missing {sorted(set(expected)-set(actual))}; "
                         f"unexpected {sorted(set(actual)-set(expected))}")


def _safe_path(root, relative, *, exists=True):
    _text(relative, "Path")
    pure = PurePosixPath(relative)
    if (pure.is_absolute() or "\\" in relative or pure.as_posix() != relative
            or any(part in {".", ".."} for part in pure.parts)
            or not pure.parts or ":" in pure.parts[0]):
        raise ValueError("Use a canonical relative path inside the root: " + relative)
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlink paths are not evidence: " + relative)
    if not current.resolve().is_relative_to(root):
        raise ValueError("Path escapes root: " + relative)
    if exists and not current.is_file():
        raise ValueError("Missing evidence/output file: " + relative)
    return current


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ValueError("SHA-256 must be 64 lowercase hexadecimal characters")
    return value


def _evidence(value, root, forbidden):
    _mapping(value, {"path", "sha256"}, label="Evidence")
    path = _safe_path(root, value["path"])
    if path.resolve() in forbidden:
        raise ValueError("A manifest cannot serve as its own evidence")
    if path.stat().st_size == 0:
        raise ValueError("Evidence file is empty: " + value["path"])
    if sha256(path) != _digest(value["sha256"]):
        raise ValueError("Evidence hash is stale: " + value["path"])
    return path


def validate(expectations, matrix, root, *, complete=False, record=None, forbidden_paths=()):
    """Return structural coverage. Expected inventory must be captured before production."""
    report = {"valid": False, "complete": False, "errors": [],
              "coverageBasis": "selected-record-and-declared-targets" if record else "declared-expectations-only",
              "limitations": list(LIMITATIONS)}
    try:
        root = Path(root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("Root must be a directory")
        forbidden = {Path(path).resolve() for path in forbidden_paths}
        _mapping(expectations, {"schema", "requirements", "outputs", "checks"}, label="Expectations")
        _mapping(matrix, {"schema", "outputs", "checks"}, label="Matrix")
        if expectations["schema"] != EXPECTATIONS or matrix["schema"] != MATRIX:
            raise ValueError("Unknown expectations/matrix schema")
        requirements = _ids(expectations["requirements"], "Requirements")
        if record is not None:
            if not isinstance(record, dict) or not isinstance(record.get("requirements"), list):
                raise ValueError("Selected record has no requirement list")
            record_ids = _rows(record["requirements"], "Record requirements")
            _same_ids(requirements, record_ids, "Selected record requirements")
        expected_outputs = _rows(expectations["outputs"], "Expected outputs")
        expected_checks = _rows(expectations["checks"], "Expected checks")
        outputs = _rows(matrix["outputs"], "Outputs")
        checks = _rows(matrix["checks"], "Checks")
        _same_ids(outputs, expected_outputs, "Output IDs")
        _same_ids(checks, expected_checks, "Check IDs")
        covered_requirements, covered_outputs = set(), set()
        output_requirements = {identity: set() for identity in expected_outputs}
        locations = set()
        for identity, spec in expected_outputs.items():
            _mapping(spec, {"id", "requirements", "kind", "deliveryRequired"},
                     {"path", "locator"}, "Expected output " + identity)
            linked = _ids(spec["requirements"], identity + " requirements")
            if not linked <= requirements:
                raise ValueError("Output names unknown requirements: " + identity)
            if type(spec["deliveryRequired"]) is not bool or spec["kind"] not in {"local", "external"}:
                raise ValueError("Invalid output kind/deliveryRequired: " + identity)
            if spec["kind"] == "local":
                if "locator" in spec or "path" not in spec:
                    raise ValueError("Local output needs path only: " + identity)
                _safe_path(root, spec["path"], exists=False)
                location = ("local", spec["path"])
            else:
                if "path" in spec or "locator" not in spec or not spec["deliveryRequired"]:
                    raise ValueError("External output needs locator and deliveryRequired: " + identity)
                location = ("external", _text(spec["locator"], identity + " locator"))
            if location in locations:
                raise ValueError("Duplicate output location: " + location[1])
            locations.add(location)
            actual = outputs[identity]
            _mapping(actual, {"id", "status"}, {"revision", "receipt", "deliveryCheck"}, "Output " + identity)
            if actual["status"] not in OUTPUT_STATES:
                raise ValueError("Unknown output status: " + identity)
            if "revision" in actual:
                _text(actual["revision"], identity + " revision")
            if "deliveryCheck" in actual:
                _text(actual["deliveryCheck"], identity + " deliveryCheck")
            if "receipt" in actual:
                _mapping(actual["receipt"], {"path", "sha256"}, label="Receipt evidence")
                _safe_path(root, actual["receipt"]["path"], exists=False)
                _digest(actual["receipt"]["sha256"])
            ready = actual["status"] in {"prepared", "delivered"}
            if complete and not ready:
                raise ValueError("Output is incomplete: " + identity)
            if ready:
                revision = _text(actual.get("revision"), identity + " revision")
                if spec["kind"] == "local":
                    path = _safe_path(root, spec["path"])
                    if sha256(path) != _digest(revision):
                        raise ValueError("Output revision is stale: " + identity)
                    if "receipt" in actual:
                        raise ValueError("Local output does not use an external receipt: " + identity)
                else:
                    receipt_path = _evidence(actual.get("receipt"), root, forbidden)
                    receipt = parse_json(receipt_path.read_text(encoding="utf-8"))
                    _mapping(receipt, {"target", "revision", "status", "source"}, label="Remote receipt")
                    if (receipt["target"] != spec["locator"] or receipt["revision"] != revision
                            or receipt["status"] not in {"delivered", "verified"}):
                        raise ValueError("Remote receipt identity/version/status mismatch: " + identity)
                    _evidence(receipt["source"], root, forbidden | {receipt_path.resolve()})
            if complete and spec["deliveryRequired"] and actual["status"] != "delivered":
                raise ValueError("Required delivery is unverified: " + identity)

        for identity, spec in expected_checks.items():
            _mapping(spec, {"id", "requirements", "kind", "criterion", "targets"}, {"dimensions"}, "Expected check " + identity)
            linked = _ids(spec["requirements"], identity + " requirements")
            if not linked <= requirements or spec["kind"] not in KINDS:
                raise ValueError("Check has unknown requirement/kind: " + identity)
            _text(spec["criterion"], identity + " criterion")
            target_ids = _ids(spec["targets"], identity + " targets", empty=True)
            if not target_ids <= expected_outputs.keys():
                raise ValueError("Check names unknown output: " + identity)
            dimensions = spec.get("dimensions", {})
            if not isinstance(dimensions, dict):
                raise ValueError("Dimensions must be an object")
            for key, value in dimensions.items():
                _text(key, "Dimension name"); _text(value, "Dimension value")
            covered_requirements.update(linked)
            covered_outputs.update(target_ids)
            for output_id in target_ids:
                output_requirements[output_id].update(linked)
            actual = checks[identity]
            _mapping(actual, {"id", "status", "targets", "evidence"}, {"observed"}, "Check " + identity)
            if actual["status"] not in CHECK_STATES:
                raise ValueError("Unknown check status: " + identity)
            if "observed" in actual:
                _text(actual["observed"], identity + " observed result")
            if complete and actual["status"] != "passed":
                raise ValueError("Check has not passed: " + identity)
            bindings = _rows(actual["targets"], identity + " output bindings")
            if actual["status"] == "passed":
                _text(actual.get("observed"), identity + " observed result")
                _same_ids(bindings, target_ids, identity + " verified output IDs")
            elif not set(bindings) <= target_ids:
                raise ValueError("Unexpected output binding: " + identity)
            for output_id, binding in bindings.items():
                output_spec = expected_outputs[output_id]
                _mapping(binding, {"id", "revision"}, {"locator"}, "Output binding")
                _text(binding["revision"], "Output binding revision")
                if binding["revision"] != outputs[output_id].get("revision") or not binding["revision"]:
                    raise ValueError("Check is bound to a stale output revision: " + identity)
                if actual["status"] == "passed" and outputs[output_id]["status"] not in {"prepared", "delivered"}:
                    raise ValueError("Passed check targets an unprepared output: " + identity)
                if output_spec["kind"] == "external":
                    if binding.get("locator") != output_spec["locator"]:
                        raise ValueError("Check remote target mismatch: " + identity)
                elif "locator" in binding:
                    raise ValueError("Local check binding cannot name a remote locator")
            if not isinstance(actual["evidence"], list):
                raise ValueError("Evidence must be a list: " + identity)
            if actual["status"] == "passed" and not actual["evidence"]:
                raise ValueError("Passed check has no evidence: " + identity)
            seen_evidence = set()
            for evidence in actual["evidence"]:
                path = _evidence(evidence, root, forbidden)
                if path in seen_evidence:
                    raise ValueError("Duplicate evidence in check: " + identity)
                seen_evidence.add(path)
        _same_ids(covered_requirements, requirements, "Requirement check coverage")
        _same_ids(covered_outputs, expected_outputs, "Output check coverage")
        for identity, spec in expected_outputs.items():
            if not set(spec["requirements"]) <= output_requirements[identity]:
                raise ValueError("Output requirements lack target-specific checks: " + identity)
            actual = outputs[identity]
            delivery_id = actual.get("deliveryCheck")
            if actual["status"] == "delivered" or (complete and spec["deliveryRequired"]):
                if not isinstance(delivery_id, str) or delivery_id not in checks:
                    raise ValueError("Missing delivery check: " + identity)
                check_spec, check = expected_checks[delivery_id], checks[delivery_id]
                if (check_spec["kind"] != "delivery" or identity not in check_spec["targets"]
                        or check["status"] != "passed"):
                    raise ValueError("Delivery lacks matching passed readback: " + identity)
            elif delivery_id is not None and delivery_id not in checks:
                raise ValueError("Unknown deliveryCheck: " + identity)
        report.update(valid=True, complete=bool(complete), checkedRequirements=len(requirements),
                      checkedOutputs=len(outputs), checkedChecks=len(checks))
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        report["errors"].append(str(exc))
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--expectations", type=Path, required=True)
    parser.add_argument("--matrix", type=Path, required=True)
    parser.add_argument("--record", type=Path, help="Selected record.json; requirement IDs must match")
    parser.add_argument("--complete", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        def read_input(path):
            absolute = path.absolute() if path.is_absolute() else root / path
            relative = absolute.relative_to(root).as_posix()
            safe = _safe_path(root, relative)
            return parse_json(safe.read_text(encoding="utf-8"))
        expectations, matrix = read_input(args.expectations), read_input(args.matrix)
        record = read_input(args.record) if args.record else None
        report = validate(expectations, matrix, root, complete=args.complete, record=record,
                          forbidden_paths=[root / args.expectations, root / args.matrix])
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        report = {"valid": False, "complete": False, "errors": [str(exc)], "limitations": LIMITATIONS}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
