# A context graph for ADRL's decision memory

**Initial knowledge bootstrap, 2026-09-08:** the [experiment lab](adrl-experiment-lab-plan-2026-09-08.md) proposes task/harness/deployment experiments feeding MEM and a compatible K0 candidate snapshot before fleet rollout. The graph is an optional projection over that evidence. Real model execution is distinguished from simulation, and lab-derived knowledge remains subject to existing evidence-admission and graduation rules.

8 September 2026 · Proposed product/architecture application · No implementation or new authority

**Recommendation: complete and use the existing MEM architecture for adaptation, and evaluate a bounded context graph as a candidate improvement to its retrieval projections.** MEM already defines decision/outcome memory, verification, correction, retrieval and comparative-evidence ownership. Its job already supports retrieving relevant experience, learning better policies and revisiting architectural assumptions.

This incorporates the user's clarification that the graph is for memory and adaptation. Repository structure is one source of context. The central object is the history of decisions, evidence and reviewed changes.

## Start with the taxonomy already specified

The user explicitly asked us to recheck MEM. The complete decision sections of MEM-001 through MEM-010 and the relevant current implementation were re-read. The following capabilities come from the existing taxonomy; they are not inventions of this proposal.

| Existing ADR | What is already specified | How it supports adaptation |
|---|---|---|
| [MEM-001](../adr/MEM/ADRL-MEM-001.md) | Decision/outcome/event ledger, immutable route identity and appended corrections | Preserve what happened and revise conclusions without rewriting history |
| [MEM-002](../adr/MEM/ADRL-MEM-002.md) | Pending, turn-closed and final outcomes, with late evidence | Avoid learning success too early; incorporate later repairs/reverts |
| [MEM-003](../adr/MEM/ADRL-MEM-003.md) | Verification tied to exact output and verifier version | Establish which apparent outcomes are supported by checks |
| [MEM-004](../adr/MEM/ADRL-MEM-004.md) | Separate capability from other failure causes | Learn the right lesson from failure |
| [MEM-005](../adr/MEM/ADRL-MEM-005.md) | Prompt-derived data controls and retroactive suppression | Keep connected memory inside the allowed data boundary |
| [MEM-006](../adr/MEM/ADRL-MEM-006.md) | Provider-independent facade and observable degraded operation | Keep memory replaceable and avoid treating missing evidence as clean history |
| [MEM-007](../adr/MEM/ADRL-MEM-007.md) | Rebuildable, stamped retrieval projections | Provide the existing architectural home for evaluating a graph projection |
| [MEM-008](../adr/MEM/ADRL-MEM-008.md) | Retrieval remains advisory/shadow until evidence gates pass | Use past experience without granting premature routing authority |
| [MEM-009](../adr/MEM/ADRL-MEM-009.md) | Counterfactuals attach to an explicit route ID | Compare alternatives against the correct decision |
| [MEM-010](../adr/MEM/ADRL-MEM-010.md) | Retention/erasure reaches stored and derived artifacts | Make forgetting and evidence invalidation part of memory's lifecycle |

**Existing implementation also matters.** [NumpyIndex](../../adrl-core/src/adrl/ledger/projections.py) implements stamped cosine retrieval, rebuild/refresh and erasure invalidation. [ShadowRetriever](../../adrl-core/src/adrl/ledger/shadow_retrieval.py) retrieves neighbours and derives a local-success statistic from capability evidence, recording shadow advice. The [learning dataset code](../../adrl-core/src/adrl/learning/dataset.py) defines historical-neighbour feature machinery. [ExperimentArchive](../../adrl-core/src/adrl/ledger/improvement.py) preserves encrypted offline experiment history.

These mechanisms exist. Their presence does not establish that the running product uses qualified memory to improve choices: shadow retrieval is deliberately excluded from routing/proxy imports, the runtime selector constructs the heuristic estimator, and the present real-work evidence remains limited. This is a source inspection, not a fresh execution or broad maturity reassessment.

**The graph's incremental proposition is narrower:** typed multi-hop connections across task context, comparable experience and reviewed changes may retrieve better evidence than the current similarity/structured approach. Existing route/event/counterfactual links already encode relationships. Simply drawing those links as a graph adds no demonstrated routing value. Compare the candidate with that existing foundation before replacing anything.

The roadmap should therefore say: qualify and use existing MEM → measure its contribution to routing → test graph enrichment where a named query remains weak → admit improved retrieval/features only after their gates.

## The laptop and offline-learning architecture

**User architecture clarification, 8 September:** ADRL runs alongside the developer's harness. It retains local experience, while a separate process learns from qualified evidence and distributes improved knowledge back to developer installations. This fits the existing separation of FND, MEM, LRN, EVL and OPS.

Use three deployment/economic rungs: local, lower-cost cloud and frontier cloud. OpenAI and other proprietary providers can occupy the cloud rungs. Actual capability is measured for a task/profile; these categories are not a universal intelligence ranking.

    Developer laptop
    ┌─────────────────────────────────────────────────────────────┐
    │ Harness → permitted context → ADRL routing → model request  │
    │    │                               │                        │
    │    └─ tool/work observations ───────┤                        │
    │                                    ↓                        │
    │                  MEM: local decision/outcome history        │
    │                       + qualified retrieval view            │
    │                                    ↑                        │
    │                    installed approved policy package        │
    └─────────────────────────────────────────────────────────────┘
                    │ eligible, authorized evidence only
                    ↓
           Offline learning and evaluation
           candidate → independent comparison → approval
                    │ signed, compatible policy package
                    └──────────────────────→ developer laptop

Model requests go to a local runtime or an approved provider/gateway according to the qualified harness profile. The learning/evaluation process is outside the live request path. It can initially run on an authorized local machine; an organization-controlled service is a later deployment choice. The laptop should not need to call a central learning service for each routing decision.

### Two kinds of knowledge, with different lifecycles

**Local experience memory:** “What happened here?” The harness supplies attributed observations about tools, edits and task progress. ADRL supplies its own route choice, reason codes, permitted options, policy version and dispatch receipt. MEM connects them to exact outputs and independently verified or corrected outcomes. A hook reporting a model name is not proof that ADRL selected it.

**Released learned knowledge:** “What general lesson has enough evidence to use?” A versioned package may contain model-capability estimates for supported task slices, calibrated comparative effects, allowed policy parameters, abstention settings and compatible feature definitions. These are learned/generalized conclusions, not a copy of every developer's graph.

Distilling knowledge down to the laptop initially means compiling or training a compact routing-policy artifact. It can be rules, tables or a small estimator. Training a new coding model is a separate future proposal and is unnecessary for this architecture.

Local task context and qualified local memory combine with the installed package to guide the next decision. Permission, privacy pins, deployment availability and semantic compatibility are rechecked locally; a package cannot override those restrictions.

### The improvement cycle

1. **Observe locally.** Record decisions and harness observations separately, linked by reliable identity.
2. **Qualify outcomes.** Tie checks to exact output, account for late repair/revert evidence and separate capability from environmental failures.
3. **Admit evidence for a specific use.** A local learner can use eligible local data; a shared learner receives only material explicitly permitted for that destination and purpose. Aggregated statistics and embeddings are not automatically non-sensitive.
4. **Build a candidate offline.** Start from the previous approved package. The learner may discover a task/model capability pattern, a better calibration or a proposed rule change.
5. **Evaluate independently.** Compare complete-task benefit against baselines and the incumbent on fresh evidence, with all gates and search costs.
6. **Approve and distribute.** LRN-005 supplies artifact versions; LRN-007 and EVL govern graduation; OPS controls signing and release.
7. **Activate on a compatible cohort.** Check signature, feature/profile/model compatibility and freshness. Activate at an approved boundary; preserve in-flight semantics. Retain rollback to a compatible approved package without discarding current restrictions.
8. **Observe the effect.** Record package version on decisions. Regressions, drift or invalidated evidence can withdraw the affected package.

The first shared package can be team-specific. A cross-customer learning pool requires a separately validated product/data agreement; it is not an assumed startup asset. Neither local updates nor centrally produced packages grant autonomous promotion.

### What changes in the taxonomy

Most of this shape is already present: FND-001's local removable engine/adapters; MEM's experience and retrieval; LRN-003/004's conditional learning and feature snapshots; LRN-005's versioned artifacts; LRN-007's explicit graduation; EVL's assessment; and OPS signing/recovery.

The incremental design work is the **evidence-export and policy-distribution contract**: allowed evidence, destination/tenant, source lineage, update eligibility, package compatibility, expiry/revocation, activation boundary and rollback. Reuse existing contracts wherever possible. A fleet rollout service is future OPS/W11 scope, not a hidden prerequisite for the first local experiment.

P1/P2 preserve local experience and exercise the contract with synthetic/manual packages that retain their non-learning status. P3 can perform a human-led improvement cycle within approved rules. P5 builds qualified learned packages; P4/W11 qualify distribution across the relevant installations as demand requires. P6/P7 improve the process that produces those packages.

**Ordinary improvement:** package B routes better than A. **Recursive improvement:** a revised offline improvement process produces better packages than the previous process, for the same total budget, under independent evaluation. Both ultimately have to help real developer tasks.

## 1. What ADRL should remember

A flat event can say, “Model A failed.” Connected memory should let us determine:

> What was the task? What context was available? Which choices were permitted? Why did the policy select A? Did A actually serve it? Was the failure caused by capability, missing context, an unavailable tool or infrastructure? What did an independently executed alternative do? Which policy and ADR were challenged?

Those distinctions prevent the system from learning “A is bad” when the actual problem was an unavailable database.

The logical graph has these connections:

    Task → decision-time context → routing decision → actual attempt
                  ↓                       ↓                ↓
          repository/tool state    policy + ADR clause   output
                  ↓                       ↓                ↓
           relevant past cases     allowed alternatives  verification
                                                          ↓
                                                   qualified outcome
                                                          ↓
                                       proposed improvement → evaluation
                                                                  ↓
                                              approved policy / ADR amendment
                                                                  ↓
                                                       future decisions

This is a proposed unified graph view. Several underlying connections already exist in the MEM contracts and ledger; the complete graph view and its value remain unimplemented/unqualified. A retrieved old case can inform a future decision only through the applicable authority gates. Recording an alternative as available does not mean we observed its outcome.

## 2. How MEM, LRN and RTG fit together

| Part | Responsibility |
|---|---|
| MEM | Preserve attributable events, construct a permitted view of connected experience, retrieve relevant evidence |
| Classifier/advisor | Describe task scope or advise on an ambiguous case within RTG-006's bounds |
| LRN | Estimate the additional verified benefit of a model choice in this context, with uncertainty |
| RTG and CAS | Choose and execute an allowed action using benefit, cost, state and valid transition boundaries |
| EVL | Test whether a proposed change improves outcomes on fresh, properly admitted evidence |
| Decision owners | Adopt, narrow or reject policy/architectural amendments and record the reasoning |

The graph is a representation of memory. The learner is the mechanism that generalizes from evidence. The router is the decision maker under policy. The graph does not itself establish causality or grant permission.

A useful early product can retrieve relevant past cases for a human review. A later qualified product can derive features or comparative evidence for LRN. Automatic retrieval, learned authority and automatic promotion are separate capabilities with separate gates.

## 3. A concrete example

Consider the request: **“Fix this parser bug.”** The following is hypothetical:

1. MEM links the request to a context snapshot: parser changes, string escaping, available checks, current model, repository version and budget.
2. The graph retrieves earlier permitted cases connected to the same kind of change. It retains successful attempts, failures, uncertainty and later corrections.
3. Several cheap-model attempts passed superficial checks but failed an independent escaping test. Other cases show that a stronger model also failed when the necessary specification was absent.
4. ADRL therefore has two candidate explanations: a model-capability limitation on one slice, and missing context on another. It does not collapse both into “always use frontier.”
5. A controlled experiment compares model choices on fresh eligible cases with adequate context. If a capability difference is confirmed, LRN can learn it after evidence admission.
6. RTG proposes a narrower starting rule or transition rule. EVL checks the proposed policy against the incumbent, including cost and regressions.
7. An approved change records the affected RTG/LRN clause and evidence. If broader findings undermine a local-first architectural assumption, they become a scoped ADR amendment proposal.

This is how memory can evolve decisions. A single apparent success, a similar-sounding task or a graph edge labelled “caused” is insufficient.

## 4. Three linked views

**Work context:** task, authorized repository snapshot, relevant files/symbols, dependencies, tools and acceptance checks. Prefer existing deterministic repository/tool metadata and supplied context before purchasing or constructing a broad index.

**Decision experience:** exact decision-boundary snapshot, permitted deployments, policy version, factual reason codes, intended/served identity, attempt, output, verifier, outcome, costs, interruptions and later corrections. Do not invent unavailable internal model reasoning or treat an explanation generated afterward as a contemporaneous reason.

**Improvement history:** candidate, supporting/challenging evidence, baseline, evaluation window, rejected alternatives, reviewer disposition, policy/ADR version and rollback. This lets us ask whether our changes really helped and whether the improvement process itself is getting better.

Keep observed relations separate from inferred ones. A parser reference found by a syntax analyzer, a relationship guessed by an LLM and a human-approved conclusion carry different provenance and confidence. Entity resolution must not merge unrelated tasks, versions, repositories or tenants because names happen to match.

## 5. Build a projection, preserve the evidence source

MEM-001 already owns the event ledger; MEM-007 owns rebuildable retrieval projections. The recommended first graph is a **derived view over admitted evidence and authorized context references**, with its own version and validity rules. It must not become a competing truth store.

A small graph does not require a new graph database. Start by testing bounded relational joins/adjacency over the existing provider abstraction. Compare an external graph engine only when query complexity, scale or operational needs justify it. “Graph” is a data model choice before it is an infrastructure purchase.

The proposed projection identity extends existing MEM-007 principles: ledger position, context/repository snapshot, schema/extractor version, resolution version and any embedding model. Record the exact projection/features used by a decision. Changed sources, versions or permissions can invalidate the view.

Two times matter: **when a fact applied** and **when ADRL learned it**. A late verifier correction may describe yesterday's task but was unavailable to yesterday's router. Historical training/evaluation must reconstruct what was known then; current reviews should incorporate the correction. Never use a future outcome when reconstructing the input of the decision it judged.

Repository context outside the ledger needs explicit authorized source identity and lifecycle. If a source has been erased, rebuilding the projection must not resurrect its content. Reproducibility then reports the evidence unavailable; it is not a justification for indefinite retention.

## 6. Queries worth proving before building broadly

The first graph proposal should support only a few decision-relevant queries:

1. What exactly was known, permitted and selected at this boundary?
2. Which earlier eligible cases share relevant context, with what contradictory evidence?
3. Which failures are attributable to capability versus environment, protocol or missing context?
4. What happened to comparable tasks after a policy change?
5. Which evidence supported or challenged this ADR clause, and what remains unresolved?

Do not assume “many nearby successes” is a calibrated probability. The old policy selected which models ran; outcomes for unchosen alternatives are usually missing. LRN still needs its admitted paired/exploration evidence and uncertainty treatment.

A graph can make label construction and discovery easier, but observed relationships remain associations. Valid branches and randomized/appropriately controlled comparisons provide the causal evidence.

## 7. Guardrails specific to connected memory

- Apply tenant, permission, privacy and retention filters before traversal and returned context assembly. Connected paths can reveal information even when individual fields appear innocuous.
- Treat text from repositories, tools and memory as data. It cannot override instructions, release authority, budgets or permitted deployments.
- Preserve origin and verification quality separately. Synthetic cases, pilot cases and organic verified outcomes must not become interchangeable through a graph query.
- Retain late failures, reverts and contradictory evidence. Entity merging, deduplication and supersession must not erase inconvenient results or inflate sample counts.
- Bound traversal depth, returned evidence, elapsed time and resource cost. On missing, stale or untrusted memory, use the approved degraded/abstention path; do not fabricate confidence.
- Inventory content in nodes, edges, indexes, summaries, embeddings, caches, temporary files, WAL and backups. Erasure and late pins must invalidate derived copies according to their actual scope.
- Keep mutable projection maintenance behind the provider contract. Do not introduce in-place changes to authoritative event history.
- Separate current-task observations from future labels. LRN-004's broad deny-list needs an explicit time-indexed disposition before new prior-step verification signals become learned inputs.

## 8. How this changes the implementation sequence

| Product milestone | Graph-related work proposed | Guardrail/exit |
|---|---|---|
| P1: visible dependable routing | Define the minimum experience links and show one synthetic decision-to-evidence traversal | Projection is explicit research/diagnostic scope; no organic-quality or learning claim |
| P2: one-harness value | Capture qualified task/context/decision/output relationships; audit completeness | Existing custody, verifier, privacy and evidence gates apply |
| P3: adaptation | Evaluate bounded memory queries in shadow and test whether context-aware choices help | MEM-008 gates remain; missingness/contradictions and latency are reported |
| P4: cross-harness reuse | Add harness/profile/source identity without conflating incompatible experiences | Same query contract, independently qualified sources and semantics |
| P5: policy learning | Feed approved graph-derived features or evidence into LRN | LRN-004 snapshots, data admission, no future leakage, calibrated abstention |
| P6/P7: improvement and RSI | Link failed proposals, experiments and adopted/rejected changes | Compare improvement methods against independent fresh judging and total costs |

The graph is considered early in the schema/query design. It does not justify delaying the first routing proof for a company-wide knowledge platform.

## 9. The experiment that earns this architecture

Compare three candidate memory representations over the **same authorized evidence**:

- A: structured task/decision fields without historical retrieval.
- B: flat or vector retrieval over the same admitted past cases.
- C: bounded context-graph retrieval over those cases and relationships.

Keep the selector family, candidate deployments, output-context budget, task assignment and independent verifier fixed where possible. First measure retrieval relevance, provenance correctness, stale/future/cross-tenant exclusions and contradictory-evidence retrieval. Then measure actual routing quality, completed-task benefit, decision latency and total cost including extraction, indexing, refresh and storage.

Use development cases for design and fresh later cases for confirmation. When choices alter execution, run valid independent branches. Report whether the graph helped retrieval, changed a decision, or actually improved a completed task; these are different findings.

If C adds no worthwhile benefit over B, retain the simpler representation. If it only improves human explanation, value and price that separately from autonomous routing. No preselected graph library or benchmark result settles this test.

## 10. Taxonomy ownership and maturity

| ADRs | Proposed application |
|---|---|
| MEM-001/002/003/004/009 | Events, outcome lifecycle, exact verification, typed causes and explicit comparative links |
| MEM-005/010 | Content inventory, data minimization, late pins and erasure across connected/derived memory |
| MEM-006/007 | Provider abstraction, bounded degraded behavior and versioned rebuildable graph projection |
| MEM-008 | Retrieval usefulness and authority gates |
| LRN-003/004/006 | Context-conditioned comparative benefit, decision-time snapshots and uncertainty |
| RTG-003/007/009, CAS-003 | Decision context, temporal choices, total cost and safe boundaries |
| LRN-005/007, EVL-001–009, OPS-002/007 | Versioned proposals, independent assessment, promotion and rollback |

Propose an explicitly scoped application to MEM-007 for graph projections and to MEM-008 for graph retrieval evaluation. Resolve LRN-004's temporal-field issue and the existing T1/T5 conflict before admitting the relevant learned evidence. Add a new ADR only if these owners cannot express the contract coherently; no new ID is assigned here.

A graph schema is D0 design; implemented traversal may be D1; qualified provenance/leakage/fault tests can support scoped D2. Organic shadow, controlled use and graduation still require their existing gates. None of these maturity changes has occurred in this proposal.

## 11. Research grounding and its limits

[Context Graph](https://arxiv.org/abs/2406.11160), a 2024 paper, describes adding temporal validity and provenance to entity relationships. Its reported evaluations concern knowledge completion and question answering, not coding-model routing.

[Zep](https://arxiv.org/abs/2501.13956), a 2025 architecture paper from the system's authors, describes temporal graph memory for evolving conversational/business information. Its memory-benchmark results motivate a candidate representation; they do not prove ADRL routing gains or independent commercial superiority.

[RepoGraph](https://arxiv.org/abs/2410.14684), ICLR 2025, evaluates repository-structure support for software-engineering agents. It supports testing code relationships as context, without establishing that graph-based model selection is better.

[Microsoft GraphRAG](https://microsoft.github.io/graphrag/) documents a graph-based retrieval approach for assembling model context. Retrieval for answering a question and retrieval for choosing a coding model are different evaluation targets.

These primary abstracts/documentation were checked on 8 September 2026. This is a focused design review, not a reproduced benchmark or full systematic graph-memory survey.

The product decision is therefore: **test connected decision memory in MEM, use it to supply qualified context to LRN/RTG, and let measured benefit determine how far to invest.**

See the [product roadmap](../reports/adrl-product-roadmap-2026-09-08.md) for customer, investment and release gates.
