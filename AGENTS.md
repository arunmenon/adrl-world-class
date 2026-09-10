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
