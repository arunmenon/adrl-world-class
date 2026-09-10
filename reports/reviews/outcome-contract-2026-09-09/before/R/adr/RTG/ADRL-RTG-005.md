# ADRL-RTG-005 — Objective: verified quality, retry, latency, session cost

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D2 Tested for the decision as a *routing criterion*: telemetry collection for the four terms is in shadow, but the objective itself has never been evaluated against a baseline on real traffic (one verified task; 34/300 decisions), so "shadow" over-states what has been observed |
| Review verdict | AMEND |
| Tenets | 3, 8 |
| Related decisions | RTG-002, RTG-007, RTG-009 (proposed), MEM-002, MEM-003, LRN-001, EVL-005 |
| Open questions | Q4, Q6 |

## Decision

Runtime optimisation uses expected verified quality, retry risk, latency and expected session-marginal cost — with prompt-cache state inside the cost term, not reported alongside it — rather than difficulty alone; each term is a named, versioned measurement with a published data source, and a term whose measurement is absent for a turn is treated as unknown, not as zero.

1. The cost term is defined by RTG-009: expected remaining-session cost given the current cache state of each candidate rung, including the cache-rebuild cost of any rung switch and the expected cost of cascade on failure.
2. The quality term is "expected verified quality" only where a deterministic verifier (MEM-003) exists for the task class; elsewhere it is a proxy label and is marked as such (LRN-001), and the policy's weight on it is reduced accordingly.
3. Weights between the terms are versioned policy constants until RTG-007 replaces them with a learned utility; changing a weight is a policy version change recorded on decision rows.
4. Latency is weighted by interaction mode: interactive user turns weight latency highly; background subagent turns (SEM-006) may weight it near zero.

## Context and rationale

Difficulty is not the objective; it is one input. A hard task on a cheap rung fails, retries, and costs more than going straight to frontier. An easy task in a huge, already-cached session may be cheaper to keep where it is than to move. Policy weighs expected verified quality, retry risk, latency and cost. Cache: cheapest-per-turn can be more expensive per session, because switching cloud models breaks prompt-cache reuse exactly when the transcript is largest. The original register said this in the rationale and left it out of the decision — the register's own open item ("prompt-cache economics need to be inside the objective, not reported alongside it") is now applied. Two commercial coding-agent routers have converged on the same conclusion: GitHub Copilot routes only at cache boundaries because mid-session switching raised cost without quality gains, and Not Diamond optimises "total session quality and cost outcomes rather than the quality and cost of the next request alone".

## Adversarial review (2026-09-02)

### Steelman
A difficulty classifier answers the wrong question; the right question is which rung minimises expected total cost at acceptable quality, and that depends on retry probability, wait time and the cache-state of a long transcript. Stating the four terms explicitly prevents a naive per-turn cost minimiser from being built. Telemetry for all four terms already exists in shadow.

### Attacks
1. **The single most important term — cache — is missing from the decision sentence.** Anthropic prices cache reads at 0.1× (0.025× on newest models) and writes at 1.25–2×; on a 100k-token transcript a rung switch costs roughly 12–20× the marginal cost of staying. The register's own open item concedes this; two production coding routers (Copilot, Not Diamond) have built their objective around it. A decision that says "cost" without saying "session cost with cache" will be implemented as list-price-per-turn.
2. **"Expected verified quality" is not measurable on today's corpus.** Only one task has strong test-based verification; automatic verification is not connected to every eligible task. An objective term with no data collapses to zero weight or to a proxy label — and LRN-001 says proxy labels are "abundant and quietly wrong". The text must say what happens when the term is absent.
3. **Four terms with no weights is not an objective; it is a list.** Two engineers can implement RTG-005 and get opposite rung orderings. Without versioned weights on decision rows, MEM cannot attribute a routing change to a policy change (tenet 8), and EVL cannot compare policies.
4. **Latency is not one number for coding-agent traffic.** Phase 0 found subagent work "effectively free at the margin" and background subagents run concurrently with the parent. A latency term tuned for a developer waiting at the prompt is wrong for a background `Explore` agent and vice versa; the objective must be mode-aware or it optimises the wrong thing on ~half the traffic.
5. **The D3 claim conflates measuring inputs with evaluating the objective.** `outcomes.py`/`telemetry.py` collecting retries and latency in shadow is D3 for *telemetry*. The objective — a way of ordering rungs — has not been compared against always-local / always-frontier / current-heuristic baselines on organic traffic (Q6). EVL-005 forbids counting simulator runs. The register even says "partial target".

### Evidence
- Anthropic, "Prompt caching" — cache read 0.1× base / 0.025× on Claude Fable 5.1 and Mythos 5.1; write 1.25× (5-min) / 2× (1-hour); `cache_read_input_tokens` reported in usage (attack 1) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- OpenAI, "Prompt caching" — reads 0.1× on GPT-5.6+; "a different model can use different weights and caching behavior", i.e. caches do not survive a model change (attack 1) — https://developers.openai.com/api/docs/guides/prompt-caching
- GitHub Docs, "About Copilot auto model selection" — "Routing occurs along natural cache boundaries to avoid additional cache related costs. Switching models mid-session has shown increased cost without ample improvements in quality." (attack 1) — https://docs.github.com/copilot/concepts/auto-model-selection
- Not Diamond, "Not Diamond Code" (vendor blog 2026) — optimises "total session quality and cost outcomes rather than the quality and cost of the next request alone"; may "stay on a more expensive model to preserve a warm cache" (attack 1) — https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- OpenTelemetry GenAI semantic conventions — `gen_ai.usage.cache_read.input_tokens` / `gen_ai.usage.cache_creation.input_tokens` are standard attributes, so the cost term is observable through the gateway (attack 1, follow-up) — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/ (registry page now marked "moved to the OpenTelemetry GenAI semantic conventions repository", https://github.com/open-telemetry/semantic-conventions-genai)
- Dekoninck et al., "A Unified Approach to Routing and Cascading" (arXiv 2024) — routing quality is "critical[ly]" dependent on ex-ante estimate noise; an unverified quality term is exactly high ex-ante noise (attack 2) — https://arxiv.org/abs/2410.10347
- No academic study found that models per-session cost of LLM routing under provider prompt caching; the only sources are vendor pricing pages and the two commercial routers above. Stated explicitly rather than inferred.

### Verdict
**AMEND.** Attack 1 lands decisively and is conceded by the register's own open item; the fix is to put the cache-aware session cost in the decision and delegate its definition to a dedicated ADR (RTG-009) because it is load-bearing for RTG-002, RTG-005, RTG-007 and CAS-005 alike. Attacks 2 and 3 land: the objective must say what happens when a term is unmeasured and must carry versioned weights or it is not comparable across policy versions. Attack 4 lands and is cheap to fix (clause 4). Attack 5 lands on maturity: the inputs are shadowed, the objective is not, and the register should say D2 for the decision until a baseline comparison on organic traffic exists. The principle — optimise utility, not difficulty — is right and stands.

## Amendments applied
- Replaced "cost" with "expected session-marginal cost — with prompt-cache state inside the cost term, not reported alongside it".
- Added "each term is a named, versioned measurement... unknown, not zero".
- Added clauses 1–4 (cost per RTG-009; verified vs proxy quality; versioned weights; mode-aware latency).
- Maturity recommendation lowered to D2 for the objective as a routing criterion.

## Follow-ups
- [ ] Write ADRL-RTG-009 (proposed in this review) and reference it from `policy.py`.
- [ ] Ingest `cache_read_input_tokens` / `cache_creation_input_tokens` (Anthropic) and `cached_tokens` (OpenAI) from gateway responses into `telemetry.py`; report per-session cache hit ratio by rung on the shadow scorecard.
- [ ] Record `objective_version` and the weight vector on every decision row.
- [ ] Baseline comparison on organic shadow traffic: RTG-005 ordering vs always-local / always-frontier / RTG-002-heuristic, measured after cache effects (Q6) — this is the gate to re-claim D3.
- [ ] Add `interaction_mode` (interactive / background-subagent / utility) as a feature and weight latency by it.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: cache-aware session cost placed inside the objective; terms named/versioned; unmeasured terms are unknown; latency mode-aware; maturity recommendation D2 | "Runtime optimisation uses expected verified quality, retry risk, latency and cost rather than difficulty alone." |
