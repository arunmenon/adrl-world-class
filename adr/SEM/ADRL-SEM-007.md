# ADRL-SEM-007 - Protocol profiles (Proposed)

| Field | Value |
|---|---|
| Bucket | SEM - Interaction Semantics |
| Status | Proposed 2026-09-03 (new, from external review) |
| Maturity | D2 for the Messages boundary and local services, plus one bounded live observation pilot (2026-09-07). Full cross-protocol contract remains incomplete, D0 for the second profile; no general D3/D4 graduation or live gateway validation |
| Review verdict | PROPOSED (new) |
| Tenets | 1, 7 |
| Related decisions | FND-001, SEM-001, SEM-002, SEM-003, SEM-004, CAS-003, CAS-004, CAS-007 |
| Open questions | Q1, Q7 |

## Lab A.1 implementation evidence, 2026-09-08

The workbench runs the real Messages profile and Claude Code adapter against a synthetic client and in-process endpoint. It captures profile/adapter versions from decision context; actual harness binary/model revisions remain absent. The Responses cell is explicitly unqualified and never sent. This is fixture conformance and diagnostic scope, not another supported harness/protocol, real network streaming qualification or production admission.

[Report](../../reports/adrl-lab-first-run-2026-09-08.md), [runner](../../../adrl-core/tools/run_routing_lab.py), [tests](../../../adrl-core/tests/unit/test_routing_lab.py), [run evidence](../../reports/research/routing-lab-2026-09-08/run-2/results.json), [engineering checks](../../reports/research/routing-lab-2026-09-08/engineering-checks.json), [validation](../../reports/research/routing-lab-2026-09-08/validation.json), [follow-on scope](../../reports/waves/lab-a-routing-experiment.md). All eleven checks pass: 894 tests passed, eight engine cases skipped without new authorization, 320 stable inputs. Existing 316 inputs are unchanged. Decision wording, architectural status and formal maturity are unchanged; no whole-decision promotion or real-task learning evidence.

## Decision

Every wire format ADRL accepts is a named, versioned protocol profile that defines its request classes, turn and boundary signals, identity headers, content-bearing rules, error shapes and handoff rules; profile `anthropic-messages-v1` is the Anthropic Messages API with the six request classes of SEM-001, and no other format (in particular the OpenAI Responses API spoken by Codex CLI) enters scope until it has its own profile with an adapter, a mechanical discriminator and a captured corpus.

1. *Profile contents*: request-class discriminator (SEM-001), user-turn and action-boundary definitions (FND-003, CAS-003), session and lineage identity sources (SEM-002, SEM-006), utility fingerprints (SEM-004), content-bearing rule per class, protocol-conformant error shapes (SAF-004, CAS-007), and the provider-pair handoff rules the profile participates in (CAS-004). Each is versioned with the profile.
2. *No branch without a profile*: a discriminator, classifier or rewrite may not gain a code path for a second format; the second format is a second profile selected by endpoint path and headers before classification.
3. *Responses API prerequisites*: a `openai-responses-v1` profile requires, before Proposed status: a mapping of input and output item types to request classes; a state model for `previous_response_id` and server-side conversation state; handling of reasoning items (encrypted, same-family only); tool output items as the boundary signal; compaction semantics; and a scrubbed corpus of at least the SEM-001 fixture set.
4. *Cross-profile handoff* is forbidden until both profiles are at D2 and CAS-004 carries a pair rule for them.


## Claude initial-choice candidate, 2026-09-09

<!-- taxonomy-sync:claude-adapter:ADRL-SEM-007 --> Constructor-only native Claude initial-choice candidate preserves every parsed JSON field except model, including thinking, output settings, tools and cache markers. Ambiguous duplicate-key JSON and pre-existing assistant/tool-result history cannot start selection. One lineage retains the fixed choice. Native Claude Code and real-provider compatibility remain untested. [Implementation and evidence limits](../../reports/reviews/claude-adapter-2026-09-09/report.md). Formal maturity/status/verdict are unchanged.


## Product service evidence, 2026-09-07

API preview 2 implements local session binding/status, encrypted event intake, timeline and decision reads, plus Claude Code connection files and two tool-event hooks. Verification submissions from harness credentials are forbidden. The Messages path and these service operations have D2 evidence for their tested scope; real harness validation, OpenCode and the Responses runtime remain pending.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Earlier subscription pilot plan, 2026-09-07

The [subscription pilot](../../reports/adrl-claude-subscription-pilot-2026-09-07.md) proposes
separating native Claude model traffic from ADRL's local observation API. Hook delivery does
not constitute admission or coverage of a model wire profile. The current connection helper
sets the gateway base URL; a separate observation-only launch mode must be implemented and
tested before claiming it works with subscription traffic. Native Claude authentication stays
with Claude Code, separate from ADRL workload assertions. This is planning evidence only;
the existing D2 scope and Proposed status remain unchanged.

## Live observation pilot, 2026-09-07

API preview 3 implements an immutable gateway/observe session mode and the observation-only Claude Code connector. Observe mode leaves provider headers/base URL untouched, marks model interception and controls unavailable, and rejects identified model requests sent to ADRL. One Claude Code 2.1.263 session produced 18 reconciled tool events, including one PostToolUseFailure. The Messages wire profile remains validated offline; no real gateway, second harness or Responses validation is claimed.

The [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md) links the applied 15-file package, 511 passing tests,
all required checks, reviewed outcomes and remaining blockers. Architectural status is unchanged;
this evidence does not promote the full decision to D3 or D4. Earlier dated sections preserve
their original implementation and planning scope.

## Session verification implementation, 2026-09-07

API preview 4 extends timeline entries with typed session-verification-v1 receipts. The local product verify command uses the bound session and exact signed workspace; it introduces no model-protocol transformation or public verification-submit endpoint. Preview-2/3 observation envelopes remain readable and deliverable, while session clients use preview 4. The shared receipt/timeline design is reusable in principle across harnesses, but OpenCode reuse and the Responses runtime are not yet validated.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Forward implementation plan, 2026-09-07 (proposed)

The proposed roadmap retains one shared engine, narrow harness adapters and native protocol profiles. It preserves the two-harness/two-protocol gate before a stable product contract, with OpenCode reuse before Codex/Responses admission and an early Responses state/transport spike. New task lifecycle/API details are to be designed in W3/W5; no new endpoint or profile is implemented by the plan. Capability, implementation and real conformance must be reported separately.

See the [detailed wave roadmap](../../reports/adrl-implementation-roadmap-2026-09-07.md) and
[wave execution packet](../../reports/adrl-wave-execution-template.md). The roadmap maps all
77 stable decisions to review waves. This is planning linkage only: prior decision wording,
architectural status, existing implementation evidence and maturity remain unchanged.

## W0 execution baseline, 2026-09-07

W0 reconciled stale service documentation against the implemented preview-4 session/event/read operations and the separate observation pilot. The capabilities payload and API contract are unchanged. Exact export comparison is now a non-mutating required check. The prepared W3 and Responses investigation packets do not register a second harness/profile or establish task-close attribution.

See the [W0 packet](../../reports/waves/w0-baseline.md), [journey](../../reports/adrl-implementation-journey.md),
[check/source evidence](../../reports/research/adrl-w0-baseline-2026-09-07.json),
[maturity inventory](../../reports/research/adrl-maturity-baseline-2026-09-07.json) and
[engineering runner](/Users/arunmenon/projects/adrl-core/tools/check_all.py).
All 556 implementation tests and eleven engineering checks pass for the recorded build. This is
scoped local evidence; prior decision wording, status and maturity remain unchanged.

## W3.1 retained operator captures, 2026-09-08

W3.1 adds an internal operator capture API and one database migration. The generated public API remains preview 4 and passes an exact unchanged export comparison. No new HTTP endpoint, CLI command, harness adapter, profile or trusted task-close claim is introduced. Existing session-verification behavior and old receipts remain compatible; retained-capture timeline/CLI/verification integration is W3.3 work.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2a operator attempt journal, 2026-09-08

W3.2a exposes only an internal operator journal and migration 0008. No public HTTP operation, CLI command, harness hook or protocol profile is added; the exact generated API export remains preview 4. Old capture/receipt evidence remains readable. The capture library and journal are deliberately not presented as a complete task-close interface: supervisor association and later retained verification/timeline/CLI integration remain W3.2b/W3.3 work.

See the [plain-language report](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2a-attempt-journal-2026-09-08.json),
[implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/attempts.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-lifecycle.md).
All 631 tests and eleven checks pass for the recorded build. This is scoped offline evidence;
prior wording, architectural status and maturity fields are preserved. Full W3 remains open.

## W3.2b2c writer-boundary research, 2026-09-08

The investigation recommends optional isolated execution behind shared product identity/task/evidence contracts while retaining native observation at its declared depth. This is a proposed backend direction, not a mandatory Docker dependency, a registered profile, public endpoint or second-harness claim. Harness adaptation and execution ownership must retain distinct capability declarations; an observed task cannot silently acquire exact-close attribution.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## Context and rationale

The register's overview names Codex CLI as a harness, the register README repeats it, and FND-001 scopes it out "until a Responses-format discriminator and corpus exist". The implementation followed FND-001, so the README claim is currently false, and the gap is not a discriminator branch. The Responses API differs from Messages in the unit of state (input and output items rather than messages), in conversation state (`previous_response_id` and stored state rather than a full transcript), in reasoning (encrypted items that only the same provider can read), and in how tool outputs and compaction appear. Every SEM decision assumes the Messages shape. Treating a wire format as a profile makes those assumptions explicit and stops a second format from being bolted onto a discriminator written for the first.

## Adversarial review (2026-09-03)

### Steelman
A profile is the honest unit: SEM's decisions are precise because they are about one wire format, and the register should say so. Making the second format a profile with prerequisites keeps SEM at D3 for what it covers and D0 for what it does not, instead of averaging the two.

### Attacks (self-applied)
1. **Profiles duplicate SEM.** Mitigation: a profile is a table of which SEM decision applies with which parameters; SEM decisions stay the authority.
2. **Codex users get nothing.** Mitigation: they get passthrough with no gating, which is today's state; SEM-007 makes that visible as an unclassified profile with its own egress marker rather than silent passthrough.
3. **Server-side state defeats per-request gating.** A Responses request with `previous_response_id` does not carry the transcript, so SAF-003's new-content scan cannot see earlier content and the pin cannot cover it. This is the strongest reason for clause 3: the profile must decide whether ADRL forbids stored state for gated lineages or resolves it, before the format is admitted.

### Evidence
- ADRL external implementation review, 2026-09-03, item SEM: README line 3 versus FND-001 clause 4, verified.
- OpenAI, Responses API reference and conversation-state guide: input and output items, `previous_response_id`, stored state - https://developers.openai.com/api/reference/cli/resources/responses/methods/create and https://developers.openai.com/api/docs/guides/conversation-state (cited by the 2026-09-03 external review; the conversation-state guide was fetched in the 2026-09-02 review under CAS-004)
- ADRL-FND-001 clause 4 and ADRL-SEM-001 (this register).

### Verdict
**PROPOSED (new).** Recommended for acceptance at D0; the register README is corrected to match FND-001 in the same change.

## Amendments applied

New decision; no prior text.

## Follow-ups

- [x] Write `profiles/anthropic-messages-v1.yaml` from the current SEM parameters; new pipeline decision contexts record profile and adapter IDs/versions. Historical rows remain unchanged.
- [x] Decide the initial stored-state rule for a future Responses profile: the compatibility spike excludes referenced server state; a future gated profile rejects non-null `previous_response_id` and conversation references until resolution is designed and tested. This does not activate a Responses runtime profile.
- [ ] Capture a scrubbed Codex CLI corpus only after that decision.
- [ ] Complete Messages-specific gate/cascade extraction, a Responses corpus, opaque-state custody rules and native conformance before admitting Responses.
- [ ] Validate OpenCode utility/session behavior before claiming a second harness adapter.

## Earlier foundation evidence, 2026-09-07

The first extraction adds `ProtocolProfile`, `RequestView`, `StreamObserver` and `HarnessAdapter`
interfaces, the existing Messages implementation, Claude Code correlation extraction, versioned
decision context, and a product API preview. Only capability discovery is served; session/event
services remain unimplemented. The applied package passes 463 tests, including 35 new cases.
This establishes offline implementation evidence for the extracted boundary; it does not change
the register's overall disposition or establish live harness maturity. See the
[implementation record](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-09 | <!-- taxonomy-sync:claude-adapter:ADRL-SEM-007 --> [Offline Claude candidate](../../reports/reviews/claude-adapter-2026-09-09/report.md); Constructor-only native Claude initial-choice candidate preserves every parsed JSON field except model, including thinking, output settings, tools and cache markers. Ambiguous duplicate-key JSON and pre-existing assistant/tool-result history cannot start selection. One lineage retains the fixed choice. Native Claude Code and real-provider compatibility remain untested. | Previous decision wording and dated evidence preserved; no grade change |
| 2026-09-08 | Added scoped Lab A.1 synthetic workbench evidence and limitations | Prior decision wording, status, maturity and dated evidence retained |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2a attempt journal application, checks and remaining supervision/recovery gates | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded W0 baseline, repeatable checks and explicit remaining gates | Prior decision wording and evidence preserved; no architecture or maturity change |
| 2026-09-07 | Linked proposed implementation roadmap and dependent decision questions | Prior decision and evidence preserved; no runtime or maturity change in this planning pass |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-09-07 | Recorded applied observation mode and the first live subscription pilot | Decision policy and status unchanged; prior evidence was offline or synthetic, with observation-only launch still planned |
| 2026-09-07 | Scoped live-observation evidence without general graduation | D2 offline evidence for the extracted Messages boundary and local product services (2026-09-07). Full cross-protocol contract remains incomplete, with D0 for the unbuilt second profile; no live harness maturity is established |
| 2026-09-07 | Recorded proposed observation-only subscription path and its coverage limits | Decision unchanged; no observation-only subscription launcher or live harness evidence existed |
| 2026-09-07 | Extended scoped maturity evidence to local product services | Full cross-protocol contract remains incomplete (D0 for the unbuilt second profile); the extracted Messages boundary has D2 offline evidence as of 2026-09-07. No live harness maturity is established by this package |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Synchronized scoped maturity and linked register entries without changing Proposed status | Maturity: D0 Design, review recommends D0 Design (profile v1 is what the 2026-09-02 implementation speaks; no second profile exists) |
| 2026-09-03 | Proposed (external review) | none |
| 2026-09-07 | Recorded Messages extraction, API preview and initial Responses admission scope with offline evidence; overall status remains Proposed | No named runtime profile or public product contract |


### Candidate placement limitation, 2026-09-09

The initial-choice implementation is currently a constructor-only proxy experiment collaborator; it does not yet live behind the native protocol profile serialization interface. This scoped candidate placement is not the production adapter contract. Profile integration remains required before making this a consumable harness feature. JSON values are preserved, not original whitespace or Unicode escaping, on the explicit rewrite path. Normal passthrough remains byte-exact.
