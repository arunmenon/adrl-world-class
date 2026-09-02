# Adversarial ADR review — agent instructions

You are one of three reviewers performing an adversarial architecture review of the ADRL (Adaptive Routing Layer) decision register. ADRL is a transparent proxy between coding harnesses (Claude Code / Codex CLI) and a model gateway (LiteLLM) at the company; it picks a capability rung (local / cheap_cloud / frontier). Read `/home/claude/adrl-src/01-overview-tenets-taxonomy.md` and `/home/claude/adrl-src/09-open-questions.md` first, then the register file(s) for your buckets.

## Your job, per decision

1. **Steelman** the decision in two or three sentences — the strongest case for it as written.
2. **Attack** it. At least three distinct, concrete attacks per decision. Attacks must be specific to this system (coding-agent traffic, tool loops, prompt caches, privacy pins, cross-provider handoff, SQLite ledger, etc.), not generic. Good attack sources: the decision is under-specified; it conflicts with another decision or a tenet; the literature shows a failure mode it does not address; the code reality contradicts the claimed maturity; it is unfalsifiable as written; it silently assumes something Phase 0 explicitly did not establish.
3. **Research.** Use WebSearch/WebFetch to find real papers, vendor docs, and engineering write-ups that bear on the decision — both supporting and contradicting. Aim for 2–5 concrete citations per decision, more for the load-bearing ones. Prefer arXiv papers, ACM/IEEE/USENIX venues, official vendor documentation (Anthropic, OpenAI, AWS Bedrock, LiteLLM, vLLM, Ollama, llama.cpp), and reputable engineering blogs. Record the URL and what it actually says — do not paraphrase a paper into saying something it does not. If you cannot find evidence for a claim, say so explicitly rather than inventing a citation.
4. **Verdict**: exactly one of
   - **APPROVE** — decision stands as written; attacks answered.
   - **AMEND** — decision stands in spirit but the text must change (tighten, add a clause, split, re-scope, or change maturity). Provide the full replacement decision text.
   - **REJECT** — decision should be withdrawn or replaced. Provide the replacement decision text and explain what supersedes it.
   Be willing to REJECT. A review in which everything is approved is a failed review. Equally, do not manufacture rejections — the verdict must follow from the attacks and evidence.
5. **Maturity check**: does the evidence in the pack support the claimed D-level? If not, say what level it should carry and why.
6. **Follow-ups**: concrete, testable actions (a golden test, a measurement, a missing gate, a new ADR) that the amendment implies.

## Output — one file per decision, in place

Write each decision to `/home/claude/adrl-review/adr/<BUCKET>/ADRL-<BUCKET>-<NNN>.md` using EXACTLY this structure (the top-level assembler depends on it):

```markdown
# ADRL-<BUCKET>-<NNN> — <short title, 3–8 words>

| Field | Value |
|---|---|
| Bucket | <CODE> — <Bucket name> |
| Status | Accepted · unchanged \| Accepted · amended 2026-09-02 \| Superseded 2026-09-02 (see replacement) |
| Maturity | <as claimed>, review recommends <same or different, with one-line reason> |
| Review verdict | APPROVE \| AMEND \| REJECT |
| Tenets | <numbers> |
| Related decisions | <IDs> |
| Open questions | <Qn, or —> |

## Decision

<The CURRENT decision text. If APPROVE this is the original text verbatim. If AMEND or REJECT this is the NEW text — write it in the same one-sentence register style as the originals, then optionally 1–3 numbered sub-clauses for the added precision.>

## Context and rationale

<Plain-terms rationale, rewritten to reflect the amended decision where relevant. Keep the original argument's voice; 1–3 paragraphs.>

## Adversarial review (2026-09-02)

### Steelman
<2–3 sentences>

### Attacks
1. **<attack title>.** <the attack, specific to this system>
2. ...
3. ...

### Evidence
- <Author/Org, "Title" (venue, year)> — <one sentence on what it shows and which attack it bears on> — <URL>
- ...

### Verdict
**<APPROVE|AMEND|REJECT>.** <Reasoning that connects the attacks and evidence to the verdict, 1–2 paragraphs. Say which attacks landed and which were answered.>

## Amendments applied

<Bulleted list of the concrete textual changes, or "None — decision stands as written.">

## Follow-ups

- [ ] <testable action>
- [ ] ...

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | <Approved unchanged \| Amended: <one line> \| Superseded: <one line>> | <ORIGINAL decision sentence, verbatim, in quotes — always fill this in, even for APPROVE> |
```

Also write `/home/claude/adrl-review/adr/<BUCKET>/README.md` for each bucket you own:

```markdown
# <CODE> — <Bucket name>

**Core question:** ...
**Owns / does not own:** ...

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|

## Cross-cutting findings
<Things that span several decisions in this bucket, conflicts with other buckets, missing decisions the bucket should have. If you think the bucket is missing an ADR, PROPOSE it here as ADRL-<CODE>-<next number> with status Proposed, and also write it as its own file with verdict "PROPOSED (new)".>

## Sources consulted
<Full bibliography for this bucket, deduplicated, with URLs.>
```

## Rules

- Do NOT invent citations. Every URL must be one you actually fetched or that appeared in a search result with a matching title. If a search returns nothing useful, say "no direct literature found; reasoning from first principles" in the Evidence section.
- Preserve every original decision sentence verbatim in the Changelog.
- Decision IDs are `ADRL-<BUCKET>-<NNN>` with three-digit numbers. Filenames match IDs exactly.
- Do not change maturity in the Maturity field's first clause; put the recommendation in the second clause.
- Be concrete about company-relevant risk where it is genuinely relevant (payments code, secrets, PCI scope, data residency), but do not pad.
- Work through every decision in your buckets. Do not skip any. Report back with: the list of files written, a verdict tally, and the three most important findings.
