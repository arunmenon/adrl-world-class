# Codex initial reconciliation of the Fable review

8 September 2026. This is a first source-backed triage, not completion of all forty dispositions or a fix wave.

## Product conclusion

The central criticism is justified: we have not demonstrated outcome-driven adaptive routing on real tasks. Instrumentation and isolated component tests did not establish that the composed learning loop worked. The outcome producer/consumer mismatch is a genuine integration defect. The estimator fallback and path-dependent diagnostic configuration also need correction. Passing 911 local tests was evidence about those tests on that checkout, not proof of an effective adaptive router.

The next engineering priority should be one complete, attributable decision/outcome path, then routing-selection and portable-lab correctness, then a controlled real-task comparison. Further graph, subjective-task and multi-harness expansion should not obscure those prerequisites. This is a sequencing recommendation, not a runtime change or new experiment authorization.

## Evidence checked directly

- C/src/adrl/cascade/controller.py `_event` and state-valued producers versus C/src/adrl/ledger/outcomes.py `project_outcome` and `routes_in_state`: mismatched outcome contract.
- C/src/adrl/routing/router.py `decide` and `_advise`: selected estimator rung is passed into the advisor but discarded without a classifier.
- C/tools/run_routing_lab.py `execute` and C/config/repo-classification-v1.json: absolute-path identity and SHADOW loading for LIVE diagnostic components.
- C/src/adrl/routing/rule_health.py and learning/tiers.py: divergent health-event shape and missing correction event declaration.
- R/adr/EVL/ADRL-EVL-007.md: new-runtime historical-grade transfer restriction.
- R/reports/waves/w0-baseline.md: explicit technical-self-review scope and reviewer-dependent release/graduation gate.

No runtime tests were executed by Codex in this reconciliation; reviewer reproductions remain attributed to the reviewer. No source code or historical ADR fields were edited.

## Where I disagree or require qualification

RV-13 conflates local engineering validation with formal independent graduation. The W0 packet explicitly permitted the former while holding the latter. I accept that our completion language needed to make this clearer; I do not accept that the actual passing checks are thereby invalid. The reviewer must reconsider the blanket scope; its blocking designation remains preserved.

RV-02's minimum middle-tier rate is not enough: routing must respond to the declared objective and ultimately verified comparative quality/cost, not a desired distribution. RV-10's observation-plus-capture route needs proof of actual routing control; observing a native harness does not itself let ADRL select the model. The proposed first repair slice bundles event repair, verifier precision and learning-contract admission; these should have separable acceptance gates. Repeated verification runs alone do not establish verifier accuracy against independent ground truth.

Historical grades should be labelled as historical and current implementation assessed separately. We should neither carry them forward unqualified nor mechanically adopt the reviewer's 77 suggested assessments as formal maturity changes.

The review's 98 not-reviewed files and inconsistent coverage description mean it is broad but not exhaustive. These limits do not negate the concrete defects. List-price CLI telemetry is not verified subscription spend, and a session_ identifier from an external Claude session must be validated before attempting local CLI resume.

## Handoff state

All forty rows now have an author triage response. Only the explicitly accepted rows were accepted; the rest remain unresolved or disputed. No issue is marked fixed. Original findings, original table and reviewer status are preserved. The next action is to finish targeted evidence verification and prepare the smallest event-contract repair packet for independent pre-wave review, keeping other open defects visible. Real-harness exposure, reviewer appointments and formal grade decisions retain their existing gates.
