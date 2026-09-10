# ADRL: run, learn and course-correct

**Current forward plan, proposed 2026-09-07:** the [long-horizon roadmap](adrl-implementation-roadmap-2026-09-07.md)
consolidates the next implementation waves, dependencies, per-wave guardrails and evidence gates.
The plan below retains its historical scope; the new roadmap does not turn planned work into
implemented behavior or authorize a new model/deployment run.

**Later implementation, 2026-09-07:** [independent session verification](adrl-session-verification-2026-09-07.md)
is now applied in API preview 4, with 532 passing tests. Two verifier jobs each passed eight
checks on the existing repaired task and added receipts to a copied timeline. Earlier figures
and outstanding-work lists below describe the original report date/stage; the linked update
contains the current scope and next steps.

**Current result, 2026-09-07:** [the first live observation pilot](adrl-live-observation-pilot-2026-09-07.md)
is complete. Native Max authentication was confirmed with normal macOS access; no new login was
needed. Observation mode is applied in API preview 3, with 511 passing tests and 18 reconciled
real tool events. The repair passed eight independent checks. The preparation/planning text
below preserves its earlier scope and must not be read as current launch or authentication status.

**Subscription pilot application, 2026-09-07:** the user's Claude Code subscription supports
starting with a native baseline. A [prepared dataset-validator task and model guide](adrl-claude-subscription-pilot-2026-09-07.md)
separates that baseline, a planned observation-only integration and the later API-funded gateway
pilot. The fixture reproduces two template failures and two passing configuration tests. No model
run occurred. The observation-only launcher remains unimplemented; this preparation satisfies
neither the gateway validation gate nor the stable-API gate.

**Latest implementation update, 2026-09-07:** the [local product services](adrl-product-services-implementation-2026-09-07.md)
are applied in API preview 2, with 506 passing tests and a synthetic loopback HTTP check.
Session binding, observation intake, evidence reads and Claude Code connection files now exist.
The original planning text below retains its dated scope. Real Claude Code task validation,
missing hook/outcome integration, OpenCode and Responses remain outstanding.

7 September 2026 | Concrete implementation and architecture experiment plan | Revised for the multi-harness product requirement

## What we are trying to achieve

Build ADRL as a reusable product across coding harnesses, then improve it by running it, deliberately testing its assumptions, and changing its design where observations justify a change. Here, course correction means changing configuration, implementation, decision text or product scope. Training a model is not the objective of this plan.

The first engineering milestone is a versioned integration contract and an extracted protocol boundary. The first working path is a real Claude Code task with a checked result and an understandable record. The first portability milestone is Claude Code and OpenCode using the same service, policy engine and evidence contract. Before freezing the first product API, Codex must exercise a second protocol through an admitted Responses profile. Repeatable policy experiments proceed as each integration becomes trustworthy.

Start the real path with Claude Code CLI, one explicitly classified repository suitable for cloud processing and one known-good Claude deployment. Add OpenCode on that same Messages profile to test adapter reuse. Evaluate a local candidate after compatibility is established; a cheaper cloud candidate can follow. Exact model versions, available hardware, provider access, repository and a spend cap are deployment inputs to settle before paid runs. Do not copy the sample inventory's model names, context capacities or data-use claims as verified facts. Claude Code's non-Claude path needs our own compatibility testing; Anthropic does not support that routing configuration. [Vendor scope](https://code.claude.com/docs/en/llm-gateway)

The companion [multi-harness product contract](/Users/arunmenon/projects/adrl-world-class/design/adrl-multi-harness-product-contract-2026-09-07.md) defines the proposed API, adapter/profile separation, integration order and release gates. It is a design proposal, not an implemented API. This revision replaces the earlier single-harness framing of the first work package.

## What was checked today

- The existing Python environment and ADRL CLI work.
- `adrl config check` passed its nine configuration checks and verified the manifest signature. The unused EU residency class has no matching cloud deployment; this must not be mistaken for available EU routing.
- The focused configuration, composed-system and adversarial baseline passed: **39 tests in 2.75 seconds**. It uses a simulated gateway. This is not the complete repository test suite, a real-provider test or production certification.
- The default `adrl-core/data` directory is absent. This establishes only that the default local data directory is absent, not that no deployment exists elsewhere.
- No real harness session, model server or paid experiment was started during this planning pass.

There is enough implementation to begin integration work. There are still experiment tools to finish: the existing `learning evaluate` command checks artifact loadability, not quality or savings; the branch runner needs a concrete harness wrapper and complete measurements; automatic verification and hook coverage need to be exercised end to end.

Three known behaviors deserve immediate attention: unlisted gateway model groups currently count as healthy; the repository rung ceiling is advisory on the shadow frontier path; and tool-failure hooks are not ingested. Test these directly. Fix the first before relying on endpoint health, restrict the initial shadow population explicitly, and publish the missing hook coverage instead of implying it exists.

## The repeating work cycle

For each question, use this sequence:

1. **Name the assumption.** Quote the current ADR clause and state the behavior we expect.
2. **Define a result that could change our mind.** Choose the workload, comparison, success measure and stopping condition before running it.
3. **Run against a recorded build and configuration.** Keep the harness, model, context, tools and test environment identifiable.
4. **Inspect the result, including failures.** Classify whether the problem is implementation, configuration, compatibility, measurement or the design itself.
5. **Make a bounded correction.** Change the smallest relevant rule, mechanism or scope. Keep other variables stable when comparing alternatives.
6. **Repeat the experiment.** Preserve the original reproducer and verify that the correction works without breaking the established behavior.
7. **Update the register and evidence together.** Preserve old wording, link the experiment and implementation, and state precisely which population the conclusion covers.

A reproducible privacy-boundary violation can stop an experiment immediately. An economic result usually needs repeated comparisons. One disappointing run is a reason to investigate, not sufficient evidence that the entire routing strategy is wrong.

## Work sequence and deliverables

The time ranges below are engineering estimates for one engineer with access to the harness and gateway. Evidence volume, model compatibility and discovered defects can extend them. A calendar date never substitutes for an exit criterion.

| Stage | Work | Deliverable and condition for advancing |
|---|---|---|
| 0. Establish the baseline and product boundary, 3-5 days | Preserve the uncommitted snapshot; run repository checks; draft API schemas and adapter/profile interfaces; capture harness differences; decide how to admit Responses state; choose pilot inputs | Reproducible baseline, blocking-defect list and a contract preview grounded in two protocols. New behavior is mapped to proposed ADR wording |
| 1a. Extract and complete the Claude Code path, 3-5 days | Extract the Messages profile; add session/event/evidence surfaces; connect Claude Code; exercise streaming, tools and verification | One completed task can be traced from request to checked outcome. Existing byte/stream guarantees and controls survive extraction |
| 1b. Prove reuse with OpenCode, 2-4 days initially | Add its configuration and event adapter using the same service and policy contracts | Both harnesses pass equivalent control scenarios; no duplicated routing or pin implementation; actual setup effort is recorded |
| 2. Challenge the controls, 2-3 days | Run the E01-E04 scenarios below with synthetic secrets and isolated fixtures | A coverage table marking enforced, observed only and outside scope. No unresolved forbidden dispatch or duplicated side effect in the exercised paths |
| 3. Observe normal work, 3-5 working days initially | Keep gates enforced, routing and fallback in shadow; inspect at least 20 completed tasks for instrumentation gaps | Task-level records reconcile with provider usage and manual outcome checks. More data is collected if important paths remain unseen |
| 4. Compare design alternatives, 1-2 weeks initially | Use a frozen set of 30 tasks to debug comparisons; expand according to the uncertainty observed | Comparable executed outcomes for the current policy and alternatives, with failures, cost and waiting time included. The 30-task set is a diagnostic batch, not a graduation threshold |
| 5. Amend and repeat, every completed experiment batch | Resolve observations, implement the selected change, update affected ADRs and rerun | An evidence-linked disposition: keep, tune, amend, replace or defer. Wider live exposure follows only after the relevant checks pass |
| Product release gate, estimated after the stage 0 spike | Complete Codex/Responses; rerun conformance; package adapters and quickstarts; finalize version compatibility | Two harnesses and two protocols have real validation. Every advertised capability has evidence, and unknown/unsupported behavior is explicit |

Plan on an initial two-to-three-week engineering window for the common boundary and two-harness pilot, subject to the integration defects found. Begin Responses design in stage 0 and continue its work as capacity permits alongside the experiment queue. Estimate its completion after the state/transport spike. A stable product API cannot be declared merely because the Messages pilot works or a calendar deadline arrives.

## The first experiment queue

Run E01-E04 before drawing economic conclusions. Exercise E08 alongside the first and second adapters, then again for Responses. E05-E07 depend on trustworthy measurement and controls in each tested integration.

| Experiment | Question and test | Evidence to collect | Likely correction if it fails |
|---|---|---|---|
| E01: Interpret and preserve traffic | Send a normal turn, tool continuation, pre-warm, token count, compaction and permission-classifier request through the chosen harness/version. Compare the unchanged path with the gateway directly | Classification, content-bearing flag, request/response byte comparison where required, identity continuity and compatibility failures | SEM-001/004 and FND-001/003: fix classification or narrow protocol support; add the missing fixture |
| E02: Keep restrictions attached to content | Put a synthetic secret in a tool result, restart ADRL, compact, fork a child and return its result. Include unknown or invalid workload identity, scanner failure and ledger failure | Every attempted destination, block/pin result, restart persistence, false pins and parent/child propagation | SAF-001/002/003, TRU-001/002, SEM-006 and FND-004: fix lost state or propagation; amend the failure policy where the contract itself is inadequate |
| E03: Know where traffic went | Test streamed and non-streamed replies, a gateway fallback, absent/mismatched receipts, checkpoint shipment and verification | Intended versus confirmed deployment, unknown fraction, anchor age, acknowledged checkpoints and uncovered egress paths | TRU-002/003 and OPS-006/007: change the gateway contract or qualify the audit claim. Missing evidence remains unknown |
| E04: Make verification trustworthy | Check known-correct patches, known-incorrect patches, deliberately flaky checks and verifier execution failures. Repeat unchanged examples | Correctness of the verifier against independently specified answers, repeatability, snapshot identity, protected-path changes and indeterminate outcomes | SAF-007, MEM-003/004 and EVL-004: repair the verifier or label lifecycle. A stable verifier can still be wrong |
| E05: Test the local safe zone | Execute 30 small, independently checkable tasks across three slices: narrow bug fixes, test maintenance and mechanical refactors. Include hard-looking and easy-looking counterexamples | Acceptance, human repair, latency, tool/protocol failures, context use and paid cost by model and slice | RTG-001/003/004: shrink, expand or redraw the local scope; revise task features only if they explain different outcomes |
| E06: Test handoff and stickiness | On a selected subset, compare staying with one model, a bounded cheap-first attempt, a compact handoff and a tested downshift. Repeat from the same starting state in separate workspaces | Completed-task cost, cache effects, repeated work, inherited-state failures and duplicated side effects | CAS-003/004/005 and RTG-009: change the handoff boundary, transfer format, attempt budget or lowering rule |
| E07: Audit evidence and maturity | Trace sample tasks through request, verified outcome, closure, failure type and readiness reporting. Attempt an erasure and reconstruction check on fixture data | Missing/duplicate rows, origin versus verification quality, excluded fractions, actual repository diversity and derived-data deletion | MEM-001/004/010, LRN-001/002/003 and EVL-002/004/008: repair schema or evidence rules before making a learning/readiness claim |
| E08: Prove portability | Run equivalent control scenarios through Claude Code and OpenCode, then Responses/Codex. Include concurrent sessions, unknown endpoints, native errors/streams, event retries, resume and child return | Adapter/profile versions, coverage differences, setup time, manual interventions, shared-engine reuse and unsupported paths | FND-001/003, SEM-001/002/006/007 and relevant MEM/TRU contracts: correct adapter mapping, amend the common interface or narrow the support claim |

FND and OPS are reviewed across the queue. LRN enters chiefly through the evidence contract in E07. We do not need to build a learned router to discover that the current taxonomy or routing assumptions need amendment.

For E05, first compare a fixed strong baseline, a fixed local candidate and the current heuristic as three explicit, isolated policies. Thirty tasks across three policies means 90 executions before repeats. Add the cheaper cloud baseline only if its inclusion answers a named question. Choose a fresh confirmation set after tuning so the same 30 tasks do not become both the tuning set and the proof.

Shadow recommendations cannot supply the outcomes of policies that were not executed. Controlled alternatives therefore need separate real harness runs from a shared initial state. Do not reconstruct those outcomes by replaying another model's later tool results. The existing branch types and worktree runner provide useful starting points, but their harness binding, same-model repeat support, isolation and measurement must be completed and validated first.

## How we decide what to change

| Observation | Classification | Action |
|---|---|---|
| Code forwards content that the existing ADR forbids | Implementation defect | Fix code and preserve the failing test. The intended decision can stand |
| Local work succeeds but the configured attempt budget wastes time | Parameter problem | Change the versioned policy on a tuning set, then confirm on new tasks |
| Correct implementation repeatedly loses to a simpler permitted strategy | Design assumption challenged | Amend or replace the relevant routing/cascade decision, with scope and evidence |
| A new request type is invisible to the classifier | Coverage or protocol gap | Add a class/profile or narrow supported scope; update SEM and related tests |
| Two buckets prescribe incompatible behavior | Ownership or contract conflict | Resolve one owner and one shared contract. Update both references without changing stable IDs |
| Results are inconsistent, unverified or too sparse | Insufficient evidence | Keep the question open, restrict the claim and improve the experiment |

The architectural buckets can change if ownership repeatedly becomes ambiguous. Most early corrections will probably concern clauses, parameters and implementation rather than the entire taxonomy. This is an expectation to test, not a constraint on the review.

Different changes require different decisions. Routine fixes that restore an existing invariant can proceed with regression evidence. A change to what data may reach which destination is a policy decision for the responsible owner; better cost figures do not authorize it. Experimental branches can explore alternatives while their register disposition remains Proposed.

## What we will record for every run

Keep an experiment manifest outside prompt payloads. Include experiment ID, source snapshot/hash, configuration versions, harness and gateway versions, adapter version, protocol profile/version, API schema version, effective coverage, exact served model/deployment, task and initial-state identifiers, policy arm, verifier version, origin, outcome, wall time, token/cache usage, cost basis, blocks, retries, fallback, receipt confidence and failure attribution. Link runs to `route_id` and lineage; retain provenance for corrections. Compare results by harness and protocol; a result in one integration does not automatically establish the same economics or coverage in another.

The task scorecard should show:

- Accepted tasks divided by all attempted eligible tasks, plus inconclusive outcomes.
- Total paid model cost for all attempts divided by accepted tasks; also report total spend and failures when the denominator is zero.
- Median and tail completion time, plus sampled developer repair time.
- Privacy violations in the tested paths, false blocks/pins, unconfirmed destinations and missing evidence.
- Results by workload slice, policy and serving configuration; report the excluded population.

Separate model capability from end-to-end reliability. A timeout can be excluded from a capability analysis while still counting as a failed attempt and incurred cost in the product scorecard. Keep secrets, prompts and identifying paths under the existing data-class and retention rules; a traceability requirement does not authorize plaintext logging.

Set the total paid-run cap before starting. Estimate the next batch using completed pilot-run costs multiplied by remaining arms and repeats, plus an explicit contingency. Enforce that cap through the gateway and the experiment runner. Report actual spend after each batch. No dollar budget has been selected or authorized by this plan.

## Concrete startup sequence

The existing Claude Code startup interfaces are present. The following remains a useful first-path sequence after stage 0 produces a validated pilot profile, endpoints and credentials. It is not the finished multi-harness onboarding experience or a claim that those deployment inputs are configured today. The product work will package this flow behind adapters and a connection diagnostic.

1. Snapshot both repositories, including the current uncommitted files, without committing unrelated work. Record hashes of source and versioned policy files.
2. Create an isolated pilot configuration and data directory. Configure and sign the exact repository classification and endpoint inventory. Use a new pilot key set and a separately controlled anchor before claiming independently verifiable audit history.
3. Point `ADRL_CONFIG_DIR` at that profile. Set **all** of `ADRL_DATA_DIR`, `ADRL_LEDGER_PATH`, `ADRL_EGRESS_LEDGER_PATH` and `ADRL_KEYSTORE_PATH`; changing the data directory alone does not relocate the other paths in the current settings model.
4. Set `ADRL_GATE_MODE=enforce`, `ADRL_ROUTING_MODE=shadow` and `ADRL_FALLBACK_MODE=shadow`. Leave exploration disabled. The first repository must explicitly permit the baseline destination: the known shadow-mode class-ceiling limitation must not be hidden by this choice.
5. Generate the gateway configuration and start the pinned LiteLLM version with the actual provider credentials. Verify enabled endpoint health and streaming identity. LiteLLM documents deployment ID headers, but we must test their presence on this deployment. Streamed cost components may require separate usage/log reconciliation. [Gateway startup](https://docs.litellm.ai/docs/proxy/quick_start), [response headers](https://docs.litellm.ai/docs/proxy/response_headers)
6. Start ADRL and inspect `/healthz`, including gateway, ledger, component installation and anchoring state. A listening port alone is insufficient.
7. Launch Claude Code using ADRL's signed workload assertion, the same keystore as the proxy, and the printed session ID. Apply the emitted headers without discarding any other required headers. Set the base URL only for this pilot terminal session and verify the gateway credential path. [Claude Code connection guide](https://code.claude.com/docs/en/llm-gateway-connect)
8. Complete one controlled task, verify the result, close its outcome, and reconcile its decision, served identity and usage. Rehearse stopping routing while preserving applicable data restrictions.

Relevant commands, with the pilot environment already set in each terminal:

```bash
cd /Users/arunmenon/projects/adrl-core
.venv/bin/python -m adrl.cli.main config check
.venv/bin/python -m adrl.cli.main gateway-config --config-dir "$ADRL_CONFIG_DIR" --out "$ADRL_DATA_DIR/litellm.yaml"
.venv/bin/python -m adrl.cli.main serve --host 127.0.0.1 --port 8788
```

In the separate harness terminal, after setting the same pilot environment:

```bash
cd /Users/arunmenon/projects/adrl-core
.venv/bin/python -m adrl.cli.main launch --repo "$ADRL_PILOT_REPO"
```

Apply the launch output, then start the harness from the selected repository with `ANTHROPIC_BASE_URL=http://127.0.0.1:8788` and `claude --session-id "$ADRL_LAUNCH_SESSION_ID"`. A deployment credential can change which account pays for traffic; the provider/gateway credential owner and cap must be explicit. [Billing behavior](https://code.claude.com/docs/en/llm-gateway)

Do not enable `routing=live` by inserting dummy evidence references. The null rung evidence references currently block live routing intentionally. Controlled experimental exposure needs a real recorded admission decision; ordinary traffic stays in shadow until the applicable evidence exists. Readiness and artifact-loadability commands are aids, not automatic promotion authority.

## First implementation work package

The next coding task should deliver **the API preview and adapter/profile interfaces, an extracted Messages path, and a concrete Responses admission decision**, corresponding to P0-P1 in the product proposal. Follow it with the Claude Code and OpenCode adapters, E01-E04/E08 and one consistent task scorecard. Acceptance across this first pilot requires:

- An isolated configuration, ledger and keystore that do not overwrite the existing setup.
- A recorded build and resolved runtime versions, with valid signatures and real endpoint checks.
- A harness session with authenticated workload identity and a completed verified task.
- Claude Code and OpenCode connecting to the same engine through separate adapters, with versioned capability declarations and equivalent control scenarios.
- Documented session, event and evidence schemas; duplicate-event handling and producer authority validated at their boundaries.
- Explicit treatment of unknown endpoints and unsupported protocol features; catch-all forwarding cannot count as gated support.
- A Responses state/transport spike and an admission decision; the first stable API remains gated on completing that second protocol.
- A run record connecting actual dispatch, outcome and cost; unsupported or missing fields are explicit.
- Executable failure scenarios for pin persistence, missing identity, missing receipt and verifier failure.
- A rollback that stops experimental routing; restricted sessions remain local-or-block rather than silently returning to unrestricted cloud traffic.
- The full six checks required by `adrl-core/AGENTS.md` after implementation changes, plus the relevant new integration scenarios.

Review the first five tasks individually to find instrumentation problems, then review each completed experiment batch. For each design correction, produce a single reviewable package containing the observation, proposed ADR wording, implementation/configuration diff, regression result, effect on maturity and rollback. Update the decision's changelog, bucket overview and index when its disposition is accepted. Use the accompanying experiment template to keep that record short and consistent.

Success for this first cycle is a reusable boundary, two working harness adapters and well-supported design corrections. The later stable release also requires the second protocol. An unchanged ADR with stronger evidence is a useful outcome, and a simpler adapter contract discovered through testing is a product improvement.

## Local evidence for this plan

- [Implementation README](/Users/arunmenon/projects/adrl-core/README.md)
- [Known implementation gaps](/Users/arunmenon/projects/adrl-core/docs/known-gaps.md)
- [Runtime settings](/Users/arunmenon/projects/adrl-core/src/adrl/config/settings.py)
- [Operator and learning commands](/Users/arunmenon/projects/adrl-core/src/adrl/cli/main.py)
- [Workload launcher](/Users/arunmenon/projects/adrl-core/src/adrl/gates/cli.py:224)
- [Branch runner](/Users/arunmenon/projects/adrl-core/src/adrl/learning/pairs.py)
- [Source-check and test baseline](/Users/arunmenon/projects/adrl-world-class/reports/research/adrl-course-correction-baseline-2026-09-07.json)
- [Experiment record template](/Users/arunmenon/projects/adrl-world-class/reports/adrl-experiment-template.md)
- [Multi-harness product contract and release gates](/Users/arunmenon/projects/adrl-world-class/design/adrl-multi-harness-product-contract-2026-09-07.md)

## Implementation update, 7 September 2026

The initial product foundation has been applied to `adrl-core`: protocol and identity adapter
interfaces, the extracted Messages path, versioned decision context, capability discovery and
executable API preview schemas. The complete suite passes 463 tests. The candidate Responses
scope is documented; real Codex corpus/transport work remains. Authenticated session/event
services and real Claude Code/OpenCode onboarding are the next implementation package.

See the [implementation record](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md)
for exact coverage, checks and remaining release blockers. This does not mark the full P0-P5
product plan complete or establish a second harness integration.
