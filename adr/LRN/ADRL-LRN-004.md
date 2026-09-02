# ADRL-LRN-004 — Pre-decision features, enforced by construction

| Field | Value |
|---|---|
| Bucket | LRN — Learning and Adaptation |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D1 Code — the prohibition is stated in `learning_contract.py` and tested as a rule, but the enforcement mechanisms (decision-time feature snapshot, time-respecting projections, temporal split) do not exist, so leakage is currently prevented by convention |
| Review verdict | AMEND |
| Tenets | 8, 9 |
| Related decisions | MEM-001, MEM-007, MEM-008, CAS-006, OPS-006, LRN-001, LRN-003, LRN-005, EVL-006 |
| Open questions | — |

## Decision

Learned models may use only information available before the routing decision, enforced by construction: the exact feature vector the router observed is persisted on the decision event at decision time and is the only feature source for training; retrieval and similar-task features are computed against a projection frozen at the decision's ledger position (MEM-007); evaluation uses time-ordered splits; and outcome, served-rung, verification and any later-session information are prohibited features with a maintained deny-list checked in CI.

1. **Snapshot at decision time.** `decisions` rows carry `features_v<N>` as observed by `features.py` at the decision boundary; training reads that column and never recomputes features from the ledger.
2. **Time-respecting retrieval.** Any neighbour/retrieval feature used in training is computed from a projection rebuilt "as of" the decision's ledger high-water mark; a projection containing later rows is a leak.
3. **Temporal validation.** Holdouts are later-in-time than training data; random K-fold over turns is prohibited because turns within a session and episode are dependent.
4. **Deny-list.** `served_rung` (CAS-006/OPS-006), any `outcome_*`, verification results, escalation events, `closed_*` timestamps, and session fields populated after the decision are prohibited; the list is versioned with the feature schema (LRN-005).

## Context and rationale

No peeking at the future. A feature derived from how the turn turned out — the served rung after transport fallback, whether escalation fired, whether the verifier passed — will make offline metrics look superb and live performance collapse, because at decision time none of it exists. The register asks the right question: how is this enforced, not just stated?

The amendment answers it with the standard mechanism from the leakage literature: learn-predict separation with legitimacy tagging. The router already computes a feature vector at the decision boundary; persisting *that vector* as the training source makes leakage structurally impossible for direct features, because training never touches the ledger's later columns. The remaining leak paths are subtler and specific to this system — a retrieval index that contains the future (MEM-007), and random splits over dependent turns — and both are closed by clauses 2 and 3. Training/serving skew is the other half of the same problem: if training recomputes features from the ledger with different code than served them, the model learns a distribution it will never see live.

## Adversarial review (2026-09-02)

### Steelman
The no-time-machine rule is the most fundamental correctness constraint in offline learning and the one most often violated by accident. Stating it as a decision, naming the two most likely offenders (outcome and future-session leakage) and tying it to `learning_contract.py` is more than most teams do before their first model.

### Attacks
1. **Stated, not enforced.** The register's own open item concedes it. A prohibition in a contract file is checked against a manifest's column names; it cannot see a feature that was *recomputed* from ledger rows written after the decision (e.g. "number of turns in this session" computed at training time over the whole session). Only a decision-time snapshot closes this class.
2. **The retrieval index is a leak by construction.** MEM-008's similar-task lookup runs over the NumPy index built from the whole ledger. In offline evaluation of retrieval-advised routing, a historical decision's neighbours include later sessions whose outcomes are known — the model "remembers" the future. Without MEM-007's ledger high-water mark and an as-of rebuild, this leak cannot even be detected.
3. **`served_rung` is the most tempting leak.** CAS-006 and OPS-006 correctly record the rung that actually served. It is also the perfect proxy for "what happened next" and sits in the same row family as the decision. It must be on a deny-list by name, not covered by "outcome leakage" in general.
4. **Random splits over turns leak through sessions and episodes.** Turns in one session share the repo, the developer, the task and the sticky-escalation state (CAS-005). A random K-fold puts turn 7 in training and turn 8 in test; the model learns the session, not the task. The decision says nothing about split design, and the register's single-user corpus makes this worse.
5. **Training/serving skew is leakage's twin and is unaddressed.** If `features.py` changes between the time a decision was logged and the time a model is trained, recomputing features from the ledger yields a vector the router never saw. Snapshotting at decision time fixes this for free, and the ML-readiness literature lists "training and serving features compute the same values" as a required test.
6. **Privacy-suppressed features are missing-not-at-random.** MEM-005 suppresses embeddings for private/pinned turns; a model trained with embedding features will see them missing precisely on sensitive work. That is legitimate (it was missing at decision time too) but must be encoded as an explicit missingness indicator, not imputed — otherwise "no embedding" becomes a learned proxy for "sensitive", which the model must not act on for routing (SAF-001 owns that). Rationale note and follow-up, not text.

### Evidence
- S. Kaufman, S. Rosset, C. Perlich, O. Stitelman, "Leakage in Data Mining: Formulation, Detection, and Avoidance" (ACM TKDD 6(4), 2012) — formal legitimacy ("no time machine"); two leakage types (feature leakage; training-example contamination, e.g. KDD-Cup 2007 Netflix); recommended fix is learn-predict separation with legitimacy tagging; attacks 1, 2, 4 — https://dl.acm.org/doi/10.1145/2382577.2382579 (PDF mirror: https://www.cs.umb.edu/~ding/history/470_670_fall_2011/papers/cs670_Tran_PreferredPaper_LeakingInDataMining.pdf)
- E. Breck et al., "The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction" (IEEE BigData 2017) — Infra test "training is reproducible"; Monitoring test "training and serving are not skewed" (feature codepaths differ at train vs inference); Data test "feature expectations captured in a schema"; attack 5 — https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/
- D. Sculley et al., "Hidden Technical Debt in Machine Learning Systems" (NIPS 2015) — data dependencies and hidden feedback loops as debt sources; a retrieval index that feeds on its own outcomes is a hidden feedback loop (attack 2) — https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems
- SQLite, "PRAGMA data_version" / "Write-Ahead Logging" — mechanism for MEM-007's ledger-position stamps that clause 2 depends on — https://www.sqlite.org/pragma.html

### Verdict
**AMEND.** Attacks 1–5 all land and all have the same root: the decision prohibits but does not construct. The leakage literature's answer is thirty years old and cheap here — snapshot the feature vector at the decision boundary, freeze projections at the decision's ledger position, split by time, and deny-list the known post-decision columns by name. The maturity claim is downgraded to D1 for the enforcement, not for the rule.

## Amendments applied

- Added "enforced by construction" with four mechanisms: decision-time feature snapshot as the sole training source; as-of projections for retrieval features; temporal splits; versioned deny-list including `served_rung`.
- Rationale expanded to cover training/serving skew and the MNAR nature of privacy-suppressed features.

## Follow-ups

- [ ] Add `features_v<N>` (JSON) to the `decisions` row written by `live_router.py`/`features.py`; golden test that a training manifest reading any other feature source is rejected by `learning_contract.py`.
- [ ] Implement as-of projection rebuild (MEM-007 follow-up) and require it in any offline evaluation of retrieval features; golden test: neighbour with a later `route_id` than the query decision is never returned.
- [ ] Replace any random K-fold in evaluation code with time-ordered, session-grouped splits; golden test that no session spans train and holdout.
- [ ] Add the deny-list to `learning-contract-v1.json` with `served_rung`, `outcome_*`, `verified_*`, `escalated`, `closed_*` and CI-check manifests against it.
- [ ] Encode embedding-missingness as an explicit indicator and confirm in EVL that the estimator's behaviour on missing-embedding turns does not differ from the deterministic policy in a way that acts as a privacy proxy.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: enforcement by construction — decision-time feature snapshot, as-of projections, temporal splits, named deny-list | "Learned models may use only information available before the routing decision; outcome and future-session leakage are prohibited." |
