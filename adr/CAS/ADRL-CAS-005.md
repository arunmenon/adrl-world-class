# ADRL-CAS-005 — Sticky escalation within an episode

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · unchanged |
| Maturity | D2 Tested, review recommends D2 Tested (hysteresis is implemented and tested; the ratchet-cost measurement in the follow-ups is needed before D3) |
| Review verdict | APPROVE |
| Tenets | 1, 6 |
| Related decisions | SEM-005, SEM-003, CAS-006, CAS-007, RTG-009, SAF-002, SEM-006 |
| Open questions | Q3 |

## Decision

Escalation is sticky within an episode; only a conservative episode boundary may lower the rung.

## Context and rationale

Escalate up, stay up, and only come down on a real boundary. Without stickiness you get flapping — paying the switch cost repeatedly and destroying the cache each time. The cost model now proposed in RTG-009 makes the argument numeric: every rung switch on a long transcript is a cache-write event at 1.25–2× base input on the new rung, and providers' caches are per-model, so an oscillating router pays that repeatedly. Control-systems and network-routing precedent (BGP route-flap damping: suppress on accumulated instability, release only when a decaying penalty crosses a *lower* reuse threshold) is the same asymmetric-threshold design: the bar to come down is deliberately higher than the bar to go up. The lowering event is owned by SEM-005, which is where the "is the boundary too conservative to ever fire?" question belongs; this decision only says that no *other* event may lower the rung.

## Adversarial review (2026-09-02)

### Steelman
Asymmetric hysteresis is the textbook cure for oscillation, and every rung switch in this system has a real, measurable cost (cache rebuild, handoff, cold context) plus a correctness risk (CAS-004). Tying the release to a semantic event rather than a timer means the rung never drops mid-task. It is small, tested, and composes cleanly with SEM-005 and CAS-006.

### Attacks
1. **Sticky-up plus conservative-down is a ratchet toward always-frontier.** The SEM bucket's own open item asks whether episode detection is "so conservative a rung is never lowered in practice". If so, one escalation early in a long session converts the rest of the session to frontier and the savings case evaporates — while the router still pays its own overhead. This is a real risk, but it is a *calibration* risk in SEM-005 (the boundary), not a defect in the stickiness rule, and the correct response is to measure the ratchet cost (follow-up) rather than to weaken stickiness.
2. **A time-decay alternative exists and is not considered.** BGP damping decays its penalty exponentially so a suppressed route eventually returns without a semantic event. A TTL on escalation (e.g. drop after N turns without a trip-wire) would bound the ratchet. Answered: a timer-based drop is exactly the "false boundary silently drops a hard task back to local mid-flight" failure SEM-005 rejects; and provider cache TTLs (5 min default on Anthropic) mean a long idle gap already makes the *next* decision cache-cold on every rung, at which point SEM-005's conservative boundary has a cheap moment to fire. Decay belongs in SEM-005's boundary detector as one signal, not in CAS-005 as an override.
3. **"Episode" is shared with subagents and is not defined for them.** A background subagent escalating (Q3) — does the parent's episode become sticky-high? Does the child's? Answered by scope: CAS-005 is per routing identity, and SEM-006 (D0) says subagents get their own identity; until that exists subagents pass through and never escalate, so there is no flap to prevent. The gap is real but belongs to the proposed CAS-008, not to this text.
4. **Stickiness keyed to intent, not to what served, would drift.** If the sticky rung is the one ADRL *asked for* and the gateway served another, the next continuation is routed on a fiction. Answered by CAS-006, which is the runtime twin of this decision and is amended in this review to record served model as well as rung.
5. **Stickiness interacts with the privacy pin only in one direction, and that is correct.** A pinned session cannot escalate (SAF-004), so it cannot be sticky-high; an unpinned session that escalates and is then pinned mid-episode drops to local because the pin is a gate (SAF-001) and gates precede stickiness. No conflict; noted so that a future reader does not "fix" it.

### Evidence
- IETF, RFC 2439 "BGP Route Flap Damping" — penalty accumulates per flap, route suppressed above a cutoff and reused only when the exponentially-decayed penalty falls below a *lower* reuse threshold; rationale is limiting oscillation load on peers (steelman; attack 2) — https://www.rfc-editor.org/rfc/rfc2439
- Anthropic, "Prompt caching" — cache writes 1.25×/2× base, reads 0.1×; 5-minute default TTL; exact-prefix matching — the per-switch cost that stickiness avoids (steelman; attack 2) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- GitHub Docs, "About Copilot auto model selection" — "Switching models mid-session has shown increased cost without ample improvements in quality" — an independent production finding for the same stance (steelman) — https://docs.github.com/copilot/concepts/auto-model-selection
- OpenRouter, "Auto Router" docs — implements "Session Stickiness" but allows a different model "on every turn" when the task type shifts; the contrast case that CAS-005 rejects (attack 1 context) — https://openrouter.ai/docs/guides/routing/routers/auto-router
- Claude Code, "Create custom subagents" — background subagents run concurrently; nested spawning to three layers (attack 3) — https://code.claude.com/docs/en/sub-agents
- ADRL register SEM-005 / open item — "Episode-boundary detection is conservative by design — so conservative a rung is never lowered in practice?" (attack 1).

### Verdict
**APPROVE.** Every attack either lands on a *neighbouring* decision (SEM-005 calibration, SEM-006/CAS-008 subagents, CAS-006 served-rung) or is answered by the cost model and precedent. The one substantive risk — the ratchet — is real but is a property of the boundary detector's threshold, and weakening stickiness to compensate would reintroduce the mid-task drop the tenet forbids. The text stands as written; the follow-ups make the ratchet cost visible so SEM-005 can be tuned on evidence.

## Amendments applied
None — decision stands as written.

## Follow-ups
- [ ] Shadow metric: for sessions with at least one escalation, the share of subsequent turns and tokens served above the initial rung until episode release ("ratchet cost"), reported after cache effects (RTG-009). Feed to SEM-005 tuning.
- [ ] Golden test: a trip-wire escalation followed by a non-boundary user turn stays at the escalated rung; the same followed by a SEM-005 boundary event lowers it.
- [ ] Golden test: pin applied mid-episode on an escalated session → next request routes local (gate precedes stickiness) and outcome typed `policy_constraint`.
- [ ] Cross-reference CAS-008 (proposed) for subagent stickiness scope once SEM-006 leaves D0.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Escalation is sticky within an episode; only a conservative episode boundary may lower the rung." |
