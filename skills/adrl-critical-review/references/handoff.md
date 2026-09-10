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
