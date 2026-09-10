# ADRL-SAF-009 — Egress ledger and gate-audit integrity (Proposed)

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Proposed 2026-09-02 (new, from adversarial review) · superseded by TRU-003 on 2026-09-03, pending disposition; schema and rules retained by reference |
| Maturity | D0 Design, review recommends D0 Design |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 8 |
| Related decisions | SAF-001, SAF-002, SAF-003, SAF-004, SAF-008, FND-004, MEM-001, MEM-005, MEM-006, OPS (observability) |
| Open questions | Q5, Q7 |

## Decision

Every request that leaves the machine, every gate verdict, every fail-open event, every pin, every audited release, and every operator bypass is recorded in an append-only, tamper-evident egress ledger that is separate from the routing-evidence ledger and survives its absence; the question "did this lineage's content ever leave the machine, and under which verdict?" is answerable from the egress ledger alone.

1. *Separate and surviving*: the egress ledger is written by the gate stage before forwarding (write-ahead), is not behind MEM-006's fail-safe facade (a NullProvider for the *evidence* ledger must not silence the *egress* ledger), and a write failure on a pinned lineage is a gate failure (fail-closed per FND-004 as amended).
2. *Tamper-evident*: entries are hash-chained (each entry commits to the previous entry's digest) with periodic signed checkpoints shipped off-device, so that deletion or edit of local entries is detectable by an auditor who holds only the checkpoints.
3. *Content-free*: the ledger stores hashed session/lineage keys, request class, destination rung and deployment tag, gate verdicts with detector tier and span hashes, byte counts, and actor/reason for human actions; it never stores prompt content, embeddings or locating features (MEM-005 applies).
4. *Complete for the ADRL path only*: harness traffic that bypasses `ANTHROPIC_BASE_URL` (telemetry, fast-mode and WebFetch safety checks) is outside this ledger's scope and is recorded as a known exclusion in the OPS egress baseline.

## Context and rationale

SAF-002's argument for a one-way pin is that it makes "did this code ever leave the machine?" a yes/no question. This review found that the question is not currently answerable: pin state lives in a process dict; passthrough, utility and subagent requests leave the machine without a pin check; fail-open events are invisible by design; the operator bypass is unlogged; and the routing-evidence ledger sits behind a fail-safe facade whose NullProvider means "routing continues, unlogged" — which for privacy evidence is exactly wrong. Each of those is fixed in its own decision; this gate makes the fixes verifiable. It also gives the audited human release (SAF-002 sub-clause 3) and the operator bypass (FND-004) somewhere to land that an auditor can trust, which push protection and Purview both treat as part of the control rather than an afterthought (every push-protection bypass creates an alert, an audit-log event and owner notification; every Purview label downgrade records its justification).

Tamper evidence matters because the ledger lives on the developer's machine and the developer is, in the threat model, the person most motivated to make a pinned session look unpinned. Crosby and Wallach's history-tree construction (USENIX Security 2009) is the standard reference for logs whose logger is untrusted and whose auditors hold only commitments; a hash chain with off-device signed checkpoints is the minimal practical form.

## Adversarial review (2026-09-02)

### Steelman
Without this ledger every other SAF decision is a promise; with it, each becomes a claim that can be checked. It is cheap (a few hundred bytes per request), it stores nothing sensitive, and it converts the register's most important sentence — the one-bit answer — from rhetoric into a query. It is also the artefact a the company privacy or PCI review will ask for first.

### Attacks (self-applied)
1. **Double-write cost on the hot path.** A write-ahead entry on every request adds latency at p99, especially on continuations. Mitigation: append to a local file with fsync batching bounded by a small time window; the pinned-lineage fail-closed rule applies only when the append itself errors, not when fsync is deferred.
2. **The egress ledger becomes a new PII store.** Hashed session keys joined with timestamps still identify a person's working hours. Mitigation: HMAC keys per deployment (SEM-002 sub-clause 3), retention limits, and access restricted to the audit role; content-free by construction.
3. **Checkpoints need an off-device trust anchor.** Shipping signed checkpoints requires an endpoint, which is itself egress and must be on the allow-list and available offline (queue locally). Mitigation: checkpoints are tiny, content-free, and can ride the existing telemetry path to the gateway (Q7: gateway team may already own such an endpoint).
4. **It duplicates MEM-001.** MEM-001's append-oriented ledger keyed by `route_id` looks similar. The difference is purpose and failure mode: MEM may be absent (NullProvider) and the router continues; the egress ledger may not be absent for pinned lineages. Keeping them separate is the point; a shared schema is acceptable if the availability semantics differ.
5. **Scope gap for non-ADRL egress.** Sub-clause 4 records this honestly; the complementary control is device-level.

### Evidence
- Crosby and Wallach, "Efficient Data Structures for Tamper-Evident Logging" (USENIX Security 2009) — canonical construction for tamper-evident logs under an untrusted logger with auditor-held commitments (abstract not extracted in this review; cited for the construction by title) — https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident
- GitHub Docs, "About push protection" — every bypass "Creates an alert … Adds the bypass event to the audit log … Sends an email alert" to owners; audit is part of the control; bears on the rationale — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
- Microsoft Learn, "Learn about sensitivity labels" (Purview) — label downgrade justifications are recorded and reviewable in Activity Explorer; bears on the rationale — https://learn.microsoft.com/en-us/purview/sensitivity-labels
- ADRL evidence pack, `04-register-MEM-LRN.md` — MEM-006: "if memory is unavailable, routing continues (degraded, unlogged)"; the egress ledger must not inherit this property; bears on sub-clause 1 and attack 4.
- Anthropic, "Gateway protocol reference" (Claude Code docs) — the fast-mode availability check and the WebFetch domain safety check call api.anthropic.com directly rather than following ANTHROPIC_BASE_URL; bears on sub-clause 4 — https://code.claude.com/docs/en/llm-gateway-protocol
- OWASP, "Top 10 for LLM Applications 2025" (PDF; listing confirmed via promptfoo) — LLM02 Sensitive Information Disclosure; an auditable record of what left the boundary is the standard mitigation posture — https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf

### Verdict
**PROPOSED (new).** This decision exists because the review could not verify SAF-002's central claim from the evidence pack, and because three separate amendments (FND-004 fail-open recording, SAF-002 audited release, SAF-008 classification evidence) each need a durable, trustworthy place to write. Self-applied attacks are engineering trade-offs with known mitigations. Recommended for acceptance at D0 with the write-ahead, content-free egress ledger as the D1 exit and hash-chaining plus checkpoints as the D2 exit.

## Amendments applied

New decision; no prior text.

## Follow-ups

- [ ] Schema: `egress_events(seq, prev_digest, ts, lineage_hmac, request_class, content_bearing, destination_rung, deployment_tag, gate_verdicts[], detector_tier, span_hashes[], bytes_out, actor, reason, digest)`; append-only file or table outside the MEM facade.
- [ ] Write-ahead in the gate stage; fault test: append failure on pinned lineage → request blocked; on unpinned lineage → forwarded with `ledger_degraded` mark.
- [ ] Hash chain and signed checkpoint every N entries / T minutes; verifier tool that, given checkpoints, detects deletion or edit of local entries.
- [ ] Query tool: `adrl audit --lineage <id>` answers "left the machine? (yes/no), when, to which deployment, under which verdicts".
- [ ] Record FND-004 fail-open events, SAF-002 releases, operator bypasses and SAF-008 classifications here; golden tests for each.
- [ ] OPS: document the non-ADRL egress exclusions and the device-level controls that cover them.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
| 2026-09-03 | Superseded by ADRL-TRU-003 (external review); text retained | unchanged |
