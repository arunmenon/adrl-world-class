# TRU - Trust, Residency and Egress

**Planning checkpoint, 2026-09-08:** the user requested the target adaptive routing/RSI architecture before further implementation. [Blueprint](../../reports/adrl-adaptive-routing-rsi-blueprint-2026-09-08.md) and [all-ADR map](../../reports/research/adaptive-routing-blueprint-2026-09-08/taxonomy-map.md) are proposals for disposition. Implementation continuation is paused; no decision wording, status or maturity is changed by the blueprint.

**W3.2 current pinned-engine validation, 2026-09-08:** [receipt and transport correction](../../reports/adrl-w3-transport-receipts-2026-09-08.md)
separates stopped preparation from active I/O while preserving original ownership and v1 history.
895 tests and all eleven checks pass, with zero skips and 316 stable inputs. All thirteen
fixtures and the image are absent; no new cleanup exception. The bounded d2 synthetic lifecycle
closes; active-copy custody is next. Full W3, real-harness/independent qualification and all
architectural status/maturity fields remain unchanged. Inventory: 371 fields/381 entries.


**W3.2 runtime prototype, 2026-09-08:** [one-shot fixture execution](../../reports/adrl-w3-isolated-launch-2026-09-08.md).
Permanent launch denial, authenticated lifecycle and serialized recovery are implemented;
861 offline tests and eleven checks pass, with eight engine cases skipped. Two bounded engine
runs each had 3 passes/1 failure; lost stopped-create receipt diagnosis remains open. All eight
fixtures and one image are absent, including one documented operator-cleanup exception.
Schema 12 inventories 370 fields/380 entries. Eight ADRs preserve prior text and every grade;
no exact-close, learning, real-harness or full-W3 qualification.


**W3.2 identity research, 2026-09-08:** [resolved startup comparison](../../reports/adrl-w3-execution-identity-2026-09-08.md).
101 offline cases and seven new engine observations passed; all seven fixtures and one image
were removed. Original ownership and a pinned capability profile remain mandatory; task completion cannot follow from a restart counter.
The 812-test runtime baseline is reused after verifying 306 hashes. Eight ADRs preserve prior
text and all grades; full W3 remains open.


**W3.2b2d2 research, 2026-09-08:** [launch identity gate](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md).
Keep the authenticated preparation binding and proposed execution identity distinct. A default-looking change is not blanket authority. Proposed permanent one-shot denial and abort/discard remain unimplemented.
The unchanged 812-test baseline is reused with 306 verified hashes. Eight ADRs preserve prior text and grades; full W3 stays open.


**W3.2b2d1 update, 2026-09-08:** [stopped ownership](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md).
Exact returned resource/engine/configuration evidence establishes scoped cleanup authority. No adoption from names, labels or saved PIDs. Host/daemon administration and database/key rollback limits remain explicit.
All 812 tests and eleven checks pass. Seven owning ADRs preserve prior wording, status and maturity; full W3 remains open.


**W3.2b2c research, 2026-09-08:** [writer-boundary observations](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md).
The proposed backend must establish original resource/engine/configuration ownership before recovery. Labels, caller assertions and saved host PIDs alone grant no authority.
Six synthetic observations are separate from the unchanged 759-test runtime baseline. No status, maturity or release promotion.


**W3.2b2b2 update, 2026-09-08:** [process coordination](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md).
Admission uses the existing authenticated v2 attempt and bound canonical workspace. Lost readable authority requests stop; no caller proof or persisted PID grants release authority. Broader isolation and same-account hostile-state defense remain open.
All 759 tests and eleven checks pass. Prior status/maturity fields remain unchanged; full W3 remains open.


**W3.2b2b1 update, 2026-09-08:** [key revocation](../../reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md).
After a failed shred audit, persistent revocation still prevents product payload access, rebinding and new observations. No new identity authority or public API operation.
All 724 tests and eleven checks pass. No status or maturity promotion; full W3 stays open.

**W3.2b1 update, 2026-09-08:** [owned process groups](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md).
Cleanup authority comes from the in-memory owned launcher, not saved PIDs; workload assertion and SCM qualification are unchanged.
All 669 tests and eleven checks pass. No architectural-status or maturity promotion;
full W3 and exact task-close attribution remain open.

**W3.2a update, 2026-09-08:** the [internal attempt journal](../../reports/adrl-w3-2a-attempt-journal-2026-09-08.md)
records encrypted starts, close requests and interruption, preserving original initial state
through retries. All 631 tests and eleven checks pass. Journal reservation is not a process
lock; supervisor/capture association and recovery remain open. No status or maturity promotion.

**W3.1 update, 2026-09-08:** [retained operator captures](../../reports/adrl-w3-1-operator-captures-2026-09-08.md)
now preserve encrypted capture-time output through an internal API. All 593 tests and eleven
checks pass. Exact task-close attribution, active-copy erasure/crash recovery and verifier/CLI
integration remain later W3 work. No maturity grade or architectural status is promoted.

**Current session verification update, 2026-09-07:** [TRU-001](ADRL-TRU-001.md) record
API preview 4, independent encrypted session receipts and 532 passing tests. Two verifier jobs
each passed eight tests on the same prior pilot task; no general graduation or learning admission
follows. See the [report](../../reports/adrl-session-verification-2026-09-07.md). Earlier notes
below preserve their original scope.

**Live observation pilot, 2026-09-07:** [ADRL-TRU-001](ADRL-TRU-001.md) records
API preview 3 and its scoped live evidence: 18 reconciled tool events in one Claude Code session,
with 511 passing implementation tests. No general graduation or gateway-control claim follows.
See the [pilot report](../../reports/adrl-live-observation-pilot-2026-09-07.md); earlier notes below retain their dated scope.

**Latest product service update, 2026-09-07:** [TRU-001](ADRL-TRU-001.md) record the applied session,
observation and evidence services, with 506 passing tests and a synthetic loopback HTTP check.
This is D2 evidence for the tested scope; real harness and cross-protocol validation remain
pending. See the [implementation report](../../reports/adrl-product-services-implementation-2026-09-07.md).

**Earlier foundation update, 2026-09-07:** [TRU-001](ADRL-TRU-001.md) distinguishes the new adapter's
correlation signals and capability endpoint's distribution manifest from authenticated workload
authority. The product credential/session service remains pending; no full-contract maturity
reassessment is claimed here. See the [synchronization record](../../reports/adrl-register-sync-2026-09-07.md).
The implementation defects described below are the dated 2026-09-03 review baseline.

**Core question:** Which deployments may this workload's content reach, and can we prove where it went?
**Owns / does not own:** Owns workload identity (which repository and data class a lineage belongs to, and how that is known), the permitted deployment set (which concrete endpoints, trust zones and geographies may serve a lineage), and egress anchoring (the tamper-evident, externally anchored record of where content actually went). Does not own content scanning, pins, feasibility or blocking (SAF), rung choice inside the permitted set (RTG), or execution and escalation mechanics (CAS).

## Why this bucket exists (2026-09-03)

The 2026-09-02 review proposed SAF-008 (repository and data-class gate) and SAF-009 (egress ledger) inside SAF. The first implementation of the register (`adrl-core`, 2026-09-02) built both as specified and an external review on 2026-09-03 showed that both, as specified, are labels rather than controls: repository identity was read from prompt text and is spoofable; residency was carried but never compared to a deployment's geography; "local" was a rung name, so a local model group pointed at a remote host passed every configuration check and was recorded as never leaving the machine; and egress checkpoints existed only as a manual method signed with a development key. None of these is a SAF question. SAF asks what is forbidden in the content; TRU asks whom the content may be sent to and how that is proven. The bucket is created so that security owns those three decisions with their own maturity ladder, and so that SAF's gates operate on an authenticated identity and a concrete deployment rather than on strings.

## Review summary (2026-09-03)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-TRU-001 | Authenticated workload identity | PROPOSED (new) | none → D0 | Repository identity must come from a trusted launcher assertion tied to SCM inventory plus a content fingerprint, never from prompt or tool text; unknown identity is local-only |
| ADRL-TRU-002 | Permitted deployment set | PROPOSED (new) | none → D0 | The monotone object is a signed inventory entry (deployment id, rung, provider, api_base, trust zone, geo, data-use profile), not a rung label; dispatch yields a served-deployment receipt |
| ADRL-TRU-003 | Egress anchoring | PROPOSED (new) | none → D0 | Automatic signed checkpoints under a separate externally managed key, off-device anchoring with acknowledgements, verifier checks signatures; the left-the-machine answer is receipt-based |

Dispositions requested: accept TRU-001 to TRU-003 at D0; mark SAF-008 and SAF-009 superseded by them (their text is retained for the content-tier PII clause of SAF-008 and the content-free schema of SAF-009, which TRU-002 and TRU-003 cite).

## Cross-cutting findings

1. **A rung is an economic tier, not a security boundary.** FND-002's rung-closed contract and RTG-008's leak contract both bind the gateway to a rung. A rung has members, and a member is an endpoint with a provider, a host, a trust zone and a geography. Every SAF property that mentions "local" or "in-region" is a property of the endpoint, so the object the gates tighten must be the set of endpoints. TRU-002 makes that the monotone object and FND-002 and RTG-008 are amended to cite it.
2. **Identity precedes classification.** A signed manifest is only as strong as its lookup key. SAF-008 keyed on a working directory and a remote read from the system prompt, which the harness composes from files the developer controls. TRU-001 moves the key to an assertion from a trusted launcher (the process that starts the harness and knows the checkout from SCM inventory), corroborated by a content fingerprint, and makes unknown identity local-only rather than default-class.
3. **The audit trail must be anchored outside the developer's machine and outside the developer's keys.** SAF-009's hash chain detects edits only for an auditor who holds checkpoints that the local process could not have forged. TRU-003 separates the checkpoint key from every other key, requires automatic checkpoints and off-device acknowledgements, and refuses development keys unless a development flag is set.
4. **The egress answer must be built from receipts.** "Did this lineage's content leave the machine?" was answered from the destination rung name. TRU-002's served-deployment receipt (provider, api_base host, geo, trust zone, as observed on the response or asserted by the gateway) is the only admissible evidence for that answer, and a local deployment that is not loopback is a configuration error, not a local deployment.
5. **Harness egress outside ADRL remains a known exclusion** (SAF-008 attack 6, SAF-009 clause 4) and is unchanged by this bucket; it belongs to OPS device-level policy.

## Sources consulted

- ADRL external implementation review, 2026-09-03 (findings P0-1 to P0-3, P1-5, P2-8), verified against `adrl-core` on 2026-09-03.
- Model Context Protocol, "Tools" (specification 2025-06-18): clients must treat tool annotations as untrusted unless the server is trusted - https://modelcontextprotocol.io/specification/2025-06-18/server/tools (cited by the 2026-09-03 external review; not independently fetched)
- Debenedetti et al., "Defeating Prompt Injections by Design" (CaMeL, arXiv 2503.18813): trusted control flow separated from untrusted data, capabilities enforced outside the model - https://arxiv.org/abs/2503.18813 (cited by the 2026-09-03 external review; not independently fetched)
- "Bounded Agents" (arXiv 2608.15888): monotone delegated authority and budgets - https://arxiv.org/abs/2608.15888 (cited by the 2026-09-03 external review; not independently fetched; single-author preprint, not a sole foundation)
- Crosby, Wallach, "Efficient Data Structures for Tamper-Evident Logging" (USENIX Security 2009) - https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident (fetched in the 2026-09-02 review)
- AWS, "Route model inference requests across AWS Regions with cross-Region inference" (Bedrock) - https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html (fetched in the 2026-09-02 review)
- Microsoft Learn, "Learn about sensitivity labels" (Purview) - https://learn.microsoft.com/en-us/purview/sensitivity-labels (fetched in the 2026-09-02 review)
- Anthropic, "Gateway protocol reference" (Claude Code docs) - https://code.claude.com/docs/en/llm-gateway-protocol (fetched in the 2026-09-02 review)
- LiteLLM, "Fallbacks (Provider Failover)" - https://docs.litellm.ai/docs/proxy/reliability (fetched in the 2026-09-02 review)
