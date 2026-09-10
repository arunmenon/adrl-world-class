# SAF — Safety, Privacy, Hard Constraints

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
were removed. The single supported OOM transformation is separated from unsafe control drift; no general sandbox qualification follows.
The 812-test runtime baseline is reused after verifying 306 hashes. Eight ADRs preserve prior
text and all grades; full W3 remains open.


**W3.2b2d2 research, 2026-09-08:** [launch identity gate](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md).
Pinned source explains the observed false/null unsupported OOM-control transformation. A narrowly scoped capability-specific comparison must pass before start; arbitrary configuration drift remains a refusal. No active sandbox qualification.
The unchanged 812-test baseline is reused with 306 verified hashes. Eight ADRs preserve prior text and grades; full W3 stays open.


**W3.2b2d1 update, 2026-09-08:** [stopped ownership](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md).
An explicitly selected local engine prepares a pinned synthetic image with bounded inspected controls. No container is started by the new primitive. This adds no untrusted-repository sandbox or runtime containment qualification.
All 812 tests and eleven checks pass. Seven owning ADRs preserve prior wording, status and maturity; full W3 remains open.


**W3.2b2c research, 2026-09-08:** [writer-boundary observations](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md).
The constrained PID-namespace fixture suppressed a detached late writer on init exit/container kill. Explicit seccomp and no host mounts were part of the tested configuration; complete isolation and real-task qualification remain open.
Six synthetic observations are separate from the unchanged 759-test runtime baseline. No status, maturity or release promotion.


**W3.2b2b2 update, 2026-09-08:** [process coordination](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md).
Supervised disposable fixture execution now keeps a permanent block because group cleanup cannot establish all-writer quiescence. This does not qualify a sandbox, safe workspace release or real task payload capture.
All 759 tests and eleven checks pass. Prior status/maturity fields remain unchanged; full W3 remains open.


**W3.2b1 update, 2026-09-08:** [owned process groups](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md).
Process-group cleanup is tested; a detached writer survives. Sandbox isolation and an all-writer boundary are not established.
All 669 tests and eleven checks pass. No architectural-status or maturity promotion;
full W3 and exact task-close attribution remain open.

**W3.1 update, 2026-09-08:** [retained operator captures](../../reports/adrl-w3-1-operator-captures-2026-09-08.md)
now preserve encrypted capture-time output through an internal API. All 593 tests and eleven
checks pass. Exact task-close attribution, active-copy erasure/crash recovery and verifier/CLI
integration remain later W3 work. No maturity grade or architectural status is promoted.

**Latest offline improvement evidence, 2026-09-07:** [SAF-007](ADRL-SAF-007.md) record
the applied verifier-comparison workflow and its limits. The current and proposed verifiers
classified 4/7 and 7/7 curated examples correctly; 549 implementation tests pass. These are
visible variants of one task family, with no automatic promotion or learning admission.
See the [report](../../reports/adrl-improvement-experiment-2026-09-07.md).

**Current session verification update, 2026-09-07:** [SAF-007](ADRL-SAF-007.md) record
API preview 4, independent encrypted session receipts and 532 passing tests. Two verifier jobs
each passed eight tests on the same prior pilot task; no general graduation or learning admission
follows. See the [report](../../reports/adrl-session-verification-2026-09-07.md). Earlier notes
below preserve their original scope.

**Core question:** What is forbidden or infeasible?
**Owns / does not own:** Owns the non-negotiable gates, secret handling, feasibility, blocking and protected resources. Does not own quality optimisation inside the allowed set.

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-SAF-001 | Hard gates first, on every request | AMEND | D2 → D2 | Ordering is right; scope is per-turn in practice while secrets arrive per-request in tool results; FND-004's fallback could override; monotonicity unstated |
| ADRL-SAF-002 | One-way pin, durable, lineage-scoped, audited release | AMEND | D2 → D1 | Pin state is a single-process dict (not durable) and does not cover `count_tokens`, utility or forked-subagent traffic; Q5 answered: keep session scope, add reason-coded audited human release (push-protection / Purview precedent) |
| ADRL-SAF-003 | Secret detection per request, precision-measured | AMEND | D3 → D3 conditional on published precision, else D2 | Scanner points at the typed instruction, not the tool results; literature shows 25–75% precision across tools; detectors must be tiered by measured precision; suppression must cover locating features and be retroactive |
| ADRL-SAF-004 | Pinned sessions fail loudly, in the harness's dialect | AMEND | D2 → D2 | Gateway fallback groups can reach cloud without ADRL; "surfaced to the user" needs a harness-recognisable, non-retried error contract; intra-local escalation omitted |
| ADRL-SAF-005 | Block, and make the block recoverable | AMEND | D2 → D2 | A block the harness does not recognise is a dead end; compaction deadlock for any local rung below the harness's ≥100k auto-compact floor; must be caught at configuration time |
| ADRL-SAF-006 | Infeasible rungs removed before optimisation | APPROVE | D2 → D2 | Correct and load-bearing; estimator precision (tokenizer, output/thinking budget, gateway-owned health) recorded as follow-ups |
| ADRL-SAF-007 | Verification runs sandboxed, then diffed | REJECT | D2 → D0 (control) / D1 (check) | Text promises a constraint; code performs a post-hoc diff; verifier has unrestricted network egress and writable home; replaced by OS-enforced sandbox (harness runtime, strict mode), snapshot execution, command allow-list |
| ADRL-SAF-008 | Repository and data-class gate | PROPOSED (new) | — → D0 | Missing gate: repository identity (PCI scope, residency, PII class) sets a rung ceiling before any content scan; residency enforced via geographic inference profiles; PII as a distinct tier |
| ADRL-SAF-009 | Egress ledger and gate-audit integrity | PROPOSED (new) | — → D0 | "Did this code ever leave the machine?" is not currently answerable; write-ahead, content-free, hash-chained egress ledger outside the fail-safe MEM facade |

Tally (existing seven): 1 APPROVE, 5 AMEND, 1 REJECT. Two new decisions proposed.

## Cross-cutting findings

1. **The gates guard the wrong message.** The register binds secret detection to "before routing" and routing to "once per user turn". Together they scan the developer's typed sentence and skip the fifteen `tool_result` continuations that actually carry `.env` files, command output and fixtures — the dominant ingress for secrets in coding-agent traffic. SAF-001 and SAF-003 are amended to run on the new content of every request; FND-003 and SEM-001 carry the matching changes. This is the most important finding in the bucket and it is a wording defect, not a design defect: nothing in the architecture prevents per-request gating, and SEM-003's "no fresh *difficulty* decision" was already precise.

2. **The pin has holes on three sides and is not durable.** (a) `count_tokens` bodies carry the full prompt and are passed through "unchanged"; (b) utility calls carry the user text and, for compaction, the whole transcript; (c) forked subagents carry the entire parent conversation and the SEM-006 interim passes them through. (d) Pin state is a Python dict: a proxy restart unpins every live session while the harness keeps sending. SAF-002 is amended for coverage and durability and its maturity lowered to D1; the SEM amendments supply the content-bearing flag and lineage keys.

3. **The escape hatch overrides the gate.** FND-004's blanket fail-open would send a pinned session to the cloud on a scanner exception. FND-004 is rejected and replaced with fail-open for unpinned sessions only, fail-closed for pinned; SAF-001 names the fallback path as something that cannot override a gate.

4. **Precision is the binding constraint and it is unmeasured.** The register says so; the literature quantifies it (25–75% precision across tools on one benchmark, 46% for the tool with the best recall; generic secrets were two-thirds of detections in one vendor's 2022 data while the most widely deployed push-protection deliberately covers only high-confidence patterns). SAF-003 now requires tiered detectors with per-detector precision measured on company-representative traffic and published. SAF-002's audited release with reason codes is the feedback loop that makes that measurement possible from live use.

5. **Q5 is answered, not dodged.** Session (transcript) scope is forced: once a secret is in the context it is in every subsequent request, and the influence-based relabelling that mitigates label creep in the IFC literature requires regenerating outputs from reduced contexts, which a coding harness's transcript does not allow. The relief valve is therefore human, audited, reason-coded and per-finding — exactly what GitHub push protection and Microsoft Purview do for the same trade-off. "One-way" is preserved for every automated actor.

6. **The verifier is the largest unmitigated egress path.** SAF-007's post-hoc protected-path check does not constrain network access or writes outside the repository. A test suite (or a `conftest.py` the model just wrote) can exfiltrate the working tree. The replacement adopts the harness's own OS-enforced sandbox in strict mode, which Claude Code documents in detail including the self-widening-write failure the original missed.

7. **Blocking must speak the harness's language.** Anthropic documents that Claude Code auto-compacts only when it recognises a too-long error in the vendor's wording (or a stable `capability_rejected:` token) and that its auto-compact window is clamped to ≥100k tokens. SAF-004/005 are amended so blocks are recoverable and so a local rung too small to hold the compaction request is rejected at configuration time — otherwise every long pinned session deadlocks.

8. **Two gates are missing.** Nothing in the register reacts to *where the code lives* (PCI scope, residency, PII class), which is known before the first prompt with lookup-table precision; and nothing makes the register's central promise ("did this code ever leave the machine?") answerable from evidence, because the routing ledger is behind a fail-safe facade that may be absent. SAF-008 and SAF-009 are proposed at D0 with concrete D1 exits.

9. **Adversarial evidence is still zero.** Every SAF decision remains "tested, not attacked". Each amended file lists an adversarial suite (encoded secrets, split reads, non-text blocks, subagent delegation text, gateway fallback configs, proxy SIGKILL, sandbox egress) as its first follow-up; none of the maturity recommendations above should rise until those run.

## Sources consulted

- Basak, Cox, Reaves, Williams, "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (ESEM 2023, arXiv 2307.00714) — https://arxiv.org/abs/2307.00714
- Meli, McNiece, Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories" (NDSS 2019) — https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/
- Morris, Kuleshov, Shmatikov, Rush, "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023, arXiv 2310.06816) — https://arxiv.org/abs/2310.06816
- "Rethinking the Privacy of Text Embeddings: A Reproducibility Study of 'Text Embeddings Reveal (Almost) As Much As Text'" (arXiv 2507.07700, 2025) — https://arxiv.org/abs/2507.07700
- "Permissive Information-Flow Analysis for Large Language Models" (arXiv 2410.03055, 2024) — https://arxiv.org/html/2410.03055
- Costa, Köpf et al., "Securing AI Agents with Information-Flow Control" (arXiv 2505.23643, 2025) — https://arxiv.org/abs/2505.23643
- Wikipedia, "LOMAC" (low-water-mark mandatory access control) — https://en.wikipedia.org/wiki/LOMAC
- Crosby, Wallach, "Efficient Data Structures for Tamper-Evident Logging" (USENIX Security 2009) — https://www.usenix.org/conference/usenixsecurity09/technical-sessions/presentation/efficient-data-structures-tamper-evident
- GitHub Docs, "About push protection" — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
- GitGuardian, "GitHub Push Protection: Benefits and Key Limitations Explained" — https://blog.gitguardian.com/github-push-protection-enhancing-open-source-security-with-limitations-to-consider/
- Microsoft Learn, "Learn about sensitivity labels" (Microsoft Purview) — https://learn.microsoft.com/en-us/purview/sensitivity-labels
- AWS, "Route model inference requests across AWS Regions with cross-Region inference" (Bedrock) — https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- OWASP, "Top 10 for LLM Applications 2025" (PDF) — https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf ; listing confirmed via Promptfoo, "OWASP LLM Top 10" — https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/
- Anthropic, "Configure the sandboxed Bash tool" (Claude Code docs) — https://code.claude.com/docs/en/sandboxing
- Anthropic, "Create custom subagents" (Claude Code docs) — https://code.claude.com/docs/en/sub-agents
- Anthropic, "Gateway protocol reference" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-protocol
- Anthropic, "Connect Claude Code to an LLM gateway" (Claude Code docs) — https://code.claude.com/docs/en/llm-gateway-connect
- Anthropic, "Token counting" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/token-counting
- Anthropic, "Prompt caching" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude Platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- LiteLLM, "Fallbacks (Provider Failover)" — https://docs.litellm.ai/docs/proxy/reliability
- LiteLLM, "Secret Detection/Redaction (Enterprise-only)" — https://docs.litellm.ai/docs/proxy/guardrails/secret_detection
- LiteLLM, "PII, PHI Masking - Presidio" (title from search) — https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2
- AuthZed, "Understanding 'Failed Open' and 'Fail Closed' in Software Engineering" — https://authzed.com/blog/fail-open
- Northflank, "How to sandbox AI agents in 2026: MicroVMs, gVisor & isolation strategies" (title from search) — https://northflank.com/blog/how-to-sandbox-ai-agents
