# ADRL independent review: 7 to 8 September 2026

Reviewer: Claude Fable 5.1, interactive Claude Code session `session_011qFLwZ3EjPPrB3QqneJa63`, invoked by the product owner through `/adrl-critical-review`. Review date: 8 September 2026 IST. Input inventory: `reports/research/independent-review-handoff-2026-09-08/manifest.json`, 691 files, verified byte for byte at freeze and again at the end of the review (zero drift). Output scope: both repositories, the product roadmap, all 77 ADRs. This is a review, not a fix; no repository file was modified, no maturity was promoted, no model was called for ADRL, no scheduler was touched. The supporting evidence is in `appendix/`; the finding register with stable IDs is `findings.md`; the machine-readable tables are `changes.csv`, `roadmap.csv`, `adr-maturity.csv`, `coverage.csv`, `review-manifest.json`.

## 1. Executive verdict

**What ADRL can actually do today.** It can sit in front of Claude Code as a transparent proxy, classify each request, detect secrets in tool results, pin a session to local-only durably, write an append-only ledger and a hash-chained egress ledger, and record which model tier a keyword rule chose. In a synthetic lab it can show that choice reaching an in-process fake endpoint. It observed one real Claude Code session (18 tool events) without making a routing decision. It cannot yet choose the middle tier on merit, learn from any outcome, reproduce its own lab results on another machine, or demonstrate a routed real task.

**Did the two days move us toward adaptive routing?** Partly, and less than the volume of work suggests. The genuine advances are process advances: a repeatable observe, amend, replay, check loop with retained failed candidates; hash-chained evidence manifests; capture and session-verification that survive later edits; honest prose about limits. The routing decision itself did not become adaptive. It moved from one lexical rule to a better lexical rule, and the rule is the whole router: the estimator, thresholds and cost model that the register describes are inert in the shipped configuration (RV-02). Roughly half of the engineering effort went into a container execution backend that no product stage needs (RV-30).

**Strongest accomplishment.** The evidence discipline. Every test count from 549 to 911 matches an on-disk log; every W3 evidence hash chains to the frozen source; failed candidates, disqualified runs and an unexplained lost receipt were kept rather than tidied away. That discipline is what made this review possible, and it is rarer than working code.

**Greatest gap.** The evidence loop is severed at its first link. The cascade writes outcome transitions under one event type and every consumer reads another (RV-01), so no organic decision can ever become an attributed outcome, a label, a readiness count or a training example. Everything downstream (tiers, pairs, estimators, abstention, exploration) is well tested and unreachable. Combined with the inert estimator, the system records decisions it cannot learn from and makes decisions the ADRs do not describe.

**Where investment should go next.** Fix the pipe, make the decision real, then run the smallest honest real-task comparison. Not more infrastructure, not planning packs, not a context graph, not a second harness.

Scoped recommendations, each with confidence:

| Scope | Recommendation | Confidence | Reason |
|---|---|---|---|
| Evidence discipline, W3.1 capture, session verification, egress ledger | Continue | High | Sound, reproducible, and needed by every later step. |
| Outcome pipe (MEM-002 lifecycle, closer, labels, readiness) | Continue as the next slice, blocking everything else in learning | High | RV-01, RV-05 to RV-09 are correctness defects with clear fixes and tests. |
| Routing decision (RTG-002/003/006, features-v2) | Conditional continue | High | Condition: the estimator must be able to change a decision, the lab must be path-independent and load in the mode it runs, and an over-route budget must be stated (RV-02, RV-03, RV-04, RV-17). |
| Container isolated-execution chain (W3.2b1 to W3.2b2d2, active-copy custody as prerequisite) | Pause | High | It cannot host a real harness and no product stage requires it (RV-10, RV-30). Reclassify as a W6 or SAF-007 spike. |
| Planning packs, context graph, K0 checkpoint and distribution, RSI blueprint implementation | Pause until P2 has a result | High | No ablation baseline exists and no organic example can reach them (RV-31, EL M4, M5). |
| Register maturity display and leadership artefacts | Rethink the presentation, not the ledger | High | Historical D3 and D4 grades shown as current, index stale for 21 decisions, executive materials frozen at entry 014 (RV-12, RV-23, RV-25). |
| Independent review process | Rethink | High | Twenty-one "validated" labels without a named reviewer (RV-13). This review is the first, and it arrived after the claims. |

**The central question answered plainly.** ADRL is not yet a demonstrated adaptive router. It is a well-instrumented control layer with a keyword router in front of it and a learning stack behind a broken pipe. The instrumentation is the asset. Whether it becomes an adaptive router depends on the three slices in section 8, each of which is small.

## 2. Two-day change ledger

The full ledger is `changes.csv` (48 items) with the narrative in `appendix/chronology.md`. The order was fixed without Git: the six pre-W0 runtime packages chain by manifest hash, and the W3 chain is ordered by fifteen backup directory names whose recorded check-manifest hashes match disk.

**7 September, before journey entry 001 (23:44 IST).** Independent research review; register synchronisation; course-correction plan and baseline; multi-harness product contract; product foundation (14:18, 463 tests); product services (15:46, 506); Claude subscription pilot preparation; observation mode (16:12, 511); two real Claude Code sessions; session verification (16:39, 532); improvement experiment (18:15, 549); the implementation roadmap. Then W0 baseline.

**8 September.** W3.1 operator captures; W3.2a attempt journal; W3.2b1 process ownership; W3.2b2a terminal capacity; W3.2b2b1 key revocation (spawned by a key-resurrection defect); W3.2b2b2 process coordination (three focused repair cycles); W3.2b2c writer boundary; W3.2b2d1 stopped-resource ownership; W3.2b2d2 launch contract, identity and transport (two failed launch runs with zero of six cases accepted, two failed engine runs, a failed and a cancelled combined check, one unexplained lost create receipt); W7.0 routing diagnostic (two failed review hypotheses); Lab A.1 (run 1 disqualified by a manifest key collision, run 2 accepted); W7.0a routing correction (candidate 1 failed the sticky-cascade test, candidate 2 accepted); product roadmap, RSI blueprint, context-graph proposal, lab plan, planning starter packs, executive review and deck, ADRL-NOW.

By kind: 16 implementation items, 8 specifications, 6 reporting, 4 research, 4 prepared-not-executed, 3 bug fixes, 2 experiments, 3 discovered outside the author's map (the executive deck built outside the snapshot, two paid reviewer calls for the skill smoke test, one slice fetching source over the network). Twenty failed or repaired items are itemised in the chronology.

**Counts reconciled.** 322 source hashes in the final check manifest match the frozen runtime 322 of 322. `tests.log` reads 911 passed, 8 skipped; the 8 are the Docker-gated engine cases, skipped whenever `ADRL_RESOURCE_*` is unset, which passed once on the 316-input build and have been skipped since. The 720 decisions are `before.json` plus `after-final.json` (360 each); candidate 1's 360 are uncounted. The 240 demonstration decisions are in `results.json`. Reproducing the suite off the author's path gives 906 passed, 5 failed: four need the excluded dev key, one is the path dependency of RV-03.

**After the inventory timestamp.** Only the handoff folder's own files changed. Seven register documents were edited between the 08:45Z correction validation and the inventory, consistent with journey entry 021.

## 3. Roadmap crosswalk

`roadmap.csv` has 42 rows: product stages P0 to P7, waves W0 through W12 with sixteen executed slices, lab phases A to E. Assessed state across all rows: 0 customer-validated, 0 independently-evaluated, 1 real-harness-demonstrated (the 7 September observation pilot, which made zero routing decisions), 18 offline-tested, 23 planned. No coding task has ever been routed by ADRL on a real harness. No customer conversation has occurred; P0 has no artefacts and the roadmap disclaims the named customer.

Causal chains that hold: W0, W3.1 capture, W3.2a journal, the key-revocation fix, the W7.0 diagnostic, Lab A.1 and W7.0a each enable a named measurement that feeds P1 or P2. Chains that do not hold: W3.2b1 through W3.2b2d2 (process runner, capacity, coordination, Docker probe, stopped-resource ownership, launch, identity, transport) support no product stage; the W3 contract never required a container backend and W3.2b2c called it optional.

Unmet exit gates, by stage: P0 needs any buyer evidence; P1 needs a real selector (RV-02), honest live loading (RV-04) and path independence (RV-03); P2 needs a real-task comparison with attributed outputs, which the next stated W3 step does not reach (RV-10); every later stage needs the outcome pipe (RV-01).

Sequencing corrections in priority order: run P0 discovery now in parallel with engineering; make the next packet a small two-arm real comparison on one owned repository under the existing subscription using W3.1 capture and manual verification; name reviewers with a date; bring the controlled-listener slice forward; merge Lab B, P2 and the first W7 packet, which are the same work under three names; park planning packs, K0, the context graph and OpenCode until P2 has a result.

Duplicated planning: five numbering systems (product P0 to P7, contract P0 to P5, waves W0 to W12, blueprint milestones 1 to 6, lab phases A to E, plus course-correction stages); the 30-task diagnostic appears in five documents; pilot durations, setup targets, rollback windows, label counts, the two-harness gate and the open-decision lists are each repeated two to five times. The plan manifest JSON still says W7 depends on W5 and every wave is proposed.

Startup premise: the documents are candid and the hypothesis is coherent, but the original differentiator (a local rung) cannot be exercised on the first harness under the vendor's guidance, so the first product is Claude-to-Claude tier selection on Claude Code, the space already occupied by vendor auto-routers. All economics are modeled from inputs the brief itself calls invented; observed spend is under one dollar across two sessions. Leadership can honestly be told that implementation risk has fallen and that routing-value and demand risk are untouched.

## 4. ADR maturity matrix

`adr-maturity.csv` has one row per ADR (77 rows; files, INDEX, inventory and the 7 September baseline all reconcile at 77; 55 files are in the 2 September commit and 22 are untracked). All 77 Status and Maturity fields are byte-identical to the 7 September baseline, so the "no promotion" claim holds. Against the EVL-007 definitions for adrl-core's tested scope: 36 records agree with their recorded level, 16 are recorded higher than the evidence supports, 25 are recorded lower.

Recorded higher: the historical D3 and D4 claims (for example CAS-001, RTG-003, MEM-008, SAF-003, SEM-002) that EVL-007 rule two says cannot transfer to a new implementation, plus SAF-007's D2 for a decision whose read isolation and allow-list remain unmet. Recorded lower: eleven fields that still describe defects closed on 3 September (SAF-008, SAF-009, CAS-009, TRU-002, TRU-003, OPS-002, OPS-003, OPS-005, OPS-007, RTG-009, LRN-006) and fields for LRN-003, LRN-004, LRN-008, EVL-005 and TRU-001 that contradict their own 8 September body text or the INDEX.

What improved in the window without a grade change, by bucket: MEM and OPS gained tested capture, journal, coordination and revocation mechanics (large tested progress attached to OPS-001 and SAF-007, neither of which covers container execution: RV-34); LRN-004 gained the features-v2 snapshot and the exploration compatibility guard; RTG-002/003 gained the lab and the correction record; EVL-005 gained a lab that labels synthetic evidence as such. What did not improve: any decision depending on organic outcomes, because none can be produced (RV-01).

Traceability: forward traceability from runtime patches to ADR sections is sound. INDEX rows omit the five latest W3 slices for eight ADRs and every 8 September routing item for thirteen ADRs, although each changelog entry says the index was synchronised (RV-23). Reverse traceability fails where the claim rests on the old codebase (RV-14) or on a path-bound run (RV-03).

## 5. Prioritised findings

Forty findings are in `findings.md`: one critical, fifteen high, sixteen medium, eight low, each with kind, confidence, file references, claim versus observation, product consequence, correction and acceptance criterion. The ones that change what we should do:

1. RV-01 (critical): the outcome pipe is broken; nothing organic can become a label.
2. RV-02 (high): the estimator and thresholds are inert; the middle tier is unreachable on merit.
3. RV-03, RV-04 (high): the routing evidence is path-bound and reached live dispatch through an undisclosed shadow-mode bypass.
4. RV-10, RV-30 (high): the stated next W3 step cannot reach a real-task demonstration, and half the effort went there.
5. RV-12, RV-13 (high): grades the build has not earned are displayed as current, and no reviewer has ever been named.
6. RV-16, RV-15 (high): two experiment records whose summaries overstate what their bodies concede.

Blocking dispositions: RV-01 blocks any MEM-002 lifecycle or readiness claim; RV-02 blocks RTG-002 D2 for the shipped configuration; RV-03 and RV-04 block the W7.0a and Lab A.1 "validated" labels; RV-13 blocks every self-assigned "validated" label pending an owner decision on how to treat them retroactively; RV-29 requires an owner disposition for the closed W3.2b2d2 slice.

Strategic disagreements with the author, preserved as such: strongest-signal lexical aggregation moves error from under-routing to over-routing without a stated price; destructive-intent vocabulary is treated as a capability signal; path-bound developer configuration is treated as product configuration; the harness-adapter abstraction is ahead of its evidence; the learning stack was built ahead of the outcome pipe; task diversity should come from other people's work rather than more author prompts.

## 6. Learning loop and integration assessment

```
decision ──► pending event ──► closed_turn ──► closed_final ──► verification ──► label ──► tier ──► example ──► pairs ──► estimator ──► abstention ──► artifact ──► graduation ──► local action
 tested      tested BUT        tested BUT       never fires     tested, no      tested,   T1        blocked    never run   tested on    tested on    tested,     human-only,  planned
             invisible to      invisible to     on live path    precision       ignores   unreach-  by v2      (0 counter- synthetic    stub         refuses      none         (K0, W11)
             consumers         consumers        (RV-01)         record (RV-07)  correc-   able      contract   factual                            unsigned
             (RV-01)           (RV-01)                                          tions     (RV-07)   (RV-08)    events)                            (correct)
                                                                                (RV-06)
```
Implemented and tested in isolation: every box. Measured on organic traffic: none. The first three links fail on the live path; retrieval and embeddings are never composed (RV-31); rule-health refresh is not wired (RV-18). RSI has no champion and challenger, rollback, drift monitoring or improver-cost code; the blueprint states them as plans and does not distinguish predicting per-arm success from estimating comparative benefit. A manually repaired rule and a synthetic replay are what exists; neither is autonomous RSI, and the register mostly says so.

Capability matrix (state the evidence supports):

| Dimension | State |
|---|---|
| Harnesses | Claude Code: transparent passthrough and one native observation pilot; no routed real task. OpenCode, Codex: none. Adapter is a header extractor with one implementation; Claude Code tool names are parsed directly in gates, features and cascade. |
| Protocols | Anthropic Messages: implemented. OpenAI Responses: scope document only; SEM-007 admission not attempted. |
| Modes | Shadow: implemented. Live: refuses to load without evidence references; the lab reaches it through a shadow-loaded bundle (RV-04). Gates enforce or observe: implemented and tested. |
| Task types | 36 author-written synthetic prompts, 6 distinct lab prompts, 3 planning packs unexecuted; no repository, language, difficulty or user diversity. |
| Memory | Append-only ledger and egress ledger: implemented, tested, hash-verified. Outcome lifecycle: broken on the live path (RV-01). Retrieval and embeddings: never composed. Erasure: key shredding tested; physical, backup and active-copy erasure unqualified. |
| Offline learning | Tiers, dataset, pairs, estimators, abstention, artifacts: tested on synthetic data, unreachable from traffic (RV-07, RV-08). No branched pair has ever run. |
| RSI | Planned. The improver is a person. |

## 7. Leadership claims

Full audit of 37 quoted claims and 12 cross-document contradictions is in `appendix/leadership-claims.md`.

Safe to say now: ADRL runs as a transparent proxy on Claude Code traffic; secrets in tool results pin a session durably; every request leaving the machine is ledgered with a hash chain; failed experiments are retained; automation is paused and no paid budget or live exposure has been approved; the register has 77 decisions and no grade was changed in the window.

Only with qualification: "911 tests pass" (on the author's path with the dev key; 8 engine cases skipped since the 316-input build); "the controlled endpoint received the frontier request" (under a developer manifest entry and a shadow-loaded bundle); "we observed a real Claude Code task" (observation only, zero routing decisions, self-attested trace); "the first routing correction is implemented" (a lexical rule with an unmeasured over-route rate); "all 77 grades unchanged" (including thirteen historical D3 grades the current build has not earned).

Not yet supported: "a working local prototype" as a routing product; "adaptive improvement" or "learning" of any kind; "the current adaptive loop is concrete" (the loop is manual and its evidence pipe is broken); any savings, quality or economics figure; "no immediate input blocks the next offline work" (budget, reviewers, harness profile and four policy decisions are unmade); the laptop-plus-offline-learner-plus-distribution operating model (no code).

The prose in the author's reports is careful. The overinterpretation risk sits in titles, tables and figures that travel without their footnotes: the deck and PDF frozen at "finish Wave 3" and 895 tests; slide 11 calling manual edits "learning"; the lab table showing `claude-fable-5-1, gateway_reported` from a synthetic endpoint.

## 8. Next three bounded slices

If these three cannot be done in three slices, the honest statement is that no real-task demonstration is possible yet; I believe they can.

**Slice 1: make a decision become an outcome.** Why first: nothing downstream is measurable until it does (RV-01, RV-05 to RV-09). Owning: MEM-001, MEM-002, MEM-003, LRN-001, LRN-004, LRN-005. Prerequisites: none beyond the frozen source. Outputs: one outcome event contract shared by producers and consumers; a closer supervisor; the learning reader honouring corrections; a verifier-precision CLI and record; a `features-v2` learning contract admitted through LRN-005. Tests: a producer-to-consumer integration test that drives proxy and cascade to `closed_final` and a non-zero readiness count; a correction-flips-label test; a precision-record-makes-T1 test. Stop condition: any change to routing behaviour or thresholds; any new package. Authority: none beyond existing offline engineering. Promotion gate: MEM-002 and LRN-001 may state scoped D2 for the composed path; nothing else moves.

**Slice 2: make the routing decision the one the register describes.** Why second: the estimator is inert and the evidence is path-bound (RV-02, RV-03, RV-04, RV-17). Owning: RTG-002, RTG-003, RTG-006, LRN-004, OPS-005, TRU-001. Prerequisites: slice 1 for the health refresh to have inputs. Outputs: advisor falls back to the estimator selection and records overrides; a lab-only synthetic repository class independent of path; the lab loads its bundle in the mode it runs, with synthetic evidence references declared as such; a frozen paraphrase set authored by someone other than the implementer with a stated over-route budget; rule-health refresh wired with a provenance event. Tests: a sensitivity test where a constant estimator changes a decision; identical lab output from two paths on a clean machine; the paraphrase set as a dated artefact. Stop condition: any threshold tuned to produce a preferred distribution; any classifier call. Authority: none beyond offline engineering. Promotion gate: RTG-002 scoped D2 for the shipped configuration only if the sensitivity test passes.

**Slice 3: the smallest credible end-to-end demonstration.** Real task, observed routing, attributed quality, cost and latency, evidence-backed correction. Why third: it is the first measurement of routing value and it needs slices 1 and 2 to be honest. Owning: EVL-001, EVL-003, EVL-007, W3.1 capture (MEM-003, SAF-002), OPS-008. Design: five tasks from the roadmap's own task classes on one repository the owner controls, two arms (the router's choice versus always-frontier), run through native observation plus the existing W3.1 capture and snapshot verifier, attribution held at `operator_capture`, learning off, manual verification by a named reviewer, cost from the subscription's own usage, latency from the ledger. Outputs: ten attributed outcomes in the ledger through the slice-1 pipe; one course correction proposed from them and replayed through the lab. Tests: capture-to-verifier binding; the ledger shows both arms per task with matching tree identity. Stop conditions: any secret detected (pin, stop); any task touching deployment or payments paths; more than one repair cycle per task. Authority needed from the owner: use of the existing Claude subscription for ten runs, a named evaluation reviewer and a named security reviewer, and confirmation that the container backend is not required for this demonstration. Promotion gate: none; the output is the first P2 evidence, not a grade.

## 9. Coverage and reproducibility

`coverage.csv` assigns every in-scope file (691 inventoried plus 4 discovered): 296 deep-reviewed, 273 supporting-read, 11 historical-context, 17 generated or duplicate, 98 not reviewed (not opened by any inspector; mostly W3 evidence JSON bodies, patches for slices whose manifests were checked, and the pptx and PDF, which the leadership inspector did open). Nothing was inaccessible except by policy: secret-category files were hashed and not read; backup snapshot directories under the private state directory were not copied, and the W3 engine logs that live only there were not inspected (RV-20).

Commands run: hash comparison of 691 files at freeze and at close (zero drift); pytest of the W3 modules in a disposable copy (329 passed, 8 skipped); full pytest in a disposable copy (906 passed, 5 failed, 8 skipped; four failures need the excluded dev key, one is RV-03); the routing lab from a disposable copy (9 of 16 rows differ from the archived run); a 43-input feature battery through the extractor and policy; an offline drive of the composed pipeline into the closer, labeller and learning reader; ledger, learning, routing and cascade suites (181 passed). Each inspector's commands and skips are listed at the end of its appendix. Skipped deliberately: the full suite with the sandbox test that writes under the home directory (one inspector), the demonstration driver that depends on the sibling path, any classifier run, any validator that overwrites history, any Docker or network use.

Source mismatches: none between the inventory and disk; three W7.0a files differ from the last W3 evidence, as the author states; the routing demonstration's reproduction command fails on three hashes against the current tree.

Open questions and missing evidence: the header the pinned gateway sends on streamed responses (RV-26); the cause of the lost create receipt; whether the eight engine tests pass on the 322-input source; any organic evidence for any ADR in this implementation; any second author, repository or user.

## 10. What would convince us that ADRL is becoming a better adaptive router, rather than simply a more elaborate system?

Four things, in order, none of which is a test count.

First, a decision made by the running proxy on a real Claude Code task shows up, without a restart or a script, as a closed and labelled outcome in the ledger that a second person can read. Today it cannot.

Second, on a frozen set of tasks that the implementer did not write, the router's choice beats always-frontier on cost at matching verified quality for at least the mechanical class, and the middle tier is chosen on merit at least once. Today the middle tier is unreachable and the tasks are the author's.

Third, a change to routing behaviour is proposed from those outcomes, replayed through the lab, and the replay is reproducible on a machine that is not the author's. Today the lab is path-bound.

Fourth, when that change ships, a named reviewer who did not write it signs the disposition, and the register records the scoped level the evidence supports rather than the level the old codebase once earned.

Until the first of these is true, more infrastructure makes the system more elaborate and not more adaptive. The good news is that the first is a small slice, and the discipline that surrounds it is already in place.
