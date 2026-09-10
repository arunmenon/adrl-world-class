# ADRL-FND-001 — Transparent control layer, protocol-scoped

| Field | Value |
|---|---|
| Bucket | FND — System Boundary and Principles |
| Status | Accepted · amended 2026-09-02 · product boundary clarified 2026-09-07 |
| Maturity | D3 Shadow, review recommends D3 Shadow for the Anthropic-Messages path only; the Codex CLI (Responses API) path has no evidence and should carry D0 |
| Review verdict | AMEND |
| Tenets | 1, 7 |
| Related decisions | FND-002, FND-004, SEM-001, SEM-004, SAF-004, SAF-005, CAS-004 |
| Open questions | Q1, Q7 |

## Decision

ADRL is a protocol-transparent, removable control layer between an Anthropic-Messages-format coding harness and the model gateway; it never changes the wire contract the harness observes except through the enumerated user-facing surfaces owned by SAF.

1. *Protocol-transparent* means: request headers the harness marks forward-unchanged (`anthropic-version`, `anthropic-beta`) reach the gateway byte-for-byte; response bodies, streaming events (including keep-alive pings) and upstream error wording are relayed unmodified on the passthrough path; and any body the layer must rewrite for a non-Claude rung (for example stripping `thinking`, `cache_control`, or beta tool fields) is rewritten by ADRL, not left for the upstream to reject.
2. *Removable* means the golden test: point `ANTHROPIC_BASE_URL` back at the gateway and every behaviour is unchanged, with nothing to uninstall and no residual state the harness depends on.
3. *Enumerated surfaces* means the only developer-visible differences ADRL may introduce are those listed in SAF-004/SAF-005 (blocked or surfaced failures on a pinned session) and the harness's own capability-degradation behaviour when a request is served by a non-Claude rung; each such surface must be documented, and each is a measured cost, not a transparency violation.
4. Harnesses that speak the OpenAI Responses API (Codex CLI) are out of scope for this decision until a Responses-format discriminator and corpus exist (SEM-001 follow-up).
5. *Product boundary, clarified 2026-09-07*: ADRL is developed as one reusable policy, routing and evidence engine with harness adapters and versioned protocol profiles (SEM-007). Harness setup, identity correlation and event translation belong to adapters; native model semantics belong to profiles. Product APIs use a separate `/adrl/v1` namespace. This direction does not expand the currently supported model-traffic protocols beyond clause 4's admission rule.


## Claude initial-choice candidate, 2026-09-09

<!-- taxonomy-sync:claude-adapter:ADRL-FND-001 --> Scoped application: a constructor-only Claude initial-choice experiment may rewrite only the model field after enforcing gates in LIVE mode. Normal frontier, OFF and SHADOW paths remain byte-exact. This candidate has no startup setting or approved live launch profile; it does not grant an exception to admission. Continuations preserve non-model fields; no cross-model mid-session handoff is implemented. [Implementation and evidence limits](../../reports/reviews/claude-adapter-2026-09-09/report.md). Formal maturity/status/verdict are unchanged.


## Product service evidence, 2026-09-07

The shared product API now binds authenticated local sessions, records encrypted observations and serves scoped evidence reads. Bound Messages traffic rejects conflicting identity and unadmitted endpoints. Local ADRL credential headers are stripped before gateway dispatch; provider credentials and unchanged body bytes are preserved. Unbound legacy forwarding remains outside this guarantee.

The [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md)
links the 506-test result, loopback smoke check, source hashes and remaining limitations.
Architectural status is unchanged by this evidence update; historical maturity statements
below retain their dated review scope.

## Earlier foundation implementation, 2026-09-07

The Messages boundary and Claude Code correlation adapter have been extracted. Capability
discovery is implemented; session, event and evidence-reading APIs are preview schemas with
unimplemented operations rejected locally. Original Messages relay behavior is covered by the
retained regressions. Unclassified provider paths still use legacy forwarding without profile
guarantees; rejecting unsupported model operations remains release work. The historical D3 claim
above is not transferred to this new implementation, whose extracted path has offline D2 evidence.
See the [implementation record](/Users/arunmenon/projects/adrl-world-class/reports/adrl-product-foundation-implementation-2026-09-07.md).

## Context and rationale

"Transparent" is a testable property, not a marketing word. Claude Code asks for one model alias and gets back a normal Anthropic-protocol response; it does not know a router exists. The removal test is the anchor: point `ANTHROPIC_BASE_URL` back at the gateway and everything still works.

The amendment narrows the claim in two ways that the original text left implicit. First, transparency is a property of the *wire contract*, not of the developer's experience: SAF-004 and SAF-005 deliberately surface failures to the developer, and a first request served by a local model will, per Anthropic's own gateway contract, cause Claude Code to disable a rejected capability (adaptive thinking, thinking signatures, mid-conversation system messages, `cache_control` on those messages) *for the rest of the conversation*. Those are real, deliberate behaviour changes and the decision has to own them rather than claim they do not exist. Second, the original text names Codex CLI as a harness, but Codex CLI speaks only the OpenAI Responses API (Chat Completions support was removed in February 2026), so nothing in the Anthropic-shaped discriminator, session key or continuation rule applies to it, and no Codex traffic is in the Phase 0 corpus.

## Adversarial review (2026-09-02)

### Steelman
A layer that can be inserted and removed with zero harness changes is the only kind of layer an enterprise developer population will tolerate; every alternative (plugins, harness forks, per-developer config) has a support cost that dwarfs the savings. Anthropic publishes a gateway contract precisely so that such layers can be built, and the removal test is a crisp, automatable definition. The decision is the licence for everything else in the register.

### Attacks
1. **The decision contradicts SAF-004/SAF-005 as written.** "If a developer ever has to change how they work because of ADRL, this decision has been violated" — but SAF-004 says a pinned session that cannot complete is *surfaced to the developer*, and SAF-005 *blocks*. Both are developer-visible behaviour changes that do not exist without ADRL. Either FND-001 is violated by design, or "transparent" needs a narrower definition.
2. **A local first request silently degrades the whole conversation.** Anthropic's gateway protocol states that Claude Code sends `thinking: {"type": "adaptive"}` to model names it does not recognise (gateway aliases included), and that when an upstream rejects the `thinking` field, a thinking signature, a mid-conversation system message, or a `cache_control` marker, Claude Code "retries the request and disables the rejected capability for the rest of the conversation". If ADRL routes the first turn to a local rung and the rejection propagates, extended thinking is off for the session even after escalation to frontier. That is invisible to the developer and to the ledger (it looks like frontier answering without thinking) and it directly poisons the quality signal MEM/LRN rely on.
3. **The transparency test is a removal test, not a shadow test.** D3 Shadow means the layer runs against real traffic without affecting execution. In shadow, ADRL relays everything unchanged, so shadow evidence proves nothing about transparency when ADRL *does* alter a request (rewrite for local, strip thinking on handoff). The claimed maturity is for the passthrough path only.
4. **Codex CLI is named but unsupported.** Codex CLI's `wire_api` accepts only `"responses"`; the Responses API uses `input` items, `function_call_output`, and encrypted reasoning items — none of which SEM-001's taxonomy recognises. Naming Codex in the boundary decision without a corpus, discriminator or session key silently expands scope that Phase 0 did not establish.
5. **"Inspect without modifying" is the vendor's rule, and ADRL must modify.** The gateway contract says "a gateway that rewrites or redacts request bodies for content inspection breaks the pairing the same way stripping does, so inspect without modifying." A router that sends a request to a non-Claude model *must* rewrite the body (drop beta fields, `cache_control`, `thinking`, `output_config`). The decision has to state who owns that rewrite and that it never happens on the passthrough/frontier path.
6. **Egress that bypasses the layer.** The same contract documents that Claude Code sends telemetry, version checks, the fast-mode availability check and the WebFetch domain-safety check to `api.anthropic.com` *directly*, ignoring `ANTHROPIC_BASE_URL`. ADRL is therefore not the only path off the machine, which matters for SAF (see proposed SAF-008/009) and for any claim that "the layer sees all traffic".

### Evidence
- Anthropic, "Gateway protocol reference" (Claude Code docs, 2026) — documents which headers must be forwarded verbatim, that Claude Code sends adaptive `thinking` to unrecognised model names, that a rejected capability is disabled for the rest of the conversation, that gateways must "inspect without modifying", and that some traffic bypasses `ANTHROPIC_BASE_URL`; bears on attacks 2, 5, 6 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs, 2026) — troubleshooting table shows a gateway that rewrites context-limit errors defeats Claude Code's auto-compaction, and that capability variables have no effect behind `ANTHROPIC_BASE_URL`; bears on attacks 1, 5 — https://code.claude.com/docs/en/llm-gateway-connect
- Daniel Vaughan, "Codex CLI Custom Model Providers: The Complete Configuration Guide" (blog, Apr 2026; third-party) — states `wire_api` accepts only `"responses"` and that Chat Completions support was removed Feb 2026; bears on attack 4 — https://codex.danielvaughan.com/2026/04/23/codex-cli-custom-model-providers-configuration-guide/
- OpenAI, "Reasoning models" (API guide) — encrypted reasoning items, `store=false`, and same-model-family reuse only; shows the Responses wire shape is structurally different from Messages; bears on attack 4 — https://developers.openai.com/api/docs/guides/reasoning
- George Sung, "Tracing Claude Code's LLM Traffic" (Medium, 2026) — empirical wire trace of Claude Code showing background requests and sub-agent request shapes, confirming the layer sees a mix of traffic classes; bears on attack 3 — https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5

### Verdict
**AMEND.** Attacks 1, 2, 4 and 5 land. The decision's strongest form — removable, protocol-faithful — survives, but the sentence "if a developer ever has to change how they work … this decision has been violated" is contradicted by two accepted SAF decisions and by documented harness behaviour when a non-Claude rung answers. The fix is to define transparency at the wire level, enumerate the deliberate exceptions, and assign the body-rewrite responsibility to ADRL. Attack 4 is a scope correction rather than a rejection: nothing in the register is wrong for Codex, it is simply unevidenced. Attack 6 does not change this decision but feeds the proposed SAF-008/009. Attack 3 lowers confidence in the D3 claim for the rewrite path; the passthrough path is legitimately D3.

## Amendments applied

- Replaced "transparent control layer between the coding harness and model gateway" with "protocol-transparent, removable control layer between an Anthropic-Messages-format coding harness and the model gateway".
- Added sub-clause 1 defining protocol transparency (forward-unchanged headers, unmodified streaming/errors on passthrough, ADRL-owned rewrite for non-Claude rungs).
- Added sub-clause 2 making the removal test the normative definition.
- Added sub-clause 3 enumerating the permitted developer-visible surfaces (SAF-004/005, harness capability degradation on non-Claude rungs).
- Added sub-clause 4 scoping Codex CLI out until evidence exists.

## Follow-ups

- [ ] Golden test: first user turn routed to local rung → assert that the harness does NOT receive a `400` naming `thinking`/`adaptive` (ADRL strips the field before the local endpoint), and that a later escalation to frontier still carries `thinking` enabled. Record the outcome in `tests/test_router_proxy.py`.
- [ ] Golden test: passthrough path relays SSE `ping` events and upstream error bodies byte-for-byte (the gateway contract's 300 s byte watchdog and error-wording retry both depend on it).
- [ ] Measurement: in shadow, count sessions where the harness would have disabled a capability because of ADRL's rewrite; report as a transparency-violation rate.
- [ ] Write the "developer-visible surfaces" list as an appendix to SAF-004/005 and link it from this decision.
- [ ] New ADR (SEM): Responses-API discriminator and session key for Codex CLI, status Proposed, before Codex is named as in scope anywhere else.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-09 | <!-- taxonomy-sync:claude-adapter:ADRL-FND-001 --> [Offline Claude candidate](../../reports/reviews/claude-adapter-2026-09-09/report.md); Scoped application: a constructor-only Claude initial-choice experiment may rewrite only the model field after enforcing gates in LIVE mode. Normal frontier, OFF and SHADOW paths remain byte-exact. This candidate has no startup setting or approved live launch profile; it does not grant an exception to admission. Continuations preserve non-model fields; no cross-model mid-session handoff is implemented. | Previous decision wording and dated evidence preserved; no grade change |
| 2026-09-07 | Recorded applied product services, their scoped D2 evidence and limitations | Decision policy unchanged; the prior foundation did not implement session/event/read services |
| 2026-09-07 | Added the user-authorized multi-harness product boundary and scoped implementation evidence | Clause 5 and the dated implementation section were absent; clauses 1-4 retained |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: transparency defined at wire level; SAF surfaces enumerated; Codex CLI scoped out pending evidence | "ADRL is a transparent control layer between the coding harness and model gateway." |
