"""Verify the append-only review ledger under reports/reviews (schema review-ledger-v1).

Fails when an immutable file's hash differs from its folder manifest, when LEDGER.jsonl or a
dispositions.jsonl has lost or reordered lines relative to the hashes recorded in the ledger,
when a finding id is duplicated or a disposition references an unknown finding, when a review
folder is absent from the ledger, or when a legacy folder's registered hashes changed.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REVIEWS = ROOT / "reports" / "reviews"
LEDGER = REVIEWS / "LEDGER.jsonl"
SKIP_DIRS = {"__pycache__"}


def sha256_of(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def folder_hashes(folder: pathlib.Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(folder.rglob("*")):
        if path.is_file() and not any(part in SKIP_DIRS for part in path.relative_to(folder).parts):
            result[str(path.relative_to(folder))] = sha256_of(path)
    return result


def read_ledger() -> list[dict]:
    events = []
    for number, line in enumerate(LEDGER.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"LEDGER.jsonl line {number} is not JSON: {exc}") from exc
    return events


def main() -> int:
    problems: list[str] = []
    if not LEDGER.exists():
        print("review ledger: LEDGER.jsonl missing")
        return 1
    events = read_ledger()
    timestamps = [e.get("ts", "") for e in events]
    if timestamps != sorted(timestamps):
        problems.append("LEDGER.jsonl timestamps are not monotonic")
    registered = {e["review_id"] for e in events if "review_id" in e}
    folders = sorted(p for p in REVIEWS.iterdir() if p.is_dir() and p.name not in SKIP_DIRS)
    for folder in folders:
        review_id = folder.name
        if review_id not in registered:
            problems.append(f"{review_id}: folder not registered in LEDGER.jsonl")
            continue
        legacy = [e for e in events if e.get("review_id") == review_id and e.get("event") == "legacy-registered"]
        manifest_path = folder / "manifest.json"
        if legacy and not manifest_path.exists():
            recorded = legacy[-1].get("file_hashes", {})
            current = folder_hashes(folder)
            for rel, digest in recorded.items():
                if current.get(rel) != digest:
                    problems.append(f"{review_id}: legacy file changed or removed: {rel}")
            continue
        if not manifest_path.exists():
            problems.append(f"{review_id}: manifest.json missing for a schema-v1 folder")
            continue
        manifest = json.loads(manifest_path.read_text())
        current = folder_hashes(folder)
        for rel, entry in manifest.get("files", {}).items():
            if entry.get("class") == "immutable" and current.get(rel) != entry.get("sha256"):
                problems.append(f"{review_id}: immutable file changed or missing: {rel}")
        for rel, entry in manifest.get("files", {}).items():
            if entry.get("class") == "append-only":
                path = folder / rel
                if not path.exists():
                    problems.append(f"{review_id}: append-only file missing: {rel}")
                    continue
                lines = path.read_text().splitlines()
                sealed = entry.get("lines", 0)
                if len(lines) < sealed:
                    problems.append(f"{review_id}: append-only file shrank: {rel}")
                elif sealed and hashlib.sha256("\n".join(lines[:sealed]).encode()).hexdigest() != entry.get("prefix_sha256"):
                    problems.append(f"{review_id}: append-only file prefix changed: {rel}")
        findings_path = folder / "findings.json"
        if findings_path.exists():
            findings = json.loads(findings_path.read_text())
            ids = [f["id"] for f in findings.get("findings", [])]
            if len(ids) != len(set(ids)):
                problems.append(f"{review_id}: duplicate finding ids")
            dispositions_path = folder / "dispositions.jsonl"
            if dispositions_path.exists():
                for number, line in enumerate(dispositions_path.read_text().splitlines(), start=1):
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if record.get("finding_id") not in ids:
                        problems.append(f"{review_id}: dispositions.jsonl line {number} references unknown finding {record.get('finding_id')}")
    for problem in problems:
        print(f"review ledger: {problem}")
    if problems:
        return 1
    print(f"review ledger: ok ({len(folders)} reviews, {len(events)} ledger events)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
