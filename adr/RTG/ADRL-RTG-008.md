# ADRL-RTG-008 — Rung vs endpoint, with a leak contract

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (separation is tested; the gateway-side contract added here is a Q7 deliverable and does not change the level) |
| Review verdict | AMEND |
| Tenets | 7 |
| Related decisions | FND-002, RTG-001, RTG-005, RTG-009 (proposed), CAS-004, CAS-005, CAS-006, OPS-006 |
| Open questions | Q1, Q7 |

## Decision

Capability-rung selection is separate from endpoint/provider selection inside a rung, subject to a contract with the gateway that (a) the served model and provider are reported back on every response, (b) the endpoint serving a session is held stable within a rung for the life of a turn and, absent failure, an episode, and (c) rung membership is a versioned, shared configuration — because prompt caches and reasoning signatures are model-specific, so an endpoint change inside a rung is not free to ADRL's objective.

1. The gateway reports `gen_ai.response.model` and `gen_ai.provider.name` (OpenTelemetry GenAI conventions) or equivalent on every response; ADRL records them (CAS-006) and treats a within-rung model change as a cache-cold and signature-invalidating event in RTG-009 accounting.
2. Within-rung failover is the gateway's decision (FND-002), but it is *visible* to ADRL and counts as an infrastructure outcome (CAS-002), never as a capability outcome.
3. ADRL never names a model in policy; the rung→model list lives in shared, versioned config owned jointly with the gateway team so that a model deprecation is a config change on both sides, not a routing-logic change.

## Context and rationale

"Frontier" is a capability, not a model name. ADRL picks the rung; the gateway picks which model, which provider, and what retry behaviour serves it. FND-002 restated where it bites. The amendment acknowledges that the separation leaks in three specific places: caches are per-model (both Anthropic and OpenAI say so), thinking-block signatures and encrypted reasoning items are model- or family-specific, and sticky state must record what actually served (CAS-006). None of these argue against the separation — they argue for a contract across it, which is precisely what Q7 asks for.

## Adversarial review (2026-09-02)

### Steelman
Rate-of-change is the right reason to split: model ids, quotas and providers churn monthly; "how hard is this work" does not. Coupling them makes every deprecation a routing change. Every commercial gateway (LiteLLM, Bedrock, OpenRouter) already implements provider-level fallback, so ADRL re-implementing it would duplicate mechanical execution the gateway owns.

### Attacks
1. **The abstraction leaks through the cache.** Anthropic's cache requires "100% identical prompt segments" and is keyed to the request as sent; OpenAI states "a different model can use different weights and caching behavior". If the gateway swaps model within the "frontier" rung mid-session (load balancing, quota), the transcript is re-billed at full write cost — an ADRL cost-objective event caused by a decision ADRL cannot see. RTG-005's cache term is unimplementable unless the gateway reports the served model.
2. **The abstraction leaks through reasoning signatures.** Anthropic thinking blocks carry a `signature` that, for Claude Fable 5.1 / Mythos 5.1 preserved thinking blocks, "covers the `system` prompt, the `tools`, and the messages that preceded the block"; moving to an earlier model "loses it, the API drops them"; OpenAI's encrypted reasoning "can be reused only within the same model family". A within-rung provider swap is therefore a CAS-004 handoff event, not a transparent retry — and ADRL's continuation logic must know it happened.
3. **Served-rung observability (CAS-006/OPS-006) presupposes a reporting contract that RTG-008 does not state.** If the gateway rewrites the response `model` field to the alias the client asked for (a common gateway behaviour), ADRL records the *intended* model and CAS-006 is silently violated. Kiro users have opened issues asking to see which model "auto" actually used — the same observability gap at the product layer.
4. **"Inside a rung" assumes the gateway knows the rung.** The gateway sees a model alias, not a rung. Unless rung membership is shared config (clause 3), the gateway's fallback list for `frontier-alias` may include a model that ADRL's registry considers `cheap_cloud`, and a "within-rung" failover becomes an unrecorded rung change.

### Evidence
- OpenTelemetry, GenAI semantic conventions — `gen_ai.request.model` ("model a request is being made to") vs `gen_ai.response.model` ("the name of the model that generated the response"); `gen_ai.provider.name`; cache usage attributes (attacks 1, 3) — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (registry page now marked "moved to the OpenTelemetry GenAI semantic conventions repository", https://github.com/open-telemetry/semantic-conventions-genai)
- Anthropic, "Prompt caching" — "Cache hits require 100% identical prompt segments"; hierarchy tools→system→messages (attack 1) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- OpenAI, "Prompt caching" — "A different model can use different weights and caching behavior" (attack 1) — https://developers.openai.com/api/docs/guides/prompt-caching
- Anthropic, "Thinking" (platform docs) — for Fable 5.1 / Mythos 5.1 preserved thinking blocks the signature "covers the `system` prompt, the `tools`, and the messages that preceded the block"; conversation moving to an earlier model "loses it, the API drops them" (attack 2) — https://platform.claude.com/docs/en/build-with-claude/thinking
- OpenAI, "Reasoning models" (API docs) — "Persisted reasoning can be reused only within the same model family" (attack 2) — https://developers.openai.com/api/docs/guides/reasoning
- Kiro GitHub issues #8575 "In auto mode show model used while agent running" and #8903 "Show which model is used per response in Auto mode" — product-level demand for served-model disclosure (attack 3) — https://github.com/kirodotdev/Kiro/issues/8575
- LiteLLM, "Reasoning content" docs — cross-provider switching requires `drop_params`/`modify_params` to strip thinking fields, i.e. the gateway's translation layer is where within-rung swaps become lossy (attack 2) — https://docs.litellm.ai/docs/reasoning_content

### Verdict
**AMEND.** The separation is correct and every attack is a *leak* rather than a refutation — but the leaks are real, and two of them (cache, signatures) hit the cost objective and the handoff logic directly. Attacks 1–3 land and are answered by a stated contract (clauses 1–2) that turns the leaks into observable, typed events. Attack 4 lands and is answered by shared versioned rung membership (clause 3). This is the concrete Q7 boundary: ADRL owns rung choice and needs three things from the gateway — served identity, within-rung stability, and shared membership config.

## Amendments applied
- Added the three-part gateway contract (served identity reported; endpoint stability within turn/episode; shared versioned rung membership) and the reason (caches and signatures are model-specific).
- Added clauses 1–3.

## Follow-ups
- [ ] Confirm with the gateway team that LiteLLM returns the served model id and provider unrewritten (or in a header) on every response including failover; add a `tests/test_router_proxy.py` case where the gateway reports a different model than requested.
- [ ] Add `served_model`, `served_provider` to the decision/outcome schema (with CAS-006).
- [ ] Publish `rung-membership-v1.json` as shared config; CI on both repos validates alias lists against it.
- [ ] Measure in shadow how often the served model differs from the first model in the rung's list (within-rung failover rate) and the cache-cold cost it implies.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: gateway contract added (served identity, within-rung stability, shared membership) because caches and signatures are model-specific | "Capability-rung selection is separate from endpoint/provider selection inside a rung." |
