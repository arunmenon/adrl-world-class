# Roadmap crosswalk: product stages, engineering waves, lab phases

Independent review, frozen snapshot of 2026-09-08 (register hash-verified, 691 entries). Companion table: `roadmap.csv` (42 rows). Assessed states use the six-level vocabulary from the review brief; the highest level the evidence supports is chosen and the basis is recorded per row.

## 1. Summary of the crosswalk

Three plans describe the same program with different units. The product roadmap has eight stages, P0 to P7 (`reports/adrl-product-roadmap-2026-09-08.md`, section 6). The implementation roadmap has twelve waves, W0 and W3 to W12 (`reports/adrl-implementation-roadmap-2026-09-07.md`, section 7), plus two historical waves the plan manifest calls "wave 1/2 evidence". The experiment-lab plan has five phases, Lab A to Lab E (`design/adrl-experiment-lab-plan-2026-09-08.md`, section 8). Two further documents add their own numbering: the multi-harness product contract has stages P0 to P5 that reuse the letter P with a different meaning, and the adaptive-routing blueprint has milestones 1 to 6. The course-correction plan of 2026-09-07 has stages 0 to 5 and experiments E01 to E08.

The evidence state is uniform across all of them:

| Assessed state | Rows | What sits there |
|---|---|---|
| customer-validated | 0 | Nothing |
| independently-evaluated | 0 | Nothing. Every record says `independent_review: false` or equivalent |
| real-harness-demonstrated | 1 | The 2026-09-07 observation pilot: two Claude Code sessions, hooks only, zero routing decisions |
| offline-tested | 18 | W0, the nine W3 sub-slices, W7.0 diagnostic, Lab A.1, W7.0a, and the wave/phase rows they partially satisfy |
| planned | 23 | P0, P2 to P7, W4 to W12, Lab B to E, the deferred custody slice, the planning packs, the Responses spike |

Two facts frame everything else. First, no coding task has ever been executed under ADRL routing on any harness. The one real-harness exercise ran in observation mode and produced zero decisions (`reports/research/adrl-live-observation-pilot-2026-09-07.json`, `adrl_model_requests: 0`, `decision_rows: 0`). Second, no customer conversation has occurred. P0 has no artifacts, and the only named customer setting is disclaimed by the roadmap as historical.

## 2. The causal chain for each substantial piece of work

The test for each piece is: this enables X, which allows measuring Y, which supports milestone Z. Where the chain breaks, I say where.

**W0 baseline (entry 002).** Enables attributable test results per source hash; allows measuring regression and drift across slices; supports every later completion claim. Chain intact. Its one unmet exit item, assigning actual people to review roles, has been carried through nineteen later entries with no owner or date. That single omission blocks independent evaluation for every row in the table.

**W3.1 operator capture (entry 003).** Enables a retained copy of a workspace that survives later edits; allows measuring whether a verifier judged the code the agent left; supports P1's "exact completion/evidence" and P2's attribution. Chain intact and short. Combined with a manual quiesce, it is already sufficient for a bounded real comparison, which is the point the rest of W3 missed.

**W3.2a attempt journal (entry 004).** Enables start, close-request and interruption records; allows distinguishing interrupted attempts from failed tasks in a denominator; supports P2's "count every assigned attempt". Chain intact.

**W3.2b1 process-group runner, W3.2b2a terminal capacity, W3.2b2b2 coordination (entries 005, 006, 008).** These enable process ownership and reserved terminal records for a synthetic command. They allow measuring whether a helper process kept writing after "done". They support a hostile-writer boundary that the frozen W3 packet placed "outside the initial boundary" (`reports/waves/w3-task-capture.md`, item 3). The chain to a product milestone breaks here: no P-stage or lab phase needs group containment before the first real-task comparison. W3.2b1 itself records that a detached child still wrote, so the boundary was not achieved either.

**W3.2b2b1 key revocation (entry 007).** A defect was found by a fault probe (restoring a wrapped key resurrected access) and fixed with a persisted marker. This enables erasure that survives file restoration; allows the erasure claim in MEM-010 to be tested; supports the security owner's data-boundary story for P1. Chain intact. This is the best example in the two days of testing changing the design.

**W3.2b2c writer-boundary probe (entry 009).** Six Docker observations. Enables a decision on whether a container can be the writer boundary; allows measuring what survives client death and host mode changes. Its own recommendation was an optional backend, "not a mandatory Docker dependency". The chain to a milestone exists only for W6/SAF-007 (controlled execution), not for W3, P1 or P2.

**W3.2b2d1 stopped-resource ownership and W3.2b2d2 launch, identity, isolated launch, transport v2 (entries 010 to 014).** Five entries, two failed engine allowances, one repaired timeout mechanism whose historical cause "remains unknown". These enable launching a self-authored static binary in a pinned Docker engine with durable receipts. They allow measuring lost-acknowledgement recovery for that fixture. They support no product stage directly: the roadmap's W3 exit needs a real Claude task with a close handshake; the lab's Lab B needs a real harness profile, which the transport work explicitly does not provide ("Fixture lifetime is specific to the pinned synthetic executable"). This is roughly half of the two-day engineering effort, and it is the clearest case of infrastructure consuming the roadmap, which the product roadmap's own risk table names as a risk.

**W7.0 diagnostic (entry 015).** Enables seeing actual router output across 24 prompts and 5 conditions; allows measuring rule sensitivity to wording and mixed intent; supports P1's "correct mixed-intent defects" and the sequencing amendment. Chain intact and the highest value per hour in the record. It was triggered by the user's inability to connect the executive deck to adaptive routing, not by the plan.

**Lab A.1 workbench (entry 019).** Enables replaying a frozen 16-cell suite through the real composition root; allows measuring selected versus dispatched tier and receipt provenance; supports P1's explanation-matches-execution exit. Chain intact. Four files.

**W7.0a features-v2 (entry 020).** Enables the extractor to see the strongest signal; allows measuring route changes on 720 component decisions with regressions published; supports P1. Chain intact. It also shifts ordinary routing slightly toward frontier (9 to 8 local, 15 to 16 frontier), so its cost consequence is unmeasured until W7 runs real tasks.

**Planning documents of 2026-09-08 (entries 016 to 018): blueprint, product roadmap, investment brief, context-graph proposal, lab plan, lab assessment extension.** Roughly 250 KB of new planning text in one day. They enable a shared vocabulary; they allow measuring nothing; they support a funding decision (P0 entry). The chain to evidence is absent by design. The problem is not that they exist but that they restate one another (section 5).

**PRD/HLD/LLD planning packs (entry 021).** Enable a task type whose assessment is expert judgment; allow measuring nothing until a harness mode is qualified and reviewers are calibrated; support no milestone before P2. This is the second-clearest premature generalisation.

**Executive deck, PDF and review (output directory).** Enable a leadership narrative; allow measuring nothing; supported a briefing that the routing report later said "blurred that distinction" between infrastructure and routing progress.

## 3. Necessary prerequisites that no engineering slice can supply

Each of these blocks P2, which is the stage that tests the thesis. None has an owner or date in the execution state beyond "Codex and product owner".

- A paid or attributable model-run budget (`paid_api_budget_approved: false`). The subscription is not portable credit and gateway credentials change who pays (product roadmap section 4).
- Named independent evaluation and security reviewers (`independent_reviewer_assigned: false`). Without them, no row can rise above offline-tested.
- A concrete real-harness profile: image, network, credential and retention choices (execution state `implementation_gates`).
- Dispositions of DQ1 to DQ4 (evidence origin, deployable baselines, controlled-path availability, release versus routing graduation). DQ3 is visible in Lab A.1: the missing-identity cell responded instead of being rejected.
- An owned or authorized repository set with independent checks for at least three task families.
- The RTG-007 trajectory amendment and LRN-004 time-indexed allowlist, before any P3 adaptation claim.

## 4. Premature generalisation

The following were designed or built ahead of any evidence that would tell whether they are needed:

1. An isolated Docker execution backend with launch, identity comparison and transport policies, before one real task has been captured with the existing operator capture.
2. Planning-document task packs with subjective rubrics, before one coding task has been compared under routing.
3. K0, a version-pinned knowledge snapshot with a compatibility manifest across harness, adapter, deployment and feature versions, before any outcome exists to snapshot.
4. A context-graph projection over MEM, before the existing NumpyIndex and ShadowRetriever (present in `src/adrl/ledger`) have been qualified on any real evidence.
5. Fleet distribution of signed policy packages to developer laptops, described in the investment brief as the "proposed operating model", with no code and no team demand.
6. A seventeen-harness survey and three-harness product matrix, when Anthropic's own guidance rules out the first harness ever exercising the local rung.
7. Detailed P6/P7/W10/W12 improver-versus-improver experiments in five documents, with zero learned artifacts.

## 5. Duplicated planning across the plans

Concrete duplicates, by name:

- The 30-task diagnostic with 90 executions: course-correction E05, implementation roadmap W7, product roadmap P2 (30 tasks), lab plan section 4 (60 or 150 executions), blueprint section 10.
- The two-week, 100-attempt pilot floor: implementation roadmap W8B and product roadmap P3.
- The 15-minute setup target: implementation roadmap W5 and W8B, product roadmap P4.
- The 60-second kill switch and 10-minute restore: implementation roadmap section 6 and product roadmap section 8.
- The 300-label learning minimum: implementation roadmap W9, product roadmap section 8, EVL-004.
- The two-harness, two-protocol gate: FND-005, multi-harness contract P5, course-correction release gate, implementation roadmap W8B, product roadmap P4.
- The first real one-harness comparison: implementation roadmap W7, product roadmap P2, lab plan Lab B, blueprint milestone 3, course-correction stage 4.
- OpenCode as second harness: course-correction 1b, multi-harness contract P3, implementation roadmap W5, product roadmap P4, lab plan Lab C, lab-planning packet step 5.
- Improver A versus improver B: implementation roadmap W12, product roadmap P7, blueprint milestone 6, lab plan section 9, investment brief.
- Open decision lists: DQ1 to DQ8 (implementation roadmap section 9), the twelve-row "Decisions to resolve" table (product roadmap section 10), blueprint section 9 tensions, lab-assessment "Taxonomy disposition required".
- Task families: seven task classes (product roadmap section 7), six families (lab plan section 4 and ADRL-NOW).
- The letter P: multi-harness contract P0 to P5 versus product roadmap P0 to P7. The course-correction plan's "P0-P1 in the product proposal" refers to the contract, so a reader of "P1" has two incompatible meanings on the same day.
- Dependency tracking: the plan manifest still records W7 as depending on W5 and every wave as `proposed` with `implementation_started: false`, while the prose amendment and execution state say otherwise.

## 6. Infrastructure that could be simplified without losing evidence integrity

Evidence integrity in this program rests on three things: source hashes per slice, raw result files, and the eleven engineering checks. Everything else is narrative that repeats them. Candidates for removal or consolidation:

- The dated overlay headers stacked on documents. The product roadmap carries four, INDEX.md more than ten. The execution state JSON already holds the current position; overlays make every document a changelog and hide which sentence is current.
- Nine artifacts per slice (packet, plain-language report, evidence JSON, patch, journey entry, ADR notes, bucket README, INDEX line, CHANGELOG line). The JSON plus the patch plus one journey entry carry all the evidence. Owning-ADR notes could be a link from the JSON rather than prose edits to seven files.
- One validation script per research directory, each recomputing hashes, links and ADR text comparisons. One shared validator with a manifest argument would produce the same records.
- Private source backups per slice under `.adrl-execution-state`, when the repository is under git and hashes are already recorded. A commit per slice would be simpler and more auditable than an uncommitted working tree plus mirrored copies.
- Four leadership views of the same state (executive review, deck, PDF, ADRL-NOW) plus the routing report and investment brief. One product-facing page regenerated from the execution state would end the contradictions documented in the leadership appendix.
- Four planning documents with five numbering systems. One plan with one numbering and one open-decision list.
- The Docker backend as W3 scope. Reclassify as a W6/SAF-007 spike with its evidence retained, and close W3 by binding W3.1 capture to one real task.

## 7. Sequencing corrections

In order of leverage:

1. Run P0 discovery now, in parallel with any engineering. It costs no engineering time and is the only input that can say whether the remaining W3 chain is worth finishing.
2. Make the next engineering packet a five-task, two-arm real comparison (fixed model versus heuristic) on one owned repository under the existing subscription, using operator capture and manual verification. This tests the measurement pipeline before more custody work and gives P2 its first data.
3. Assign reviewers with names and a date. Until then, every "validated" label is self-review.
4. Bring W6 slice 1 (controlled listener rejecting missing identity) forward; it is small and offline, and P1's exit needs it.
5. Freeze the W7 comparison packet with a budget line. Merge Lab B, P2 and the first W7 packet into one packet.
6. Park the planning-document packs, K0 design, context-graph proposal and OpenCode adapter until P2 has a result.
7. Update the plan manifest so its dependency graph matches the amended prose, or retire the manifest.

## 8. The startup premise

Sources: `reports/adrl-startup-investment-brief-2026-09-08.md`, `reports/adrl-product-roadmap-2026-09-08.md`, `reports/adrl-product-report-2026-09-03.md`.

**Initial buyer and user.** Buyer: VP Engineering or CTO; champion: platform lead; user: developer keeping their harness. Segment hypothesis: 50 to 300 engineers, existing model API or gateway budget, repositories with meaningful tests. The brief calls this "an assumption for discovery, not a validated customer segment". No conversation has tested it.

**Painful problem.** "A cheap model call can lead to an expensive task if the developer must retry, repair and review it repeatedly. An expensive model can also be wasteful on simple work," plus evidence a buyer can defend. Plausible, but the register contains no customer artifact showing that any team has this problem at a size worth a vendor.

**Alternatives.** The roadmap names Not Diamond Code, LiteLLM auto-routing, Portkey, Copilot Auto, and "fixed model plus ordinary engineering controls", the last being "a serious customer alternative and a mandatory experimental comparator". The 2026-09-03 report's competitive framing ("no enterprise gateway or vendor auto-router has a local rung as a target") is contradicted five days later: "Local placement and session awareness are insufficient differentiation" and "Do not repeat the blanket claim that vendor routers hide served identity."

**Differentiation.** The current claim is a combination: customer-controlled routing, outcomes tied to exact work, reusable policies across qualified harnesses. The roadmap concedes "Each element has competitors" and that the combination is an advantage "only if customers obtain a worthwhile result more easily than with alternatives". The original headline differentiator, the local rung, cannot be exercised on the first harness: "Anthropic does not support routing Claude Code to non-Claude models through gateways; do not market this trial as local-model or cross-provider routing." The first product is therefore Claude-to-Claude tier selection on Claude Code, which is the space Copilot Auto and Not Diamond already occupy.

**Installation and integration burden.** From the course-correction startup sequence: isolated config directory, five environment variables, signed repository classification and endpoint inventory, a new key set and anchor, a pinned LiteLLM gateway with provider credentials, ADRL serve, a launcher-signed workload assertion, base-URL override and session ID in the harness, plus hooks for observation. The product roadmap's 15-minute target is untested. The runtime is single-process, single-user, with no hosted CI and preview-4 API.

**Operational and support cost.** Unknown and unmodeled. The roadmap's cost figure of $1,000 incremental monthly cost is an invented planning input. The team model is four technical people plus a founder plus part-time reviewers.

**Evidence acquisition cost.** Modeled: $270,000 for 90 days ($180,000 people at $15,000 loaded per person-month, $15,000 evaluation compute, $15,000 independent review, $15,000 operations, $45,000 contingency). Observed: the only measured model spend in the record is $0.1172 and $0.1749 API-equivalent for the two pilot sessions ($0.2921 combined, harness-reported, not an invoice), and zero for every synthetic run. The two-day engineering effort itself is uncosted.

**Path to repeatable value.** P2 comparison, then P3 with two design partners and one paying continuation, then P4 reusability. The commercial hurdle is "confirmed net value at least three times the subscription fee". Nothing in the record is on that path yet beyond P1's component work.

**Falsifiable stop or pivot criteria.** Present and reasonable at each stage (P0: no controllable budget or alternatives suffice; P2: quality loss, negative net value, no advantage over a practical alternative; P5: keep rules or a bought selector; P7: no reproducible improver advantage). Missing: a stop rule for infrastructure, such as "no further W3 sub-slice without a dated real-task comparison packet", and dates or owners for the P0 decision.

**Modeled versus observed economics.** All customer economics are modeled with declared invented inputs: $40,000 monthly addressable spend, $1,000 incremental cost, $1,500 fee; scenarios at 25/50/75 percent coverage and 10/20/30 percent reduction giving gross $1,000/$4,000/$9,000 and net -$1,500/$1,500/$6,500; cash break-even at $25,000 monthly spend; a $1,000 to $3,000 per team per month price anchor. Sources: product roadmap section 11 and `product-roadmap-2026-09-08/validation.json` (`illustrative_economics_recomputed`). The only observed figures are the two pilot session costs and wall times (54.1 s and 96.9 s), and the roadmap correctly says they are unsuitable for comparison because the harness version changed between runs. There is no observed routing saving, no observed quality delta, and no observed developer time.

The premise is coherent as a hypothesis and the documents are unusually candid about it. The risk is not the premise but the ratio: two days produced fourteen offline engineering slices, six planning documents and three leadership views against zero customer signals and zero real routed tasks. The roadmap's own sentence applies: "More infrastructure is justified when it removes a named obstacle to that proof."
