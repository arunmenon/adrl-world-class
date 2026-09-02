# ADRL-LRN-005 — Every artifact is fully versioned

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · unchanged |
| Maturity | D2 Tested, review recommends D2 Tested for the contract (`learning_contract.py`, `learning-contract-v1.json` are tested), with the explicit note that no learned artifact has ever been produced, so the contract has been tested against fixtures only |
| Review verdict | APPROVE |
| Tenets | 9 |
| Related decisions | LRN-001, LRN-003, LRN-004, LRN-006, LRN-007, MEM-001, MEM-007, OPS (rollback), EVL-006, EVL-007 |
| Open questions | — |

## Decision

Every learned artifact versions its feature schema, data snapshot, objective, calibration, thresholds and policy compatibility.

## Context and rationale

A model artifact you cannot reproduce is a liability. Every artifact carries the feature schema it expects, the data snapshot it was trained on, the objective it optimised, its calibration mapping, the thresholds that turn its output into advice, and the policy versions it is compatible with. That is what makes "roll back the router" a real operation rather than a hope, and what lets EVL say which artifact a readiness claim is about.

The review leaves the text unchanged. The six named components are the right ones and map cleanly onto both the model-card and the ML-production-readiness literature; the attacks below add items the *manifest* should carry (training code commit, seed, embedding-model version, ledger high-water mark, evidence-tier mix, evaluation report) and one runtime property (fail closed on incompatibility), all of which are implementation follow-ups on `learning-contract-v1.json` rather than changes to a decision that already says "everything that determines the artifact is versioned". The one substantive caveat is on maturity: a versioning contract that has never versioned a real artifact is tested against fixtures, and the register should say so.

## Adversarial review (2026-09-02)

### Steelman
Reproducibility and rollback are the two properties without which a learned router cannot be operated safely; the decision names precisely the components that vary between trainings and makes each one part of the artifact's identity. It is the LRN-side precondition for EVL-006/007 (offline evaluation and explicit graduation) and for Tenet 9's "versioned features, calibration, holdouts... rollback".

### Attacks
1. **The list is incomplete for reproducibility.** Training code commit, random seed, the local embedding model version (which changes every embedding feature), the ledger high-water mark the "data snapshot" refers to (MEM-007), and the evidence-tier mix (LRN-001) are all needed to reproduce an artifact and none is named. "Data snapshot" is doing a lot of work. Answered: the decision says the artifact versions "its data snapshot"; the amendment belongs in the manifest schema, and a follow-up adds the missing fields. The decision's intent is clearly "everything that determines the artifact".
2. **"Policy compatibility" is undefined and unenforced.** Which policy versions (SAF gates, RTG thresholds, CAS trip-wire config, failure-type enum version from MEM-004) does an artifact declare compatibility with, and what happens at load time if the running policy differs? If the answer is "a warning", the decision protects nothing. Answered by follow-up: fail closed — an artifact whose declared compatibility does not match the running policy versions is not loaded and the deterministic policy runs (LRN-006/007 posture). This is a runtime rule in OPS/EVL, not a change to this text.
3. **A version is not a report.** Versioning the calibration and thresholds says which ones were used; it does not say how good they were. Model-card practice pairs the artifact with its evaluation conditions and results on named slices. The EVL-006 offline evaluation report should be part of the artifact bundle (by hash), or a rollback target could be an artifact that was never evaluated. Follow-up on the manifest.
4. **D2 for a contract with no artifact.** The contract is tested against fixtures. No learned artifact exists (LRN-003, LRN-006, LRN-007 are D0). The claim "Tested" is true of the code and vacuous of the property. Recommend keeping D2 with the caveat stated in the register.
5. **Rollback is only real if the previous artifact's *inputs* still exist.** Rolling back to artifact N−1 requires N−1's feature schema to be computable from today's decision rows (LRN-004 snapshot) and N−1's embedding model to be available. If the embedding model was upgraded and old vectors shredded (MEM-010), N−1 cannot be re-evaluated, only re-served. Answered: acceptable, provided OPS keeps the last K embedding-model versions; follow-up.

### Evidence
- M. Mitchell et al., "Model Cards for Model Reporting" (FAT* 2019; arXiv 1810.03993) — artifacts should ship with intended use, evaluation conditions and per-slice results; supports attack 3's "bundle the evaluation report" — https://arxiv.org/abs/1810.03993
- E. Breck et al., "The ML Test Score" (IEEE BigData 2017) — Infra tests: "training is reproducible", "model quality is validated before serving", "models can be quickly and safely rolled back to a previous serving version"; Data test: "feature expectations are captured in a schema"; attacks 1, 2, 5 — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — configuration debt and data dependencies as first-class debt; an artifact that does not pin its data and config versions is the canonical example (attack 1) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- Microsoft Azure Architecture Center, "Event Sourcing pattern" — snapshots and stream positions as the identity of derived state; the "data snapshot" should be a ledger position (attack 1) — https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing

### Verdict
**APPROVE.** Every attack is either a manifest-field addition (1, 3), a runtime enforcement rule owned by OPS/EVL (2, 5), or a maturity caveat (4). None changes what the decision says; all sharpen how it is implemented. The decision is already the general statement — every determinant of the artifact is versioned — and the follow-ups enumerate the determinants the current schema misses.

## Amendments applied

None — decision stands as written.

## Follow-ups

- [ ] Extend `learning-contract-v1.json` → v2 with: training code commit, seed, embedding-model version, ledger high-water mark, evidence-tier mix (LRN-001), feature deny-list version (LRN-004), failure-type enum version (MEM-004), and a hash of the EVL-006 evaluation report.
- [ ] Define "policy compatibility" as a set of (policy id, version) pairs: SAF gate config, RTG thresholds, CAS trip-wire config, MEM-004 enum; golden test that loading an artifact with a mismatched pair fails closed to the deterministic policy and emits telemetry.
- [ ] OPS: retain the last K embedding-model versions and document that rollback beyond K is serve-only, not re-evaluable.
- [ ] Register note: mark LRN-005 as "D2 (contract tested against fixtures; no artifact produced)" until the first real artifact exists.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Every learned artifact versions its feature schema, data snapshot, objective, calibration, thresholds and policy compatibility." |
