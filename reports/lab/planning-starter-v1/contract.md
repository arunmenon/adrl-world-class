# Shared planning-task contract, draft v1

8 September 2026. Prepared specification, not a runtime API or qualified harness.

A task pack is independent of the harness and model. Its identity includes the
brief, supplied facts, required output, constraints and evaluation profile. Changing
any of these creates a new pack version. `manifest.json` fingerprints this package.

## Task definition

`tasks.json` supplies task ID, deliverable type, input brief, output filename,
requirement IDs, critical defects and rubric dimensions. All three tasks are
curated synthetic work; learning eligibility is false. They have different domains,
but three author-created examples do not establish representative task diversity.

## Execution profile, required before running

Resolve the task against a separate execution profile containing:

- Harness binary/version, adapter ID/version, native agent/mode, actual prompt/tool
  configuration and the evidence that the adapter can control or observe routing.
- Effective permissions for reading inputs, writing only the document output,
  shell/network use and any mode transition. Do not infer them from a mode name.
- Model deployment, protocol profile, revision or moving-alias uncertainty,
  reasoning/sampling settings and context limits.
- Isolated starting workspace identity, output custody/capture mechanism,
  per-attempt wall time, token/spend limits and stop behavior.

The initial profile is unresolved. No Claude Code, OpenCode or Responses execution
is represented as qualified. No model or paid-call budget is granted by this pack.

## Common result, proposed fields

Capture experiment/task/profile/attempt IDs, exact input and output identities,
start/end/state, observed mode changes, actual ADRL route IDs when they exist,
dispatch/receipt provenance, resource usage and review effort. A harness-only run
must not fabricate an ADRL routing decision. Every planned arm remains accounted
for when blocked, unsupported, failed, interrupted or indeterminate.

Separate `constraint_checks`, `expert_assessments` and `later_utility_observations`.
Each assessment identifies the artifact hash, rubric version, assessor, supporting
passages, uncertainty and date. Corrections append a superseding assessment. Do
not put a rubric score into a deterministic verification flag or T1 capability label.

## Comparison and portability

First compare model choices within the same qualified harness/mode and task input.
Then compare two harnesses as complete systems using the same task pack and shared
reporter. Preserve native differences and unsupported capabilities explicitly.

The portability acceptance test is two actual adapters using these unchanged task
definitions and evaluation profiles. A second adapter enum or simulated native
mode does not pass that test. Multi-stage plan-to-build comparisons are a later
extension; these three initial tasks produce standalone documents.
