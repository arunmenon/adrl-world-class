# ADRL-FND-002 — Semantic policy vs mechanical execution, rung-closed

| Field | Value |
|---|---|
| Bucket | FND — System Boundary and Principles |
| Status | Accepted · amended 2026-09-02 · amended 2026-09-03 (proposed amendment, pending disposition) |
| Maturity | D2 Tested, review recommends D2 Tested (the split is implemented; the rung-closed fallback contract with the gateway is not yet tested and must be before D3) |
| Review verdict | AMEND |
| Tenets | 7 |
| Related decisions | FND-001, RTG-008, CAS-006, SAF-002, SAF-003, SAF-004, SAF-006 |
| Open questions | Q1, Q7 |

## W7.0a scoped application and evidence, 2026-09-08

The composition root adds a fail-closed exploration compatibility check between the configured learning contract and current live feature semantics. A mismatch raises ConfigError before loading an exploration artifact. Ordinary routing without exploration is unchanged at composition level. This does not change gateway configuration, model membership, protocol support or rollout authority.

[Report](../../reports/adrl-routing-correction-2026-09-08.md), [implementation guide](../../../adrl-core/docs/routing-features.md), [code diff](../../reports/research/routing-correction-2026-09-08/implementation.patch), [tests](../../../adrl-core/tests/unit/routing/test_mixed_intent.py), [all route changes](../../reports/research/routing-correction-2026-09-08/route-changes-final.md), [checks](../../reports/research/routing-correction-2026-09-08/checks-final/manifest.json), [validation](../../reports/research/routing-correction-2026-09-08/validation.json). Final validation: 159 focused tests; all eleven checks; 911 passed, eight engine cases skipped; 322 stable inputs. One initial candidate failed an existing sticky-cascade test and over-routed the flag case; both were repaired without changing the original suite. Decision text/status/formal maturity stay unchanged; named offline behavior only, no organic qualification or full-decision promotion.

## Decision

ADRL owns semantic policy; LiteLLM and providers own mechanical model execution, subject to a deployment-set-closed execution contract: no gateway retry, fallback or context-window fallback may serve a request from a deployment outside the permitted deployment set ADRL computed for it (TRU-002), and the signed deployment inventory (deployment id, rung, provider, api_base, trust zone, geography, data-use profile) is a shared, versioned configuration that both sides read.

1. "Mechanical execution" includes endpoint choice within a rung, provider choice within a rung, retry, cooldown, transport, and health signalling.
2. Any gateway feature that changes the *model class* in response to request content or size (LiteLLM `context_window_fallbacks`, `content_policy_fallbacks`, cross-rung `fallbacks`) is semantic and is disabled or constrained to the same rung for ADRL-originated traffic; for privacy-pinned traffic the gateway fallback set is the local rung only.
3. Where the gateway also offers content controls that overlap SAF (secret redaction, PII masking), ADRL's gate is authoritative for the routing decision and the gateway's control is defence in depth, never a substitute; the two rulesets are diffed and reconciled on a schedule.
4. The monotone object the gates tighten and the gateway honours is the permitted deployment set, never a rung label; a rung is the economic tier of a deployment (RTG-001). A `local` deployment is loopback or unix-socket by inventory rule, and the served-deployment receipt (TRU-002 clause 4) is the detective backstop that CAS-006 records.

## Context and rationale

ADRL says "this is hard", not "use this model". The reason for the split is rate-of-change: endpoints, model IDs, quotas and providers churn constantly, while the semantic question — how hard is this piece of work — is stable. Coupling them would make every model deprecation a routing-logic change.

The amendment closes a hole the original text left open. LiteLLM is not a passive executor: its documented reliability features include context-window fallbacks (re-route to a larger model when the input does not fit) and content-policy fallbacks (re-route to a different provider when one rejects the content). Both are *semantic* decisions in ADRL's own vocabulary, and both can cross a rung boundary. Left unconstrained, a request ADRL sent to the local rung because of a privacy pin could be silently served by a cloud model because the local context window overflowed — which violates SAF-002 and SAF-004 without either side noticing, and records the wrong rung unless CAS-006 catches it. The boundary is therefore not "ADRL semantic, gateway mechanical" but "ADRL semantic, gateway mechanical *within the rung*".

## Adversarial review (2026-09-02)

### Steelman
This is the load-bearing split and it is the right one: the gateway team (gateway) already owns endpoint health, retries and spend controls for every consumer at the company, and duplicating that in ADRL would produce two sources of truth for model availability. Capability rungs are a stable abstraction; concrete model IDs are not. Every other bucket can be written against "rung" without knowing a single endpoint name, which is exactly what has let the register stay coherent through model churn.

### Attacks
1. **LiteLLM makes semantic decisions too.** The LiteLLM reliability docs describe context-window fallbacks that "map context window error messages across providers" and re-route to a larger model, and content-policy fallbacks that re-route on provider refusals. If a local-rung request overflows the local model's context and the gateway's fallback group includes a cloud model, the pin in SAF-002 is broken by the *mechanical* layer. The decision's split is only safe if fallback groups are rung-closed, and nothing in the text says so.
2. **The rung→endpoint mapping lives in two places.** ADRL's `router/backends.py` maps roles to endpoints; LiteLLM's config maps model groups to deployments. If they drift (a new deployment added to the `local` group that is actually a cloud-hosted small model, or a `frontier` alias repointed to a cheaper model), ADRL's semantic decision is executed against a different reality and CAS-006's "record what served" is the only detector. That is a detective control for what should be a preventive one.
3. **Overlapping content controls create two answers.** LiteLLM Enterprise ships secret detection (Yelp `detect-secrets`, `pre_call`, redact) and Presidio PII masking. If the enterprise gateway enables them, a prompt may be *redacted* by the gateway after ADRL *pinned* on the same content, or pinned by ADRL on a pattern the gateway does not flag. Q7 asks where the line is; this decision should draw it for content controls, not just for retries.
4. **Health is a shared signal with two consumers.** SAF-006 removes unhealthy rungs before optimisation, but health is a gateway-owned mechanical fact (cooldowns, health checks). If ADRL maintains its own health view it will disagree with LiteLLM's cooldown state in exactly the moments that matter (partial outages). The decision should say health is read from the gateway, not inferred by ADRL.
5. **Q1 pressure: vendors are moving the semantic layer into the gateway.** Bedrock Intelligent Prompt Routing decides per request on "predicted response quality" across a model family. If the gateway grows an internal quality router, "semantic policy" is no longer exclusively ADRL's. The decision should state which semantic decisions ADRL will never delegate (privacy pin, rung ceiling, stickiness) even if cloud-to-cloud choice inside a rung is delegated.

### Evidence
- LiteLLM, "Fallbacks (Provider Failover)" (docs) — documents standard, content-policy and context-window fallbacks; context-window fallbacks re-route on input size, i.e. a content-dependent model change; bears on attacks 1, 2 — https://docs.litellm.ai/docs/proxy/reliability
- LiteLLM, "Secret Detection/Redaction (Enterprise-only)" (docs) — `detect-secrets`-based redaction in `pre_call` mode with 100+ plugins; bears on attack 3 — https://docs.litellm.ai/docs/proxy/guardrails/secret_detection
- LiteLLM, "PII, PHI Masking - Presidio" (docs; title from search) — gateway-side PII masking exists as a guardrail; bears on attack 3 — https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2
- AWS, "Understanding intelligent prompt routing in Amazon Bedrock" (docs) — per-request routing on predicted quality within a model family, English-optimised, no customisation on application data; bears on attack 5 and Q1 — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- Anthropic, "Gateway protocol reference" (Claude Code docs) — the gateway may consume `x-claude-code-*` headers for routing/attribution but must forward `anthropic-*` headers; shows the vendor already expects the gateway layer to make some routing decisions; bears on attack 4 — https://code.claude.com/docs/en/llm-gateway-protocol

### Verdict
**AMEND.** Attacks 1 and 3 land and are the reason for the amendment: the split is correct but incomplete, because the gateway's own fallback machinery can cross rung boundaries and its own content guardrails can disagree with SAF. Attack 2 is answered by making rung membership a shared versioned config rather than two hand-maintained maps. Attack 4 is folded into sub-clause 1 (health is gateway-owned and read, not inferred). Attack 5 is a Q1 matter; the amendment names the non-delegable decisions in the rationale without pre-empting Q1.

## Adversarial review (2026-09-03)

### Steelman
The 2026-09-02 amendment closed the gateway-fallback hole at rung granularity, which is the granularity the gateway's configuration speaks. Keeping the contract at that level is simple and the generator already enforces it.

### Attacks
1. **A rung is a name, not a place.** The first implementation showed that a `local` model group whose `api_base` pointed at an external host passed every rung-closure check. "Rung-closed" cannot express "stays on this machine" or "stays in this geography", which are the properties SAF-002, SAF-004 and SAF-008 need from this contract.
2. **Residency has no object to bind to.** SAF-008 asked residency to be "enforced through FND-002's rung-closed contract"; a rung has no geography, so the implementation carried residency as a field nothing read.
3. **Served identity at rung granularity hides substitution.** CAS-006 records the served rung and model; without the deployment id, a within-rung move from an in-region to a global endpoint is invisible to the egress ledger.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P0-1, verified against `adrl-core` (configuration checks pass with a remote local group; residency unread).
- ADRL-TRU-002 (proposed) for the inventory schema and receipt.

### Verdict
**AMEND (proposed).** The split stands; the closure object changes from rung to permitted deployment set. Pending disposition of TRU-002.

## Amendments applied

- Appended "subject to a rung-closed execution contract" and the definition that no gateway retry/fallback/context-window fallback may leave the selected rung.
- Added sub-clause 1 enumerating what "mechanical execution" includes (health explicitly gateway-owned).
- Added sub-clause 2 naming the LiteLLM features that are semantic and constraining them to the rung; local-only fallback set for pinned traffic.
- Added sub-clause 3 assigning authority for overlapping content controls (ADRL gate authoritative; gateway guardrail defence in depth; ruleset diff).
- 2026-09-03: "rung-closed" replaced by "deployment-set-closed"; the shared configuration is the signed deployment inventory of TRU-002; clause 4 added naming the permitted deployment set as the monotone object and requiring local deployments to be loopback.

## Follow-ups

- [ ] Fault test: local-rung request that exceeds the local context window with a LiteLLM `context_window_fallbacks` group containing a cloud model → assert the request is *not* served by cloud when pinned, and that CAS-006 records the served rung when unpinned.
- [ ] Config contract: a single `rungs.yaml` (or equivalent) consumed by both `router/backends.py` and the LiteLLM config generator, with a CI check that every LiteLLM model group maps to exactly one rung and no fallback group spans rungs.
- [ ] Reconciliation job: diff ADRL's secret-detection ruleset against the gateway's `detect_secrets_config`; report patterns present in one but not the other.
- [ ] Decide (Q7) and record: ADRL reads health from the gateway's health/cooldown API rather than probing endpoints itself.
- [ ] Q1 note: write the non-delegable list (privacy pin, rung ceiling, stickiness, episode boundary) as an appendix so a future "use Bedrock IPR inside the cloud rungs" decision has a fixed boundary.
- [ ] 2026-09-03: regenerate the gateway configuration from `deployment-inventory-v1`; CI rejects a `local` entry that is not loopback or unix-socket and any fallback group that is not closed under the per-request permitted set.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded W7.0a scoped feature/compatibility application and before/after evidence | Prior decision text and dated evidence retained; features-v1 used first-match classification and exploration lacked this explicit live-feature/contract check |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: rung-closed execution contract; gateway fallbacks constrained to rung; content-control authority assigned | "ADRL owns semantic policy; LiteLLM and providers own mechanical model execution." |
| 2026-09-03 | Amended (proposed, external review): closure object is the permitted deployment set, not the rung | "ADRL owns semantic policy; LiteLLM and providers own mechanical model execution, subject to a rung-closed execution contract: no gateway retry, fallback or context-window fallback may serve a request from an endpoint outside the capability rung ADRL selected, and rung membership of every endpoint is a shared, versioned configuration that both sides read." |
