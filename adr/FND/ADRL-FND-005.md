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
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Approved unchanged | "Scope expands only through measured phase gates; component presence is not readiness." |
