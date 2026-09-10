# PRD task: controlled feature rollout

This is a fictional product brief. Produce `prd.md` for an initial feature-rollout
capability in an existing SaaS application. Plan the product; do not implement it.
Use only the supplied facts. Label assumptions and unresolved decisions explicitly.

## Supplied facts

- The application serves 200 business tenants. Each tenant has administrators and
  ordinary members. Existing authentication already provides tenant and role IDs.
- Product operators currently ask an engineer to enable or disable a feature for
  a tenant. Requests are tracked informally and rollbacks are slow.
- Release one must allow an authorized internal operator to enable/disable a named
  feature for selected tenants. Ordinary members cannot change rollout state.
- Feature evaluation already exists in the application; this project manages its
  configuration, not a new experimentation or SDK platform.
- A disable action must reach the evaluation layer within 60 seconds under normal
  operation. Define how the team will measure this requirement.
- Operator actions must identify who changed what and when. Tenant A must not see
  tenant B's configuration. Avoid adding customer personal data to the audit record.
- Two engineers are available for six weeks. Percentage rollouts, experimentation
  analytics and customer self-service are outside release one.
- Interview evidence, existing request volume and baseline rollback time have not
  been supplied. Do not invent them or claim a measured financial benefit.

## Required deliverable

Write a decision-ready PRD covering the problem, users, workflows, scope/non-goals,
requirements with stable IDs, measurable acceptance criteria, success measures,
risks, rollout approach and open questions. Distinguish supplied requirements from
your proposed choices. Avoid prescribing a technology stack without a product need.

Evaluation identifiers: PRD-1 scope, PRD-2 authorization/isolation, PRD-3 propagation,
PRD-4 audit/minimization, PRD-5 grounded assumptions. Word count is not a quality metric.
