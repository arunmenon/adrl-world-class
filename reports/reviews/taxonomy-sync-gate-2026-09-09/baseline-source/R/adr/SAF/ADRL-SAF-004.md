# ADRL-SAF-004 — Pinned sessions fail loudly, in the harness's dialect

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D2 Tested (the surfacing contract with the harness is untested; the no-cloud rule depends on FND-002's rung-closed fallback, also untested) |
| Review verdict | AMEND |
| Tenets | 2, 5 |
| Related decisions | SAF-002, SAF-005, SAF-006, CAS-007, FND-001, FND-002, FND-004, SEM-004 |
| Open questions | Q5 |

## Decision

A pinned lineage cannot fall back or escalate to any cloud rung by any actor — ADRL, the gateway's fallback groups, or a retry — and unresolved failure is surfaced to the developer as a non-retried, harness-recognisable error that names the pin, the detector and the recovery options.

1. *Non-retried* means the response uses a status and body the harness does not auto-retry (a 4xx with a stable `capability_rejected:`-style token or the vendor's own error wording), so the developer sees one clear failure rather than a retry storm or a silent stall.
2. *Recovery options* are: continue locally with reduced context (developer-initiated `/compact`), the audited release path of SAF-002 sub-clause 3 where policy permits, or stop; the message must not suggest disabling ADRL.
3. Within the local rung, escalation to a larger local model is permitted and is the preferred first recovery; a pinned lineage's fallback set in the gateway is the local rung only (FND-002 sub-clause 2).

## Context and rationale

A pinned session fails loudly rather than reaching for cloud. On a pinned route escalation is not available; if work cannot complete, the developer is told. "Just this once, use cloud" converts a privacy guarantee into a probability.

The amendment closes the two paths by which cloud is still reachable — the gateway's own fallback machinery (which does not know about pins) and harness auto-retry — and specifies *how* the failure is surfaced, because the harness is not a passive display. Claude Code's documented behaviour is to retry on some errors, to disable a capability for the rest of the conversation on others, and to auto-compact only when it recognises a too-long error in its own wording. A block that arrives as a generic 500 produces retries; a block that arrives as a 400 the harness does not recognise produces a dead end the developer must diagnose. "Surfaced to the user" is therefore a protocol design problem, and the decision has to own it. The amendment also names the obvious first recovery the original omitted: a bigger local model is still local.

## Adversarial review (2026-09-02)

### Steelman
This is the decision that turns the pin from a preference into a guarantee. Every "just this once" path is a probability distribution over exfiltration, and an auditor cannot reason about a probability. Failing loudly is also honest to the developer: they learn that the task is beyond the local rung *because* of the pin, which is information they can act on (split the task, remove the secret from the context, ask for a release).

### Attacks
1. **The gateway can escalate to cloud without asking.** LiteLLM's fallback and context-window-fallback groups re-route on errors and on input size. If a pinned request to `local` overflows and the `local` group's fallback contains a cloud deployment, the request is served from the cloud with no ADRL decision involved. "Cannot escalate to cloud" must bind the gateway configuration, not only ADRL's policy.
2. **"Surfaced" is undefined at the protocol level.** Claude Code retries some errors, disables capabilities on others, and matches too-long errors by wording. A block delivered as a 5xx invites retries (each re-sending the pinned transcript to ADRL — harmless locally, but a stall for the developer); a block delivered as an unrecognised 4xx is a confusing dead end. The decision must specify status, body and stability of the error token, or the surfacing fails in practice.
3. **The failure message is a social-engineering surface.** A developer blocked on a pinned session, under deadline, with an error that says "ADRL blocked this request", will look for the off switch. The register admits this outcome is worse than the pin. The message must route the developer to legitimate recoveries (compact, larger local, audited release), never mention the bypass variable, and be tested for that.
4. **Local escalation is missing.** RTG-001 has one local rung; in practice a local rung contains several models (a 7B fast model and a 70B slow one, say). "Escalation is not available" on a pinned route forecloses the obvious safe recovery. The decision should permit intra-rung escalation explicitly.
5. **Utility calls fail differently.** On a pinned session, a title or suggestion call that cannot be served locally should not "fail loudly" — that would surface a spurious error for a cosmetic request. SEM-004 as amended answers with an empty valid response; this decision should defer to it so the two do not conflict.
6. **Developer-side escape hatches exist outside ADRL.** The developer can set `ANTHROPIC_BASE_URL` back to the gateway, or use the harness's direct-to-Anthropic paths (fast mode check, WebFetch safety check) that ignore the gateway variable. SAF-004 cannot prevent that and should not claim to; it can only make the *ADRL path* airtight and leave device-level egress to the proposed SAF-008/009.

### Evidence
- LiteLLM, "Fallbacks (Provider Failover)" — fallbacks, content-policy fallbacks and context-window fallbacks re-route automatically; bears on attack 1 — https://docs.litellm.ai/docs/proxy/reliability
- Anthropic, "Gateway protocol reference" (Claude Code docs) — Claude Code retries and disables a capability on certain rejections; retry logic "matches on the upstream's error wording"; a gateway envelope breaks recovery "unless the envelope's message carries a stable `capability_rejected:` token"; bears on attack 2 — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — a gateway-worded context-limit error is not recognised, so Claude Code "doesn't compact and retry automatically"; `/compact` is the manual recovery; bears on attacks 2, 3 — https://code.claude.com/docs/en/llm-gateway-connect
- GitHub Docs, "About push protection" — a block is accompanied by "a detailed message explaining the reason for the block" and structured bypass reasons; precedent for a block message that routes to legitimate recovery; bears on attack 3 — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
- AuthZed, "Understanding 'Failed Open' and 'Fail Closed'" (blog) — fail-closed for sensitive data handling; supports the steelman — https://authzed.com/blog/fail-open

### Verdict
**AMEND.** Attack 1 lands and is the substantive change: "cannot escalate to cloud" is only true if the gateway's fallback groups are rung-closed for pinned traffic. Attack 2 lands: "surfaced to the user" has no protocol definition and the harness's documented behaviour makes the naive implementation fail. Attacks 3 and 4 are one clause each and materially improve the developer outcome the register worries about. Attack 5 is resolved by deferring to SEM-004. Attack 6 correctly bounds the decision's claim. The principle — no cloud, fail loudly — is preserved verbatim in spirit.

## Amendments applied

- Replaced "cannot fall back or escalate to cloud" with "cannot fall back or escalate to any cloud rung by any actor — ADRL, the gateway's fallback groups, or a retry".
- Replaced "unresolved failure is surfaced to the user" with the non-retried, harness-recognisable error contract naming pin, detector and recovery options.
- Added sub-clause 1 (error status/token contract), sub-clause 2 (permitted recoveries; never suggest disabling), sub-clause 3 (intra-local escalation permitted; local-only gateway fallback).

## Follow-ups

- [ ] Fault test with a LiteLLM config whose `local` group has a cloud fallback: pinned overflow request → assert no cloud call (CI check on config: pinned fallback groups are local-only).
- [ ] Protocol test: block response against current Claude Code — assert exactly one visible error, no auto-retry, and that `/compact` is offered; repeat on each Claude Code release used at the company.
- [ ] Copy review of the block message: names pin and detector, lists recoveries, does not mention `ANTHROPIC_BASE_URL` or any bypass.
- [ ] Add intra-local escalation (small→large local model) to `router/escalation_controller.py` for pinned lineages; golden test that it is tried before surfacing.
- [ ] Coordinate with SEM-004: cosmetic utility calls on a pinned session never produce a surfaced error.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: binds gateway fallbacks and retries; defines the surfacing contract; permits intra-local escalation | "A pinned session cannot fall back or escalate to cloud; unresolved failure is surfaced to the user." |
