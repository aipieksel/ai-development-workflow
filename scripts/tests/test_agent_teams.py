"""Adversarial team/registry cases using synthetic, non-authenticating evidence."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from agent_registry import load_registry, resolve_profile
from contract_fixture import (declare_returned_contributions, fixture_assignment,
                              make_readonly_contract, refresh_contract)
from test_contract import fixture
from task_policy import ARCHITECT, BUILDER, INVESTIGATOR, REVIEWER, UI_DIRECTOR, VERIFIER
from workflow_contract import (LEGACY_SCHEMA, SCHEMA, canonical_hash, migration_proposal,
                               selection as contract_selection, validate_contract)


class RegistryTests(unittest.TestCase):
    def test_complete_canonical_operation_and_legacy_inventory(self):
        registry = load_registry()
        self.assertEqual(set(registry["families"]), {"investigator", "architect", "builder", "ui-design-director", "reviewer", "verification-engineer"})
        self.assertEqual((len(registry["operations"]), len(registry["legacyProfiles"]), len(registry["capabilities"])), (26, 38, 37))
        for operation, mapping in registry["operations"].items():
            resolved = resolve_profile(registry["families"][mapping["family"]]["profile"], operation,
                                       capabilities=mapping["capabilities"], registry=registry)
            self.assertEqual(resolved["family"], mapping["family"])
            self.assertIn(operation, resolved["capabilities"])
        for old_path in registry["legacyProfiles"]:
            self.assertTrue((ROOT / old_path).read_text().strip())
            self.assertIn(resolve_profile(old_path, registry=registry)["family"], registry["families"])

    def test_canonical_architect_consult_uses_explicit_planning_capability(self):
        registry = load_registry()
        for capability in ("plan-code", "plan-goals", "design-architecture"):
            with self.subTest(capability=capability):
                resolved = resolve_profile(ARCHITECT, "consult", capabilities=[capability], registry=registry)
                self.assertEqual(resolved["capabilities"], [capability])
                self.assertEqual(resolved["family"], "architect")
        self.assertEqual(resolve_profile("agents/code-goal-planner/agent.md", "consult", registry=registry)["capabilities"], ["plan-code"])

    def test_mixed_legacy_execution_preserves_builder_authority_and_specialty(self):
        registry = load_registry()
        for path, specialty in (("agents/code-reviewer/agent.md", "review-code"),
                                ("agents/e2e-runner/agent.md", "run-e2e"),
                                ("agents/security-verifier/agent.md", "review-security")):
            with self.subTest(path=path):
                result = resolve_profile(path, "execute_and_test", "repo-write-scoped", registry=registry)
                self.assertEqual(result["family"], "builder")
                self.assertIn(specialty, result["capabilities"])
        self.assertEqual(resolve_profile("agents/code-reviewer/agent.md", "review", "read-only", registry=registry)["family"], "reviewer")
        with self.assertRaisesRegex(ValueError, "operation/profile family mismatch"):
            resolve_profile(REVIEWER, "execute-plan", "repo-write-scoped", capabilities=["review-code"], registry=registry)
        with self.assertRaisesRegex(ValueError, "incompatible"):
            resolve_profile(REVIEWER, capabilities=["fast-build"], registry=registry)
        with self.assertRaisesRegex(ValueError, "docs-only"):
            resolve_profile(BUILDER, "execute-plan", "docs-only", capabilities=["execute-plan"], registry=registry)

    def test_registry_rejects_chained_alias_and_unsafe_missing_or_empty_instructions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "package"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            path = root / "agents/registry.json"
            original = path.read_text()
            data = json.loads(original)
            data["operationAliases"]["a"] = "b"
            data["operationAliases"]["b"] = "a"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "chained/circular"):
                load_registry(root)
            for bad in ("../outside.md", "agents/missing.md"):
                data = json.loads(original)
                data["capabilities"]["fast-build"]["instructions"] = bad
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_registry(root)
            path.write_text(original)
            (root / "agents/builder/agent.md").write_text("\n")
            with self.assertRaisesRegex(ValueError, "empty instruction"):
                load_registry(root)

    def test_mandatory_worker_contract_is_bound_and_cannot_be_missing_empty_or_symlinked(self):
        from workflow_catalog import build_catalog
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "package"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            path = root / "agents/capabilities/worker-contract.md"
            original = path.read_bytes()
            before_registry = load_registry(root)["fingerprint"]
            before_catalogue = build_catalog(root)["catalogueFingerprint"]
            path.write_bytes(original + b"\nSynthetic changed mandatory instruction.\n")
            self.assertNotEqual(load_registry(root)["fingerprint"], before_registry)
            self.assertNotEqual(build_catalog(root)["catalogueFingerprint"], before_catalogue)
            path.unlink()
            with self.assertRaisesRegex(ValueError, "missing instruction"):
                load_registry(root)
            path.write_text("\n")
            with self.assertRaisesRegex(ValueError, "empty instruction"):
                load_registry(root)
            path.unlink()
            target = Path(temporary) / "outside.md"
            target.write_bytes(original)
            path.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "symlinked instruction"):
                load_registry(root)

    def test_alternate_catalogue_selection_uses_only_its_supplied_registry(self):
        from workflow_catalog import build_catalog, validate_selection
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            root = workspace / "package"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
            path = root / "agents/registry.json"
            data = json.loads(path.read_text())
            data["capabilities"]["alternate-review"] = {"instructions": "agents/capabilities/review.md", "families": ["reviewer"]}
            path.write_text(json.dumps(data))
            # The alternate package is data, never imported executable Python.
            (root / "scripts/task_policy.py").write_text("raise RuntimeError('foreign code must not execute')\n")
            catalog = build_catalog(root)
            _, record_data = fixture(workspace / "project")
            selected = copy.deepcopy(record_data["workflowContract"]["selection"])
            selected["delegation"]["assignments"][-1]["capabilities"].append("alternate-review")
            # This test inspects an alternate catalogue/registry as data. It is
            # not an execution receipt for that package's separate search index.
            selected.pop("selectionSchema")
            selected.pop("discovery")
            selected.pop("workflow")
            selected.update(catalogueFingerprint=catalog["catalogueFingerprint"], intent="implement",
                            request="Exercise the supplied alternate package's review capability.",
                            chain=[{"id": "mode:build", "why": "This fixture verifies an authorized bounded build."}],
                            specialists=[], existingEvidence=[])
            result = validate_selection(selected, catalog)
            self.assertTrue(result["valid"], result["errors"])


class TeamContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name)
        self.record, self.data = fixture(self.project)
        self.contract = self.data["workflowContract"]

    def state(self, identity):
        return next(row for row in self.contract["progress"]["phases"] if row["id"] == identity)

    def refresh(self):
        refresh_contract(self.record, self.data)

    def validate(self, **options):
        return validate_contract(self.record, self.data, **options)

    def finish(self):
        for identity in ("execute", "verify", "accept"):
            self.state(identity).update(status="complete", ownerId="fixture:critic" if identity == "accept" else "fixture:executor",
                                        evidence=["fixture:result-" + identity])
        self.contract["progress"].update(currentPhase="accept", resultRevision="fixture:exact-source-revision-A")
        for worker in self.contract["roster"]["workers"]:
            worker["status"] = "completed"
        self.contract["roster"]["activeAgentCount"] = 1
        declare_returned_contributions(self.contract)
        self.refresh()

    def add_advice(self, identity, profile, capability, actor):
        selected = self.contract["selection"]
        selected["phases"].insert(1, {"id": identity, "title": identity.title() + " advice", "kind": "other",
            "operation": capability, "writeScope": "record-only", "owner": identity, "dependsOn": ["scope"]})
        plan = next(row for row in selected["phases"] if row["id"] == "plan")
        plan["dependsOn"].append(identity)
        selected["delegation"]["assignments"].insert(0, fixture_assignment(identity, profile, capabilities=[capability] + (["ui-design"] if profile == UI_DIRECTOR else [])))
        for assignment in selected["delegation"]["assignments"]:
            if assignment["phaseId"] in {"critique", "accept"}:
                assignment["independentFrom"].append(identity)
        self.contract["progress"]["phases"].insert(1, {"id": identity, "status": "complete", "ownerId": actor,
            "authorIds": [actor], "evidence": ["fixture:" + identity + "-advice"], "workHash": None})
        self.contract["roster"]["workers"].append({"id": actor, "role": identity, "status": "completed", "evidence": ["fixture:" + identity + "-dispatch-and-result"]})
        self.contract["roster"]["profiles"].append({"name": profile, "ownerId": actor})
        self.contract["roster"]["assignments"].append({"assignmentId": identity, "workerId": actor})
        declare_returned_contributions(self.contract)
        self.refresh()

    def test_useful_two_worker_sequential_completion_reports_separate_counts(self):
        self.finish()
        result = self.validate(completing=True)
        self.assertEqual((result["requiredContributors"], result["returnedContributors"]), (2, 2))
        self.assertEqual(self.contract["roster"]["activeAgentCount"], 1)
        self.assertTrue(result["completionValidated"])

    def test_missing_status_only_echo_and_duplicate_contribution_fail(self):
        self.finish()
        original = copy.deepcopy(self.contract["contributions"])
        for mutate, message in (
            (lambda rows: rows.pop(1), "lacks a useful current contribution"),
            (lambda rows: rows[1].update(kind="status"), "status-only"),
            (lambda rows: rows[1].update(summary="Done."), "substantive result"),
            (lambda rows: rows.append(copy.deepcopy(rows[1])), "contribution identity"),
        ):
            with self.subTest(message=message):
                self.contract["contributions"] = copy.deepcopy(original)
                mutate(self.contract["contributions"])
                self.refresh()
                with self.assertRaisesRegex(ValueError, message):
                    self.validate(completing=True)
        self.contract["contributions"] = original

    def test_limitations_required_and_unresolved_required_work_blocks_completion(self):
        self.finish()
        row = self.contract["contributions"][1]
        row.pop("limitations")
        with self.assertRaisesRegex(ValueError, "explicit limitations"):
            self.validate(completing=True)
        row["limitations"] = ["unknown"]
        self.refresh()
        with self.assertRaisesRegex(ValueError, "placeholders"):
            self.validate(completing=True)
        row.update(limitations=["The required independent target remains unavailable in this synthetic case."], disposition="unresolved")
        self.refresh()
        with self.assertRaisesRegex(ValueError, "unresolved in-scope"):
            self.validate(completing=True)
        row.update(limitations=[], disposition="incorporated")
        self.refresh()
        self.assertTrue(self.validate(completing=True)["completionValidated"])

    def test_rejected_suggestion_can_be_a_useful_resolved_contribution(self):
        self.finish()
        row = self.contract["contributions"][0]
        row.update(disposition="rejected", effect="Rejected the optional expansion because the inspected single-owner scope does not require it.")
        self.refresh()
        self.assertEqual(self.validate(completing=True)["returnedContributors"], 2)

    def test_final_acceptance_cannot_be_reused_for_changed_result(self):
        self.finish()
        self.contract["progress"]["resultRevision"] = "fixture:different-source-revision-B"
        with self.assertRaisesRegex(ValueError, "exact current integrated result"):
            self.validate(completing=True)

    def test_stale_contribution_cannot_be_silently_counted(self):
        self.finish()
        self.contract["contributions"][1]["workHash"] = "stale-fixture-work"
        with self.assertRaisesRegex(ValueError, "contribution is stale"):
            self.validate(completing=True)

    def test_all_secondary_authors_participate_in_independence(self):
        self.state("execute")["authorIds"].append("fixture:critic")
        self.refresh()
        with self.assertRaisesRegex(ValueError, "independent duty shares|cannot provide independent"):
            self.validate()

    def test_incorporated_author_cannot_be_hidden_by_omitting_author_ids(self):
        self.finish()
        self.state("execute")["authorIds"] = ["fixture:coordinator"]
        self.state("execute")["ownerId"] = "fixture:coordinator"
        self.refresh()
        with self.assertRaisesRegex(ValueError, "actual assigned workers|missing from all-author"):
            self.validate(completing=True)

    def test_architecture_author_cannot_switch_profile_to_independent_critic(self):
        selected = self.contract["selection"]
        selected["routing"].update(impact="cross-cutting", changedSharedContract=True)
        self.add_advice("architecture", ARCHITECT, "design-architecture", "fixture:architect")
        self.assertTrue(self.validate()["admitted"])
        self.state("critique")["ownerId"] = "fixture:architect"
        self.contract["review"]["reviewerId"] = "fixture:architect"
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "critique")["workerId"] = "fixture:architect"
        self.contract["roster"]["profiles"].append({"name": "agents/plan-reviewer/agent.md", "ownerId": "fixture:architect"})
        declare_returned_contributions(self.contract)
        self.refresh()
        with self.assertRaisesRegex(ValueError, "independent duty shares"):
            self.validate()

    def test_adopted_preparation_authorship_changes_invalidate_criticism_binding(self):
        self.state("plan")["authorIds"].append("fixture:executor")
        with self.assertRaisesRegex(ValueError, "criticism does not cover the exact"):
            self.validate()

    def test_coordinator_can_finalize_plan_with_real_worker_coauthor_without_solo_implementation(self):
        selected = self.contract["selection"]
        selected["delegation"]["assignments"].insert(0, fixture_assignment("plan", BUILDER, identity="plan-coauthor", capabilities=["plan-code"]))
        self.state("plan")["authorIds"].append("fixture:executor")
        self.contract["roster"]["assignments"].append({"assignmentId": "plan-coauthor", "workerId": "fixture:executor"})
        self.contract["roster"]["profiles"].append({"name": BUILDER, "ownerId": "fixture:executor"})
        declare_returned_contributions(self.contract)
        self.refresh()
        self.assertEqual(self.state("plan")["ownerId"], "fixture:coordinator")
        self.assertTrue(self.validate()["admitted"])
        self.state("execute").update(ownerId="fixture:coordinator", authorIds=["fixture:coordinator", "fixture:executor"])
        self.refresh()
        with self.assertRaisesRegex(ValueError, "actual assigned workers"):
            self.validate()

    def test_queued_future_executor_does_not_fake_a_running_or_returned_worker(self):
        self.state("execute").update(status="pending", ownerId=None, authorIds=[])
        self.contract["progress"]["currentPhase"] = "critique"
        roster = self.contract["roster"]
        roster["assignments"] = [row for row in roster["assignments"] if row["assignmentId"] != "execute"]
        roster["workers"] = [row for row in roster["workers"] if row["id"] != "fixture:executor"]
        roster["profiles"] = [row for row in roster["profiles"] if row["ownerId"] != "fixture:executor"]
        roster.update(activeAgentCount=1, plannedWorkers=[{"role": "Builder", "phaseIds": ["execute"]}])
        self.refresh()
        self.assertEqual(self.validate()["returnedContributors"], 1)
        with self.assertRaisesRegex(ValueError, "completion requires"):
            self.validate(completing=True)

    def test_plan_and_standalone_reviewer_task_have_two_actual_useful_results(self):
        for mode in ("plan", "review"):
            with self.subTest(mode=mode):
                _, data = fixture(self.project, suffix="readonly-" + mode)
                record = self.project / "documents/tasks/development" / ("2026-09-07-00001-readonly-" + mode)
                contract = make_readonly_contract(record, data, mode, complete=True)
                if mode == "review":
                    contract["selection"]["workflow"] = "GVR"
                    primary = next(row for row in contract["selection"]["delegation"]["assignments"] if row["phaseId"] == "inspect")
                    primary.update(profile=REVIEWER, capabilities=["review-code"])
                    next(row for row in contract["selection"]["phases"] if row["id"] == "inspect")["operation"] = "review-code"
                    contract["roster"]["profiles"].append({"name": REVIEWER, "ownerId": "fixture:executor"})
                    declare_returned_contributions(contract)
                    refresh_contract(record, data)
                result = validate_contract(record, data, require_product_write=False, completing=True)
                self.assertEqual(result["returnedContributors"], 2)
                self.assertFalse(result["admitted"])

    def test_material_and_shared_ui_require_distinct_advice_and_full_ui_checks(self):
        selected = self.contract["selection"]
        selected["uiContext"] = {"applicable": True, "kind": "design", "reason": "The fixture requests new layout decisions and state behavior."}
        selected["delegation"]["assignments"][1]["capabilities"].append("ui-design")
        selected["delegation"]["assignments"][2]["capabilities"] += ["ui-design", "review-ui"]
        with self.assertRaisesRegex(ValueError, "distinct UI Director"):
            self.validate()
        self.add_advice("design", UI_DIRECTOR, "design-ui", "fixture:ui-director")
        self.finish()
        self.assertEqual(self.validate(completing=True)["requiredContributors"], 3)
        selected["uiContext"]["kind"] = "shared"
        selected["routing"].update(impact="cross-cutting", changedSharedContract=True)
        self.add_advice("architecture", ARCHITECT, "design-architecture", "fixture:architect")
        self.finish()
        self.assertEqual(self.validate(completing=True)["requiredContributors"], 4)

    def test_substantial_validation_adds_a_distinct_verifier_before_acceptance(self):
        selected = self.contract["selection"]
        selected["verificationContext"] = {"required": True, "triggers": ["lifecycle"], "reason": "A fresh installation lifecycle is an explicit deliverable."}
        with self.assertRaisesRegex(ValueError, "distinct Verification Engineer"):
            self.validate()
        selected["phases"].insert(-1, {"id": "lifecycle", "title": "Verify installation lifecycle", "kind": "verify", "operation": "run-tests",
                                       "writeScope": "test-output-only", "owner": "Verifier", "dependsOn": ["verify"]})
        selected["phases"][-1]["dependsOn"] = ["lifecycle"]
        selected["delegation"]["assignments"].append(fixture_assignment("lifecycle", VERIFIER, ["plan", "execute"], capabilities=["run-tests"]))
        self.contract["progress"]["phases"].insert(-1, {"id": "lifecycle", "status": "pending", "ownerId": None, "authorIds": [], "evidence": [], "workHash": None})
        self.refresh()
        self.assertTrue(self.validate()["admitted"], "Future Verifier may wait for a slot before its phase is due")
        self.state("lifecycle").update(status="complete", ownerId="fixture:verifier", evidence=["fixture:lifecycle-result"])
        self.contract["roster"]["workers"].append({"id": "fixture:verifier", "role": "Verification Engineer", "status": "completed", "evidence": ["fixture:verifier-dispatch-and-result"]})
        self.contract["roster"]["profiles"].append({"name": VERIFIER, "ownerId": "fixture:verifier"})
        self.contract["roster"]["assignments"].append({"assignmentId": "lifecycle", "workerId": "fixture:verifier"})
        self.finish()
        self.assertEqual(self.validate(completing=True)["requiredContributors"], 3)

    def test_publication_cannot_borrow_future_or_unrelated_verifier_duty(self):
        selected = self.contract["selection"]
        selected["verificationContext"] = {"required": True, "triggers": ["lifecycle"],
                                            "reason": "Fresh installation is a required acceptance prerequisite."}
        specifications = [
            (3, "source-inspection", "other", "research-technical", "read-only", ["critique"], INVESTIGATOR, [], "fixture:third", True),
            (-1, "lifecycle", "verify", "run-tests", "test-output-only", ["verify"], VERIFIER, ["plan", "execute"], "fixture:critic", True),
        ]
        for index, identity, kind, operation, scope, dependencies, profile, independent, actor, complete in specifications:
            selected["phases"].insert(index, {"id": identity, "title": identity.title(), "kind": kind,
                "operation": operation, "writeScope": scope, "owner": "assigned worker", "dependsOn": dependencies})
            self.contract["progress"]["phases"].insert(index, {"id": identity, "status": "complete", "ownerId": actor,
                "authorIds": [], "evidence": ["fixture:" + identity + "-result"], "workHash": None})
            selected["delegation"]["assignments"].append(fixture_assignment(identity, profile, independent, capabilities=[operation]))
            self.contract["roster"]["assignments"].append({"assignmentId": identity, "workerId": actor})
            self.contract["roster"]["profiles"].append({"name": profile, "ownerId": actor})
        next(row for row in selected["phases"] if row["id"] == "execute")["dependsOn"].append("source-inspection")
        next(row for row in selected["phases"] if row["id"] == "accept")["dependsOn"] = ["lifecycle"]
        self.contract["roster"]["workers"].append({"id": "fixture:third", "role": "Investigator with future readback duty",
            "status": "completed", "evidence": ["fixture:third-actual-inspection-result"]})
        for identity, kind, operation, scope, dependencies in [
            ("publish", "execute", "publish-result", "external-write", ["accept"]),
            ("readback", "verify", "run-tests", "test-output-only", ["publish"]),
        ]:
            selected["phases"].append({"id": identity, "title": identity.title(), "kind": kind, "operation": operation,
                "writeScope": scope, "owner": "coordinator" if identity == "publish" else "Verifier", "dependsOn": dependencies})
            self.contract["progress"]["phases"].append({"id": identity, "status": "in-progress" if identity == "publish" else "pending",
                "ownerId": "fixture:coordinator" if identity == "publish" else None, "authorIds": [], "evidence": [], "workHash": None})
        selected["delegation"]["assignments"].append(fixture_assignment("readback", VERIFIER, ["plan", "execute"], capabilities=["run-tests"]))
        self.contract["roster"]["assignments"].append({"assignmentId": "readback", "workerId": "fixture:third"})
        self.contract["roster"]["profiles"].append({"name": VERIFIER, "ownerId": "fixture:third"})
        self.finish()
        self.contract["progress"]["currentPhase"] = "publish"
        self.refresh()
        with self.assertRaisesRegex(ValueError, "separate Verifier's completed final-result prerequisite"):
            self.validate()

        # A completed Verifier duty on the old source still cannot corroborate
        # the final result accepted by that same Reviewer actor.
        early = next(row for row in selected["delegation"]["assignments"] if row["id"] == "source-inspection")
        early.update(profile=VERIFIER, capabilities=["run-tests"])
        next(row for row in selected["phases"] if row["id"] == "source-inspection")["operation"] = "run-tests"
        declare_returned_contributions(self.contract)
        self.refresh()
        with self.assertRaisesRegex(ValueError, "separate Verifier's completed final-result prerequisite"):
            self.validate()

        # The distinct actor now actually returns the required final-result
        # lifecycle check. Post-publication readback remains honestly pending.
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "lifecycle")["workerId"] = "fixture:third"
        self.state("lifecycle")["ownerId"] = "fixture:third"
        declare_returned_contributions(self.contract)
        self.refresh()
        self.assertTrue(self.validate()["admitted"])
        self.assertEqual(self.state("readback")["status"], "pending")
        final_check = next(row for row in self.contract["contributions"] if row["assignmentId"] == "lifecycle")
        for revision in (None, "fixture:old-result"):
            final_check["resultRevision"] = revision
            self.refresh()
            with self.assertRaisesRegex(ValueError, "substantial verification is not bound"):
                self.validate()

    def test_readonly_approach_critique_cannot_replace_result_countercheck(self):
        make_readonly_contract(self.record, self.data, "review", complete=True)
        self.assertTrue(self.validate(require_product_write=False, completing=True)["completionValidated"])
        selected = self.contract["selection"]
        selected["phases"] = [row for row in selected["phases"] if row["id"] != "corroborate"]
        next(row for row in selected["phases"] if row["id"] == "report")["dependsOn"] = ["inspect"]
        selected["delegation"]["assignments"] = [row for row in selected["delegation"]["assignments"] if row["phaseId"] != "corroborate"]
        self.contract["progress"]["phases"] = [row for row in self.contract["progress"]["phases"] if row["id"] != "corroborate"]
        self.contract["progress"]["currentPhase"] = "inspect"
        with self.assertRaisesRegex(ValueError, "actual primary result"):
            self.validate(require_product_write=False, completing=True)

    def test_standalone_plan_review_corroborates_the_actual_review(self):
        make_readonly_contract(self.record, self.data, "review", complete=True)
        selected = self.contract["selection"]
        selected["workflow"] = "GPR"
        selected["phases"] = [row for row in selected["phases"] if row["id"] != "inspect"]
        next(row for row in selected["phases"] if row["id"] == "critique")["operation"] = "review-plan"
        next(row for row in selected["phases"] if row["id"] == "corroborate")["dependsOn"] = ["critique"]
        selected["delegation"]["assignments"] = [row for row in selected["delegation"]["assignments"] if row["phaseId"] != "inspect"]
        next(row for row in selected["delegation"]["assignments"] if row["phaseId"] == "corroborate")["independentFrom"] = ["plan", "critique"]
        self.contract["progress"]["phases"] = [row for row in self.contract["progress"]["phases"] if row["id"] != "inspect"]
        self.state("corroborate")["ownerId"] = "fixture:executor"
        self.contract["roster"]["assignments"] = [row for row in self.contract["roster"]["assignments"] if row["assignmentId"] != "inspect"]
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "corroborate")["workerId"] = "fixture:executor"
        self.contract["roster"]["profiles"].append({"name": "agents/code-reviewer/agent.md", "ownerId": "fixture:executor"})
        declare_returned_contributions(self.contract)
        self.refresh()
        self.assertTrue(self.validate(require_product_write=False, completing=True)["completionValidated"])

    def test_named_approach_review_cannot_be_corroborated_instead_of_later_inspection(self):
        make_readonly_contract(self.record, self.data, "review", complete=True)
        selected = self.contract["selection"]
        next(row for row in selected["phases"] if row["id"] == "critique")["operation"] = "review-plan"
        next(row for row in selected["delegation"]["assignments"] if row["phaseId"] == "corroborate")["independentFrom"] = ["critique"]
        self.state("corroborate")["ownerId"] = "fixture:executor"
        next(row for row in self.contract["roster"]["assignments"] if row["assignmentId"] == "corroborate")["workerId"] = "fixture:executor"
        self.contract["roster"]["profiles"].append({"name": "agents/code-reviewer/agent.md", "ownerId": "fixture:executor"})
        with self.assertRaisesRegex(ValueError, "actual primary result"):
            self.validate(require_product_write=False, completing=True)

    def test_capture_only_selection_keeps_its_bounded_countercheck_without_extra_stage(self):
        selected = copy.deepcopy(self.contract["selection"])
        selected.update(workflow="0", mode="review")
        selected["phases"] = [
            {"id": "source", "title": "Capture requested source", "kind": "capture", "operation": "assess-codebase",
             "writeScope": "record-only", "owner": "Investigator", "dependsOn": []},
            {"id": "check", "title": "Corroborate captured source", "kind": "verify", "operation": "review-code",
             "writeScope": "read-only", "owner": "Reviewer", "dependsOn": ["source"]},
        ]
        selected["delegation"]["assignments"] = [
            fixture_assignment("source", INVESTIGATOR, capabilities=["assess-codebase"]),
            fixture_assignment("check", REVIEWER, ["source"], capabilities=["review-code"]),
        ]
        _, phases = contract_selection({"schema": SCHEMA, "selection": selected})
        self.assertEqual(list(phases), ["source", "check"])
        self.assertFalse(any(row["kind"] == "plan" or row["writeScope"] in {"repo-write-scoped", "external-write"} for row in phases.values()))

    def test_migration_proposal_preserves_old_evidence_without_claiming_v2_admission(self):
        old = copy.deepcopy(self.contract)
        old["schema"] = LEGACY_SCHEMA
        old.pop("contributions")
        original = copy.deepcopy(old)
        proposal = migration_proposal(old)
        self.assertEqual(old, original)
        self.assertFalse(proposal["executionAdmitted"])
        new = proposal["proposedContract"]
        self.assertEqual(new["schema"], SCHEMA)
        self.assertEqual(new["roster"]["workers"], old["roster"]["workers"])
        self.assertEqual(new["legacyEvidence"]["contract"], original)
        self.assertEqual(new["contributions"], [])
        self.assertEqual(new["review"]["status"], "pending")
        with self.assertRaises(ValueError):
            validate_contract(self.record, self.data, new)

    def test_completion_cli_is_read_only_and_does_not_grant_execution(self):
        self.finish()
        source = self.record / "record.json"
        source.write_text(json.dumps(self.data))
        before = source.read_bytes()
        result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/workflow_contract.py"), "validate",
                                 "--record", str(self.record), "--completion"], capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        response = json.loads(result.stdout)
        self.assertTrue(response["completionValidated"])
        self.assertFalse(response["executionAdmitted"])
        self.assertFalse(response["admitted"])
        self.assertEqual(source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
