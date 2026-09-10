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
