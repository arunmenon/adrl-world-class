# ADRL as a product across coding harnesses

**Latest implementation update, 2026-09-07:** the [local product services](../reports/adrl-product-services-implementation-2026-09-07.md)
are applied in API preview 2, with 506 passing tests and a synthetic loopback HTTP check.
Session binding, observation intake, evidence reads and Claude Code connection files now exist.
The original planning text below retains its dated scope. Real Claude Code task validation,
missing hook/outcome integration, OpenCode and Responses remain outstanding.

7 September 2026 | Proposed product boundary and first release plan

This proposal incorporates the requirement that ADRL be a reusable product across harnesses. It supplements the research review and revises the implementation plan. Endpoint names, commands and interfaces below are design proposals unless explicitly marked existing. No new runtime API or harness integration was implemented in this pass; no ADR status was changed.

## The product we should build

ADRL should be a service that a coding harness can connect to for model access under a shared policy, with a record explaining each decision and its outcome. A developer should be able to change their coding harness while retaining their repository policy, permitted destinations and evidence history.

The integration package should handle the differences: where to configure the endpoint, how to establish workload identity, and how to report tool and session events. It should not contain its own routing algorithm or secret policy.

The first release should run locally as one ADRL service, using the existing gateway abstraction for model providers. Define the interfaces so a managed deployment can follow. Shared multi-user operation needs its own authentication, tenant isolation and operations work; a localhost pilot does not establish those properties.

There are two independent portability questions:

- **Harness portability:** can Claude Code and OpenCode share the same ADRL engine despite different session and tool behavior?
- **Protocol portability:** can that engine also handle the Responses API used by Codex without assuming that every request is an Anthropic message?

The first pilot must answer the first question. The first product release must answer both. Routing economics is a third question, measured after the relevant integration is trustworthy.

## First integrations and why

| Integration | Initial configuration | What it proves | Release role |
|---|---|---|---|
| Claude Code CLI | Messages profile, approved Claude deployment, signed workload binding | The existing implementation can support a complete real session | First working adapter |
| OpenCode | Anthropic provider pointed at ADRL, same approved deployment and policy | Harness differences can be contained in an adapter and its fixtures | Required for the first portability pilot |
| Codex CLI | Custom provider using the Responses profile, initially a compatible fixed deployment | The common engine survives a second protocol and state model | Required before the first stable product API |

Claude Code documents gateway endpoint and custom-header configuration. OpenCode documents provider base URLs, custom headers, and plugin events around tools and sessions. These are integration entry points; they do not establish ADRL compatibility by themselves. Use API credentials appropriate to each configured provider. [Claude Code connection guide](https://code.claude.com/docs/en/llm-gateway-connect), [OpenCode providers](https://opencode.ai/docs/providers/), [OpenCode plugins](https://opencode.ai/docs/plugins/)

Codex documents custom providers and currently supports `responses` as its wire API. It therefore exercises a different protocol boundary. [Provider configuration](https://learn.chatgpt.com/docs/config-file/config-advanced), [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)

Start the Responses design and a small compatibility spike during the first work package. Do not wait for all routing experiments to finish. Supporting two harnesses through one protocol is useful evidence, but insufficient evidence for a stable cross-protocol contract.

Further harnesses can follow through the same adapter kit. A harness that exposes only observations gets explicitly limited coverage. Merely receiving hooks cannot establish that ADRL prevented a model dispatch or accounted for all network traffic.

## Three parts with clear ownership

| Part | Responsibilities | What adding a harness should change |
|---|---|---|
| Harness adapter | Configuration, launch, authenticated workload binding, session/child mapping, utility fingerprints, hook translation, version-specific fixtures | A small adapter package, capability declaration and tests |
| Protocol profile | Parse inspection views; identify content and boundaries; preserve native streams and errors; define state, reasoning and handoff rules | A new profile only when the wire semantics differ |
| Shared ADRL engine | Resolve identity and policy; enforce restrictions and durable pins; choose permitted deployments; manage routing state; record dispatch and outcome evidence | General rules may improve through experiments, but no duplicated per-harness policy engine |

The engine should consume a common decision context: authenticated workload, lineage, profile and adapter versions, content-bearing status, request class, boundary signals, requested capabilities and policy constraints. It should return a decision that the selected profile can apply safely.

Keep the original request bytes beside that inspection view. Do not flatten all messages, tool outputs and opaque reasoning into a universal text transcript. Preserve the existing unchanged-path guarantees. Every permitted rewrite needs an explicit profile rule and regression evidence.

Selecting a protocol does not select a model family. A deployment is eligible only when both policy and the tested capability contract permit it. A gateway's ability to translate JSON is insufficient evidence of working tool calls, compaction, context handling or handoff.

## A small, versioned API surface

Harnesses should continue speaking their supported model protocol. They should not need a new ADRL prompt format. Put product administration, events and evidence under a separate namespace so they cannot collide with provider APIs.

The following is a candidate v1 surface. Publish it as a preview first; freeze its compatibility promise only after the two-harness and two-protocol tests. Existing `/healthz` and `/metrics` remain operational endpoints.

| Surface | Proposed endpoint | Meaning and authority |
|---|---|---|
| Native model traffic | `POST /v1/messages`, `POST /v1/messages/count_tokens` | Existing paths; extract their current semantics into a named profile. The shared engine checks before dispatch |
| Native model traffic | `POST /v1/responses` | New profile and implementation required. Native streaming, errors and continuation must be tested |
| Discovery | `GET /adrl/v1/capabilities` | List installed profiles, adapters, tested versions and deployment support. No credentials or sensitive inventory details |
| Session binding | `POST /adrl/v1/sessions` | Authenticate the launcher; bind a workload to an authorized policy and scoped session credential. An arbitrary client cannot declare its repository unrestricted |
| Session status | `GET /adrl/v1/sessions/{session_id}` | Return effective policy, lineage, coverage and current evidence gaps to an authorized caller |
| Evidence ingestion | `POST /adrl/v1/events` | Accept typed, scoped observations from adapters and verified outcomes from authorized verifier producers |
| Evidence reading | `GET /adrl/v1/sessions/{session_id}/timeline` | Paginated decision, dispatch and outcome records with provenance and uncertainty |
| Decision explanation | `GET /adrl/v1/decisions/{route_id}` | Explain a recorded decision, policy versions, intended destination and related dispatch attempts |

For the pilot, keep policy administration in signed configuration and the operator CLI. Avoid making a generic policy-editing API part of the first integration requirement. Ordinary harness credentials cannot release pins or loosen policy.

The event endpoint is observational in the first release: successful ingestion means the event was durably recorded, not that an action was permitted or a claimed outcome was independently verified. Model-egress enforcement remains on the request path. A future synchronous hook authorization API needs a separately specified blocking contract, timeout behavior and binding between checked content and the actual operation.

### Session and identity rules

A session request includes the adapter/version, requested profile, registered workload reference and optional parent-session reference. The server validates these against the launcher's authority and resolves the policy itself. Child binding requires authority over the parent and preserves inherited restrictions. A resumed session must restore persistent policy state.

Return an opaque session identifier, profile/version, policy version, effective coverage and an expiring credential or credential reference. The adapter maps this into the harness's supported connection mechanism. Keep upstream provider credentials separate from ADRL workload credentials. Neither a native session header nor possession of a claimed repository path is authorization.

A missing, expired or inconsistent binding must produce the documented restricted behavior or rejection. A new credential must not reset an existing restricted lineage. State the pilot's same-machine trust boundary explicitly.

### Event rules

An event envelope needs a schema version, event ID, authenticated producer, session reference, optional route reference, producer sequence, occurrence time, server receipt time, event type and typed payload. Producer and workload authority come from authentication; client-supplied labels are checked against it.

Support at-least-once delivery with idempotency scoped to producer and event ID. Return success only after durable append. Identical retries return the original acknowledgement; reuse of an ID with different content is a conflict. Keep late events and sequence gaps visible rather than inventing a complete ordering. Duplicate delivery must not double-count cost or completed tasks.

Initial adapter events can describe tool completion/failure, compaction, child relationships and task closure. A harness saying its tests passed is a reported result; a trusted verifier must bind an independently verified result to the exact task snapshot. Raw prompts, tool output and secrets do not belong in ordinary event metadata. Use approved protected references when retained content is needed.

### Coverage rules

Report capabilities separately: request interception, identity binding, new-content inspection, pre-dispatch enforcement, tool-event coverage, lineage coverage, served-destination evidence and outcome verification. Each dimension must say whether it is enforced, observed, unavailable or unknown, with its tested scope. A single integration-depth score hides too much.

Effective coverage is the intersection of the adapter's tested capabilities, selected protocol, deployment configuration and current runtime health. A plugin cannot award itself an enforcement guarantee. Preserve the coverage snapshot associated with each decision; a later software upgrade must not rewrite what an older run established.

Unknown content-bearing endpoints must be rejected on an enforcing listener until admitted by a profile. Explicit observation-only operation can be separate and visibly limited. This changes today's catch-all forwarding behavior and requires an FND/SEM disposition before implementation. It prevents a connected but unclassified endpoint from being described as protected.

### Compatibility and operations rules

- Version the public schemas, protocol profiles and adapters independently; record all three on runs. Publish supported harness version ranges with fixture evidence.
- Give product APIs typed errors for authentication, policy denial, unsupported capability, conflicting event identity and temporary unavailability. Model endpoints retain their profile's native error shape.
- Scope read access to authorized workloads. Keep the first server bound to loopback; managed remote access needs authenticated transport and isolation work before exposure.
- Define timeout, cancellation, retry and streaming behavior. Event retry safety does not make model requests or executed tools safe to replay.
- A returned route ID identifies a recorded decision; record individual dispatch attempts beneath it. Do not infer the served model from the requested alias or assume one decision equals one billable attempt.

## What “easy to integrate” should mean

Ship one installer/service, an adapter kit, generated configuration, a connection check and one consistent evidence view. A supported harness should require configuration and an optional hook package, with no source patch to the harness.

The intended user flow is: select a harness, select a registered repository policy, connect, run a diagnostic task, then inspect its timeline. Proposed CLI commands could be `adrl connect claude-code`, `adrl connect opencode` and `adrl doctor --harness opencode`. These commands do not exist today; the current CLI provides `launch`, `serve` and configuration commands.

Make usability measurable. With credentials, models and repository classification already prepared, target a new developer completing setup and a diagnostic run within 15 minutes using the quickstart, without editing ADRL internals. Record actual setup time, failed steps and manual interventions. This is an initial product target, not an achieved result or an estimate including model downloads.

The adapter kit should include schemas, a reference adapter, scrubbed traffic fixtures, event examples, a compatibility runner and a checklist generated from machine-readable capabilities. HTTP remains the core contract; language-specific helpers can follow actual integration needs.

## Build sequence with evidence gates

| Work package | Concrete output | Condition for advancing |
|---|---|---|
| P0: Define and challenge the contract | API preview schemas; adapter/profile interfaces; Claude and OpenCode fixtures; Responses state/transport spike; proposed FND/SEM wording | Examples from both protocols fit without losing security-relevant information. Unsupported behavior is explicitly rejected or scoped out |
| P1: Extract the existing path | Messages profile; shared decision context; native byte/stream/error preservation | Existing checks pass; captured Messages fixtures preserve behavior except explicitly dispositioned fixes |
| P2: Complete Claude Code | Reproducible adapter launch, workload binding, events and timeline | A real verified task plus E01-E04 failure scenarios; cost and destination evidence distinguish known from unknown |
| P3: Add OpenCode | Configuration/plugin adapter using the same engine and policy contracts | Equivalent control scenarios pass. Both adapters coexist in one service. No second routing or pin implementation |
| P4: Complete Codex/Responses | Admitted Responses profile, CLI adapter, corpus and conformance results | State, reasoning, tools, compaction, cancellation and supported transports are handled or explicitly rejected without silent downgrade |
| P5: Freeze and package v1 | Versioned contract, compatibility matrix, quickstarts and measured setup results | Two harnesses and two protocols have real evidence; every advertised capability has tests and an explicit scope |

OpenCode is the faster reuse test. Codex is the stronger test of the abstraction. Start P0's Responses work early and run its implementation work alongside integration learning as capacity permits; do not treat P4 as an optional later expansion.

For Responses, start by evaluating an HTTP streaming configuration with explicit client-carried state. If the chosen Codex version requires referenced server state or another transport, either implement and test that requirement or keep the integration in preview. Do not silently drop `previous_response_id`, conversation references, encrypted reasoning or compaction items. Their semantics can change what content the model actually receives. Responses supports continuation by reference, so request-local inspection alone cannot establish complete history coverage. [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state)

The first implementation pull request should be bounded to P0 and P1: interfaces and schemas, extraction of the Messages path, retained regression evidence, and a documented Responses admission choice. It should establish the reusable boundary before adding more routing policy. Record the proposal in the appropriate ADRs before implementing newly authorized semantics.

## Course correction remains part of the product work

The original E01-E07 queue still applies. Add **E08: portability and integration effort**. Run equivalent control scenarios through Claude Code and OpenCode, then through the Responses profile. Include concurrent sessions, child return, resume/restart, missing hooks, duplicate events, unsupported content, stream interruption and conflicting identity. A common privacy rule should have the same observable effect; protocol-specific behavior should have an explicit profile explanation.

Record differences by harness and protocol rather than pooling them into one success rate. A routing policy that works in one harness can encounter different prompts, tools and stopping behavior in another. Protocol compatibility and model capability must both be qualified before economic results transfer.

| If testing shows… | Change primarily… |
|---|---|
| Harness lifecycle or utility requests are mapped incorrectly | Adapter and its versioned corpus; SEM mappings where required |
| The API format cannot express the current shared context faithfully | Protocol interface and SEM-007; inspect affected FND/CAS assumptions |
| Correctly interpreted requests bypass a restriction | Shared enforcement implementation, or the relevant SAF/TRU contract if its premise fails |
| A cheaper model loses on completed-task cost or quality | Versioned routing/cascade policy and the supporting RTG/CAS decision |
| A hook claim cannot establish what actually happened | Evidence confidence and producer authority under MEM/EVL/TRU |
| Integrations repeatedly duplicate the same logic | Move that responsibility into the shared contract and rerun existing adapters |

This gives the taxonomy a practical job: it identifies the owner and evidence needed for each correction. It does not dictate the public API layout. Keep stable decision IDs while revising clauses; restructure buckets only when repeated ownership conflicts justify it.

## Grounding in the current repository

The current ASGI layer explicitly serves Messages and token counting. The parser's `is_api` recognizes the Messages prefix; other paths leave the gated pipeline before identity resolution, and `_forward_non_api` reads the whole upstream response. Therefore catch-all relay is neither a Responses implementation nor evidence of preserved Responses streaming or policy enforcement.

The existing ports and decision types are useful foundations, but the pipeline directly depends on Messages parsing, classification, identity conventions and response handling. Extract those dependencies deliberately. The proposed SEM-007 already calls for named profiles, a Responses state decision and a captured corpus; this proposal makes that work a product milestone.

- [Existing ASGI surface](/Users/arunmenon/projects/adrl-core/src/adrl/proxy/asgi.py)
- [Wire parsing](/Users/arunmenon/projects/adrl-core/src/adrl/wire/parse.py)
- [Pipeline and non-API forwarding](/Users/arunmenon/projects/adrl-core/src/adrl/proxy/pipeline.py)
- [Shared ports](/Users/arunmenon/projects/adrl-core/src/adrl/core/ports.py)
- [Protocol-profile proposal, SEM-007](/Users/arunmenon/projects/adrl-world-class/adr/SEM/ADRL-SEM-007.md)
- [Updated run and course-correction plan](/Users/arunmenon/projects/adrl-world-class/reports/adrl-course-correction-plan-2026-09-07.md)

The previously recorded 39 passing focused tests cover the existing simulated-gateway baseline. They establish no result for these proposed APIs or additional harnesses. This document was checked for source links and consistency with that baseline; implementation and real-harness validation remain the next work.

## Subsequent implementation

The first product foundation was implemented after this proposal: Messages/identity interfaces,
versioned decision context, capability discovery and API preview schemas. See the
[implementation record](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md)
for the applied changes and 463-test result. Session/event handlers, second-harness integration
and Responses admission remain outstanding; the proposal's implementation disclaimer describes
its original planning pass.
