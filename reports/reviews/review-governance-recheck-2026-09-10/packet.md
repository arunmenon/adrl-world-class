Independent Fable correction recheck, scope local review ledger governance, owners FND-005 and EVL-009. No tools/delegation. Prior review below; verify RG-01 exact global finding recheck binding, RG-02 installed skill copy identity (same bytes and hashes below), RG-03 newly appended disposition vocabulary; also RG-P07 narrower refusal/idempotence plus mirror identity. New CLAUDE.md imports AGENTS.md so Claude sees rules; no runtime behavioral change. 13 guard tests /32 total passed. No graduation or remote claims. Return JSON only with review_id review-governance-recheck-2026-09-10, verdict accepted or changes-requested, summary, verified_findings array of exact prior global IDs, findings array each id/global_id/severity/kind/blocking/confidence/owning_adrs/title/evidence/acceptance_criteria/appendix_refs. Max 450 words.
Reviewing the guard, tests, skill and register mappings against the seven pre-findings, then the behavioral exercise. Output follows.

```json
{
  "review_id": "review-governance-post-2026-09-10",
  "verdict": "reviewed-with-open-items",
  "summary": "All six blocking pre-findings are satisfied in review_ledger_guard.py and covered by named passing tests. RG-P07 is not returned as verified: the disclosed narrower alternative (index read via ls-files --stage plus cat-file, refusal of existing hooks/hooksPath instead of chaining, idempotence tested) is acceptable, but byte-identity of the installed skill copies is not evidenced in the packet. Behavioral exercise: an implementer-labelled verified-fixed record citing a later report stays blocking because blockers() requires role reviewer, a sealed immutable/add-only artifact and a matching reviewer recheck event; a prose report outside the ledger resolves to no manifest entry, so supported is false. An implementer-labelled deferred-with-reason stays blocking because waiver needs role owner, sealed evidence, an owner disposition event and an exact --scope match. test_blocker_actor_evidence_and_latest_line exercises both paths. Those records alone do not permit a completion claim; the skill also says a later prose report never silently supersedes a structured finding. Remaining blockers outside this wave: the six retrospective structured blockers including RV-01 remain unresolved and six legacy reviews remain unknown; nothing here clears them. Taxonomy mappings for FND-005 and EVL-009 are consistent across CHANGELOG, INDEX, bucket READMEs and ADR rows with no field change. This is scope acceptance of a local, bypassable control, not graduation or remote enforcement.",
  "verified_pre_findings": ["RG-P01", "RG-P02", "RG-P03", "RG-P04", "RG-P05", "RG-P06"],
  "findings": [
    {
      "id": "RG-01",
      "global_id": "review-governance-post-2026-09-10:RG-01",
      "severity": "low",
      "kind": "gap",
      "blocking": false,
      "confidence": 0.8,
      "owning_adrs": ["EVL-009"],
      "title": "Recheck evidence is not bound to the finding it clears",
      "evidence": "blockers() validates that the cited artifact is sealed and has a matching reviewer recheck event, but never checks that the artifact or event names finding_id. One recheck artifact can clear every blocking finding in the folder. README discloses that evidence justification is unchecked.",
      "acceptance_criteria": "Recheck events carry finding ids; verified-fixed clears only when the cited event lists that finding_id. Test with one artifact cited by two findings.",
      "appendix_refs": []
    },
    {
      "id": "RG-02",
      "global_id": "review-governance-post-2026-09-10:RG-02",
      "severity": "low",
      "kind": "coverage",
      "blocking": false,
      "confidence": 0.7,
      "owning_adrs": ["FND-005"],
      "title": "Installed skill copy identity not evidenced",
      "evidence": "The packet supplies only the register SKILL.md. The report claims installed Codex and Claude copies are reviewed extra scope, but no hashes for those copies were provided, so byte-identity is unverified.",
      "acceptance_criteria": "inputs.json lists both installed copies with sha256 equal to the register copy.",
      "appendix_refs": []
    },
    {
      "id": "RG-03",
      "global_id": "review-governance-post-2026-09-10:RG-03",
      "severity": "low",
      "kind": "defect",
      "blocking": false,
      "confidence": 0.9,
      "owning_adrs": ["EVL-009"],
      "title": "Disposition vocabulary declared but not enforced at write time",
      "evidence": "DISPOSITIONS is defined but unused; validate() checks ROLES only for ledger events. A misspelled disposition or actor in dispositions.jsonl commits successfully and remains permanently unresolved rather than being rejected before it enters append-only history.",
      "acceptance_criteria": "validate() rejects unknown disposition values or roles in newly appended rows only, preserving committed history. Test for a typo row.",
      "appendix_refs": []
    }
  ]
}
```
INPUT HASHES
{"/Users/arunmenon/projects/adrl-world-class/tools/review_ledger_guard.py": {"sha256": "1cbb70888f8fc9773b8c1f0e74959c4f1fc77baabf8df426b17d84113af39a31", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/0/review_ledger_guard.py"}, "/Users/arunmenon/projects/adrl-world-class/tests/test_review_ledger_guard.py": {"sha256": "0fe0768d692ed2edf935bc559dce0604ba50b285063d9a8c77d08bdc616d2aed", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/1/test_review_ledger_guard.py"}, "/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md": {"sha256": "6ba9787aa7ac6e33b00912bc46d03722623fafe29205b07aa027bd3c3d4a832b", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/2/SKILL.md"}, "/Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md": {"sha256": "c07ecebfafab64aa2a98f66380065c8e16b3766f5d972c1532df12477de0bbed", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/3/README.md"}, "/Users/arunmenon/projects/adrl-world-class/AGENTS.md": {"sha256": "73b243a6033b6b7360470887175a6199c7d8018e81b96562702394c3a98018f7", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/4/AGENTS.md"}, "/Users/arunmenon/projects/adrl-world-class/CLAUDE.md": {"sha256": "cd95b79c551375a248f5b855cb9aecab3437867eda1536c6ae10a6f134226f6f", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/5/CLAUDE.md"}, "/Users/arunmenon/projects/adrl-core/AGENTS.md": {"sha256": "5e182174b281e0be16dc23354ad2ceece44e63f8e2b02599af8a4a9430ee1e65", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/6/AGENTS.md"}, "/Users/arunmenon/projects/adrl-core/CLAUDE.md": {"sha256": "13fcfc1e216a1ccd467f11030db96ee3a70c56e3f5cc971cccc7bb0d1827d0ee", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/7/CLAUDE.md"}, "/Users/arunmenon/projects/adrl-world-class/reports/review-governance-2026-09-10.md": {"sha256": "b9a572becda3a94c2b545bd0097ddac6ddb298e7576d8c0c027229cd4ca8255d", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/8/review-governance-2026-09-10.md"}, "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/all-tests.log": {"sha256": "972ba641a9b22a63e6bb1509c36341fbf0db7c326130cc10a26ea2edc17fe0fc", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/9/all-tests.log"}, "/Users/arunmenon/.codex/skills/adrl-review-ledger/SKILL.md": {"sha256": "6ba9787aa7ac6e33b00912bc46d03722623fafe29205b07aa027bd3c3d4a832b", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/10/SKILL.md"}, "/Users/arunmenon/.codex/skills/adrl-review-ledger/agents/openai.yaml": {"sha256": "a96bd85888bc76c5f291c351b7955ff70655e79a4a59541a27c8cc3255ecfd73", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/11/openai.yaml"}, "/Users/arunmenon/.codex/skills/adrl-critical-review/SKILL.md": {"sha256": "467520e86db60d93c7f6098d1ce328c23db21bf744dab2bad7b20b361931fb0d", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/12/SKILL.md"}, "/Users/arunmenon/.codex/skills/adrl-critical-review/references/handoff.md": {"sha256": "38bd1b5dbe4e6931cbb5ec45494c12cc3fcd6ff1735444d269e845ea72e96726", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/13/handoff.md"}, "/Users/arunmenon/.claude/skills/adrl-review-ledger/SKILL.md": {"sha256": "6ba9787aa7ac6e33b00912bc46d03722623fafe29205b07aa027bd3c3d4a832b", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/14/SKILL.md"}, "/Users/arunmenon/.claude/skills/adrl-review-ledger/agents/openai.yaml": {"sha256": "a96bd85888bc76c5f291c351b7955ff70655e79a4a59541a27c8cc3255ecfd73", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/15/openai.yaml"}, "/Users/arunmenon/.claude/skills/adrl-critical-review/SKILL.md": {"sha256": "467520e86db60d93c7f6098d1ce328c23db21bf744dab2bad7b20b361931fb0d", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/16/SKILL.md"}, "/Users/arunmenon/.claude/skills/adrl-critical-review/references/handoff.md": {"sha256": "38bd1b5dbe4e6931cbb5ec45494c12cc3fcd6ff1735444d269e845ea72e96726", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/17/handoff.md"}, "/Users/arunmenon/projects/adrl-world-class/.git/hooks/pre-commit": {"sha256": "a05ffe033461ba46d7787b02232b03cdc9a06c6667e82ca46429064c4f4bbb9c", "snapshot": "/Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/recheck/source/18/pre-commit"}}
FILE /Users/arunmenon/projects/adrl-world-class/tools/review_ledger_guard.py
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

FILE /Users/arunmenon/projects/adrl-world-class/tests/test_review_ledger_guard.py
"""Review history, staged-index and blocker-state regressions. ADRL-FND-005/EVL-009."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "guard", Path(__file__).resolve().parents[1] / "tools/review_ledger_guard.py"
)
g = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(g)
RID = "example-2026-09-10"
TS = "2026-09-10T04:00:00+00:00"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False) + "\n").encode()


def event(files, kind, ref, actor="coordinator:test"):
    row = {
        "ts": TS,
        "review_id": RID,
        "event": kind,
        "actor": actor,
        "ref": ref,
        "sha256": g.digest(files[RID + "/" + ref]),
        "note": "fixture",
        "finding_ids": [RID + ":RV-01"],
    }
    files["LEDGER.jsonl"] += encoded(row)


def fixture():
    files = {RID + "/" + name: b"test\n" for name in g.REQUIRED}
    finding = {
        "id": "RV-01",
        "global_id": RID + ":RV-01",
        "blocking": True,
        "severity": "high",
        "kind": "defect",
        "confidence": 0.9,
        "owning_adrs": ["FND-005"],
        "title": "fixture",
        "appendix_refs": [],
    }
    files[RID + "/findings.json"] = encoded({"review_id": RID, "findings": [finding]})
    files[RID + "/status.json"] = encoded({"state": "changes-requested"})
    files[RID + "/dispositions.jsonl"] = b""
    manifest = {"schema": "review-ledger-v1", "review_id": RID, "files": {}}
    for name, kind in g.REQUIRED.items():
        manifest["files"][name] = {
            "class": kind,
            "sha256": g.digest(files[RID + "/" + name]),
        }
        if kind == "append-only":
            manifest["files"][name] = {"class": kind, "lines": 0}
    files[RID + "/manifest.json"] = encoded(manifest)
    files["LEDGER.jsonl"] = b""
    event(files, "opened", "packet.md")
    event(files, "status", "status.json")
    return files


def extend(files, name, data):
    key = RID + "/manifest.json"
    old = files[key]
    manifest = json.loads(old)
    archive = next(
        "manifest-" + str(i) + ".json"
        for i in range(1, 100)
        if RID + "/manifest-" + str(i) + ".json" not in files
    )
    files[RID + "/" + archive] = old
    files[RID + "/" + name] = data
    manifest["files"][archive] = {"class": "immutable", "sha256": g.digest(old)}
    manifest["files"][name] = {"class": "add-only", "sha256": g.digest(data)}
    files[key] = encoded(manifest)
    event(files, "reconciliation", "manifest.json")


class GuardTests(unittest.TestCase):
    def test_valid_initial_and_unchanged(self):
        f = fixture()
        g.validate(f, {})
        g.validate(f, dict(f))

    def test_folder_deletion_and_ledger_reorder_rejected(self):
        before = fixture()
        for current in [
            {"LEDGER.jsonl": before["LEDGER.jsonl"]},
            {
                **before,
                "LEDGER.jsonl": b"".join(
                    reversed(before["LEDGER.jsonl"].splitlines(keepends=True))
                ),
            },
        ]:
            with self.assertRaises(ValueError):
                g.validate(current, before)

    def test_coordinated_rehash_cannot_rewrite_committed_finding(self):
        before = fixture()
        after = dict(before)
        after[RID + "/findings.json"] = after[RID + "/findings.json"].replace(
            b"fixture", b"revised"
        )
        m = json.loads(after[RID + "/manifest.json"])
        m["files"]["findings.json"]["sha256"] = g.digest(after[RID + "/findings.json"])
        after[RID + "/manifest.json"] = encoded(m)
        with self.assertRaises(ValueError):
            g.validate(after, before)

    def test_add_only_history_and_manifest_class_cannot_change(self):
        before = fixture()
        extend(before, "reconciliation/check.md", b"evidence\n")
        g.validate(before, {})
        for op in ["content", "class"]:
            after = dict(before)
            if op == "content":
                after[RID + "/reconciliation/check.md"] = b"changed\n"
            else:
                m = json.loads(after[RID + "/manifest.json"])
                m["files"]["packet.md"]["class"] = "replaceable"
                after[RID + "/manifest.json"] = encoded(m)
            with self.assertRaises(ValueError):
                g.validate(after, before)

    def test_legitimate_manifest_extension_and_status_event(self):
        before = fixture()
        after = dict(before)
        extend(after, "reconciliation/check.md", b"evidence\n")
        after[RID + "/status.json"] = encoded({"state": "awaiting-recheck"})
        event(after, "status", "status.json")
        g.validate(after, before)
        del after[RID + "/manifest-1.json"]
        with self.assertRaises(ValueError):
            g.validate(after, before)

    def test_unlisted_file_and_silent_status_change_rejected(self):
        before = fixture()
        for path, data in [
            ("extra.md", b"unlisted"),
            ("status.json", encoded({"state": "reviewed"})),
        ]:
            with self.assertRaises(ValueError):
                g.validate({**before, RID + "/" + path: data}, before)

    def test_legacy_cannot_add_manifest_or_files(self):
        before = {RID + "/old.md": b"old\n"}
        before["LEDGER.jsonl"] = encoded(
            {
                "ts": TS,
                "review_id": RID,
                "event": "legacy-registered",
                "actor": "coordinator:test",
                "ref": RID + "/",
                "file_hashes": {"old.md": g.digest(b"old\n")},
            }
        )
        g.validate(before, {})
        for name in ["manifest.json", "new.md"]:
            with self.assertRaises(ValueError):
                g.validate({**before, RID + "/" + name: b"{}"}, before)

    def test_append_bytes_and_unusual_newlines(self):
        first = encoded({"ts": TS, "note": "text\u2028inside"})
        g.append_only(first, first + encoded({"ts": TS, "note": "next"}), "x")
        for base, after in [
            (first, first.replace(b"\n", b"\r\n")),
            (first, first[:-1]),
            (first[:-1], first + b"{}\n"),
        ]:
            with self.assertRaises(ValueError):
                g.append_only(base, after, "x")

    def test_unknown_ids_and_global_id_mismatch(self):
        before = fixture()
        after = dict(before)
        after[RID + "/dispositions.jsonl"] = encoded(
            {
                "ts": TS,
                "actor": "implementer:test",
                "finding_id": "missing",
                "disposition": "accepted",
                "evidence": "",
                "note": "x",
            }
        )
        event(after, "disposition", "dispositions.jsonl")
        with self.assertRaises(ValueError):
            g.validate(after, before)
        after = fixture()
        d = json.loads(after[RID + "/findings.json"])
        d["findings"][0]["global_id"] = "wrong:RV-01"
        after[RID + "/findings.json"] = encoded(d)
        m = json.loads(after[RID + "/manifest.json"])
        m["files"]["findings.json"]["sha256"] = g.digest(after[RID + "/findings.json"])
        after[RID + "/manifest.json"] = encoded(m)
        with self.assertRaises(ValueError):
            g.validate(after, {})

    def test_blocker_actor_evidence_and_latest_line(self):
        f = fixture()
        extend(f, "reconciliation/recheck.md", b"reviewer evidence\n")
        event(f, "recheck", "reconciliation/recheck.md", "reviewer:fable")
        row = {
            "ts": TS,
            "actor": "implementer:codex",
            "finding_id": "RV-01",
            "disposition": "verified-fixed",
            "evidence": "reconciliation/recheck.md",
            "note": "fixture",
        }
        f[RID + "/dispositions.jsonl"] = encoded(row)
        self.assertEqual(len(g.blockers(f)["blocking_findings"]), 1)
        row["actor"] = "reviewer:fable"
        f[RID + "/dispositions.jsonl"] += encoded(row)
        self.assertEqual(g.blockers(f)["blocking_findings"], [])
        row["disposition"] = "unrecognized"
        f[RID + "/dispositions.jsonl"] += encoded(row)
        self.assertEqual(len(g.blockers(f)["blocking_findings"]), 1)
        row.update(actor="owner:Arun", disposition="deferred-with-reason", scope="P2")
        event(f, "disposition", "reconciliation/recheck.md", "owner:Arun")
        f[RID + "/dispositions.jsonl"] += encoded(row)
        self.assertEqual(len(g.blockers(f)["blocking_findings"]), 1)
        self.assertEqual(len(g.blockers(f, "P2")["waived_for_scope"]), 1)
        self.assertEqual(len(g.blockers(f, "P3")["blocking_findings"]), 1)

    def test_recheck_does_not_clear_another_finding(self):
        f = fixture()
        extend(f, "reconciliation/recheck.md", b"reviewer evidence\n")
        event(f, "recheck", "reconciliation/recheck.md", "reviewer:fable")
        findings = json.loads(f[RID + "/findings.json"])
        second = dict(findings["findings"][0], id="RV-02", global_id=RID + ":RV-02")
        findings["findings"].append(second)
        f[RID + "/findings.json"] = encoded(findings)
        f[RID + "/dispositions.jsonl"] = b"".join(
            encoded(
                {
                    "ts": TS,
                    "actor": "reviewer:fable",
                    "finding_id": fid,
                    "disposition": "verified-fixed",
                    "evidence": "reconciliation/recheck.md",
                    "note": "test",
                }
            )
            for fid in ["RV-01", "RV-02"]
        )
        self.assertEqual(
            [x["id"] for x in g.blockers(f)["blocking_findings"]], ["RV-02"]
        )

    def test_new_disposition_typos_rejected(self):
        for actor, state in [
            ("reviewr:fable", "accepted"),
            ("reviewer:fable", "verifed-fixed"),
        ]:
            before = fixture()
            after = dict(before)
            after[RID + "/dispositions.jsonl"] = encoded(
                {
                    "ts": TS,
                    "actor": actor,
                    "finding_id": "RV-01",
                    "disposition": state,
                    "evidence": "",
                    "note": "typo",
                }
            )
            event(after, "disposition", "dispositions.jsonl")
            with self.assertRaisesRegex(ValueError, "unknown new disposition"):
                g.validate(after, before)

    def test_staged_tamper_not_hidden_by_clean_worktree_and_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", "-C", directory, *args], capture_output=True, check=True
                )

            git("init", "-q")
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            for name, data in fixture().items():
                p = root / g.PREFIX / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
            tool = root / "tools/review_ledger_guard.py"
            tool.parent.mkdir()
            tool.write_bytes(Path(g.__file__).read_bytes())
            git("add", ".")
            git("commit", "-qm", "baseline")
            g.install_hook(root)
            g.install_hook(root)
            target = root / g.PREFIX / RID / "packet.md"
            original = target.read_bytes()
            target.write_bytes(b"changed")
            git("add", str(target))
            target.write_bytes(original)
            g.validate(g.worktree(root), g.git_files(root, "HEAD"))
            with self.assertRaises(ValueError):
                g.validate(g.git_files(root, None), g.git_files(root, "HEAD"))
            result = subprocess.run(
                ["git", "-C", directory, "commit", "-m", "tamper"],
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            hook = root / ".git/hooks/pre-commit"
            hook.write_text("#!/bin/sh\nexit 0\n")
            with self.assertRaises(ValueError):
                g.install_hook(root)
            self.assertEqual(hook.read_text(), "#!/bin/sh\nexit 0\n")


if __name__ == "__main__":
    unittest.main()

FILE /Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md
---
name: adrl-review-ledger
description: Create and reconcile ADRL review records, query outstanding findings, and check review-history integrity before completion or commits. Use whenever an ADRL agent publishes reviews, dispositions, rechecks or review-status claims.
---

# ADRL review ledger governance

Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`.
Read the canonical [schema](/Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md).
Use `adrl-critical-review` for independent criticism and `adrl-taxonomy-sync` for architecture
closure. This skill governs their records; it does not grant execution, spend or graduation.

## Before work or a completion claim

From the register run:

```sh
python3 tools/review_ledger_guard.py check
python3 tools/review_ledger_guard.py blockers
```

Read the actual findings and their append-only dispositions for the applicable wave/ADRs.
Do not assume a constant number of blockers. Legacy reviews are explicitly unknown to the
machine-readable query, not approved or fully accounted for. A later prose report does not
silently supersede an unresolved structured finding; append a linked reconciliation first.
A failure blocks the affected integrity/completion claim. Preserve the evidence and fix the
current record; never repair history by rehashing an edited original.

## Publish a checkpoint

Serialize ledger mutations through one coordinator; never run parallel writers. Prepare
externally, use collision-free new names, and stop on a publication conflict.

- Use a new `<slug>-<YYYY-MM-DD>` folder per independent checkpoint. Prepare externally while
  incomplete, then publish the fixed schema files together. Pre-wave and post-wave reviews
  are separate checkpoints; a recheck may be a new add-only reconciliation artifact.
- Freeze `packet.md` and `inputs.json` before review. Include source paths, hashes, revisions,
  dirty/untracked scope and exclusions. A hash cannot reconstruct source: retain an exact
  external snapshot or retrievable commit/blob, and record its location. Keep secrets out.
  Do not add source copies to this ledger; preserve already registered legacy copies unchanged.
- Retain the actual reviewer output and invocation/model metadata. `findings.json` and
  `findings.md` must describe the same reviewer findings with stable IDs. Global IDs are
  `<review_id>:<local_id>`. The initial immutable `dispositions.md` records unresolved findings.
  Do not invent reviewer findings, approval or identity. Record coordinator normalization.
- Publish `dispositions.jsonl`, `status.json` and `manifest.json`. Classify every file;
  `manifest.json` excludes itself. Original evidence is immutable, reconciliation files are
  add-only, dispositions are append-only, and status is replaceable with an accompanying event.
- Append timestamped actor/ref/hash events to `LEDGER.jsonl`. Publish new files and registration
  together; run the guard before claiming integrity. Never backdate a new event into history.

## Reconcile without rewriting

Append one disposition per change with `ts`, `actor`, local `finding_id`, `disposition`,
`evidence`, and `note`. Use actual roles (`implementer:`, `reviewer:`, `owner:`, `coordinator:`).
Actors are provenance labels, not authenticated signatures. Link the retained original action;
never attribute an implementer's conclusion to the reviewer or owner.

`accepted`, `fixed-awaiting-recheck` and `disputed-with-evidence` do not close a blocking finding.
`verified-fixed` needs reviewer recheck evidence. `deferred-with-reason` needs an owner ruling
with an explicit `scope`; it is not a fix. The blockers command conservatively keeps deferrals
visible unless called with that exact `--scope`, and reports scoped waivers separately.
Unsupported evidence or self-verification remains blocking. Existing authorization may supply
the owner ruling; do not manufacture new approval requirements or ask twice.

Add fixes/rechecks under new `reconciliation/` filenames; never replace an earlier response.
Before extending a manifest, retain its exact previous bytes as `manifest-<n>.json`, classify
the archive immutable, and preserve existing classifications and sealed evidence. Append a
reconciliation event linking the new manifest. Status changes also need a new status event.
Legacy folders remain frozen: reconcile them in a new checkpoint linked to the original.

## Before committing

Run both the existing checker and the new staged guard:

```sh
python3 tools/check_review_ledger.py
python3 tools/review_ledger_guard.py check --staged
```

The staged guard compares the proposed Git index with committed HEAD. A clean working copy
cannot excuse a tampered staged file. Use the local hook installed by
`python3 tools/review_ledger_guard.py install-hook` in new clones; never overwrite an existing
hook or hooksPath configuration to force installation. Report setup conflicts.

Also complete the applicable taxonomy-sync receipt and independent review. This integrity
check permits honest unresolved reviews to be committed; it does not approve a wave or clear
its blockers. Do not use `--no-verify`, remove the hook, or weaken validation to get a commit
through without an explicit user override recorded with its scope.

## Honest enforcement claims

The installed local Git hook blocks ordinary commits on this checkout. It is bypassable and
is not remote branch protection. Committed-baseline checks cannot prove that a brand-new
record was never edited before its first commit. Manifests prove consistency, not truthful
claims, authenticated actors, code fixes, test quality or graduation. New clones need hook
installation; remote required checks are a separate deployment. Report exactly which checks
ran, review state, unresolved scope and the next gate.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.

FILE /Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md
# Review ledger

`reports/reviews/` is the append-only ledger of independent reviews of ADRL. Schema `review-ledger-v1`. Its purpose is that a person or an agent can later parse every review across waves without reading prose: which checkpoint was reviewed, what inputs were frozen, what was found, what the implementer answered, what was rechecked, and what remains open.

## Layout

One folder per review, named `<slug>-<YYYY-MM-DD>`. A conforming folder contains:

| File | Written by | Mutability | Purpose |
|---|---|---|---|
| `packet.md` | coordinator | immutable after open | checkpoint, objective, scope, exclusions, baseline, hypotheses, acceptance conditions |
| `inputs.json` | coordinator | immutable | frozen-input manifest: every reviewed file with SHA-256, dirty and untracked scope, exclusions |
| `invocation.json` | coordinator | immutable | requested and observed model, session, tools, permission denials, coverage limits |
| `review.md` | reviewer | immutable | the original review text |
| `findings.md` | reviewer | immutable | findings with stable IDs, severity, confidence, evidence, acceptance criteria |
| `findings.json` | reviewer | immutable | the same findings, machine-readable: `{id, global_id, severity, kind, blocking, confidence, owning_adrs, title, appendix_refs}` |
| `dispositions.md` | reviewer | immutable | the initial disposition table, every row `unresolved` |
| `dispositions.jsonl` | implementer, reviewer, owner | append-only | one line per disposition change: `{ts, actor, finding_id, disposition, evidence, note}` |
| `status.json` | coordinator | replaceable; every change also appended to `LEDGER.jsonl` | `not-started`, `in-review`, `changes-requested`, `awaiting-recheck`, `reviewed-with-open-items`, `reviewed`, `unavailable` |
| `appendix/` | reviewer | immutable | inspection reports and machine-readable tables |
| `reconciliation/` | implementer | add-only (new files may be added, existing ones never edited) | implementer responses, rechecks, fix references |
| `manifest.json` | coordinator | replaced only when files are added; prior manifests kept as `manifest-<n>.json` | every file's SHA-256 and its mutability class |

Global finding IDs are `<folder>:<local id>`, for example `fable-retrospective-2026-09-08:RV-01`. Severity and original finding text never change; a reviewer revises by appending, an implementer disputes by appending, an owner rules by appending.

## Ledger index

`LEDGER.jsonl` holds one JSON object per line, append-only, in time order: `{ts, review_id, event, actor, ref, sha256, note}`. Events: `opened`, `inputs-frozen`, `findings-recorded`, `reconciliation`, `disposition`, `recheck`, `status`, `closed`, `legacy-registered`. Folders created before this schema (`legacy-v0`) are registered with their file hashes at registration time and are frozen from then on; their internal layout is not normalised.

## Verification

`tools/check_review_ledger.py` fails when an immutable file's hash differs from its manifest, when `dispositions.jsonl` or `LEDGER.jsonl` has lost or reordered lines, when a finding ID is duplicated or a disposition references an unknown ID, when a review folder is absent from the ledger, or when a legacy folder's registered hashes changed. Run it with the other register checks before any commit that touches `reports/reviews/`.

## Rules

- A review is never edited to make it agree with a later fix; the fix and the recheck are new lines and new files.
- Reviewer unavailability is recorded as `unavailable`, never as passed.
- `reviewed` never means formal maturity graduation; maturity moves only through the register's own rules.
- Snapshots of reviewed sources are not stored here; `inputs.json` carries hashes plus retrieval references to commits/blobs or externally retained snapshots. Hashes verify matching bytes but cannot reconstruct missing source or prove the code changed.

## Agent workflow and local enforcement

Use the shared [adrl-review-ledger skill](../../skills/adrl-review-ledger/SKILL.md).
`python3 tools/review_ledger_guard.py check` adds committed-HEAD comparison to the existing
consistency checker. `check --staged` checks the actual index that would be committed.
Run `install-hook` once per clone; existing hooks or hooksPath configurations are preserved
and require explicit integration rather than being overwritten. The hook is local and
bypassable, not server branch protection or actor authentication.

History comparison preserves exact committed bytes. JSONL additions start after an LF newline
boundary, with timezone-aware monotonic timestamps. CRLF conversion, removal/reordering and
Unicode line-separator reinterpretation do not excuse changing committed bytes. Legacy sealed
prefix metadata keeps its original normalization for compatibility; committed-byte comparison
is the additional history guarantee. First-commit provenance still depends on the retained
reviewer record and independently frozen inputs.

Published checkpoints contain all fixed files above. Prepare externally while incomplete;
publish a new checkpoint together with its ledger registration. Every file is classified by
its manifest (except the manifest itself). A manifest extension archives its exact previous
bytes and appends a reconciliation event. Status and disposition changes require matching new
ledger events. Reviewer rechecks use immutable/add-only artifacts and `recheck` events.

Disposition vocabulary: `unresolved`, `accepted`, `fixed-awaiting-recheck`, `verified-fixed`,
`deferred-with-reason`, `disputed-with-evidence`. Roles are `coordinator`, `implementer`,
`reviewer`, `owner`, followed by `:<identity>`. Last appended record per finding wins.
Unknown values remain unresolved in the query. `blockers` clears `verified-fixed` only for a
reviewer-labelled record with a sealed evidence reference and matching reviewer `recheck`
event. Owner deferrals need sealed evidence plus an owner `disposition` event and exact `scope`;
`blockers --scope <scope>` reports such waivers separately. This validates recorded provenance,
not whether the actor is genuine or the evidence justifies its conclusion. Historical legacy
reviews remain unknown to automated finding queries. Unresolved findings can be committed;
integrity acceptance does not approve completion or promotion.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.

FILE /Users/arunmenon/projects/adrl-world-class/AGENTS.md
# Keeping the ADRL register and implementation aligned

This repository is the architecture decision register for ADRL. Runtime implementation is in
the sibling `adrl-core` repository. Follow these rules when changing either as part of this work.

- Before completing an implementation change, identify its owning ADRs and record the result in
  those records. A behavior change updates the decision or its explicitly scoped application;
  a refactor or bug fix can retain the decision and add implementation evidence.
- Preserve stable ADR IDs, prior decision wording in the changelog, and dated research findings.
  Distinguish product direction, implemented behavior, tested behavior and planned work.
- Update `INDEX.md`, the affected bucket overviews and `CHANGELOG.md` with the same scope. Link
  the code, test/evidence record, limitations and outstanding follow-ups. Do not mark work done
  merely because a schema, interface or component exists.
- Keep architectural status separate from maturity. Offline tests can support D2 for the tested
  behavior; they do not establish D3, D4, D5, another harness, or the whole decision's promise.
- `source/` preserves historical input. Add a clearly dated current-context note when necessary;
  do not rewrite historical observations as if they described the current implementation.
- Preserve unrelated uncommitted changes. Verify local links, decision-index coverage and the
  implementation evidence cited by a register update. Documentation-only synchronization does
  not require rerunning the runtime suite if the tested source hashes still match.

## Independent review checkpoints

For substantive ADRL implementation waves, use the `adrl-critical-review` skill
(Codex: `/Users/arunmenon/.codex/skills/adrl-critical-review/SKILL.md`; Claude Code:
`/Users/arunmenon/.claude/skills/adrl-critical-review/SKILL.md`). Require an independent
pre-wave challenge and post-wave evidence review before claiming the affected wave complete.
Retain original reviewer findings, Codex dispositions, material-fix rechecks and unresolved
disagreements. Reviewer absence is pending review, never approval. Model agreement does not
promote maturity or replace existing graduation authority. Scope reviews to the change; use
full roadmap/all-ADR coverage for retrospective and milestone reviews. This process does not
restart automation or authorize additional execution exposure.

## Taxonomy synchronization completion gate

Before implementation/configuration/adapter/tooling changes, use `adrl-taxonomy-sync` at
`/Users/arunmenon/projects/adrl-world-class/skills/adrl-taxonomy-sync/SKILL.md`
(installed in both Codex and Claude). Capture the declared dirty-worktree baseline before edits.
At closure, map every changed input to owning ADRs, synchronize dated evidence in the ADRs,
INDEX, affected bucket rows and CHANGELOG, and retain independent semantic review. Run
`python3 /Users/arunmenon/projects/adrl-world-class/tools/check_taxonomy_sync.py check`
with its required baseline, packet and new outside-repository receipt arguments.
A failed or absent receipt means taxonomy synchronization is incomplete: do not claim the
implementation wave complete. Recheck after any source/evidence/review change. Preserve
historical grades and unrelated changes; this local gate does not replace runtime tests,
human graduation, or remote CI/branch protection. Scope exclusions and unresolved historic
register defects must be explicit. Routine documentation updates need no extra permission.

Review outputs live in `reports/reviews/` as an append-only ledger (schema `review-ledger-v1`, see
`reports/reviews/README.md`). Run `python3 tools/check_review_ledger.py` before any commit that
touches that directory. Reviewer findings and severities are never edited; responses, rechecks and
owner rulings are appended.

## Review-ledger governance

Use `adrl-review-ledger` at
`/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md` before
publishing review records, reconciling findings or making a completion claim. The skill is
installed for both Codex and Claude. Query applicable blockers; legacy coverage is unknown,
and an implementer's deferral is not reviewer verification or an owner ruling.

Preserve original findings and registered legacy folders. Append actor-labelled dispositions,
new recheck artifacts and matching ledger events. Before a register commit run
`python3 tools/review_ledger_guard.py check --staged` from the register. A local register hook
runs this check; new clones need `python3 tools/review_ledger_guard.py install-hook`.
For runtime work, review the sibling register's current blockers and complete taxonomy sync;
the register hook does not validate runtime commits or grant completion authority. Never
bypass or weaken the guard merely to make a commit succeed. Remote enforcement is not configured.

FILE /Users/arunmenon/projects/adrl-world-class/CLAUDE.md
# ADRL register instructions

@AGENTS.md

FILE /Users/arunmenon/projects/adrl-core/AGENTS.md
# adrl-core engineering rules

These rules apply to every change in this repository. The architecture source of truth is the ADR
register in `../adrl-world-class/adr/<BUCKET>/ADRL-<BUCKET>-NNN.md` (reviewed 2026-09-02). The stack
proposal that this repository implements is `../adrl-world-class/design/implementation-stack.md`.

## Ownership

- Every module docstring names its primary ADRL ID on the first line, for example
  `"""Secret detection on new content. Primary: ADRL-SAF-003."""`. Secondary IDs are listed only for
  real cross-cutting contracts.
- Packages map to buckets: `wire` (SEM), `gates` (SAF), `routing` (RTG), `cascade` (CAS), `ledger`
  (MEM), `learning` (LRN). `core`, `config`, `proxy`, `telemetry` and `cli` are shared plumbing.
- A task implements an indexed decision. It does not need a new decision merely because it adds a
  file. If no decision fits, stop and propose one in the register; do not invent behaviour.

## Invariants the code must keep

- Never rewrite a request body on the frontier or passthrough path. The bytes the harness sent are
  the bytes the gateway receives, and response bytes (SSE `ping` events, upstream error wording)
  are relayed unmodified. Body rewrites exist only for non-Claude rungs (ADRL-FND-001).
  One carve-out (ADRL-CAS-004): after an escalation whose source turn carried no thinking
  blocks, the `thinking` parameter is stripped from frontier-bound requests until the next user
  turn, and the plan records `thinking_suppressed`.
  Scoped FND-001 application (2026-09-09): the constructor-only Claude initial-choice
  experiment may change only model after enforcing deployment gates in explicitly LIVE mode.
  Normal startup does not enable it; SHADOW/OFF and LIVE admission are not bypassed.
  This offline candidate is not an authorized live profile or a mid-session switch.
- No `UPDATE` or `DELETE` SQL anywhere under `src/`. The evidence ledger and the egress ledger are
  append-only. Corrections are new events; erasure is key deletion plus an `erased` event
  (ADRL-MEM-001, ADRL-MEM-010). `tools/check_ledger_discipline.py` enforces this in CI.
- Every "versioned policy constant" named in an ADR is a field on a versioned config model, and the
  config version is recorded on the decision row it influenced. Changing a threshold is a config
  version bump, never a literal in code.
- Shadow code never imports into live routing. Nothing under `adrl.learning` and no module whose
  name starts with `shadow_` may be imported by `adrl.routing` or `adrl.proxy` (ADRL-MEM-008).
- A privacy pin can only be released by the audited human path (ADRL-SAF-002). No code path in
  routing, cascade, fallback or episode handling may clear pin state.
- Gate outcomes only tighten the permitted rung set within a lineage. `PermittedSet.tighten`
  raises on any attempt to widen (ADRL-SAF-001).
- Terminal failures are rendered as Anthropic Messages API error objects, never as synthetic
  assistant content (ADRL-CAS-007).

## Code quality

- No mock implementations. Write the real thing, or leave a `TODO(ADRL-XXX-NNN):` comment naming
  the owning decision and raise `NotImplementedError` with the same text.
- Type hints on every public function; `mypy --strict` must pass.
- No em dashes in any file, including docs, docstrings and log messages.
- Descriptive names. No adjectives in file names.
- `structlog` for logging, never `print` in `src/`.
- Pydantic v2 at config and record boundaries; frozen dataclasses for internal value objects.

## Running checks

```bash
.venv/bin/python -m ruff check src tests tools
.venv/bin/python -m ruff format --check src tests tools
.venv/bin/python -m mypy
.venv/bin/python -m pytest -q
.venv/bin/python tools/check_ledger_discipline.py
.venv/bin/python -m adrl.cli.main config check
```

All six must pass before a change is considered done. Use `uv sync --all-extras` to refresh the
virtual environment; the lockfile is checked in and only binary wheels are used.

## Taxonomy synchronization completion gate

Before implementation/configuration/adapter/tooling changes, use `adrl-taxonomy-sync` at
`/Users/arunmenon/projects/adrl-world-class/skills/adrl-taxonomy-sync/SKILL.md`
(installed in both Codex and Claude). Capture the declared dirty-worktree baseline before edits.
At closure, map every changed input to owning ADRs, synchronize dated evidence in the ADRs,
INDEX, affected bucket rows and CHANGELOG, and retain independent semantic review. Run
`python3 /Users/arunmenon/projects/adrl-world-class/tools/check_taxonomy_sync.py check`
with its required baseline, packet and new outside-repository receipt arguments.
A failed or absent receipt means taxonomy synchronization is incomplete: do not claim the
implementation wave complete. Recheck after any source/evidence/review change. Preserve
historical grades and unrelated changes; this local gate does not replace runtime tests,
human graduation, or remote CI/branch protection. Scope exclusions and unresolved historic
register defects must be explicit. Routine documentation updates need no extra permission.

## Review-ledger governance

Use `adrl-review-ledger` at
`/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md` before
publishing review records, reconciling findings or making a completion claim. The skill is
installed for both Codex and Claude. Query applicable blockers; legacy coverage is unknown,
and an implementer's deferral is not reviewer verification or an owner ruling.

Preserve original findings and registered legacy folders. Append actor-labelled dispositions,
new recheck artifacts and matching ledger events. Before a register commit run
`python3 tools/review_ledger_guard.py check --staged` from the register. A local register hook
runs this check; new clones need `python3 tools/review_ledger_guard.py install-hook`.
For runtime work, review the sibling register's current blockers and complete taxonomy sync;
the register hook does not validate runtime commits or grant completion authority. Never
bypass or weaken the guard merely to make a commit succeed. Remote enforcement is not configured.

FILE /Users/arunmenon/projects/adrl-core/CLAUDE.md
# adrl-core engineering rules

These rules apply to every change in this repository. The architecture source of truth is the ADR
register in `../adrl-world-class/adr/<BUCKET>/ADRL-<BUCKET>-NNN.md` (reviewed 2026-09-02). The stack
proposal that this repository implements is `../adrl-world-class/design/implementation-stack.md`.

## Ownership

- Every module docstring names its primary ADRL ID on the first line, for example
  `"""Secret detection on new content. Primary: ADRL-SAF-003."""`. Secondary IDs are listed only for
  real cross-cutting contracts.
- Packages map to buckets: `wire` (SEM), `gates` (SAF), `routing` (RTG), `cascade` (CAS), `ledger`
  (MEM), `learning` (LRN). `core`, `config`, `proxy`, `telemetry` and `cli` are shared plumbing.
- A task implements an indexed decision. It does not need a new decision merely because it adds a
  file. If no decision fits, stop and propose one in the register; do not invent behaviour.

## Invariants the code must keep

- Never rewrite a request body on the frontier or passthrough path. The bytes the harness sent are
  the bytes the gateway receives, and response bytes (SSE `ping` events, upstream error wording)
  are relayed unmodified. Body rewrites exist only for non-Claude rungs (ADRL-FND-001).
  One carve-out (ADRL-CAS-004): after an escalation whose source turn carried no thinking
  blocks, the `thinking` parameter is stripped from frontier-bound requests until the next user
  turn, and the plan records `thinking_suppressed`.
- No `UPDATE` or `DELETE` SQL anywhere under `src/`. The evidence ledger and the egress ledger are
  append-only. Corrections are new events; erasure is key deletion plus an `erased` event
  (ADRL-MEM-001, ADRL-MEM-010). `tools/check_ledger_discipline.py` enforces this in CI.
- Every "versioned policy constant" named in an ADR is a field on a versioned config model, and the
  config version is recorded on the decision row it influenced. Changing a threshold is a config
  version bump, never a literal in code.
- Shadow code never imports into live routing. Nothing under `adrl.learning` and no module whose
  name starts with `shadow_` may be imported by `adrl.routing` or `adrl.proxy` (ADRL-MEM-008).
- A privacy pin can only be released by the audited human path (ADRL-SAF-002). No code path in
  routing, cascade, fallback or episode handling may clear pin state.
- Gate outcomes only tighten the permitted rung set within a lineage. `PermittedSet.tighten`
  raises on any attempt to widen (ADRL-SAF-001).
- Terminal failures are rendered as Anthropic Messages API error objects, never as synthetic
  assistant content (ADRL-CAS-007).

## Code quality

- No mock implementations. Write the real thing, or leave a `TODO(ADRL-XXX-NNN):` comment naming
  the owning decision and raise `NotImplementedError` with the same text.
- Type hints on every public function; `mypy --strict` must pass.
- No em dashes in any file, including docs, docstrings and log messages.
- Descriptive names. No adjectives in file names.
- `structlog` for logging, never `print` in `src/`.
- Pydantic v2 at config and record boundaries; frozen dataclasses for internal value objects.

## Running checks

```bash
.venv/bin/python -m ruff check src tests tools
.venv/bin/python -m ruff format --check src tests tools
.venv/bin/python -m mypy
.venv/bin/python -m pytest -q
.venv/bin/python tools/check_ledger_discipline.py
.venv/bin/python -m adrl.cli.main config check
```

All six must pass before a change is considered done. Use `uv sync --all-extras` to refresh the
virtual environment; the lockfile is checked in and only binary wheels are used.

## Shared current governance

@AGENTS.md

FILE /Users/arunmenon/projects/adrl-world-class/reports/review-governance-2026-09-10.md
# Review-ledger governance, 10 September 2026

The shared adrl-review-ledger skill tells Codex and Claude how to publish immutable findings, append dispositions/rechecks, query applicable blockers and verify staged commits. Both repository instruction files require it. The existing critical-review skill now points to this schema and preserves initial dispositions rather than rewriting them.

The new review_ledger_guard.py complements check_review_ledger.py. It compares candidate bytes with committed HEAD, including actual staged blobs in commit mode. Committed ledger/disposition prefixes, original evidence, classes and legacy file sets cannot be rewritten by updating a current manifest. Manifest extensions archive the exact old manifest; status/disposition changes require ledger events. Global IDs and reference consistency are checked.

A local pre-commit hook is installed in adrl-world-class and tested using an isolated Git repository. Existing hooks/hooksPath are refused rather than overwritten or silently chained; manual integration is required in that case. No hook was installed in adrl-core: its instructions require sibling ledger/taxonomy review, while the register hook protects register history only. New clones need installation. Remote protected branches/required checks are not configured; local controls can be bypassed and are not tamper-proof.

The blocker query uses last-line disposition state, requires a reviewer-labelled verified-fixed record with sealed evidence and a matching recheck event naming that exact global finding ID, and reports exact-scope owner waivers separately. Unknown values and implementer deferrals remain unresolved. Actor names are not authenticated and evidence presence is not proof of a fix. Six registered legacy reviews remain unknown to structured finding queries. The six existing retrospective blockers remain recorded, including RV-01; reconciling historical prose repairs into that structured history is separate work.

Thirteen guard tests (32 register tests total) cover deletion, rehashing, immutable/add-only edits, valid manifest extension, status event omission, legacy bypass, byte-prefix changes including CRLF/U+2028, global/unknown IDs, actor/evidence/scope precedence, staged-versus-worktree tampering and hook preservation/idempotence. No runtime suite rerun is claimed: this changes development governance and core AGENTS.md only, not runtime code or model behavior.

Owners: FND-005 and EVL-009. Formal status/maturity/verdict fields unchanged. Independent Fable pre/post review and taxonomy closure are required before completion; final evidence will be linked from the completion record. Reviewed source copies are outside reports/reviews, with hashes and retrieval paths in the checkpoint inputs. Historical review folders remain unchanged.

The review README, register CLAUDE.md import, installed skill copies and local hook are explicitly reviewed extra scope beyond the taxonomy checker's fixed source list. Source consistency is distinct from installed-hook integrity and remote enforcement. Commit/push, blanket blocker clearance, live execution, paid API use, automation restart and maturity promotion are not part of this work.

FILE /Users/arunmenon/projects/.adrl-execution-state/review-governance-20260910/all-tests.log
................................
----------------------------------------------------------------------
Ran 32 tests in 1.033s

OK

FILE /Users/arunmenon/.codex/skills/adrl-review-ledger/SKILL.md
---
name: adrl-review-ledger
description: Create and reconcile ADRL review records, query outstanding findings, and check review-history integrity before completion or commits. Use whenever an ADRL agent publishes reviews, dispositions, rechecks or review-status claims.
---

# ADRL review ledger governance

Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`.
Read the canonical [schema](/Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md).
Use `adrl-critical-review` for independent criticism and `adrl-taxonomy-sync` for architecture
closure. This skill governs their records; it does not grant execution, spend or graduation.

## Before work or a completion claim

From the register run:

```sh
python3 tools/review_ledger_guard.py check
python3 tools/review_ledger_guard.py blockers
```

Read the actual findings and their append-only dispositions for the applicable wave/ADRs.
Do not assume a constant number of blockers. Legacy reviews are explicitly unknown to the
machine-readable query, not approved or fully accounted for. A later prose report does not
silently supersede an unresolved structured finding; append a linked reconciliation first.
A failure blocks the affected integrity/completion claim. Preserve the evidence and fix the
current record; never repair history by rehashing an edited original.

## Publish a checkpoint

Serialize ledger mutations through one coordinator; never run parallel writers. Prepare
externally, use collision-free new names, and stop on a publication conflict.

- Use a new `<slug>-<YYYY-MM-DD>` folder per independent checkpoint. Prepare externally while
  incomplete, then publish the fixed schema files together. Pre-wave and post-wave reviews
  are separate checkpoints; a recheck may be a new add-only reconciliation artifact.
- Freeze `packet.md` and `inputs.json` before review. Include source paths, hashes, revisions,
  dirty/untracked scope and exclusions. A hash cannot reconstruct source: retain an exact
  external snapshot or retrievable commit/blob, and record its location. Keep secrets out.
  Do not add source copies to this ledger; preserve already registered legacy copies unchanged.
- Retain the actual reviewer output and invocation/model metadata. `findings.json` and
  `findings.md` must describe the same reviewer findings with stable IDs. Global IDs are
  `<review_id>:<local_id>`. The initial immutable `dispositions.md` records unresolved findings.
  Do not invent reviewer findings, approval or identity. Record coordinator normalization.
- Publish `dispositions.jsonl`, `status.json` and `manifest.json`. Classify every file;
  `manifest.json` excludes itself. Original evidence is immutable, reconciliation files are
  add-only, dispositions are append-only, and status is replaceable with an accompanying event.
- Append timestamped actor/ref/hash events to `LEDGER.jsonl`. Publish new files and registration
  together; run the guard before claiming integrity. Never backdate a new event into history.

## Reconcile without rewriting

Append one disposition per change with `ts`, `actor`, local `finding_id`, `disposition`,
`evidence`, and `note`. Use actual roles (`implementer:`, `reviewer:`, `owner:`, `coordinator:`).
Actors are provenance labels, not authenticated signatures. Link the retained original action;
never attribute an implementer's conclusion to the reviewer or owner.

`accepted`, `fixed-awaiting-recheck` and `disputed-with-evidence` do not close a blocking finding.
`verified-fixed` needs reviewer recheck evidence. `deferred-with-reason` needs an owner ruling
with an explicit `scope`; it is not a fix. The blockers command conservatively keeps deferrals
visible unless called with that exact `--scope`, and reports scoped waivers separately.
Unsupported evidence or self-verification remains blocking. Existing authorization may supply
the owner ruling; do not manufacture new approval requirements or ask twice.

Add fixes/rechecks under new `reconciliation/` filenames; never replace an earlier response.
Before extending a manifest, retain its exact previous bytes as `manifest-<n>.json`, classify
the archive immutable, and preserve existing classifications and sealed evidence. Append a
reconciliation event linking the new manifest. Status changes also need a new status event.
Legacy folders remain frozen: reconcile them in a new checkpoint linked to the original.

## Before committing

Run both the existing checker and the new staged guard:

```sh
python3 tools/check_review_ledger.py
python3 tools/review_ledger_guard.py check --staged
```

The staged guard compares the proposed Git index with committed HEAD. A clean working copy
cannot excuse a tampered staged file. Use the local hook installed by
`python3 tools/review_ledger_guard.py install-hook` in new clones; never overwrite an existing
hook or hooksPath configuration to force installation. Report setup conflicts.

Also complete the applicable taxonomy-sync receipt and independent review. This integrity
check permits honest unresolved reviews to be committed; it does not approve a wave or clear
its blockers. Do not use `--no-verify`, remove the hook, or weaken validation to get a commit
through without an explicit user override recorded with its scope.

## Honest enforcement claims

The installed local Git hook blocks ordinary commits on this checkout. It is bypassable and
is not remote branch protection. Committed-baseline checks cannot prove that a brand-new
record was never edited before its first commit. Manifests prove consistency, not truthful
claims, authenticated actors, code fixes, test quality or graduation. New clones need hook
installation; remote required checks are a separate deployment. Report exactly which checks
ran, review state, unresolved scope and the next gate.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.

FILE /Users/arunmenon/.codex/skills/adrl-review-ledger/agents/openai.yaml
interface:
  display_name: "Adrl Review Ledger"
  short_description: "Help with Adrl Review Ledger tasks"

FILE /Users/arunmenon/.codex/skills/adrl-critical-review/SKILL.md
---
name: adrl-critical-review
description: Coordinate independent Codex and Claude review of ADRL wave plans, implementation evidence, roadmap alignment and taxonomy maturity. Apply before substantive ADRL waves and before claiming completion, as well as explicit retrospective reviews.
---

# ADRL critical review

The product owner wants Codex and Claude to challenge each other throughout implementation. Codex normally owns implementation and evidence; Claude Fable 5.1 independently reviews. This is a development review process, not ADRL runtime RSI, formal human graduation, or proof of customer value.

## Ledger contract

Before publishing review artifacts or claiming findings resolved, use `adrl-review-ledger`
(`/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md`). Its fixed
schema and append-only history rules govern storage. Initial findings/dispositions are immutable;
subsequent responses and rechecks are new records. Keep exact source snapshots outside the
review ledger and include retrieval references/hashes. Never overwrite a registered legacy folder.

## Establish the checkpoint

Read both repositories' instructions, current execution state, product roadmap, journey and owning ADRs. Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`. Reconcile newer overlays and stale claims. Never hardcode test counts, stages or maturity in this skill.

Use three scopes:
- **Pre-wave:** challenge proposed behavior, roadmap value, owning decisions, assumptions, minimum scope, alternatives, acceptance evidence, permissions and stop conditions before substantive implementation.
- **Post-wave:** independently inspect frozen source and raw evidence before a completion claim. Include failed candidates and source hashes. Review regressions and scope of maturity claims.
- **Retrospective/milestone:** review the whole product roadmap and all ADRs. For the 7–8 September review use the existing full prompt in `reports/adrl-independent-review-prompt-2026-09-08.md` and its companion inventory. Future reviews generate fresh inventories and time windows.

Do not request another full audit for trivial wording edits. Scope routine wave review to changed behavior and dependencies, expanding if evidence reveals broader risk.

## Independent handoff

Read [references/handoff.md](references/handoff.md) for packet and invocation details. Give Claude the user intent, raw artifacts, baseline, frozen scope and required outputs. Provide author claims as hypotheses, not the expected verdict. Keep the first review independent of the implementer's proposed rebuttal. The reviewer does not edit the implementation or grade its own repairs.

Invoke the actual Claude tool/CLI, not a Codex subagent relabeled Claude. Pin the user-requested model and retain returned model/session metadata. No silent fallback if unavailable. Use existing authorized subscription access; do not switch to separately billed APIs. Keep secrets and unrelated files out of context. The user has authorized this ADRL reviewer collaboration, not unrestricted experiment execution or spending.

Use read-only tools and fresh review outputs. Exclude shell/write tools from unattended reviewer invocation unless a bounded isolated validation specifically requires and permits them. Capture response externally through the coordinator. Inspect local hooks/settings/tool exposure before source-bearing invocations; never bypass permissions. Read-only tool policy is not a filesystem sandbox. Limit the accessible snapshot and record incomplete coverage.

## Reconcile without rubber-stamping

Codex is the named coordinator and records packet provenance. Give the reviewer the complete relevant declared source snapshot, including dirty and untracked files, plus an exclusions manifest; the reviewer can challenge scope and request omitted relevant evidence. Freeze a copied snapshot with a complete hash manifest and compare hashes before/after review; a commit is optional and cannot substitute for uncommitted contents.

Persist the original review before responding. Reviewer severity and original text are immutable history. Codex cannot remove a block by downgrading severity. A reviewer may revise its assessment with evidence; unresolved contested blocking findings require an explicit product-owner disposition. For each finding record stable ID, severity, confidence, source/evidence, owning ADR, product consequence and disposition: accepted, fixed-awaiting-recheck, verified-fixed, deferred-with-reason, disputed-with-evidence, or unresolved. Preserve both positions. A reviewer recommendation is not automatically a correct finding.

Codex reproduces accepted issues and fixes them only within the authorized wave. Claude rechecks material fixes against the new snapshot and relevant regressions. Normally allow one initial review and at most two correction/review rounds per wave, constrained by any tighter existing run/repair limit. Stop churn; report unresolved disagreements to the product owner with evidence and a concrete decision. Do not endlessly optimize to the reviewer's wording.

Unresolved critical/high findings affecting privacy, correctness, evidence integrity or the wave's acceptance criterion block the affected completion/exposure claim. Nonblocking findings may be explicitly deferred with owner and gate. Reviewer unavailability means `unavailable`, not passed or waived; continue independent preparation within existing authority. Do not silently advance the gated wave. A user can explicitly override the process with the limitation recorded.

## Close the loop into the register

After reconciliation, update the owning ADRs, INDEX, overviews and CHANGELOG when behavior/evidence warrants it, following repository rules. Record review disposition and links in the journey/current state and review log. Distinguish acceptance, implemented behavior, tested scope and formal maturity. No automatic D-grade promotion, release or policy admission from model agreement.

Each wave packet and completion report should expose: pre-review state, frozen input identity, reviewer identity, findings/dispositions, post-review state, evidence limits, and next product gate. Use statuses `not-started`, `in-review`, `changes-requested`, `awaiting-recheck`, `reviewed-with-open-items`, `reviewed`, or `unavailable`; `reviewed` never means formal graduation. Updates after the reviewed snapshot invalidate the affected acceptance evidence and require proportionate recheck.

Report plainly: what Codex built, what Claude challenged, what changed because of review, what remains disputed, and what this proves for adaptive routing. Do not claim the skill is an enforced CI control, an autonomous scheduler, or an already completed review.

FILE /Users/arunmenon/.codex/skills/adrl-critical-review/references/handoff.md
# Handoff contract and Claude invocation

For every checkpoint create a fresh folder under the register's `reports/reviews/` named `<slug>-<YYYY-MM-DD>`, following the ledger schema in the register's `reports/reviews/README.md` (`review-ledger-v1`: add `findings.json`, `dispositions.jsonl`, `manifest.json`, and append events to `LEDGER.jsonl`; run `tools/check_review_ledger.py`). An external folder is acceptable only while the review is in progress; fold it in at close. The folder holds:

- `packet.md`: checkpoint, objective, scope/exclusions, roadmap stage, owning ADRs, baseline, hypotheses, alternatives, acceptance conditions, restrictions and expected report. Post-review packets include code/tests/raw negative and positive evidence, not only the author's summary.
- `inputs.json`: timestamp, exact source paths and SHA-256, dirty/untracked scope, known omissions. Preserve current uncommitted source; a clean Git worktree can omit it.
- `review.md` and invocation metadata: original independent output, requested and observed model, tool configuration, session, termination/completeness, permission denials and coverage. If served identity is unavailable record that explicitly.
- `dispositions.md`: immutable initial unresolved table. Later author responses and reviewer/owner rulings append to `dispositions.jsonl`; detailed rechecks are new `reconciliation/` artifacts. Follow adrl-review-ledger; never edit initial findings or dispositions to reflect a fix.
- `status.json`: checkpoint state, input hash, findings outstanding and next step. Missing/failed/partial output cannot produce `reviewed`.

For full retrospectives additionally require all-ADR and roadmap coverage matrices. Do not force every ordinary wave to reread every unchanged ADR.

Claude Code was present locally when this skill was created. Check `claude --version` and `claude --help` again before dispatching. Official model ID is `claude-fable-5-1`; verify availability rather than substituting the rolling `fable` alias. Sources: https://platform.claude.com/docs/en/models/fable-5-1/overview and https://code.claude.com/docs/en/skills .

Use a fresh session with `--print`, `--model claude-fable-5-1`, JSON output, and a restricted built-in tool list such as `Read,Glob,Grep`. Disable customizations/MCP where supported, for example `--safe-mode --strict-mcp-config --permission-mode dontAsk`; inspect current help because flags can change. Safe mode disables skills, so embed the complete reviewer instructions and packet explicitly, rather than assuming `/adrl-critical-review` loads. Supply paths via explicit args, not shell interpolation of file content. Prefer subprocess argument arrays and stdin. Save JSON/stdout/stderr outside reviewed source. Cap each call's elapsed time and scope; a terminated call is partial, not a completed review. API dollar caps are not reliable subscription quota controls.

For interactive Claude Code the mirrored personal skill is available at `~/.claude/skills/adrl-critical-review/SKILL.md`; invoke `/adrl-critical-review`. Codex's canonical copy is `~/.codex/skills/adrl-critical-review/`. Keep both copies identical when revising shared instructions. Automatic discovery is advisory; repository instructions provide the durable checkpoint requirement.

Reviewer instruction template:

> Independently review the attached ADRL checkpoint. You are the reviewer, not the implementer. Challenge scope, architecture, product value and evidence using the actual files. Treat claims as hypotheses. Return prioritized evidence-backed findings, counterevidence, uncovered scope and a scoped disposition. Do not edit sources, run model/engine experiments, widen permissions or promote ADR maturity. Report missing access rather than guessing. Do not delegate back to Codex or recursively invoke another reviewer. Your review is one input to reconciliation, not release authority.

Record secret-exclusion categories in the manifest without exposing secret contents. Model self-description is not identity evidence; retained CLI metadata establishes reported provenance, not independent attestation of serving infrastructure.

Run `python3 tools/review_ledger_guard.py check` before publishing, and `check --staged` before committing. Read committed-baseline and actor/legacy limitations in the ledger skill. External source snapshots must be retrievable; hashes alone cannot reconstruct dirty reviewed code.

FILE /Users/arunmenon/.claude/skills/adrl-review-ledger/SKILL.md
---
name: adrl-review-ledger
description: Create and reconcile ADRL review records, query outstanding findings, and check review-history integrity before completion or commits. Use whenever an ADRL agent publishes reviews, dispositions, rechecks or review-status claims.
---

# ADRL review ledger governance

Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`.
Read the canonical [schema](/Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md).
Use `adrl-critical-review` for independent criticism and `adrl-taxonomy-sync` for architecture
closure. This skill governs their records; it does not grant execution, spend or graduation.

## Before work or a completion claim

From the register run:

```sh
python3 tools/review_ledger_guard.py check
python3 tools/review_ledger_guard.py blockers
```

Read the actual findings and their append-only dispositions for the applicable wave/ADRs.
Do not assume a constant number of blockers. Legacy reviews are explicitly unknown to the
machine-readable query, not approved or fully accounted for. A later prose report does not
silently supersede an unresolved structured finding; append a linked reconciliation first.
A failure blocks the affected integrity/completion claim. Preserve the evidence and fix the
current record; never repair history by rehashing an edited original.

## Publish a checkpoint

Serialize ledger mutations through one coordinator; never run parallel writers. Prepare
externally, use collision-free new names, and stop on a publication conflict.

- Use a new `<slug>-<YYYY-MM-DD>` folder per independent checkpoint. Prepare externally while
  incomplete, then publish the fixed schema files together. Pre-wave and post-wave reviews
  are separate checkpoints; a recheck may be a new add-only reconciliation artifact.
- Freeze `packet.md` and `inputs.json` before review. Include source paths, hashes, revisions,
  dirty/untracked scope and exclusions. A hash cannot reconstruct source: retain an exact
  external snapshot or retrievable commit/blob, and record its location. Keep secrets out.
  Do not add source copies to this ledger; preserve already registered legacy copies unchanged.
- Retain the actual reviewer output and invocation/model metadata. `findings.json` and
  `findings.md` must describe the same reviewer findings with stable IDs. Global IDs are
  `<review_id>:<local_id>`. The initial immutable `dispositions.md` records unresolved findings.
  Do not invent reviewer findings, approval or identity. Record coordinator normalization.
- Publish `dispositions.jsonl`, `status.json` and `manifest.json`. Classify every file;
  `manifest.json` excludes itself. Original evidence is immutable, reconciliation files are
  add-only, dispositions are append-only, and status is replaceable with an accompanying event.
- Append timestamped actor/ref/hash events to `LEDGER.jsonl`. Publish new files and registration
  together; run the guard before claiming integrity. Never backdate a new event into history.

## Reconcile without rewriting

Append one disposition per change with `ts`, `actor`, local `finding_id`, `disposition`,
`evidence`, and `note`. Use actual roles (`implementer:`, `reviewer:`, `owner:`, `coordinator:`).
Actors are provenance labels, not authenticated signatures. Link the retained original action;
never attribute an implementer's conclusion to the reviewer or owner.

`accepted`, `fixed-awaiting-recheck` and `disputed-with-evidence` do not close a blocking finding.
`verified-fixed` needs reviewer recheck evidence. `deferred-with-reason` needs an owner ruling
with an explicit `scope`; it is not a fix. The blockers command conservatively keeps deferrals
visible unless called with that exact `--scope`, and reports scoped waivers separately.
Unsupported evidence or self-verification remains blocking. Existing authorization may supply
the owner ruling; do not manufacture new approval requirements or ask twice.

Add fixes/rechecks under new `reconciliation/` filenames; never replace an earlier response.
Before extending a manifest, retain its exact previous bytes as `manifest-<n>.json`, classify
the archive immutable, and preserve existing classifications and sealed evidence. Append a
reconciliation event linking the new manifest. Status changes also need a new status event.
Legacy folders remain frozen: reconcile them in a new checkpoint linked to the original.

## Before committing

Run both the existing checker and the new staged guard:

```sh
python3 tools/check_review_ledger.py
python3 tools/review_ledger_guard.py check --staged
```

The staged guard compares the proposed Git index with committed HEAD. A clean working copy
cannot excuse a tampered staged file. Use the local hook installed by
`python3 tools/review_ledger_guard.py install-hook` in new clones; never overwrite an existing
hook or hooksPath configuration to force installation. Report setup conflicts.

Also complete the applicable taxonomy-sync receipt and independent review. This integrity
check permits honest unresolved reviews to be committed; it does not approve a wave or clear
its blockers. Do not use `--no-verify`, remove the hook, or weaken validation to get a commit
through without an explicit user override recorded with its scope.

## Honest enforcement claims

The installed local Git hook blocks ordinary commits on this checkout. It is bypassable and
is not remote branch protection. Committed-baseline checks cannot prove that a brand-new
record was never edited before its first commit. Manifests prove consistency, not truthful
claims, authenticated actors, code fixes, test quality or graduation. New clones need hook
installation; remote required checks are a separate deployment. Report exactly which checks
ran, review state, unresolved scope and the next gate.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.

FILE /Users/arunmenon/.claude/skills/adrl-review-ledger/agents/openai.yaml
interface:
  display_name: "Adrl Review Ledger"
  short_description: "Help with Adrl Review Ledger tasks"

FILE /Users/arunmenon/.claude/skills/adrl-critical-review/SKILL.md
---
name: adrl-critical-review
description: Coordinate independent Codex and Claude review of ADRL wave plans, implementation evidence, roadmap alignment and taxonomy maturity. Apply before substantive ADRL waves and before claiming completion, as well as explicit retrospective reviews.
---

# ADRL critical review

The product owner wants Codex and Claude to challenge each other throughout implementation. Codex normally owns implementation and evidence; Claude Fable 5.1 independently reviews. This is a development review process, not ADRL runtime RSI, formal human graduation, or proof of customer value.

## Ledger contract

Before publishing review artifacts or claiming findings resolved, use `adrl-review-ledger`
(`/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md`). Its fixed
schema and append-only history rules govern storage. Initial findings/dispositions are immutable;
subsequent responses and rechecks are new records. Keep exact source snapshots outside the
review ledger and include retrieval references/hashes. Never overwrite a registered legacy folder.

## Establish the checkpoint

Read both repositories' instructions, current execution state, product roadmap, journey and owning ADRs. Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`. Reconcile newer overlays and stale claims. Never hardcode test counts, stages or maturity in this skill.

Use three scopes:
- **Pre-wave:** challenge proposed behavior, roadmap value, owning decisions, assumptions, minimum scope, alternatives, acceptance evidence, permissions and stop conditions before substantive implementation.
- **Post-wave:** independently inspect frozen source and raw evidence before a completion claim. Include failed candidates and source hashes. Review regressions and scope of maturity claims.
- **Retrospective/milestone:** review the whole product roadmap and all ADRs. For the 7–8 September review use the existing full prompt in `reports/adrl-independent-review-prompt-2026-09-08.md` and its companion inventory. Future reviews generate fresh inventories and time windows.

Do not request another full audit for trivial wording edits. Scope routine wave review to changed behavior and dependencies, expanding if evidence reveals broader risk.

## Independent handoff

Read [references/handoff.md](references/handoff.md) for packet and invocation details. Give Claude the user intent, raw artifacts, baseline, frozen scope and required outputs. Provide author claims as hypotheses, not the expected verdict. Keep the first review independent of the implementer's proposed rebuttal. The reviewer does not edit the implementation or grade its own repairs.

Invoke the actual Claude tool/CLI, not a Codex subagent relabeled Claude. Pin the user-requested model and retain returned model/session metadata. No silent fallback if unavailable. Use existing authorized subscription access; do not switch to separately billed APIs. Keep secrets and unrelated files out of context. The user has authorized this ADRL reviewer collaboration, not unrestricted experiment execution or spending.

Use read-only tools and fresh review outputs. Exclude shell/write tools from unattended reviewer invocation unless a bounded isolated validation specifically requires and permits them. Capture response externally through the coordinator. Inspect local hooks/settings/tool exposure before source-bearing invocations; never bypass permissions. Read-only tool policy is not a filesystem sandbox. Limit the accessible snapshot and record incomplete coverage.

## Reconcile without rubber-stamping

Codex is the named coordinator and records packet provenance. Give the reviewer the complete relevant declared source snapshot, including dirty and untracked files, plus an exclusions manifest; the reviewer can challenge scope and request omitted relevant evidence. Freeze a copied snapshot with a complete hash manifest and compare hashes before/after review; a commit is optional and cannot substitute for uncommitted contents.

Persist the original review before responding. Reviewer severity and original text are immutable history. Codex cannot remove a block by downgrading severity. A reviewer may revise its assessment with evidence; unresolved contested blocking findings require an explicit product-owner disposition. For each finding record stable ID, severity, confidence, source/evidence, owning ADR, product consequence and disposition: accepted, fixed-awaiting-recheck, verified-fixed, deferred-with-reason, disputed-with-evidence, or unresolved. Preserve both positions. A reviewer recommendation is not automatically a correct finding.

Codex reproduces accepted issues and fixes them only within the authorized wave. Claude rechecks material fixes against the new snapshot and relevant regressions. Normally allow one initial review and at most two correction/review rounds per wave, constrained by any tighter existing run/repair limit. Stop churn; report unresolved disagreements to the product owner with evidence and a concrete decision. Do not endlessly optimize to the reviewer's wording.

Unresolved critical/high findings affecting privacy, correctness, evidence integrity or the wave's acceptance criterion block the affected completion/exposure claim. Nonblocking findings may be explicitly deferred with owner and gate. Reviewer unavailability means `unavailable`, not passed or waived; continue independent preparation within existing authority. Do not silently advance the gated wave. A user can explicitly override the process with the limitation recorded.

## Close the loop into the register

After reconciliation, update the owning ADRs, INDEX, overviews and CHANGELOG when behavior/evidence warrants it, following repository rules. Record review disposition and links in the journey/current state and review log. Distinguish acceptance, implemented behavior, tested scope and formal maturity. No automatic D-grade promotion, release or policy admission from model agreement.

Each wave packet and completion report should expose: pre-review state, frozen input identity, reviewer identity, findings/dispositions, post-review state, evidence limits, and next product gate. Use statuses `not-started`, `in-review`, `changes-requested`, `awaiting-recheck`, `reviewed-with-open-items`, `reviewed`, or `unavailable`; `reviewed` never means formal graduation. Updates after the reviewed snapshot invalidate the affected acceptance evidence and require proportionate recheck.

Report plainly: what Codex built, what Claude challenged, what changed because of review, what remains disputed, and what this proves for adaptive routing. Do not claim the skill is an enforced CI control, an autonomous scheduler, or an already completed review.

FILE /Users/arunmenon/.claude/skills/adrl-critical-review/references/handoff.md
# Handoff contract and Claude invocation

For every checkpoint create a fresh folder under the register's `reports/reviews/` named `<slug>-<YYYY-MM-DD>`, following the ledger schema in the register's `reports/reviews/README.md` (`review-ledger-v1`: add `findings.json`, `dispositions.jsonl`, `manifest.json`, and append events to `LEDGER.jsonl`; run `tools/check_review_ledger.py`). An external folder is acceptable only while the review is in progress; fold it in at close. The folder holds:

- `packet.md`: checkpoint, objective, scope/exclusions, roadmap stage, owning ADRs, baseline, hypotheses, alternatives, acceptance conditions, restrictions and expected report. Post-review packets include code/tests/raw negative and positive evidence, not only the author's summary.
- `inputs.json`: timestamp, exact source paths and SHA-256, dirty/untracked scope, known omissions. Preserve current uncommitted source; a clean Git worktree can omit it.
- `review.md` and invocation metadata: original independent output, requested and observed model, tool configuration, session, termination/completeness, permission denials and coverage. If served identity is unavailable record that explicitly.
- `dispositions.md`: immutable initial unresolved table. Later author responses and reviewer/owner rulings append to `dispositions.jsonl`; detailed rechecks are new `reconciliation/` artifacts. Follow adrl-review-ledger; never edit initial findings or dispositions to reflect a fix.
- `status.json`: checkpoint state, input hash, findings outstanding and next step. Missing/failed/partial output cannot produce `reviewed`.

For full retrospectives additionally require all-ADR and roadmap coverage matrices. Do not force every ordinary wave to reread every unchanged ADR.

Claude Code was present locally when this skill was created. Check `claude --version` and `claude --help` again before dispatching. Official model ID is `claude-fable-5-1`; verify availability rather than substituting the rolling `fable` alias. Sources: https://platform.claude.com/docs/en/models/fable-5-1/overview and https://code.claude.com/docs/en/skills .

Use a fresh session with `--print`, `--model claude-fable-5-1`, JSON output, and a restricted built-in tool list such as `Read,Glob,Grep`. Disable customizations/MCP where supported, for example `--safe-mode --strict-mcp-config --permission-mode dontAsk`; inspect current help because flags can change. Safe mode disables skills, so embed the complete reviewer instructions and packet explicitly, rather than assuming `/adrl-critical-review` loads. Supply paths via explicit args, not shell interpolation of file content. Prefer subprocess argument arrays and stdin. Save JSON/stdout/stderr outside reviewed source. Cap each call's elapsed time and scope; a terminated call is partial, not a completed review. API dollar caps are not reliable subscription quota controls.

For interactive Claude Code the mirrored personal skill is available at `~/.claude/skills/adrl-critical-review/SKILL.md`; invoke `/adrl-critical-review`. Codex's canonical copy is `~/.codex/skills/adrl-critical-review/`. Keep both copies identical when revising shared instructions. Automatic discovery is advisory; repository instructions provide the durable checkpoint requirement.

Reviewer instruction template:

> Independently review the attached ADRL checkpoint. You are the reviewer, not the implementer. Challenge scope, architecture, product value and evidence using the actual files. Treat claims as hypotheses. Return prioritized evidence-backed findings, counterevidence, uncovered scope and a scoped disposition. Do not edit sources, run model/engine experiments, widen permissions or promote ADR maturity. Report missing access rather than guessing. Do not delegate back to Codex or recursively invoke another reviewer. Your review is one input to reconciliation, not release authority.

Record secret-exclusion categories in the manifest without exposing secret contents. Model self-description is not identity evidence; retained CLI metadata establishes reported provenance, not independent attestation of serving infrastructure.

Run `python3 tools/review_ledger_guard.py check` before publishing, and `check --staged` before committing. Read committed-baseline and actor/legacy limitations in the ledger skill. External source snapshots must be retrievable; hashes alone cannot reconstruct dirty reviewed code.

FILE /Users/arunmenon/projects/adrl-world-class/.git/hooks/pre-commit
#!/bin/sh
# ADRL review-ledger guard v1
set -eu
root=$(git rev-parse --show-toplevel)
exec python3 "$root/tools/review_ledger_guard.py" check --staged
