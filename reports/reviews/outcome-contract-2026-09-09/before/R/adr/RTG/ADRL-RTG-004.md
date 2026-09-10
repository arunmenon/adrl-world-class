# ADRL-RTG-004 — Local-first only with a bounded, clean cascade

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (feasibility check is tested; the bounded-attempt and workspace-clean conditions added here need their own tests before the level is re-confirmed) |
| Review verdict | AMEND |
| Tenets | 2, 3, 5 |
| Related decisions | RTG-002, SAF-002, SAF-004, SAF-005, SAF-006, CAS-001, CAS-003, CAS-004, CAS-007 |
| Open questions | Q2, Q5 |

## Decision

Local-first is conditional and is used only when a controlled cascade remains feasible — meaning a higher permitted rung is healthy, the transcript after a bounded local attempt still fits that rung with margin, the local attempt's side effects are recoverable, and the attempt is capped — except on a privacy-pinned session, where local is the only rung and SAF-004 governs instead.

1. Feasibility is evaluated at decision time as: (a) at least one higher rung is permitted by the gates and healthy (SAF-006); (b) current context + the local attempt budget + the handoff note (CAS-004) ≤ the next rung's context ceiling minus a versioned safety margin; (c) the local attempt is bounded by a versioned budget (tool calls, wall-clock, or tokens), after which trip-wires (CAS-001) are evaluated regardless of error state.
2. Local-first is not selected for a turn whose expected first actions are non-idempotent or destructive (deployment, migration, git history rewrite, payments-code paths per Q2), because a wrong local attempt there is not cleanly recoverable even at an action boundary (CAS-003).
3. On a privacy-pinned session this decision does not apply: local is selected because it is the only permitted rung, escalation is unavailable by design, and failure surfaces to the user (SAF-004, CAS-007). The ledger records `cascade_feasible=false, reason=pinned` so these turns are never counted as evidence for or against local-first.

## Context and rationale

Never route local into a dead end. Local is chosen only when, if it fails, we can still escalate cleanly. If a task is already at the edge of the local context window, an escalation later would have nowhere to go. The question is not just "can local probably do this?" but "if local is wrong, is recovery still possible?" The amendment spells out what "cleanly" and "possible" mean: the next rung must have room for the transcript *after* the local attempt, the attempt must be capped so the developer's wait is bounded, and the attempt must not have already done something the stronger model cannot undo. It also resolves an apparent contradiction with SAF-004: on a pinned session no cascade is feasible, yet local must be used — so pinned sessions are carved out and labelled, rather than silently violating this rule or silently distorting local-rung evidence.

## Adversarial review (2026-09-02)

### Steelman
This is the guard that stops "local-first" from becoming "local at all costs" (tenet 3). It reasons about the *second* step, not the first, which is exactly what the cascade literature says matters: cascades are cheap only when the escalation path is real. It is tested in `policy.py` and `live_router.py`.

### Attacks
1. **It contradicts SAF-002/SAF-004 as written.** A privacy-pinned session cannot escalate to cloud, so "a controlled cascade" is never feasible there — a literal reading forbids local on exactly the sessions that must be local. The register's plain-terms text does not address this. Either RTG-004 is silently ignored on pinned sessions (undocumented behaviour) or pinned sessions violate an Accepted decision.
2. **"Feasible" only reasons about context, not about side effects.** The plain-terms text talks about context-window headroom. But a local model that emits a wrong `Edit`/`Bash` before tripping a wire has *changed the workspace*; escalation at an action boundary (CAS-003) prevents replay but does not undo the edit. The next model inherits a mutated repo it did not reason its way into. SWE-agent reports that after one failed edit the chance of eventual edit success falls from 90.5% to 57.2% — cascading failed edits are a recognised failure class. "Recoverable" needs to be part of feasibility.
3. **The failed-attempt cost is unbounded.** Nothing caps how long local may flail before the trip-wires fire; CAS-001 fires on counts, and OpenHands' equivalent thresholds are 3–6 repetitions. For a developer at the keyboard a 6-repetition loop on a slow local model is a minute or more of dead time. Local-first must carry an attempt budget or the "developer waits through a failed attempt first" cost that RTG-002 worries about is uncontrolled.
4. **Escalation after a local attempt carries the local attempt's transcript into the expensive rung.** Every failed local tool loop is now paid input at frontier prices, and the frontier cache is cold (the prefix differs from anything cached). RTG-004's context check must include the local attempt's token growth, not just the current size, or the "fits" test is wrong at exactly the moment it matters.

### Evidence
- Yang et al., "SWE-agent" (NeurIPS 2024) — "Any attempt at editing has a 90.5% chance of eventually being successful. This probability drops off to 57.2% after a single failed edit"; cascading failed edits are 23.4% of failures (attack 2) — https://arxiv.org/html/2405.15793
- OpenHands, "Stuck Detector" (SDK docs) — repeating action-observation 4+, action-error 3+, alternating 6+ cycles before flagging; establishes what "bounded attempt" looks like in a production agent (attack 3) — https://docs.openhands.dev/sdk/guides/agent-stuck-detector
- Dekoninck et al., "A Unified Approach to Routing and Cascading for LLMs" (arXiv 2024) — cascading is only useful with a good post-hoc estimator; otherwise "the effectiveness of cascading strategies is severely limited" (steelman, attack 3) — https://arxiv.org/abs/2410.10347
- Anthropic, "Prompt caching" — "Cache hits require 100% identical prompt segments"; a transcript grown by a local attempt cannot hit any frontier cache (attack 4) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- MCP blog, "Tool Annotations as Risk Vocabulary" (2026) — `destructiveHint` / `idempotentHint` semantics as a vocabulary for "recoverable" (clause 2) — https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- ADRL register, SAF-004: "A pinned session cannot fall back or escalate to cloud; unresolved failure is surfaced to the user" (attack 1).

### Verdict
**AMEND.** Attack 1 is a genuine register conflict and is resolved by clause 3 (explicit carve-out with ledger marker, so pinned turns do not contaminate local-rung evidence — a MEM-004 concern as well). Attack 2 lands: "clean" recovery is about side effects as much as context, and clause 2 adds the destructive-first-action exclusion using MCP's annotation vocabulary. Attacks 3 and 4 land and are answered by clause 1(b)–(c): the context test must include the attempt's growth, and the attempt must be capped. The core decision — local only when escalation remains real — is well supported and stands.

## Amendments applied
- Expanded "controlled cascade remains feasible" into the four-part feasibility test in clause 1.
- Added clause 2: no local-first when the expected first actions are non-idempotent or destructive.
- Added clause 3: pinned-session carve-out with explicit ledger reason.

## Follow-ups
- [ ] Golden test: local attempt budget exhausted with no errors → trip-wire evaluation runs and escalation is offered (not "no errors, keep going").
- [ ] Golden test: pinned session with context above local ceiling → SAF-005 block, not an RTG-004 "infeasible cascade" verdict.
- [ ] Tag Claude Code / MCP tools with side-effect class (read-only / idempotent / destructive) in `features.py` and exclude destructive-first turns from local-first.
- [ ] Shadow measurement: median tokens and wall-clock added by failed local attempts before escalation, split by trip-wire type.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: feasibility defined (healthy higher rung, context headroom after attempt, recoverable side effects, capped attempt); pinned-session carve-out | "Local-first is conditional and is used only when a controlled cascade remains feasible." |
