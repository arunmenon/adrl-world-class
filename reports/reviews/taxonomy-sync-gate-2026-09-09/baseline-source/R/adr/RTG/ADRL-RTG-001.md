# ADRL-RTG-001 — Three capability rungs with measured boundaries

| Field | Value |
|---|---|
| Bucket | RTG — Routing Intelligence and Economics |
| Status | Accepted · amended 2026-09-02 · amended 2026-09-03 (proposed amendment, pending disposition) |
| Maturity | D3 Shadow, review recommends D3 Shadow for the rung *model*, but the local rung's capability boundary is unmeasured (Phase 0 non-claim), so the register must carry that qualifier |
| Review verdict | AMEND |
| Tenets | 3, 7 |
| Related decisions | RTG-002, RTG-004, RTG-008, FND-002, SAF-006, LRN-003, EVL-004 |
| Open questions | Q1, Q2 |

## Decision

The policy reasons over three economic and service tiers, called rungs (local, cheap cloud, frontier), each defined by a versioned, measured capability boundary rather than by a model name and each realised by deployments in the signed inventory (TRU-002); rungs do not form a total capability order, "higher" means an approved escalation edge for a task slice, and per-request reasoning effort is a parameter inside a rung, not a rung.

1. Each rung carries a published boundary (context ceiling, permitted task classes, verified non-inferiority evidence) in the runtime registry; a rung whose boundary has no organic evidence is marked as such and its permitted scope is the conservative subset (Q2).
2. Adding or splitting a rung requires the same evidence as adding a learned component: a measured boundary and a scorecard entry, not a new model alias.
3. Reasoning effort / thinking budget within the frontier and cheap-cloud rungs is a dispatch parameter (CAS/gateway), and a change of effort is not a rung change for sticky-state purposes (CAS-005, CAS-006).
4. Escalation edges are declared per task slice in the registry (`escalation-edges-v1`: slice, from rung, to rung, evidence reference); a trip-wire escalation follows a declared edge; where no edge exists for a slice the request is placed at the highest permitted deployment from the start.
5. A rung is not a trust boundary: "local" as a safety property is `trust_zone: local_host` on a deployment (TRU-002), never the rung name.

## Context and rationale

Three rungs, because two is too blunt and five is unmeasurable. Local (free, private, limited context and capability), cheap cloud, frontier. Two rungs would force every "medium" task into one extreme; each additional rung needs its own measured capability boundary and its own evidence. Three is what we can actually defend — and the amendment makes "defend" concrete: a rung exists in the policy only when the registry can say what it is safe for. The routing literature offers no principled answer to "how many tiers", but it does show that adding candidates to a router gives sharply diminishing returns and that most realised gains come from coarse domain structure, which is an argument for few, well-separated rungs.

The amendment also closes a gap that commercial routers have already run into: modern models expose a second axis — reasoning effort / thinking budget — that changes cost by multiples inside what ADRL calls one rung. Treating effort as a hidden fourth rung would silently break the sticky-state and cache reasoning in CAS; treating it as a dispatch parameter keeps the rung model at three.

## Adversarial review (2026-09-02)

### Steelman
Rungs are stable abstractions over a churning model catalogue; three is the smallest number that separates "free and private", "cheap and capable enough" and "best available". Every rung must be evidenced separately, so the count is bounded by what the team can measure, which is an honest constraint. The literature's finding that router gains come from coarse structure rather than fine-grained discrimination supports a small ordinal ladder.

### Attacks
1. **The local rung has no measured boundary, so the ladder has a phantom bottom step.** The Evidence & Readiness page states local-rung reliability on realistic code is *not* established (small edit ops on small files; mixed-whitespace exact-string edits untested on the production model). A rung the policy reasons over but cannot characterise is a rung the policy can only guess about; every RTG-002/004 argument that depends on "local is likely to complete" inherits the guess.
2. **Reasoning effort is an unacknowledged fourth axis.** Not Diamond's coding-agent router explicitly selects "models and reasoning efforts", and frontier providers price effort/thinking as orders-of-magnitude cost differences. If ADRL's rung model ignores effort, either the gateway silently varies it (breaking the cost model in RTG-005) or the register needs a rung per effort level (contradicting "three").
3. **"Cheap cloud" has no membership criterion.** Local is defined by locality, frontier by "best", but cheap cloud is defined by price — which is a gateway concern (FND-002). Without a capability criterion the middle rung is whichever model the gateway team has on discount this quarter, and RTG-002's "likely to complete" has no stable meaning there.
4. **Three rungs assumes rungs are totally ordered in capability; they are not.** A local model may be *better* than cheap cloud at a narrow dialect (e.g. a fine-tuned edit format) and worse at reasoning. RouterBench found predictive routers that beat the best single model on some datasets and lost on others, i.e. capability is task-conditional. A strict ladder forces a monotone assumption the evidence does not support.

### Evidence
- Hu et al., "RouterBench: A Benchmark for Multi-LLM Routing System" (arXiv 2024) — predictive routers beat the best single model on some datasets and underperform on others; oracle routing consistently exceeds all routers, showing capability is task-conditional, not a single ladder (attack 4) — https://arxiv.org/abs/2403.12031
- LLMRouterBench (arXiv 2026) — "adding more models shows clear diminishing returns, while a carefully selected subset can yield substantially better outcomes"; realised gains come from "coarse-grained domain structure", supporting few well-separated rungs (steelman) — https://arxiv.org/html/2601.07206v1
- "Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey" (arXiv 2026) — provides no systematic analysis of optimal tier count; most cascades studied are binary or ternary, so "three" has no literature against it but no literature for it either — https://arxiv.org/html/2603.04445v2
- Not Diamond, "Not Diamond Code: intelligent model routing for coding agents" (vendor blog, 2026) — routes per step over both model and reasoning effort, treating effort as a first-class routing dimension (attack 2) — https://www.notdiamond.ai/blog/not-diamond-code-intelligent-model-routing-for-coding-agents
- ADRL Evidence & Readiness page (internal) — "Local-rung reliability on realistic code is not established" (attack 1).

### Verdict
**AMEND.** Attack 1 lands and is already conceded by the project's own non-claims; the decision text must not read as if all three rungs are equally characterised. Attack 2 lands: effort is a real cost axis that the three-rung sentence is silent about, and the cheapest fix is to declare it a within-rung dispatch parameter so CAS stickiness and cache accounting remain rung-based. Attack 3 is partially answered by RTG-008 (the gateway owns model identity) but the *capability* criterion for cheap cloud still belongs to RTG and is added as a registry field. Attack 4 is answered in practice by SAF-006 (infeasible rungs are removed before ordering) and RTG-004 (local only with a cascade), which together make the ladder an ordering of *fallbacks*, not a claim of monotone capability; no text change beyond clause 1 is needed. The count of three stands.

## Adversarial review (2026-09-03)

### Steelman
Three ordered rungs are the simplest model that supports a cascade, and the evidence that most gains come from coarse structure argues for exactly this.

### Attacks
1. **The order is assumed, not measured.** Agent routing work finds models specialise rather than forming one capability order; a cheap model that is better on a slice would be escalated away from under a total order.
2. **The rung name was doing safety work it cannot do.** SAF decisions read "local" as "never leaves the machine"; the implementation let a local rung be remote.
3. **Effort as a within-rung parameter is kept**, but the same argument applies: a rung is an economic tier and nothing else.

### Evidence
- Agent-as-a-Router (arXiv 2606.22902) and MTRouter (arXiv 2604.23530): cited by the 2026-09-03 external review; not independently fetched.
- ADRL external implementation review, 2026-09-03, finding P0-1, verified.

### Verdict
**AMEND (proposed).** Rungs become economic and service tiers with declared escalation edges per slice; the safety meaning of "local" moves to TRU-002. Pending disposition.

## Amendments applied
- Added "each defined by a versioned, measured capability boundary rather than by a model name".
- Added clause 1: published per-rung boundary with an explicit "no organic evidence" marker and conservative default scope.
- Added clause 2: rung changes require evidence, not aliases.
- Added clause 3: reasoning effort is a dispatch parameter, not a rung.
- 2026-09-03: rungs redefined as economic and service tiers realised by inventory deployments; total capability order removed; escalation edges per slice (clause 4); rung is not a trust boundary (clause 5).

## Follow-ups
- [ ] Add `boundary` fields (context ceiling, permitted task classes, evidence reference, evidence date) to the runtime registry entries for `local`, `cheap_cloud`, `frontier`; CI fails if a rung is enabled in `live` mode without an evidence reference.
- [ ] Golden test: a request whose only difference is `thinking`/effort budget must not produce a rung change in `router/state.py`.
- [ ] Produce the Q2 local-rung slice definition (mechanical, small-context, small-diff, no security/deployment paths) as the initial `local` boundary and run the non-inferiority comparison against `cheap_cloud` on that slice before widening.
- [ ] Record in the registry which capability criterion (not price) admits a model to `cheap_cloud`.
- [ ] 2026-09-03: publish `escalation-edges-v1` for the Q2 slice; CI fails a live rung whose edges lack evidence references.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: rungs must carry measured boundaries; effort is a within-rung parameter | "The policy reasons over three capability/cost rungs: local, cheap cloud, and frontier." |
| 2026-09-03 | Amended (proposed, external review): tiers with approved escalation edges, not a total capability order; local is a deployment trust zone | "The policy reasons over three capability/cost rungs — local, cheap cloud, and frontier — each defined by a versioned, measured capability boundary rather than by a model name, with per-request reasoning effort treated as a parameter inside a rung, not as a rung." |
