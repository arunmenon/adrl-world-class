# ADRL-CAS-007 — Terminal failure surfaced; ADRL owns zero retries

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (terminal-failure surfacing is tested; the retry-ownership contract with the gateway and the protocol-conformant error shape need tests before D3) |
| Review verdict | AMEND |
| Tenets | 2, 5, 7 |
| Related decisions | CAS-002, CAS-003, CAS-005, SAF-004, SAF-005, FND-001, FND-002, FND-004, RTG-008 |
| Open questions | Q7 |

## Decision

Failure at the top permitted rung, or on a privacy-pinned route, is surfaced to the developer as a protocol-conformant error carrying the typed cause, rather than hidden by another automatic retry — where ADRL itself performs no retries at any rung, the gateway's retries are bounded by a per-turn budget agreed under FND-002, and a retry never crosses a rung, a pin, or a streamed-response boundary.

1. Surfacing: the harness receives a well-formed error in the protocol it speaks (Anthropic Messages error object for Claude Code; the equivalent for Codex CLI) with a stable ADRL error code and the CAS-002 type; ADRL never synthesises a normal-looking assistant message to explain a failure, because that would be a fabricated model output inside the transcript.
2. Retry ownership: ADRL makes exactly one attempt per request at the chosen rung. Connection-level retries before any response byte is forwarded are the gateway's (FND-002) under a per-turn budget (attempts and wall-clock) shared as versioned config; no retry after first byte (CAS-003 clause 2); no gateway fallback to a model outside the rung's membership list (RTG-008 clause 3) or to a cloud model on a pinned session (SAF-004).
3. Ledger: a surfaced failure closes the outcome as `closed_turn` with the type, the rung, the number of gateway attempts observed, and `surfaced=true`; a later developer re-issue of the same instruction is a new turn (FND-003) and is not counted as an automatic retry.

## Context and rationale

At the end of the ladder, tell the truth. If frontier fails, or a privacy-pinned route fails, surface the failure instead of quietly retrying. The amendment settles two things the original left to interpretation. First, *who retries*: retries at multiple layers multiply — Google's SRE guidance is that attempts compound as the product across layers and that each layer should ask "if you really need to perform retries at a given level". A transparent proxy between a harness (which has its own retry logic) and a gateway (which has its own) is precisely the middle layer that should not add a third loop. Second, *how to surface*: ADRL is transparent (FND-001) and the harness expects either a normal response or an API error; injecting an explanatory assistant message would be ADRL authoring model output, which is both a transparency violation and a poisoned transcript for any later continuation. A protocol error with a typed cause is what Claude Code already knows how to show a developer.

## Adversarial review (2026-09-02)

### Steelman
Silent retries at the top rung waste money, hide capability limits from the developer, and on a pinned route would be a privacy violation if they ever reached for cloud (SAF-004). Making the terminal failure explicit is what lets FND-004's "worst case is what you had before" hold: the developer sees the same kind of error they would see without ADRL.

### Attacks
1. **"Another automatic retry" is ambiguous about layers, and the layer that matters most is the gateway.** LiteLLM/the enterprise gateway retries and falls back on its own; Claude Code retries on some errors too. If ADRL adds its own retry, a single failed frontier call becomes harness×ADRL×gateway attempts — the retry amplification the SRE literature warns about, and on a rate-limited frontier endpoint it worsens the outage. The decision must say ADRL's own retry count is zero and bound the gateway's.
2. **A gateway "retry" can be a rung change or a pin violation in disguise.** LiteLLM fallback lists are per alias; if the `frontier` alias's fallback includes a cheaper model, a gateway retry silently lowers the rung (CAS-005/006 violation); if a local-only alias has any cloud fallback, it violates SAF-004. Retry ownership must come with membership constraints (clause 2).
3. **"Surfaced" is undefined for a transparent proxy.** Three options exist — pass the upstream error through unchanged, wrap it with an ADRL code, or return a synthetic assistant message saying "could not complete". The third looks friendliest and is the worst: it is ADRL-authored content in the transcript, it will be cached and continued from, and it is indistinguishable from model output in MEM. Clause 1 forbids it.
4. **Failure at the top rung is not one kind of failure.** A 429/529 at frontier is infrastructure and may legitimately be retried once by the gateway; a verifier failure at frontier is capability and must not be; a context-window rejection is feasibility and should have been caught by SAF-006. Surfacing "the failure" without the CAS-002 type gives the developer nothing to act on and gives MEM nothing to learn from.
5. **Streaming makes "retry" unsafe after first byte** (CAS-003 attack 2). A retry after a `tool_use` block has been forwarded can duplicate a side effect. This decision is where the retry budget lives, so the no-retry-after-first-byte rule must be stated here as well as in CAS-003.

### Evidence
- Google SRE Book, "Addressing Cascading Failures" — "A single request at the highest layer may produce a number of attempts as large as the product of the number of attempts at each layer"; "Limit retries per request"; "Consider having a server-wide retry budget"; "decide if you really need to perform retries at a given level"; randomised exponential backoff (attacks 1, 5) — https://sre.google/sre-book/addressing-cascading-failures/
- Stripe, "Designing robust and predictable APIs with idempotency" — retry after an ambiguous failure is unsafe without an idempotency key; the lost-response case (attack 5) — https://stripe.com/blog/idempotency
- Anthropic, "Parallel tool use" / tool-use docs — every `tool_use` must receive a `tool_result`; a synthetic assistant message inserted by a proxy would break this pairing on the next continuation (attack 3) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- LiteLLM, "Anthropic" provider docs and "Reasoning content" docs — gateway-side parameter dropping and fallback behaviour are configuration, i.e. the gateway's retry/fallback semantics are policy that must be pinned, not assumed (attack 2) — https://docs.litellm.ai/docs/providers/anthropic
- ADRL register SAF-004 — "A pinned session cannot fall back or escalate to cloud; unresolved failure is surfaced to the user" (attack 2).
- ADRL register FND-004 — "Failure defaults to unchanged upstream behaviour" (attack 3; a synthetic message is not unchanged upstream behaviour).
- No direct literature found on retry semantics specific to LLM gateways beyond vendor docs; reasoning from SRE precedent.

### Verdict
**AMEND.** Attack 1 is the load-bearing one: the decision cannot mean "no retries anywhere" (the gateway must handle connection failures) and cannot mean "ADRL retries but not at the top" (that is the amplification case); it must mean ADRL retries zero times and the gateway's retries are bounded and constrained — which is also the Q7 boundary on retry ownership. Attack 2 lands and is answered by binding gateway fallback to rung membership and pins. Attack 3 lands: "surfaced" needed a definition and the synthetic-message option needed to be ruled out explicitly. Attack 4 is answered by carrying the CAS-002 type. Attack 5 is a cross-reference to CAS-003, stated here because the budget lives here. The principle — tell the truth at the end of the ladder — stands.

## Amendments applied
- Added "as a protocol-conformant error carrying the typed cause".
- Added the retry-ownership contract: ADRL zero retries; gateway bounded per turn; no retry across rung, pin or streamed boundary.
- Added clauses 1–3 (surfacing shape and prohibition on synthetic messages; retry ownership and constraints; ledger fields).

## Follow-ups
- [ ] Golden test: frontier returns 5xx after headers but before first content byte → gateway may retry within budget; ADRL forwards the final outcome once; outcome row shows attempts observed.
- [ ] Golden test: frontier fails after a `tool_use` block is streamed → no retry; protocol error to harness; outcome `infrastructure`, `partial_stream=true`, `surfaced=true`.
- [ ] Golden test: pinned session, local endpoint down → protocol error with `policy_constraint`/`infrastructure` type; assert no request reached any cloud backend.
- [ ] Publish the ADRL error-code table and confirm Claude Code and Codex CLI render it (manual check on each harness version in use).
- [ ] Agree with the gateway team the per-turn retry budget and the rule that alias fallback lists are subsets of rung membership (Q7, RTG-008).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: surfacing defined as protocol-conformant typed error; ADRL zero retries; gateway retries bounded and constrained to rung/pin/streaming rules | "Failure at the top rung, or on a privacy-pinned route, is surfaced rather than hidden by another automatic retry." |
