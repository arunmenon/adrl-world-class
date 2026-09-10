# Next lab milestone: portable planning tasks with attributable assessment

8 September 2026. Task-pack preparation complete; execution implementation and
qualification remain open. This packet does not authorize paid runs or deployments.

## Product outcome

Run a PRD, HLD or LLD task through a qualified harness mode and inspect the exact
output, constraints, expert assessments, routing decisions and total effort. Later
use a second harness without changing the task definition or report format.

## Concrete starting point

The [starter contract](../lab/planning-starter-v1/contract.md) and three task packs
cover different domains: feature-rollout PRD, webhook-delivery HLD and inventory-
reservation LLD. [Assessment profile](../lab/planning-starter-v1/assessment.md) keeps
hard constraints, judgment and later usefulness separate. No task has run yet.

## Bounded delivery sequence

1. Resolve the contract against existing runtime task capture and experiment APIs;
   add only missing lifecycle/assessment contracts. Map owning ADRs before code.
2. Complete the existing W3 exact-output custody/capture prerequisite. Preserve
   original artifacts and attach assessments to their content identities.
3. Qualify the first Claude Code mode/profile, including document-output permission,
   stop behavior, credentials, model/protocol and finite per-run limits. Do not
   treat the mode name as proof of effective restrictions.
4. Run the three starter tasks once each as a diagnostic under that approved profile,
   accounting for every attempted/blocked/failed task. Have appropriate reviewers
   calibrate the draft rubric. This is not enough for model ranking or learning.
5. Add independent task variations and a separately qualified OpenCode adapter.
   Demonstrate common task/report reuse, then freeze a model-comparison matrix.

## Exit evidence and limits

The executable milestone needs actual input/output hashes, native and effective
mode records, attributable decisions where ADRL routed, receipt uncertainty, complete
attempt accounting and artifact-bound assessments. A schema or mock adapter alone
does not complete it. Original and amended assessments remain inspectable.

Planning task support must not imply subjective learning admission. LRN-001 and
MEM/EVL assessed-evidence disposition remain separate; current T1 rules and all
formal grades stay unchanged. Fixed-budget real execution and reviewer assignment
are prerequisites only for the dependent steps, not reasons to stop useful offline
implementation. The implementation heartbeat remains paused.

Owners: SEM-007, MEM-002/003/004, LRN-001/004/005, RTG-005, EVL-004/005/007.
Follow the existing maximum of three failed repair cycles for a bounded coding task.
Related [scope and evidence design](../../design/adrl-lab-planning-and-assessment-2026-09-08.md).
