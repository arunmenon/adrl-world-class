# ADRL-LRN-007 — No autonomous online promotion

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · unchanged |
| Maturity | D0 Design, review recommends D0 Design — the graduation pipeline (EVL-006/007) is the thing that would implement it and it has never been exercised |
| Review verdict | APPROVE |
| Tenets | 4, 9 |
| Related decisions | LRN-005, LRN-006, LRN-008 (proposed), EVL-005, EVL-006, EVL-007, EVL-009, OPS (rollback) |
| Open questions | Q4 |

## Decision

Learning may propose policy updates, but deployment requires offline evaluation and explicit graduation; no autonomous online promotion.

## Offline verifier improvement implementation, 2026-09-07

The applied improve CLI can recommend candidate_supported, no_improvement, regression or indeterminate. It contains no deployment or promotion command and creates no routing or learning artifact. Every final report declares review_required=true and eligible_for_learning=false. The example candidate remains archived for review, without replacing the prior pilot verifier.

The trusted local operator prepares and executes reviewed proposals. There is no proposal-generating agent, automated human-approval service or remote role implementation. Future adoption needs its own review and evidence; a recommendation is not graduation. Recursive improvement of the proposal mechanism has not been implemented or demonstrated.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## Forward implementation plan, 2026-09-07 (proposed)

The roadmap places optional learned routing in W9, bounded automated proposals in W10 and a conditional comparison of improvement methods in W12. No autonomous promotion is introduced. Candidate authors remain separate from release assessment and signing authority where required. Evidence origin/quality and algorithm decisions must be reconciled before learning, and a failed improvement hypothesis may lead to keeping a simpler policy. No proposer, training run or scheduled background loop is launched by this plan.

See the [detailed wave roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md) and
[wave execution packet](../../reports/adrl-wave-execution-template.md). The roadmap maps all
77 stable decisions to review waves. This is planning linkage only: prior decision wording,
architectural status, existing implementation evidence and maturity remain unchanged.

## Context and rationale

No model promotes itself. Deployment requires offline evaluation against baselines and an explicit human graduation step (EVL-006/007). No metric threshold auto-promotes, because a threshold is a number computed on a corpus that this register repeatedly describes as thin, single-user and biased by privacy suppression; a self-promoting loop on such a corpus would compound whatever the corpus gets wrong.

The review leaves the text unchanged and records the case against it honestly. Bandits and online learners run safely in production at consumer scale, and the review brief asks whether this decision is too conservative. The answer is that every published safe deployment of online learning relies on preconditions ADRL does not have: cheap, fast, high-volume, low-noise reward; logged propensities; offline evaluation before an A/B test; and a bounded action space where a bad arm costs a click, not a duplicated migration on a payments repo. Where those preconditions are absent the conservative rule is not conservatism, it is arithmetic. Two things the decision does *not* forbid should be said plainly: recalibrating thresholds inside an approved artifact is a new artifact version (LRN-005) and goes through the same gate; and logged exploration (LRN-008) is not promotion — it is data collection under a fixed, graduated policy.

## Adversarial review (2026-09-02)

### Steelman
Tenet 9 says learning cannot self-promote, and this is that tenet as a decision. The register's own evidence pack says the corpus is single-user, retrieval is biased by privacy suppression, one task has strong verification and simulator evidence is not organic; any automatic promotion rule computed on that corpus would promote on artefacts of the corpus. Explicit human graduation is also the only step at which company-specific risk (payments code, PCI scope) can be weighed by someone accountable.

### Attacks
1. **Too conservative — online learning runs safely in production elsewhere.** Spotify runs contextual bandits on its home page and Netflix on artwork; these systems adapt continuously. Answered by the details: Spotify's 2025 deployment was preceded by offline benchmarking against historical baselines and an online A/B test against a control, uses ε-greedy exploration under a KL-divergence penalty that bounds deviation from the predicted distribution, and is described as cautious and supervised. Its 2018 bandit work likewise validated on historical logs and then a live A/B test. That *is* offline evaluation plus explicit graduation; the bandit adapts parameters inside a graduated policy, which LRN-007 permits as long as parameter changes are versioned (LRN-005). What those systems have and ADRL lacks — millions of cheap, immediate, unbiased rewards — is the actual reason ADRL cannot go further.
2. **"No autonomous promotion" could freeze useful recalibration.** If a calibration map (LRN-006) drifts, must a human re-graduate a threshold nudge? Answered: yes, as a new artifact version through EVL-006/007, but the gate can be lightweight for parameter-only changes with the same feature schema and objective. That is a process design in EVL, not a change to this text. The alternative — automatic recalibration in place — is exactly the hidden feedback loop the technical-debt literature warns about.
3. **Offline evaluation is misleading for agentic routing.** Replay-based offline evaluation of model switching scores the wrong world. If the "offline evaluation" the decision requires is a replay, it will pass artifacts that fail live. Answered: EVL-006's offline evaluation must be branched or paired (LRN-002), not replay; and the decision requires graduation *after* offline evaluation, which in EVL includes shadow and canary — the live steps the replay-gap paper recommends. Cross-reference recorded as a follow-up for EVL-006.
4. **Human graduation is a bottleneck that will be bypassed under pressure.** A monthly graduation meeting will be skipped when a savings number is on the table. Answered: this is the point of writing it down as a decision with EVL-009's "blockers never averaged away". The mitigation is to make the gate cheap to run (automated evidence pack, canary tooling) so that the human step is a review, not a project.
5. **Exploration looks like online learning.** LRN-008 randomises a fraction of ambiguous-band turns. Does that violate "no autonomous online promotion"? Answered: no — the exploration policy is itself a graduated, fixed artifact; it changes *data*, not *policy*; the estimators trained on that data still go through this gate. The rationale now says so explicitly.

### Evidence
- Spotify Research, "Calibrated Recommendations with Contextual Bandits on Spotify Homepage" (2025) — deployed March 2025 after offline benchmarking against historical baselines (+35% podcast accuracy vs 7-day baseline) and an online A/B test against a 90-day baseline; ε-greedy with a KL-divergence penalty bounding deviation; cautious, supervised rollout; attack 1 — https://research.atspotify.com/2025/9/calibrated-recommendations-with-contextual-bandits-on-spotify-homepage
- J. McInerney et al., "Explore, Exploit, Explain: Personalizing Explainable Recommendations with Bandits" (RecSys 2018; Spotify Research) — bandit validated on historical logs then via live A/B test at scale; attack 1 — https://research.atspotify.com/publications/explore-exploit-explain-personalizing-explainable-recommendations-with-bandits
- E. Breck et al., "The ML Test Score" (IEEE BigData 2017) — "Model quality is validated before serving", "Models are tested via a canary process before production serving", "Models can be quickly and safely rolled back"; the graduation pipeline this decision requires, as an industry rubric (attacks 2, 4) — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — hidden feedback loops as a named debt category; automatic in-place recalibration is one (attack 2) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- A. Gonuguntla (CMU), "The Replay Gap" (arXiv 2608.08239, 2026) — replay-based offline evaluation of agentic model switching mispredicts outcomes; live/branched evaluation required (attack 3) — https://arxiv.org/html/2608.08239
- A. Swaminathan, T. Joachims, "Counterfactual Risk Minimization" (ICML 2015) — learning from logged bandit feedback requires logged propensities; the precondition for any future relaxation toward online learning (attack 5, LRN-008) — https://arxiv.org/abs/1502.02362

### Verdict
**APPROVE.** The "too conservative" attack is the important one and it does not survive contact with the production bandit literature: the cited deployments perform offline evaluation and A/B graduation and bound the policy's deviation, which is what this decision requires; their continuous adaptation lives *inside* a graduated policy with cheap, immediate, high-volume reward that ADRL does not have. Attacks 2 and 5 are clarified in the rationale (versioned recalibration; exploration ≠ promotion) without changing the text. Attack 3 lands on EVL-006 (offline evaluation must be branched, not replay). Attack 4 is process design.

## Amendments applied

None — decision stands as written. Rationale expanded to state that (a) parameter recalibration is a new artifact version through the same gate and (b) logged exploration under a graduated policy is data collection, not promotion.

## Follow-ups

- [ ] EVL-006: require that "offline evaluation" of any routing artifact uses branched pairs (LRN-002) or logged-propensity OPE (LRN-008), never replay; record this as an EVL amendment.
- [ ] EVL-007: define a lightweight graduation path for parameter-only artifact changes (same feature schema, objective and deny-list version) so that recalibration is cheap to graduate and no one is tempted to automate it.
- [ ] OPS: automate the evidence pack and canary/rollback tooling so the human graduation step is a review, not a project.
- [ ] Golden test: no code path in `live_router.py`/`policy.py` loads an artifact that lacks a graduation record (LRN-005 manifest field signed by EVL-007).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Linked proposed implementation roadmap and dependent decision questions | Prior decision and evidence preserved; no runtime or maturity change in this planning pass |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Learning may propose policy updates, but deployment requires offline evaluation and explicit graduation; no autonomous online promotion." |
