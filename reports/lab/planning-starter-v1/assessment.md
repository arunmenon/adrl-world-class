# Assessment profile: planning-rubric-draft-v1

Prepared for calibration, not a qualified verifier. The author of these packs is
also the author of this rubric; there is no independent review or held-out set yet.

## Constraint checks

For every requirement ID, record `satisfied`, `violated` or `indeterminate`, with
the artifact passage and reason. Some checks can later be automated, such as schema
parsing or numerical arithmetic. Substantive traceability and logical consistency
initially require review. Presence of a heading or keyword is never proof of compliance.

Critical defects cannot be canceled by other scores: unauthorized access in the PRD;
cross-tenant leakage, prohibited payload handling or an exactly-once side-effect
promise in the HLD; overselling, cross-tenant access or duplicate stock release in
the LLD. Unknown evidence is indeterminate, not an automatic pass or capability failure.

## Expert-assessed dimensions

Score each task's five named dimensions independently:

- 0: contradicts supplied requirements or lacks usable evidence.
- 1: addresses the dimension partially; material gaps remain.
- 2: substantively sound; specific limited revisions are needed.
- 3: grounded and actionable, with important tradeoffs or uncertainties handled.

Require a supporting passage and explanation. These anchors are a starting draft;
calibrate them with examples before using numerical comparisons as evidence. Do
not average scores into an automatic acceptance threshold. Keep assessor disagreement,
confidence and critical defects visible. Concision is welcome; length is not rewarded.

## Calibration and review

Use two independent reviewers with relevant product/architecture/engineering
expertise on an initial calibration set. Hide model identity and randomize order.
Record disagreements before adjudication. A later LLM judge must be checked against
this reviewed set and known defective controls; record judge/prompt/rubric versions.
The generating model cannot certify its own work as objectively verified.

## Later usefulness

Record acceptance, human revision time, major revision count and implementation
findings separately from the first rubric assessment, linked to the exact artifact
version. Fix the implementer/environment when comparing plan utility experimentally;
otherwise state the confounds. Include generation and review costs when available.

All evidence from this starter pack remains curated synthetic. No human score,
document acceptance or LLM judge score automatically becomes T1 training evidence.
