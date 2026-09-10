# ADRL Adversarial Architecture Review — Review Log

**Latest forward planning, 2026-09-07:** the [implementation roadmap](reports/adrl-implementation-roadmap-2026-09-07.md)
links the current baseline to twelve evidence-gated work packages and eight proposed decision
dispositions. All 77 ADRs have a review-wave assignment. No new scientific adjudication,
implementation, graduation or model experiment is claimed. The four directly owning planning
records preserve their prior text and statuses.

**Latest implementation evidence, 2026-09-07:** the [offline verifier experiment](reports/adrl-improvement-experiment-2026-09-07.md)
records 549 passing tests and a 4/7 baseline versus 7/7 candidate comparison on curated examples.
The same assistant authored candidate and fixtures; this is a mechanism exercise, not a blind
assessment, new scientific review or recursive self-improvement result. Twelve owning records
preserve implementation scope and remaining gaps. Historical research verdicts are unchanged.

**Latest implementation evidence, 2026-09-07:** the [session verification report](reports/adrl-session-verification-2026-09-07.md)
records applied API preview 4, 532 passing tests, and two repeated verifier jobs on one prior
pilot task. Ten owning ADRs now record the session application, erasure, authority and sandbox
limits. This is implementation evidence; historical research verdicts and claims below retain
their dates. No new scientific review or population-level evaluation is claimed by this update.

## 2026-09-07 live observation pilot

The [pilot report](reports/adrl-live-observation-pilot-2026-09-07.md) records applied observation
mode, 511 passing tests, and a real 18-event hook session. Independent compatibility review
rejected the initial four-test-passing fix; the repair passed eight tests. This is limited live
integration evidence. No policy-economic comparison, general graduation or verified learning
label follows. Five owning ADRs, their index rows and bucket summaries are synchronized.

**Date:** 2026-09-02
**Scope:** all 49 Accepted decisions in the seven captured buckets (FND, SEM, SAF, RTG, CAS, MEM, LRN) of the ADRL decision register (Confluence, updated 2026-08-27), plus the seven Open Questions.
**Not in scope:** EVL and OPS (pages not captured; only EVL-004/005/006/007/009 and OPS-001/006 are known by cross-reference).
**Method:** each decision was steel-manned, then attacked from at least four angles specific to this system (coding-agent wire traffic, tool loops, prompt caches, privacy pins, cross-provider handoff, SQLite ledger, the Phase 0 non-claims), then tested against the literature and vendor documentation (121 distinct sources, of which 25 load-bearing citations were re-fetched and checked line-by-line). Every decision received exactly one verdict — APPROVE, AMEND or REJECT — and, per the register's own rule, every original sentence is preserved verbatim in the file's changelog. Amended and replacement text was written in place. Six new decisions are proposed where a bucket was found to be missing one.

## Disposition tally

| Verdict | Count | Decisions |
|---|---|---|
| APPROVE | 8 | FND-005, SEM-003, SAF-006, CAS-005, MEM-008, MEM-009, LRN-005, LRN-007 |
| AMEND | 38 | everything else in the original 49 |
| REJECT (replaced) | 3 | FND-004, SAF-007, MEM-005 |
| PROPOSED (new) | 6 | SAF-008, SAF-009, RTG-009, CAS-008, MEM-010, LRN-008 |

**Maturity changes recommended** (claimed → recommended): FND-004 D4→D3 · SAF-002 D2→D1 · SAF-007 D2→D1 · SEM-004 D3→D2 · CAS-004 D3→D2 · RTG-005 D3→D2 · MEM-005 D2→D1 · LRN-001 D2→D1 · LRN-004 D2→D1 · **SEM-003 D2→D3 (upgrade)**. Ten changes, nine down and one up. In every downgrade the pattern is the same: the D-level certified the *text* of the decision, or a contract file, rather than the *behaviour* the decision promises.

## The ten findings that matter most

1. **The gates scan the wrong message.** SAF-003 binds secret detection to "before routing"; FND-003 binds routing to "once per user turn". Read together, the scanner sees the developer's typed instruction and skips the ~15 `tool_result` continuations that actually carry `.env` contents, command output and fixtures — the dominant secret ingress in coding-agent traffic. This is a wording defect, not an architectural one: SEM-003 already scopes itself to the *difficulty* decision. SAF-001, SAF-003, FND-003 and SEM-001 are amended to gate every request class on new content; SEM-003 is approved unchanged. *(SAF, SEM, FND)*

2. **The privacy pin is not a guarantee today.** Four independent holes: (a) pin state is a single-process Python dict, so a proxy restart unpins live sessions; (b) `count_tokens` bodies (full prompt, ~72% of wire volume) pass through "unchanged"; (c) compaction/title utility calls and forked subagents (which inherit the whole parent transcript) bypass it under the SEM-004/006 interims; (d) FND-004's blanket fail-open sends a pinned session to the cloud on a scanner exception, and LiteLLM's documented context-window fallbacks can do the same mechanically. FND-004 is **rejected and replaced** (fail-open only for unpinned sessions; fail-closed for pinned; every fail-open recorded and rate-alerted). SAF-002 gains durability, lineage scope and full request-class coverage, and — answering Q5 — an audited, reason-coded, per-finding human release modelled on GitHub push protection. SAF-009 is proposed so "did this code ever leave the machine?" becomes a ledger query rather than a promise. *(SAF, FND, SEM)*

3. **SAF-007 claims a preventive control and ships a detective one.** `verifier.py` checks *after* execution that protected files were unchanged; it does nothing about network egress or writes outside the repository, so a test suite (or a `conftest.py` the model just wrote) can exfiltrate the working tree — the largest unmitigated egress path in a privacy layer. **Rejected and replaced** with the harness's own OS-enforced sandbox in strict mode, snapshot execution and a command allow-list. *(SAF)*

4. **The embedding store is a lossy copy of the company source code.** MEM-005's rationale says "derived data counts as data" but its decision stores embeddings for every non-private turn. Morris et al. (EMNLP 2023) recover 92% of 32-token inputs exactly from embeddings; a 2025 reproducibility study confirms it; zero-shot inversion needs only black-box encoder access — and ADRL ships the encoder next to `router-memory.db`. The concrete hole: SAF-002 pins a session at turn *k*, but turns 1…*k−1* are already embedded and, under MEM-001, immutable. **Rejected and replaced**: embeddings and hashes are reclassified as prompt-class data, pin suppression becomes retroactive, hashes are keyed, and retention/erasure moves to the new MEM-010 (crypto-shredding by session). *(MEM, SAF)*

5. **RTG has no cost unit.** RTG-002 ("cheapest"), RTG-005 ("cost") and RTG-007 ("marginal utility") each depend on a definition none of them gives, while cache reads bill at 0.1× (0.025× on the newest Anthropic models), writes at 1.25–2×, and caches are per model. GitHub Copilot's auto model selection and Not Diamond have both independently moved to session-level, cache-boundary routing. **RTG-009 proposed** (session-marginal, cache-aware cost accounting); RTG-002/005/007 amended to cite it. *(RTG)*

6. **CAS-001's blind spot is the majority failure class.** SWE-agent puts 52% of unresolved runs in "incorrect implementation" vs 23% in cascading edits; MAST puts 21% of failures in verification. Counter-based trip-wires cannot see any of these; only deterministic verification can, and only one task has strong verification today. CAS-001 promotes verifier outcomes to a first-class wire and publishes the miss rate. The consequence for Q2 is direct: **the local rung's scope may not exceed the task classes for which a verifier exists**, because there the escalation instrument is blind. *(CAS, RTG)*

7. **CAS-004's stripping rule breaks the most likely escalation path.** Anthropic requires the latest assistant turn's `thinking`/`redacted_thinking` blocks to be echoed unmodified when thinking is on ("rejected with a 400 error"); the API itself drops blocks an older model cannot read; OpenAI's encrypted reasoning is same-family only; LiteLLM has open multi-turn bugs on exactly this seam. A single "remove private reasoning" rule 400s on a cheap-Anthropic→frontier-Anthropic escalation with thinking enabled. Replaced with a versioned per-provider-pair table; maturity down to D2 because shadow mode never sends a transformed transcript to a target provider. *(CAS)*

8. **The CAS-003 replay trace the register asked for found two cases — neither is an escalation.** (i) A transport retry after a `tool_use` block has been streamed re-generates the same action with a new id and the harness executes both; (ii) with parallel tool calls, a continuation carrying a partial `tool_result` set is not a boundary. Both closed by "no re-issue after first streamed tool content" and "boundary = every `tool_use` id answered". CAS-007 fixes ADRL's own retry count at zero and bounds the gateway's — the concrete Q7 retry-ownership line. *(CAS)*

9. **LRN-003 never names its estimand, and its central dichotomy is false.** "Marginal utility of frontier" is a conditional average treatment effect (treatment = rung, outcome = verified result, conditioning = pre-decision features). Naming it supplies the estimators (T/X/DR-learners), the S-learner shrinkage pitfall, what "calibrated" means for a difference of probabilities, and the fact that three rungs need two effects. RouteLLM and Hybrid LLM are classifiers trained on comparative outcomes that generalise — so "classifier vs estimator" is the wrong line; the prohibition is re-aimed at the label source. Off-policy evaluation cannot substitute for pairs on deterministic logs (no propensities, no overlap), and the power arithmetic (McNemar, α=0.05, 80% power) says δ=0.10 needs ~115–235 pairs per slice versus 34 evaluated decisions and one verified task. The 2026 "Replay Gap" study shows model swaps diverge at the first post-fork action in 74–77% of cases, so pairs must be live branches, not replays. **LRN-008 proposed** (bounded, gated, propensity-logged exploration in the ambiguous band). *(LRN, MEM)*

10. **The harness now publishes the identity SEM was reverse-engineering.** Anthropic's gateway contract documents `x-claude-code-session-id`, `x-claude-code-agent-id` and `x-claude-code-parent-agent-id`, which make SEM-002's key and SEM-006's constraint inheritance a lookup rather than a design problem. Separately, Claude Code sends adaptive `thinking` to unrecognised model aliases and *disables a rejected capability for the rest of the conversation*, so a first turn routed local without ADRL stripping the field silently degrades the whole session (FND-001 amended). Codex CLI is named as a harness but speaks only the Responses API — scoped out of FND-001 pending a corpus. *(SEM, FND)*

## Cross-bucket conflicts found and how they were resolved

| Conflict | Resolution |
|---|---|
| FND-004 (universal fail-open, D4) vs SAF-001/002/004 (gates) | FND-004 replaced: fail-open by pin state and failure class; a fallback path can never override a gate. |
| FND-003 "route once per turn" vs SAF-003 "scan before routing" | Split *routing* (once per turn — kept) from *gating* (every content-bearing request — new). |
| FND-002 split vs LiteLLM context-window / content-policy fallbacks | Fallback groups must be rung-closed and local-only for pinned traffic; shared versioned rung config consumed by both ADRL and gateway. Q7 answered for fallbacks. |
| RTG-004 (local-first requires a cascade) vs SAF-002/004 (pinned sessions have no cascade) | Explicit carve-out with a ledger marker: pinned sessions are local-or-block, never "local-first with escalation armed". |
| RTG-006 (advisory LLM classifier) vs SAF-003 (a cloud classifier call on a flagged session is a leak) | Classifier placement bound to the gate result; on a pinned session the classifier is local or absent. |
| RTG-007 vs LRN-003 (same decision, two texts) | RTG-007 owns the runtime target and the pre-build gate; LRN-003 owns the estimand and training data; both cite RTG-009 units and one EVL baseline set. |
| CAS-002 (four types) vs MEM-004 (four types) vs `outcomes.py` (six) | Both adopt `failure-types-v2`: the six code types plus `context_feasibility`; schema test proposed so the register cannot drift silently. |
| CAS-003/007 vs FND-001/004 (a synthetic "could not complete" assistant message would poison the transcript) | Terminal failures are protocol-conformant errors, never synthetic assistant content. |
| CAS-005 vs SEM-005 (ratchet toward always-frontier if boundaries never fire) | Not a CAS defect; ratchet-cost metric added so SEM-005 can be tuned on evidence. |
| CAS-008 interim vs SEM-006 interim | CAS-008 defers to SEM-006's constrained passthrough (harness-requested model, pin inherited); forks start at the parent's served rung. |
| MEM-003 vs SAF-007 (policy-blocked verification) | Recorded as `indeterminate`, never `fail`. |
| MEM-006 vs SAF-004 (degraded memory on a pinned session) | Pin state must be durable outside the fail-safe facade; degraded memory never unpins. |
| MEM-007 vs LRN-004 (retrieval index contains the future) | Projections carry a ledger high-water mark; as-of rebuilds required for offline evaluation. |
| LRN-002/007 vs EVL-006 ("offline evaluation") | Offline evaluation of a routing artifact must be branched or propensity-weighted, never replay. |
| SEM-004 compaction vs SAF-005 blocking | Compaction is content-bearing (must go local on a pinned lineage); a local rung too small to hold the compaction request is rejected at configuration time to avoid deadlock. |

## What this review says to the seven Open Questions

- **Q1 (build vs. buy).** The review agrees with the lean and sharpens the boundary: the differentiator is *everything gated by pin state* — per-request scanning, durable one-way pin, lineage inheritance, fail-closed for pinned traffic, an egress ledger — none of which a cloud-side router can provide because it never sees the local decision. Cloud-to-cloud choice is commodity, with the caveat that independent benchmarks (RouterBench, LLMRouterBench) show commercial routers frequently failing to beat the best single model; Bedrock's router routes within one model family only and cannot learn from application data. Adopt an external router for cloud-to-cloud only after RTG-009 gives you a cost unit to compare it on.
- **Q2 (local safe zone).** Drawn by capability *and* risk is right, and the review adds a third axis: **verifiability**. Because CAS-001's trip-wires are blind to methodical-but-wrong runs, the local rung's permitted scope should not exceed the task classes for which a deterministic verifier exists. Categories never allowed on local regardless of accuracy: anything SAF-008 classifies as restricted (PCI scope, residency-bound repos), anything touching deployment or migrations, and any turn whose compaction request the local rung cannot hold.
- **Q3 (subagents).** Passthrough *does* leave an unacceptable gap — for the pin, not for routing. Forked subagents inherit the entire parent transcript and were passed through regardless of pin state. SEM-006 is amended to *constrained* passthrough (pin and gate state inherited immediately; harness-requested model honoured; own `route_id` and lineage). CAS-008 (proposed) gives the cleaner model: escalation scoped to a single routing identity, constraints flow parent→child at spawn, outcomes flow child→parent as typed evidence, budgets propagate. The identity problem is solved by the harness's own headers.
- **Q4 (marginal utility).** Keep it simple and cache-aware first — and state the bar. RTG-007 now carries a pre-build gate: published ambiguous-band share of turns *and* spend on a representative population, an oracle-bound gain from counterfactual pairs, and a versioned minimum realised gain over always-local, always-frontier and the current heuristic *after cache effects*. Abstention (LRN-006) must reach D2 before the estimator is trained. If the estimand is named (CATE), the modelling is not the hard part; the pairs are.
- **Q5 (pin granularity).** Session — more precisely, session *lineage* — is forced: once a secret is in the context it is in every subsequent request, and a coding harness's transcript cannot be relabelled by regenerating outputs from reduced contexts. The relief valve is the same one GitHub push protection and Microsoft Purview use: human, audited, reason-coded (`false_positive`, `test_fixture`), per finding, disabled by policy for restricted repositories. One-way is preserved for every automated actor. Scanner precision remains the highest-leverage knob and is now a measured, published, per-detector figure (SAF-003).
- **Q6 (evidence before live routing).** The lean is right and the review adds four conditions: the excluded fraction (pinned, suppressed, degraded-memory, subagent) reported next to every metric as a representativeness condition; verifier precision measured before "verified" counts as tier-1; counterfactual pairs as live branches with a stated power target per slice; and the adversarial suites listed in every SAF file run at least once — no maturity in SAF should rise while the gates are "tested, not attacked".
- **Q7 (gateway boundary).** Draw the line as *configuration, not prose*: ADRL's own retry count is zero; the gateway's retries are bounded per turn and never re-issue after first streamed tool content; fallback groups are rung-closed and local-only for pinned traffic; the gateway returns served model/provider identity on every response; overlapping content controls are ADRL-authoritative with the gateway as defence in depth. Shared telemetry via the GenAI semantic conventions.

## Register-wide rules the review proposes

1. Any enum or state set named in a decision is versioned, and the decision cites the version (prompted by CAS-002/MEM-004 vs `outcomes.py`).
2. A D-level certifies behaviour, not text: a decision whose promised property is not implemented cannot exceed D1, whatever its tests cover (prompted by FND-004, SAF-002, SAF-007).
3. Every evidence metric reports its denominator and its excluded fraction (prompted by MEM-005/006, SEM-006, LRN-002).
4. "Tested, not attacked" is a maturity ceiling for SAF: no SAF decision rises above D2 until its adversarial suite has run.
5. Cross-bucket interims (passthrough, fail-open, advisory) must state which gates they still honour.

## What the review could not find

- No peer-reviewed work on LLM-routing cost under provider prompt caching (a 2026 survey lists it as absent).
- No external evidence on the fraction of *coding-agent* turns that are routing-ambiguous beyond vendor claims and this project's own corpus.
- No literature on parent/child escalation semantics with budget propagation for LLM agents.
- No LLM-gateway-specific retry literature beyond vendor documentation.
- Two citations could not be fetched and are flagged as such in the files rather than relied on (Demir et al. "Pitfalls of Hashing"; Madras et al. 2018).

## Provenance and limits of this review

The register text was reconstructed from photographs of the Confluence pages and from Codex walkthroughs of the `cc-local` repository; the reviewers did not have read access to the source code itself. Where the review relies on a code-reality fact (Python-dict session state, six failure types, one verified task, 34/300 evaluated decisions, no graph built) it is the fact as reported in the context pack. Every such reliance is a candidate for correction by someone with the repository open — and the proposed schema tests exist precisely so the register and the code stop drifting apart unobserved.

## 2026-09-03 addendum: external review of the first implementation

A brand-new implementation of this register (`adrl-core`) was built on 2026-09-02 and reviewed externally on 2026-09-03. Eleven concrete claims were verified against the code; nine reproduced exactly, one was right on substance (the development signing key was on disk and unignored, not committed), and one was numerically right but cited the wrong file. The findings and their dispositions:

| Finding | Severity | Register disposition |
|---|---|---|
| Residency and "local" are labels: nothing compares a deployment's geography or host to policy; a local model group pointed at a remote host passed every configuration check and was recorded as never leaving the machine | P0 | TRU-002 proposed (permitted deployment set with signed inventory and served-deployment receipts); FND-002, RTG-001 amended; RTG-008 to follow |
| Repository identity derived by regex from prompt and tool text; unknown repositories fall to a class that permits a cloud rung | P0 | TRU-001 proposed (launcher assertion tied to SCM inventory, content fingerprint, unknown is local-only); SAF-008 superseded in part |
| Egress checkpoints manual, unshipped, verifier ignores signatures, development key loaded unconditionally | P0 | TRU-003 proposed (separate key, automatic checkpoints, off-device anchoring, signature verification, dev-key refusal); SAF-009 superseded |
| Side-effect classifier trusts MCP hints unconditionally and classifies compound commands by first word; read-only calls omitted from the record | P1 | CAS-009 proposed; CAS-003 amended |
| Plaintext paths, remotes, argv and verifier output survive crypto-erasure | P1 | MEM-005 and MEM-010 amended (field-level inventory, erasure proof) |
| Gate observe mode writes durable pins and triggers erasure before the mode is consulted | P1 | OPS decision required (shadow-finding versus pin namespaces); recorded for the OPS draft |
| Multi-file feature counts extensions, not paths; verification snapshot optional | P2 | Implementation defects; no register change |
| Register README names Codex CLI as a harness while FND-001 scopes it out | consistency | SEM-007 proposed; README corrected |

The review also argued, from five 2026 routing preprints, that routing should carry a second, temporal estimand at each safe boundary (continue versus escalate, conditioned on the partial trajectory), that static routers plateau below an oracle, and that replayed transcripts are not counterfactuals. RTG-007 is amended to add the temporal estimand with the static CATE as its baseline and replay prohibited; RTG-001 drops the assumed total capability order. Those sources were not independently fetched and are treated as experiment guides.

The review's governance conclusion is adopted: the implementation is a substantial D1/D2 build, not a complete implementation of the register; the traceability map covers 52 of 55 decisions; and no maturity claim transfers from the prior implementation to the new one.

## 2026-09-07: Product implementation evidence and register synchronization

The product foundation extracts the Messages protocol boundary and Claude Code identity adapter,
adds capability discovery and a versioned product API preview, and records profile/adapter
provenance in decision context. The applied implementation passed 463 tests and all six required
checks. All 25 changed source files matched the tested hashes when this register was synchronized.

FND-001 now explicitly describes the shared engine, adapter/profile boundary and product API.
FND-005 applies measured scope expansion to the first stable interface: two harnesses and two
protocols. SEM-007 records D2 evidence for the extracted Messages boundary and the initial
Responses admission design, while retaining Proposed status for its incomplete full contract.
SEM-002, CAS-007, MEM-001 and TRU-001 record implementation evidence and limits without changing
their policy clauses. The index and affected bucket overviews expose the same status.

This is an implementation evidence update, not a new disposition of the research critique.
Live harness validation, a second adapter, a Responses runtime, and product session/event services
remain pending. The historical findings above remain dated records; they are not automatically
claims about current code. See the [synchronization record](reports/adrl-register-sync-2026-09-07.md)
and [implementation report](reports/adrl-product-foundation-implementation-2026-09-07.md).

## 2026-09-07: Local product services applied

API preview 2 now implements authenticated root-session binding, encrypted observations and
scoped evidence reads, with an isolated Claude Code connection helper and two tool hooks.
The package passed 506 tests and all six required checks. A real loopback HTTP smoke check
used synthetic observations and no model calls. Ten decision records and their bucket views
were synchronized. This supplies scoped D2 service evidence; it does not establish real-harness
D3 maturity or accept every pending proposal. See the [implementation report](reports/adrl-product-services-implementation-2026-09-07.md)
for the credential-forwarding and cancellation fixes, source hashes and outstanding limitations.

## 2026-09-09: RV-01 repair critique and recheck

Claude Fable 5.1 independently reviewed the bounded plan and source/evidence, then rechecked material test additions. [Critique, dispositions and final evidence](reports/reviews/outcome-contract-2026-09-09/report.md). No remaining material blocker for this scope; green final checks satisfy its stated condition. Reviewer did not execute tests; no graduation authority or other-finding closure is implied.

## 2026-09-09: taxonomy-sync local completion workflow

Claude Fable 5.1 performed pre-wave challenge, post-wave review and material-fix recheck of the declared workflow scope. Original findings and dispositions retained; four post-review blockers verified fixed, nonblocking limitations explicit. Final 19 tests and local closure pass on rechecked source. No all-ADR audit, runtime/maturity promotion or remote enforcement claim. [Review folder](reports/reviews/taxonomy-sync-gate-2026-09-09/report.md), [recheck](reports/reviews/taxonomy-sync-gate-2026-09-09/recheck.md), [receipt provenance](reports/reviews/taxonomy-sync-gate-2026-09-09/completion.json).

## 2026-09-09: Claude Code compatibility pre-review

Actual Fable 5.1 source-embedded review returned no-go for current live forced-switch implementation and conditional scouting suggestions. Original review retained; unresolved launch blockers and coordinator disagreements recorded. No post-wave completion, model-task execution or maturity promotion. [Report](reports/reviews/claude-code-compatibility-2026-09-09/report.md), [dispositions](reports/reviews/claude-code-compatibility-2026-09-09/dispositions.md).

## 2026-09-09: Claude initial-choice candidate

Fable independently reviewed the offline implementation, verified the reproduced egress-identity correction and stop wording, then accepted final documentation corrections. Original outputs and coordinator dispositions retained. Local taxonomy receipt passed; seven owners synchronized, formal grades unchanged. Real native operation and ROI remain unqualified. [Completion](reports/reviews/claude-adapter-2026-09-09/completion.md), [final acceptance](reports/reviews/claude-adapter-2026-09-09/final-review.md).
