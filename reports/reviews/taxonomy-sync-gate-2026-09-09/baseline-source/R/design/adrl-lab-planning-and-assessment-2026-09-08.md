# Planning modes and assessed deliverables in the ADRL lab

8 September 2026. Product requirement and proposed design extension. No runtime,
learning admission, ADR decision or maturity change is made by this document.

## The gap and the intended product

The current routing lab contains synthetic coding requests and scripted trajectories.
It has no real harness-mode matrix, PRD/HLD/LLD task pack or qualified subjective
assessment pipeline. General experiment accounting is a foundation; it is not proof
that these workloads are already supported.

The lab should evaluate planning and design as first-class deliverables as well as
coding. It should also evaluate multi-stage work: planning, design, implementation
and revision. A planning task can have high reasoning demands with no code-writing
permission. Do not equate read-only permissions with low difficulty or local routing.

## Keep the dimensions separate

An experiment profile should record:

- Task and phase: PRD, HLD, LLD, implementation, review or revision.
- Native harness/version and its native agent/mode identifier.
- Effective permissions: source reads/writes, document output, shell, network and
  tools, including any approved exceptions and mode changes during execution.
- Provider/model deployment, revision or alias uncertainty, reasoning settings,
  context limits, protocol and supported tool behavior.
- Input context snapshot, artifact versions, output identity and evaluation profile.

This is a proposed contract, not a claim that the current runtime interaction_mode
enum already encodes native Plan/Build modes. Adapter evidence must identify actual
mode and permissions; a prompt containing the word “plan” is insufficient.

Claude Code documents Plan as a permission mode. OpenCode documents Build and Plan
agents with configurable model, prompt and tool permissions. Their semantics are
not interchangeable merely because the names match. Pin the tested version/config
and effective capabilities. Sources: [Claude Code modes](https://code.claude.com/docs/en/permission-modes),
[OpenCode agents](https://opencode.ai/docs/agents).

Planning quality, model availability and native harness compatibility are separate
questions. Admit only tested combinations. Mark an unsupported combination explicitly;
do not silently switch mode or widen permissions. Document generation may require
an authorized output path or external capture even when source edits are forbidden.

## Task families and the evidence they need

| Deliverable | Input and objectively checkable elements | Assessed quality |
|---|---|---|
| PRD | Stakeholder brief, source evidence, constraints, traceable requirements and measurable acceptance criteria | Prioritization, problem framing, useful scope, ambiguity handling and decisions needed |
| HLD | Approved requirements, existing architecture, interface facts, capacity calculations and mandatory security/reliability constraints | Decomposition, tradeoffs, feasibility, failure handling and evolutionary cost |
| LLD | Approved HLD, repository/API/schema snapshots, interface contracts and testable invariants | Implementability, edge cases, maintainability and consistency of detailed choices |
| Plan then implement | Frozen plan plus starting repository, allowed tools and common implementation checks | Plan usefulness, downstream defects, rework and total effort |
| Review and revise | Frozen artifact, specified review findings and unchanged requirements | Whether revision resolves findings without introducing new contradictions |

Include clear, ambiguous, conflicting, incomplete and stale-context briefs. Vary
greenfield versus existing systems, task scope, domains and languages. Omitted
information may require a question or an explicitly labeled assumption, not a
confident invention. Evaluate planning-only outputs separately from their later use.

## Pluggable evaluation without pretending judgment is a unit test

An evaluation profile should combine three distinct channels:

1. Deterministic checks for what can actually be checked: schema validity, internal
   references, known constraints, numerical calculations and executable examples.
   Required headings alone establish format, not substantive completeness.
2. Rubric-based expert assessment for judgment. Freeze dimensions and anchored
   examples before comparison. Keep dimension scores, evidence spans, reasons,
   missing information and critical defects. Permit ties, uncertainty and disagreement.
3. Later utility evidence: review effort, revisions, downstream implementation and
   defects, attributed to the exact artifact used. This is delayed and affected by
   the implementer and environment; do not attribute all downstream differences to
   the planning model. Hold these factors fixed in controlled comparisons when possible.

Initially calibrate on a small, diverse set reviewed independently by two relevant
humans, with disagreement resolution and recorded agreement. Blinding model identity
and randomizing presentation order reduce avoidable evaluation confounds. Record
rubric version, reviewer identity/role, artifact hash, context, date and reasons.

LLM judges can assist with triage and rubric suggestions, but a single uncalibrated
judge is not the authority. Evaluate against the human calibration set, swap pairwise
order, inspect verbosity/style effects, include known strong and defective examples,
and retain disagreement. Version the judge model and prompt as well as the rubric.
The [MT-Bench/Chatbot Arena judge study](https://arxiv.org/abs/2306.05685) documents
position, verbosity and self-enhancement biases; judge quality needs its own evidence.

Do not let a high style score cancel a violated mandatory requirement. For example,
an HLD that contradicts a supplied data-residency constraint has a critical defect
even if it is well written. Keep acceptance and release decisions separate from
individual assessment scores.

## What routing should learn from these tasks

The target is useful, accepted work for its total cost and time, including review
and revision effort. It is not the longest document, most polished prose or highest
self-awarded score. A cheaper draft requiring extensive expert repair may be more
expensive overall. Phase-specific routing is a hypothesis to test, not a fixed rule
that planning must use frontier or implementation must use local.

Compare both fixed model/deployment profiles and routing-policy profiles. For
multi-stage experiments preserve phase-specific artifacts, mode changes, decisions
and costs, and use permitted transition boundaries. This proposal does not amend
CAS stickiness or authorize arbitrary mid-session downshifts.

MEM should preserve the context, exact artifact, assessments and later corrections
as attributable evidence. A context-graph projection may connect requirements,
design decisions, review findings and later outcomes. Evaluate any graph benefit
against the same tasks without that projection; do not assume graph storage improves
decisions. LRN must use only information available before the route being learned.

## Taxonomy disposition required before learning admission

LRN-001 currently restricts the estimator objective to deterministically verified,
cause-typed, final, organic T1 evidence. MEM-003 defines deterministic verification;
MEM-004 forbids defaulting uncertain causes to capability failure. Human preference
or an LLM rating does not automatically satisfy these contracts. Lab-generated PRDs
remain lab-origin evidence even if a human accepts them.

Propose a separately typed assessed-evidence contract before using such scores as
learning targets. It must define reliability, eligible uses, reviewer/judge calibration,
uncertainty, auditability, delayed corrections and release gates. Do not overload
verified=true or relabel evidence to fit existing T1 rules.

Owners for disposition: SEM-007 (native mode/profile capabilities); LRN-004/005
(decision-time features and versions); MEM-002/003/004 (assessment, corrections and
cause attribution); LRN-001/003 (objective and admission); RTG-005 (quality, review cost
and latency); EVL-004/005/007 (evidence quality, origin and scoped maturity). Status
and maturity remain unchanged pending disposition and implementation.

## Bounded next deliverable

Extend the proposed shared task contract with task phase, deliverable type,
native/effective mode and evaluation profile. Prepare one small PRD, HLD and LLD
task pack with fixed inputs, hard constraints and review rubrics. Qualify the first
harness/mode and then a second adapter using unchanged task/evaluation contracts.
Real runs retain the existing output-capture, isolation and finite-budget prerequisites.
Initially publish assessed evidence separately, without training admission.

This extends the [experiment lab plan](adrl-experiment-lab-plan-2026-09-08.md) and
[product roadmap](../reports/adrl-product-roadmap-2026-09-08.md); it is not completed
support for planning artifacts or subjective learned routing.
