# ADRL Architecture Decision Records — reviewed and amended

This repository holds the ADRL (Adaptive Routing Layer) decision register as **architecture decision records, one file per decision, organised by bucket**, after an adversarial architecture review conducted on 2026-09-02. ADRL is a transparent control layer between a coding harness (Claude Code / Codex CLI) and the model gateway (LiteLLM); it chooses a capability rung — `local`, `cheap_cloud`, `frontier` — while the gateway chooses the endpoint.

The register was published on Confluence on 2026-08-27 with 49 Accepted decisions across nine buckets. Seven buckets (49 decisions) are captured here. Every decision was steel-manned, attacked, tested against the literature and vendor documentation, and given exactly one verdict. Amended and replacement text was **written in place**; the original sentence is preserved verbatim in every file's changelog. Six new decisions are proposed.

## Start here

| If you want… | Read |
|---|---|
| The findings and the answers to the seven Open Questions | [`REVIEW-LOG.md`](REVIEW-LOG.md) |
| Every decision, verdict and maturity change on one page | [`INDEX.md`](INDEX.md) |
| One bucket's decisions, cross-cutting findings and sources | `adr/<BUCKET>/README.md` |
| A single decision in full | `adr/<BUCKET>/ADRL-<BUCKET>-<NNN>.md` |
| Every source cited, grouped by host | [`BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md) |
| The register text as it stood before the review | [`source/`](source/) |

## Layout

```
adr/
  FND/   System Boundary and Principles      ADRL-FND-001 … 005
  SEM/   Interaction Semantics                ADRL-SEM-001 … 006
  SAF/   Safety, Privacy, Hard Constraints    ADRL-SAF-001 … 007  (+008, 009 proposed)
  RTG/   Routing Intelligence and Economics   ADRL-RTG-001 … 008  (+009 proposed)
  CAS/   Execution, Cascade, Recovery         ADRL-CAS-001 … 007  (+008 proposed)
  MEM/   Memory, Evidence, Label Integrity    ADRL-MEM-001 … 009  (+010 proposed)
  LRN/   Learning and Adaptation              ADRL-LRN-001 … 007  (+008 proposed)
  EVL/   (not captured — see source/)
  OPS/   (not captured — see source/)
source/  Register reconstruction the review worked from, plus the review instructions
```

Each bucket directory has a `README.md` with the bucket's core question, a verdict table, cross-cutting findings, and its bibliography.

## Anatomy of a decision file

```
# ADRL-XXX-NNN — short title
| Field | Value |                 Bucket · Status · Maturity (claimed, review recommends …)
                                  · Review verdict · Tenets · Related decisions · Open questions
## Decision                       The CURRENT text. Original if APPROVE; new text if AMEND/REJECT.
## Context and rationale          Plain-terms argument, updated to match the current text.
## Adversarial review (date)
   ### Steelman                   Strongest case for the decision as written.
   ### Attacks                    ≥3 numbered, system-specific attacks.
   ### Evidence                   Sources, one line each on what they show, with URLs.
   ### Verdict                    APPROVE / AMEND / REJECT with reasoning.
## Amendments applied             The concrete textual changes.
## Follow-ups                     Testable actions the amendment implies.
## Changelog                      Every prior text, verbatim.
```

## Conventions

- **Status** and **Maturity** are independent, as in the register. Status is whether the decision is agreed (Accepted / Proposed / Superseded). Maturity is how far it is proven (D0 Design · D1 Code · D2 Tested · D3 Shadow · D4 Pilot · D5 Graduated). The Maturity field carries the register's claim first and the review's recommendation second; the review does not itself change a claimed level.
- **Verdicts.** APPROVE: text stands, attacks answered. AMEND: text changed in place. REJECT: original withdrawn, replacement written in place, status `Superseded 2026-09-02`. PROPOSED (new): a decision the bucket was found to be missing; status `Proposed`, maturity D0.
- **IDs** are permanent. A rejected decision keeps its ID; the replacement lives under it and the changelog records the supersession.
- **Citations.** Every URL in an Evidence section was fetched or appeared in a search result with a matching title during the review; 25 load-bearing citations were re-fetched and checked line-by-line and the text corrected where it overstated a source. Two sources that could not be fetched are flagged as such in the files.

## How to respond

Comment inline on the decision file you care about. If you think a verdict is wrong, name the attack you believe was answered or the evidence you believe was misread. If you think an amendment violates a tenet, name the tenet. Proposed decisions (`Proposed` status) need an owner and a disposition — accepted, rejected with reason, or deferred — before they enter the canonical register.

## Provenance

Register text: Confluence, the internal architecture space, author Arun Menon, published 2026-08-27, reconstructed from photographs on 2026-09-02. Code-reality facts: Codex CLI walkthroughs of the `cc-local` repository and `routing/docs/architecture-code-map.md` (2026-09-02). The reviewers did not have the repository open; every code-reality claim is as reported in the context pack and should be re-checked by someone who does. See the last section of `REVIEW-LOG.md`.
