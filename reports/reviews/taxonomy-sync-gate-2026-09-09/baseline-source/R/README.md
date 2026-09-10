# ADRL Architecture Decision Records — reviewed and amended

**W3.2 latest, 2026-09-08:** [original receipts and pinned-engine lifecycle validated](reports/adrl-w3-transport-receipts-2026-09-08.md).
Execution v2 separates preparation from active I/O; 895 tests/all eleven checks pass with zero
skips and 316 stable inputs. All thirteen fixtures/image are absent. Bounded d2 closes;
[active-copy custody](reports/waves/w3-active-copy-custody.md) is next. Full W3 and all grades stay open/unchanged.


**W3.2 runtime prototype, 2026-09-08:** [one-shot isolated fixture execution](reports/adrl-w3-isolated-launch-2026-09-08.md)
adds durable launch denial, authenticated lifecycle and recovery. Final offline validation:
861 passed, eight engine cases skipped, all eleven checks, 315 stable inputs. Current workflow
engine qualification stays open after a lost create reply; all eight test fixtures and the image
are gone. Schema 12/API preview 4; no status/maturity promotion.


**W3.2 identity research, 2026-09-08:** [startup mismatch resolved](reports/adrl-w3-execution-identity-2026-09-08.md).
101 offline research cases and seven new bounded engine observations passed. All seven
containers and one image were removed; no runtime launch was added. Next: one-shot execution
with durable denial, sealing and recovery. The unchanged 812-test/eleven-check runtime baseline
is reused with 306 verified hashes. Eight ADRs updated; no status/maturity promotion.


**W3.2b2d2 research, 2026-09-08:** [launch-contract progress](reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md)
found a startup identity mismatch: the captured OomKillDisable field changes from false to null
on the selected engine. Two bounded runs failed, zero of six cases are accepted, and both
fixtures/image were removed. Active launch remains unavailable. The runtime is unchanged at
its verified 812-test/eleven-check baseline with all 306 declared hashes checked; no promotion.


**W3.2b2d1 implementation, 2026-09-08:** [stopped resource ownership](reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md)
adds create/bind/inspect/non-force-remove with authenticated recovery and permanent workspace
blocking. All 812 tests and eleven checks pass; 306 declared hashes are stable. Schema 11 has
325 checked fields and API preview 4 is unchanged. Seven ADRs record tested scope, no grade
promotion. Launch, full writer stopping, capture binding and plaintext erasure remain open.


Latest research, 8 September 2026: [W3.2b2c writer boundary](reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md)
identifies an isolated-container candidate using the existing local engine. Six bounded
observations show both its useful lifetime boundary and remaining client-death/path/descriptor
limits. Runtime remains at the verified 759-test baseline; no backend or release is claimed.
Follow the [journey](reports/adrl-implementation-journey.md) for the next ownership/recovery slice.


Latest slice, 8 September 2026: [W3.2b2b2 process coordination](reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md)
connects attempts to owned fixture execution, observes erasure/expiry/closure and keeps a durable
workspace block across interruption and restart. All 759 tests and eleven checks pass. A stronger
writer boundary must precede safe release and real task capture. Follow the
[journey](reports/adrl-implementation-journey.md).


Latest slice, 8 September 2026: [W3.2b2b1 key revocation](reports/adrl-w3-2b2b1-key-revocation-2026-09-08.md)
fixes restored-key access after a failed erasure audit. Revocation now precedes key mutation;
724 tests and eleven checks pass. Process/erasure/release coordination is still next.
Follow the [journey](reports/adrl-implementation-journey.md) for this course correction.

Latest slice, 8 September 2026: [W3.2b2a terminal capacity](reports/adrl-w3-2b2a-terminal-capacity-2026-09-08.md)
reserves space for cancellation/interruption when a new journal attempt starts. All 697 tests
and eleven checks pass. Erasure/process/release coordination remains next; follow the
[journey](reports/adrl-implementation-journey.md).

Latest slice, 8 September 2026: [W3.2b1 process ownership](reports/adrl-w3-2b1-process-ownership-2026-09-08.md)
adds tested command-group cleanup, with 669 passing tests and eleven checks. Detached and
unrelated writers remain outside its scope; exact task closure is still gated. Follow the
[journey](reports/adrl-implementation-journey.md) for the next admission/recovery work.

Latest slice, 8 September 2026: [W3.2a attempt journal](reports/adrl-w3-2a-attempt-journal-2026-09-08.md)
is internally implemented with 631 passing tests. It records intent/interruption; the process
supervisor and exact task-close attribution remain pending. Follow the [journey](reports/adrl-implementation-journey.md).

Latest slice, 8 September 2026: [W3.1 retained operator captures](reports/adrl-w3-1-operator-captures-2026-09-08.md)
is implemented internally and passes 593 tests. Exact task-close attribution and real task
capture remain later W3 work. The [journey](reports/adrl-implementation-journey.md) tracks continuation.

Execution started on 7 September 2026. Follow the [running implementation journey](reports/adrl-implementation-journey.md)
for the current slice, evidence, limits and next action. W0 has a fresh 556-test engineering baseline;
the plan and earlier reports below retain their original dates and scope.

This repository holds the ADRL (Adaptive Routing Layer) decision register as **architecture decision records, one file per decision, organised by bucket**. ADRL's product direction is a shared policy, routing and evidence engine that integrates with coding harnesses through adapters, protocol profiles and a separate product API. The first implementation boundary supports Anthropic Messages with Claude Code correlation; Codex remains outside the supported traffic scope until a Responses profile passes admission. ADRL chooses the permitted capability rung while the gateway chooses an endpoint within its constraints.

The initial capture contained 49 Accepted decisions from seven of the original taxonomy's nine buckets. Those decisions were reviewed on 2026-09-02, with amended and replacement text written in place and prior wording retained in their changelogs. Six new decisions were proposed that day. The 2026-09-03 addendum added TRU, first captures of EVL and OPS, SEM-007, CAS-009 and six proposed amendments. The current register contains **77 decisions across ten bucket directories**, including proposals awaiting disposition.

## Forward implementation plan, proposed 2026-09-07

Start with the [long-horizon implementation roadmap](reports/adrl-implementation-roadmap-2026-09-07.md):
reliable task evidence, two-harness reuse, controlled execution, routing comparisons and a
supported local product. Learning, automated proposals, managed teams and RSI follow only
when their evidence gates justify them. Every wave has scope, guardrails, exit evidence,
recovery and owning ADRs. The [execution packet](reports/adrl-wave-execution-template.md)
turns an approved wave into bounded work. This planning pass launches no implementation.

## Current implementation record — 2026-09-07

The [first offline improvement experiment](reports/adrl-improvement-experiment-2026-09-07.md)
is now implemented, with **549 passing tests** and all required checks passing. ADRL compares
reviewed verifier proposals against a baseline, preserves encrypted trial evidence, and returns
a recommendation for review. The current verifier classified **4 of 7 curated examples**
correctly; the candidate classified **7 of 7**, with both repetitions agreeing.

These are visible examples from one task family, designed alongside the candidate. They do
not establish broad verifier accuracy, routing benefits or recursive self-improvement. Nothing
was automatically adopted or admitted to learning. The [earlier session-verification path](reports/adrl-session-verification-2026-09-07.md)
remains available; the public API is still preview 4. Exact task-close attribution, fresh tasks,
a second harness and Responses remain pending. Twelve owning ADRs record the applied scope;
prior reports and architectural statuses are preserved.

Implementation work includes updating its owning ADRs, this register's index and change history
before completion. The repository's [maintenance instructions](AGENTS.md) make that workflow explicit.

## Start here

| If you want… | Read |
|---|---|
| The findings and the answers to the seven Open Questions | [`REVIEW-LOG.md`](REVIEW-LOG.md) |
| Every decision, verdict and maturity change on one page | [`INDEX.md`](INDEX.md) |
| What the latest implementation changed in the decisions | [First measured improvement and maturity](reports/adrl-improvement-experiment-2026-09-07.md) |
| What to run next and how tests can change the design | [Course-correction plan](reports/adrl-course-correction-plan-2026-09-07.md) |
| One bucket's decisions, cross-cutting findings and sources | `adr/<BUCKET>/README.md` |
| A single decision in full | `adr/<BUCKET>/ADRL-<BUCKET>-<NNN>.md` |
| Every source cited, grouped by host | [`BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md) |
| The register text as it stood before the review | [`source/`](source/) |

## Layout

```
adr/
  FND/   System Boundary and Principles      ADRL-FND-001 … 005
  SEM/   Interaction Semantics                ADRL-SEM-001 … 006  (+007 proposed)
  SAF/   Safety, Privacy, Hard Constraints    ADRL-SAF-001 … 007  (+008, 009 proposed)
  RTG/   Routing Intelligence and Economics   ADRL-RTG-001 … 008  (+009 proposed)
  CAS/   Execution, Cascade, Recovery         ADRL-CAS-001 … 007  (+008, 009 proposed)
  MEM/   Memory, Evidence, Label Integrity    ADRL-MEM-001 … 009  (+010 proposed)
  LRN/   Learning and Adaptation              ADRL-LRN-001 … 007  (+008 proposed)
  TRU/   Trust, Residency and Egress        ADRL-TRU-001 … 003  (Proposed 2026-09-03)
  EVL/   Evaluation, Graduation, Rollout      ADRL-EVL-001 … 009  (Proposed 2026-09-03, first capture)
  OPS/   Platform, Runtime, Operations        ADRL-OPS-001 … 008  (Proposed 2026-09-03, first capture)
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
- **Verdicts.** APPROVE: text stands, attacks answered. AMEND: text changed in place. REJECT: original withdrawn, replacement written in place, status `Superseded 2026-09-02`. PROPOSED (new): a decision the bucket was found to be missing; architectural acceptance remains pending. Tested portions can have scoped evidence without accepting or graduating the full proposal.
- **IDs** are permanent. A rejected decision keeps its ID; the replacement lives under it and the changelog records the supersession.
- **Citations.** Every URL in an Evidence section was fetched or appeared in a search result with a matching title during the review; 25 load-bearing citations were re-fetched and checked line-by-line and the text corrected where it overstated a source. Two sources that could not be fetched are flagged as such in the files.

## How to respond

Comment inline on the decision file you care about. If you think a verdict is wrong, name the attack you believe was answered or the evidence you believe was misread. If you think an amendment violates a tenet, name the tenet. Proposed decisions (`Proposed` status) need an owner and a disposition — accepted, rejected with reason, or deferred — before they enter the canonical register.

## Provenance

Register text: Confluence, the internal architecture space, author Arun Menon, published 2026-08-27, reconstructed from photographs on 2026-09-02. Code-reality facts: Codex CLI walkthroughs of the `cc-local` repository and `routing/docs/architecture-code-map.md` (2026-09-02). The reviewers did not have the repository open; every code-reality claim is as reported in the context pack and should be re-checked by someone who does. See the last section of `REVIEW-LOG.md`.
