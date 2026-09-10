"""Committed-history and staged-index guard. Owners: ADRL-FND-005, ADRL-EVL-009.

Actor labels are not authentication; valid history is not approval of its claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "reports/reviews/"
ROLES = {"coordinator", "implementer", "reviewer", "owner"}
DISPOSITIONS = {
    "unresolved",
    "accepted",
    "fixed-awaiting-recheck",
    "verified-fixed",
    "deferred-with-reason",
    "disputed-with-evidence",
}
EVENTS = {
    "opened",
    "inputs-frozen",
    "findings-recorded",
    "reconciliation",
    "disposition",
    "recheck",
    "status",
    "closed",
    "legacy-registered",
}
REQUIRED = {
    name: "immutable"
    for name in [
        "packet.md",
        "inputs.json",
        "invocation.json",
        "review.md",
        "findings.md",
        "findings.json",
        "dispositions.md",
    ]
}
REQUIRED.update({"dispositions.jsonl": "append-only", "status.json": "replaceable"})


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def records(data: bytes) -> list[dict]:
    require(not data or data.endswith(b"\n"), "JSONL must end at a newline boundary")
    # Split only at LF: U+2028 inside a JSON string is not a record separator.
    result = [json.loads(line) for line in data.split(b"\n") if line.strip()]
    require(
        all(isinstance(row, dict) for row in result), "JSONL records must be objects"
    )
    times = [datetime.fromisoformat(row["ts"]) for row in result]
    require(all(t.tzinfo is not None for t in times), "timestamps require timezone")
    require(times == sorted(times), "timestamps must be monotonic in file order")
    return result


def append_only(before: bytes, after: bytes, path: str) -> None:
    require(
        not before or before.endswith(b"\n"),
        f"{path}: baseline has no newline boundary",
    )
    require(
        after.startswith(before), f"{path}: committed prefix rewritten or truncated"
    )
    records(after)


def safe_name(name: str) -> bool:
    return (
        bool(name)
        and not name.startswith("/")
        and "\\" not in name
        and all(p not in {"", ".", ".."} for p in name.split("/"))
    )


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], stderr=subprocess.PIPE
    )


def git_files(root: Path, revision: str | None) -> dict[str, bytes]:
    """Read actual blobs from HEAD or the index, never the unstaged worktree."""
    entries = []
    if revision is None:
        lines = git(root, "ls-files", "--stage", "-z", "--", PREFIX).split(b"\0")
        for line in filter(None, lines):
            info, name = line.split(b"\t", 1)
            mode, oid, stage = info.split()
            require(stage == b"0", "unmerged review index")
            entries.append((mode, oid, name))
    else:
        exists = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", revision],
            capture_output=True,
            check=False,
        )
        if exists.returncode:
            require(
                revision == "HEAD" and not git(root, "rev-list", "--all").strip(),
                "baseline commit unavailable",
            )
            return {}
        for line in filter(
            None, git(root, "ls-tree", "-rz", revision, "--", PREFIX).split(b"\0")
        ):
            info, name = line.split(b"\t", 1)
            mode, kind, oid = info.split()
            require(kind == b"blob", "review entry is not a blob")
            entries.append((mode, oid, name))
    require(
        all(mode in {b"100644", b"100755"} for mode, _, _ in entries),
        "review symlinks/gitlinks are not admitted",
    )
    if not entries:
        return {}
    raw = subprocess.check_output(
        ["git", "-C", str(root), "cat-file", "--batch"],
        input=b"".join(oid + b"\n" for _, oid, _ in entries),
    )
    result = {}
    position = 0
    for _, _, name in entries:
        end = raw.index(b"\n", position)
        header = raw[position:end].split()
        size = int(header[2])
        position = end + 1
        result[name.decode()[len(PREFIX) :]] = raw[position : position + size]
        position += size + 1
    return result


def worktree(root: Path) -> dict[str, bytes]:
    base = root / PREFIX
    result = {}
    for path in base.rglob("*"):
        require(not path.is_symlink(), "review symlinks are not admitted")
        if path.is_file() and "__pycache__" not in path.relative_to(base).parts:
            result[path.relative_to(base).as_posix()] = path.read_bytes()
    return result


def validate(current: dict[str, bytes], before: dict[str, bytes]) -> dict:
    require("LEDGER.jsonl" in current, "ledger missing")
    require(set(before) <= set(current), "committed review file/folder deleted")
    append_only(
        before.get("LEDGER.jsonl", b""), current["LEDGER.jsonl"], "LEDGER.jsonl"
    )
    events = records(current["LEDGER.jsonl"])
    old_events = records(before.get("LEDGER.jsonl", b""))
    added_events = events[len(old_events) :]
    registered = {e["review_id"] for e in events}
    folders = {key.split("/", 1)[0] for key in current if "/" in key}
    require(registered == folders, "ledger registration/folder set mismatch")
    global_ids = set()
    legacy_ids = []
    for event in events:
        require(event.get("event") in EVENTS, "unknown ledger event")
        require(
            event.get("actor", "").split(":", 1)[0] in ROLES, "unknown event actor role"
        )
        require(
            re.fullmatch(r"[a-z0-9][a-z0-9-]*", event["review_id"]) is not None,
            "invalid review id",
        )
    for review in sorted(folders):
        prefix = review + "/"
        files = {
            k[len(prefix) :]: v for k, v in current.items() if k.startswith(prefix)
        }
        old = {k[len(prefix) :]: v for k, v in before.items() if k.startswith(prefix)}
        history = [e for e in events if e["review_id"] == review]
        legacy = [e for e in history if e["event"] == "legacy-registered"]
        if legacy:
            if before:
                require(
                    any(e in old_events for e in legacy),
                    "new legacy registration needs an explicit migration, not a schema bypass",
                )
            require(len(legacy) == 1, "legacy folder re-registered")
            hashes = legacy[0].get("file_hashes", {})
            require(set(files) == set(hashes), f"{review}: legacy file set changed")
            require(
                all(digest(files[k]) == h for k, h in hashes.items()),
                f"{review}: legacy content changed",
            )
            legacy_ids.append(review)
            continue
        require("manifest.json" in files, f"{review}: manifest missing")
        manifest = json.loads(files["manifest.json"])
        require(
            manifest.get("schema") == "review-ledger-v1"
            and manifest.get("review_id") == review,
            "manifest identity mismatch",
        )
        entries = manifest["files"]
        require(
            set(entries) == set(files) - {"manifest.json"},
            f"{review}: manifest coverage mismatch",
        )
        require(all(safe_name(k) for k in entries), "unsafe manifest path")
        for name, kind in REQUIRED.items():
            require(
                entries.get(name, {}).get("class") == kind,
                f"{review}: missing/wrong role {name}",
            )
        for name, entry in entries.items():
            kind = entry.get("class")
            require(
                kind in {"immutable", "add-only", "append-only", "replaceable"},
                "unknown mutability class",
            )
            require(
                not name.startswith("reconciliation/") or kind == "add-only",
                "reconciliation must be add-only",
            )
            if kind in {"immutable", "add-only"}:
                require(
                    digest(files[name]) == entry.get("sha256"),
                    f"{review}/{name}: sealed hash mismatch",
                )
            if kind == "append-only":
                rows = files[name].decode().splitlines()
                count = entry.get("lines", 0)
                require(
                    type(count) is int and 0 <= count <= len(rows),
                    "invalid sealed line count",
                )
                if count:
                    require(
                        digest("\n".join(rows[:count]).encode())
                        == entry.get("prefix_sha256"),
                        "sealed disposition prefix changed",
                    )
                append_only(old.get(name, b""), files[name], prefix + name)
        if old:
            prior = json.loads(old["manifest.json"])["files"]
            for name, entry in prior.items():
                require(
                    name in entries and entries[name]["class"] == entry["class"],
                    "historical class removed/changed",
                )
                if entry["class"] in {"immutable", "add-only"}:
                    require(
                        files[name] == old[name] and entries[name] == entry,
                        f"{prefix + name}: committed evidence rewritten/rehash",
                    )
                if entry["class"] == "append-only":
                    require(
                        entries[name].get("lines", 0) >= entry.get("lines", 0),
                        "manifest seal shrank",
                    )
            if files["manifest.json"] != old["manifest.json"]:
                require(
                    bool(set(entries) - set(prior)),
                    "manifest replaced without added files",
                )
                require(
                    any(
                        re.fullmatch(r"manifest-\d+\.json", k)
                        and v == old["manifest.json"]
                        and entries[k]["class"] == "immutable"
                        for k, v in files.items()
                    ),
                    "previous manifest bytes not archived",
                )
        if not old or files["status.json"] != old.get("status.json"):
            require(
                any(
                    e["review_id"] == review
                    and e["event"] == "status"
                    and e.get("ref") == "status.json"
                    and e.get("sha256") == digest(files["status.json"])
                    for e in added_events
                ),
                f"{review}: status change lacks matching new event",
            )
        if files["dispositions.jsonl"] != old.get("dispositions.jsonl", b""):
            require(
                any(
                    e["review_id"] == review
                    and e["event"] == "disposition"
                    and e.get("ref") == "dispositions.jsonl"
                    and e.get("sha256") == digest(files["dispositions.jsonl"])
                    for e in added_events
                ),
                f"{review}: disposition append lacks matching event",
            )
        if old and files["manifest.json"] != old["manifest.json"]:
            require(
                any(
                    e["review_id"] == review
                    and e["event"] == "reconciliation"
                    and e.get("ref") == "manifest.json"
                    and e.get("sha256") == digest(files["manifest.json"])
                    for e in added_events
                ),
                f"{review}: manifest extension lacks event",
            )
        statuses = [e for e in history if e["event"] == "status"]
        require(
            bool(statuses)
            and statuses[-1].get("ref") == "status.json"
            and statuses[-1].get("sha256") == digest(files["status.json"]),
            f"{review}: latest status event mismatch",
        )
        finding_doc = json.loads(files["findings.json"])
        require(
            finding_doc.get("review_id") == review, "findings review identity mismatch"
        )
        findings = finding_doc["findings"]
        ids = set()
        for finding in findings:
            fid = finding["id"]
            gid = review + ":" + fid
            require(
                fid not in ids
                and gid not in global_ids
                and finding.get("global_id") == gid,
                "duplicate/mismatched finding identity",
            )
            require(
                type(finding.get("blocking")) is bool,
                "finding blocking must be boolean",
            )
            require(
                all(
                    k in finding
                    for k in [
                        "severity",
                        "kind",
                        "confidence",
                        "owning_adrs",
                        "title",
                        "appendix_refs",
                    ]
                ),
                "finding schema incomplete",
            )
            ids.add(fid)
            global_ids.add(gid)
        prior_rows = len(records(old.get("dispositions.jsonl", b"")))
        for row_number, row in enumerate(records(files["dispositions.jsonl"])):
            require(row.get("finding_id") in ids, "unknown disposition finding")
            require(
                all(k in row for k in ["actor", "disposition", "evidence", "note"]),
                "disposition schema incomplete",
            )
            if row_number >= prior_rows:
                require(
                    row["disposition"] in DISPOSITIONS, "unknown new disposition state"
                )
                require(
                    row["actor"].split(":", 1)[0] in ROLES,
                    "unknown new disposition role",
                )
        for event in history:
            ref = event.get("ref", "")
            require(
                safe_name(ref) and ref in files,
                f"{review}: event reference missing/unsafe",
            )
            if ref == "manifest.json" or entries[ref]["class"] == "replaceable":
                continue  # Historical replacement hashes refer to retained earlier states.
            content = files[ref]
            if entries[ref]["class"] == "append-only":
                prefixes = [
                    digest(b"".join(content.splitlines(keepends=True)[:i]))
                    for i in range(len(content.splitlines()) + 1)
                ]
                require(
                    event.get("sha256") in prefixes,
                    "event append reference hash mismatch",
                )
            else:
                require(
                    event.get("sha256") == digest(content),
                    "event reference hash mismatch",
                )
    return {
        "reviews": len(folders),
        "events": len(events),
        "legacy_unknown": legacy_ids,
    }


def blockers(files: dict[str, bytes], scope: str | None = None) -> dict:
    output = []
    waived = []
    legacy = []
    events = records(files["LEDGER.jsonl"])
    reviews = {e["review_id"] for e in events}
    legacy_ids = {e["review_id"] for e in events if e["event"] == "legacy-registered"}
    for review in sorted(reviews):
        name = review + "/findings.json"
        if review in legacy_ids or name not in files:
            legacy.append(review)
            continue
        latest = {
            row["finding_id"]: row
            for row in records(files.get(review + "/dispositions.jsonl", b""))
        }
        for finding in json.loads(files[name])["findings"]:
            if not finding["blocking"]:
                continue
            state = latest.get(finding["id"], {})
            role = state.get("actor", "").split(":", 1)[0]
            evidence = state.get("evidence", "")
            key = evidence.removeprefix(PREFIX) if isinstance(evidence, str) else ""
            if key not in files:
                key = review + "/" + key
            supported = False
            if key in files and "/" in key:
                evidence_review, evidence_rel = key.split("/", 1)
                manifest_key = evidence_review + "/manifest.json"
                if manifest_key in files:
                    entry = json.loads(files[manifest_key])["files"].get(
                        evidence_rel, {}
                    )
                    event_kind = "recheck" if role == "reviewer" else "disposition"
                    supported = (
                        entry.get("class") in {"immutable", "add-only"}
                        and entry.get("sha256") == digest(files[key])
                        and any(
                            e["review_id"] == evidence_review
                            and e["event"] == event_kind
                            and e.get("ref") == evidence_rel
                            and e.get("sha256") == digest(files[key])
                            and e.get("actor", "").split(":", 1)[0] == role
                            and (
                                role != "reviewer"
                                or finding["global_id"] in e.get("finding_ids", [])
                            )
                            for e in events
                        )
                    )
            if (
                state.get("disposition") == "verified-fixed"
                and role == "reviewer"
                and supported
            ):
                continue
            item = {**finding, "latest_disposition": state or None}
            if (
                state.get("disposition") == "deferred-with-reason"
                and role == "owner"
                and supported
                and scope
                and state.get("scope") == scope
            ):
                waived.append(item)
            else:
                output.append(item)
    return {
        "blocking_findings": output,
        "waived_for_scope": waived,
        "legacy_unknown": legacy,
        "actor_authentication": False,
        "scope": scope,
    }


def install_hook(root: Path) -> dict:
    configured = subprocess.run(
        ["git", "-C", str(root), "config", "--get", "core.hooksPath"],
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    require(
        not configured,
        "hooksPath is configured; preserve it and integrate the guard explicitly",
    )
    hook = Path(
        git(root, "rev-parse", "--git-path", "hooks/pre-commit").decode().strip()
    )
    if not hook.is_absolute():
        hook = root / hook
    body = '#!/bin/sh\n# ADRL review-ledger guard v1\nset -eu\nroot=$(git rev-parse --show-toplevel)\nexec python3 "$root/tools/review_ledger_guard.py" check --staged\n'
    if hook.exists():
        require(
            hook.read_text() == body,
            "existing pre-commit hook preserved; explicit integration required",
        )
    else:
        hook.write_text(body)
    hook.chmod(0o755)
    return {
        "installed": str(hook),
        "scope": "local register commits; not server protection",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "blockers", "install-hook"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--scope")
    args = parser.parse_args()
    try:
        if args.command == "install-hook":
            result = install_hook(args.root)
        else:
            before = git_files(args.root, "HEAD")
            current = git_files(args.root, None) if args.staged else worktree(args.root)
            result = validate(current, before)
            if args.command == "blockers":
                result = blockers(current, args.scope)
        print(json.dumps(result, indent=2))
        return 0
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"review ledger guard: FAILED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
