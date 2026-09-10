# ADRL-CAS-006 — Record the served model, not only the served rung

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (served-rung correction is tested in `tests/test_router_proxy.py`; served-model capture and the state-loss case are untested and are added as gates for D3) |
| Review verdict | AMEND |
| Tenets | 6, 7, 8 |
| Related decisions | CAS-002, CAS-004, CAS-005, RTG-008, RTG-009, OPS-001, OPS-006, MEM-001, SEM-002 |
| Open questions | Q7 |

## Decision

Sticky state records the rung that actually served the response, including transport fallback — and, alongside it, the served model and provider identity as reported by the gateway, and the confidence of that record — because prompt caches and reasoning signatures follow the model, not the rung.

1. Fields: `served_rung`, `served_model`, `served_provider`, `served_source` ∈ {gateway_reported, proxy_observed, assumed_intended} on both sticky state (`router/state.py`) and the outcome row (MEM-001). `assumed_intended` is set when the gateway did not report identity; a continuation routed on an `assumed_intended` record is flagged so the outcome is `unverifiable` for cause typing if it fails (CAS-002).
2. A within-rung change of `served_model` between consecutive requests of an episode is recorded as an infrastructure event (CAS-002 clause 2), triggers the CAS-004 provider-pair rule for the next continuation if the model family changed, and is charged as a cache-cold switch in RTG-009.
3. If sticky state is unavailable (process restart; OPS-001 single-process dict), the next request in an episode is routed as a fresh decision but with `state_loss=true` on the decision row, and the outcome is excluded from stickiness evidence.

## Context and rationale

Record what happened, not what you asked for. The router may choose "cheap cloud"; the transport layer may fail over elsewhere. If sticky state stores intent, the next continuation is routed at a rung that is not actually serving. This is the runtime twin of OPS-006. The amendment extends "what happened" from rung to model, because the two costliest consequences of a substitution — a cold prompt cache and an unreadable reasoning signature — are model-level facts that a rung-level record cannot see. It also names where the record comes from: the OpenTelemetry GenAI conventions already distinguish `gen_ai.request.model` from `gen_ai.response.model` ("the name of the model that generated the response"), and gateways can rewrite the latter to the requested alias; a record that does not know its own provenance cannot be trusted by CAS-002's typer.

## Adversarial review (2026-09-02)

### Steelman
Intent/served divergence is a classic distributed-systems bug and this decision closes it at the only place that can observe both (the proxy). It is tested. Recording served state also makes every ledger row cause-clean about *which* capability produced the outcome (tenet 8).

### Attacks
1. **Rung is the wrong granularity for the two things stickiness protects.** Stickiness exists to preserve the cache and avoid handoffs (CAS-005). Both are per-model: Anthropic's cache requires an identical prefix on the same request path; OpenAI's caches are per-model; thinking signatures are model-family-specific. A gateway that fails over from one frontier model to another has kept the *rung* and lost both the cache and the signature. A rung-only record tells the next continuation "nothing changed" when everything that matters did.
2. **The proxy may not be able to observe the served model.** LiteLLM and other gateways commonly echo the requested alias in the response `model` field. Bedrock's Intelligent Prompt Routing "dynamically chooses the model" per request; Kiro's users had to file issues (#8575, #8903) to get the served model shown at all. If the gateway does not report, CAS-006 records intent while believing it records fact — the exact failure it exists to prevent — with no marker that it did so. Provenance of the record (clause 1) is therefore part of the decision.
3. **Single-process state loses the served record on restart.** Session-to-route tracking is a Python dict. After a restart mid-episode the router has no sticky state and re-decides from scratch, possibly *lowering* the rung without a SEM-005 boundary — a silent violation of CAS-005 that the current text does not acknowledge. Clause 3 makes it visible and excludes it from evidence rather than pretending it cannot happen.
4. **"Transport fallback" is narrower than what actually substitutes.** Provider-level routers (Bedrock IPR, OpenRouter auto) substitute for *quality/cost* reasons, not only transport failure. If the enterprise gateway ever enables such a feature inside a rung alias, the substitution is neither a failure nor a fallback but still changes the served model. The record must be keyed on reported identity, not on an inferred "fallback happened" flag.

### Evidence
- OpenTelemetry GenAI semantic conventions — `gen_ai.request.model` "The name of the GenAI model a request is being made to" vs `gen_ai.response.model` "The name of the model that generated the response"; `gen_ai.provider.name` (attacks 1, 2; clause 1) — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (registry page now marked "moved to the OpenTelemetry GenAI semantic conventions repository", https://github.com/open-telemetry/semantic-conventions-genai)
- Anthropic, "Thinking" — for Fable 5.1 / Mythos 5.1 preserved thinking blocks the signature covers system, tools and preceding messages; earlier models "can't read their blocks, the API drops them" (attack 1) — https://platform.claude.com/docs/en/build-with-claude/thinking
- OpenAI, "Prompt caching" — "A different model can use different weights and caching behavior" (attack 1) — https://developers.openai.com/api/docs/guides/prompt-caching
- AWS, "Understanding intelligent prompt routing in Amazon Bedrock" — "For each incoming request, the system analyzes the prompt... dynamically chooses the model" (attack 4) — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- Kiro GitHub issues #8575 / #8903 — requests to "show model used" in auto mode; evidence that served-model disclosure is not a given in auto-routing products (attack 2) — https://github.com/kirodotdev/Kiro/issues/8575
- OpenRouter, "Auto Router" — "can pick a different model on every turn" with session stickiness only while the model remains a top candidate (attack 4) — https://openrouter.ai/docs/guides/routing/routers/auto-router
- ADRL context pack, code-reality — "Session-to-route tracking is held in a Python dict (single-process)" (attack 3).

### Verdict
**AMEND.** Attack 1 lands: the decision records the right *kind* of thing at the wrong granularity for the properties stickiness protects. Attack 2 lands and is the most important addition — a served record without provenance is intent wearing a fact's label. Attack 3 lands and is answered by making state loss explicit rather than silent. Attack 4 lands and is answered by keying on reported identity. The decision's principle is exactly right; it needed one more field and a provenance marker.

## Amendments applied
- Added served model and provider identity and the record's provenance to the decision sentence.
- Added clause 1 (fields and `served_source` semantics), clause 2 (within-rung model change as typed event with CAS-004/RTG-009 consequences), clause 3 (state-loss marker).

## Follow-ups
- [ ] Extend `tests/test_router_proxy.py`: gateway response reports a different model than requested within the same rung → `served_model` updated, `served_source=gateway_reported`, infrastructure event recorded, next continuation applies CAS-004 pair rule if family changed.
- [ ] Test: gateway response omits model identity → `served_source=assumed_intended`; a subsequent failure is typed `unverifiable`.
- [ ] Test: simulate process restart mid-episode → `state_loss=true` on next decision; row excluded from stickiness metrics.
- [ ] Agree with the gateway team (Q7/RTG-008) the response field or header carrying served model/provider unrewritten.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-09 | <!-- taxonomy-sync:claude-adapter:ADRL-CAS-006 --> [Offline candidate](../../reports/reviews/claude-adapter-2026-09-09/report.md); Direct experiment observation ignores gateway-specific identity headers and preserves the actual provider model source. Host is the fixed configured HTTPS destination; deployment, geography and trust receipt fields stay unknown. Intended deployment is separate. Any response not reporting the target model, including upstream errors or missing identity, stops further dispatch. No fabricated confirmed receipt. | Prior decision wording preserved; no grade change |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: served model/provider and record provenance added; within-rung substitution typed; state loss made explicit | "Sticky state records the rung that actually served the response, including transport fallback." |


## Claude initial-choice candidate, 2026-09-09

<!-- taxonomy-sync:claude-adapter:ADRL-CAS-006 --> Direct experiment observation ignores gateway-specific identity headers and preserves the actual provider model source. Host is the fixed configured HTTPS destination; deployment, geography and trust receipt fields stay unknown. Intended deployment is separate. Any response not reporting the target model, including upstream errors or missing identity, stops further dispatch. No fabricated confirmed receipt. [Evidence and limits](../../reports/reviews/claude-adapter-2026-09-09/report.md). Formal grades and status unchanged.
