# ADRL-MEM-009 — Counterfactuals bind only to explicit route_id

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · unchanged |
| Maturity | D2 Tested, review recommends D2 Tested — `counterfactual.py` and `live_verification.py` enforce explicit binding under test; usable volume is very low but that is a corpus fact, not a maturity fact |
| Review verdict | APPROVE |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-002, MEM-003, MEM-006, SEM-006, CAS-005, LRN-002, LRN-004, LRN-008 (proposed), EVL-005 |
| Open questions | Q3, Q6 |

## Decision

Counterfactual evidence attaches only to an explicit `route_id`; time or session proximity is never used to guess ownership.

## Context and rationale

No guessing by timestamp, ever. A counterfactual is the most expensive evidence the system produces — a second attempt of the same task on a different rung — and its entire value is that it is about *that* decision. Pairing by "same session, roughly the same time" would work most of the time and silently mis-pair occasionally; a mis-paired counterfactual is a confident, wrong label on the most influential row in the corpus. Better to have fewer counterfactuals than any that are wrong. This is also why the corpus is small, and the register asks whether the rule should be relaxed for volume. It should not.

The review leaves the text unchanged. Explicit binding is necessary; the attacks below show it is not sufficient — a counterfactual also has to be run from the same state, which is LRN-002's job — and that the binding has to survive the memory-degraded path (MEM-006) and the subagent gap (SEM-006). Those are recorded as follow-ups and cross-references, not as changes to a rule that is already stated as strongly as it can be.

## Adversarial review (2026-09-02)

### Steelman
Provenance standards require derivation to be asserted, not inferred from co-occurrence; lineage tools correlate by run id, not by time. The decision applies that principle to the one place in ADRL where inference-by-proximity would be tempting and cheap. It is tested, it is unambiguous, and it makes the counterfactual corpus small and honest rather than large and contaminated.

### Attacks
1. **Explicit binding is necessary but not sufficient.** A counterfactual attached to the right `route_id` but executed from a different working-tree state (later edits, different tool results, different prompt-cache state) is still about a different world. Recent branched-rollout work on agentic model switching shows that replaying a logged trajectory with a different model diverges at the first post-fork action in 74–77% of early swaps and that replay-based evaluation predicted zero of five success-relevant outcome flips. The counterfactual must be a live branch from the same snapshot and turn state, not a re-run "for the same route_id". Answered: that requirement is LRN-002's, amended there; this decision correctly owns only ownership.
2. **How does the `route_id` reach the counterfactual runner?** The harness never sees `route_id` unless the proxy injects it (e.g. in metadata). If the counterfactual runner obtains the id by looking up "the decision this session made most recently", the rule is violated by the lookup even though the stored link is explicit. The decision forbids proximity guessing but does not say the id must be *carried*, not *looked up*. Answered by code map (`counterfactual.py` takes the id explicitly under test) and a follow-up test on the propagation path.
3. **Degraded memory breaks the binding silently.** Under MEM-006 an unlogged decision has no persisted `route_id`. A counterfactual then either fails to attach (good) or attaches to a `route_id` that exists only in process memory and is lost on restart (bad). Answered by MEM-006's amendment (degraded decisions excluded from evidence) plus a follow-up test here.
4. **Subagents have no route identity.** SEM-006 is D0 and subagent traffic passes through. Any counterfactual for work a subagent did cannot bind to anything, which means the rule makes subagent counterfactuals impossible rather than wrong. That is the correct outcome; it must be stated as a known exclusion in the evidence pack so the corpus bias is visible.
5. **Volume pressure will come back.** The register's own open item invites relaxing this rule for volume. The counter-argument is quantitative: with a corpus of tens of pairs, a single mis-pair is a multi-percent label error, and label-error rates of a few percent are enough to reverse model rankings. Relaxing the rule for volume trades a small sample with clean labels for a slightly larger sample with unknown contamination — strictly worse for the estimator LRN-003 wants. Answered.

### Evidence
- A. Gonuguntla (CMU), "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World" (arXiv 2608.08239, 2026) — branching rollouts on SWE-bench with Qwen3-4B/14B swaps: 74–77% of early swaps diverge at action 0 vs 6–35% for same-model controls; 61–94% of post-fork actions differ; 5 outcome flips all in swap arms; replay predicted 0/5 success-relevant calls; recommends live/branched evaluation and OPE validated against branched ground truth (attack 1) — https://arxiv.org/html/2608.08239
- W3C, "PROV-DM: The PROV Data Model" — `wasDerivedFrom` must be asserted; a chain of usage and generation is necessary but not sufficient for derivation; the standards basis for "explicit only" — https://www.w3.org/TR/prov-dm/
- OpenLineage, "Object Model" — run state updates are correlated by a client-maintained `runId`, not by time; industry analogue of explicit binding (steelman) — https://openlineage.io/docs/spec/object-model/
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021) — a few percent label error changes model rankings; quantifies why one mis-paired counterfactual in a tiny corpus is unacceptable (attack 5) — https://arxiv.org/abs/2103.14749

### Verdict
**APPROVE.** Attacks 1, 3 and 4 are answered by neighbouring decisions (LRN-002, MEM-006, SEM-006) and recorded as follow-ups; attack 2 is a propagation-path test, not a text change; attack 5 is the register's own invitation to relax, and the evidence says no. The rule is correctly scoped to ownership and is stated in its strongest form. Do not relax it for volume; get volume from LRN-008 (proposed exploration channel) instead.

## Amendments applied

None — decision stands as written.

## Follow-ups

- [ ] Golden test: the counterfactual runner receives `route_id` as an explicit argument carried from the proxy's decision event; assert there is no code path that resolves it by session/time lookup (grep `counterfactual.py`, `live_verification.py` for "latest"/"most recent" resolution).
- [ ] Golden test: counterfactual submitted for a `route_id` that was never persisted (NullProvider path) is rejected with a logged reason, not attached.
- [ ] EVL pack: state the subagent exclusion explicitly (no counterfactuals for subagent work until SEM-006 leaves D0) and report the excluded share of traffic.
- [ ] LRN-002: require counterfactuals to be branched from the same snapshot and turn state (see LRN-002 amendment).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Counterfactual evidence attaches only to an explicit `route_id`; time or session proximity is never used to guess ownership." |
