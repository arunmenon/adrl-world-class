# ADRL-EVL-005: Simulator and benchmark evidence is not organic evidence

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture; referenced by the overview, LRN-001, MEM-009 since 2026-08-27) |
| Maturity | D1 Code; adrl-core `learning/tiers.py` assigns simulator and benchmark examples to tier T4 and refuses to pool them with organic tiers; no scorecard separates them yet |
| Review verdict | PROPOSED (new) |
| Tenets | 8, 9 |
| Related decisions | LRN-001, LRN-002, MEM-009, EVL-004, EVL-006, EVL-008 |
| Open questions | Q6 |

## Experiment-lab planning note, 2026-09-08

The proposed experiment lab records execution mode separately from evidence origin. Actual models running benchmark/generated tasks still produce lab evidence, not organic developer outcomes. Such evidence may bootstrap descriptive K0 knowledge and permitted weak-signal work; it cannot satisfy organic gates or independently authorize live learned routing. See the [lab proposal](../../design/adrl-experiment-lab-plan-2026-09-08.md). This is a pending planning application; decision text, status and maturity remain unchanged.

## Lab A.1 implementation evidence, 2026-09-08

A reusable synthetic workbench now reports curated T4 provenance separately from execution mode and marks exports ineligible for learning. Every planned cell remains visible, including blocked, unsupported, errored and interrupted work. The run exercises six task families but creates no verified task outcomes, organic labels or K0 checkpoint. This is a scoped developer diagnostic; the general experiment archive/API and real-harness runner remain open.

[Report](../../reports/adrl-lab-first-run-2026-09-08.md), [runner](../../../adrl-core/tools/run_routing_lab.py), [tests](../../../adrl-core/tests/unit/test_routing_lab.py), [run evidence](../../reports/research/routing-lab-2026-09-08/run-2/results.json), [engineering checks](../../reports/research/routing-lab-2026-09-08/engineering-checks.json), [validation](../../reports/research/routing-lab-2026-09-08/validation.json), [follow-on scope](../../reports/waves/lab-a-routing-experiment.md). All eleven checks pass: 894 tests passed, eight engine cases skipped without new authorization, 320 stable inputs. Existing 316 inputs are unchanged. Decision wording, architectural status and formal maturity are unchanged; no whole-decision promotion or real-task learning evidence.

## Decision

Evidence produced by the simulator, by public benchmarks, or by any synthetic task generator is a separate evidence family from organic traffic. It is recorded with `source=synthetic`, assigned to its own tier (LRN-001 T4), reported in its own section of every scorecard, and never counted toward any gate that names organic evidence (EVL-004, the RTG-007 pre-build gate, the D3 and D4 rungs of EVL-007). Synthetic evidence may qualify a mechanism (a trip-wire fires, a transform produces a valid request, a sandbox denies egress) and may bound a claim (a rung cannot be worse than its benchmark score suggests), but it cannot establish that a rung is reliable on the organisation's code.

## Offline verifier improvement implementation, 2026-09-07

Every new verifier comparison is explicitly curated_synthetic and ineligible for learning. Seven distinct content fingerprints include two correct implementations, four deliberate defects and a missing-configuration environment. These are variants of one task family, authored with the candidate by the same assistant; they are not seven organic task completions, independently sampled cases or a blind holdout.

The report separates these cases from prior Claude pilot observations. Correct classification on all seven establishes the mechanism exercise only. Duplicate fingerprints are rejected to prevent counting identical copies, but distinct fingerprints cannot establish semantic diversity or statistical independence. Fresh examples with independent expectation review are the next evidence requirement.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## Context and rationale

The overview lists "simulator evidence ≠ organic evidence (EVL-005)" among the explicit non-claims and records that local-rung reliability on realistic code is not established because the only evidence is small edits on small files. LRN-001 made the separation a tier. This decision is the rule those cite. Its purpose is to stop a passing simulator run from being read as readiness, which is the failure FND-005 warns against.

## Adversarial review (2026-09-03)

### Steelman
Synthetic tasks are written by the people who wrote the router and share their blind spots; a benchmark is public and models have seen it. Neither says anything about a payments monorepo with its own edit dialect. Keeping them in a separate family costs nothing and prevents the most tempting overclaim.

### Attacks
1. **Synthetic evidence is the only evidence that exists for adversarial safety cases.** Answered: mechanism qualification is explicitly permitted; the adversarial suites (SAF) are synthetic by nature and count toward SAF maturity, not toward routing readiness.
2. **A well-built simulator seeded from organic transcripts is closer to organic than the rule admits.** Answered: seeding from organic data does not make outcomes organic; it makes them replay-adjacent (EVL-003). The family label stays synthetic.
3. **Total separation forbids using benchmarks to prune obviously infeasible rungs.** Answered: bounding claims are permitted; a benchmark can remove a rung from consideration, never admit one.

### Evidence
- `source/01-overview-tenets-taxonomy.md`; explicit non-claim "simulator evidence ≠ organic evidence (EVL-005)"; local-rung reliability "NOT established".
- ADRL-LRN-001; tier T4 for simulator and benchmark data; pooling forbidden.
- ADRL-FND-005; component presence is not readiness; the same logic applied to evidence provenance.

### Verdict
**PROPOSED.** Already enforced by LRN-001's tiering; this decision gives the rule a home and names what synthetic evidence may still do.

## Follow-ups

- [ ] Scorecard section "synthetic evidence" listing mechanism qualifications and bounds separately from organic metrics.
- [ ] Golden test: a readiness computation that includes a `source=synthetic` outcome in an organic count fails.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Added scoped Lab A.1 synthetic workbench evidence and limitations | Prior decision wording, status, maturity and dated evidence retained |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
