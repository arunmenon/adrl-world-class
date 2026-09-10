# Findings

## review-governance-post-2026-09-10:RG-01 — Recheck evidence is not bound to the finding it clears

blockers() validates that the cited artifact is sealed and has a matching reviewer recheck event, but never checks that the artifact or event names finding_id. One recheck artifact can clear every blocking finding in the folder. README discloses that evidence justification is unchecked.

Acceptance: Recheck events carry finding ids; verified-fixed clears only when the cited event lists that finding_id. Test with one artifact cited by two findings.

## review-governance-post-2026-09-10:RG-02 — Installed skill copy identity not evidenced

The packet supplies only the register SKILL.md. The report claims installed Codex and Claude copies are reviewed extra scope, but no hashes for those copies were provided, so byte-identity is unverified.

Acceptance: inputs.json lists both installed copies with sha256 equal to the register copy.

## review-governance-post-2026-09-10:RG-03 — Disposition vocabulary declared but not enforced at write time

DISPOSITIONS is defined but unused; validate() checks ROLES only for ledger events. A misspelled disposition or actor in dispositions.jsonl commits successfully and remains permanently unresolved rather than being rejected before it enters append-only history.

Acceptance: validate() rejects unknown disposition values or roles in newly appended rows only, preserving committed history. Test for a typo row.

