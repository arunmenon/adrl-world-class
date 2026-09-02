# ADRL-SAF-001 — Hard gates first, on every request

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (gates are tested, not attacked; the per-request scope introduced here is untested) |
| Review verdict | AMEND |
| Tenets | 2, 4 |
| Related decisions | FND-003, FND-004, SEM-001, SEM-003, SAF-002, SAF-003, SAF-006, RTG-002, RTG-006, LRN-006 |
| Open questions | Q2 |

## Decision

Hard gates execute on every request — user turn, continuation, utility, subagent, pre-warm and passthrough alike — before, and cannot be overridden by, heuristics, learned policy, or the routing-path failure fallback; gate outcomes may only tighten the permitted set within a session.

1. The gate set produces a permitted-rung set per request; optimisation (RTG) chooses only within it. A request with an empty permitted set follows SAF-004/SAF-005.
2. Gate outcomes are monotone within a session lineage: a later request may remove rungs (pin, infeasibility) but never restore one that a gate removed, except through the audited human release path defined in SAF-002.
3. The gate stage has its own failure semantics (FND-004 as amended): gate failure on a pinned session is fail-closed; on an unpinned session the request is marked `unscanned` and the mark can never widen the permitted set.

## Context and rationale

Ordering is the security property. Gates run first and produce a set of permitted rungs; only then does anything optimise inside that set. The classifier is never in a position to say "frontier would give a better answer" and send secret-bearing code to the cloud.

The amendment fixes scope, not ordering. The register binds gates to "before routing" (SAF-003) and routing to "once per user turn" (FND-003). Read together, gates run once per turn — and the fourteen continuation requests that follow, which carry `tool_result` blocks with file contents, command output and environment dumps, are exactly where secrets enter the transcript. A gate that runs only on the typed instruction scans the one message least likely to contain a credential. The amendment also names the two things that *could* override a gate today and forbids them: FND-004's original blanket fail-open, and any state reset (episode boundary, session restart) that would restore a rung a gate removed.

## Adversarial review (2026-09-02)

### Steelman
This is tenet 2 in decision form and the simplest possible precedence rule: partition first, optimise second. It is how every mature policy engine works (admission control before scheduling; authorization before business logic), it is trivially auditable, and it makes the learned router's authority question moot for safety — an ML component that only ever sees the permitted set cannot leak by being wrong.

### Attacks
1. **Gates are per-turn in practice, and secrets arrive per-request.** SAF-003 says detection occurs "before routing"; FND-003 says routing is per user turn; SEM-003 says continuations trigger no fresh decision. Nothing in the register says gates run on continuations. The dominant ingress for secrets in coding-agent traffic is the tool result (`Read` of `.env`, `Bash` output of `env`, a test fixture with a live token), not the user's typed sentence. If the gate runs once per turn, it misses most of the surface.
2. **Passthrough and utility classes bypass the gate by construction.** SEM-001 says passthrough is "passed through unchanged" and SEM-004 says unknown calls pass through. A `count_tokens` request carries the full prompt. If the gate set does not run on these classes, "hard gates execute before heuristics" is true and irrelevant for ~72% of wire volume.
3. **FND-004 overrides the gate.** The original FND-004 says failure defaults to unchanged upstream behaviour. A scanner exception is a failure. So on a pinned session a scanner crash sends the request to the cloud — the gate is overridden not by a heuristic but by the escape hatch. The decision says gates "cannot be overridden by heuristics or learned policy" and is silent on the fallback path, which is the one that actually can.
4. **Monotonicity is assumed, not stated.** SAF-002 says pins are one-way; SAF-006 removes infeasible rungs per request; SEM-005 releases hysteresis at a boundary. Nothing says what a gate outcome does when the *session* restarts, is resumed, or an episode boundary fires. A state reset that clears gate outcomes is a bypass that no heuristic needed.
5. **Gates are tested, not attacked.** The evidence pack says so. A regex scanner can be defeated by trivial transformations that still leave a usable secret in the transcript (base64 in a tool result, a key split across two `Read` calls, a secret in an image or PDF block that `count_tokens` accepts). Ordering does not help if the gate itself is porous; SAF-003's precision/recall is the real bound.
6. **The LLM classifier reads the same content as the gate.** RTG-006 puts an advisory LLM in the hot path on the ambiguous middle. It cannot override the gate — but it *sees* the content on an unpinned session and its call goes to whichever rung serves classification. If that is a cloud model, the classifier is itself an egress path that runs after gating but before the gate's *consequence* for that request is known. Sub-clause 1's ordering must include the classifier call as a routed request.

### Evidence
- Anthropic, "Token counting" (Claude Platform docs) — `count_tokens` accepts system, tools, images, PDFs, thinking blocks and messages: the full prompt; bears on attack 2 — https://platform.claude.com/docs/en/build-with-claude/token-counting
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — a tool-use loop is one assistant turn with many round trips; every round trip carries new `tool_result` content; bears on attack 1 — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- AuthZed, "Understanding 'Failed Open' and 'Fail Closed'" (blog) — fail-open in an authorization control grants access during failures; bears on attack 3 — https://authzed.com/blog/fail-open
- Costa, Köpf et al., "Securing AI Agents with Information-Flow Control" (arXiv 2505.23643, 2025) — dynamic taint tracking of confidentiality labels through an agent loop, enforced deterministically before actions; precedent that labels must propagate per step, not per task; bears on attacks 1, 4 — https://arxiv.org/abs/2505.23643
- Basak et al., "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (ESEM 2023, arXiv 2307.00714) — best-recall open-source tool at 88%, most at or below 67%; gates are only as hard as the scanner; bears on attack 5 — https://arxiv.org/abs/2307.00714

### Verdict
**AMEND.** Attacks 1, 2 and 3 land and together describe the largest privacy gap in the register: the gate is correctly *ordered* and incorrectly *scoped*, and the escape hatch can override it. Attack 4 is closed by one sentence on monotonicity. Attack 5 is real but belongs to SAF-003. Attack 6 is a subtle ordering issue folded into sub-clause 1 (the classifier call is itself a routed request subject to the permitted set). The precedence principle survives untouched; the amendment makes it apply to the traffic that matters.

## Amendments applied

- Added "on every request — user turn, continuation, utility, subagent, pre-warm and passthrough alike".
- Added "or the routing-path failure fallback" to the list of things that cannot override gates.
- Added "gate outcomes may only tighten the permitted set within a session".
- Added sub-clause 1 (permitted set per request; classifier call included), sub-clause 2 (monotonicity, human release path excepted), sub-clause 3 (gate failure semantics by pin state, `unscanned` marker).

## Follow-ups

- [ ] Golden test: continuation whose `tool_result` contains a high-confidence AWS key → session pinned on that request; the request is served locally or blocked.
- [ ] Golden test: `count_tokens` on a pinned session → not forwarded to the gateway.
- [ ] Golden test: scanner raises on a pinned session → fail-closed; on an unpinned session → forwarded with `unscanned` in the ledger; a later request cannot use `unscanned` to lift a pin.
- [ ] Golden test: RTG-006 classifier call on a session that becomes pinned in the same request → classifier call served locally or skipped.
- [ ] Adversarial suite (first "attacked, not tested" evidence): base64 secret in tool output; secret split across two reads; secret inside a PDF/image block; secret in a subagent delegation message. Report which are caught.
- [ ] Instrument: per-request gate latency at p99 on continuations (the amendment multiplies gate invocations ~15×).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: gates on every request class; fallback path cannot override; monotone outcomes; gate failure semantics | "Hard gates execute before, and cannot be overridden by, heuristics or learned policy." |
