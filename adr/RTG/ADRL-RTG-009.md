# ADRL-RTG-009 — Session-marginal, cache-aware cost accounting

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Proposed 2026-09-02 (new, from adversarial review) |
| Maturity | D0 Design, review recommends D0 Design (partial telemetry exists in `telemetry.py`/`outcomes.py`; the accounting rule itself is not implemented) |
| Review verdict | PROPOSED (new) |
| Tenets | 1, 3, 8 |
| Related decisions | RTG-002, RTG-005, RTG-007, RTG-008, CAS-004, CAS-005, CAS-006, SEM-003, FND-003, MEM-001, EVL-005 |
| Open questions | Q4, Q6 |

## Decision

Routing cost is accounted per session continuation, not per HTTP request: the cost of a candidate rung for a turn is the expected cost of the remainder of the episode on that rung given its current prompt-cache state, plus the cache-rebuild cost if the rung differs from the one currently serving, plus the expected cost of cascade on failure; a rung switch is never scored at list price alone.

1. Inputs: provider-reported cache usage (`cache_read_input_tokens`, `cache_creation_input_tokens` on Anthropic; `cached_tokens` on OpenAI; `gen_ai.usage.cache_*` via OpenTelemetry) attached to every outcome row; per-rung price vectors (base input, cache write, cache read, output) versioned in config; cache TTL per provider (Anthropic 5 min default / 1 h option; OpenAI 5–10 min in-memory, longer retention options) so a stale cache is not assumed warm.
2. Switch cost: when the candidate rung ≠ the served rung (CAS-006), the transcript is charged at cache-write price on the candidate, and the served rung's cache is treated as forfeited; when a within-rung model change is reported by the gateway (RTG-008), the same charge applies.
3. Expected-remaining-episode length is a named estimator (initially: empirical distribution of continuations per turn from the shadow corpus, conditioned on request kind and band); its version is recorded on the decision row.
4. Reporting: every cost figure in EVL scorecards and readiness reports is labelled "after cache effects" or "list price"; comparisons across the two are prohibited (this codifies the Evidence page's "cost figures are upper bounds and asymmetric" non-claim).

## Context and rationale

Every decision in RTG that mentions cost — RTG-002 ("cheapest"), RTG-005 ("cost"), RTG-007 ("marginal utility") — currently leaves the unit unstated, and the register's own open item says "prompt-cache economics need to be inside the objective, not reported alongside it." Phase 0's most robust finding was that the prompt-cache hit ratio on real traffic is very high and that a per-request router would destroy it. Provider pricing makes the asymmetry stark: a cached read is 0.1× (0.025× on the newest Anthropic models) of base input, a write is 1.25–2×. On a 100k-token coding transcript, staying on the current rung costs roughly a tenth to a fortieth of what a switch costs *for the input alone*, before any quality effect. Two shipping coding-agent routers — GitHub Copilot's auto selection and Not Diamond Code — have independently reached the same design: route at cache boundaries and optimise session cost rather than next-request cost. This ADR gives ADRL one definition of cost that RTG-002/005/007 can share, that CAS-005 stickiness can be justified against numerically, and that EVL can compare policies on without the asymmetry the Evidence page warns about.

## Adversarial review (2026-09-02)

### Steelman
This is the cost model the tenets already imply (route turns, not requests; continuations inherit routes) written down as arithmetic. It is directly measurable from provider usage fields, requires no learned component, and converts the "never switch mid-turn" stance from a rule into a consequence of the objective. It also prevents a future learned router from "discovering" per-turn cost savings that are per-session losses.

### Attacks
1. **Cache state is not observable before the request is sent.** ADRL knows only what the *last* response reported; TTL expiry (5 minutes idle on Anthropic by default) between a developer's turns means the "warm" assumption can be wrong after a coffee break. Clause 1 requires TTL-aware staleness; the estimator should treat cache as warm only within TTL of the last served request and otherwise price a write.
2. **Episode length is unknown at decision time.** Charging a switch against "remaining episode" needs a forecast; if the episode ends on this turn, the switch was nearly free. Clause 3 makes the forecast a named, versioned estimator so its error is measurable; a bad estimator biases toward stickiness, which is the conservative direction for cache cost but the expensive direction if frontier is sticky (CAS-005).
3. **It could become a reason never to escalate.** A large warm *local* transcript is free and a large warm cheap-cloud transcript is nearly free, so a strict session-cost objective would resist escalation exactly when the transcript is largest — which is when the hard problem is likely. The objective must be traded against verified quality (RTG-005), and trip-wire-triggered escalation (CAS-001) must be exempt from the switch charge: the charge informs *routing*, not *recovery*.
4. **Local has no cache-pricing analogue, so its cost is mis-modelled as zero.** Local inference has real wall-clock and hardware cost, and a local prefill over 100k tokens on a laptop-class engine is slow enough to be a latency term. Clause 1's price vector must carry a non-zero local cost (at minimum a latency-equivalent) or local looks infinitely sticky.

### Evidence
- Anthropic, "Prompt caching" — 5-min default TTL, 1-h option; write 1.25×/2×, read 0.1× (0.025× on Claude Fable 5.1 / Mythos 5.1); usage fields; exact-prefix matching (clauses 1–2, attack 1) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- OpenAI, "Prompt caching" — reads 0.1× on GPT-5.6+; on GPT-5.6+ a cached prefix "remains eligible for reuse for 30 minutes after its most recent write or reuse"; earlier models with in-memory retention keep entries "around 5 to 10 minutes of inactivity, up to one hour", with a 24h retention option; per-model caches; `usage.input_tokens_details.cached_tokens` (clauses 1–2) — https://developers.openai.com/api/docs/guides/prompt-caching
- OpenTelemetry GenAI conventions — `gen_ai.usage.cache_read.input_tokens`, `gen_ai.usage.cache_creation.input_tokens` (clause 1) — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (registry page now marked "moved to the OpenTelemetry GenAI semantic conventions repository", https://github.com/open-telemetry/semantic-conventions-genai)
- GitHub Docs, "About Copilot auto model selection" — "Routing occurs along natural cache boundaries... Switching models mid-session has shown increased cost without ample improvements in quality" (rationale) — https://docs.github.com/copilot/concepts/auto-model-selection
- Not Diamond, "Not Diamond Code" (2026) — session-level objective; will "stay on a more expensive model to preserve a warm cache" or "break cache to upgrade" depending on context utilisation (rationale, attack 3) — https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- OpenRouter, "Auto Router" docs — implements "Session Stickiness" preferring the model a conversation "landed on", but re-ranks per prompt; an example of the per-request design this ADR rejects — https://openrouter.ai/docs/guides/routing/routers/auto-router
- No peer-reviewed study found that models LLM-routing cost under provider prompt caching; the 2026 routing survey lists cost accounting with caching as absent from the literature. Reasoning from vendor pricing and the two production routers above.

### Verdict
**PROPOSED (new).** The bucket has three decisions that depend on a cost unit none of them defines, and the register's own open item names the gap. Attacks 1–4 are design constraints, each answered by a clause; none refutes the need. Recommend acceptance at D0 with RTG-002/005/007 amended to reference it (done in this review).

## Amendments applied
- New decision; no prior text.

## Follow-ups
- [ ] Implement cache-usage ingestion from gateway responses into `outcomes.py`; publish per-rung cache hit ratio and effective input price per session on the shadow scorecard.
- [ ] Implement the switch-cost calculation in `policy.py` behind a flag; shadow-log the rung ordering with and without it and report how often they differ.
- [ ] Build the episode-length estimator from the shadow corpus; record its version on decision rows.
- [ ] Add a non-zero local cost vector (latency-equivalent) to the price config.
- [ ] Golden test: trip-wire escalation (CAS-001) is not blocked or delayed by the switch charge.
- [ ] Relabel every cost figure in `reports/` and the readiness scorecard as "after cache effects" or "list price".

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
