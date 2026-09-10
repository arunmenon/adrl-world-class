"""Check scoped implementation/register closure. Primary: ADRL-FND-005.

Secondary: ADRL-EVL-009. Standard-library local gate, not remote branch protection.
Private-key/cache exclusions follow core's engineering runner. Reports and runtime
payloads are excluded from the walk; evidence/review references are pinned separately.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

SCOPE = {
    "R": {
        "dirs": ["adr", "tools", "tests", "skills", "design", "profiles"],
        "files": [
            "AGENTS.md",
            "README.md",
            "INDEX.md",
            "CHANGELOG.md",
            "reports/adrl-wave-execution-template.md",
        ],
    },
    "C": {
        "dirs": ["src", "tests", "tools", "config", "docs", "api", "artifacts"],
        "files": [
            "AGENTS.md",
            "CLAUDE.md",
            "README.md",
            "pyproject.toml",
            "uv.lock",
            ".gitignore",
        ],
    },
}
EXCLUSIONS = "reports except wave template; source history; .project; .git; runtime data; .env*, *.key, *.pem, *.pyc and cache directories. Expand the reviewed tool scope before changing excluded engineering inputs."
FIELDS = ("Status", "Maturity", "Review verdict")
ADR = re.compile(r"ADRL-[A-Z]{3}-\d{3}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(root: Path, name: str) -> Path:
    part = Path(name)
    if part.is_absolute() or ".." in part.parts:
        raise ValueError(f"unsafe relative path: {name}")
    p = root
    for item in part.parts:
        p = p / item
        if p.is_symlink():
            raise ValueError(f"symlink not permitted: {p}")
    return p


def fields(text: str) -> dict[str, str]:
    result = {}
    for key in FIELDS:
        rows = re.findall(
            r"^\| " + re.escape(key) + r" \| (.*?) \|\s*$", text, re.MULTILINE
        )
        if len(rows) != 1:
            raise ValueError(f"expected one {key} field")
        result[key] = rows[0]
    return result


def snapshot(roots: dict[str, Path]) -> dict:
    files, metadata = {}, {}
    for tag, root in roots.items():
        if root.is_symlink() or not root.is_dir():
            raise ValueError(f"invalid root: {root}")
        paths = [safe(root, n) for n in SCOPE[tag]["files"]]
        for n in SCOPE[tag]["dirs"]:
            directory = safe(root, n)
            if directory.exists():
                paths.extend(directory.rglob("*"))
        for p in sorted(set(paths)):
            rel = p.relative_to(root)
            if set(rel.parts) & {
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
                ".ruff_cache",
            }:
                continue
            if p.name.startswith(".env") or p.suffix in {".key", ".pem", ".pyc"}:
                continue
            safe(root, str(rel))
            if p.is_file():
                key = tag + ":" + rel.as_posix()
                files[key] = digest(p)
                if tag == "R" and rel.parts[0] == "adr" and ADR.fullmatch(p.stem):
                    metadata[p.stem] = fields(p.read_text())
    return {
        "schema": "adrl-sync-baseline-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "roots": {k: str(v) for k, v in roots.items()},
        "scope": SCOPE,
        "exclusions": EXCLUSIONS,
        "files": files,
        "fields": metadata,
    }


def pin(root: Path, ref: dict) -> Path:
    p = safe(root, ref["path"])
    if not p.is_file() or digest(p) != ref["sha256"]:
        raise ValueError(f"missing/stale pinned reference: {ref['path']}")
    return p


def linked(line: str, doc: Path, target: Path) -> bool:
    for raw in re.findall(r"\]\(([^)]+)\)", line):
        path = raw.strip("<>").split("#")[0]
        if "://" not in path and (doc.parent / path).resolve() == target.resolve():
            return True
    return False


def coverage(root: Path, known: set[str], buckets: set[str]) -> None:
    index = (root / "INDEX.md").read_text()
    rows = re.findall(r"^\| \[(ADRL-[A-Z]{3}-\d{3})\]", index, re.MULTILINE)
    if len(rows) != len(set(rows)) or set(rows) != known:
        raise ValueError("INDEX missing/duplicate/unknown ADR rows")
    for bucket in sorted(buckets):
        text = (root / "adr" / bucket / "README.md").read_text()
        rows = re.findall(r"^\| \[?(ADRL-[A-Z]{3}-\d{3})(?:\]| \|)", text, re.MULTILINE)
        expected = {a for a in known if a.split("-")[1] == bucket}
        if len(rows) != len(set(rows)) or set(rows) != expected:
            raise ValueError(f"bucket {bucket} missing/duplicate/unknown ADR rows")


def check(roots: dict[str, Path], baseline: dict, packet: dict) -> dict:
    current = snapshot(roots)
    if (
        baseline["schema"] != current["schema"]
        or baseline["scope"] != SCOPE
        or baseline["roots"] != current["roots"]
    ):
        raise ValueError("baseline schema/scope/roots mismatch")
    if not baseline.get("fields"):
        raise ValueError("baseline lacks preserved ADR fields")
    before, after = baseline["files"], current["files"]
    delta = {
        k: {"before": before.get(k), "after": after.get(k)}
        for k in before.keys() | after.keys()
        if before.get(k) != after.get(k)
    }
    if not delta or packet["changes"] != delta:
        raise ValueError(
            "changed-file manifest incomplete or stale (includes additions/deletions)"
        )
    owners = packet["owners"]
    if not owners or len({o["id"] for o in owners}) != len(owners):
        raise ValueError("empty/duplicate owner records")
    ids = {o["id"] for o in owners}
    known = set(current["fields"])
    if not ids <= known:
        raise ValueError("unknown/deleted owning ADR")
    coverage(roots["R"], known, {a.split("-")[1] for a in ids})
    derived = {"R:INDEX.md", "R:CHANGELOG.md"}
    for aid in ids:
        derived |= {
            f"R:adr/{aid.split('-')[1]}/{aid}.md",
            f"R:adr/{aid.split('-')[1]}/README.md",
        }
    required = set(delta) - derived
    if set(packet["file_owners"]) != required:
        raise ValueError("missing/extra file ownership mapping")
    used = set()
    for name, mapped in packet["file_owners"].items():
        if not mapped or not set(mapped) <= ids:
            raise ValueError(f"unmapped input: {name}")
        if name.startswith("R:adr/"):
            raise ValueError(f"unexplained register edit: {name}")
        used.update(mapped)
    if used != ids:
        raise ValueError("owner has no mapped input")
    wave = packet["wave"]
    if not re.fullmatch(r"[a-z0-9-]+", wave):
        raise ValueError("invalid wave identifier")
    date.fromisoformat(packet["date"])
    for owner in owners:
        aid = owner["id"]
        if (
            owner["kind"] not in {"behavior", "evidence", "refactor", "workflow"}
            or not owner["summary"].strip()
            or not owner["limitations"].strip()
        ):
            raise ValueError("owner requires change kind, summary and limitations")
        if owner["fields"] != current["fields"][aid]:
            raise ValueError(f"stale ADR fields: {aid}")
        if baseline["fields"].get(aid) != current["fields"][aid]:
            auth = json.loads(pin(roots["R"], owner["field_change_record"]).read_text())
            if (
                auth["adr"] != aid
                or auth["before"] != baseline["fields"].get(aid)
                or auth["after"] != current["fields"][aid]
                or not auth["human_name"].strip()
            ):
                raise ValueError("invalid status/maturity/verdict disposition")
            date.fromisoformat(auth["date"])
        if not owner["evidence"]:
            raise ValueError("evidence required")
        evidence = [pin(roots["R"], ref) for ref in owner["evidence"]]
        marker = f"<!-- taxonomy-sync:{wave}:{aid} -->"
        docs = [
            f"adr/{aid.split('-')[1]}/{aid}.md",
            "INDEX.md",
            f"adr/{aid.split('-')[1]}/README.md",
            "CHANGELOG.md",
        ]
        for name in docs:
            doc = safe(roots["R"], name)
            if "R:" + name not in delta:
                raise ValueError(f"register not updated: {name}")
            lines = [
                line
                for line in doc.read_text().splitlines()
                if marker in line and packet["date"] in line
            ]
            if name == "INDEX.md" or name.endswith("README.md"):
                lines = [
                    line
                    for line in lines
                    if line.startswith("| ") and aid in line.split("|")[1]
                ]
            if not any(linked(line, doc, evidence[0]) for line in lines):
                raise ValueError(f"missing dated evidence mapping: {name} {aid}")
            if name.endswith(aid + ".md") and not any(
                line.startswith("| ") for line in lines
            ):
                raise ValueError(f"ADR changelog row missing: {aid}")
    review = packet["review"]
    pin(roots["R"], review["record"])
    reviewed = json.loads(pin(roots["R"], review["inputs"]).read_text())
    if reviewed != after:
        raise ValueError("reviewed source drift")
    if (
        review["status"] != "accepted"
        or not review["reviewer"].strip()
        or set(review["covered_adrs"]) != ids
    ):
        raise ValueError("review_pending or incomplete semantic coverage")
    if review.get("blocking_findings") != []:
        raise ValueError("unresolved review blockers")
    canonical = safe(roots["R"], "skills/adrl-taxonomy-sync/SKILL.md")
    expected_mirrors = [
        Path.home() / ".codex/skills/adrl-taxonomy-sync/SKILL.md",
        Path.home() / ".claude/skills/adrl-taxonomy-sync/SKILL.md",
    ]
    for mirror in expected_mirrors:
        if (
            mirror.is_symlink()
            or not mirror.is_file()
            or mirror.read_bytes() != canonical.read_bytes()
        ):
            raise ValueError(f"missing/drifted installed skill: {mirror}")
    return {
        "status": "passed",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "changed_files": sorted(delta),
        "owning_adrs": sorted(ids),
        "source": after,
        "exclusions": EXCLUSIONS,
        "bucket_coverage_scope": "Affected buckets only; global INDEX IDs checked. Historical unrelated bucket defects remain open.",
        "limitations": "Local declared-scope check plus reviewer attestations; not semantic proof, historical-grade reconciliation or tamper-proof CI enforcement. Rerun after any input/evidence/review change.",
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["begin", "check"])
    p.add_argument("--register", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--core", type=Path)
    p.add_argument("--baseline", type=Path)
    p.add_argument("--packet", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    roots = {
        "R": a.register.absolute(),
        "C": (a.core or a.register.parent / "adrl-core").absolute(),
    }
    try:
        if a.out.exists():
            raise ValueError("output exists; preserve old receipts")
        if a.command == "check" and any(
            a.out.resolve().is_relative_to(root.resolve()) for root in roots.values()
        ):
            raise ValueError("closure receipt must be outside both repositories")
        if a.command == "begin":
            # Keep baseline outside scanned inputs to avoid self-reference.
            if any(
                a.out.resolve().is_relative_to(root.resolve())
                for root in roots.values()
            ):
                raise ValueError("baseline output must be outside both repositories")
            result = snapshot(roots)
        else:
            if not a.baseline or not a.packet:
                raise ValueError("check requires --baseline and --packet")
            result = check(
                roots,
                json.loads(a.baseline.read_text()),
                json.loads(a.packet.read_text()),
            )
            result["baseline_sha256"] = digest(a.baseline)
            result["packet_sha256"] = digest(a.packet)
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(result.get("status", "baseline recorded"))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f"taxonomy_sync: FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
