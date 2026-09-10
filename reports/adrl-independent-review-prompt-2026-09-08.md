# Independent ADRL product, architecture and implementation review

**Prepared for Fable 5.1. Review window: 7–8 September 2026, Asia/Kolkata, through the accompanying inventory timestamp.**

Copy this entire prompt into a reviewer with filesystem access to the repositories below. This is a review assignment, not a report of a review already performed. The inventory is a discovery aid, not proof that its files or their claims are correct.

## Your assignment

Act as an independent CTO, product architect and evaluation reviewer for ADRL. Thoroughly review the work performed during these two days. Determine whether it advances the product roadmap and the architecture decision register, where maturity has actually improved, where claims exceed evidence, and what we should do next.

Be willing to disagree with the implementation author, earlier research critiques, and the current roadmap. Also recognize sound work: do not manufacture defects to appear adversarial. Start from evidence, not from an assumed verdict. Explain your conclusions in intuitive language for a product lead and senior leaders, supported by precise technical appendices.

The central question is: **Are we building a useful, context-aware adaptive routing product, or accumulating infrastructure and documents without proving better routing and customer value?** Evaluate both possibilities fairly.

## Product intent against which to review

ADRL is intended to make routing decisions on a developer's laptop across local, economical cloud and frontier model deployments. These are economic/capability options, not three vendor categories. It should integrate with different harnesses through a coherent API and explicit capability contracts, starting with Claude Code and subsequently another harness.

Routing should consider the request, available context and relevant trajectory, subject to privacy, permissions, protocol and operational constraints. MEM already belongs to the taxonomy: it records attributable experience and supports usable memory. A context graph is a candidate way to organize/retrieve that experience, not inherently a proven improvement. Offline learning should convert qualified outcomes into compatible, versioned knowledge or policy snapshots distributed to local installations. Thousands of laptops are a future scale objective, not an existing deployment claim.

Distinguish three improvements throughout: (1) an engineer or coding agent changes a routing rule; (2) an offline learner derives a better checkpoint from outcomes; (3) RSI improves the process that creates and qualifies those checkpoints. None automatically proves the next. The user also wants planning work such as PRDs, HLDs and LLDs included, with appropriate treatment of subjective quality. Assess whether that expansion supports or dilutes the initial product focus.

## Access, scope and preservation

- Architecture register: `/Users/arunmenon/projects/adrl-world-class` (call this R).
- Runtime: `/Users/arunmenon/projects/adrl-core` (call this C).
- Evidence map: `R/reports/research/independent-review-handoff-2026-09-08/README.md`.
- File inventory and hashes: `R/reports/research/independent-review-handoff-2026-09-08/manifest.json`.
- Read both repositories' `AGENTS.md` and applicable instructions first.

Inventory current tracked, modified and untracked files. Much of C is untracked: **Git diff alone cannot establish the work done.** Reconcile Git history, source snapshots, dated patches, manifests, journal entries and before/after evidence. Do not infer when a change occurred from modification time alone. The W0 baseline is an in-window checkpoint, not necessarily the start of 7 September. Mark unavailable pre-window baselines as unknown; do not attribute all current code to these two days.

Include 3 September reports and historical `source/` as context for what was challenged, not as two-day implementation achievements. Read every journey entry, and identify earlier 7 September work that predates the journey. Follow citations to code and raw evidence rather than stopping at summaries. Independently discover work omitted from the supplied map. Changes after the inventory timestamp must be reported separately.

Keep this a review. Do not edit implementation, tests, taxonomy, expected outcomes, historical evidence, scheduler settings or source repositories; do not commit or submit fixes. Write review outputs to a new directory outside both repos, such as `/Users/arunmenon/projects/adrl-review-fable-2026-09-08/`, without overwriting an existing review. No paid/model calls, engine/container mutations, live routing or real developer payload experiments are authorized by this assignment. Existing subscriptions and past bounded execution approvals are not blanket experiment authority.

You may inspect scripts and run bounded offline checks in a disposable copy with synthetic inputs and isolated output, after confirming their side effects. Do not blindly rerun validators: some overwrite historical evidence or depend on ambient configuration. Record commands, source hashes, outcomes, skips and limitations. Do not install dependencies or escalate exposure merely to complete a review. Do not read or publish credentials, `.env`, private keys or unrelated developer data. Use declared source scopes and cited source-only snapshots. If a test cannot be safely run, label it unverified and specify the missing prerequisite.

If filesystem or web access is missing, identify precisely what is unavailable. You may deliver a partial review but must label it partial. Never claim code inspection, reproduction or source verification from an executive summary alone.

## Required review method

### 1. Reconstruct the actual two-day change set

Build a chronology and workstream ledger with: intended outcome, files changed, baseline, behavior before/after, claimed validation, independently inspected evidence, outstanding work, roadmap stage and owning ADRs. Include abandoned approaches, failed candidates, repair cycles and disqualified runs. Separate new implementation, bug fixes, experiments, research, specifications, reporting and prepared-but-unexecuted task packs.

Audit all of these workstreams, including any additional ones you discover:

1. Independent research review and register synchronization; course-correction plan; revised product/integration contract.
2. Public APIs, session identity, event/timeline services, capabilities, verification and protocol profiles; whether advertised contracts are actually enforced.
3. Live observation and Claude subscription pilot: what was observed versus controlled, which harness/model actually ran, and what outcomes were verified.
4. Verifier/improvement experiments and their archive, outcome attribution, independence, exact-output and recovery limitations.
5. W0 baseline and the complete W3 capture/attempt/process/resource chain: operator capture, attempt journal, terminal capacity, key revocation, coordination, writer boundary, stopped ownership, launch identity, isolated execution and transport receipts. Include failed launch/recovery evidence and unfinished custody/extraction work.
6. Routing demonstration, synthetic workbench Lab A.1, invalid first export, corrected export, and W7.0a mixed-intent repair, including the failed intermediate candidate.
7. Product roadmap, engineering waves, lab phases, RSI blueprint, context graph proposal, offline checkpoint/distribution plan and unresolved architectural dispositions.
8. Planning/mode/assessment proposal and PRD/HLD/LLD starter packs: contracts prepared versus runnable integration versus assessed task results.
9. Executive reports/decks, running journey, ADRL-NOW, progress skill and execution/automation state: accuracy, contradictions and whether a nontechnical leader could reasonably overinterpret them.

### 2. Judge product progress and sequencing

Crosswalk product P0–P7, engineering W waves and Lab phases using their actual definitions. For every stage, distinguish planned, implemented, offline-tested, real-harness demonstrated, independently evaluated and customer-validated. Do not invent completion percentages.

For each substantial piece of work explain the causal link: “this enables X, which allows us to measure Y, which supports product milestone Z.” Identify necessary prerequisites, premature generalization, duplicated planning, and infrastructure that could be simplified without sacrificing evidence integrity. In particular, challenge whether the next W3 prerequisite is the minimum needed for a credible real-task demonstration, or whether a narrower safe path exists. Do not bypass a genuine privacy or attribution gate just to show progress.

Evaluate the startup premise: initial buyer and user, painful problem, alternatives, differentiation, installation/integration burden, operational/support cost, evidence acquisition cost, path to repeatable value and falsifiable stop/pivot criteria. Distinguish modeled economics from observed economics. Specify what leadership can honestly be told today and what remains an investment hypothesis.

### 3. Audit all ADRs and their maturity

Read the entire current register, INDEX, bucket overviews, CHANGELOG, REVIEW-LOG and the maturity baseline. Enumerate IDs from files and independently compare with INDEX; the expected count is 77, but report discrepancies rather than forcing that number. Use the taxonomy's actual buckets and EVL-007 definitions, not a generic maturity scale.

Produce **one row for every ADR**, including unchanged records. Columns: ID/title; baseline status and maturity (or unavailable); current recorded status and maturity; two-day decision/application/evidence changes; runtime/test references; scope actually supported; your assessed maturity or inability to assess; limitations; next promotion gate; associated product milestone. Separate architectural acceptance from implementation maturity and narrow tested behavior from the whole ADR's promise. Do not average ordinal grades into a product percentage.

Check that every behavior change has an owning ADR, scoped application or decision update, preserved prior wording/changelog, synchronized INDEX and overview, and valid evidence links. Check reverse traceability: every claimed ADR implementation or maturity improvement must resolve to code and qualifying evidence. Flag both unsupported promotions and records that conceal meaningful tested progress by failing to describe its scope. Recommendations must not silently alter the ledger.

### 4. Deeply inspect the routing product

Trace representative requests end to end: harness inputs and identity → context/features → permission/protocol gates → selected route → actual dispatch/served identity → cascade → outcome/ledger. Explain three examples in plain language, plus one failure or limitation. Cite real traces; label any illustrative hypothetical.

Review intent extraction and the features-v1/v2 change, overlap handling, ordinal typo fixes, strongest lexical match, concurrency handling, context/trajectory signals and thresholds. Challenge unseen mixed intents, negation, quoted words, explanation versus modification, long irrelevant versus meaningful context, ambiguity, and multilingual or unfamiliar task wording where relevant. Determine which deficiencies existed before, which were introduced, and which remain. Do not use agreement with author-assigned heuristic labels as proof of optimal model selection.

Verify exploration and learning-contract compatibility, fail-closed behavior, startup versus dynamic state, failure attribution, permission narrowing, sticky pins, cascade constraints, streamed errors and served-endpoint uncertainty. Distinguish initial route, later dispatch and hindsight quality. Separate runnable production paths from diagnostic overrides or fixtures, especially synthetic SHADOW-bundle injection into LIVE test composition.

Assess integration honestly: reusable API contract versus hardwired Messages fixture; real harness adapter versus a harness-name enum; control versus observation-only; task phase versus native harness mode versus model reasoning/settings. Check SEM-007 Responses admission and FND-005 interoperability gates. Specify what must be proven before claiming a second harness or protocol is supported.

### 5. Inspect MEM, learning and RSI as one evidence loop

Trace how a decision becomes an attributed outcome, an eligible example, a candidate checkpoint, a qualified comparison, a released compatible package and a local action. Mark every missing link.

Check exact artifact/tree identity, independent verification, late/corrected outcomes, causal label cleanliness, decision-time feature availability, graph provenance and retrieval authority, temporal leakage, tenant/privacy boundaries, encryption, key destruction versus surviving plaintext/WAL/output copies, and recovery after process death. An append-only ledger is not by itself useful or safe memory.

Check MEM-008 advisory authority and the current LRN-001 eligibility contract, including synthetic/curated versus organic examples. Distinguish prediction of task difficulty from estimating comparative routing benefit. Compare graph enrichment with a simpler feature/retrieval baseline; require an ablation before claiming value. Inspect LRN versioning and exploration incompatibilities after features-v2.

For RSI require a testable proposed loop: champion/challenger, independent held-out outcomes, safety constraints, promotion authority, rollback and drift monitoring; then a separate comparison of the improvement process itself, including cost. State whether any such improvement is implemented, measured or merely planned. A manually repaired rule or successful synthetic replay is not autonomous RSI.

### 6. Audit experimental validity and task diversity

Inspect raw inputs, outputs, journals, manifests, source hashes, graders and negative results. Reconcile every published count. Do not add passing tests across source revisions; do not count repeated conditions as independent tasks, endpoint responses as solved tasks, or in-process synthetic transports as real harness runs.

Review the early verifier experiment, routing demonstration, 16-cell lab, original/fresh before-after matrices and planning starter pack separately. Check test leakage, author-built expectations, reuse of cases, candidate selection bias and regression coverage. Retain the invalid first lab export and failed first routing candidate in the explanation. Check whether archived passing results match current source, and whether engine tests passed historically but were skipped in a later offline run.

Assess diversity across task family, repository/language, context structure, difficulty, uncertainty, tool trajectory, privacy constraints, deployment, harness/version/mode and failure type. Identify empty cells. A large matrix produced by repeating a few prompts is not a broad benchmark.

For PRD/HLD/LLD distinguish deterministic constraints, expert rubric assessment and later utility/rework. Examine critical defects, missing assumptions, blinded independent review, judge calibration/agreement, order/verbosity/self-preference biases, abstention, uncertainty and assessment cost. Check that subjective scores cannot silently enter an objective/organic training contract, and that simulated rubrics do not imply reviewers were assigned. Separate a portability test from a causal harness/model comparison; identify confounders and pin versions/settings/inputs/artifacts.

### 7. Check research grounding and operational guardrails

Independently verify high-impact scientific and vendor claims on which changed or proposed decisions depend. Start with existing source ledgers, then fetch primary papers/docs where accessible. Check actual publication date, method, benchmark, counterevidence and applicability. Distinguish fetched from search-only references. Prioritize escalation economics, prompt versus trajectory routing, outcome-conditioned learning, model/protocol constraints, compaction/identity/receipts and isolation/erasure assumptions. Explain what you did not recheck; do not present a citation count as an independent literature review.

Check authorization boundaries, bounded repair/run limits, failure preservation, source/evidence ownership, disabled automatic graduation, paused continuation and unresolved independent-review gates. Security review by a language model does not itself satisfy every formal human/independent graduation requirement. Report concrete violations or missing proof, not generic warning lists.

## Required deliverables

Write a polished main report plus machine-readable appendices. Use short plain-language explanations in the main report and file/line or evidence-record references for auditability.

1. **Executive verdict:** what can actually be done today; whether the last two days moved us toward adaptive routing; strongest accomplishment; greatest gap; where investment should go next. Give scoped continue / conditional continue / pause / rethink recommendations with confidence and reasons, not one inflated global readiness label.
2. **Two-day change ledger and coverage table**, including work before the first journey entry and material failed/abandoned candidates.
3. **Roadmap crosswalk** covering product stages, engineering waves and lab phases: actual evidence, unmet exit gates, dependencies and sequencing corrections.
4. **Full ADR maturity matrix** with one row per actual ADR and a concise explanation of what improved without a formal grade change. Preserve unknown baselines.
5. **Prioritized findings:** severity, confidence, affected files/ADRs, claim versus observation, reproduction or inspection evidence, product consequence, recommended correction and measurable acceptance criteria. Separate observed defects, unsupported claims, missing experiments and strategic disagreements.
6. **Learning-loop and integration assessment:** one simple diagram showing implemented/tested/planned links, and a capability matrix for harnesses, protocols, modes, task types, memory, offline learning and RSI.
7. **Leadership claims:** safe to say now / only with qualification / not yet supported. Audit the actual deck/report language, not just current source.
8. **Next three bounded implementation slices:** why each is next, owning ADRs, prerequisites, outputs, meaningful tests, stop conditions, authority needed and exact promotion gate. Include the smallest credible end-to-end demonstration from real task → observed routing → attributed quality/cost/latency → evidence-backed course correction. If it cannot fit three slices, say so.
9. **Coverage and reproducibility appendix:** every inventoried file assigned deep-reviewed, supporting-read, generated/duplicate, historical-context, not-reviewed or inaccessible, with reasons; commands actually run; source mismatches; open questions and missing evidence. No claim of exhaustive completion while material areas remain unreviewed.

Suggested output files: `review.md`, `changes.csv`, `roadmap.csv`, `adr-maturity.csv`, `findings.md`, `coverage.csv`, and `review-manifest.json`. Record review date, input inventory hash and output scope. Finish by answering: **“What would convince us that ADRL is becoming a better adaptive router, rather than simply a more elaborate system?”**

Do not begin by paraphrasing the author's progress report. Begin with the access/inventory check, establish a review checklist, inspect the evidence, and then form your own conclusions. If context limits require multiple passes, persist a coverage ledger and resume it; never silently drop older workstreams.
