# ADRL-SAF-006 — Infeasible rungs removed before optimisation

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · unchanged |
| Maturity | D2 Tested, review recommends D2 Tested (correct; the feasibility estimator's tokenizer and budget assumptions need a measured error bound before D3) |
| Review verdict | APPROVE |
| Tenets | 2, 3 |
| Related decisions | SAF-001, SAF-005, RTG-002, RTG-004, CAS-006, FND-002, SEM-003 |
| Open questions | Q2, Q7 |

## Decision

Unhealthy or context-infeasible rungs are removed before optimisation.

## Context and rationale

"Infeasible" is a safety concern. A rung whose endpoint is unhealthy or whose context window cannot hold the request is removed from the candidate set before optimisation — not scored poorly and possibly still chosen. A low score can be outweighed by a large cost advantage; a removed rung cannot.

The review leaves the sentence unchanged and records where its implementation must be precise. Feasibility is an *estimate*: the harness's `count_tokens` numbers come from Anthropic's tokenizer, local models tokenize differently, and the budget must include the output reservation and any thinking budget, not only the input. Health is a *shared* fact: the gateway owns cooldowns and health checks (FND-002 as amended), so ADRL's feasibility gate should read the gateway's view rather than maintain a rival one. And feasibility is *per request*, not per turn — a continuation can outgrow the rung the turn started on, which is why SAF-001 as amended runs gates on every request and why CAS owns what happens next.

## Adversarial review (2026-09-02)

### Steelman
Hard constraints belong in the feasible set, not in the objective; every optimisation textbook and every scheduler agrees. Scoring an infeasible rung "poorly" invites a weighting bug to send a 150k-token pinned transcript to a 32k local model, which then truncates or errors and the trip-wire has to clean up. Removal is cheap, deterministic and auditable, and it is what makes RTG-002's "cheapest healthy rung likely to complete" a well-formed question.

### Attacks
1. **Wrong tokenizer.** `count_tokens` is Anthropic's estimate for Claude; the docs say the count is an estimate even for Claude. Local models (Llama, Qwen, Mistral families) have different vocabularies and can differ materially on code. A feasibility check that uses the Claude count for a local rung is wrong in an unknown direction. The estimator must use the rung's tokenizer or an error-bounded ratio that errs long.
2. **Budget is more than input.** Feasibility must reserve `max_tokens` for output and, on rungs that support it, the thinking budget; a request that fits its input into the window with 200 tokens to spare is not feasible. The decision says "context window cannot hold the request", which a reader may implement as input-only.
3. **Health has two owners.** LiteLLM runs cooldowns and health checks; if ADRL probes endpoints independently, the two views diverge under partial outage — ADRL removes a rung the gateway would have served, or keeps one the gateway has cooled down. Q7 territory; the decision should read gateway health rather than infer it (folded into FND-002).
4. **Feasibility changes within a turn.** A route chosen at the turn start can become infeasible on the tenth continuation. Removal "before optimisation" is per decision; SEM-003 says continuations do not re-decide. The gate must still run per request (SAF-001 as amended), and infeasibility mid-turn is a CAS escalation (unpinned) or SAF-005 block (pinned) — the decision does not need to say this, but its neighbours must.
5. **Empty feasible set.** If every rung is unhealthy or infeasible, "remove before optimisation" yields nothing to optimise. For unpinned sessions FND-004 (amended) falls open to the gateway; for pinned sessions SAF-004/005 surface. Answered by neighbours.
6. **Health flapping creates route flapping.** If a rung's health oscillates, feasibility oscillates, and sticky state (CAS-005) is the only thing preventing the route from flapping with it. Removal must not by itself trigger a re-decision on a healthy sticky route — only on the request that cannot be served.

### Evidence
- Anthropic, "Token counting" (Claude Platform docs) — "The token count is an estimate"; counts may include system-added tokens; bears on attack 1 — https://platform.claude.com/docs/en/build-with-claude/token-counting
- Anthropic, "Prompt caching" (Claude Platform docs) — minimum cacheable lengths differ by model (512–4,096 tokens), a reminder that token accounting is model-specific; bears on attack 1 — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- LiteLLM, "Fallbacks (Provider Failover)" — cooldowns remove a deployment from rotation after `allowed_fails` failures within a window for `cooldown_time` seconds; health-check-driven routing; per-model `num_retries`; the gateway already maintains a health view; bears on attack 3 — https://docs.litellm.ai/docs/proxy/reliability
- Anthropic, "Connect Claude Code to an LLM gateway" — `CLAUDE_CODE_MAX_OUTPUT_TOKENS` must be set below the gateway model's output limit, i.e. output budget is part of feasibility; bears on attack 2 — https://code.claude.com/docs/en/llm-gateway-connect
- No direct literature found on tokenizer-count divergence for code across model families; reasoning from first principles for attack 1 (measurement is a follow-up).

### Verdict
**APPROVE.** None of the attacks reaches the sentence. Attacks 1 and 2 are implementation precision for the estimator and are recorded as follow-ups with a measurable acceptance criterion. Attack 3 is resolved in FND-002's amendment. Attacks 4–6 are answered by SAF-001, SAF-004/005, FND-004 and CAS-005 as they stand or as amended. The decision is short, correct and load-bearing for RTG-002 and RTG-004; changing its text would add nothing.

## Amendments applied

None — decision stands as written.

## Follow-ups

- [ ] Measure tokenizer divergence: Claude `count_tokens` vs each local model's tokenizer on 200 real code-heavy requests from the corpus; set a per-rung safety ratio that errs long at p99.
- [ ] Feasibility formula in `router/policy.py`: `input_est × ratio + max_tokens + thinking_budget ≤ window − margin`; unit tests at the boundary.
- [ ] Read health from the gateway's cooldown/health API (FND-002 follow-up); fault test that ADRL and LiteLLM agree on a rung's health during an injected partial outage.
- [ ] Golden test: continuation outgrows a healthy sticky local route on an unpinned session → CAS escalation at action boundary, no re-decision on earlier requests.
- [ ] Golden test: rung health flaps while a sticky route is healthy → no route change.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Unhealthy or context-infeasible rungs are removed before optimisation." |
