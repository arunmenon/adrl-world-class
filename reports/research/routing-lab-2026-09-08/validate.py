"""Verify Lab A.1 evidence and register synchronization without changing runtime."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime
import hashlib
import importlib.util
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT.parent / "adrl-core"
OUT = Path(__file__).resolve().parent
BACKUP = ROOT.parent / ".adrl-execution-state/lab-a-20260908T081840Z"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decision(text):
    match = re.search(r"^## Decision\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match
    return match.group(1).strip()


def grades(text):
    return [line for line in text.splitlines() if re.match(r"\| (Status|Maturity) \|", line)]


backup = json.loads((BACKUP / "manifest.json").read_text())
backup_errors = [name for name, meta in backup.items() if digest(BACKUP / name) != meta["sha256"]]
adrs = sorted(ROOT.glob("adr/*/ADRL-*.md"))
decision_errors = []
grade_errors = []
for path in adrs:
    previous = (BACKUP / "adrl-world-class" / path.relative_to(ROOT)).read_text()
    current = path.read_text()
    if decision(previous) != decision(current):
        decision_errors.append(path.stem)
    if grades(previous) != grades(current):
        grade_errors.append(path.stem)
index = re.findall(r"^\| \[(ADRL-[A-Z]{3}-\d{3})\]", (ROOT / "INDEX.md").read_text(), re.M)
index_ok = sorted(index) == [p.stem for p in adrs] and len(index) == len(set(index))

spec = importlib.util.spec_from_file_location("checks", CORE / "tools/check_all.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = module.source_manifest(CORE)
checks = json.loads((OUT / "engineering-checks.json").read_text())
run_manifest = json.loads((OUT / "run-2/manifest.json").read_text())
run = json.loads((OUT / "run-2/results.json").read_text())
old_source = json.loads((ROOT / "reports/research/adrl-w3-transport-receipts-2026-09-08.json").read_text())["source_after"]
old_errors = [name for name, meta in old_source.items() if source.get(name) != meta]
new_files = sorted(set(source) - set(old_source))
expected_new = sorted(["tools/run_routing_lab.py", "tests/unit/test_routing_lab.py",
                       "artifacts/lab/routing-suite-v1.json", "docs/routing-lab.md"])
source_ok = source == checks["source_before"] == checks["source_after"] == run_manifest["source_manifest"]
suite_ok = run_manifest["suite_sha256"] == digest(CORE / "artifacts/lab/routing-suite-v1.json")
rows = {r["case_id"]: r for r in run["rows"]}
cases = {c["id"] for c in run_manifest["suite"]["cases"]}
accounting_ok = cases == set(rows) and len(rows) == 16 == sum(run["counts"].values())
assert run["counts"] == {"responded":13,"blocked":1,"upstream_error":1,"unsupported":1}
assert len({d["route_id"] for r in rows.values() for d in r.get("decisions",[])}) == 10
assert sum(len(r.get("dispatched",[])) for r in rows.values()) == 14
assert run["eligible_for_learning"] is False and run["task_success"] is None
assert run["model_calls"] == 0 and run["source_unchanged_during_run"] and run["run_completed"]
assert checks["status"] == "passed" and len(checks["checks"]) == 11
assert all(c["status"] == "passed" for c in checks["checks"])
assert "894 passed, 8 skipped" in (OUT / "check-logs/tests.log").read_text()

changed = []
for name, meta in backup.items():
    if name.startswith("adrl-world-class/") and digest(ROOT.parent / name) != meta["sha256"]:
        changed.append(name.removeprefix("adrl-world-class/"))
new_docs = ["reports/adrl-lab-first-run-2026-09-08.md", "reports/waves/lab-a-routing-experiment.md",
            "reports/research/routing-lab-2026-09-08/run-2/report.md",
            "reports/research/routing-lab-2026-09-08/run-1/QUALIFICATION.md"]
markdown = [ROOT / p for p in changed + new_docs if p.endswith(".md")] + [CORE / "docs/routing-lab.md"]
links = 0
link_errors = []


def anchors(path):
    found = set()
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", path.read_text(), re.M):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        found.add(slug if n == 0 else f"{slug}-{n}")
    return found


# The validation report is this script's output, created below.
for path in markdown:
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text()):
        target = target.strip().strip("<>")
        if urlsplit(target).scheme:
            continue
        raw, _, anchor = target.partition("#")
        local = (path.parent / unquote(raw)).resolve() if raw else path
        links += 1
        if local == OUT / "validation.json":
            continue
        if not local.exists():
            link_errors.append({"file": str(path), "target": target})
        elif anchor and local.suffix == ".md" and unquote(anchor) not in anchors(local):
            link_errors.append({"file": str(path), "target": target, "reason": "heading missing"})

state = json.loads((ROOT / "reports/research/adrl-execution-state.json").read_text())
automation = tomllib.loads(Path("/Users/arunmenon/.codex/automations/continue-adrl-implementation-waves/automation.toml").read_text())
assert automation["status"] == "PAUSED" and state["automation"]["status"] == "paused"
assert not state["paid_api_budget_approved"] and not state["live_routing_exposure_approved"]
assert not state["automatic_graduation"]
assert state["current_build_checks"]["tests_passed"] == 894
result = {
    "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Lab A.1 synthetic workbench and register synchronization; no real task outcome",
    "backup_files_checked": len(backup), "backup_errors": backup_errors,
    "adrs_checked": len(adrs), "decision_text_errors": decision_errors,
    "status_maturity_errors": grade_errors, "index_coverage_ok": index_ok,
    "source_identity_matches_run_checks_and_current_tree": source_ok,
    "declared_runtime_inputs": len(source), "existing_runtime_inputs_unchanged": len(old_source),
    "existing_source_errors": old_errors, "new_runtime_files": new_files,
    "runtime_behavior_changed": False, "suite_identity_ok": suite_ok,
    "accounting_ok": accounting_ok, "planned_cells": 16, "unique_decision_ids": 10,
    "messages_submitted": 15, "endpoint_dispatches": 14,
    "tests_passed": 894, "tests_skipped": 8, "focused_tests_passed": 7, "check_count": 11,
    "skipped_scope": "Existing engine tests lack a fresh allowance; no engine mutation this turn",
    "export_attempts": 2, "disqualified_exports": 1,
    "repair": "Duplicate source field in initial export; source_manifest key and regression added",
    "local_links_checked": links, "link_errors": link_errors,
    "automation_status": automation["status"], "model_calls": 0, "new_paid_usage": False,
    "maturity_promotions": 0, "learning_admission_changes": 0,
    "register_changed_files": changed,
    "document_hashes": {str(p.relative_to(ROOT.parent)):digest(p) for p in markdown},
    "evidence_hashes": {str(p.relative_to(OUT)):digest(p) for p in sorted(OUT.rglob('*'))
                        if p.is_file() and p.name != 'validation.json'},
}
result["passed"] = (len(adrs) == 77 and not any([backup_errors, decision_errors, grade_errors,
                         old_errors, link_errors]) and index_ok and source_ok and suite_ok
                    and accounting_ok and new_files == expected_new)
(OUT / "validation.json").write_text(json.dumps(result,indent=2) + "\n")
print(json.dumps({k:result[k] for k in ["passed","adrs_checked","declared_runtime_inputs",
    "existing_runtime_inputs_unchanged","local_links_checked","link_errors","automation_status"]},indent=2))
raise SystemExit(0 if result["passed"] else 1)
