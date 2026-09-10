"""Negative closure checks. Primary: ADRL-FND-005. Secondary: ADRL-EVL-009."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "sync", Path(__file__).parents[1] / "tools/check_taxonomy_sync.py"
)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.roots = {"R": self.base / "register", "C": self.base / "core"}
        self.home = self.base / "home"
        self.patcher = patch.object(Path, "home", return_value=self.home)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.aid = "ADRL-FND-005"
        self.write("C:src/changed.py", "already dirty before baseline\n")
        self.write(
            "R:adr/FND/ADRL-FND-005.md",
            "# Decision\n| Status | Accepted |\n| Maturity | D1 |\n| Review verdict | APPROVE |\n",
        )
        self.write(
            "R:INDEX.md", "| [ADRL-FND-005](adr/FND/ADRL-FND-005.md) | initial |\n"
        )
        self.write("R:adr/FND/README.md", "| ADRL-FND-005 | initial |\n")
        self.write("R:CHANGELOG.md", "# History\n")
        self.write("R:skills/adrl-taxonomy-sync/SKILL.md", "canonical skill\n")
        for tag in [".codex", ".claude"]:
            q = self.home / tag / "skills/adrl-taxonomy-sync/SKILL.md"
            q.parent.mkdir(parents=True)
            q.write_text("canonical skill\n")
        self.baseline = sync.snapshot(self.roots)
        self.write("C:src/changed.py", "new behavior\n")
        self.write("R:reports/reviews/proof.txt", "test evidence\n")
        self.write("R:reports/reviews/review.md", "semantic review\n")
        for name, link in [
            ("adr/FND/ADRL-FND-005.md", "../../reports/reviews/proof.txt"),
            ("INDEX.md", "reports/reviews/proof.txt"),
            ("adr/FND/README.md", "../../reports/reviews/proof.txt"),
            ("CHANGELOG.md", "reports/reviews/proof.txt"),
        ]:
            q = self.roots["R"] / name
            line = f"| {self.aid} | 2026-09-09 <!-- taxonomy-sync:wave:{self.aid} --> [evidence]({link}) |\n"
            if name == "INDEX.md":
                line = line.replace(self.aid, f"[{self.aid}](adr/FND/{self.aid}.md)", 1)
            if name in ["INDEX.md", "adr/FND/README.md"]:
                q.write_text(line)
            else:
                q.write_text(q.read_text() + line)
        self.packet = {
            "wave": "wave",
            "date": "2026-09-09",
            "owners": [
                {
                    "id": self.aid,
                    "kind": "behavior",
                    "summary": "real behavior change",
                    "limitations": "fixture only",
                    "fields": sync.fields(
                        (self.roots["R"] / f"adr/FND/{self.aid}.md").read_text()
                    ),
                    "evidence": [self.ref("reports/reviews/proof.txt")],
                }
            ],
            "file_owners": {"C:src/changed.py": [self.aid]},
            "review": {
                "record": self.ref("reports/reviews/review.md"),
                "status": "accepted",
                "reviewer": "independent fixture reviewer",
                "covered_adrs": [self.aid],
                "blocking_findings": [],
            },
        }
        self.refresh()

    def write(self, key, text):
        tag, name = key.split(":", 1)
        p = self.roots[tag] / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def ref(self, name):
        return {"path": name, "sha256": sync.digest(self.roots["R"] / name)}

    def refresh(self):
        after = sync.snapshot(self.roots)["files"]
        before = self.baseline["files"]
        self.packet["changes"] = {
            k: {"before": before.get(k), "after": after.get(k)}
            for k in before.keys() | after.keys()
            if before.get(k) != after.get(k)
        }
        self.write("R:reports/reviews/inputs.json", json.dumps(after))
        self.packet["review"]["inputs"] = self.ref("reports/reviews/inputs.json")

    def run_gate(self):
        return sync.check(self.roots, self.baseline, self.packet)

    def test_complete_dirty_baseline_passes(self):
        self.assertEqual(self.run_gate()["status"], "passed")

    def test_missing_owner(self):
        self.packet["file_owners"] = {}
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_added_input_not_hidden(self):
        self.write("C:src/new.py", "new")
        self.refresh()
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_deleted_input_requires_mapping(self):
        (self.roots["C"] / "src/changed.py").unlink()
        self.refresh()
        self.packet["file_owners"] = {}
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_deleted_mapped_input_passes(self):
        (self.roots["C"] / "src/changed.py").unlink()
        self.refresh()
        self.assertEqual(self.run_gate()["status"], "passed")

    def test_stale_evidence(self):
        self.write("R:reports/reviews/proof.txt", "different")
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_missing_each_register_mapping(self):
        for name in [
            "INDEX.md",
            "CHANGELOG.md",
            "adr/FND/README.md",
            "adr/FND/ADRL-FND-005.md",
        ]:
            with self.subTest(name=name):
                p = self.roots["R"] / name
                old = p.read_text()
                p.write_text(old.replace("taxonomy-sync:wave", "no-marker"))
                self.refresh()
                with self.assertRaises(ValueError):
                    self.run_gate()
                p.write_text(old)
                self.refresh()

    def test_duplicate_index(self):
        p = self.roots["R"] / "INDEX.md"
        p.write_text(p.read_text() * 2)
        self.refresh()
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_field_change_needs_human_record(self):
        p = self.roots["R"] / f"adr/FND/{self.aid}.md"
        p.write_text(p.read_text().replace("| D1 |", "| D4 |"))
        self.refresh()
        self.packet["owners"][0]["fields"] = sync.fields(p.read_text())
        with self.assertRaises((KeyError, ValueError)):
            self.run_gate()

    def test_pending_review(self):
        self.packet["review"]["status"] = "pending"
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_post_review_source_drift(self):
        self.write("C:src/changed.py", "later modification")
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_mirror_drift(self):
        (self.home / ".claude/skills/adrl-taxonomy-sync/SKILL.md").write_text("drift")
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_symlink_input(self):
        (self.roots["C"] / "src/link.py").symlink_to(self.roots["C"] / "src/changed.py")
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_unsafe_evidence_path(self):
        self.packet["owners"][0]["evidence"][0]["path"] = "../escape"
        with self.assertRaises(ValueError):
            self.run_gate()


if __name__ == "__main__":
    unittest.main()
