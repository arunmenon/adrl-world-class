# Workflow review dispositions

- Coordinator/scope: accepted. Codex named coordinator; complete declared source snapshot plus contested exclusions required.
- Freeze: accepted underlying need; rejected mandatory commit. Dirty and untracked files must be copied and hashed, with before/after verification. A commit alone would omit current work and is not necessary to detect mutation.
- Severity: accepted. Preserve reviewer severity; coordinator cannot downgrade away a block. Reviewer correction with evidence or explicit product-owner disposition resolves a dispute.
- Status mismatch: accepted; use `unavailable` consistently.
- Dated retrospective pointer: retained as an explicitly historical assignment, not a current default window. Future reviews require fresh windows/inventories.
- Identity: retain original JSON/session/model usage. Do not infer served identity from self-description. No-session-persistence means account session-history verification is not guaranteed; retained raw response is provenance, not independently attested identity.
- Manual repair: agree it is not RSI. A manual repair can still improve adaptive-routing behavior; it is not evidence of an autonomous learning process.

This is a skill review, not a two-day ADRL review, runtime test or maturity promotion.

## Operating model

Codex prepares the next bounded wave → Fable challenges the plan → Codex implements and tests → Fable inspects frozen evidence → Codex addresses findings → Fable rechecks material fixes → ADR evidence and roadmap position are updated. Blocking disagreements remain visible for the product owner.

Installed for automatic discovery in both tools, with an explicit register AGENTS checkpoint. Invocation: Codex `$adrl-critical-review`; Claude Code `/adrl-critical-review`. This is an instruction-based process, not a CI-enforced gate or scheduler. The existing implementation automation was not restarted.

## Recheck result

Fable 5.1 reported no remaining material blockers in the skill body and dispositions. Scope excluded runtime, handoff implementation and full retrospective. Nonblocking identity/secret-exclusion clarifications were added to the shared handoff reference afterward. The full two-day review remains not started.
