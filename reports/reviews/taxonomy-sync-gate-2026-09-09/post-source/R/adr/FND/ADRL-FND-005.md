# ADRL-FND-005 — Scope expands only through measured gates

| Field | Value |
|---|---|
| Bucket | FND — System Boundary and Principles |
| Status | Accepted · unchanged |
| Maturity | D3 Shadow, review recommends D3 Shadow with a note: the D-scale measures runtime behaviour and fits a governance commitment poorly; the honest reading is "the readiness tooling runs against shadow data and its verdicts have so far been respected" |
| Review verdict | APPROVE |
| Tenets | 8, 9 |
| Related decisions | EVL-004, EVL-005, EVL-006, EVL-007, EVL-009, LRN-007, MEM-008, RTG-006 |
| Open questions | Q6 |

## Decision

Scope expands only through measured phase gates; component presence is not readiness.

### Product application, 2026-09-07

For the current product workstream, keep the public API in preview until real integrations have
validated at least two harnesses and two protocols. Claude Code is the first path, OpenCode tests
reuse of the Messages profile, and Codex tests a separately admitted Responses profile. Passing
offline tests for the first extraction does not satisfy that release gate. Changes to the contract
during preview are versioned and recorded with their compatibility impact. See the
[product contract](/Users/arunmenon/projects/adrl-world-class/design/adrl-multi-harness-product-contract-2026-09-07.md)
and [implementation evidence](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md).

## Product service evidence, 2026-09-07

The local product-service package passed 506 tests and a real loopback HTTP smoke check using synthetic observations. This adds D2 evidence for the tested services. No real Claude Code task, second harness or second protocol was validated; the first stable product-interface gate remains unmet.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Earlier subscription pilot plan, 2026-09-07

Use the existing Claude Code subscription for a native task baseline before a planned
observation-only integration. Neither establishes that ADRL intercepted model requests,
enforced egress policy or saved model cost. The later gateway pilot needs separate provider
access and a budget. The [pilot brief](../../reports/adrl-claude-subscription-pilot-2026-09-07.md)
records a prepared independent repository fixture and its existing test failures. No real
harness run or maturity promotion occurred; the two-harness/two-protocol release gate stands.

## Live observation pilot, 2026-09-07

A native subscription baseline and one instrumented repair session now exist. The repair passed eight independently checked tests; 18 real tool events reconciled with ADRL. This is one bounded observation pilot. No gateway privacy, local routing, organic quality or savings claim follows, and the two-harness/two-protocol release gate remains unmet.

The [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md) links the applied 15-file package, 511 passing tests,
all required checks, reviewed outcomes and remaining blockers. Architectural status is unchanged;
this evidence does not promote the full decision to D3 or D4. Earlier dated sections preserve
their original implementation and planning scope.

## Session verification implementation, 2026-09-07

The product now has an applied local operator verification path whose receipts can be read beside one live pilot session's observations. The implementation suite passes 532 tests; the final live check used two repeated verifier jobs on the same prior task and copied state. This supports scoped D2 for the receipt contract plus concrete local execution evidence. It does not graduate routing, privacy controls or the overall product. The two-harness/two-protocol stable-release gate remains unmet.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

The applied 13-file package passes 549 tests and all six required checks; the data inventory covers 256 fields. Source application verified the 274-file baseline and preserved 267 untouched originals. The first offline verifier comparison is concrete scoped implementation evidence: 4/7 baseline and 7/7 candidate classifications on seven curated variants of one earlier task family.

This supports D2 for the tested comparison/archive contract. It does not graduate the whole product, establish a trained router, demonstrate recursive self-improvement, validate another harness or satisfy the two-harness/two-protocol stable-release gate. The next evidence priorities are exact task-close binding and fresh independently reviewed tasks.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## Forward implementation plan, 2026-09-07 (proposed)

The proposed long-horizon roadmap separates trustworthy evidence, portability, controlled execution, measured routing and stable local release from later learned routing, automated proposals, managed teams and RSI research. Each wave has evidence gates and an explicit recovery path. A completed implementation task does not move maturity or grant deployment authority. Current implementation evidence remains the 549-test package and the scoped curated experiment; the plan adds no runtime capability.

See the [detailed wave roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md) and
[wave execution packet](../../reports/adrl-wave-execution-template.md). The roadmap maps all
77 stable decisions to review waves. This is planning linkage only: prior decision wording,
architectural status, existing implementation evidence and maturity remain unchanged.

## W0 execution baseline, 2026-09-07

W0 now records bounded local engineering checks and before/after hashes for declared source inputs. A failed check, stale contract or changed input prevents a passing combined result. The source backups preserve the existing dirty repositories. This improves evidence attribution and repeatability; the two-harness/two-protocol product gate remains unmet.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.


## Taxonomy synchronization tooling, 2026-09-09

A local development completion gate now requires declared-source change ownership and dated register/evidence mappings, pinned semantic review and final drift checks. This is a scoped application of measured engineering gates; it does not amend runtime graduation blockers or promote maturity. Global INDEX IDs and affected bucket coverage are checked; historical grade/other-bucket reconciliation remains unfinished. Code: [checker](../../../adrl-world-class/tools/check_taxonomy_sync.py), [tests](../../../adrl-world-class/tests/test_taxonomy_sync.py). 2026-09-09 <!-- taxonomy-sync:taxonomy-sync-gate:ADRL-FND-005 --> [Evidence and limits](../../reports/reviews/taxonomy-sync-gate-2026-09-09/report.md).

## Context and rationale

"We wrote the code" is not "it is ready". Scope expands only through measured gates. This is a governance commitment rather than a technical one, and it is what licenses the honest D0 entries elsewhere in the register. Without it, the natural pressure is to treat a merged component as a delivered capability — which is precisely how a cost optimisation ends up degrading someone's workflow.

The review leaves the sentence unchanged. Its weakness is not in the text but in what surrounds it: the gates are defined and graded by the same team (`config/readiness-score-v1.json`, `tools/check_readiness_score.py`), there is no stated rule that thresholds are fixed *before* the measurement is taken, and there is no de-promotion trigger — the decision is written as a ratchet upward. Those are follow-ups on EVL and OPS, not changes to the principle. The register's own maturity ordering (FND strongest, LRN weakest, no decision at D5) is evidence the commitment is being honoured today.

## Adversarial review (2026-09-02)

### Steelman
This is the decision that keeps the register honest. Every other bucket's D0 entries — the learned router, subagent identity, the utility estimator — exist as D0 only because this decision makes it safe to admit them. It maps directly onto NASA's readiness-level discipline (a prototype demonstrated in a relevant environment is not one demonstrated in the operational environment) and onto SRE canary practice (exposure grows with evidence, not with code completeness). A the company engineering review is more likely to be harmed by scope creep in a cost project than by any single routing bug.

### Attacks
1. **Self-graded gates.** The readiness score is authored, computed and interpreted by the team that wants to pass it. NASA's TRL scale and Google's canary process both assume an assessor or an SLI-based automatic judgment that the deploying team does not control. Nothing in the pack names an independent approver for a phase transition; EVL-007's "explicit human graduation" does not say *whose* human.
2. **Thresholds are not pre-registered.** A gate whose threshold can be chosen after the measurement is a gate that always passes. The pack says "34 evaluated decisions vs required 300" for similar-task lookup, which is a pre-set number and good practice; it does not say the same for every gate in `readiness-score-v1.json`, and nothing forbids editing the JSON in the same PR that adds the evidence.
3. **No de-promotion path.** The decision only speaks of expansion. If a D4 pilot produces regressions, the register has no rule that says the decision drops to D3 and what evidence would restore it. Canary practice is symmetric: a failed canary rolls back. A ratchet-up-only governance rule will accumulate optimistic maturity labels — FND-004's D4 claim, which this review lowers, is an instance.
4. **"Measured" without "representative".** Q6 states representativeness, not volume, is binding; the Phase 0 corpus is single-user and workflow-heavy. A gate can be measured and passed on unrepresentative traffic. Google's canary chapter warns that a canary must span enough diversity and time for behaviour to be attributable; the decision should not be satisfied by any measurement, only by measurements on the population the next phase will expose.
5. **The D-scale is being used for non-runtime decisions.** FND-005 is "D3 Shadow", but a governance rule does not "run against real traffic". Labelling it D3 is a category error that slightly undermines the scale's credibility for the decisions where it matters.

### Evidence
- NASA, "Technology Readiness Levels" (nasa.gov) — TRL 5–6 (relevant/lab environment) is distinguished from TRL 7–8 (operational environment demonstration); shows a mature readiness scale separates "works in the lab" from "works in the field", supporting the principle and attack 4 — https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/
- Google SRE, "Canarying Releases" (SRE Workbook, ch. 16) — canary population and duration must be chosen so observed behaviour is attributable; before/after comparisons are confounded by time; multiple simultaneous canaries contaminate signal; bears on attacks 3, 4 — https://sre.google/workbook/canarying-releases/
- ADRL evidence pack, `01-overview-tenets-taxonomy.md` — "no decision at D5", "live adaptive routing intentionally blocked", "34 evaluated decisions vs required 300"; internal evidence that the commitment is currently being honoured; bears on the verdict.
- No direct literature found on pre-registration of engineering readiness thresholds; reasoning from first principles (attack 2) and by analogy to pre-registered study designs.

### Verdict
**APPROVE.** None of the attacks lands on the sentence itself; each lands on the machinery that enforces it, which belongs to EVL and OPS. Attack 3 (no de-promotion) is the most serious and is recorded as a follow-up for an EVL amendment rather than a change here, because "scope expands only through gates" does not preclude contraction — it simply does not mention it. Attack 5 is a labelling issue noted in the maturity field. The decision stands as written because it is doing its job: this review's own downgrades (FND-004, SAF-002, SAF-007) are only possible because the register separates acceptance from maturity.

## Amendments applied

None — decision stands as written.

## Follow-ups

- [ ] EVL amendment (proposed): phase-gate thresholds are pre-registered — `readiness-score-v1.json` is versioned and a threshold change and the evidence that meets it may not land in the same change.
- [ ] EVL amendment (proposed): de-promotion triggers — name the regression conditions under which a decision's maturity is lowered, and what restores it.
- [ ] Name the approver role for each D3→D4 and D4→D5 transition (independent of the ADRL team; candidate: enterprise gateway owner plus security architect for SAF).
- [ ] Add a representativeness check to every gate: the population measured must be the population the next phase exposes (Q6).
- [ ] Register housekeeping: mark governance-only decisions (this one) with a maturity note rather than a runtime D-level.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-07 | Linked proposed implementation roadmap and dependent decision questions | Prior decision and evidence preserved; no runtime or maturity change in this planning pass |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Recorded applied observation mode and the first live subscription pilot | Decision policy and status unchanged; prior evidence was offline or synthetic, with observation-only launch still planned |
| 2026-09-07 | Recorded native-subscription baseline and separately scoped observation/gateway pilot stages | Decision unchanged; the earlier product application did not distinguish these billing and coverage paths |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Applied the measured-scope principle to the first stable multi-harness API; release gate remains unmet | Principle unchanged; this product-specific application was absent |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Scope expands only through measured phase gates; component presence is not readiness." |

| 2026-09-09 | <!-- taxonomy-sync:taxonomy-sync-gate:ADRL-FND-005 --> [Local sync-gate evidence](../../reports/reviews/taxonomy-sync-gate-2026-09-09/report.md); no grade change | Prior decision wording and dated evidence preserved |
