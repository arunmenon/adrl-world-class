# EVL: Evaluation, Graduation, Rollout

**Planning task-pack preparation, 2026-09-08:** [the next lab packet](../../reports/waves/lab-planning-deliverables.md) supplies draft PRD/HLD/LLD tasks and assessed-evidence contracts. Actual harness/mode execution, assessment calibration and any learning admission remain open. No runtime, decision text/status or maturity change is implied.

**Current Lab A.1 evidence, 2026-09-08:** [the synthetic routing workbench](../../reports/adrl-lab-first-run-2026-09-08.md) records tested scope for [EVL-005](ADRL-EVL-005.md). Actual decisions/dispatch and negative cases are inspectable; the engine and policy are unchanged. 894 tests passed, eight engine cases skipped, all eleven checks passed. Decision text/status/maturity and real-harness/learning gates remain unchanged. Only this bounded foreground slice restarted; hourly continuation stays paused. Earlier planning checkpoints below are historical.

**Experiment lab, 2026-09-08:** [the proposed lab](../../design/adrl-experiment-lab-plan-2026-09-08.md) extends existing task/evidence contracts across qualified harnesses and task types. Initial knowledge is pinned to supported versions and remains a candidate; simulated/benchmark evidence is not organic, and changing harnesses changes the comparison scope. Decision wording, maturity and implementation are unchanged; execution stays paused.

**Product planning, 2026-09-08:** The plan exposes first-harness baseline, T1/T5 and time-indexed feature conflicts; proposed experiments do not waive current evaluation or graduation rules. See the [startup roadmap](../../reports/adrl-product-roadmap-2026-09-08.md) and [context-graph proposal](../../design/adrl-context-graph-memory-proposal-2026-09-08.md). Implementation remains paused; decision text, architectural status and maturity are unchanged.

**Planning checkpoint, 2026-09-08:** the user requested the target adaptive routing/RSI architecture before further implementation. [Blueprint](../../reports/adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) and [all-ADR map](../../reports/research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) are proposals for disposition. Implementation continuation is paused; no decision wording, status or maturity is changed by the blueprint.

**W0 execution baseline, 2026-09-07:** [local engineering checks](../../reports/waves/w0-baseline.md)
now record source identity, individual failures and contract/ADR coverage. All 556 tests and
eleven checks pass. The [journey](../../reports/adrl-implementation-journey.md) tracks bounded
continuation. Status/maturity and broader release gates remain unchanged; historical notes follow.

**Forward plan proposed, 2026-09-07:** the [implementation roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md)
assigns this bucket's decisions to evidence-gated waves, with explicit stop/recovery conditions.
This is a planning update; current implementation and maturity remain as recorded below.

**Latest offline improvement evidence, 2026-09-07:** [EVL-006](ADRL-EVL-006.md), [EVL-005](ADRL-EVL-005.md), [EVL-009](ADRL-EVL-009.md), [EVL-008](ADRL-EVL-008.md) record
the applied verifier-comparison workflow and its limits. The current and proposed verifiers
classified 4/7 and 7/7 curated examples correctly; 549 implementation tests pass. These are
visible variants of one task family, with no automatic promotion or learning admission.
See the [report](../../reports/adrl-improvement-experiment-2026-09-07.md).

**Current session verification update, 2026-09-07:** [EVL-008](ADRL-EVL-008.md) record
API preview 4, independent encrypted session receipts and 532 passing tests. Two verifier jobs
each passed eight tests on the same prior pilot task; no general graduation or learning admission
follows. See the [report](../../reports/adrl-session-verification-2026-09-07.md). Earlier notes
below preserve their original scope.

**Live observation pilot, 2026-09-07:** [ADRL-EVL-008](ADRL-EVL-008.md) records
API preview 3 and its scoped live evidence: 18 reconciled tool events in one Claude Code session,
with 511 passing implementation tests. No general graduation or gateway-control claim follows.
See the [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md); earlier notes below retain their dated scope.

**Core question:** Is the behaviour ready for more exposure?
**Owns / does not own:** Owns baselines, holdouts, scorecards, exit gates, shadowing, canaries and readiness claims. Does not own runtime business logic, routing policy or the safety gates themselves.

Not captured in the 2026-08-27 source pack; known until 2026-09-03 only by cross-reference (EVL-004, 005, 006, 007, 009). This is the first capture. Every decision is Proposed and needs an owner and a disposition before entering the canonical register.

## First capture (2026-09-03)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-EVL-001 | Baseline set: four fixed comparators, two price bases | PROPOSED (new) |; → D0 | Q6 cannot be answered without a versioned comparator set; generalises the Phase 0 best-single-model baseline |
| ADRL-EVL-002 | Holdout and calibration protocol | PROPOSED (new) |; → D1 | adrl-core implements temporal session-grouped splits; no protocol document or scorecard yet |
| ADRL-EVL-003 | Branch protocol and replay prohibition | PROPOSED (new) |; → D0 | Writes the LRN-002/007 versus EVL-006 ruling into the owning bucket |
| ADRL-EVL-004 | Label quantity and quality gate | PROPOSED (new) |; → D1 | Five decisions cite a threshold this bucket never stated; four pre-registered conditions |
| ADRL-EVL-005 | Simulator and benchmark evidence is not organic | PROPOSED (new) |; → D1 | Already enforced by LRN-001 tiering; names what synthetic evidence may still do |
| ADRL-EVL-006 | Offline evaluation report | PROPOSED (new) |; → D0 | Six required items, hashed into the manifest; consolidates LRN-003/005/007 obligations |
| ADRL-EVL-007 | Human graduation and the D2 to D5 ladder | PROPOSED (new) |; → D1 | The ladder every review downgrade assumed; new implementations inherit no maturity above D2 |
| ADRL-EVL-008 | Scorecard format | PROPOSED (new) |; → D0 | Exclusions before metrics; the review's denominator rule as a template |
| ADRL-EVL-009 | Blockers are never averaged away | PROPOSED (new) |; → D1 | Eight pre-registered blockers, versioned; a score cannot absorb one  2026-09-09 <!-- taxonomy-sync:taxonomy-sync-gate:ADRL-EVL-009 --> [Scoped sync gate](../../reports/reviews/taxonomy-sync-gate-2026-09-09/report.md); maturity unchanged |

Tally: 9 PROPOSED.

## Cross-cutting findings

1. **The bucket was load-bearing while absent.** MEM-002, MEM-004, MEM-008, LRN-001, LRN-003, LRN-005, LRN-007 and LRN-008 all defer a threshold, a report or a gate to EVL. Each obligation is now placed in one decision here, and each such decision cites the decisions that created it.

2. **Replay is prohibited as evidence anywhere in the register** (EVL-003). The review resolved this as a cross-bucket conflict; the bucket that owns evaluation now states it, with the Replay Gap study cited as the register already cites it and the 2026-09-03 external review's further preprints recorded as corroboration, not proof.

3. **A brand-new implementation inherits no maturity above D2** (EVL-007). The adrl-core rewrite of 2026-09-02 starts each decision at the level its own tests support. Measurements about traffic (tokenizer ratios, cache-hit ratio, continuation share) transfer as config defaults; measurements about code do not.

4. **Exclusions come before metrics** (EVL-008). Pinned, suppressed, degraded-memory, subagent and erased shares are the first section of every scorecard, implementing the review's register-wide denominator rule.

5. **Blockers are a versioned list, not a weight** (EVL-009). Eight blockers are pre-registered, five of them created by other buckets' amendments. Adding or removing one is a config version with a reason.

6. **Dependencies on OPS.** Graduation signatures need a key held outside the training team (OPS-002); D4 needs an exercised rollback (OPS-007); the fail-open blocker needs the SLO thresholds (OPS-008); the unanchored-ledger blocker needs checkpoint verification (SAF-009, OPS-007).

## Sources consulted

- Register files: `source/01-overview-tenets-taxonomy.md`, `REVIEW-LOG.md`, ADRL-FND-005, ADRL-RTG-007, ADRL-RTG-009, ADRL-MEM-002, ADRL-MEM-006, ADRL-MEM-008, ADRL-MEM-009, ADRL-MEM-010, ADRL-LRN-001 to LRN-008.
- A. Gonuguntla, "The Replay Gap: Static Evaluation of Model Switching in LLM Agents Scores the Wrong World" (arXiv 2608.08239, 2026), as cited in ADRL-MEM-009; https://arxiv.org/html/2608.08239
- C. Northcutt, A. Athalye, J. Mueller, "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021), as cited in ADRL-MEM-009; https://arxiv.org/abs/2103.14749
- Google SRE, "Canarying Releases" (The Site Reliability Workbook), as cited in `adr/SEM/README.md`; https://sre.google/workbook/canarying-releases/
- SWE-Router (arXiv 2607.00053), Agent-as-a-Router (arXiv 2606.22902), The Routing Plateau (arXiv 2606.07587); cited by the 2026-09-03 external review; not independently fetched.
