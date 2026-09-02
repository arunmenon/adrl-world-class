# SAF — Safety, Privacy, Hard Constraints

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
