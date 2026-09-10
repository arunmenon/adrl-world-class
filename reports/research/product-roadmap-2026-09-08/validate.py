"""Read-only verification of the product-planning synchronization."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import datetime
import hashlib
import json
import re
import tomllib

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BACKUP = ROOT / ".codex-executive-build/product-roadmap-planning-backup"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decision(text):
    match = re.search(r"^## Decision\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    assert match
    return match.group(1).strip()


def grades(text):
    return [s for s in text.splitlines() if re.match(r"\| (Status|Maturity) \|", s)]


backup = json.loads((BACKUP / "manifest.json").read_text())["files"]
backup_errors = [p for p, m in backup.items() if digest(BACKUP / p) != m["sha256"]]
adr_files = sorted(ROOT.glob("adr/*/ADRL-*.md"))
decision_errors = []
grade_errors = []
for path in adr_files:
    previous = (BACKUP / path.relative_to(ROOT)).read_text()
    current = path.read_text()
    if decision(previous) != decision(current):
        decision_errors.append(str(path.relative_to(ROOT)))
    if grades(previous) != grades(current):
        grade_errors.append(str(path.relative_to(ROOT)))

baseline_path = ROOT / "reports/research/adrl-w3-transport-receipts-2026-09-08.json"
baseline = json.loads(baseline_path.read_text())
runtime_errors = [
    name for name, meta in baseline["source_after"].items()
    if digest(ROOT.parent / "adrl-core" / name) != meta["sha256"]
]
index = (ROOT / "INDEX.md").read_text()
index_errors = [p.stem for p in adr_files if p.stem not in index]
new_docs = [
    "reports/adrl-product-roadmap-2026-09-08.md",
    "reports/adrl-startup-investment-brief-2026-09-08.md",
    "design/adrl-context-graph-memory-proposal-2026-09-08.md",
]
changed = [p for p, m in backup.items() if digest(ROOT / p) != m["sha256"]]
markdown = [ROOT / p for p in changed + new_docs if p.endswith(".md")]
link_errors = []
links = 0


def anchors(path):
    result = set()
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", path.read_text(), re.M):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        result.add(slug if n == 0 else f"{slug}-{n}")
    return result


for path in markdown:
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text()):
        target = target.strip().strip("<>")
        if urlsplit(target).scheme:
            continue
        raw, _, anchor = target.partition("#")
        local = (path.parent / unquote(raw)).resolve() if raw else path
        links += 1
        if not local.exists():
            link_errors.append({"file": str(path.relative_to(ROOT)), "target": target})
        elif anchor and local.suffix == ".md" and unquote(anchor) not in anchors(local):
            link_errors.append({"file": str(path.relative_to(ROOT)), "target": target,
                                "reason": "heading anchor missing"})

state = json.loads((ROOT / "reports/research/adrl-execution-state.json").read_text())
automation_path = Path("/Users/arunmenon/.codex/automations/continue-adrl-implementation-waves/automation.toml")
automation = tomllib.loads(automation_path.read_text())
assert state["automation"]["status"] == "paused"
assert str(automation["status"]).lower() == "paused"
assert state["paid_api_budget_approved"] is False
assert state["live_routing_exposure_approved"] is False
assert state["automatic_graduation"] is False

economics = [
    {"coverage": c, "reduction": s, "gross_saving": 40000*c*s,
     "net_saving": 40000*c*s-2500}
    for c, s in [(0.25, 0.10), (0.50, 0.20), (0.75, 0.30)]
]
assert [r["net_saving"] for r in economics] == [-1500, 1500, 6500]
assert (4*3*15000+15000+15000+15000)*1.2 == 270000
assert 2500/(0.5*0.2) == 25000

result = {
    "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Documentation/planning verification; no runtime suite rerun",
    "backup_files_checked": len(backup), "backup_errors": backup_errors,
    "adrs_checked": len(adr_files), "decision_text_errors": decision_errors,
    "status_maturity_errors": grade_errors, "index_coverage_errors": index_errors,
    "runtime_inputs_checked": len(baseline["source_after"]), "runtime_hash_errors": runtime_errors,
    "reused_runtime_tests_passed": baseline["final_tests_passed"],
    "reused_runtime_check_count": baseline["check_count"],
    "local_markdown_links_checked": links, "link_errors": link_errors,
    "changed_backed_up_files": changed,
    "new_document_hashes": {p: digest(ROOT / p) for p in new_docs},
    "current_planning_source_hashes": {p: digest(ROOT / p) for p in changed},
    "source_ledger_sha256": digest(OUT / "sources.json"),
    "automation_status": automation["status"],
    "runtime_changed": False, "maturity_promotions": 0, "model_calls": 0,
    "new_paid_usage": False, "customer_outreach": False,
    "illustrative_economics_recomputed": economics,
}
result["passed"] = (
    len(adr_files) == 77 and len(baseline["source_after"]) == 316
    and not any([backup_errors, decision_errors, grade_errors, index_errors,
                 runtime_errors, link_errors])
)
(OUT / "validation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in [
    "passed", "adrs_checked", "runtime_inputs_checked", "local_markdown_links_checked",
    "automation_status", "link_errors", "decision_text_errors", "status_maturity_errors",
    "runtime_hash_errors", "index_coverage_errors"]}, indent=2))
raise SystemExit(0 if result["passed"] else 1)
