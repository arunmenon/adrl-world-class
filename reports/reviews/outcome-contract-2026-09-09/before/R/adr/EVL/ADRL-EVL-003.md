# ADRL-EVL-003: Branch protocol and replay prohibition

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; adrl-core has a branched-pair contract and a subprocess branch runner (LRN-002), but no branch has been executed on organic traffic |
| Review verdict | PROPOSED (new) |
| Tenets | 5, 8, 9 |
| Related decisions | LRN-002, LRN-007, LRN-008, MEM-009, CAS-004, EVL-001, EVL-006 |
| Open questions | Q4, Q6 |

## Decision

Counterfactual evidence about a routing choice comes only from live branches: both arms execute from the same repository snapshot, transcript prefix, tool results, harness dialect and verifier version up to the decision boundary (LRN-002), bound to an explicit `route_id` (MEM-009). Replaying a logged trajectory with a different model, or substituting a model into a stored transcript and scoring the stored outcome, is prohibited as evidence anywhere in the register: not in an evaluation report, not in a readiness score, not in a graduation pack. Off-policy estimates from logged propensities (LRN-008) are admissible only after they have been validated against live branches on the same slice, and the validation result is attached to the estimate.

## Context and rationale

The review resolved the LRN-002/007 versus EVL-006 conflict by ruling that offline evaluation must be branched or propensity-weighted, never replay. This decision is that ruling written in the bucket that owns evaluation. The grounds are the Replay Gap study already cited by MEM-009 and the LRN README: early model swaps diverge at the first post-fork action in most cases, and replay predicted none of the outcome flips that branching found. A brand-new implementation makes the point sharper, since it has no logged trajectories of its own yet and would be tempted to reuse the old repository's.

## Adversarial review (2026-09-03)

### Steelman
Branching is the only evaluation whose world is the one the router would actually create. Prohibiting replay costs compute; permitting it costs correctness, and the register already accepted the cost side when it amended LRN-002.

### Attacks
1. **Branches are expensive and the pair budget (LRN-002) is in the hundreds per slice.** Answered: cost is why LRN-008 exists; the prohibition does not require pairs to exist, it requires that what is called evidence be a pair.
2. **Same-model branches also diverge, so divergence is not evidence of a swap effect.** Answered: LRN-002 requires a same-model control divergence as the noise floor; a branch study reports it.
3. **The prohibition blocks cheap sanity checks.** Answered: replay may be used to test the plumbing (does the transform produce a valid request), never to produce an outcome label; the scorecard has a separate "plumbing checks" section.
4. **The evidence rests on a single 2026 preprint.** Answered: the external review of 2026-09-03 cites the same study and three further routing preprints that reach the same conclusion from other angles; those are recorded as guides for experiments, not settled proof, and the prohibition stands on the register's own tenet 8.

### Evidence
- A. Gonuguntla, "The Replay Gap" (arXiv 2608.08239, 2026), as cited in ADRL-MEM-009 and `adr/LRN/README.md`; 74–77% of early swaps diverge at action 0; replay predicted 0 of 5 success-relevant flips.
- SWE-Router (arXiv 2607.00053), Agent-as-a-Router (arXiv 2606.22902), The Routing Plateau (arXiv 2606.07587); cited by the 2026-09-03 external review; not independently fetched; used only as corroboration that execution-grounded signals matter.
- `REVIEW-LOG.md`, cross-bucket conflicts table; "Offline evaluation of a routing artifact must be branched or propensity-weighted, never replay."

### Verdict
**PROPOSED.** Turns an existing review ruling into a bucket decision. Needs an owner; no new evidence is required to accept it.

## Follow-ups

- [ ] Golden test: an evaluation report whose evidence rows carry `source=replay` is rejected by the scorecard builder.
- [ ] Run the first same-model control branch on the shadow corpus to establish the noise floor before any swap branch is scheduled.
- [ ] Attach the branch-versus-OPE validation result to every LRN-008 estimate that enters a scorecard.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
