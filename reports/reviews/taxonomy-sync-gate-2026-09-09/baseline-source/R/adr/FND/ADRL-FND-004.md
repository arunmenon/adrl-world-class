# ADRL-FND-004 — Fail to last-known-safe, not fail-open

| Field | Value |
|---|---|
| Bucket | FND — System Boundary and Principles |
| Status | Superseded 2026-09-02 (see replacement) |
| Maturity | D4 Pilot, review recommends D3 Shadow — no decision in the register affects live execution for any population ("live adaptive routing intentionally blocked"), so nothing can be D4; and the failure-injection matrix has not been run against real traffic |
| Review verdict | REJECT |
| Tenets | 2, 3 |
| Related decisions | FND-001, SAF-001, SAF-002, SAF-004, SAF-005, CAS-007, MEM-006, OPS (operator controls) |
| Open questions | Q5, Q7 |

## Decision

On failure ADRL falls back to the last-known-safe behaviour for the session, which is unchanged upstream behaviour for an unpinned session and local-only-or-block for a privacy-pinned session; there is a one-step operator bypass that is audited and that cannot release a pin.

1. *Routing-path failures* (classifier timeout, ledger unavailable, policy exception, rung-selection error) fail open to the upstream gateway for unpinned sessions and to the local rung for pinned sessions.
2. *Gate-path failures* (secret scanner unavailable or timed out) fail open to upstream for unpinned sessions but mark the request `unscanned` in the ledger; for a session that is already pinned they fail closed (local rung or block per SAF-004/005). An `unscanned` request can never be the basis for releasing or skipping a pin.
3. *Proxy-path failures* (the ADRL process itself is unreachable) are not something ADRL can fail-open from; the one-step operator bypass — repoint `ANTHROPIC_BASE_URL` at the gateway — is the documented recovery and its use is logged.
4. Every automatic fail-open event is recorded with its failure class; a sustained fail-open rate above a configured threshold is itself an alert, because a layer that is silently bypassed is a layer that is silently off.

## Context and rationale

The worst case should be what you had before. If ADRL crashes, times out, or cannot reach a verdict, the request proceeds as if the layer were not installed. That is what makes the layer safe to insert into a working setup, and it is the right default for an *optimisation* layer: the pre-ADRL baseline is "everything goes to the cloud gateway", so failing to that baseline costs money, not safety.

The original text is rejected because its quantifier is wrong. "Failure defaults to unchanged upstream behaviour" is a universal statement, and it is false for the one population where ADRL has made a promise the baseline never made: privacy-pinned sessions. Once ADRL has told a developer (and an auditor) that this session's code stays on the machine, "unchanged upstream behaviour" on a scanner crash sends that code to the cloud. That is textbook fail-open in a security control — the pattern every authorization and admission-control system is warned against — and it means the pin's guarantee (SAF-002: "did this code ever leave the machine? yes or no") depends on the uptime of the scanner. The replacement keeps fail-open where the baseline is genuinely the safe state and requires fail-closed where ADRL itself created a stronger state. It also distinguishes the three failure surfaces the original conflated, because "the proxy process died" has no in-process fallback at all: the harness's `ANTHROPIC_BASE_URL` points at a dead socket, and only the operator bypass restores service.

## Adversarial review (2026-09-02)

### Steelman
For an optimisation layer inserted into a working developer setup, the pre-ADRL behaviour is by definition acceptable to the organisation, so falling back to it can never make things worse than the status quo. Fail-open is what lets the layer be piloted without a change-management fight, and the "escape hatch must be better proven than the feature" ordering is exactly right. Kubernetes admission webhooks, WAFs and inline proxies all offer fail-open precisely because availability of the protected path usually matters more than the marginal control.

### Attacks
1. **Fail-open contradicts SAF-002/SAF-004 for pinned sessions.** SAF-002 says once local-only, stays local-only; SAF-004 says a pinned session cannot fall back to cloud. FND-004 says on failure the request "proceeds exactly as if the layer were not installed" — i.e. to the cloud gateway. Both cannot be true. In the one situation where the ordering matters (scanner or policy failure on a pinned session), the D4 escape hatch overrides the D2 privacy gate. The register's own "scrutinise" note calls FND-004 "the reason this can be piloted at all"; it is also the reason the pin is not a guarantee.
2. **Fail-open is the recognised anti-pattern for security controls.** The AuthZed analysis states fail-open "can inadvertently grant access to unauthorized users during unexpected failures" and recommends fail-closed for "sensitive data handling". The Gardener issue on Kubernetes `failurePolicy=Ignore` shows the operational reality: teams misread fail-open semantics and end up with policy that is bypassed or enforced unpredictably. ADRL's scanner is a data-handling control; the same reasoning applies.
3. **"Proxy crashes → unchanged upstream behaviour" is physically false.** The harness talks to ADRL because `ANTHROPIC_BASE_URL` points at it. If the ADRL process is dead, the harness gets a connection refused, not the gateway. Only a process supervisor, a network-level bypass, or the operator repointing the variable restores service. The decision claims a property (transparent failure) for a failure class (proxy death) it cannot deliver in-process. In shadow mode this is the *only* way ADRL can affect execution, and it is the failure the decision does not cover.
4. **Silent fail-open turns the layer off without anyone noticing.** If the classifier times out on 30% of turns and each one falls open to frontier, the cost savings evaporate and the ledger records nothing useful — but nothing alerts, because "no change" is by design invisible. A fail-open rate is an SLI that must be surfaced; the decision does not require it.
5. **D4 is not supportable.** D4 means "affects execution for a constrained population". The evidence pack states live adaptive routing is intentionally blocked and the corpus is single-user. The fail-open *mechanism* (modes `off`/`shadow`/`live`) exists and is tested; that is D2, and running it against real shadow traffic is D3. There is no pilot population for whom the fallback has been exercised under real failure.
6. **The operator bypass is under-specified.** "One-step" says nothing about who may invoke it, whether it is audited, whether it can be invoked per session or only globally, or whether it releases pins. A bypass that can release a pin is a pin release path, which SAF-002 forbids.

### Evidence
- AuthZed, "Understanding 'Failed Open' and 'Fail Closed' in Software Engineering" (blog, 2024) — fail-open prioritises availability, fail-closed security; fail-open in authorization "can inadvertently grant access to unauthorized users during unexpected failures"; bears on attacks 1, 2 — https://authzed.com/blog/fail-open
- gardener/gardener, issue #7013 "Webhook with `failurePolicy=Ignore` can be problematic" (GitHub) — documents operational confusion over Kubernetes fail-open webhook semantics and the resulting mismatch between intended and actual policy enforcement; bears on attack 2 — https://github.com/gardener/gardener/issues/7013
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — `ANTHROPIC_BASE_URL` is the single configured endpoint; there is no client-side fallback host when the configured gateway is unreachable; bears on attack 3 — https://code.claude.com/docs/en/llm-gateway-connect
- Google SRE, "Canarying Releases" (SRE Workbook, ch. 16) — a canary must have a population and a duration long enough that "the observed behavior is actually attributable to the canaried change"; bears on attack 5 (no pilot population exists) — https://sre.google/workbook/canarying-releases/
- Cisco Community, "Fail-open & Fail-close explanation" (knowledge base; title from search, not fetched) — general networking definition of the terms; background for attack 2 — https://community.cisco.com/t5/security-knowledge-base/fail-open-amp-fail-close-explanation/ta-p/5012930

### Verdict
**REJECT.** Attack 1 is decisive on its own: the decision as written directly contradicts two accepted SAF decisions for the population those decisions exist to protect, and the register's ordering ("the escape hatch should be better proven than the feature it protects") makes the escape hatch the *winner* of that contradiction. Attacks 2 and 3 show the original conflated a legitimate optimisation-layer default with a security-control default and with an infrastructure failure it cannot handle in-process. Attack 5 removes the D4 claim. The steelman survives for unpinned sessions, and the replacement keeps that behaviour verbatim for them; what supersedes the original is the split by failure class and by pin state, plus the audit and alerting requirements. Attack 6 is closed by "audited and cannot release a pin".

## Amendments applied

- Replaced the universal "failure defaults to unchanged upstream behaviour" with "falls back to the last-known-safe behaviour for the session", defined per pin state.
- Added sub-clauses 1–3 splitting routing-path, gate-path and proxy-path failures with distinct behaviour; gate-path failures on pinned sessions fail closed; `unscanned` marking introduced.
- Added sub-clause 4 requiring fail-open events to be recorded by class and rate-alerted.
- Operator bypass made audited and explicitly unable to release a pin.
- Maturity recommendation lowered to D3.

## Follow-ups

- [ ] Fault-injection matrix (each run against replayed real traffic in shadow): classifier timeout; SQLite locked; scanner exception; scanner timeout; LiteLLM 5xx; LiteLLM 429; proxy SIGKILL. For each, assert the replacement decision's behaviour per pin state and that the ledger records the failure class.
- [ ] Golden test: pinned session + scanner exception → request goes to local rung or is blocked; never to the gateway.
- [ ] Golden test: operator bypass invoked on a pinned session → session remains pinned (bypass affects routing, not gating) and the bypass event is in the ledger with actor and reason.
- [ ] SLI: fail-open rate per failure class, with an alert threshold; add to the OPS dashboard.
- [ ] Deployment runbook: document that proxy-process death has no in-process fallback; specify supervisor/restart policy and the operator bypass procedure.
- [ ] Re-evaluate maturity to D4 only after a named pilot population has experienced at least one injected and one organic failure of each class.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Superseded: fail-open retained for unpinned sessions only; fail-closed for pinned sessions; failure classes split; bypass audited and pin-preserving; D4→D3 recommended | "Failure defaults to unchanged upstream behaviour, with a one-step operator bypass." |
