# ADRL-EVL-008: Scorecard format: every number with its denominator, window and exclusions

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture) |
| Maturity | D0 Design; the old repository published `reports/learning-readiness.md`; adrl-core produces a readiness report object but no scorecard document |
| Review verdict | PROPOSED (new) |
| Tenets | 8 |
| Related decisions | FND-005, MEM-005, MEM-006, MEM-010, SEM-006, LRN-002, EVL-001, EVL-002, EVL-004, EVL-005, EVL-009 |
| Open questions | Q6 |

## Decision

The evidence pack for any window is one scorecard with a fixed structure: (1) window identity (dates, harness and model versions, config versions, ledger high-water mark); (2) traffic denominators (requests by class, turns, sessions, lineages, users, repositories); (3) the excluded fraction by reason (pinned, suppressed, degraded memory, subagent passthrough, unverifiable, erased) reported before any metric; (4) organic metrics under EVL-002 with intervals; (5) synthetic evidence in its own section (EVL-005); (6) counterfactual pairs: budget, count, noise floor (LRN-002); (7) open blockers (EVL-009) listed by name with the decision they block; (8) the maturity ladder position of every decision the window bears on (EVL-007). A figure that appears without its denominator and window is not admissible in the register.

## Live observation pilot, 2026-09-07

The manual pilot report distinguishes two engineered sessions, one task family, one repository and one user from organic evaluation. The first fix passed four tests but failed independent compatibility review; the repair passed eight tests. Feedback, initial code, verifier and Claude version changed, so the runs are not counterfactual pairs and imply no latency/cost effect. Reported API-equivalent cost is separated from subscription billing. This does not implement the general scorecard generator or satisfy graduation gates.

The [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md) links the applied 15-file package, 511 passing tests,
all required checks, reviewed outcomes and remaining blockers. Architectural status is unchanged;
this evidence does not promote the full decision to D3 or D4. Earlier dated sections preserve
their original implementation and planning scope.

## Session verification implementation, 2026-09-07

The final verification exercise contains two local verifier jobs, each running eight test cases, on one existing repaired task. These are repeated checks, not two new coding tasks or counterfactual policy pairs. The copied timeline grew from 18 observations to 22 entries with no changed prior entries, model calls or provider spend. An earlier developmental run is disclosed separately. The report gives denominators and excludes verifier precision, routing quality, savings and organic learning claims; the general scorecard generator remains unimplemented.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

The first comparison reports seven curated code variants, two arms and two repeats: 28 verifier trials, 98 executed commands and 30 archive records. Baseline and candidate contain eight and eleven tests respectively; repetition does not multiply the seven-case denominator. Correct case classifications are 4/7 and 7/7; no uncertainty interval or organic accuracy estimate is claimed.

The configured budget allows at most 98 commands and a sum of 2940 seconds of declared timeout ceilings. This is admission accounting, not a total wall-clock or resource guarantee. The exercise made no model calls. The full product-level cost/quality/latency scorecard is still pending.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## Context and rationale

The review proposed a register-wide rule that every evidence metric reports its denominator and its excluded fraction, prompted by MEM-005, MEM-006, SEM-006 and LRN-002. A scorecard with a fixed order makes the rule a template rather than a reminder, and puts the exclusions before the metrics so the reader meets the denominator first. The old repository's readiness scorecard is the precedent; this decision generalises its shape and adds the sections the review found missing.

## Adversarial review (2026-09-03)

### Steelman
Fixed structure is what makes two windows comparable and what makes a missing section visible. The exclusions-first ordering is the cheapest defence against the invisible-denominator finding in the MEM review.

### Attacks
1. **Eight sections for a small team is bureaucracy.** Answered: sections 1 to 3 are generated from the ledger; only 7 and 8 need judgement.
2. **Erasure changes past scorecards.** Answered: a scorecard records the ledger high-water mark and erased-session count at generation time and is itself immutable; MEM-010 makes erasure in a window an EVL-009 blocker for that window.
3. **The scorecard encourages metric shopping across windows.** Answered: windows are declared in advance in the EVL config, not chosen after the fact.

### Evidence
- `REVIEW-LOG.md`, register-wide rules; "Every evidence metric reports its denominator and its excluded fraction."
- ADRL-MEM-010; counts of erased sessions and reasons reported in the EVL pack; erasure inside a window is a blocker.
- ADRL-MEM-009 follow-up; the subagent exclusion must be stated in the EVL pack with its share of traffic.
- `source/01-overview-tenets-taxonomy.md`; the old readiness scorecard and its "transparent ADR evidence index".

### Verdict
**PROPOSED.** A template, not a new principle; needed before the first D2 to D3 move.

## Follow-ups

- [ ] Write `evl-scorecard-v1.md` template and a generator over the ledger for sections 1 to 6.
- [ ] Golden test: the generator refuses to emit a metric whose denominator is zero or unreported.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Recorded applied observation mode and the first live subscription pilot | Decision policy and status unchanged; prior evidence was offline or synthetic, with observation-only launch still planned |
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
