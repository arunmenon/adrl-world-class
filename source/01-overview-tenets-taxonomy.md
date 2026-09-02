# ADRL — Overview, Design Tenets, Taxonomy & Maturity Model

## What ADRL is, in one paragraph

ADRL is a transparent control layer between the coding harness (Claude Code / Codex CLI) and model execution. It decides **which model capability rung** should serve a piece of work — free local, cheap cloud, or frontier — while LiteLLM continues to own the concrete model endpoint, provider, retry and transport. The goal is to cut cloud spend and keep data local where possible **without the developer feeling a quality drop**.

**Architectural agreement is independent of implementation maturity.** Every decision carries two separate attributes: Status (Accepted / Proposed) and Maturity (D0–D5: Design → Code → Tested → Shadow → Pilot → Graduated).

**Current posture:** deterministic and heuristic routing has shadow-grade evidence; the **learned router is design-stage and deliberately not authorised** to make decisions. Live routing is gated.

## Design Tenets

1. **Route turns, not HTTP requests.** A user task generates many tool and continuation requests. The router decides at the start of a user turn; continuations inherit the route to preserve context and prompt caches.
2. **Safety and feasibility precede optimization.** Privacy pins, secret detection, context limits, health and policy constraints are hard gates. Heuristics or ML cannot override them.
3. **Local-first, conditionally.** Use the cheapest healthy model likely to complete the task — not local at all costs. Hard tasks can go directly to frontier; easy tasks use local with escalation armed.
4. **Deterministic rules own clear cases.** Learned routing is reserved for the ambiguous middle. The learned system advises; it is not the safety authority.
5. **Escalation is mechanical and boundary-safe.** Trip-wires detect failures such as tool errors, loops or invalid output. Escalation occurs at an action boundary, with transcript handoff and no blind replay of partial tool execution.
6. **State is sticky within an episode.** Once a task escalates it stays elevated until a conservative episode boundary permits lowering the rung. No oscillation between rungs inside a task.
7. **Separate capability choice from endpoint choice.** ADRL chooses a capability rung. LiteLLM chooses the concrete model endpoint, provider, retry and transport.
8. **Evidence must be cause-clean and provenance-aware.** Outcomes distinguish task difficulty from infrastructure, dialect, privacy and policy failures. Every decision is tied to an immutable `route_id`; shadow, organic, simulator and counterfactual data remain separate and are never pooled.
9. **Learning cannot self-promote.** Learned policies require versioned features, calibration, holdouts, baseline comparisons, shadowing, canaries, rollback and explicit graduation.

## The nine buckets

| Code | Bucket | Core question | Owns | Does not own |
|---|---|---|---|---|
| FND | System Boundary and Principles | Who owns what, and what invariants govern the system? | Product boundary, control-plane ownership, invariants, architectural shape | Individual routing thresholds or model training |
| SEM | Interaction Semantics | What does this request or interaction mean? | Request, turn, continuation, session, episode, utility call and subagent meaning | Which model wins for a classified turn |
| SAF | Safety, Privacy, Hard Constraints | What is forbidden or infeasible? | Non-negotiable gates, secret handling, feasibility, blocking, protected resources | Quality optimisation inside the allowed set |
| RTG | Routing Intelligence and Economics | Which permitted rung is the best choice? | Runtime choice of rung, utility, cost, uncertainty, policy precedence | How a chosen rung executes, or how models are trained |
| CAS | Execution, Cascade, Recovery | How is the choice executed, retried or escalated? | Dispatch, trip-wires, escalation, context transfer, stickiness, fallback | Initial semantic classification or long-term learning |
| MEM | Memory, Evidence, Label Integrity | What happened, and can we trust the record? | Decision/outcome ledger, lifecycle, retrieval evidence, provenance, label correctness | Choosing a route directly, or training a model |
| LRN | Learning and Adaptation | How do we learn a better policy? | Training data, targets, features, calibration, artifacts, retraining, abstention | Live rollout approval or hard safety gates |
| EVL | Evaluation, Graduation, Rollout | Is the behaviour ready for more exposure? | Baselines, holdouts, scorecards, exit gates, shadowing, canaries, readiness claims | Runtime business logic |
| OPS | Platform, Runtime, Operations | How is the system operated, observed and rolled back? | State backends, health, observability, CI, budgets, deployment, rollback, operator controls | Semantic routing policy |

Flow: SEM → SAF → RTG → CAS → MEM → (LRN, EVL). OPS supports every stage. FND defines the boundary and invariants.

## Maturity scale

| Level | Name | Meaning |
|---|---|---|
| D0 | Design | Decided on paper. No implementation. |
| D1 | Code | Implemented, not yet systematically tested. |
| D2 | Tested | Unit/integration/fault tests pass. |
| D3 | Shadow | Runs against real traffic without affecting execution. |
| D4 | Pilot | Affects execution for a constrained population. |
| D5 | Graduated | Approved for general production use. |

## Evidence & Readiness (summary)

Phase 0 (shadow/evidence-gathering) complete. Phase 1 engineering substantially built, exit criteria not met. Live adaptive routing intentionally blocked. Learned routing not trained, not authorised. No decision at D5.

Phase 0 findings: never-switch-mid-turn vindicated (prompt-cache hit ratio on real traffic very high); router overhead negligible; most decisions made by simple rules (learned/ambiguous band is a minority); five design assumptions met reality and every correction simplified the design (session keying via metadata.user_id; tool-ID handling); a best-single-model cost baseline exists.

Explicit non-claims: corpus is single-user, workflow-heavy, subagent work effectively free at margin (directional findings usable, magnitudes not); local-rung reliability on realistic code NOT established (only small edit ops on small files; mixed-whitespace exact-string edit dialect untested on production model); cost figures are upper bounds and asymmetric (cache pricing); no adversarial evidence for the safety gates (tested, not attacked); simulator evidence ≠ organic evidence (EVL-005).

Blocking gates: organic verifier labels, label precision, learned-router authority. Blockers never averaged away (EVL-009).

Bucket maturity strongest→weakest: FND → SEM → OPS → CAS → RTG → SAF → MEM → EVL → LRN.

Known code-reality facts (from Codex walkthrough of `cc-local` repo, 2026-09-02):
- MEM is SQLite (`router-memory.db`, tables decisions/outcomes/outcome_events/embeddings), behind a facade with a NullProvider fallback; embeddings via local embedding model + NumPy in-memory index; no vector DB.
- Failure types in `outcomes.py`: task_capability, harness_dialect, infrastructure, policy_constraint, user_abort, unverifiable.
- Only ONE task has strong test-based verification. Similar-task lookup has 34 evaluated decisions vs required 300. Session-to-route tracking is held in a Python dict (single-process). Automatic verification not connected to every eligible task.
- Graph-lite (`graph_lite.py`) exists and is tested but no graph is generated in any active DB; nodes: Turn/Session/Model/Rule/Trip-wire.
- Proposed SDLC intent taxonomy `sdlc-intent-v1` with classifier `modernbert-sdlc-v1` (labels like change.fix, assure.test) — unbuilt.
- Router files: proxy/wire_capture_proxy.py, router/live_router.py, policy.py, state.py, discriminator.py, hook.py, episode.py, backends.py, features.py, llm_classifier.py, shadow_classifier.py, tripwires.py, escalation_controller.py, escalate.py, rule_health.py, memory_*.py, outcomes.py, telemetry.py, verifier.py, live_verification.py, counterfactual.py, shadow_retrieval.py, graph_lite.py, learning_contract.py, learning_readiness.py.
- Cross-references seen: EVL-004 (label quantity/quality threshold for retrieval authority), EVL-005 (simulator ≠ organic), EVL-006/007 (offline eval + explicit human graduation), EVL-009 (blockers never averaged), OPS-001 (multi-worker future), OPS-006 (record served rung, not intended).
