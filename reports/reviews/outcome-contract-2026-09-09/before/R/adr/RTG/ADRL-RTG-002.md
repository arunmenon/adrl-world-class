# ADRL-RTG-002 — Cheapest rung likely to complete, defined

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (the ordering rule is tested; the completion-probability inputs it consumes are heuristic and unverified, which clause 1 now makes explicit) |
| Review verdict | AMEND |
| Tenets | 2, 3 |
| Related decisions | RTG-001, RTG-004, RTG-005, RTG-009 (proposed), SAF-006, CAS-005, MEM-004 |
| Open questions | Q2, Q4, Q6 |

## Current implementation evidence, 2026-09-08: routing diagnostic

The unchanged Router made 240 decisions across 24 synthetic task prompts, five conditions and two repeats. Selected tiers stayed within the supplied permitted sets. Task/context/failure inputs changed choices. These are component decisions, not model completions, calibrated success estimates or measured routing benefit. Mixed-intent under-classification needs correction in the feature/rule path.

[Report](../../reports/adrl-routing-in-action-2026-09-08.md) · [raw traces](../../reports/research/routing-demonstration-2026-09-08/results.json) · [next correction packet](../../reports/waves/routing-decision-quality.md). The focused 135 routing/cascade/learning tests pass; all 316 runtime inputs match the previous full build. Architectural status, maturity and decision wording are unchanged.

## Lab A.1 implementation evidence, 2026-09-08

The real Router now has a repeatable full-Messages-path diagnostic: a typo routes local, the same prompt with larger context routes frontier, and two preserved mixed-intent prompts still route local. Ten distinct decision IDs are attributable through dispatch and receipt events. Existing features, heuristic estimator, costs, thresholds and routing policy are unchanged. No calibration, task-success or economic benefit is established. Mixed-intent correction remains the next proposed behavioral change.

[Report](../../reports/adrl-lab-first-run-2026-09-08.md), [runner](../../../adrl-core/tools/run_routing_lab.py), [tests](../../../adrl-core/tests/unit/test_routing_lab.py), [run evidence](../../reports/research/routing-lab-2026-09-08/run-2/results.json), [engineering checks](../../reports/research/routing-lab-2026-09-08/engineering-checks.json), [validation](../../reports/research/routing-lab-2026-09-08/validation.json), [follow-on scope](../../reports/waves/lab-a-routing-experiment.md). All eleven checks pass: 894 tests passed, eight engine cases skipped without new authorization, 320 stable inputs. Existing 316 inputs are unchanged. Decision wording, architectural status and formal maturity are unchanged; no whole-decision promotion or real-task learning evidence.

## W7.0a scoped application and evidence, 2026-09-08

The selector, cost model and published thresholds are unchanged. The features-v2 extractor now gives stronger lexical signals precedence, preventing two mixed-intent requests from inheriting clear-local treatment. Both now dispatch frontier in the synthetic full-path lab. Simple mechanical requests remain local; quoted and negated hard-action words can over-route. These observations do not establish model capability or savings.

[Report](../../reports/adrl-routing-correction-2026-09-08.md), [implementation guide](../../../adrl-core/docs/routing-features.md), [code diff](../../reports/research/routing-correction-2026-09-08/implementation.patch), [tests](../../../adrl-core/tests/unit/routing/test_mixed_intent.py), [all route changes](../../reports/research/routing-correction-2026-09-08/route-changes-final.md), [checks](../../reports/research/routing-correction-2026-09-08/checks-final/manifest.json), [validation](../../reports/research/routing-correction-2026-09-08/validation.json). Final validation: 159 focused tests; all eleven checks; 911 passed, eight engine cases skipped; 322 stable inputs. One initial candidate failed an existing sticky-cascade test and over-routed the flag case; both were repaired without changing the original suite. Decision text/status/formal maturity stay unchanged; named offline behavior only, no organic qualification or full-decision promotion.

## Decision

Within hard constraints, select the cheapest healthy rung whose estimated probability of completing the turn meets that rung's published completion threshold, where cost is the expected cost of the turn *including* the expected cost of a cascade if the rung fails and the prompt-cache state of the session.

1. "Likely to complete" means P(complete | rung, features) ≥ τ_rung, where τ_rung is a versioned policy constant per rung, and P is a named estimator (today: the deterministic band heuristics; later: RTG-007) whose calibration is reported against verified outcomes (MEM-003, LRN-001).
2. "Cheapest" is measured in expected session-marginal cost per RTG-009, not list price per turn; a rung whose cheap first attempt is expected to fail and escalate is charged the escalation cost too (RTG-005).
3. If no rung meets its threshold, the policy selects the highest permitted rung and records `no_rung_met_threshold` on the decision row so the case is visible in MEM rather than absorbed into the ordering.

## Context and rationale

The load-bearing words are "likely to complete", not "cheapest". If the policy optimised for cost alone it would send everything local and rely on escalation to clean up — and the developer waits through a failed attempt first. "Likely to complete" makes this a quality decision wearing a cost decision's clothes. The amendment does two things the original sentence left implicit: it names what "likely" means (a threshold on a named estimator, so the rule can be wrong in a measurable way) and it names what "cheapest" means (expected cost including cascade and cache effects, so a cheap-looking first attempt cannot hide an expensive session). The literature is unambiguous that cascades are only cheaper than direct routing when the estimate of "will this rung succeed" is good; with a noisy estimate, the cascade's retries eat the savings.

## Adversarial review (2026-09-02)

### Steelman
This is the FrugalGPT/Hybrid-LLM insight applied to an ordered ladder: choose the smallest model that will do, and let escalation absorb the residual. Health and hard constraints are removed first (SAF-006, SAF-001), so the ordering only ranges over feasible rungs. It is tested, and the rule is simple enough to be audited by reading `policy.py`.

### Attacks
1. **"Likely" is unquantified, so the rule is unfalsifiable as written.** Without a threshold and a named estimator there is no way to say the policy routed *wrongly* — every outcome is consistent with "we thought it was likely". Phase 0 produced only 34 of 300 required evaluated decisions and one task with strong verification, so today's "likely" is a heuristic band, not a probability. The text must say so.
2. **"Cheapest" is undefined and, on real agent traffic, per-turn list price is the wrong unit.** Anthropic bills cache reads at 0.1× base input (0.025× on the newest models) and cache writes at 1.25–2×; OpenAI similarly. A rung switch on a 150k-token transcript pays the full write cost again. GitHub's Copilot auto-selection reports that "switching models mid-session has shown increased cost without ample improvements in quality" and routes "along natural cache boundaries". The decision sentence does not mention cache, so a literal implementation optimises the wrong quantity. RTG-005's rationale mentions it; the *decision* text of RTG-002 does not.
3. **It double-owns the objective with RTG-005.** RTG-002 says minimise cost subject to likely completion; RTG-005 says optimise expected verified quality, retry risk, latency and cost. These are different objectives, and both are Accepted. One must be the deterministic instantiation of the other, or a future learned policy has two contradictory acceptance criteria.
4. **Cascade cost is invisible to the rule.** FrugalGPT-style cascades save money only when the scorer is good; the Unified Routing/Cascading paper shows cascading degrades "substantially" as post-hoc quality-estimate noise rises. ADRL's post-hoc estimator is the trip-wire set (CAS-001), which by the project's own admission misses methodical-but-wrong runs. A rule that treats a cheap first attempt as free of downstream cost systematically under-prices local.

### Evidence
- Chen, Zaharia, Zou, "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance" (arXiv 2023 / TMLR 2024) — LLM cascade with a learned scorer; reports up to 98% cost reduction *given a good scorer*, which is the premise attack 4 questions — https://arxiv.org/abs/2305.05176
- Ding et al., "Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing" (ICLR 2024) — routes on predicted quality gap with a tunable desired-quality level; the "desired quality" knob is precisely the τ_rung this amendment adds — https://arxiv.org/abs/2404.14618v1
- Dekoninck et al., "A Unified Approach to Routing and Cascading for LLMs" (arXiv 2024) — cascading performance "substantially" degrades with post-hoc estimation noise; good quality estimators are "the critical factor" (attack 4) — https://arxiv.org/abs/2410.10347
- Anthropic, "Prompt caching" (platform docs) — cache read 0.1× base (0.025× on Claude Fable 5.1 / Mythos 5.1), 5-min write 1.25×, 1-hour write 2×; hierarchy tools→system→messages (attack 2) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- OpenAI, "Prompt caching" (API docs) — reads 0.1× on GPT-5.6+, "a different model can use different weights and caching behavior" (attack 2) — https://developers.openai.com/api/docs/guides/prompt-caching
- GitHub Docs, "About Copilot auto model selection" — "Routing occurs along natural cache boundaries... Switching models mid-session has shown increased cost without ample improvements in quality" (attack 2) — https://docs.github.com/copilot/concepts/auto-model-selection
- ADRL Evidence & Readiness page (internal) — 34/300 evaluated decisions; one task with strong verification (attack 1).

### Verdict
**AMEND.** Attacks 1 and 2 land squarely: the decision sentence is the most-quoted rule in the register and it defines neither of its two operative words. Attack 3 is resolved by making RTG-002 the current deterministic instantiation of the RTG-005 objective (clause 1 names the estimator; clause 2 names the cost unit via RTG-009), so the two decisions no longer compete. Attack 4 is absorbed by clause 2 (cascade cost charged to the cheap rung). The spirit — quality decision in cost clothing — is preserved; the text now says what would count as being wrong.

## Amendments applied
- Replaced "likely to complete the task" with a thresholded, named estimator (clause 1).
- Replaced bare "cheapest" with expected session-marginal cost including cascade and cache (clause 2, referencing RTG-009).
- Added clause 3: explicit handling and ledger marker when no rung clears its threshold.

## Follow-ups
- [ ] Add `tau_by_rung` to versioned policy config; log the estimator name and version on every decision row alongside `route_id`.
- [ ] Golden test: identical features with a 120k-token cached session vs a 2k-token cold session must yield different cost estimates and, at the margin, different rung choices.
- [ ] Shadow report: for decisions where local was chosen, the realised cascade rate and realised session cost vs the counterfactual direct-to-cheap-cloud estimate.
- [ ] Reconcile RTG-002 and RTG-005 wording in the Confluence register so RTG-002 is explicitly "the deterministic instantiation of RTG-005's objective".

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded W7.0a scoped feature/compatibility application and before/after evidence | Prior decision text and dated evidence retained; features-v1 used first-match classification and exploration lacked this explicit live-feature/contract check |
| 2026-09-08 | Added scoped Lab A.1 synthetic workbench evidence and limitations | Prior decision wording, status, maturity and dated evidence retained |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: "likely" thresholded on a named estimator; "cheapest" defined as session-marginal cost including cascade and cache | "Within hard constraints, select the cheapest healthy rung likely to complete the task." |
| 2026-09-08 | Added scoped offline routing-diagnostic evidence and limitations; behaviour and grades unchanged | Decision wording retained unchanged; prior implementation/research notes preserved. |
