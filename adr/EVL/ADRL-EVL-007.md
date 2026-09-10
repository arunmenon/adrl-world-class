# ADRL-EVL-007: Explicit human graduation and the D2 to D5 ladder

| Field | Value |
|---|---|
| Bucket | EVL; Evaluation, Graduation, Rollout |
| Status | Proposed 2026-09-03 (first capture; referenced by LRN-005, LRN-007, LRN-008 since 2026-08-27) |
| Maturity | D1 Code; adrl-core `learning/artifacts.py` refuses any artifact without a signed graduation record and checks policy compatibility; no graduation has ever been performed and the signing key in use is a development key (OPS-002) |
| Review verdict | PROPOSED (new) |
| Tenets | 9 |
| Related decisions | FND-005, LRN-005, LRN-007, LRN-008, EVL-006, EVL-009, OPS-002, OPS-005 |
| Open questions | Q4, Q6 |

## Decision

Maturity moves only by an explicit, recorded human decision, one rung at a time, on the evidence named for that rung:

| From | To | Evidence required | Who records it |
|---|---|---|---|
| D1 Code | D2 Tested | Unit, integration and fault tests for the decision's promised behaviour pass; for SAF decisions the adversarial suite has run at least once and its results are published | Decision owner |
| D2 Tested | D3 Shadow | The behaviour has run against organic traffic without affecting execution for a declared window (EVL config), every metric reports its excluded fraction, and no EVL-009 blocker is open for the window | Decision owner plus one reviewer outside the team |
| D3 Shadow | D4 Pilot | An EVL-006 report meets the RTG-007 minimum realised gain against all four baselines, a rollback path is exercised (OPS-007), and a constrained population is named | Graduation meeting, minuted |
| D4 Pilot | D5 Graduated | Pilot window closed with no blocker, the excluded fraction of the pilot population reported, and the security owner's sign-off for any SAF or TRU decision | Graduation meeting, minuted |

Two further rules. First, a learned artifact's graduation record is a signature over its manifest (LRN-005 v2) by a key held outside the team that trained it (OPS-002); the router refuses artifacts without it (LRN-007). A parameter-only change (same feature schema, objective, deny-list and enum versions) may use a lightweight path: a single reviewer, a report that cites unchanged sections, and the same signature. Second, a brand-new implementation inherits no historical maturity above D2: shadow and pilot evidence attaches to the code that produced it, and the adrl-core build of 2026-09-02 therefore starts every decision at the level its own tests support.

## Forward implementation plan, 2026-09-07 (proposed)

The roadmap proposes per-wave entry/exit evidence, explicit budget/stop conditions, reviewer roles and rollback that preserves pins and erasure state. Decision queue item DQ4 identifies that the current generic graduation ladder asks for routing gains even for non-routing integration/control features. A scoped qualification amendment is proposed for later disposition; the existing ladder is not changed or bypassed by this note. No new D3–D5 or release decision occurs in this planning pass.

See the [detailed wave roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md) and
[wave execution packet](../../reports/adrl-wave-execution-template.md). The roadmap maps all
77 stable decisions to review waves. This is planning linkage only: prior decision wording,
architectural status, existing implementation evidence and maturity remain unchanged.

## W0 execution baseline, 2026-09-07

W0 inventories the architectural status and maturity wording of all 77 ADRs without normalizing historical claims into a portfolio score. Starting scheduled work and passing local checks do not promote a decision. Independent review roles remain unassigned; DQ4 still needs disposition before applying a changed graduation process to integration features.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.

## Context and rationale

The register separates status from maturity and defines D0 to D5, but no decision said what moves a level. The review's downgrades all had the same cause: a level certified text or a contract file rather than behaviour. This decision writes the ladder and puts a human at each step, as LRN-007 requires. The rule about new implementations answers a question the 2026-09-03 external review raised: the old repository's D3 evidence cannot transfer to a rewrite that has never seen traffic.

## Adversarial review (2026-09-03)

### Steelman
A ladder with named evidence per rung and a minuted human step is the NASA TRL and canary discipline the FND-005 review invoked. It is cheap to operate and expensive to fake.

### Attacks
1. **Human graduation is bypassed under pressure.** Answered by LRN-007's review: the router mechanically refuses an unsigned artifact, so bypass requires forging a signature, which OPS-002 makes an incident.
2. **One reviewer "outside the team" is hard to find in a small group.** Answered: the reviewer may be the gateway team or security; the requirement is a different reporting line, not a different company.
3. **The no-inheritance rule throws away real evidence.** Answered: the evidence stays in the register attached to the old code; what it cannot do is certify new code. The old repository's measurements remain valid as config defaults (tokenizer ratios, cache-hit ratio) because those are facts about traffic, not about code.
4. **Parameter-only changes can smuggle behaviour changes.** Answered: the lightweight path is gated on unchanged version identifiers checked in CI (LRN-005), not on a description.

### Evidence
- ADRL-LRN-007; no autonomous promotion; graduation signs the manifest; lightweight path follow-up.
- ADRL-LRN-005; manifest v2 fields including the graduation record and policy compatibility.
- ADRL-FND-005; scope expands only through measured gates; the review's self-graded-gates attack citing NASA TRL and Google canarying.
- Google SRE, "Canarying Releases" (Site Reliability Workbook), as cited in `adr/SEM/README.md`; constrained-population exposure before general release (D4).
- `REVIEW-LOG.md`, register-wide rules; "A D-level certifies behaviour, not text."

### Verdict
**PROPOSED.** The ladder is the missing spine of the bucket; every maturity recommendation in the review assumed it. Needs an owner and the first minuted meeting.

## Follow-ups

- [ ] Publish the ladder in INDEX.md's preamble so every maturity field reads against it.
- [ ] Record in INDEX.md that adrl-core's decisions start at the level their own tests support (D1 or D2), independent of the register's claimed levels.
- [ ] Golden test: `load_graduated` refuses a manifest signed by the development key when `ADRL_ALLOW_DEV_KEYS` is unset (OPS-002).
- [ ] Hold the first graduation meeting on the deterministic heuristic's D2 to D3 move once shadow traffic exists; minute it in the register.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-07 | Linked proposed implementation roadmap and dependent decision questions | Prior decision and evidence preserved; no runtime or maturity change in this planning pass |
| 2026-09-03 | Proposed (first capture of the EVL bucket) |; |
