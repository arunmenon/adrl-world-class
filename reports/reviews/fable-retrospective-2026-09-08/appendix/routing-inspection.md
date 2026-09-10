# Routing product inspection

Inspector: rv-routing (independent review, 8 September 2026). Sources: frozen snapshot at `adrl-review-fable-2026-09-08/snapshot/{register,runtime}`; offline checks run only inside `adrl-review-fable-2026-09-08/disposable-routing/` (a byte-identical copy of `snapshot/runtime`, verified with `diff -rq`), using the interpreter `/Users/arunmenon/projects/adrl-core/.venv/bin/python` with `PYTHONPATH` pointing into the disposable copy (`adrl.__file__` confirmed to resolve there). No repository was written to, no model or network was called, no key material was read. Author claims were treated as hypotheses; agreement with an author-assigned label is not treated as proof of correct routing.

File references use `runtime/...` for `snapshot/runtime` and `register/...` for `snapshot/register`.

## (a) End-to-end trace of the routing product

### The code path

**Harness input and identity.** `runtime/src/adrl/proxy/pipeline.py:219-256` is the entry. The installed profile (`MessagesProfile`, `runtime/src/adrl/wire/profiles/messages.py:46-57`) claims any path that starts with `/v1/messages`. `ClaudeCodeAdapter` (`runtime/src/adrl/wire/adapters.py:58-72`) extracts five correlation signals: the `x-claude-code-session-id` header, the `metadata.user_id` session, the system text, and the agent and parent agent headers. `IdentityResolver` (`runtime/src/adrl/wire/identity.py:115-138`) hashes the session and agent chain into a lineage HMAC. Nothing here authenticates a workload; that is the signed assertion checked by the repository gate.

**Classification.** `runtime/src/adrl/wire/classify.py:130-219` assigns one of six request classes from shape alone: count_tokens, non API, unparseable, pre-warm (max_tokens ≤ 2), utility (fingerprint or small no-tool sidecar), continuation (last message carries a tool_result), subagent (agent header), else user_turn. Only user_turn requests get a fresh route decision (`Classification.is_routed`, line 53-56).

**Gates.** `runtime/src/adrl/gates/pipeline.py:210-403` runs, in order: pin lookup (a pinned lineage is narrowed to local before anything else), repository class ceiling from the signed workload assertion, new-content secret scan (a pinning finding narrows to local before the durable write and fails closed if the pin write fails), then feasibility (context ceiling and gateway health). `evaluate` (lines 194-204) projects the rung set onto attested deployments (`DeploymentSet`), so the router chooses among deployments, never bare labels.

**Features.** `runtime/src/adrl/routing/features.py:268-338` computes the decision-time snapshot from the request alone. The intent signal is the last developer-authored user message (`_last_user_text`, lines 130-144, via `turn_start_index`). `verb_class` (lines 147-172) is the features-v2 change: a mechanical-repair phrase is normalised, then the strongest matching verb class wins. Scope, context size, trajectory counters (edit failures, error results, interrupt marker in the last three messages), file mentions, tool side-effect ceiling and the derived `task_classes` are added. `assert_no_denied_fields` enforces the LRN-004 deny-list by key prefix.

**Bands and selection.** `runtime/src/adrl/routing/policy.py:27-107` evaluates five rule predicates. Two claim clear-local (mechanical edit in a small context with no failure or destructive signal; read-only explain in a small context). Three claim clear-frontier (destructive first action, context above 20k tokens, hard verb or broad multi-file scope). Ties resolve to the higher rung. Everything else is ambiguous. `BandHeuristicEstimator.probabilities` (lines 120-145) computes linear P(complete) per rung from `heuristic_score`, floors the clear band's rung at 0.85 and caps the lower rungs when the band is clear-frontier. `select_rung` (lines 158-173) walks rungs in after-cache cost order and returns the first whose probability meets its tau.

**Router composition.** `runtime/src/adrl/routing/router.py:119-199`. After `select_rung`, if the band is ambiguous the router calls `_advise` (lines 220-244). With no classifier configured, `_advise` returns the policy's `ambiguous_fallback_rung` (frontier) or the highest permitted rung. The `selected` argument is never read inside `_advise`. Cascade feasibility is then evaluated; a local choice that cannot cascade falls to the next rung. The explorer runs only in the ambiguous band on an unrestricted, unpinned, unescalated lineage.

**Cascade plan, dispatch, served identity.** `runtime/src/adrl/cascade/controller.py:225-262` plans: a user turn opens a new sticky state at the decided rung, raised to the sticky rung if a prior escalation is armed (lines 289-315); a continuation inherits the sticky rung and, at an action boundary with a pending trip-wire, escalates to the next permitted rung with a mechanical handoff note (lines 337-415, 442-508). `pipeline._prepare` (lines 305-442) picks the attested deployment, rejects any non-local deployment on a pinned lineage (lines 385-386, 492-498), writes the egress row ahead of dispatch, then appends the decision row. `_dispatch` (lines 510-570) sends exactly one request. The SSE observer (`runtime/src/adrl/wire/observe.py:109-263`) reconstructs usage, stop reason, tool blocks and the served identity from the `x-litellm-model-id` header, then the reported model, else `assumed_intended`. `DeploymentPolicy.served_identity` (`runtime/src/adrl/gates/deployments.py:163-189`) attaches the deployment receipt. `_finalize` (pipeline lines 572-627) runs cascade observation under the lineage lock, records a `served` or `upstream_error` event, the egress receipt, and any outcome events.

**Outcome and ledger.** Decisions are written to the `decisions` table with the full feature JSON, feature version, estimator name and version, propensity and context (`runtime/src/adrl/ledger/store.py:163-205`). Events carry `(route_id, producer, producer_seq)` idempotency. Trip-wire hits, escalations, policy constraints and terminal failures are `cascade`-produced events. Failure attribution lives in `_observe_failure` (controller lines 606-655): candidates are ranked by `resolve_primary` (`runtime/src/adrl/core/enums.py:116-136`) with policy constraint above context feasibility above infrastructure above dialect above task capability, and `unverifiable` when the served source was assumed.

### Three real examples, from trace records

All three come from `register/reports/research/routing-correction-2026-09-08/lab-final/results.json` (experiment `d5651e66-519f-46ee-a012-290817e285e8`), whose `manifest.json` source hashes match the frozen snapshot exactly (see section e).

**Example 1: `loop-detected` then `loop-escalated` (session `edit`).** The first request "Fix the typo in README.md" produced decision `01a0802e-327...`: verb `trivial`, scope `narrow`, score 0.0, task classes `small_context, mechanical_edit, small_diff`, rule `mechanical_edit_small_file`, decided local. The lab then sent a continuation carrying three identical `Read README.md` tool calls with identical results. The request event shows `target_rung: local` (the continuation inherited the sticky rung) and the served event `fired_wires: ['a_repeated_tool_calls']`; the trip-wire event was appended by the cascade producer at sequence 2. The lab's fourth-repeat continuation is an action boundary (every tool_use has its tool_result), so the controller emitted `escalation from local to cheap_cloud, cause a_repeated_tool_calls` and the proxy's request event shows `target_rung: cheap_cloud, decided_rung: local, escalated: True, deployment_id: cheap-haiku-us`. The endpoint received body `eecd0f80...` with model `cheap-haiku-us`; the served event is `gateway_reported`, `receipt_confirmed: True`. In plain language: the router chose local, the controller saw the model reading the same file three times, waited for a clean boundary, then moved the same route to the cheaper cloud rung with a handoff note, and the ledger shows both the original choice and the later dispatch separately.

**Example 2: `before-secret`, `secret-pin`, `pin-persists` (session `private`).** "Refactor the whole payments module" produced decision `01a0802e-331...`: verb `hard`, scope `broad`, score 1.0, expected first action `destructive` (the prompt matches the destructive-intent vocabulary and the fixture offers Edit and web_search tools), band clear-frontier, dispatched to `frontier-fable-us`. The next continuation carried a tool result containing `AWS_KEY=AKIAIOSFODNN7EXAMPLE`. The secret gate narrowed the set to local before the pin was written; the cascade emitted `policy_constraint: gate_precedes_stickiness, requested frontier, served local`; the request event shows `pinned: True, target_rung: local, deployment_id: local-qwen-7b`. The following clean continuation (`pin-persists`) still went to `local-qwen-7b` with `pinned: True`. Plain language: a difficult task started on the strongest tier, a secret appeared mid-task, and from that point the lineage could only reach the loopback deployment, with the constraint recorded as a policy event rather than a capability failure.

**Example 3: `missing-identity` and `upstream-error`.** For "Fix the typo in README.md" against an endpoint that omits the model header and model field, the served event reads `served_source: assumed_intended, receipt_confirmed: False` while `served_deployment_id` is still `local-qwen-7b` (the intended deployment). For "Refactor the whole payments module" against a 503 endpoint, the cascade closed the turn with `failure_type: infrastructure, served_source: assumed_intended` and the proxy recorded `upstream_error` at status 503. Plain language: when the gateway does not say what served, ADRL records that it is assuming, and a transport failure is attributed to infrastructure, never to model capability.

**One failure or limitation, from the trace.** The `long-context` row: the same typo prompt with 120,000 characters of the letter x appended to the system prompt produced `context_tokens_estimate: 30019`, rule `large_context`, decided and dispatched frontier at `frontier-fable-us`. The router is reacting to the byte count of irrelevant filler, not to anything about the task. This is the documented behaviour of `rule.large_context`, but it means a harness with a large static system prompt (Claude Code's own is tens of thousands of characters) will route every typo to the most expensive tier. The register presents this cell as "context influences the route"; the trace shows it is context size alone.

**Hypothetical (not observed in a trace).** If the harness client disconnects mid-stream, the Starlette `BackgroundTask` wrapping `after` (`runtime/src/adrl/proxy/asgi.py:60-64`) may not run, in which case no `served` event, receipt or sticky update is written for that route. I found no test or trace covering client-side disconnect (`rg ClientDisconnect` returns nothing under `src/adrl/proxy` or `tests/integration/proxy`).

## (b) Intent extraction

### What features-v2 changed

`register/reports/research/routing-correction-2026-09-08/implementation.patch` shows the whole change: the trivial regex gained `typos?`, `misspellings?`, `indentation`; the hard regex's dangling `concurren` became `concurren(?:cy|t)`; a `MECHANICAL_REPAIR` normaliser rewrites "fix/correct [the|a|this|these|another] [first|second|third|next|last|remaining|other] typo(s)/misspelling(s)/whitespace/indentation" to just the task noun; `verb_class` now takes the maximum-score class over all matches, except that a `write` match lying inside a small-edit span ("add a flag") is discarded. Candidate 1 (`candidate-1/src/adrl/routing/features.py`) lacked the ordinal list and the small-edit overlap exclusion; the full suite caught "Now fix the second typo" selecting frontier in the sticky-cascade test (`checks-1/tests.log`) and the matrix caught "Add a flag in cli.py" flipping to frontier (`route-changes.md`). Both were repaired in the final candidate without touching the frozen cases. That repair cycle is honestly recorded.

Concurrency in the ordinary sense (parallel tool calls) is not a routing input: `parallel_tool_calls_last_assistant` is computed (`features.py:211-219`) but no rule or estimator reads it (`rg` over `src` finds no consumer). The cascade handles parallel tool calls at the boundary level (`assess_boundary`), which is separate.

Context and trajectory signals: context tokens (chars/4 over system plus all message text), three trajectory counters over the last 12 messages, and an interrupt marker in the last 3. Thresholds: `small_context_tokens` 8,000; `large_context_tokens` 20,000; `small_diff_max_files` 2; `multi_file_min_files` 4 (`runtime/src/adrl/config/models.py:130-137`). Score adjustments: broad +0.20, narrow −0.10, large context +0.10, any edit failure +0.15, three error results +0.10, interrupt +0.30 (`features.py:222-238`).

### Offline battery: 43 constructed inputs the suites do not contain

Script: `scratchpad/intent_battery.py` (recorded below). Each prompt was run through `Router.decide` with the shipped configuration twice: once with the shipped features-v2 `verb_class`, once with a reconstruction of the features-v1 first-match `verb_class` taken verbatim from the patch's "before" side, so that "pre-existing", "introduced by v2" and "remaining" can be separated. Results are in `scratchpad/intent_battery_results.json`. Selected rows (all permitted; second rung is with only local and cheap cloud permitted):

| Input | v1 route | v2 route | Band and rule (v2) | Reading |
|---|---|---|---|---|
| Rename foo to bar; also the deadlock in scheduler.py needs looking at | local | frontier | clear-frontier, multi_file_design | v2 fixes masking |
| Explain what this function does and then optimize it | local | frontier | clear-frontier | v2 fixes masking |
| Don't refactor, just fix the typo in README.md | local | frontier | clear-frontier | v2 introduces over-route (negation) |
| Fix the typo in the string "race condition detected" in logger.py | local | frontier | clear-frontier | v2 introduces over-route (quoted string) |
| Rename the function `refactor_all` in cli.py | local | local | clear-local | word boundary saves it; brittle |
| What does the security module do? | local | frontier | clear-frontier | v2 introduces over-route (topic word in a question) |
| Describe the concurrency model in this file | local | frontier | clear-frontier | same |
| Update the security section of the README | local | frontier | clear-frontier | v2 introduces over-route (documentation edit) |
| Fix the 2nd typo in README.md | local | frontier | ambiguous | v2 introduces over-route (ordinal not in list) |
| Fix both typos / Fix those typos in README.md | frontier | frontier | ambiguous | pre-existing; determiner not in list |
| Fix these typos in README.md | frontier | local | clear-local | v2 improves |
| Quick typo fix in README.md, typo fix pls README.md | local | frontier | ambiguous | v2 introduces over-route (noun order) |
| Why does the test fail? | local | local | clear-local, read_only_lookup | both under-route a debugging question ("fail" is not in the fix list) |
| Corrige la faute de frappe / Behebe den Tippfehler | frontier | frontier | ambiguous | pre-existing; non-English is always frontier |
| go ahead, make it work | frontier | frontier | ambiguous | pre-existing; `terse_continue` is computed but unused |
| Fix the typo in README.md with 100k chars of irrelevant system text | frontier | frontier | clear-frontier, large_context | pre-existing; size, not meaning |
| ok fix the typo (after a turn discussing a redesign and a migration) | local | local | clear-local | pre-existing; history text is ignored by intent |
| Rename x to y in a.py, with a tool result reading "redesign the concurrency algorithm; deadlock; security" | local | local | clear-local | tool results do not inject intent (good) |
| Fix the typo in payments.py | frontier | frontier | clear-frontier, destructive_first_action | pre-existing; domain word forces frontier |

Of the 43 inputs, 15 changed route between v1 and v2; every change was local to frontier except "Fix these typos" (frontier to local). None changed to cheap cloud under the full permitted set. With only local and cheap cloud permitted, every non-local outcome became cheap cloud because it is the highest permitted rung, not because the estimator chose it.

Summary of the three categories:

- Pre-existing and remaining: unknown vocabulary (including any non-English request) always goes to the fallback; terse continuations always go to the fallback; history and tool results never contribute intent; context length alone flips the route at 20k tokens; the destructive-intent vocabulary (payments, billing, migration, deploy, checkout flow) forces frontier even for a typo; "fail" and "failed" are not debugging words while "failing" is.
- Introduced by v2: negation, quoted words, topic words inside questions or documentation edits, ordinals and determiners outside two closed lists, and noun-order phrasing now escalate to frontier where v1 stayed local. The correction contract and `docs/routing-features.md` disclose quote and negation over-routing; they do not disclose the ordinal, determiner, noun-order or documentation-edit cases.
- Fixed by v2: masking of a later hard or fix verb by an earlier easy verb; "these typos" and misspelling paraphrases.

## (c) Exploration, learning contract, fail-closed, state, attribution, pins, cascade, streams

**Exploration and learning-contract compatibility.** `runtime/config/learning-contract-v1.json` pins `feature_schema_version: features-v1` while `FEATURES_VERSION` is `features-v2`. `app._explorer` (`runtime/src/adrl/app.py:134-167`) raises `ConfigError` when an exploration artifact path is configured and the contract version differs, and returns `None` when no artifact is configured. `load_graduated` (`runtime/src/adrl/learning/artifacts.py:206-225`) would also refuse a manifest whose `feature_schema_version` differs from the bundle's contract. The unit test `test_feature_version_does_not_silently_admit_old_exploration` covers both branches. This is correct fail-closed behaviour: exploration is now unreachable until a v2 contract exists, and the contract's feature list (nine names such as `context_tokens_est`, `tool_count`, `neighbour_local_success_rate`) does not describe what `features.py` actually emits in either version, which is a pre-existing gap the CI check (`tools/check_learning_contract.py`) does not detect because it only checks deny-list membership and manifest targets.

**Startup versus dynamic state.** Rule health is computed once in `Router.from_components` (`router.py:93-97`); `set_rule_health` has no caller in `src` or `tools`. `CascadeController.episode_boundary` (SEM-005 ratchet release) has no caller either. `_verifier_consumed` and `_pending` are process-local. So the "adaptive" demotion shown in the demonstration (`register/reports/adrl-routing-in-action-2026-09-08.md`, section 3) is an explicit call from the research driver, not service behaviour; the report says this, and RTG-003's evidence note says it too.

**Fail-closed behaviour.** `resolve_failure` (`runtime/src/adrl/proxy/fallback.py:63-86`): pinned gate failure blocks; pinned routing failure forwards local; unpinned failures forward upstream marked `unscanned`. Pin write failure is fail-closed (`gates/pipeline.py:320-358`). Egress append failure on a pinned lineage blocks (`pipeline.py:395-399`). Classification failure on a pinned lineage raises `UnclassifiableError` (`classify.py:163-165`). These are consistent and tested by the removal and gate suites I ran (327 passed in the focused subset).

**Failure attribution.** Precedence is fixed in `enums.py:107-113` and the `upstream-error` trace shows `infrastructure` for a 503 with `assumed_intended` served source. `UNVERIFIABLE` is chosen only when no other candidate exists. Trip-wire hits are all typed `task_capability` except invalid tool calls (`harness_dialect`); there is no way for the runtime to type a hit as anything else, so a local model that loops because a tool result was truncated would be recorded as a capability failure of that rung.

**Permission narrowing.** `PermittedSet.tighten` (`core/types.py:79-88`) raises on any widening; `DeploymentSet` likewise. The router intersects the gate's rung set with the attested deployment rungs (`router.py:122-126`). `_inherited_decision` (`pipeline.py:747-768`) tightens a sticky rung to the highest permitted with reason `inherited_tightened`. The `secret-pin` trace confirms narrowing beats stickiness.

**Sticky pins.** A pin is a lineage event read through `PinRegistry` (`gates/pin.py`), inherited to descendants through `_effective_pin` (`pipeline.py:662-682`) which materialises an `inherited` pin event, and released only by the audited CLI path. On a pinned lineage the cascade never escalates (`controller.py:594-600` requires `not plan.pinned`), and `evaluate_cascade` returns `pinned` so the turn is not evidence about local-first.

**Cascade constraints.** Escalation requires a pending trip-wire, an action boundary, an unpinned lineage and a higher permitted rung. Escalation is exempt from the switch charge in the cost model. A handoff note is mechanical. The `loop-escalated` trace confirms each condition.

**Streamed errors and served-endpoint uncertainty.** An SSE `error` event is captured but the event type recorded is decided by HTTP status (`pipeline.py:616`), so a 200 stream that ends in an error event is recorded as `served` with `completed: False` and the cascade classifies it as infrastructure. Served identity falls back to `assumed_intended` and the decision explanation API maps that to confidence `assumed_intended` with the served deployment left null unless the receipt is confirmed (`runtime/src/adrl/api/service.py:290-320`). This is honest. The register's known-gaps table already says a gateway that returns no receipt header leaves every row unconfirmed.

**Initial route, later dispatch, hindsight quality.** The ledger separates these correctly: `decided_rung` on the decision row, `target_rung` and `escalated` on the request event, `served_rung` and `served_source` on the served event, and `closed_final` outcome events for hindsight. No trace in the frozen artifacts contains a `closed_final` outcome from real work; the only closed outcomes are synthetic (the demonstration's 20 invented outcomes) or terminal failures.

**Runnable production paths versus diagnostic overrides.** Three distinct things are being exercised:

1. The component matrices (`matrix_driver.py`, `run_demo.py`) call `Router.decide` directly with `make_gate()` from `tests/unit/routing/helpers.py`, which fabricates a `GateOutcome` with all rungs permitted and no deployments. No gate, pipeline, cascade or ledger runs. These are unit-level probes.
2. The routing lab (`runtime/tools/run_routing_lab.py`) composes the real pipeline. At line 271 it loads the config bundle with `routing_mode` forced to `SHADOW`, then at line 275 hands that bundle to `build_components` with settings whose `routing_mode` and `fallback_mode` are `LIVE`. I confirmed in the disposable copy that loading the shipped configuration with `routing_mode=LIVE` raises `ConfigError: live_rung_has_evidence: rung local is enabled in live mode without an evidence_ref`, because every rung in `runtime/config/rungs.yaml` has `evidence_ref: null`. The SHADOW-loaded bundle skips that check (`runtime/src/adrl/config/checks.py:58-68`). So the lab exercises a LIVE dispatch path that the production loader refuses to construct for this configuration. `environment.json` records `config_evidence_bypass: test-only bundle; no provider transport` and `live_config_admitted: False`, which is honest, but the plain-language reports say "the controlled endpoint actually received the frontier request" without saying that the live path is unreachable outside the simulator.
3. The lab's workload identity is a synthetic assertion for `root=str(ROOT)` (line 279-286), that is the absolute path of the runtime checkout. `runtime/config/repo-classification-v1.json` classifies `/Users/arunmenon/projects/adrl-core` as class `open` (all rungs) and everything else as `default` (local and cheap cloud only). When I ran the lab from the disposable copy, every row that reads `frontier` in the frozen table came out `cheap_cloud` dispatched to `cheap-haiku-us`, with gate verdict `default:assertion_default_class`. The regression test `tests/unit/test_routing_lab.py::test_composed_choices_reach_endpoint_and_context_changes_choice` fails for the same reason. This is not an author fabrication, but the "frontier" cells in every published lab table are a consequence of a developer manifest entry naming the author's checkout path, and the 911-test result is reproducible only at that path.

## (d) Integration

**API contract versus fixture.** `runtime/api/adrl-api-v1-preview.json` (preview 4) defines six product operations, typed events, coverage facts and a decision explanation with confidence levels. It is generated from Pydantic models and checked unchanged in CI. It is a real, reusable contract for session binding and observation intake. It says nothing about routing: no rung, band, feature or policy appears in any schema. The routing product's only externally visible outputs are the ledger rows and the decision explanation's `decided_rung` and `reason_codes` (`recorded_decision`, `estimator:<name>`, `no_rung_met_threshold`).

**Real adapter versus harness-name enum.** `HarnessAdapter` is a `Protocol` with one method, `identity_signals` (`adapters.py:31-38`); `ClaudeCodeAdapter` reads three headers and one metadata field. The feature extractor derives `harness_id` from the presence of one header (`features.py:311`) and nothing consumes it. Utility fingerprints, boundary detection, transcript transformation, feature extraction and trip-wires all read Messages JSON directly, as `docs/protocol-boundary.md` admits. Today the adapter is an identity-signal extractor and the harness is, in effect, a string constant. A second harness on the Messages profile (OpenCode) would need its own fingerprint corpus, session header mapping and tool-name tables (`side_effects.py` and `tripwires.py` name Claude Code's built-in tools), none of which exists.

**Control versus observation.** The `integration_mode` field distinguishes `gateway` (requests pass through ADRL) from `observe` (hooks only). The capabilities payload (`runtime/src/adrl/api/contracts.py:297-331`) reports `validation: offline_fixtures` and `tested_harness_versions: ()`. The single real Claude Code session on record was observation-only (18 tool events); no real request has been routed through the gateway path. The register's product-services report says so.

**Task phase, native harness mode, reasoning settings.** ADRL has no concept of task phase (planning versus implementation) or of the harness's own modes (plan mode, permission mode). `interaction_mode` is interactive, background subagent or utility, derived from headers and request shape. Reasoning settings are handled only as dispatch parameters: `thinking` and `output_config` are stripped for non-frontier rungs (`wire/rewrite.py:19`) and suppressed on handoff; `registry.py:19` lists `reasoning_effort` and `effort` as within-rung parameters that routing never sets. There is no effort-level routing.

**SEM-007 and FND-005 gates.** The Responses admission document is a scope decision with an acceptance table and explicitly no corpus, no fixtures and no registration. The lab's `responses-unqualified` cell is never sent (`run_routing_lab.py:313-320`). FND-005's product application requires two harnesses and two protocols with real evidence before a stable contract; the runtime reports one profile, one adapter, offline fixtures.

**What must be proven before claiming a second harness or protocol.** For OpenCode on Messages: a scrubbed captured corpus covering the six request classes and utility fingerprints from a named version; an adapter with tests for session identity, child sessions and resume; parity of the gate, cascade and side-effect tables on that corpus; a lab run whose workload assertion is not path-dependent; and a real gateway-mode session with receipts. For Codex on Responses: everything in `docs/responses-admission.md`'s table, plus profile-specific gates and cascade, before the profile is registered. None of these artifacts exists in the snapshot.

## (e) Reconciling the counts

| Claim | What the artifact contains | Hash status |
|---|---|---|
| 720 synthetic component decisions | `before.json` and `after-final.json` each hold 24 original prompts × 5 conditions × 2 repeats (240) plus 12 fresh × 5 × 2 (120); 360 + 360 = 720. Distinct prompt/condition cells: 180. Changed cells between before and after-final: 25 (7 original, 18 fresh), matching `route-changes-final.md`. Repeats were identical in every cell. | `input_sha256` in both files equals my hash of `stress-cases.json` (5db0dbfc…) and `fresh-cases.json` (13f2eaf8…). |
| 16-cell lab | 16 cases; 15 Messages submissions; 14 endpoint dispatches (pinned overflow blocked); one unsupported Responses cell never sent. | `lab-final/manifest.json` `source_manifest` has 322 entries and matches the snapshot's `source_manifest(runtime)` with zero differences; `suite_sha256` equals my hash of `artifacts/lab/routing-suite-v1.json`. |
| 24 original and 12 fresh prompts | Confirmed by file content and the hashes above. Fresh cases were frozen before the code change (contract.md); `before.json` was produced with the same fresh file (same hash). | Matches. |
| 911 tests passed, 8 skipped | `checks-final/tests.log`: 911 passed, 8 skipped. In the disposable copy `pytest --collect-only` collects 919 tests. The 8 skips are the 4 + 4 parametrised engine tests in `tests/integration/test_resource_engine.py` and `test_launch_engine.py`, which skip unless four `ADRL_RESOURCE_*` environment variables name a Docker socket and fixture. | `checks-final/manifest.json` `source_after` matches the snapshot exactly (322 entries, status passed, all eleven checks passed). `checks-1` matches except the three candidate-1 files and shows the one failed test. |
| 159 focused tests | Not independently reconstructed; the log records 159 passed in the second focused run and 145 in the first. My focused subset (routing, cascade, learning, wire, proxy, gates without sandbox, lab) ran 328 tests: 327 passed, 1 failed (the path-dependent lab assertion above). | Not applicable. |
| 316, 320, 322 stable inputs | 316 is the pre-lab manifest (`adrl-w3-transport-receipts` `source_after`), 320 adds four lab files, 322 adds `docs/routing-features.md` and `test_mixed_intent.py`. Each differs from the snapshot only by the files each later slice changed. | Consistent chain. |
| routing-lab run-1 | Manifest has `source: synthetic` and no hash map; correctly disqualified in `QUALIFICATION.md`. | Not source-bound. |

Every hash I could check matches the frozen snapshot. The counts are accurately reported. The interpretation is where the problems are.

### Resolution of the routing-lab test failure raised by the W3 inspector

The W3 inspector's full run of the frozen runtime gave 906 passed, 5 failed, 8 skipped. Four failures need the excluded private key `config/keys/dev/manifest-signing.key`; those are snapshot artefacts. The fifth, `tests/unit/test_routing_lab.py:61` (refactor decided `cheap_cloud`, test asserts `frontier`), is not a snapshot artefact. It is a genuine path dependency of the frozen source. Evidence, all from the disposable copy without reading any key file:

1. **The excluded key is not on this test's path.** `load_bundle` on the frozen `config/` returns `manifest_signature_verified: True` and `inventory_signature_verified: True`; both `.sig` files and `keys/dev/manifest-signing.pub` are present in the snapshot and verification needs only the public key (`runtime/src/adrl/config/loaders.py:101-116`). The lab signs its workload assertion with the HMAC key of the keystore it creates in its own temporary directory (`runtime/tools/run_routing_lab.py:286`, `components.keystore.hmac_key()`), not with the manifest-signing key.

2. **The assertion verified; the repository lookup missed.** The gate verdict recorded in my lab run reads `repo_class: default:assertion_default_class`. `RepoClassifier.resolve` (`runtime/src/adrl/gates/repo_class.py:198-212`) reaches that branch only when the assertion is valid but `_entry_for(asserted)` finds no manifest entry; an unverified or absent assertion would instead produce `unknown` under `unknown_identity_policy: local_only`, which would have blocked cheap cloud as well. Lookup is an exact match on the normalised root path (module docstring lines 8-9; `_entries` at lines 110-112).

3. **The manifest names one path.** `runtime/config/repo-classification-v1.json` maps only `/Users/arunmenon/projects/adrl-core` to class `open` (all rungs); the default class allows local and cheap cloud. The lab asserts `root=str(ROOT)`, the absolute path of the checkout being run (`run_routing_lab.py:279-286`). The archived run recorded `repo_class: open`, reason `open:assertion` (`lab-final/results.json`, refactor row); my run from `disposable-routing/` recorded `default`.

4. **Hashes compared.** `tools/check_all.source_manifest` over `snapshot/runtime` yields 322 entries. `routing-correction-2026-09-08/lab-final/manifest.json` `source_manifest` (322 entries) and `checks-final/manifest.json` `source_after` (322 entries, status passed, all eleven checks passed) match it with zero differing, zero missing and zero extra entries. `checks-final/tests.log` records `911 passed, 8 skipped`. So the archived validation was run on exactly the frozen source, from the path the manifest classifies as `open`.

Conclusion: the archived 911 passed / 8 skipped is reproducible on the frozen source only when the checkout lives at `/Users/arunmenon/projects/adrl-core` and the private development key is present. On any other path the frozen source itself fails `test_routing_lab.py:61`, and every "frontier" row in the published lab tables becomes `cheap_cloud`. The four key-dependent failures are an artefact of the review's key exclusion; the fifth is a defect in the frozen source and its evidence (finding F2 below).

## Findings

### Observed defects

**F1. The estimator, thresholds and cost model never influence the initial route.** Severity: high. Confidence: high.
Files: `runtime/src/adrl/routing/router.py:147-148, 220-244`; `runtime/src/adrl/routing/policy.py:120-173`; `runtime/src/adrl/config/models.py:139-153`; `runtime/config/policy.yaml:3-6, 21`.
Claim: RTG-002 "select the cheapest healthy rung whose estimated probability of completing the turn meets that rung's published completion threshold"; register maturity D2 "the ordering rule is tested".
Observation: (i) In the ambiguous band, `_advise` ignores its `selected` argument and returns the fallback whenever no classifier is configured, so `select_rung`'s output is discarded. (ii) With the shipped coefficients, local meets tau 0.80 only for `heuristic_score` ≤ 0.0556 and cheap cloud meets 0.85 only for score ≤ 0.083; the only way to reach such a score is `trivial` with narrow scope and no adjustments (score 0.0), which the clear-local rule already claims. In a clear band the floor and caps make the band's rung win regardless of cost. Therefore in every reachable state the route is determined entirely by the rule predicates plus the fallback, and cheap cloud can only ever be chosen as the highest permitted rung when frontier is excluded. The frozen matrices confirm: zero cheap-cloud initial choices in 720 decisions; all ambiguous ordinary cells (9 before, 7 + 4 after) went to frontier. Offline check: for "Write unit tests for parser.py" `select_rung` returns frontier with probabilities local 0.445, cheap 0.63, frontier 0.905, and the decision row carries `no_rung_met_threshold: False`.
Consequence: the product is a keyword rule set with a frontier default, and "unchanged thresholds and costs" is not a safeguard because they are inert. The `no_rung_met_threshold` marker cannot fire as designed in the ambiguous band.
Correction: make `_advise` fall back to the estimator selection when no classifier is present (or record that the fallback overrode it); recalibrate or remove the linear estimator; add a test asserting that at least one reachable feature state selects cheap cloud on merit.
Acceptance: a golden test in which replacing `BandHeuristicEstimator` with a constant estimator changes at least one decision; a dated measurement of the ambiguous-band share and of cheap-cloud selection rate on the 36 frozen prompts that is not zero, or an explicit register statement that the middle rung is currently unreachable on merit.

**F2. Lab routing evidence and the full test suite depend on the author's absolute checkout path.** Severity: high. Confidence: high (reproduced).
Files: `runtime/tools/run_routing_lab.py:279-286`; `runtime/config/repo-classification-v1.json:52-56`; `runtime/tests/unit/test_routing_lab.py:61, 65`; `runtime/tests/unit/gates/conftest.py:39`.
Claim: "Real ADRL stages ran against a controlled in-process endpoint"; refactor and mixed-intent cases "dispatched frontier"; "911 tests passed".
Observation: the lab signs a workload assertion for the runtime's own path. Only `/Users/arunmenon/projects/adrl-core` is classified `open`; any other path is `default` (local and cheap cloud). Running the unchanged lab from the disposable copy produced 9 rows differing from `lab-final/report.md`: every `frontier` became `cheap_cloud` at `cheap-haiku-us`, and the lab regression test failed with `assert 'cheap_cloud' == 'frontier'`.
Consequence: the published "frontier" dispatches are an artefact of a developer manifest entry, and the engineering-check result is not reproducible on another machine or path.
Correction: give the lab an explicit synthetic repository class (for example an `open` class bound to a lab-only repo id) independent of the filesystem path; make the gate conftest and lab tests use a fixture manifest.
Acceptance: `tools/run_routing_lab.py` and `pytest` produce identical results from two different absolute paths on a clean machine; the manifest in the lab output records the class used.

**F3. LIVE dispatch in the lab is obtained by loading the bundle in SHADOW mode.** Severity: high (for evidence claims), medium (for safety). Confidence: high (reproduced).
Files: `runtime/tools/run_routing_lab.py:271-275`; `runtime/src/adrl/config/checks.py:58-68`; `runtime/config/rungs.yaml:22-42`.
Claim: lab reports describe the "real composed stages" in live routing mode.
Observation: `load_bundle(settings.model_copy(update={"routing_mode": RoutingMode.SHADOW}))` bypasses `check_live_rung_has_evidence`; loading the same configuration with `routing_mode=LIVE` raises `ConfigError` because no rung has an `evidence_ref`. The pipeline is then built with `routing_mode=LIVE`. `environment.json` records the bypass.
Consequence: the only "live" routing evidence in the register was produced on a path the product refuses to start. Readers of `report.md` and the plain-language reports are not told this.
Correction: either supply a lab-only rungs configuration with synthetic `evidence_ref` values and load it in LIVE mode honestly, or label every lab table "live path simulated under a shadow-admitted bundle".
Acceptance: the lab loads its bundle with the same `routing_mode` it runs with, or every lab report and ADR evidence note carries the bypass sentence from `environment.json`.

**F4. features-v2 introduced new over-routing classes that the correction record does not name.** Severity: medium. Confidence: high (measured).
Files: `runtime/src/adrl/routing/features.py:33-78, 147-172`; `runtime/docs/routing-features.md:21-24`.
Claim: "Quotes, negation, discussion of implementation and complex topic names can over-route."
Observation: in the 43-input battery, 14 inputs moved from local to frontier under v2. Beyond quotes and negation, the new over-routes include ordinals and determiners outside the closed lists ("2nd", "both", "those"), noun-order phrasing ("typo fix"), documentation edits mentioning "security", and plain questions containing a topic word ("What does the security module do?"). The `MECHANICAL_REPAIR` normaliser covers exactly five determiners and seven ordinals.
Consequence: mechanical work will be sent to the most expensive tier in patterns that are common in real prompts; the trade is silent because no over-route rate is registered.
Correction: broaden the normaliser to any determiner or numeral before the task noun, or route repair-noun matches without a second verb to trivial; publish an over-route budget.
Acceptance: the 43-input battery (or a larger frozen paraphrase set) recorded as a dated artifact with the local rate for mechanical paraphrases at or above the v1 rate, and a register field stating the accepted over-route rate.

**F5. Outcome-driven adaptation is not wired into the service.** Severity: medium. Confidence: high.
Files: `runtime/src/adrl/routing/router.py:93-97, 116-117`; `runtime/src/adrl/cascade/controller.py:659-682`; `rg` results (no callers).
Claim: register overview and roadmap describe an adaptive router that "changes its routing policy when reliable outcomes show a better choice".
Observation: rule health is computed once at construction; `set_rule_health` and `episode_boundary` have no callers; verifier signals are only produced by the operator verification CLI.
Consequence: in a running service nothing changes routing behaviour over time except a restart. The demonstration's demotion was an explicit driver call.
Correction: a versioned refresh contract (interval, minimum verified count, provenance event) and a boundary-signal producer.
Acceptance: an integration test in which appending 20 verified closed outcomes to the ledger changes the next decision of a running pipeline without restart, with a `rule_health_refreshed` event recorded.

**F6. Decorative features.** Severity: low. Confidence: high.
Files: `runtime/src/adrl/routing/features.py:87-91, 211-219, 311, 322, 330, 348-349`.
Observation: `terse_continue`, `parallel_tool_calls_last_assistant`, `harness_id`, `interaction_mode_weight` and `latency_weight_by_mode` are computed or configured but read by no rule, estimator or cost path.
Consequence: readers of decision rows may assume these influenced the route.
Correction: either consume them or mark them informational in the feature documentation and learning contract.
Acceptance: `docs/routing-features.md` lists each emitted field with "decision input" or "record only".

**F7. Learning contract feature list does not describe the emitted snapshot.** Severity: low. Confidence: high.
Files: `runtime/config/learning-contract-v1.json:5-15`; `runtime/tools/check_learning_contract.py`.
Observation: the contract names nine features (for example `context_tokens_est`, `tool_count`, `neighbour_local_success_rate`); `compute_features` emits about thirty with different names. The CI check only tests deny-list membership.
Correction: generate the contract's feature list from `compute_features` output and check name equality in CI when the version is admitted.
Acceptance: `check_learning_contract.py` fails when a feature is emitted that the contract of the same version does not list.

### Unsupported claims

**U1.** "The controlled endpoint actually received the frontier request" (`register/reports/adrl-routing-correction-2026-09-08.md`, first section). True only under the path-dependent `open` class (F2) and the shadow-admitted bundle (F3). Recommended wording: "received the highest rung the development manifest permits for the author's checkout path, under a bundle the live loader would refuse".

**U2.** RTG-002 maturity "D2 Tested, the ordering rule is tested". The ordering rule is unit-tested in isolation but cannot alter any decision in the shipped configuration (F1). Recommend annotating the maturity field with "inert under policy-v1 constants".

**U3.** "No thresholds were tuned to achieve a preferred routing distribution" is literally true but implies the thresholds constrain the distribution; they do not (F1).

**U4.** Capabilities `identity: authenticated_binding` and `tool_events: implemented` alongside `tested_harness_versions: ()` are individually accurate but together read as a validated adapter; the adapter is a header extractor and no gateway-mode session with a real harness exists.

### Missing experiments

**M1.** Dated measurement of the ambiguous-band share on organic Claude Code traffic (RTG-003 clause 3). On the 36 frozen prompts, ordinary cells were 13 clear-local, 12 clear-frontier, 11 ambiguous after v2; nothing organic.

**M2.** Any run with the advisory classifier configured (RTG-006). The correction and lab both state none was run; the middle rung's only entry point besides restriction is this classifier.

**M3.** A sensitivity test that would fail if the estimator were replaced by a constant (see F1 acceptance).

**M4.** A path-independent lab run on a clean checkout (F2), and a lab run that loads its bundle in the mode it executes (F3).

**M5.** Client-disconnect mid-stream finalisation (hypothetical gap noted in section a).

**M6.** A frozen paraphrase set for negation, quoting, ordinals and non-English wording with an accepted over-route budget (F4).

**M7.** Any second-harness or second-protocol corpus; none exists, and the register says so.

### Strategic disagreements

**S1. Strongest-signal lexical aggregation moves the error from under-routing to over-routing without a budget.** With the middle rung unreachable on merit (F1), every over-route is a frontier dispatch. The correction was framed as conservative; conservatism in a cost product needs a stated price. I would freeze an over-route rate before the next lexical change.

**S2. Destructive-intent vocabulary is a capability signal, not a risk signal.** "Fix the typo in payments.py" routes to frontier because "payments" is in `DESTRUCTIVE_INTENT` and the harness offers an Edit tool. The rule conflates side-effect risk with model capability, and it sends the most sensitive-sounding domains to the public cloud by default. The side-effect class belongs in the gate or cascade layer, not in the band rules.

**S3. Path-bound developer configuration is treated as product configuration.** The dev manifest, the dev inventory and the tests' hard-coded `/Users/arunmenon/projects/adrl-core` mean every "real composed stages" claim inherits the author's machine. A synthetic-but-explicit lab tenant would remove this dependency.

**S4. The harness adapter abstraction is ahead of the evidence.** A `Protocol` with one implementation, tables of Claude Code tool names in three modules and Messages JSON parsed throughout means "adapter" currently means "name". The product contract is sound as a target; the register should say the runtime is at one harness, one protocol, header-level adaptation.

## Commands run

All commands were run from the review directory or the disposable copy. Outputs are summarised above; raw outputs were not retained outside this appendix and the scratchpad.

1. `ls` and `find` over `snapshot/` to inventory files; `wc -l` over routing, proxy, wire, gates, cascade and learning sources.
2. `cat -n` reads of the runtime files listed under "Files opened" below and of the register reports, ADRs and research artifacts.
3. `cp -R snapshot/runtime disposable-routing/`; `diff -rq snapshot/runtime disposable-routing` (identical apart from a `__pycache__` created by the import check); `PYTHONPATH=disposable-routing/src python -c "import adrl; print(adrl.__file__)"` printed the disposable path.
4. Offline estimator and config check (inline script in the disposable copy, `ADRL_*` paths set to the disposable directory): computed per-score probabilities against tau; `load_bundle(Settings(config_dir='config', routing_mode=LIVE))` raised `ConfigError: live_rung_has_evidence: rung local is enabled in live mode without an evidence_ref`; ran `Router.decide` and `select_rung` for "Write unit tests for parser.py".
5. Source-manifest reconciliation (inline script using `tools/check_all.source_manifest` from the disposable copy against `snapshot/runtime`): compared against `lab-final`, `lab-after`, `checks-final`, `checks-1`, routing-lab `run-2`, `engineering-checks.json` and the transport-receipts `source_after`; hashed the suite, stress-cases and fresh-cases files.
6. `scratchpad/intent_battery.py` in the disposable copy: 43 synthetic prompts through v1 and v2 `verb_class` and `Router.decide` under two permitted sets; wrote `scratchpad/intent_battery_results.json`.
7. `python tools/run_routing_lab.py --suite artifacts/lab/routing-suite-v1.json --out <scratchpad>/lab-repro` in the disposable copy with `ADRL_CLASSIFIER_BASE_URL` and `ADRL_EGRESS_ANCHOR_URL` pointed at `127.0.0.1:1` (never contacted; the runner overrides settings). Exit 0; 16 cells; table differs from `lab-final/report.md` in 9 rows. No `.data` directory was created in the disposable copy.
8. `pytest --collect-only -q -p no:cacheprovider` in the disposable copy: 919 tests collected.
9. `pytest -q -p no:cacheprovider --basetemp=<scratchpad>/pytest-tmp tests/unit/routing tests/integration/cascade tests/unit/learning tests/unit/wire tests/integration/proxy tests/unit/gates --ignore=tests/unit/gates/test_sandbox.py tests/unit/test_routing_lab.py`: 327 passed, 1 failed (`test_composed_choices_reach_endpoint_and_context_changes_choice`, cheap_cloud versus frontier). `test_sandbox.py` was excluded deliberately because it writes a probe file under the home directory.
10. `pytest -q -rs tests/integration/test_resource_engine.py tests/integration/test_launch_engine.py`: 8 skipped, reason "requires explicit local synthetic fixture and private resource accounting".
11. `rg` searches for callers of `set_rule_health`, `compute_rule_health`, `episode_boundary`, `VERIFIER_FAILED_EVENT`, `terse_continue`, `parallel_tool_calls_last_assistant`, `harness_id`, `no_rung_met_threshold`, `ClientDisconnect`, skip markers, and home-directory writes.
12. Python extraction scripts over `lab-final/results.json`, `before.json`, `after-final.json` and `api/adrl-api-v1-preview.json` to print decision rows, events, band counts and schema fragments.

Skipped: the full 919-test suite was not run because `tests/unit/gates/test_sandbox.py` writes under the home directory and the engine tests require Docker; the demonstration driver `run_demo.py` was not re-run (it depends on the `adrl-core` sibling path); no classifier endpoint was configured.

## Files opened versus skimmed

Opened in full (runtime): `src/adrl/routing/features.py`, `policy.py`, `router.py`, `cost.py`, `cascade_feasibility.py`, `advisor.py`, `side_effects.py`, `rule_health.py`; `src/adrl/proxy/pipeline.py`, `stages.py`, `fallback.py`, `upstream.py`; `src/adrl/wire/classify.py`, `identity.py`, `adapters.py`, `observe.py`, `profiles/base.py`, `profiles/messages.py`, `profiles/messages_responses.py`; `src/adrl/gates/pipeline.py`, `feasibility.py`; `src/adrl/cascade/controller.py`, `sticky.py`, `tripwires.py`; `src/adrl/learning/explore.py`, `artifacts.py`; `src/adrl/core/types.py`, `enums.py`; `src/adrl/config/models.py` (to line 400), `loaders.py`, `checks.py`, `settings.py`; `src/adrl/app.py`; `config/policy.yaml`, `rungs.yaml`, `learning-contract-v1.json`, `repo-classification-v1.json`; `tools/run_routing_lab.py`, `check_all.py`, `check_learning_contract.py`; `tests/conftest.py`, `tests/unit/routing/helpers.py`, `tests/unit/routing/test_mixed_intent.py`, `tests/unit/test_routing_lab.py`; `docs/routing-features.md`, `routing-lab.md`, `responses-admission.md`, `protocol-boundary.md`, `product-services.md`, `known-gaps.md`; `artifacts/lab/routing-suite-v1.json`; `tests/fixtures/wire/user_turn.json`.

Skimmed (runtime): `src/adrl/proxy/asgi.py` (lines 60-178), `src/adrl/proxy/observe_only.py` (head), `src/adrl/gates/pin.py` (head), `src/adrl/gates/deployments.py` (`served_identity`), `src/adrl/ledger/store.py` (decision and event inserts), `src/adrl/api/service.py` (decision explanation), `src/adrl/api/contracts.py` (`distribution_capabilities`), `src/adrl/wire/rewrite.py` and `routing/registry.py` (grep hits only), `api/adrl-api-v1-preview.json` (schemas and paths), `config/endpoint-inventory-v1.json` (deployments), `tests/integration/test_resource_engine.py` and `test_launch_engine.py` (heads), `tests/unit/gates/test_sandbox.py` (head), `tests/unit/test_engineering_tools.py` (grep hits).

Opened in full (register): `reports/adrl-routing-correction-2026-09-08.md`, `adrl-routing-in-action-2026-09-08.md`, `adrl-lab-first-run-2026-09-08.md`; `design/adrl-multi-harness-product-contract-2026-09-07.md`; `profiles/anthropic-messages-v1.yaml`; `reports/research/routing-correction-2026-09-08/` (`contract.md`, `fresh-cases.json`, `matrix_driver.py`, `route-changes.md`, `route-changes-final.md`, `implementation.patch`, `validation.json`, all logs, `candidate-1/` sources, `lab-final/report.md`, `checks-1/tests.log`, `checks-final/tests.log`); `reports/research/routing-demonstration-2026-09-08/` (`stress-cases.json`, `run.log`, `runtime-baseline.json`, `targeted-tests.log`, `validation.json`); `reports/research/routing-lab-2026-09-08/` (`run-1/QUALIFICATION.md`, `run-1/report.md`, `run-2/report.md`, logs, `validation.json`, `check-logs/tests.log`); `adr/RTG/ADRL-RTG-002.md`, `RTG-003`, `RTG-006`, `adr/LRN/ADRL-LRN-004.md`, `LRN-008`, `adr/SEM/ADRL-SEM-007.md` (first 140 lines), `adr/FND/ADRL-FND-005.md` (first 140 lines).

Skimmed or parsed programmatically (register): `before.json`, `after.json`, `after-final.json`, `lab-final/results.json`, `lab-final/manifest.json`, `lab-after/manifest.json`, `checks-1/manifest.json`, `checks-final/manifest.json`, `routing-lab-2026-09-08/run-2/manifest.json`, `run-1/manifest.json`, `engineering-checks.json`, `adrl-w3-transport-receipts-2026-09-08.json`; `reports/research/routing-demonstration-2026-09-08/run_demo.py` was not opened (its logic is duplicated in `matrix_driver.py`, which was read).

Not opened: `preview.html` and `results.json` under the demonstration directory, `reports/adrl-implementation-journey.md`, roadmap and blueprint reports, wave packets, the `.patch` files for earlier slices, and everything under `snapshot/skill-*` and `snapshot/adrl-progress-brief`.
