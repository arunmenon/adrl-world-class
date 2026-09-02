# ADRL-MEM-003 — Verification enriches, never overwrites

| Field | Value |
|---|---|
| Bucket | MEM — Memory, Evidence, Label Integrity |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested for the non-overwrite contract; note that only one task has strong verification, so the contract has one real exercise |
| Review verdict | AMEND |
| Tenets | 8 |
| Related decisions | MEM-001, MEM-002, MEM-004, MEM-009, SAF-007, LRN-001, LRN-004, EVL-004 |
| Open questions | Q6 |

## Decision

Deterministic verification enriches an outcome without overwriting observed telemetry: each verification run is appended as its own event carrying the verifier version, the exact command, the working-tree identity it ran against and its own pass/fail/indeterminate result, so that "appeared to succeed" and "verified to succeed" remain separately queryable and a verifier that ran against a drifted tree is distinguishable from one that ran against the turn's output.

1. **Verification has provenance.** A verification event records `verifier_version`, command line, protected-path policy version (SAF-007), tree identity (commit hash or content hash of touched files) and wall-clock start/end.
2. **Verification can be wrong, so it can be repeated.** Multiple verification events per `route_id` are permitted; a flaky or environment-failed run is recorded as `indeterminate`, not as `fail`, and label derivation (MEM-004) uses the latest non-indeterminate event.
3. **Verification against a drifted tree is not verification of the turn.** If the tree identity at verification time differs from the tree identity at `closed_turn` beyond the turn's own edits, the event is flagged `tree_drift=true` and is excluded from capability labels.

## Context and rationale

Running the tests must not overwrite what was observed at the time. If the verifier's result replaced the observed telemetry, the ledger would lose the single most useful signal for a router: "the model appeared to succeed but actually failed" — the case where the cheap rung is confidently wrong and no trip-wire fires. Keeping the observation and the verification as separate columns (now: separate events) is what makes that signal exist.

The amendment adds what "verification" needs to carry to be believable. A verifier is code execution against a working tree, and both the code and the tree change: tests are flaky, environments fail, and a developer keeps editing after the turn closes. Without the verifier's own provenance, a `verified=fail` event cannot be distinguished from "the tests were broken", "the environment was down" or "someone changed the file afterwards" — and every one of those would be recorded as a capability failure of the rung that served the turn.

## Adversarial review (2026-09-02)

### Steelman
Separating observation from verification is cheap, obviously correct, and required by MEM-001's append rule anyway. It preserves the "silent failure" signal that motivates the whole learned-router effort, and it gives EVL a way to measure label precision (observed vs verified) rather than assume it.

### Attacks
1. **The verifier is not ground truth; it is another noisy instrument with no recorded provenance.** Flaky tests are common (a large share caused by async waits and concurrency), and benchmark curation shows that a majority of "verified" coding tasks had invalid or over-specific tests before human review. A verification event with no verifier version, command or environment identity cannot be audited, so a verifier bug silently becomes a capability label. The decision says verification enriches; it does not say what an enrichment must contain.
2. **Verification runs after the turn, against whatever tree exists then.** The register admits automatic verification is "not connected to every eligible task" and `live_verification.py` runs post hoc. By the time it runs, the developer (or a later turn on a different rung) may have edited the same files. A pass then credits the wrong rung; a fail then blames the wrong rung. The decision must bind verification to a tree identity, or MEM-009's "explicit `route_id` only" rule is satisfied in form and violated in substance.
3. **"Enrich" hides a state transition.** MEM-002's lifecycle has no state for "verified"; verification may arrive before or after `closed_final`. If it arrives after, clause 2 of MEM-002 (late evidence re-derives the label) applies; if the decision does not say so, an implementation will reasonably treat `closed_final` as terminal and drop the verification. The two decisions need an explicit seam.
4. **One task.** The code reality is that exactly one task has strong test-based verification. The non-overwrite contract is tested, but the decision's value proposition — a stream of observed-vs-verified pairs — has a sample size of one task. Claiming D2 for the contract is fair; claiming any evidence about label precision from it is not.
5. **Verifier under SAF-007 may be constrained into indeterminacy.** Protected-path and execution policy can prevent the verifier from running the real test suite (e.g. tests that touch a payments sandbox, secrets, or network). The result is then neither pass nor fail. Without an `indeterminate` outcome the policy-blocked run will be recorded as a failure — a policy failure masquerading as capability, which is exactly what MEM-004 exists to prevent.

### Evidence
- Q. Luo, F. Hariri, L. Eloussi, D. Marinov, "An Empirical Analysis of Flaky Tests" (FSE 2014) — 201 flaky-test fixes across 51 Apache projects; async wait (45%), concurrency (20%) and test-order dependency (12%) account for 77%; supports attack 1 and clause 2 — https://mir.cs.illinois.edu/lamyaa/publications/fse14.pdf
- OpenAI, "Introducing SWE-bench Verified" (2024) — 93 professional developers screened 1,699 SWE-bench samples; 68.3% had at least one severe issue (underspecified statement, over-specific/invalid tests, environment failures); GPT-4o resolved 33.2% on the verified subset vs 16% on the original. Shows that "the tests passed/failed" is itself an unreliable label without curation; attack 1 — https://openai.com/index/introducing-swe-bench-verified/
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021 Datasets & Benchmarks) — average ≥3.3% label errors across 10 benchmark test sets, ≥6% on ImageNet val; small error rates change model rankings. Bears on attack 4: ranking rungs on a thin, noisy verified set is unstable — https://arxiv.org/abs/2103.14749
- W3C, "PROV-DM" — activities `used` entities and `generated` new ones; a verification run is an activity whose inputs (tree, verifier) should be recorded as used entities, which is what clause 1 asks — https://www.w3.org/TR/prov-dm/

### Verdict
**AMEND.** The core rule (never overwrite observation) is right and stays verbatim in spirit. Attacks 1, 2 and 5 land: a verification event with no provenance, no tree binding and no indeterminate result is a label-noise generator, and the SAF-007 interaction produces policy failures typed as capability failures. Attack 3 is fixed by cross-reference to the amended MEM-002. Attack 4 does not change the text but caps what the D2 label means.

## Amendments applied

- Added: each verification run is its own appended event (not a column on the outcome), with verifier version, command, tree identity and result (clause 1).
- Added `indeterminate` as a verification result for flaky/env/policy-blocked runs; label derivation uses latest non-indeterminate event (clause 2).
- Added `tree_drift` flag and exclusion from capability labels when the tree at verification time differs from the tree at `closed_turn` beyond the turn's own edits (clause 3).
- Rationale updated to state the seam with MEM-002 (verification after `closed_final` is late evidence).

## Follow-ups

- [ ] Extend `verifier.py` / `live_verification.py` output with `verifier_version`, command, tree identity, policy version and `indeterminate`; golden test that a SAF-007 path block produces `indeterminate`, not `fail`.
- [ ] Golden test: edit a verified file after `closed_turn`, run verification, assert `tree_drift=true` and that MEM-004 label derivation ignores it.
- [ ] Golden test: verification arriving after `closed_final` produces a `late_evidence` event and re-derives the label (seam with MEM-002).
- [ ] Report observed-vs-verified disagreement rate per rung in the EVL pack; until ≥2 tasks have strong verification, mark the number as anecdotal.
- [ ] Re-run each verification twice on the one strongly-verified task to measure its own flake rate before it is used as a label source.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: verification events carry provenance, tree identity and an indeterminate result; drifted-tree runs excluded from capability labels | "Deterministic verification enriches an outcome without overwriting observed telemetry." |
