# ADRL milestone plan: Claude Code value first

Consolidated 9 September 2026. This is the current planning sequence, replacing conflicting reader-first, five-task/two-arm and token-only criteria in earlier planning overlays. Earlier wording is preserved in [the pre-consolidation snapshot](reviews/claude-code-roi-matrix-2026-09-09/milestone-plan-before-consolidation.md). Product direction is user-requested; expanded experiment budgets and concrete evaluation/access packets are proposals, not approvals or executed work. This consolidation is Codex planning synthesis, not a new Fable acceptance or full all-ADR audit.

## Destination and current position

Build a consumable ADRL integration for Claude Code that makes permitted model choices and demonstrates lower complete cost per verified acceptable task. Preserve shared routing/evidence contracts for other harnesses, but earn first-harness value before broad expansion. Subscription usage, estimated API-equivalent cost and actual metered savings are separate claims.

Current milestone: P1. RV-01 is the latest completed repair, qualified only on its recorded offline scope. Synthetic routing demonstrations and native observation exist; live ADRL-controlled task economics, learned routing and RSI remain unproved. No engineering slice has yet been consumed under the new six-slice planning budget. Automation remains paused.

The immediate path is P1 compatibility → P2 coding diagnostic → P2 confirmation and consumable preview. Planning-workload qualification follows the coding diagnostic as a separate track and must not delay the first coding result. P0 buyer discovery runs alongside the technical path. P3 adaptation, P4 reuse, P5 learning and P6/P7 improvement automation remain later evidence milestones.

## Milestones and gates

| Milestone | Product question | Deliverable and exit | Status |
|---|---|---|---|
| P0: buyer and spend discovery | Who benefits, controls spend and wants a trial? | Evidence of controllable workflow/spend; proposed three trial organizations and two budget owners | Planned, no completion established |
| P1: Claude Code compatibility | Can ADRL control a cheaper Claude route without breaking the workflow? | Bounded spike with dispatch attribution, thinking/tool continuation and an explicit supported profile or exact blocker | Next, not started |
| P2: coding diagnostic | Is there a concrete successful cheaper choice, and where does routing choose badly? | Six coding tasks, three arms, separate controls, one complete scorecard and continuation disposition | Proposed expanded packet |
| P2: planning diagnostic | Can routing reduce cost on planning artifacts without hiding quality loss? | Three planning tasks, three arms, independent assessment, separate scorecard | Later optional packet |
| P2: confirmation and consumable preview | Can users reproduce worthwhile benefit on unseen work? | Held-out confirmation, complete economics, reversible setup and supported-version declaration | Not started |
| P3: adaptation and constrained pilot | Does changing models during work help beyond the initial choice? | Initial-only versus transition-aware evidence, then applicable shadow/pilot qualification | Not started |
| P4: cross-harness reuse | Can a second harness reuse the intelligence and evidence contracts? | Qualified second harness, two-protocol gate and integrator usability evidence | Not qualified |
| P5: learned checkpoint | Does admitted experience yield a better policy than current rules? | Independent held-out evaluation, compatible signed checkpoint and rollback | Not demonstrated |
| P6–P7: automated improvement and RSI | Does improving the improvement process earn its own cost? | Equal-budget comparisons of resulting policies on fresh independent tasks | Not demonstrated |

These are evidence milestones, not interchangeable maturity grades. A P2 diagnostic can proceed with scoped manually verified evidence while broader P1 work remains open; it cannot be presented as P1 completion or product graduation.

## P1: compatibility spike and minimum experiment readiness

Prepare a small frozen packet for independent Fable challenge, identifying permitted deployment IDs, native subscription/authentication path, loopback binding, retained fields, synthetic input, cleanup, finite request/token limits, expected control behavior and stop conditions. Never print or retain credentials. Use existing subscription access; no silent API-key substitution, purchased credits or separate paid API usage.

Time-box actual spike execution and diagnosis to one hour after packet preparation. Force a cheaper permitted Claude deployment only for integration testing. Capture requested, selected and upstream-reported model with provenance, streaming completion, prior thinking followed by a tool/continuation request, and safe failure behavior. A first-turn answer does not prove switching compatibility. If only initial choice works, document that restricted profile and assess an initial-choice diagnostic separately; do not claim mid-session switching.

Inspect the existing non-frontier rewrite before using it for cheaper Claude: it strips thinking/output configuration, cache markers and some tool definitions. Required compatibility changes belong to FND/SEM/CAS, must be scoped, tested and independently reviewed, and must not relax privacy or permission rules. A forced choice is not evidence of estimator merit. If the profile cannot run, return the exact authentication, rewrite, signature, identity or model-availability failure and a bounded disposition, not an infrastructure expansion.

Before comparative execution, establish identical initial task trees, output capture, protected verifier inputs, meaningful model control and a declared transition policy. Freeze policy/configuration/model/harness versions, tool availability and effort configuration. Initial-choice comparisons keep the selected deployment fixed except explicitly permitted safety aborts; if existing cascade behavior cannot be held fixed safely, record that blocker or explicitly evaluate a different policy, never mislabel it initial-only. Trace all actual model calls and aborts.

For selector correctness, retain the constant-estimator sensitivity test and dated merit-rate measurement from the earlier plan. Disclose uncalibrated heuristics and middle-tier reachability. Recalibration must precede evaluation freeze and use separate development cases; no threshold tuning on diagnostic tasks. If the estimator contract fails, scope any diagnostic as current-policy baseline characterization and do not claim estimator-driven product readiness.

Learning readers are not prerequisites to manually reviewed diagnostic labels. Repair a reader now only if needed for execution correctness, trustworthy attribution or the chosen verifier. Learning stays off. Full reader/correction consistency, feature admission, calibration and automatic refresh remain gated for learning.

## P2: coding diagnostic

Use six independently authored tasks: small edit/formatting, test addition or repair, bug repair, multi-file refactor, mixed simple/complex instruction, and a synthetic concurrency or security-sensitive change. The implementer does not author evaluation tasks or reference answers. Domain-sensitive work needs reviewer-defined fault/adversarial checks beyond ordinary green tests. Use owned/approved repositories and keep fixtures isolated.

Three arms per task:

1. ADRL makes live decisions under the frozen current policy.
2. Fixed frontier deployment, within the same restrictions.
3. Fixed cheapest permitted available Claude deployment, within the same restrictions.

This is a proposed budget of 18 total top-level task-arm attempts, replacing the earlier ten only when the revised packet/budget is explicitly dispositioned. Failures/interruption consume attempts. Count lower-level calls and repairs under separately frozen limits. Do not silently reuse a frontier result when ADRL chooses frontier; independent runs expose variability and overhead. Randomize or counterbalance run order with a frozen seed and document cache conditions, session isolation and unavoidable differences.

Dry-check and retain the routing distribution before execution. At least two executable classes must select an available cheaper model for the intended contrast. Do not assume test work routes cheap. If the contrast is absent, stop before the matrix and reconsider selection; a revised policy requires fresh evaluation cases. Selecting a contrasting diagnostic sample limits representativeness and must be stated.

Keep two separate control families: restricted/private synthetic inputs, and long-context/cancellation/provider failures. Apply restrictions to all arms; no permitted destination means a clean block, never frontier bypass. Three restricted-policy checks expect zero disallowed upstream requests. Recovery controls test attribution, cancellation and duplicate effects; freeze their finite local fault matrix separately. Controls are not completed coding tasks and never enter savings or capability labels. An upstream-cost-bearing long-context test requires explicit inclusion in the run budget.

### Scorecard and cost contract

For each task/arm retain task hash, initial tree hash, final tree hash, policy/configuration hash, harness/model versions, decision/reason, actual upstream identity source, complete attempt/call IDs, verifier version and checks, quality verdict, usage by disjoint cache/input/output category, elapsed time, retries and attributable overhead. A final tree identifies an output; shared initial tree and task identity establish equivalent starts. An upstream-reported model is provider evidence, not independent infrastructure attestation.

The primary economic measure is complete rate-weighted task cost under a frozen dated rate basis, with actual metered charges separately where available. Avoid double-counting cache categories. Include failures, retries, routing and normal verification cost. Separate experiment-only baseline execution and research/review effort from steady-state service cost, and report both. Subscription invoices, reported tokens, quota observations and estimated API-equivalent dollars must not be conflated.

Proposed paired win: ADRL and frontier both satisfy all preregistered mandatory checks with no critical defect, and ADRL's complete weighted cost is strictly lower. Report measurement limits and absolute differences; a small positive difference only supports diagnostic continuation. Per-class pass checks, critical defects, latency limits and cost treatment must be concrete before runs. If charges or complete usage cannot be established, the corresponding claim is inconclusive.

Report every outcome, including frontier choices where fixed-cheap passed and cheaper choices that failed while frontier passed. Describe excess cost relative to the successful tested alternatives, not a global cheapest viable model or statistically established regret. Cost per accepted task includes unsuccessful assigned attempts; with no accepted tasks it is undefined, not zero.

### Go/no-go

Continue to a larger evaluation if ADRL actually chooses cheaper on at least two executable classes and at least one achieves the paired win. This is evidence of feasibility, not aggregate ROI. Publish aggregate quality/cost and losses even when the continuation bar passes. Reconsider if control fails, choices never differ, or every cheaper choice fails verification. Missing attribution/verification/cost means inconclusive. Preserve results; any retry needs a new bounded packet rather than replacing failed rows.

## P2: planning diagnostic, separately qualified

After the coding diagnostic, consider three independently authored tasks and three arms: PRD-to-ticket drafts, PRD generation and seeded architecture review. Proposed budget: nine additional task-arm attempts with its own approval and stop decision. Coding and planning results stay in separate scorecards, and a planning success cannot rescue a failed coding claim.

Ticket drafts: requirement traceability, useful acceptance criteria, meaningful dependencies, no unjustified duplication, and reviewer return-for-rework rate. Estimates may be unknown when source evidence is insufficient; do not reward invention. This generates files, not externally published Jira issues. PRDs: hard requirement checks plus blinded assessment of problem definition, tradeoffs, feasibility and measurable success. Architecture reviews: independently seeded defects scored by severity, with adjudication of false alarms and valid unseeded findings. Hide answer keys from task execution; freeze criteria without seeing outputs.

Freeze rubrics, judging order/seed, model masking, length reporting, disagreements and adjudication. Two independent human judges are proposed for stronger subjective claims but have not been appointed. Arun's two existing roles do not equal two independent judges. Agent assessments may be provisional and clearly labeled; agreement on three tasks is not calibrated evaluator reliability or human graduation. Collect later utility where available, such as ticket drafts surviving real grooming. No planning learning admission follows automatically.

## P2: confirmation, preview and investment evidence

A positive diagnostic funds a separately budgeted held-out evaluation, not an immediate release. Start from the roadmap's proposed 30 development tasks across at least three families and two repositories, then fresh confirmation tasks; size and repeats depend on variance and the predeclared claim, not an automatic 30-task sufficiency rule. Keep tuning and confirmation separate. Include practical fixed-model/current-workflow alternatives and all applicable EVL baselines; unavailable baselines stay explicit and cannot be waived by a successful small diagnostic.

Freeze an aggregate quality tolerance, minimum worthwhile cost reduction, eligible population, observation window, uncertainty method and full expense basis before confirmation. No numeric commercial hurdle is fabricated in this planning document. Show exclusions, overhead, failed attempts, changes in active human effort and both model efficiency and actual cash evidence. Without metered or invoice evidence, limit the claim to measured usage and modeled economics. Sunk development costs do not justify another run; account for future evaluation and operating costs in the continuation decision.

The consumable preview supplies reversible connection/setup, declared Claude Code/model compatibility, verified auth/billing path, visible decisions, usage/cost reporting, unsupported-state messages and safe rollback that preserves pins. Qualify all applicable safety/custody/admission controls before exposure. Native subscription feasibility is not proof that all subscribers or models are supported. Limited prototype experiments do not establish a broadly supported release.

## P0: discovery alongside engineering

Arun leads up to 12 discovery conversations, aiming for at least eight organizations, three concrete trial interests and two spend-controlling owners. At eight conversations with no plausible buyer, retarget; at twelve with no confirmed spend controller, stop and reconsider the segment. Record disconfirming evidence and existing alternatives. No agent outreach or external messages are implied. Distinguish subscription users seeking productivity/capacity from buyers with controllable metered spend.

## P3 through P7: earned expansion

P3 compares initial-only with trajectory-aware escalation and a separately admitted downshift policy. Freeze allowed signals, context carryover, switching/cache cost, quality and rollback. RTG-004/CAS-004/CAS-005 dispositions and current primary-paper applicability are required before downshift execution. An initial-only profile cannot claim transition safety. Proposed organic shadow and pilot windows require their own authority; dates and attempt floors never replace actual evidence.

P4 qualifies a second harness, proposed OpenCode, against shared task/evidence contracts; Responses/Codex needs separate protocol admission. Preserve the two-harness/two-protocol requirement before stable API claims. Test versions, identity, effective permissions, streaming, cancellation and integrator usability.

P5 repairs and qualifies learning readers/corrections, feature compatibility, verifier quality and evidence admission before training. Compare an approved checkpoint with incumbent/fixed baselines on unseen repositories, sessions and later periods. Existing MEM remains the foundation; graph retrieval must beat simpler retrieval after cost. Pin knowledge to source/evidence/harness versions. No cross-developer export without authorization; signed promotion and rollback remain external to the learner.

P6 automates failure grouping and proposals only if total improvement cost falls. P7 compares improvers under equal budgets and independent fresh evaluation. Neither may alter its own judge, holdout, permissions, privacy controls or release authority. RSI is optional: reject it if it adds no durable value.

## Register, maturity and review responsibilities

Keep architectural status, implemented behavior, tested scope and formal maturity separate. Evidence updates go into owning ADRs plus INDEX, bucket overviews and CHANGELOG. No maturity promotion from this plan, model agreement or synthetic tests. EVL-007 requires decision-scoped testing for D2, eligible organic shadow/outside-team review for D3, and actual pilot/graduation evidence for higher levels. Earlier grades must not transfer to this runtime automatically.

P1 hygiene remains unfinished: reconcile all 77 ADRs, verify reported stale rows/fields, implement the index/evidence checker, retain historical wording and disposition present-grade conflicts. It must not block a narrowly qualified diagnostic merely by being broad; affected misleading claims must be corrected before use, and unresolved applicable blockers remain binding. Full P1 completion still requires hygiene and its declared broader gates.

Ownership: Codex implements and prepares evidence; Claude Fable 5.1 independently challenges scoped plans and reviews frozen results; Arun is product owner and both named human evaluation/security reviewer, assisted by agents. Appointments do not sign unseen criteria. Later outside-team review is distinct. Historical self-assigned validated labels (RV-13) and W3.2b2d2 deviations (RV-29) remain pending owner disposition; preserve technical evidence without retroactive authorization or inherited acceptance. No blanket waiver follows from the pivot.

Each substantive packet gets pre-review, implementation/evidence, post-review, material-fix recheck and recorded disposition. Retain original findings and failed candidates. Max two correction/review rounds or a tighter packet limit. Unresolved blocking findings prevent the affected claim/exposure. Small documentation edits get proportionate checks; full all-ADR audits belong to explicit retrospective or graduation checkpoints.

## Effort limits and reporting

Retain the six-additional-attempted-engineering-slice ceiling; the compatibility spike counts. Intended allocation is compatibility, minimum necessary repair, selection/attribution readiness, coding matrix, results/review, and bounded contingency. This is a ceiling, not a promise each item fits one slice. Failed slices count. Do not spend the contingency automatically. At slice two, escalate absent access/criteria or a still-unresolved control blocker. At slice six without the complete coding diagnostic and disposition, stop and explicitly replan. The proposed target changes from ten diagnostic outcomes to the three-arm coding scorecard only when its revised budget is dispositioned; neither target relaxes safety or evidence requirements.

The current saved task-arm limit remains ten. Proposed replacement is 18 coding task-arm attempts plus separately enumerated controls; planning's nine are a later budget. Every packet specifies model-call/token/elapsed/repair limits and billing boundary before execution. Do not interpret subscription access as unlimited or guaranteed free capacity. No automatic scheduler restart.

After each slice, update the running journey with the product question, actual changes, raw evidence, failed/skipped attempts, Fable findings/disposition, affected ADRs, expenses, remaining budget and next gate. Keep [ADRL now](ADRL-NOW.md) short. The leadership view centers on actual choices, verified work and complete economics, not test counts.

## Sources and preserved context

- [Canonical product roadmap](adrl-product-roadmap-2026-09-08.md)
- [Implementation journey](adrl-implementation-journey.md)
- [Three-arm feedback assessment](reviews/claude-code-roi-matrix-2026-09-09/assessment.md)
- [RV-01 repair and evidence](reviews/outcome-contract-2026-09-09/report.md)
- [Historical owner decisions](reviews/milestone-tightening-2026-09-09/decisions.json)
- [Experiment lab](../design/adrl-experiment-lab-plan-2026-09-08.md)
- [Assessment extension](../design/adrl-lab-planning-and-assessment-2026-09-08.md)
- [Graduation rules](../adr/EVL/ADRL-EVL-007.md)
