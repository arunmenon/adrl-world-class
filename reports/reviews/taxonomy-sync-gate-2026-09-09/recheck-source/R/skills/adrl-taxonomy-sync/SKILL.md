---
name: adrl-taxonomy-sync
description: Keep ADRL implementation changes synchronized with owning architecture decisions and verify the local closure record. Use before editing ADRL runtime, configuration, adapters, tests, tooling or architecture; apply at completion alongside independent review.
---

# ADRL taxonomy synchronization

Canonical skill: `/Users/arunmenon/projects/adrl-world-class/skills/adrl-taxonomy-sync/SKILL.md`. Identical installed copies belong in Codex and Claude skills. Register is `adrl-world-class`; runtime is sibling `adrl-core`. This is a required local completion workflow under both AGENTS.md files, not remote CI or a tamper-proof control.

## Before changing implementation

Read repository instructions and the owning ADRs. Name primary and secondary owners based on behavior, not merely file location. Adapters normally anchor in SEM-007 with relevant FND/CAS/TRU/MEM/OPS decisions. If ownership is genuinely new, propose an ADR in an existing appropriate bucket; do not silently invent a contract.

Use `python3 tools/check_taxonomy_sync.py begin --out <absolute-new-path-outside-both-repos>` from the register before edits. It includes dirty/untracked declared inputs, so unrelated existing changes are not falsely attributed to this wave. Preserve the baseline with the critical-review source snapshot. Inspect the tool's fixed scope/exclusions: changes outside that scope need a reviewed scope expansion or explicit separate disposition, not an assertion that all files were checked. A missed baseline must be reconstructed from actual saved artifacts and disclosed; never run begin after edits and pretend it was captured before.

## Complete the same change in the register

For every changed/added/deleted input, explicitly map ownership in a closure JSON record. Record whether this is behavior, evidence, refactor or workflow. Preserve decision IDs, previous decision wording in changelogs and dated history. Tests support only their actual scope. Update owning ADRs, their changelog rows, INDEX rows, affected bucket rows and root CHANGELOG with dated evidence links and the same marker `<!-- taxonomy-sync:<wave>:<ADRL-ID> -->` on each mapping line. Include an explanatory dated ADR section, not just a token marker. Markers let a checker locate the update; the semantic reviewer judges whether its content is true and sufficient.

Keep unchanged maturity/status/verdict fields exactly unchanged. A change needs a separately pinned human disposition record with `adr`, `before` and `after` field objects, `human_name`, `date`, and `display_before`/`display_after` for protected INDEX/bucket verdict and maturity cells. These fixed-format display cells are checked against baseline; historical abbreviated values are not normalized. The checker only validates the record's structure; it cannot authenticate the human or decide graduation. Historical grade/index reconciliation remains its own open work and cannot be claimed complete from this forward check.

## Closure record and review

Schema is defined by [the checker](/Users/arunmenon/projects/adrl-world-class/tools/check_taxonomy_sync.py). A worked self-application record is saved in `reports/reviews/taxonomy-sync-gate-2026-09-09/closure.json`; use its shape, never reuse its hashes or review.

Required fields: wave slug, date, `changes` covering every declared changed path with before/after SHA-256 (null for absent), `file_owners` covering non-derived changed inputs, and `owners` with id/kind/summary/limitations/current `fields` and nonempty pinned `evidence` references (`path` relative to register and `sha256`). Derived register files are the named ADRs, their bucket READMEs, INDEX and CHANGELOG; stray ADR edits fail. Include pinned semantic `review.record`, `review.inputs` (all current source hashes), status accepted, named reviewer, covered ADRs and no unresolved blocking findings. These are auditable assertions, not automatic independent verification.

Use adrl-critical-review for substantive work. Reviewer must check omitted owners, actual diff versus ADR wording, code/test links, evidence applicability, unchanged versus amended decisions, maturity limits and unsupported claims. An authored conclusion cannot stand in for the original reviewer response. Missing review means pending, never accepted. Do routine synchronization within existing authority; do not ask the user to approve ordinary evidence updates. Do not treat automated review rejection as waived.

After runtime checks, register edits, installed mirror updates and semantic review, run:

`python3 tools/check_taxonomy_sync.py check --baseline <saved-baseline.json> --packet <closure.json> --out <new-receipt-outside-both-repos.json>`

Exit nonzero means **taxonomy synchronization incomplete**, so do not claim the implementation wave complete. Keep failure output and fix it or report the blocker. The final receipt pins the baseline, closure, source and separately referenced evidence/review; rerun after any of those changes. It must be outside both repos to avoid self-reference. Do not make post-check source edits while citing the old receipt as current.

## Verification and reporting

Run stdlib checker tests with `python3 -m unittest discover -s tests -p 'test_taxonomy_sync.py' -v` from the register. Runtime changes still need core's ordinary checks. Workflow/document-only edits do not justify relabeling archived full-source tests as current when AGENTS/docs hashes changed; state the exact unchanged runtime subset if reusing evidence. Do not restart automation or authorize model runs through this workflow.

End implementation reports with: owning ADRs, synchronization receipt, independent review disposition, maturity change (usually none), and remaining limitations. This gate prevents common omissions when invoked; arbitrary edits or skipped commands remain possible until separately deployed CI/branch protection exists.
