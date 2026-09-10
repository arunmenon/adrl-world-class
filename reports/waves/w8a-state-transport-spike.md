# W8A: Responses admission risk investigation

Packet `W8A-spike-v1`, prepared during W0 on 7 September 2026. Design investigation only;
no profile registration or real provider calls. Owner: Codex; disposition: Arun Menon.
Use the existing [admission scope](/Users/arunmenon/projects/adrl-core/docs/responses-admission.md)
and [roadmap](../adrl-implementation-roadmap-2026-09-07.md). Owning ADR: SEM-007, with
FND-001, SEM-003, SAF-001/002/007, MEM-010, CAS-004/007 and TRU-001 boundaries.

Time box: at most five engineering days, one writer, at most three failed repairs per task.
No new API budget is approved. Record exact installed versions when inspecting a harness;
configuration support alone is not evidence that an end-to-end session works.

Answer these questions in a go/narrow/defer report before building the full profile:

1. Can the named native harness use the chosen HTTP transport with client-carried state,
   or does its observed request flow require server state or WebSockets?
2. Which item types, compaction/opaque reasoning custody and tool-output associations are
   indispensable? Which require a policy-compatible state resolver rather than request-local
   interpretation?
3. How do cancellation, reconnect, retry ambiguity, tool streaming and native errors behave?
   Preserve provider objects and native bytes; unsupported state must be rejected explicitly.
4. Can a privacy restriction be retained across those states and prevent incompatible provider
   handoff? No translator may discard state to make a fixture pass.
5. What remains missing for a real run: account/access mode, exact versions, bounded usage,
   approved task repository and private evidence lifecycle?

Start with local source/config inspection and official primary documentation where needed.
Inventory observations separately from assumptions and planned conformance cases. Do not run a
native model call merely to discover configuration. Real compatibility capture requires its own
bounded packet under the existing account authorization. W3/W5 contracts and W6 controls remain
dependencies of full admission. An unsuccessful spike narrows the product scope honestly; it
does not create a hidden Chat Completions translation or a provider bypass.
