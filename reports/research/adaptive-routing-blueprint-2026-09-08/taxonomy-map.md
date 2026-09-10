# ADRL target architecture: coverage of all 77 decisions

8 September 2026. Planning map; current decision wording and grades remain in force. Proposed dispositions below require the blueprint discussion before implementation. This is not a new 77-decision scientific review.

| Decision | Product responsibility | Proposed disposition |
|---|---|---|
| [ADRL-CAS-001: Deterministic trip-wires, with measured coverage](../../../adr/CAS/ADRL-CAS-001.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-CAS-002: Typed failures, versioned enum, measured attribution](../../../adr/CAS/ADRL-CAS-002.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-CAS-003: Action boundary defined; no re-issue after side effects](../../../adr/CAS/ADRL-CAS-003.md) | Execution, switching and recovery | Clarify initial versus safe-boundary decisions |
| [ADRL-CAS-004: Cross-model handoff: provider-pair rules, not one stripping rule](../../../adr/CAS/ADRL-CAS-004.md) | Execution, switching and recovery | Qualify deployment capabilities and transition edges |
| [ADRL-CAS-005: Sticky escalation within an episode](../../../adr/CAS/ADRL-CAS-005.md) | Execution, switching and recovery | Keep baseline; experiment before changing stickiness |
| [ADRL-CAS-006: Record the served model, not only the served rung](../../../adr/CAS/ADRL-CAS-006.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-CAS-007: Terminal failure surfaced; ADRL owns zero retries](../../../adr/CAS/ADRL-CAS-007.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-CAS-008: Escalation scope under subagents](../../../adr/CAS/ADRL-CAS-008.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-CAS-009: Action-effect provenance and authorization boundary (Proposed)](../../../adr/CAS/ADRL-CAS-009.md) | Execution, switching and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-001: Baseline set: four fixed comparators, two price bases](../../../adr/EVL/ADRL-EVL-001.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-002: Holdout and calibration protocol: temporal, session-grouped, tier-1 only](../../../adr/EVL/ADRL-EVL-002.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-003: Branch protocol and replay prohibition](../../../adr/EVL/ADRL-EVL-003.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-004: Label quantity and quality gate for retrieval and learned authority](../../../adr/EVL/ADRL-EVL-004.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-005: Simulator and benchmark evidence is not organic evidence](../../../adr/EVL/ADRL-EVL-005.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-006: Offline evaluation against baselines, branched or propensity-weighted](../../../adr/EVL/ADRL-EVL-006.md) | Comparison, graduation and independent assessment | Version improvers; preserve independent graduation |
| [ADRL-EVL-007: Explicit human graduation and the D2 to D5 ladder](../../../adr/EVL/ADRL-EVL-007.md) | Comparison, graduation and independent assessment | Version improvers; preserve independent graduation |
| [ADRL-EVL-008: Scorecard format: every number with its denominator, window and exclusions](../../../adr/EVL/ADRL-EVL-008.md) | Comparison, graduation and independent assessment | Retain current contract; implement/qualify within its existing scope |
| [ADRL-EVL-009: Blockers are never averaged away](../../../adr/EVL/ADRL-EVL-009.md) | Comparison, graduation and independent assessment | Version improvers; preserve independent graduation |
| [ADRL-FND-001: Transparent control layer, protocol-scoped](../../../adr/FND/ADRL-FND-001.md) | Product boundary and authority | Retain current contract; implement/qualify within its existing scope |
| [ADRL-FND-002: Semantic policy vs mechanical execution, rung-closed](../../../adr/FND/ADRL-FND-002.md) | Product boundary and authority | Retain current contract; implement/qualify within its existing scope |
| [ADRL-FND-003: Routing boundary is the user turn](../../../adr/FND/ADRL-FND-003.md) | Product boundary and authority | Clarify initial versus safe-boundary decisions |
| [ADRL-FND-004: Fail to last-known-safe, not fail-open](../../../adr/FND/ADRL-FND-004.md) | Product boundary and authority | Retain current contract; implement/qualify within its existing scope |
| [ADRL-FND-005: Scope expands only through measured gates](../../../adr/FND/ADRL-FND-005.md) | Product boundary and authority | Version improvers; preserve independent graduation |
| [ADRL-LRN-001: Evidence tiers, not "outrank"](../../../adr/LRN/ADRL-LRN-001.md) | Policy learning and improver candidates | Retain current contract; implement/qualify within its existing scope |
| [ADRL-LRN-002: Branched pairs, plus a logged-exploration channel](../../../adr/LRN/ADRL-LRN-002.md) | Policy learning and improver candidates | Retain current contract; implement/qualify within its existing scope |
| [ADRL-LRN-003: The target is a CATE, name it](../../../adr/LRN/ADRL-LRN-003.md) | Policy learning and improver candidates | Align complete-task objective and cost |
| [ADRL-LRN-004: Pre-decision features, enforced by construction](../../../adr/LRN/ADRL-LRN-004.md) | Policy learning and improver candidates | Retain current contract; implement/qualify within its existing scope |
| [ADRL-LRN-005: Every artifact is fully versioned](../../../adr/LRN/ADRL-LRN-005.md) | Policy learning and improver candidates | Version improvers; preserve independent graduation |
| [ADRL-LRN-006: Abstention with a declared risk-coverage target](../../../adr/LRN/ADRL-LRN-006.md) | Policy learning and improver candidates | Retain authority gates; specify measured refresh |
| [ADRL-LRN-007: No autonomous online promotion](../../../adr/LRN/ADRL-LRN-007.md) | Policy learning and improver candidates | Version improvers; preserve independent graduation |
| [ADRL-LRN-008: Logged exploration in the ambiguous band](../../../adr/LRN/ADRL-LRN-008.md) | Policy learning and improver candidates | Retain current contract; implement/qualify within its existing scope |
| [ADRL-MEM-001: Append-only ledger keyed by route_id](../../../adr/MEM/ADRL-MEM-001.md) | Attributable outcomes and evidence custody | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-MEM-002: Three-state outcome lifecycle with defined close](../../../adr/MEM/ADRL-MEM-002.md) | Attributable outcomes and evidence custody | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-MEM-003: Verification enriches, never overwrites](../../../adr/MEM/ADRL-MEM-003.md) | Attributable outcomes and evidence custody | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-MEM-004: Cause-typed labels, six types not four](../../../adr/MEM/ADRL-MEM-004.md) | Attributable outcomes and evidence custody | Retain current contract; implement/qualify within its existing scope |
| [ADRL-MEM-005: Prompt-derived artefacts are prompt-class data](../../../adr/MEM/ADRL-MEM-005.md) | Attributable outcomes and evidence custody | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-MEM-006: Memory facade, fail-safe but never silent](../../../adr/MEM/ADRL-MEM-006.md) | Attributable outcomes and evidence custody | Retain current contract; implement/qualify within its existing scope |
| [ADRL-MEM-007: Projections are rebuildable and versioned](../../../adr/MEM/ADRL-MEM-007.md) | Attributable outcomes and evidence custody | Retain current contract; implement/qualify within its existing scope |
| [ADRL-MEM-008: Retrieval stays advisory until gated](../../../adr/MEM/ADRL-MEM-008.md) | Attributable outcomes and evidence custody | Retain authority gates; specify measured refresh |
| [ADRL-MEM-009: Counterfactuals bind only to explicit route_id](../../../adr/MEM/ADRL-MEM-009.md) | Attributable outcomes and evidence custody | Retain current contract; implement/qualify within its existing scope |
| [ADRL-MEM-010: Retention and erasure of ledger and derived artefacts](../../../adr/MEM/ADRL-MEM-010.md) | Attributable outcomes and evidence custody | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-OPS-001: Multi-worker consistency and the single-process constraint](../../../adr/OPS/ADRL-OPS-001.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-002: Key custody and rotation](../../../adr/OPS/ADRL-OPS-002.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-003: Endpoint inventory, rollout and change control](../../../adr/OPS/ADRL-OPS-003.md) | Versioned operation, drift and recovery | Specify drift and requalification |
| [ADRL-OPS-004: Backup, restore and erasure](../../../adr/OPS/ADRL-OPS-004.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-005: Shadow-mode semantics per subsystem](../../../adr/OPS/ADRL-OPS-005.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-006: Record the served identity, not the intended one](../../../adr/OPS/ADRL-OPS-006.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-007: Audit-anchor availability, rollback and incident response](../../../adr/OPS/ADRL-OPS-007.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-OPS-008: Fail-open SLOs, alerting and bypass audit](../../../adr/OPS/ADRL-OPS-008.md) | Versioned operation, drift and recovery | Retain current contract; implement/qualify within its existing scope |
| [ADRL-RTG-001: Three capability rungs with measured boundaries](../../../adr/RTG/ADRL-RTG-001.md) | Initial and temporal routing choices | Qualify deployment capabilities and transition edges |
| [ADRL-RTG-002: Cheapest rung likely to complete, defined](../../../adr/RTG/ADRL-RTG-002.md) | Initial and temporal routing choices | Align complete-task objective and cost |
| [ADRL-RTG-003: Rules own clear cases, measured](../../../adr/RTG/ADRL-RTG-003.md) | Initial and temporal routing choices | Retain authority gates; specify measured refresh |
| [ADRL-RTG-004: Local-first only with a bounded, clean cascade](../../../adr/RTG/ADRL-RTG-004.md) | Initial and temporal routing choices | Keep baseline; experiment before changing stickiness |
| [ADRL-RTG-005: Objective: verified quality, retry, latency, session cost](../../../adr/RTG/ADRL-RTG-005.md) | Initial and temporal routing choices | Align complete-task objective and cost |
| [ADRL-RTG-006: Advisory LLM classifier, gated and bounded](../../../adr/RTG/ADRL-RTG-006.md) | Initial and temporal routing choices | Retain authority gates; specify measured refresh |
| [ADRL-RTG-007: Marginal-utility target, with a build gate](../../../adr/RTG/ADRL-RTG-007.md) | Initial and temporal routing choices | Clarify initial versus safe-boundary decisions |
| [ADRL-RTG-008: Rung vs endpoint, with a leak contract](../../../adr/RTG/ADRL-RTG-008.md) | Initial and temporal routing choices | Qualify deployment capabilities and transition edges |
| [ADRL-RTG-009: Session-marginal, cache-aware cost accounting](../../../adr/RTG/ADRL-RTG-009.md) | Initial and temporal routing choices | Align complete-task objective and cost |
| [ADRL-SAF-001: Hard gates first, on every request](../../../adr/SAF/ADRL-SAF-001.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-002: One-way pin, durable, lineage-scoped, audited release](../../../adr/SAF/ADRL-SAF-002.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-003: Secret detection per request, precision-measured](../../../adr/SAF/ADRL-SAF-003.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-004: Pinned sessions fail loudly, in the harness's dialect](../../../adr/SAF/ADRL-SAF-004.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-005: Block, and make the block recoverable](../../../adr/SAF/ADRL-SAF-005.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-006: Infeasible rungs removed before optimisation](../../../adr/SAF/ADRL-SAF-006.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-007: Verification runs sandboxed, then diffed](../../../adr/SAF/ADRL-SAF-007.md) | Hard restrictions and safe execution | Scope evidence infrastructure to trustworthy routing outcomes |
| [ADRL-SAF-008: Repository and data-class gate (Proposed)](../../../adr/SAF/ADRL-SAF-008.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SAF-009: Egress ledger and gate-audit integrity (Proposed)](../../../adr/SAF/ADRL-SAF-009.md) | Hard restrictions and safe execution | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-001: Mechanical classification of request classes](../../../adr/SEM/ADRL-SEM-001.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-002: Session key from wire headers, then metadata](../../../adr/SEM/ADRL-SEM-002.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-003: Continuations inherit the sticky route](../../../adr/SEM/ADRL-SEM-003.md) | Harness state and decision boundaries | Clarify initial versus safe-boundary decisions |
| [ADRL-SEM-004: Utility calls split by content exposure](../../../adr/SEM/ADRL-SEM-004.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-005: Episode boundaries, enumerated and measured](../../../adr/SEM/ADRL-SEM-005.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-006: Subagents inherit constraints now, routing later](../../../adr/SEM/ADRL-SEM-006.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-SEM-007: Protocol profiles (Proposed)](../../../adr/SEM/ADRL-SEM-007.md) | Harness state and decision boundaries | Retain current contract; implement/qualify within its existing scope |
| [ADRL-TRU-001: Authenticated workload identity (Proposed)](../../../adr/TRU/ADRL-TRU-001.md) | Authenticated identity and permitted destinations | Retain current contract; implement/qualify within its existing scope |
| [ADRL-TRU-002: Permitted deployment set (Proposed)](../../../adr/TRU/ADRL-TRU-002.md) | Authenticated identity and permitted destinations | Qualify deployment capabilities and transition edges |
| [ADRL-TRU-003: Egress anchoring (Proposed)](../../../adr/TRU/ADRL-TRU-003.md) | Authenticated identity and permitted destinations | Retain current contract; implement/qualify within its existing scope |
