# ADRL-SAF-008 — Repository and data-class gate (Proposed)

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Proposed 2026-09-02 (new, from adversarial review) |
| Maturity | D0 Design, review recommends D0 Design (nothing built; the register itself lists "data-residency constraints for specific repositories are not yet expressed as a gate") |
| Review verdict | PROPOSED (new) |
| Tenets | 2, 3 |
| Related decisions | SAF-001, SAF-002, SAF-003, SAF-004, FND-002, SEM-002, RTG-001 |
| Open questions | Q2, Q5 |

## Decision

A static repository and data-class gate, evaluated from the working directory's classification before any content is scanned, sets the maximum permitted rung and residency constraint for a lineage: restricted repositories (PCI-scope, payments core, HSM/key-management, regulated-data services) are local-only from the first request; residency-tagged repositories are limited to cloud rungs whose gateway deployments are pinned to an approved geography; and PII detection is a distinct detector tier from secrets, with its own pin semantics.

1. Classification source: a signed, versioned manifest (repository → class, residency, allowed rungs) owned by security, resolved from the harness's reported working directory / git remote at session start and re-resolved on any `cwd` change visible in the request (subagent `isolation: worktree`, `--add-dir`). Unknown repositories default to the organisation's default class, not to "unrestricted".
2. Residency is enforced through FND-002's rung-closed contract: a residency-tagged lineage may only be served by gateway deployments tagged with a matching geographic inference profile; global cross-region profiles are excluded for such lineages.
3. PII (customer names, PANs, account identifiers, addresses in logs or fixtures) is detected by a separate tier from secrets, because its precision/recall profile and its regulatory consequence differ; a PII finding pins to the *cloud-in-region or local* set rather than local-only, unless the repository class says otherwise.
4. The gate is evaluated before the content scanner (SAF-003) and its result is a ceiling that content scanning can only lower.

## Context and rationale

Seven gates in the register all react to *content* (secrets, context size, health) or to *policy* (pins, verification). None reacts to *where the code lives*. At the company that is the wrong order of operations: whether a repository is in PCI scope, whether its data must stay in a geography, and whether it handles cardholder or account data are known *before* the first byte of the first prompt, from the repository's identity alone. A content scanner with 46–75% precision is the wrong tool for a question that has a lookup-table answer. The register's own open-items list names the gap ("data-residency constraints for specific repositories are not yet expressed as a gate"), and Q2 asks for "categories never allowed on local regardless of accuracy" — the mirror question, categories never allowed on *cloud* regardless of scanner verdict, has the same answer and is this gate.

The precedents are mature. Microsoft Purview applies sensitivity labels to containers (sites, teams) as well as files, with labels persisting as metadata and downgrades requiring justification. GitHub push protection is configured per repository and organisation. AWS Bedrock distinguishes geographic cross-region inference profiles (processing stays within US/EU/APAC) from global profiles (any commercial region) and recommends geographic profiles "when you have data residency requirements". PII is separated from secrets because the tools differ (Presidio-class NER vs regex/entropy), the error profile differs, and the consequence differs (a leaked PAN is a PCI incident whether or not it is a "secret").

## Adversarial review (2026-09-02)

### Steelman
This gate is cheaper, more precise and earlier than any content scanner: a lookup on repository identity has effectively 100% precision for the repositories that matter most, costs nothing per request, and removes the register's dependence on scanner precision for the highest-consequence code. It also gives security a control they own (the manifest) without touching routing logic — exactly the FND-002 split applied to classification.

### Attacks (self-applied, as this is a proposal)
1. **Repository identity is spoofable from the harness side.** The working directory and git remote are reported by the harness (system prompt, CLAUDE.md context, `x-claude-code-*` headers do not carry them). A developer can clone a restricted repository into an unclassified path. Mitigation: classify on git remote *and* on content fingerprints (a small set of known-restricted file signatures) as corroboration; treat unknown as default-class, not unrestricted; and log every classification with its evidence for audit (SAF-009).
2. **Manifest drift.** New repositories appear daily; a stale manifest under-classifies. Mitigation: default class is conservative; manifest changes are signed and versioned; a weekly diff against the SCM inventory is a readiness gate.
3. **Coarse classification re-creates Q5 at repository scope.** A monorepo with one PCI directory pins every session in it. Mitigation: path-prefix classification within a repository, resolved from the files the session actually touches (the `Read`/`Edit` tool inputs are visible on the wire); the ceiling tightens when a restricted prefix is touched — monotone, like SAF-002.
4. **Residency enforcement depends on gateway tagging.** If gateway team's LiteLLM deployments are not tagged by region/profile, the gate has nothing to enforce against. Prerequisite for FND-002's shared rung config: every deployment carries `geo` and `profile` fields.
5. **PII detection precision is worse than secret detection.** NER-based PII detectors produce false positives on ordinary code (variable names that look like names, test fixtures). Sub-clause 3 therefore pins to "in-region cloud or local" rather than local-only, and the tier is measured separately (SAF-003 sub-clause 2's method).
6. **Harness egress outside the gateway.** Fast-mode checks and WebFetch domain-safety checks go to `api.anthropic.com` directly; telemetry too. A residency gate on the ADRL path does not cover them. Recorded as a limitation; device-level egress policy (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, sandbox `allowedDomains`) is the complementary control and belongs to OPS.

### Evidence
- ADRL evidence pack, `02-register-FND-SEM-SAF.md` — "Data-residency constraints for specific repositories are not yet expressed as a gate"; Q2 asks for categories never allowed on local regardless of accuracy.
- Microsoft Learn, "Learn about sensitivity labels" (Purview) — labels apply to files, emails, meetings and containers (sites/teams); persist as clear-text metadata with the content; downgrade requires justification; mandatory and default labelling; precedent for container-level classification and conservative defaults — https://learn.microsoft.com/en-us/purview/sensitivity-labels
- AWS, "Route model inference requests across AWS Regions with cross-Region inference" (Bedrock docs) — geographic profiles keep processing within US/EU/APAC; global profiles route to any commercial region; recommended geographic profiles for data-residency requirements; bears on sub-clause 2 — https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html
- GitHub Docs, "About push protection" — per-repository/organisation configuration of a blocking control with audited bypass; precedent for repository-scoped policy — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
- LiteLLM, "PII, PHI Masking - Presidio" (docs; title from search) — PII detection as a distinct guardrail class from secret detection at the gateway; bears on sub-clause 3 — https://docs.litellm.ai/docs/proxy/guardrails/pii_masking_v2
- Basak et al., arXiv 2307.00714 — content-scanner precision range (25–75%) motivates a lookup-table gate for the highest-consequence repositories — https://arxiv.org/abs/2307.00714
- Anthropic, "Gateway protocol reference" (Claude Code docs) — some harness traffic bypasses `ANTHROPIC_BASE_URL`; bears on attack 6 — https://code.claude.com/docs/en/llm-gateway-protocol

### Verdict
**PROPOSED (new).** The register invites the naming of a missing gate; this is the one with the highest company-specific leverage and the lowest implementation risk, because its core is a manifest lookup. Self-applied attacks 1–3 shape the design (corroboration, conservative default, path-prefix tightening); attack 4 is a prerequisite shared with FND-002; attacks 5 and 6 bound the claim. Recommended for acceptance at D0 with the follow-ups below as the D1 exit.

## Amendments applied

New decision; no prior text.

## Follow-ups

- [ ] Security to publish `repo-classification-v1.json` (repo → class, residency, allowed rungs, restricted path prefixes), signed and versioned; ADRL loads and verifies signature at start.
- [ ] Implement working-directory / git-remote resolution from the request (system prompt environment block, CLAUDE.md path, tool inputs); golden tests for clone-to-unclassified-path (default class applies) and monorepo restricted prefix (ceiling tightens on first touch).
- [ ] Extend the shared rung config (FND-002) with `geo` and `profile` per deployment; CI check that residency-tagged lineages have at least one feasible in-geography deployment per cloud rung.
- [ ] PII detector tier: evaluate Presidio-class detection on the SAF-003 corpus; publish precision; define pin semantics per class.
- [ ] Ledger: record classification source and evidence per lineage (feeds SAF-009).
- [ ] OPS: device-level egress baseline for Claude Code (`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, sandbox `allowedDomains`) documented as the complement to this gate.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-02 | Proposed (adversarial review) | — |
