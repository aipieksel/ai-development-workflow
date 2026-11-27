#!/usr/bin/env python3
"""Read-only Loop handoff and wait/timer decisions; no dispatch or scheduling."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sys

# Serialized XR identifiers are retained so existing checkpoint hashes stay valid.
PREFIX = "ai-development-workflow/xr-"
INTERVAL_SECONDS = 300
TERMINAL = {"accepted", "blocked", "cancelled", "interrupted"}
SUSPENDED = {"blocked", "interrupted"}
PERMANENT = TERMINAL - SUSPENDED
BOUNDARY = "Structural accounting only; does not inspect product quality or authenticate agents, evidence, wait results, or timer receipts."


def canonical_hash(document):
    """Bind parsed JSON content without depending on indentation or key order."""
    return hashlib.sha256(json.dumps(document, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _strings(value, *, nonempty=True):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(_text(x) for x in value) and len(value) == len(set(value)))


def _indexed(value, label, errors):
    if not isinstance(value, list):
        errors.append(label + " must be a list")
        return {}
    result = {}
    for item in value:
        if not isinstance(item, dict) or not _text(item.get("id")):
            errors.append(label + " needs objects with nonblank IDs")
        elif item["id"] in result:
            errors.append(label + " contains duplicate ID " + item["id"])
        else:
            result[item["id"]] = item
    return result


def _header(doc, kind, errors):
    if not isinstance(doc, dict):
        errors.append(kind + " must be an object")
        return False
    if doc.get("schema") != PREFIX + kind + "/v1":
        errors.append(kind + " has an unsupported schema")
    for key in ("runId", "sourceRevision"):
        if not _text(doc.get(key)):
            errors.append(kind + "." + key + " is required")
    if type(doc.get("round")) is not int or doc["round"] < 1:
        errors.append(kind + ".round must be a positive integer")
    return True


def _review(doc, label, errors):
    if not _header(doc, "review", errors):
        return {}, {}
    for key in ("reviewerId", "outputRevision"):
        if not _text(doc.get(key)):
            errors.append(label + "." + key + " is required")
    if doc.get("verdict") not in {"changes-required", "accepted", "blocked"}:
        errors.append(label + " has an invalid verdict")
    coverage = _indexed(doc.get("coverage"), label + ".coverage", errors)
    sides = [x.get("side") for x in coverage.values()]
    if not coverage or any(not isinstance(x, str) for x in sides) or set(sides) != {"source", "result", "comparison"}:
        errors.append(label + " must account for source, result and comparison coverage")
    for key, row in coverage.items():
        if row.get("status") not in {"reviewed", "blocked", "not-run"}:
            errors.append(label + " coverage " + key + " has an invalid status")
        if row.get("status") == "reviewed" and not _strings(row.get("evidence")):
            errors.append(label + " coverage " + key + " needs evidence references")
        if row.get("status") != "reviewed" and not _text(row.get("reason")):
            errors.append(label + " coverage " + key + " needs an unresolved reason")
    findings = _indexed(doc.get("findings"), label + ".findings", errors)
    for key, row in findings.items():
        if row.get("disposition") not in {"actionable", "suggestion", "out-of-scope"}:
            errors.append(label + " finding " + key + " has an invalid disposition")
        if not _text(row.get("summary")) or not _strings(row.get("evidence")):
            errors.append(label + " finding " + key + " needs a summary and evidence references")
        if row.get("disposition") == "actionable" and not _text(row.get("acceptance")):
            errors.append(label + " finding " + key + " needs an acceptance criterion")
        if row.get("disposition") != "actionable" and not _text(row.get("reason")):
            errors.append(label + " finding " + key + " needs a disposition reason")
    if doc.get("verdict") == "accepted":
        if any(x.get("status") != "reviewed" for x in coverage.values()):
            errors.append(label + " cannot accept unreviewed coverage")
        if any(x.get("disposition") == "actionable" for x in findings.values()):
            errors.append(label + " cannot accept unresolved actionable findings")
    return findings, coverage



def _no_repair_corroboration(review, checklist, coverage, corroboration, acknowledgement, errors):
    """Keep the original Reviewer as decision owner after a distinct countercheck."""
    if not isinstance(corroboration, dict) or not isinstance(acknowledgement, dict):
        errors.append("initial no-repair acceptance requires independent Verifier corroboration and original Reviewer acknowledgement")
        return False
    cor_fields = {"schema", "runId", "round", "sourceRevision", "outputRevision", "reviewHash", "verifierId", "coverage", "verdict", "findings", "evidence"}
    ack_fields = {"schema", "runId", "round", "sourceRevision", "outputRevision", "reviewHash", "corroborationHash", "reviewerId", "decision", "evidence"}
    if set(corroboration) != cor_fields or corroboration.get("schema") != "ai-development-workflow/loop-corroboration/v1":
        errors.append("no-repair corroboration has missing/unknown fields or schema")
    if set(acknowledgement) != ack_fields or acknowledgement.get("schema") != "ai-development-workflow/loop-acknowledgement/v1":
        errors.append("no-repair acknowledgement has missing/unknown fields or schema")
    for label, doc in (("corroboration", corroboration), ("acknowledgement", acknowledgement)):
        for key in ("runId", "round", "sourceRevision", "outputRevision"):
            if doc.get(key) != review.get(key):
                errors.append(label + " " + key + " is not bound to the current no-repair review")
        if doc.get("reviewHash") != canonical_hash(review):
            errors.append(label + " reviewHash is stale")
        if not _strings(doc.get("evidence")):
            errors.append(label + " needs actual inspected evidence references")
    verifier = corroboration.get("verifierId")
    if not _text(verifier) or verifier in {review.get("reviewerId"), checklist.get("managerId")}:
        errors.append("no-repair Verifier must be distinct from manager and original Reviewer")
    if corroboration.get("verdict") not in {"confirmed", "changes-required", "blocked"}:
        errors.append("no-repair corroboration verdict must be confirmed, changes-required or blocked")
    translated = {**corroboration, "schema": PREFIX + "review/v1", "reviewerId": verifier,
                  "verdict": "accepted" if corroboration.get("verdict") == "confirmed" else corroboration.get("verdict")}
    _, checked = _review(translated, "corroboration", errors)
    if not set(coverage) <= set(checked):
        errors.append("no-repair corroboration dropped required coverage IDs")
    if any(checked[key].get("side") != row.get("side") for key, row in coverage.items() if key in checked):
        errors.append("no-repair corroboration changed an existing coverage side")
    if acknowledgement.get("reviewerId") != review.get("reviewerId"):
        errors.append("only the original Reviewer may acknowledge its no-repair corroboration")
    if acknowledgement.get("corroborationHash") != canonical_hash(corroboration):
        errors.append("Reviewer acknowledgement does not cover the exact Verifier corroboration")
    if acknowledgement.get("decision") not in {"accepted", "changes-required", "blocked"}:
        errors.append("Reviewer acknowledgement has an invalid decision")
    if acknowledgement.get("decision") == "accepted" and corroboration.get("verdict") != "confirmed":
        errors.append("unresolved/blocked corroboration cannot be accepted")
    return acknowledgement.get("decision") == "accepted" and corroboration.get("verdict") == "confirmed" and not errors

def check_accounting(review, checklist, execution=None, acceptance=None, corroboration=None, acknowledgement=None):
    """Check declared coverage, identities and evidence references, never their truth."""
    errors = []
    findings, coverage = _review(review, "review", errors)
    if not _header(checklist, "checklist", errors) or not isinstance(review, dict):
        return {"valid": False, "errors": errors, "boundary": BOUNDARY}
    for key in ("runId", "round", "sourceRevision", "outputRevision"):
        if checklist.get(key) != review.get(key):
            errors.append("checklist " + key + " does not match the reviewed revision")
    if not _text(checklist.get("managerId")) or checklist.get("managerId") == review.get("reviewerId"):
        errors.append("manager and reviewer must have distinct nonblank identities")
    if type(checklist.get("planRevision")) is not int or checklist["planRevision"] < 1:
        errors.append("checklist.planRevision must be a positive integer")
    if checklist.get("reviewHash") != canonical_hash(review):
        errors.append("checklist reviewHash does not match the exact review")
    items = _indexed(checklist.get("items"), "checklist.items", errors)
    actionable = {key for key, row in findings.items() if row.get("disposition") == "actionable"}
    mapped = set()
    for key, row in items.items():
        if "status" in row:
            errors.append("checklist item " + key + " is immutable; report status in execution.items")
        if not _strings(row.get("findingIds")):
            errors.append("checklist item " + key + " needs unique findingIds")
        else:
            mapped.update(row["findingIds"])
        if not _text(row.get("task")) or not _text(row.get("acceptance")):
            errors.append("checklist item " + key + " needs a task and acceptance criterion")
    if mapped != actionable:
        errors.append("checklist finding coverage differs: missing=" + str(sorted(actionable - mapped))
                      + "; extra=" + str(sorted(mapped - actionable)))
    if review.get("verdict") == "changes-required" and not actionable:
        errors.append("changes-required review needs an actionable finding")

    pending = list(items)
    fresh_ready = False
    no_repair = review.get("verdict") == "accepted" and not items and execution is None
    accepted = False
    if no_repair:
        accepted = _no_repair_corroboration(review, checklist, coverage, corroboration, acknowledgement, errors)
    elif corroboration is not None or acknowledgement is not None:
        errors.append("no-repair corroboration/acknowledgement cannot replace the selected repair cycle")
    if execution is not None:
        if _header(execution, "execution", errors):
            for key in ("runId", "round", "sourceRevision", "planRevision"):
                if execution.get(key) != checklist.get(key):
                    errors.append("execution " + key + " does not match the checklist")
            if execution.get("inputRevision") != review.get("outputRevision"):
                errors.append("execution inputRevision is stale")
            if not _text(execution.get("outputRevision")):
                errors.append("execution.outputRevision is required")
            if execution.get("checklistHash") != canonical_hash(checklist):
                errors.append("execution checklistHash does not match the exact checklist")
            executor = execution.get("executorId")
            if not _text(executor) or executor in {review.get("reviewerId"), checklist.get("managerId")}:
                errors.append("executor must be distinct from manager and reviewer")
            if execution.get("outcome") not in {"complete", "partial", "blocked"}:
                errors.append("executor may report complete, partial or blocked, never acceptance")
            results = _indexed(execution.get("items"), "execution.items", errors)
            if set(results) != set(items):
                errors.append("execution item IDs must exactly match the checklist")
            pending = []
            for key, row in results.items():
                if row.get("status") not in {"implemented", "blocked", "not-run"}:
                    errors.append("execution item " + key + " has an invalid status")
                if not _text(row.get("note")):
                    errors.append("execution item " + key + " needs a completion or blocker note")
                if row.get("status") == "implemented":
                    if not _strings(row.get("evidence")):
                        errors.append("implemented item " + key + " needs evidence references")
                else:
                    pending.append(key)
            if not items:
                errors.append("an empty repair checklist does not need an executor")
            if execution.get("outcome") == "complete" and pending:
                errors.append("complete execution still contains unresolved items")
            if execution.get("outcome") != "complete" and not pending:
                errors.append("execution outcome contradicts its item statuses")
            fresh_ready = not errors and not pending and bool(items)

    if acceptance is not None:
        accepted = False
        if execution is None or not fresh_ready:
            errors.append("fresh acceptance requires fully accounted execution first")
        new_findings, new_coverage = _review(acceptance, "acceptance", errors)
        if isinstance(acceptance, dict) and isinstance(execution, dict):
            for key in ("runId", "sourceRevision"):
                if acceptance.get(key) != review.get(key):
                    errors.append("acceptance " + key + " does not match this run")
            if type(review.get("round")) is int and acceptance.get("round") != review["round"] + 1:
                errors.append("acceptance must be the next fresh review round")
            if acceptance.get("outputRevision") != execution.get("outputRevision"):
                errors.append("acceptance is bound to a stale output revision")
            if not _text(acceptance.get("reviewerId")) or acceptance.get("reviewerId") in {review.get("reviewerId"), checklist.get("managerId"), execution.get("executorId")}:
                errors.append("acceptance needs a fresh independent reviewer identity")
            if not set(coverage).issubset(new_coverage):
                errors.append("fresh review dropped previously required coverage IDs")
            if any(new_coverage[key].get("side") != row.get("side") for key, row in coverage.items() if key in new_coverage):
                errors.append("fresh review changed an existing coverage ID's source/result/comparison side")
            resolutions = _indexed(acceptance.get("resolutions"), "acceptance.resolutions", errors)
            if set(resolutions) != actionable:
                errors.append("fresh review resolutions must account for every prior actionable finding")
            for key, row in resolutions.items():
                if row.get("status") not in {"resolved", "unresolved"} or not _strings(row.get("evidence")):
                    errors.append("resolution " + key + " needs a valid status and evidence references")
                carried = new_findings.get(key, {}).get("disposition") == "actionable"
                if row.get("status") == "unresolved" and not carried:
                    errors.append("unresolved prior finding " + key + " must remain actionable in the fresh review")
                if row.get("status") == "resolved" and carried:
                    errors.append("resolved prior finding " + key + " contradicts its current actionable status")
            if acceptance.get("verdict") == "accepted" and any(x.get("status") != "resolved" for x in resolutions.values()):
                errors.append("acceptance still has unresolved prior findings")
            accepted = acceptance.get("verdict") == "accepted" and not errors
    return {"valid": not errors, "errors": errors,
            "checklistItemCount": len(items), "actionableFindingCount": len(actionable),
            "pendingItemIds": pending, "readyForFreshReview": fresh_ready and not errors,
            "reviewerAcceptanceRecorded": accepted and not errors,
            "noRepairCorroborationRecorded": no_repair and accepted and not errors, "boundary": BOUNDARY}


def _time(value):
    if not _text(value):
        raise ValueError("a timezone-aware timestamp is required")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("timestamp must include its timezone")
    return result.astimezone(timezone.utc)


def _stamp(value):
    return value.isoformat().replace("+00:00", "Z")


def _confirm_resume(state, event, now):
    """Release a resume hold only after recorded ownership and timer observations."""
    context = state.get("resumeContext")
    if not state.get("resumePending") or not isinstance(context, dict):
        raise ValueError("resumed requires a prior reconciliation-first resume request")
    worker = context.get("workerId")
    status = event.get("workerStatus")
    if event.get("workerId") != worker or not _text(event.get("workerReceipt")):
        raise ValueError("resume confirmation needs the saved worker identity and actual observation receipt")
    if worker is None:
        if context.get("phase") != "handoff" or status not in {"none", "unknown"}:
            raise ValueError("ownerless resume requires a confirmed handoff with no active worker")
    elif not _text(worker) or status not in {"running", "completed", "stopped", "unknown"}:
        raise ValueError("resume confirmation needs an observed prior worker status")
    state["resumeWorkerObservation"] = {"workerId": worker, "status": status,
                                       "receipt": event["workerReceipt"], "observedAt": _stamp(now)}
    if status == "unknown":
        return [{"type": "report-resume-blocker", "reason": "prior worker ownership remains unknown"}]
    native = state.get("mode") == "native"
    timer_status = state.get("resumeTimerStatus")
    if native:
        if not _text(state.get("resumeTimerReceipt")) or timer_status not in {"active", "inactive"}:
            return [{"type": "report-resume-blocker", "reason": "native timer status has not been reconciled for this resume"}]
        if state.get("phase") in SUSPENDED and timer_status != "inactive":
            return [{"type": "report-resume-blocker", "reason": "suspended native timer cleanup remains live or unknown"}]
        if ((timer_status == "inactive" and (state.get("timerId") is not None or state.get("status") != "stopped"))
                or (timer_status == "active" and (not _text(state.get("timerId")) or state.get("status") != "armed"))):
            return [{"type": "report-resume-blocker", "reason": "native timer checkpoint and reconciliation still disagree"}]

    state.update(resumePending=False, lastResumeAt=_stamp(now))
    state.pop("suspended", None)
    if status == "running":
        state.update(phase=context["phase"], workerId=worker)
        actions = [{"type": "continue-current-worker", "workerId": worker}]
    else:
        state.update(phase="handoff", workerId=None)
        if status == "completed":
            actions = [{"type": "advance-phase"}]
        elif status == "stopped":
            state["pendingPhase"] = context["phase"]
            actions = [{"type": "resume-phase", "phase": context["phase"], "priorWorkerId": worker}]
        else:
            actions = [{"type": "reconcile-handoff"}]
    if native and timer_status == "inactive":
        state.update(status="registering", registrationAttempt=state["registrationAttempt"] + 1)
        actions.append({"type": "register-native", "runId": state["runId"],
                        "attempt": state["registrationAttempt"], "delaySeconds": INTERVAL_SECONDS})
    elif not native:
        state.update(status="waiting", lastCheckAt=_stamp(now),
                     nextCheckAt=_stamp(now + timedelta(seconds=INTERVAL_SECONDS)))
        actions.append({"type": "wait-active-session", "seconds": 60})
    return actions


def _timer_transition(state, event):
    """Return proposed checkpoint/actions. The caller must perform actual host calls."""
    if not isinstance(event, dict) or not _text(event.get("type")):
        raise ValueError("timer event needs a type")
    now = _time(event.get("now"))
    kind = event["type"]
    actions = []
    if state is None:
        if kind != "start" or not _text(event.get("runId")) or not _text(event.get("workerId")):
            raise ValueError("start requires a run and actual active worker identity")
        if event.get("phase") not in {"review", "execute"}:
            raise ValueError("start phase must be review or execute")
        capability = event.get("nativeTimer")
        state = {"schema": PREFIX + "timer/v1", "runId": event["runId"],
                 "workerId": event["workerId"], "phase": event["phase"],
                 "intervalSeconds": INTERVAL_SECONDS, "lastCheckAt": _stamp(now),
                 "nextCheckAt": _stamp(now + timedelta(seconds=INTERVAL_SECONDS)),
                 "timerId": None, "receipt": None, "lastWakeId": None, "handledWakeIds": []}
        if capability is not None:
            if (not isinstance(capability, dict) or capability.get("kind") not in {"one-shot", "recurring"}
                    or type(capability.get("canCancel")) is not bool or not _text(capability.get("contract"))):
                raise ValueError("nativeTimer needs actual kind, canCancel and contract evidence")
            if capability["kind"] == "recurring" and not capability["canCancel"]:
                raise ValueError("a recurring timer requires supported cancellation")
            state.update(mode="native", status="registering", nativeTimer=copy.deepcopy(capability), registrationAttempt=1)
            actions.append({"type": "register-native", "runId": state["runId"], "attempt": 1, "delaySeconds": INTERVAL_SECONDS})
        else:
            if not _text(event.get("unavailableReason")):
                raise ValueError("active-session fallback needs an observed native-timer unavailability reason")
            state.update(mode="active-session", status="waiting", unavailableReason=event["unavailableReason"])
            actions.append({"type": "wait-active-session", "seconds": 60})
    else:
        state = copy.deepcopy(state)
        if (not isinstance(state, dict) or state.get("schema") != PREFIX + "timer/v1"
                or state.get("intervalSeconds") not in {INTERVAL_SECONDS, 600}):
            raise ValueError("invalid Loop timer checkpoint")
        if not _strings(state.get("handledWakeIds"), nonempty=False):
            raise ValueError("timer checkpoint needs unique handledWakeIds for this run")
        if kind == "start":
            raise ValueError("existing run must be reconciled; never register a duplicate timer")
        if event.get("runId") != state.get("runId"):
            return {"state": state, "actions": [{"type": "ignore", "reason": "different run"}], "boundary": BOUNDARY}
        terminal = state.get("phase") in TERMINAL
        if kind == "stop":
            if event.get("phase") not in TERMINAL:
                raise ValueError("stop requires a terminal run phase")
            if state.get("phase") in PERMANENT and event["phase"] != state["phase"]:
                return {"state": state, "actions": [{"type": "ignore", "reason": "accepted/cancelled runs cannot be reopened"}],
                        "boundary": BOUNDARY, "executesHostActions": False}
            if event["phase"] in SUSPENDED:
                if state.get("phase") not in SUSPENDED:
                    state["suspended"] = {"phase": state["phase"], "workerId": state.get("workerId")}
                state["phase"] = event["phase"]
            else:
                state.update(phase=event["phase"], workerId=None)
            state["resumePending"] = False
            state.pop("resumeTimerReceipt", None)
            state.pop("resumeTimerStatus", None)
            if state.get("mode") == "native" and state.get("timerId"):
                if state.get("status") == "cancel-pending":
                    actions.append({"type": "reconcile-native-registration", "timerId": state["timerId"]})
                elif state["nativeTimer"]["canCancel"]:
                    state["status"] = "cancel-pending"
                    actions.append({"type": "cancel-native", "timerId": state["timerId"]})
                else:
                    state["status"] = "retired"
                    actions.append({"type": "ignore-future-wake", "timerId": state["timerId"]})
            elif state.get("mode") == "native" and state.get("status") in {"registering", "unknown"}:
                state["status"] = "unknown"
                actions.append({"type": "reconcile-native-registration"})
            else:
                state["status"] = "stopped"
        elif kind in {"registered", "reconciled"}:
            if state.get("mode") != "native":
                raise ValueError("native registration result does not belong to this checkpoint")
            if event.get("attempt") != state.get("registrationAttempt"):
                raise ValueError("stale native registration attempt")
            if kind == "reconciled" and type(event.get("exists")) is not bool:
                raise ValueError("reconciliation must confirm whether the native timer exists")
            if kind == "reconciled" and event.get("exists") is False:
                if not _text(event.get("receipt")):
                    raise ValueError("reconciliation needs actual host evidence")
                state.update(timerId=None, receipt=event["receipt"])
                held = terminal or state.get("resumePending")
                state["status"] = "stopped" if held else "registering"
                if state.get("resumePending"):
                    state.update(resumeTimerReceipt=event["receipt"], resumeTimerStatus="inactive")
                if not held:
                    state["registrationAttempt"] += 1
                    actions.append({"type": "register-native", "runId": state["runId"], "attempt": state["registrationAttempt"], "delaySeconds": INTERVAL_SECONDS})
            else:
                if not _text(event.get("timerId")) or not _text(event.get("receipt")):
                    raise ValueError("armed status requires a real host timer ID and receipt reference")
                if state.get("timerId") not in {None, event["timerId"]}:
                    raise ValueError("different live timer ID requires reconciliation, not replacement")
                if kind == "registered" and state.get("status") not in {"registering", "unknown"}:
                    raise ValueError("unexpected registration result")
                due = (_time(event["nextCheckAt"]) if "nextCheckAt" in event else
                       _time(state["nextCheckAt"]) if kind == "reconciled" else
                       now + timedelta(seconds=INTERVAL_SECONDS))
                state.update(timerId=event["timerId"], receipt=event["receipt"], nextCheckAt=_stamp(due))
                if state.get("resumePending"):
                    state.update(resumeTimerReceipt=event["receipt"], resumeTimerStatus="active")
                if terminal:
                    state["status"] = "cancel-pending" if state["nativeTimer"]["canCancel"] else "retired"
                    actions.append({"type": "cancel-native" if state["nativeTimer"]["canCancel"] else "ignore-future-wake",
                                    "timerId": state["timerId"]})
                else:
                    state["status"] = "armed"
        elif kind == "registration-failed":
            if state.get("mode") != "native" or state.get("status") != "registering" or not _text(event.get("reason")):
                raise ValueError("unexpected or unexplained registration failure")
            if event.get("attempt") != state.get("registrationAttempt"):
                raise ValueError("stale native registration attempt")
            if event.get("outcome") not in {"not-created", "unknown"}:
                raise ValueError("registration failure must distinguish not-created from unknown")
            state.update(status="unknown" if event["outcome"] == "unknown" else "failed", reason=event["reason"])
            actions.append({"type": "reconcile-native-registration" if event["outcome"] == "unknown" else "report-monitoring-blocker"})
        elif kind == "cancelled":
            if state.get("status") != "cancel-pending" or event.get("timerId") != state.get("timerId") or not _text(event.get("receipt")):
                raise ValueError("cancellation requires the matching timer and actual receipt")
            state.update(status="stopped", timerId=None, cancellationReceipt=event["receipt"])
            if state.get("resumePending"):
                state.update(resumeTimerReceipt=event["receipt"], resumeTimerStatus="inactive")
        elif kind == "cancel-failed":
            if (state.get("status") != "cancel-pending" or event.get("timerId") != state.get("timerId")
                    or not _text(event.get("reason"))):
                raise ValueError("unexpected or unexplained cancellation failure")
            state["reason"] = event["reason"]
            actions.append({"type": "report-cleanup-pending", "timerId": state.get("timerId")})
        elif kind == "resume":
            if state.get("phase") in PERMANENT:
                actions.append({"type": "ignore", "reason": "accepted/cancelled runs cannot resume"})
            else:
                if not state.get("resumePending"):
                    context = state.get("suspended") if state.get("phase") in SUSPENDED else {
                        "phase": state.get("phase"), "workerId": state.get("workerId")}
                    if not isinstance(context, dict) or context.get("phase") not in {"review", "execute", "handoff"}:
                        raise ValueError("suspended run lacks its original phase/ownership checkpoint")
                    state.update(resumePending=True, resumeContext=copy.deepcopy(context))
                    state.pop("resumeTimerReceipt", None)
                    state.pop("resumeTimerStatus", None)
                actions.append({"type": "inspect-current-worker", "workerId": state["resumeContext"].get("workerId")})
                if state.get("mode") == "native":
                    actions.append({"type": "reconcile-native-registration", "timerId": state.get("timerId")})
                else:
                    actions.append({"type": "check-clock"})
        elif kind == "resumed":
            if state.get("phase") in PERMANENT:
                actions.append({"type": "ignore", "reason": "accepted/cancelled runs cannot resume"})
            else:
                actions.extend(_confirm_resume(state, event, now))
        elif terminal or state.get("resumePending"):
            actions.append({"type": "ignore", "reason": "run is stopped or awaiting reconciliation; never rearm or dispatch"})
        elif kind == "worker-completed":
            if (not _text(event.get("workerId")) or not _text(state.get("workerId"))
                    or event.get("workerId") != state.get("workerId")):
                actions.append({"type": "ignore", "reason": "stale worker completion"})
            else:
                state.update(workerId=None, phase="handoff")
                actions.append({"type": "advance-phase"})
        elif kind == "worker-started":
            if state.get("workerId") is not None or event.get("phase") not in {"review", "execute"} or not _text(event.get("workerId")):
                raise ValueError("worker handoff needs confirmed previous completion and one new worker")
            if state.get("pendingPhase") is not None and event["phase"] != state["pendingPhase"]:
                raise ValueError("resume must continue the unfinished worker phase")
            state.update(workerId=event["workerId"], phase=event["phase"])
            state.pop("pendingPhase", None)
        elif kind in {"wake", "tick"}:
            native = state.get("mode") == "native"
            if kind == "wake" and (not native or event.get("timerId") != state.get("timerId")
                                   or not _text(event.get("eventId")) or event.get("eventId") in state["handledWakeIds"]):
                actions.append({"type": "ignore", "reason": "stale, duplicate or unrelated wake"})
            elif native and kind == "tick":
                actions.append({"type": "await-native-event"})
            elif state.get("status") not in {"armed", "waiting"}:
                actions.append({"type": "ignore", "reason": "check already pending or monitoring unresolved"})
            elif now < _time(state["nextCheckAt"]):
                actions.append({"type": "ignore", "reason": "early native wake"} if native else
                               {"type": "wait-active-session", "seconds": min(60, max(1, int((_time(state["nextCheckAt"]) - now).total_seconds())))})
            else:
                state.update(status="checking", lastCheckAt=_stamp(now))
                if native:
                    state["lastWakeId"] = event["eventId"]
                    state["handledWakeIds"].append(event["eventId"])
                    if state["nativeTimer"]["kind"] == "one-shot":
                        state.update(lastTimerId=state["timerId"], timerId=None)
                actions.append({"type": "inspect-current-worker", "workerId": state.get("workerId")})
        elif kind == "checked":
            if state.get("status") != "checking" or not _text(event.get("receipt")):
                raise ValueError("check completion requires a pending check and observed status evidence")
            state["checkReceipt"] = event["receipt"]
            if state.get("mode") == "native" and state["nativeTimer"]["kind"] == "one-shot":
                state.update(status="registering", timerId=None)
                state["registrationAttempt"] += 1
                actions.append({"type": "register-native", "runId": state["runId"], "attempt": state["registrationAttempt"], "delaySeconds": INTERVAL_SECONDS})
            else:
                due = _time(state["nextCheckAt"])
                if state.get("mode") == "native":
                    due += timedelta(seconds=(int((now - due).total_seconds()) // INTERVAL_SECONDS + 1) * INTERVAL_SECONDS)
                else:
                    due = now + timedelta(seconds=INTERVAL_SECONDS)
                state.update(status="armed" if state.get("mode") == "native" else "waiting", nextCheckAt=_stamp(due))
        else:
            raise ValueError("unsupported Loop timer event: " + kind)
    return {"state": state, "actions": actions, "boundary": BOUNDARY,
            "executesHostActions": False}


def _monitor_config(event):
    """Normalize observed capabilities; descriptors are not host API arguments."""
    wait = event.get("waitTool")
    if wait is not None:
        if (not isinstance(wait, dict) or not _text(wait.get("name"))
                or not _text(wait.get("contract"))
                or type(wait.get("minWaitSeconds")) is not int
                or type(wait.get("maxWaitSeconds")) is not int
                or not 1 <= wait["minWaitSeconds"] <= min(60, wait["maxWaitSeconds"])):
            raise ValueError("waitTool needs actual name, contract and usable min/max timeout seconds")
        return {"mode": "wait", "waitTool": copy.deepcopy(wait)}
    if not _text(event.get("waitUnavailableReason")):
        raise ValueError("timer or final fallback requires observed wait-tool unavailability")
    result = {"waitUnavailableReason": event["waitUnavailableReason"]}
    timer = event.get("nativeTimer")
    if timer is not None:
        if (not isinstance(timer, dict) or timer.get("kind") not in {"one-shot", "recurring"}
                or type(timer.get("canCancel")) is not bool or not _text(timer.get("contract"))):
            raise ValueError("nativeTimer needs actual kind, canCancel and contract evidence")
        if timer["kind"] == "recurring" and not timer["canCancel"]:
            raise ValueError("a recurring timer requires supported cancellation")
        return {**result, "mode": "native", "nativeTimer": copy.deepcopy(timer)}
    if not _text(event.get("unavailableReason")):
        raise ValueError("active-session fallback also requires observed native-timer unavailability")
    return {**result, "mode": "active-session", "unavailableReason": event["unavailableReason"]}


def _request_wait(state, now):
    """Reserve one call context, without asserting that a tool has been called."""
    if state.get("activeWait") is not None:
        return [{"type": "reconcile-host-wait", **state["activeWait"]}]
    if not _text(state.get("workerId")):
        state["status"] = "waiting-for-worker"
        return []
    if now >= _time(state["nextCheckAt"]):
        state.update(status="checking", lastCheckAt=_stamp(now))
        return [{"type": "inspect-current-worker", "workerId": state["workerId"]}]
    cap = state["waitTool"]
    remaining = max(1, int((_time(state["nextCheckAt"]) - now).total_seconds()))
    seconds = max(cap["minWaitSeconds"], min(60, cap["maxWaitSeconds"], remaining))
    state["waitAttempt"] += 1
    pending = {"generation": state["monitorGeneration"], "attempt": state["waitAttempt"],
               "tool": cap["name"], "workerId": state["workerId"], "seconds": seconds}
    state.update(status="awaiting", activeWait=pending)
    return [{"type": "wait-host", "runId": state["runId"], **pending}]


def _start_monitor(event, now, config, *, generation=1, registration_sequence=0):
    state = {"schema": PREFIX + "timer/v1", "runId": event["runId"],
             "workerId": event.get("workerId"), "phase": event["phase"],
             "intervalSeconds": INTERVAL_SECONDS, "lastCheckAt": _stamp(now),
             "nextCheckAt": _stamp(now + timedelta(seconds=INTERVAL_SECONDS)),
             "timerId": None, "receipt": None, "lastWakeId": None, "handledWakeIds": [],
             "monitorGeneration": generation, "registrationSequence": registration_sequence,
             **copy.deepcopy(config)}
    if state["mode"] == "wait":
        state.update(waitAttempt=0, activeWait=None)
        actions = _request_wait(state, now)
    elif state["mode"] == "native":
        state.update(status="waiting-for-worker", registrationAttempt=registration_sequence)
        actions = []
        if _text(state.get("workerId")):
            state.update(status="registering", registrationAttempt=registration_sequence + 1)
            actions.append({"type": "register-native", "runId": state["runId"],
                            "attempt": state["registrationAttempt"], "delaySeconds": INTERVAL_SECONDS})
    else:
        state["status"] = "waiting"
        actions = [{"type": "wait-active-session", "seconds": 60}]
    return state, actions


def _wait_matches(state, event):
    pending = state.get("activeWait")
    return (isinstance(pending, dict)
            and all(event.get(key) == pending[key] for key in ("generation", "attempt", "tool", "workerId")))


def _wait_transition(state, event, now):
    kind = event["type"]
    terminal = state.get("phase") in TERMINAL
    held = terminal or state.get("resumePending") or state.get("reconfigurationPending")
    if kind in {"wait-returned", "wait-failed"}:
        if not _wait_matches(state, event):
            return [{"type": "ignore", "reason": "stale, duplicate or unrelated wait result"}]
        if not _text(event.get("receipt")):
            raise ValueError("wait result needs actual host observation evidence")
        state["waitReceipt"] = event["receipt"]
        if kind == "wait-failed":
            if event.get("outcome") not in {"not-waiting", "unknown"} or not _text(event.get("reason")):
                raise ValueError("wait failure needs a reason and definite/unknown ownership outcome")
            state["waitFailure"] = {"reason": event["reason"], "receipt": event["receipt"]}
            if event["outcome"] == "unknown":
                state["status"] = "unknown"
                return [{"type": "reconcile-host-wait", **state["activeWait"]}]
            state.update(activeWait=None, status="stopped" if held else "failed")
            return [{"type": "reconfigure-monitor", "reason": event["reason"]}]
        if event.get("outcome") not in {"timeout", "event", "worker-completed"}:
            raise ValueError("wait return needs timeout, event or worker-completed outcome")
        if event["outcome"] == "worker-completed" and not _text(event.get("workerReceipt")):
            raise ValueError("worker completion needs its actual worker result evidence")
        state.update(activeWait=None, status="stopped" if terminal else "waiting")
        if state.get("resumePending"):
            state.update(resumeWaitStatus="inactive", resumeWaitReceipt=event["receipt"])
        if held:
            return [{"type": "ignore", "reason": "wait ended; stopped or reconciling run cannot dispatch"}]
        if event["outcome"] == "worker-completed" and event["workerId"] == state.get("workerId"):
            state.update(workerId=None, phase="handoff", status="waiting-for-worker")
            state["workerCompletionReceipt"] = event["workerReceipt"]
            return [{"type": "advance-phase"}]
        return _request_wait(state, now)
    if kind == "wait-reconciled":
        if (event.get("generation") != state["monitorGeneration"]
                or event.get("attempt") != state["waitAttempt"]
                or event.get("tool") != state["waitTool"]["name"]
                or not _text(event.get("receipt"))
                or event.get("waitStatus") not in {"active", "inactive", "unknown"}):
            raise ValueError("wait reconciliation needs the current generation, attempt, tool, status and actual receipt")
        if state.get("activeWait") and event.get("workerId") != state["activeWait"]["workerId"]:
            raise ValueError("wait reconciliation must preserve its pending worker binding")
        state.update(waitReconciliationReceipt=event["receipt"],
                     waitReconciliationStatus=event["waitStatus"])
        if state.get("resumePending"):
            state.update(resumeWaitStatus=event["waitStatus"], resumeWaitReceipt=event["receipt"])
        if event["waitStatus"] != "inactive":
            state["status"] = "unknown"
            return [{"type": "report-monitoring-blocker", "reason": "prior wait is active or unknown; do not duplicate it"}]
        state.update(activeWait=None, status="stopped" if terminal else "waiting")
        return [] if held else _request_wait(state, now)
    if kind == "stop":
        if event.get("phase") not in TERMINAL:
            raise ValueError("stop requires a terminal run phase")
        if state.get("phase") in PERMANENT and event["phase"] != state["phase"]:
            return [{"type": "ignore", "reason": "accepted/cancelled runs cannot be reopened"}]
        if event["phase"] in SUSPENDED:
            if state.get("phase") not in SUSPENDED:
                state["suspended"] = {"phase": state["phase"], "workerId": state.get("workerId")}
            state["phase"] = event["phase"]
        else:
            state.update(phase=event["phase"], workerId=None)
        state["resumePending"] = False
        state.pop("resumeWaitReceipt", None)
        state.pop("resumeWaitStatus", None)
        state["status"] = "wait-cleanup-pending" if state.get("activeWait") else "stopped"
        return ([{"type": "reconcile-host-wait", **state["activeWait"]}]
                if state.get("activeWait") else [])
    if kind == "resume":
        if state.get("phase") in PERMANENT:
            return [{"type": "ignore", "reason": "accepted/cancelled runs cannot resume"}]
        if not state.get("resumePending"):
            context = state.get("suspended") if state.get("phase") in SUSPENDED else {
                "phase": state.get("phase"), "workerId": state.get("workerId")}
            if not isinstance(context, dict) or context.get("phase") not in {"review", "execute", "handoff"}:
                raise ValueError("resume lacks the original worker/phase checkpoint")
            state.update(resumePending=True, resumeContext=copy.deepcopy(context))
            state.pop("resumeWaitReceipt", None)
            state.pop("resumeWaitStatus", None)
        return [{"type": "inspect-current-worker", "workerId": state["resumeContext"]["workerId"]},
                {"type": "reconcile-host-wait", "generation": state["monitorGeneration"],
                 "attempt": state["waitAttempt"], "tool": state["waitTool"]["name"]}]
    if kind == "resumed":
        if state.get("phase") in PERMANENT:
            return [{"type": "ignore", "reason": "accepted/cancelled runs cannot resume"}]
        if (not state.get("resumePending") or not isinstance(state.get("resumeContext"), dict)):
            raise ValueError("resumed requires a prior resume request")
        context = state["resumeContext"]
        if event.get("workerId") != context["workerId"] or not _text(event.get("workerReceipt")):
            raise ValueError("resume requires the saved worker identity and actual observation")
        status = event.get("workerStatus")
        allowed = {"none", "unknown"} if context["workerId"] is None else {"running", "completed", "stopped", "unknown"}
        if status not in allowed:
            raise ValueError("resume requires the actual prior worker status")
        if (status == "unknown" or state.get("activeWait") is not None
                or state.get("resumeWaitStatus") != "inactive" or not _text(state.get("resumeWaitReceipt"))):
            return [{"type": "report-resume-blocker", "reason": "worker or prior wait is not reconciled"}]
        state.update(resumePending=False, lastResumeAt=_stamp(now),
                     resumeWorkerObservation={"workerId": context["workerId"], "status": status,
                                              "receipt": event["workerReceipt"], "observedAt": _stamp(now)})
        state.pop("suspended", None)
        if status == "running":
            state.update(workerId=context["workerId"], phase=context["phase"], status="waiting")
            return [{"type": "continue-current-worker", "workerId": context["workerId"]}, *_request_wait(state, now)]
        state.update(workerId=None, phase="handoff", status="waiting-for-worker")
        if status == "stopped":
            state["pendingPhase"] = context["phase"]
            return [{"type": "resume-phase", "phase": context["phase"], "priorWorkerId": context["workerId"]}]
        return [{"type": "advance-phase" if status == "completed" else "reconcile-handoff"}]
    if held:
        return [{"type": "ignore", "reason": "run is stopped or awaiting reconciliation"}]
    if kind == "worker-completed":
        if not _text(event.get("workerId")) or event["workerId"] != state.get("workerId"):
            return [{"type": "ignore", "reason": "stale worker completion"}]
        state.update(workerId=None, phase="handoff")
        actions = [{"type": "advance-phase"}]
        if state.get("activeWait"):
            actions.append({"type": "reconcile-host-wait", **state["activeWait"]})
        else:
            state["status"] = "waiting-for-worker"
        return actions
    if kind == "worker-started":
        if (state.get("workerId") is not None or state.get("activeWait") is not None
                or not _text(event.get("workerId")) or event.get("phase") not in {"review", "execute"}):
            raise ValueError("worker handoff requires prior completion and no unresolved wait")
        if state.get("pendingPhase") is not None and event["phase"] != state["pendingPhase"]:
            raise ValueError("resume must continue the unfinished worker phase")
        state.update(workerId=event["workerId"], phase=event["phase"])
        state.pop("pendingPhase", None)
        return _request_wait(state, now)
    if kind == "checked":
        if state.get("status") != "checking" or not _text(event.get("receipt")):
            raise ValueError("checked requires a pending check and observed worker status evidence")
        state.update(checkReceipt=event["receipt"], nextCheckAt=_stamp(now + timedelta(seconds=INTERVAL_SECONDS)))
        return _request_wait(state, now)
    if kind == "tick":
        if state.get("activeWait") is not None:
            return [{"type": "await-current-wait", **state["activeWait"]}]
        if state.get("status") in {"checking", "unknown", "failed"}:
            return [{"type": "ignore", "reason": "check or monitoring resolution is pending"}]
        return _request_wait(state, now)
    if kind == "wake":
        return [{"type": "ignore", "reason": "timer wake does not belong to wait monitoring"}]
    raise ValueError("unsupported Loop wait event: " + kind)


def timer_transition(state, event):
    """Propose wait-first monitoring; historical name retained for CLI/import compatibility."""
    if not isinstance(event, dict) or not _text(event.get("type")):
        raise ValueError("monitor event needs a type")
    now = _time(event.get("now"))
    kind = event["type"]
    if state is None:
        if (kind != "start" or not _text(event.get("runId")) or not _text(event.get("workerId"))
                or event.get("phase") not in {"review", "execute"}):
            raise ValueError("start requires a run and actual active reviewer/executor")
        state, actions = _start_monitor(event, now, _monitor_config(event))
    else:
        state = copy.deepcopy(state)
        if (not isinstance(state, dict) or state.get("schema") != PREFIX + "timer/v1"
                or type(state.get("intervalSeconds")) is not int
                or state["intervalSeconds"] not in {300, 600}):
            raise ValueError("invalid Loop monitoring checkpoint")
        if event.get("runId") != state.get("runId"):
            actions = [{"type": "ignore", "reason": "different run"}]
        elif kind == "start":
            raise ValueError("existing run must be reconciled; never create a duplicate monitor")
        elif kind == "reconfigure":
            if state.get("phase") in PERMANENT:
                actions = [{"type": "ignore", "reason": "accepted/cancelled runs cannot be reconfigured"}]
            elif state.get("reconfigurationPending"):
                actions = [{"type": "reconcile-monitor", "reason": "existing reconfiguration is still pending"}]
            else:
                config = _monitor_config(event)
                if not _text(event.get("receipt")):
                    raise ValueError("reconfigure needs its actual correction/capability observation reference")
                previous = copy.deepcopy(state)
                previous.pop("monitorHistory", None)
                context = state.get("suspended") if state.get("phase") in SUSPENDED else {
                    "phase": state.get("phase"), "workerId": state.get("workerId")}
                if not isinstance(context, dict) or context.get("phase") not in {"review", "execute", "handoff"}:
                    raise ValueError("reconfiguration requires the saved worker/phase context")
                stop = {**event, "type": "stop", "phase": "interrupted"}
                if state.get("mode") == "wait":
                    actions = _wait_transition(state, stop, now)
                else:
                    stopped = _timer_transition(state, stop)
                    state, actions = stopped["state"], stopped["actions"]
                state.update(reconfigurationPending=True, reconfigurationContext=copy.deepcopy(context),
                             proposedMonitor=config, previousMonitor=previous,
                             reconfigurationReceipt=event["receipt"])
                actions.append({"type": "inspect-current-worker", "workerId": context["workerId"]})
        elif kind == "reconfigured":
            if state.get("phase") in PERMANENT:
                actions = [{"type": "ignore", "reason": "accepted/cancelled runs stay terminal"}]
            elif not state.get("reconfigurationPending"):
                raise ValueError("reconfigured requires a preceding reconfiguration request")
            else:
                context = state["reconfigurationContext"]
                status = event.get("workerStatus")
                allowed = {"none", "unknown"} if context["workerId"] is None else {"running", "completed", "stopped", "unknown"}
                if (event.get("workerId") != context["workerId"] or status not in allowed
                        or not _text(event.get("workerReceipt")) or not _text(event.get("cleanupReceipt"))):
                    raise ValueError("reconfiguration needs matching observed worker and cleanup evidence")
                clean = state.get("timerId") is None and state.get("activeWait") is None and state.get("status") == "stopped"
                if status == "unknown" or not clean:
                    actions = [{"type": "report-monitoring-blocker", "reason": "old monitor or worker ownership is unresolved"}]
                else:
                    history = [*state.get("monitorHistory", []), {
                        "checkpoint": state["previousMonitor"], "correctionReceipt": state["reconfigurationReceipt"],
                        "cleanupReceipt": event["cleanupReceipt"], "workerReceipt": event["workerReceipt"],
                        "reconfiguredAt": _stamp(now)}]
                    running = status == "running"
                    start = {"runId": state["runId"], "workerId": context["workerId"] if running else None,
                             "phase": context["phase"] if running else "handoff"}
                    sequence = max(state.get("registrationAttempt", 0), state.get("registrationSequence", 0))
                    state, actions = _start_monitor(start, now, state["proposedMonitor"],
                        generation=state.get("monitorGeneration", 1) + 1, registration_sequence=sequence)
                    state["monitorHistory"] = history
                    if not running:
                        if status == "stopped":
                            state["pendingPhase"] = context["phase"]
                            actions.insert(0, {"type": "resume-phase", "phase": context["phase"], "priorWorkerId": context["workerId"]})
                        else:
                            actions.insert(0, {"type": "advance-phase" if status == "completed" else "reconcile-handoff"})
        elif (state.get("intervalSeconds") == 600 and not state.get("reconfigurationPending")
              and kind != "stop" and not (state.get("phase") in TERMINAL and kind in {
                  "registered", "reconciled", "registration-failed", "cancelled", "cancel-failed"})):
            actions = [{"type": "reconfigure-monitor", "reason": "historical 600-second checkpoint requires explicit 300-second reconciliation"}]
        elif state.get("reconfigurationPending") and kind not in {
                "stop", "registered", "reconciled", "registration-failed", "cancelled", "cancel-failed",
                "wait-returned", "wait-failed", "wait-reconciled"}:
            actions = [{"type": "ignore", "reason": "monitor reconfiguration still requires cleanup and ownership confirmation"}]
        elif kind.startswith("wait-") and state.get("mode") != "wait":
            actions = [{"type": "ignore", "reason": "wait result belongs to a prior monitoring mechanism"}]
        elif state.get("mode") == "wait" and kind in {"registered", "reconciled", "registration-failed", "cancelled", "cancel-failed"}:
            actions = [{"type": "ignore", "reason": "timer result belongs to a prior monitoring mechanism"}]
        elif state.get("mode") == "wait":
            actions = _wait_transition(state, event, now)
        else:
            before_status = state.get("status")
            result = _timer_transition(state, event)
            state, actions = result["state"], result["actions"]
            if kind == "worker-started" and before_status == "waiting-for-worker" and state.get("mode") == "native":
                state.update(status="registering", registrationAttempt=state["registrationAttempt"] + 1)
                actions.append({"type": "register-native", "runId": state["runId"],
                                "attempt": state["registrationAttempt"], "delaySeconds": INTERVAL_SECONDS})
    return {"state": state, "actions": actions, "boundary": BOUNDARY, "executesHostActions": False}


monitor_transition = timer_transition


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Account for declared review/checklist/execution artifacts")
    check.add_argument("--review", required=True)
    check.add_argument("--checklist", required=True)
    check.add_argument("--execution")
    check.add_argument("--acceptance")
    check.add_argument("--corroboration")
    check.add_argument("--acknowledgement")
    timer = sub.add_parser("timer", aliases=["monitor"], help="Print wait/timer bookkeeping decisions; never execute host calls")
    timer.add_argument("--state", help="Omit only for an actual start event")
    timer.add_argument("--event", required=True)
    args = parser.parse_args()
    try:
        if args.command == "check":
            result = check_accounting(_load(args.review), _load(args.checklist),
                                      _load(args.execution) if args.execution else None,
                                      _load(args.acceptance) if args.acceptance else None,
                                      _load(args.corroboration) if args.corroboration else None,
                                      _load(args.acknowledgement) if args.acknowledgement else None)
        else:
            result = timer_transition(_load(args.state) if args.state else None, _load(args.event))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)], "boundary": BOUNDARY}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 2 if result.get("valid") is False else 0


if __name__ == "__main__":
    raise SystemExit(main())
