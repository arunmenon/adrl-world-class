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
