# ADRL-EVL-006: Offline evaluation against baselines, branched or propensity-weighted

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture; referenced by LRN-003, LRN-007, LRN-008 since 2026-08-27) |
| Maturity | D0 Design; adrl-core has an `adrl learning evaluate` command that runs the estimators T1-only, but no evaluation report has been produced against a baseline version |
| Review verdict | PROPOSED (new) |
| Tenets | 3, 8, 9 |
| Related decisions | LRN-002, LRN-003, LRN-005, LRN-007, LRN-008, EVL-001, EVL-002, EVL-003, EVL-007 |
| Open questions | Q4, Q6 |

## Decision

Before any routing artifact (heuristic version, calibration map, estimator, exploration rule) may be proposed for graduation (EVL-007), it receives an offline evaluation report that (1) cites a baseline version (EVL-001) and reports the artifact against all four comparators at both price bases; (2) computes every metric under the holdout protocol (EVL-002); (3) draws its counterfactual evidence only from live branches or from off-policy estimates validated against branches on the same slice (EVL-003); (4) reports the excluded fraction, the suppressed fraction and the tier mix of its evidence; (5) states the minimum realised gain the artifact was required to show (RTG-007) and whether it was met; and (6) is hashed, and the hash is written into the artifact manifest (LRN-005 v2). A report that omits any item is incomplete, not failing, and cannot be presented at graduation.

## Offline verifier improvement implementation, 2026-09-07

The new offline verifier-comparison workflow applies the baseline-report discipline to a bounded verifier proposal. A frozen versioned suite and two operator plans are admitted against a declared command/timeout allowance; the minimum gain is recorded before execution. Every trial and the final recommendation are retained. The demonstrated candidate classified seven of seven curated examples correctly against four of seven for the current verifier, with two agreeing repetitions and no execution blockers.

This is a scoped verifier mechanism exercise, not the six-part routing evaluation required by the Decision above. It has no policy counterfactuals, protected holdout, four routing comparators or price-basis comparison, and cannot be submitted as a complete routing graduation report. The same assistant authored the visible fixtures and candidate. The public API remains preview 4; the workflow is a local CLI and reusable library.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## Context and rationale

LRN-007 says deployment requires "offline evaluation against baselines" and left the definition to this bucket. LRN-003 names the RouteLLM-style pairwise baseline the estimator must beat; LRN-005 v2 adds the evaluation report hash to the manifest. The review's central worry about offline evaluation was that "offline" would be read as "replay"; EVL-003 closes that, and this decision lists what else a report has to contain so that a graduation meeting is reading the same document every time.

## Adversarial review (2026-09-03)

### Steelman
A fixed report format with a hash in the manifest is how model-card practice keeps an artifact and its evaluation together. Every item in the list traces to a decision that already demanded it.

### Attacks
1. **Six required items make recalibration expensive.** Answered: EVL-007 defines a lightweight path for parameter-only changes; the report for such a change may cite the previous report for unchanged items.
2. **The "minimum realised gain" is set by the people who want to pass it.** Answered: the value is versioned next to `readiness-score-v1.json` (RTG-007) and changing it is itself a change reviewed at graduation; FND-005's self-grading attack is answered by the register-wide rule that D-levels certify behaviour.
3. **A report can be complete and still wrong.** Answered: the report format is necessary, not sufficient; EVL-007's human step and EVL-009's blockers carry the rest.

### Evidence
- ADRL-LRN-007; "Deployment requires offline evaluation against baselines and an explicit human graduation step (EVL-006/007)."
- ADRL-LRN-003 follow-up; RouteLLM-style pairwise baseline evaluated T1-only as the reference to beat.
- ADRL-LRN-005 follow-up; manifest v2 includes the EVL-006 evaluation report hash.
- ADRL-RTG-007; pre-build gate and versioned minimum realised gain.

### Verdict
**PROPOSED.** Consolidates obligations already placed on this bucket by three LRN decisions. Needs an owner and a report template.

## Follow-ups

- [ ] Write the report template (`evl-report-v1.md`) with the six sections and a machine-readable header.
- [ ] Golden test: `load_graduated` refuses a manifest whose evaluation report hash does not match a stored report.
- [ ] Produce the first report for the deterministic heuristic itself (RTG-002 at its current policy version) so the pipeline is exercised before any learned artifact exists.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
