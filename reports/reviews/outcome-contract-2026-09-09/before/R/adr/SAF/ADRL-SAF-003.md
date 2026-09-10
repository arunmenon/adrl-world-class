# ADRL-SAF-003 — Secret detection per request, precision-measured

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow conditional on publishing the shadow precision measurement; if no per-detector precision figure exists from real traffic, D2 |
| Review verdict | AMEND |
| Tenets | 2, 8 |
| Related decisions | SAF-001, SAF-002, SEM-001, SEM-003, MEM-005, MEM-007, FND-002, FND-004 |
| Open questions | Q5 |

## Decision

Secret detection runs on the new content of every request before that request is forwarded, using a detector set whose per-detector precision is measured on representative the company traffic and published, and for a secret-bearing lineage suppresses prompt-derived embeddings, instruction hashes, and any stored feature that could reconstruct or locate the secret (file paths, line spans, tool arguments).

1. *New content* means blocks not already scanned in this lineage (the latest `tool_result`s, the latest user text, new system reminders, subagent delegation text); previously scanned prefix is not re-scanned. Every content type the Messages API accepts is in scope — text, image, PDF/document blocks and tool inputs — with unsupported types treated as unscanned (SAF-001 sub-clause 3).
2. The detector set is tiered: *high-confidence* detectors (provider-specific formats, private-key headers, verified-format tokens) pin automatically; *generic* detectors (entropy, generic-password patterns) only pin when corroborated by a second signal (file path, variable name, second detector) and otherwise log a shadow finding. Tier membership is decided by measured precision, not by tool default.
3. Suppression is asymmetric: a lineage that is pinned loses embeddings and hashes for the *whole* lineage from that moment, including retroactive deletion of any embedding stored earlier in the same lineage.
4. Scanner unavailability follows FND-004 as amended (fail-closed on pinned lineages, `unscanned` marker otherwise).

## Context and rationale

Detect before deciding, and don't leak through the metadata. Scanning happens before routing. For a secret-bearing turn ADRL suppresses derived artefacts — embeddings and instruction hashes — because a vector built from your prompt is still your prompt, statistically. The consequence is lost training signal on exactly the sessions we understand least.

The amendment moves the scan from "the turn" to "the new content of every request", because tool results are where secrets arrive; it tiers the detectors by measured precision, because the literature shows a 3× spread in precision between tools on the same benchmark and the register's own analysis says precision is the binding constraint; and it widens suppression to the features that *locate* a secret, because a file path like `services/payments/keys/prod-signing.pem` in a features table is a finding in itself. The embedding-inversion evidence is stronger than the original rationale claims: Vec2Text recovers 92% of 32-token inputs exactly from state-of-the-art embeddings, the result reproduces, and the reproduction shows password-like strings with no semantics are recoverable too — so suppressing embeddings for secret-bearing content is not caution, it is the minimum.

## Adversarial review (2026-09-02)

### Steelman
Scanning before routing is the only ordering under which the scanner's verdict can affect where the content goes; scanning after would be a log, not a gate. Suppressing derived artefacts closes the side channel that most privacy designs forget, and the embedding-inversion results justify it directly. Marking the decision D3 with the honest note that precision, not recall, is the binding constraint shows the team understands the failure mode that would kill adoption.

### Attacks
1. **The scan is on the wrong message.** "Before routing" plus "routing per turn" means the scanner sees the developer's typed instruction and not the fifteen tool results that follow. In a coding session the credential is in the file the model reads or the command output it gets back, almost never in the instruction. Per-turn scanning has near-zero recall on the real ingress.
2. **Precision numbers are worse than the register implies, and unmeasured here.** On a labelled benchmark, GitHub's scanner reached 75% precision, Gitleaks 46%, a commercial tool 25%; recall ranged 52–88%. At session scope with a 46%-precision detector, more than half of pins are false. The register says precision is the binding constraint but reports no measured figure on the company traffic, so the D3 claim rests on an unquantified property.
3. **Generic detectors are where both value and noise live.** GitGuardian reports generic secrets were 67% of secrets detected in 2022, and GitHub's push protection deliberately limits itself to high-confidence provider patterns to avoid false positives — leaving generic secrets to fall through. ADRL must pick a point on that curve *per detector* and say so; a single "detector set" hides the choice.
4. **Suppressing embeddings and hashes is necessary, not sufficient.** MEM stores features (`router/features.py`) and telemetry: token counts, tool names, file paths, possibly tool arguments. A path or a `grep` argument can identify the secret's location and sometimes its shape. The suppression list should be defined by "can this reconstruct or locate the secret", not by naming two artefact types.
5. **Retroactivity.** A session runs for an hour unpinned, embeddings are written for each turn, then a secret appears in turn 40. The transcript prefix that was embedded earlier is the same prefix that is now in a pinned lineage. Suppression "for a secret-bearing turn" leaves 39 embeddings of the pinned transcript's prefix in the index. Vec2Text-class inversion on those is exactly the threat the decision names.
6. **Two scanners, two rulesets.** LiteLLM Enterprise runs `detect-secrets` in `pre_call` with 100+ plugins and *redacts*. If the enterprise gateway enables it, a request ADRL forwarded unpinned may be redacted by the gateway (fine) or a request ADRL pinned may have been un-flagged by the gateway's rules (divergence, invisible). Q7 needs a ruleset reconciliation (FND-002 sub-clause 3).
7. **Non-text blocks.** The Messages API and `count_tokens` accept images and PDFs. A screenshot of a config file or a PDF runbook with an API key passes a text-only scanner. The decision should declare these unscanned (and therefore, per SAF-001, unable to widen the permitted set) rather than silently treat them as clean.

### Evidence
- Basak et al., "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (ESEM 2023, arXiv 2307.00714) — nine tools on one benchmark: precision 75/46/25%, recall 88/67/52%; false positives from "generic regular expressions and ineffective entropy calculation"; bears on attacks 2, 3 — https://arxiv.org/abs/2307.00714
- Meli, McNiece, Reaves, "How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories" (NDSS 2019) — conservative detection restricted to private-key files and 11 high-impact platforms with distinctive formats, with manual and automatic evaluation for accuracy; over 100,000 repositories affected; precedent for a high-confidence tier; bears on attack 3 — https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/
- GitGuardian, "GitHub Push Protection: Benefits and Key Limitations" (blog) — generic secrets were 67% of detections in 2022; push protection covers a limited high-confidence pattern set by design; bears on attack 3 — https://blog.gitguardian.com/github-push-protection-enhancing-open-source-security-with-limitations-to-consider/
- Morris, Kuleshov, Shmatikov, Rush, "Text Embeddings Reveal (Almost) As Much As Text" (EMNLP 2023, arXiv 2310.06816) — Vec2Text recovers 92% of 32-token inputs exactly; recovers full names from clinical-note embeddings; supports the suppression clause and attack 5 — https://arxiv.org/abs/2310.06816
- "Rethinking the Privacy of Text Embeddings: A Reproducibility Study" (arXiv 2507.07700, 2025) — results replicate in and out of domain; quantisation and Gaussian noise mitigate; "even password-like sequences that lack clear semantics" are reconstructable; bears on attack 5 — https://arxiv.org/abs/2507.07700
- LiteLLM, "Secret Detection/Redaction (Enterprise-only)" — `detect-secrets`, `pre_call`, redaction, configurable plugin set; bears on attack 6 — https://docs.litellm.ai/docs/proxy/guardrails/secret_detection
- Anthropic, "Token counting" (Claude Platform docs) — images and PDFs are accepted inputs; bears on attack 7 — https://platform.claude.com/docs/en/build-with-claude/token-counting
- OWASP, "Top 10 for LLM Applications 2025" (PDF; listing confirmed via promptfoo summary) — LLM02 Sensitive Information Disclosure and LLM08 Vector and Embedding Weaknesses are named categories; frames the decision's two halves — https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf

### Verdict
**AMEND.** Attack 1 is the finding that matters: the scanner is pointed at the instruction, and the secret is in the tool result. Attacks 2 and 3 convert "precision is the binding constraint" from a remark into a design requirement (tiered detectors, measured precision, published). Attacks 4 and 5 widen suppression to what the threat model actually requires and make it retroactive. Attack 6 is handled in FND-002. Attack 7 adds an honest "unscanned" declaration. The decision's ordering and its suppression instinct are both correct and are strengthened, not replaced.

## Amendments applied

- Replaced "occurs before routing" with "runs on the new content of every request before that request is forwarded".
- Added the measured-and-published per-detector precision requirement.
- Widened suppression from "embeddings and identifiers" to "embeddings, instruction hashes, and any stored feature that could reconstruct or locate the secret".
- Added sub-clauses 1 (new-content scope and content types), 2 (tiered detectors by measured precision), 3 (retroactive suppression across the lineage), 4 (unavailability semantics).

## Follow-ups

- [ ] Implement incremental scanning of new blocks per request in the gate stage; p99 latency budget on continuations.
- [ ] Build a company-representative labelled corpus (real tool outputs, test fixtures, config files, payments code) and publish per-detector precision/recall; assign tiers from the results; re-run quarterly.
- [ ] Golden tests: AWS key in `tool_result` (auto-pin); high-entropy string in a test fixture with no corroboration (shadow finding, no pin); base64-encoded key; key split across two reads; PEM header in a PDF block (unscanned marker).
- [ ] Retroactive suppression: on pin, delete this lineage's embeddings from `router-memory.db` and the NumPy index (MEM-007 rebuild path); fault test that the deletion survives a crash mid-delete.
- [ ] Audit `router/features.py` and `telemetry.py` for locating features (paths, tool args); add them to the suppression list for pinned lineages.
- [ ] Ruleset diff against the gateway's `detect_secrets_config` (FND-002 follow-up).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: per-request scan of new content; tiered, precision-measured detectors; suppression widened and retroactive | "Secret detection occurs before routing and suppresses prompt-derived embeddings and identifiers." |
