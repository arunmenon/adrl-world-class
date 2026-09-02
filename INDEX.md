# ADRL Decision Index — reviewed 2026-09-02

One row per decision. **Verdict** is the adversarial-review disposition; **Maturity** shows the register's claim → the review's recommendation (D0 Design · D1 Code · D2 Tested · D3 Shadow · D4 Pilot · D5 Graduated). Click the ID for the full record, including the original text in its changelog.

| Verdict | Count |
|---|---|
| AMEND | 38 |
| APPROVE | 8 |
| PROPOSED (new) | 6 |
| REJECT | 3 |

## FND — System Boundary and Principles

Bucket review: [`adr/FND/README.md`](adr/FND/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-FND-001](adr/FND/ADRL-FND-001.md) | Transparent control layer, protocol-scoped | AMEND | D3 | Q1, Q7 | Amended: transparency defined at wire level; SAF surfaces enumerated; Codex CLI scoped out pending evidence |
| [ADRL-FND-002](adr/FND/ADRL-FND-002.md) | Semantic policy vs mechanical execution, rung-closed | AMEND | D2 | Q1, Q7 | Amended: rung-closed execution contract; gateway fallbacks constrained to rung; content-control authority assigned |
| [ADRL-FND-003](adr/FND/ADRL-FND-003.md) | Routing boundary is the user turn | AMEND | D3 | Q3 | Amended: mechanical definition of user turn; pre-warm excluded; gating per request; per-lineage boundary |
| [ADRL-FND-004](adr/FND/ADRL-FND-004.md) | Fail to last-known-safe, not fail-open | REJECT | D4 → **D3** | Q5, Q7 | Superseded: fail-open retained for unpinned sessions only; fail-closed for pinned sessions; failure classes split; bypass audited and pin-preserving; D4→D3 recommended |
| [ADRL-FND-005](adr/FND/ADRL-FND-005.md) | Scope expands only through measured gates | APPROVE | D3 | Q6 | Approved unchanged |

## SEM — Interaction Semantics

Bucket review: [`adr/SEM/README.md`](adr/SEM/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-SEM-001](adr/SEM/ADRL-SEM-001.md) | Mechanical classification of request classes | AMEND | D3 | Q3 | Amended: pre-warm class added; wire headers as signals; content-bearing flag; gates on every class; Responses format scoped out |
| [ADRL-SEM-002](adr/SEM/ADRL-SEM-002.md) | Session key from wire headers, then metadata | AMEND | D3 | Q3, Q5 | Amended: session header preferred; lineage composition; fallback construction; hashed at rest |
| [ADRL-SEM-003](adr/SEM/ADRL-SEM-003.md) | Continuations inherit the sticky route | APPROVE | D2 → **D3** | — | Approved unchanged; rationale corrected on signature portability; D3 recommended |
| [ADRL-SEM-004](adr/SEM/ADRL-SEM-004.md) | Utility calls split by content exposure | AMEND | D3 → **D2** | Q2 | Amended: cosmetic/context-bearing split; pinned-session rule; fingerprint excludes pre-warm |
| [ADRL-SEM-005](adr/SEM/ADRL-SEM-005.md) | Episode boundaries, enumerated and measured | AMEND | D2 | Q5 | Amended: signals enumerated; pin never released; boundary metrics defined |
| [ADRL-SEM-006](adr/SEM/ADRL-SEM-006.md) | Subagents inherit constraints now, routing later | AMEND | D0 | Q3 | Amended: interim changed from passthrough to constrained passthrough (pin inheritance via wire lineage); harness model choice honoured; per-lineage evidence |

## SAF — Safety, Privacy, Hard Constraints

Bucket review: [`adr/SAF/README.md`](adr/SAF/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-SAF-001](adr/SAF/ADRL-SAF-001.md) | Hard gates first, on every request | AMEND | D2 | Q2 | Amended: gates on every request class; fallback path cannot override; monotone outcomes; gate failure semantics |
| [ADRL-SAF-002](adr/SAF/ADRL-SAF-002.md) | One-way pin, durable, lineage-scoped, audited release | AMEND | D2 → **D1** | Q5 | Amended: durable, lineage-scoped, covers all content-bearing classes; audited reason-coded human release added; D1 recommended |
| [ADRL-SAF-003](adr/SAF/ADRL-SAF-003.md) | Secret detection per request, precision-measured | AMEND | D3 | Q5 | Amended: per-request scan of new content; tiered, precision-measured detectors; suppression widened and retroactive |
| [ADRL-SAF-004](adr/SAF/ADRL-SAF-004.md) | Pinned sessions fail loudly, in the harness's dialect | AMEND | D2 | Q5 | Amended: binds gateway fallbacks and retries; defines the surfacing contract; permits intra-local escalation |
| [ADRL-SAF-005](adr/SAF/ADRL-SAF-005.md) | Block, and make the block recoverable | AMEND | D2 | Q2, Q5 | Amended: harness-recognisable block; compaction-window feasibility as a configuration constraint; action-boundary blocks |
| [ADRL-SAF-006](adr/SAF/ADRL-SAF-006.md) | Infeasible rungs removed before optimisation | APPROVE | D2 | Q2, Q7 | Approved unchanged |
| [ADRL-SAF-007](adr/SAF/ADRL-SAF-007.md) | Verification runs sandboxed, then diffed | REJECT | D2 → **D1** | Q2 | Superseded: post-hoc path check replaced by OS-enforced sandbox with no egress, snapshot execution and command allow-list; check retained as evidence; D2→D0/D1 |
| [ADRL-SAF-008](adr/SAF/ADRL-SAF-008.md) | Repository and data-class gate (Proposed) | PROPOSED (new) | D0 | Q2, Q5 | Proposed (adversarial review) |
| [ADRL-SAF-009](adr/SAF/ADRL-SAF-009.md) | Egress ledger and gate-audit integrity (Proposed) | PROPOSED (new) | D0 | Q5, Q7 | Proposed (adversarial review) |

## RTG — Routing Intelligence and Economics

Bucket review: [`adr/RTG/README.md`](adr/RTG/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-RTG-001](adr/RTG/ADRL-RTG-001.md) | Three capability rungs with measured boundaries | AMEND | D3 | Q1, Q2 | Amended: rungs must carry measured boundaries; effort is a within-rung parameter |
| [ADRL-RTG-002](adr/RTG/ADRL-RTG-002.md) | Cheapest rung likely to complete, defined | AMEND | D2 | Q2, Q4, Q6 | Amended: "likely" thresholded on a named estimator; "cheapest" defined as session-marginal cost including cascade and cache |
| [ADRL-RTG-003](adr/RTG/ADRL-RTG-003.md) | Rules own clear cases, measured | AMEND | D3 | Q4 | Amended: "clear" made a measured, versioned, revocable property; ambiguous-band size made a dated measurement |
| [ADRL-RTG-004](adr/RTG/ADRL-RTG-004.md) | Local-first only with a bounded, clean cascade | AMEND | D2 | Q2, Q5 | Amended: feasibility defined (healthy higher rung, context headroom after attempt, recoverable side effects, capped attempt); pinned-session carve-out |
| [ADRL-RTG-005](adr/RTG/ADRL-RTG-005.md) | Objective: verified quality, retry, latency, session cost | AMEND | D3 → **D2** | Q4, Q6 | Amended: cache-aware session cost placed inside the objective; terms named/versioned; unmeasured terms are unknown; latency mode-aware; maturity recommendation D2 |
| [ADRL-RTG-006](adr/RTG/ADRL-RTG-006.md) | Advisory LLM classifier, gated and bounded | AMEND | D3 | Q1, Q4, Q5 | Amended: placement bound to gates and pins; latency/cost budget; named conservative fallback; provenance logging |
| [ADRL-RTG-007](adr/RTG/ADRL-RTG-007.md) | Marginal-utility target, with a build gate | AMEND | D0 | Q4, Q6 | Amended: utility units fixed to RTG-009; pre-build gate added; abstention made prerequisite; single definition shared with LRN-003 |
| [ADRL-RTG-008](adr/RTG/ADRL-RTG-008.md) | Rung vs endpoint, with a leak contract | AMEND | D2 | Q1, Q7 | Amended: gateway contract added (served identity, within-rung stability, shared membership) because caches and signatures are model-specific |
| [ADRL-RTG-009](adr/RTG/ADRL-RTG-009.md) | Session-marginal, cache-aware cost accounting | PROPOSED (new) | D0 | Q4, Q6 | Proposed (adversarial review) |

## CAS — Execution, Cascade, Recovery

Bucket review: [`adr/CAS/README.md`](adr/CAS/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-CAS-001](adr/CAS/ADRL-CAS-001.md) | Deterministic trip-wires, with measured coverage | AMEND | D3 | Q2, Q3 | Amended: verifier outcomes made a first-class wire; per-rung versioned thresholds; miss rate published; harness-mechanical signals admissible |
| [ADRL-CAS-002](adr/CAS/ADRL-CAS-002.md) | Typed failures, versioned enum, measured attribution | AMEND | D2 | Q6, Q7 | Amended: `failure-types-v2` (six code types + `context_feasibility`, shared with MEM-004); precedence rule; `unverifiable` default; attribution precision gate |
| [ADRL-CAS-003](adr/CAS/ADRL-CAS-003.md) | Action boundary defined; no re-issue after side effects | AMEND | D2 | Q3, Q7 | Amended: boundary defined as all tool_use ids answered; no re-issue after streamed tool content; mechanical side-effect record in handoff |
| [ADRL-CAS-004](adr/CAS/ADRL-CAS-004.md) | Cross-model handoff: provider-pair rules, not one stripping rule | AMEND | D3 → **D2** | Q7 | Amended: per-provider-pair reasoning rule; tool-id mapping recorded; mechanical delimited handoff note positioned per provider rules; maturity D2 recommended |
| [ADRL-CAS-005](adr/CAS/ADRL-CAS-005.md) | Sticky escalation within an episode | APPROVE | D2 | Q3 | Approved unchanged |
| [ADRL-CAS-006](adr/CAS/ADRL-CAS-006.md) | Record the served model, not only the served rung | AMEND | D2 | Q7 | Amended: served model/provider and record provenance added; within-rung substitution typed; state loss made explicit |
| [ADRL-CAS-007](adr/CAS/ADRL-CAS-007.md) | Terminal failure surfaced; ADRL owns zero retries | AMEND | D2 | Q7 | Amended: surfacing defined as protocol-conformant typed error; ADRL zero retries; gateway retries bounded and constrained to rung/pin/streaming rules |
| [ADRL-CAS-008](adr/CAS/ADRL-CAS-008.md) | Escalation scope under subagents | PROPOSED (new) | D0 | Q3 | Proposed (adversarial review) |

## MEM — Memory, Evidence, Label Integrity

Bucket review: [`adr/MEM/README.md`](adr/MEM/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-MEM-001](adr/MEM/ADRL-MEM-001.md) | Append-only ledger keyed by route_id | AMEND | D2 | Q6 | Amended: append-only made strict; added schema versioning, idempotency and logged-erasure clauses |
| [ADRL-MEM-002](adr/MEM/ADRL-MEM-002.md) | Three-state outcome lifecycle with defined close | AMEND | D2 | Q6 | Amended: closing window made explicit, versioned and measured; human correction named as evidence; non-final labels censored |
| [ADRL-MEM-003](adr/MEM/ADRL-MEM-003.md) | Verification enriches, never overwrites | AMEND | D2 | Q6 | Amended: verification events carry provenance, tree identity and an indeterminate result; drifted-tree runs excluded from capability labels |
| [ADRL-MEM-004](adr/MEM/ADRL-MEM-004.md) | Cause-typed labels, six types not four | AMEND | D2 | Q2, Q6 | Amended: enum expanded to match code plus `context_feasibility`; labels carry version/confidence/provenance; precedence and safe-default rules added |
| [ADRL-MEM-005](adr/MEM/ADRL-MEM-005.md) | Prompt-derived artefacts are prompt-class data | REJECT | D2 → **D1** | Q5 | Superseded: embeddings and hashes reclassified as prompt-class data; retroactive pin suppression; keyed hashes; no default exception |
| [ADRL-MEM-006](adr/MEM/ADRL-MEM-006.md) | Memory facade, fail-safe but never silent | AMEND | D2 | Q7 | Amended: degraded mode made observable and excluded from evidence; process-local state declared a dependency; provider concurrency contract required |
| [ADRL-MEM-007](adr/MEM/ADRL-MEM-007.md) | Projections are rebuildable and versioned | AMEND | D2 | — | Amended: projections carry identity stamps, staleness is a state, detection mechanism specified, erasure propagates |
| [ADRL-MEM-008](adr/MEM/ADRL-MEM-008.md) | Retrieval stays advisory until gated | APPROVE | D3 | Q4, Q6 | Approved unchanged |
| [ADRL-MEM-009](adr/MEM/ADRL-MEM-009.md) | Counterfactuals bind only to explicit route_id | APPROVE | D2 | Q3, Q6 | Approved unchanged |
| [ADRL-MEM-010](adr/MEM/ADRL-MEM-010.md) | Retention and erasure of ledger and derived artefacts | PROPOSED (new) | D0 | Q5 | Proposed (adversarial review) |

## LRN — Learning and Adaptation

Bucket review: [`adr/LRN/README.md`](adr/LRN/README.md)

| ID | Title | Verdict | Maturity | Q | Change on 2026-09-02 |
|---|---|---|---|---|---|
| [ADRL-LRN-001](adr/LRN/ADRL-LRN-001.md) | Evidence tiers, not "outrank" | AMEND | D2 → **D1** | Q6 | Amended: "outrank" replaced by evidence tiers with T1-only objective/holdout, verifier-precision condition, and permitted weak-signal use |
| [ADRL-LRN-002](adr/LRN/ADRL-LRN-002.md) | Branched pairs, plus a logged-exploration channel | AMEND | D2 | Q4, Q6 | Amended: pairs must be live branches from the same turn state; rule-equivalence across arms; declared power target; OPE positioned as complement via LRN-008 |
| [ADRL-LRN-003](adr/LRN/ADRL-LRN-003.md) | The target is a CATE, name it | AMEND | D0 | Q4 | Amended: estimand named as CATE; classifier-vs-estimator dichotomy replaced by label-source prohibition; cost separated from label; two effects for three rungs |
| [ADRL-LRN-004](adr/LRN/ADRL-LRN-004.md) | Pre-decision features, enforced by construction | AMEND | D2 → **D1** | — | Amended: enforcement by construction — decision-time feature snapshot, as-of projections, temporal splits, named deny-list |
| [ADRL-LRN-005](adr/LRN/ADRL-LRN-005.md) | Every artifact is fully versioned | APPROVE | D2 | — | Approved unchanged |
| [ADRL-LRN-006](adr/LRN/ADRL-LRN-006.md) | Abstention with a declared risk-coverage target | AMEND | D0 | Q4 | Amended: uncertain/OOD defined via selective prediction with target risk and feature-space OOD; abstention rate reported and bounded; abstention built before estimator |
| [ADRL-LRN-007](adr/LRN/ADRL-LRN-007.md) | No autonomous online promotion | APPROVE | D0 | Q4 | Approved unchanged |
| [ADRL-LRN-008](adr/LRN/ADRL-LRN-008.md) | Logged exploration in the ambiguous band | PROPOSED (new) | D0 | Q4, Q6 | Proposed (adversarial review) |
