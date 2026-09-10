# Review ledger

`reports/reviews/` is the append-only ledger of independent reviews of ADRL. Schema `review-ledger-v1`. Its purpose is that a person or an agent can later parse every review across waves without reading prose: which checkpoint was reviewed, what inputs were frozen, what was found, what the implementer answered, what was rechecked, and what remains open.

## Layout

One folder per review, named `<slug>-<YYYY-MM-DD>`. A conforming folder contains:

| File | Written by | Mutability | Purpose |
|---|---|---|---|
| `packet.md` | coordinator | immutable after open | checkpoint, objective, scope, exclusions, baseline, hypotheses, acceptance conditions |
| `inputs.json` | coordinator | immutable | frozen-input manifest: every reviewed file with SHA-256, dirty and untracked scope, exclusions |
| `invocation.json` | coordinator | immutable | requested and observed model, session, tools, permission denials, coverage limits |
| `review.md` | reviewer | immutable | the original review text |
| `findings.md` | reviewer | immutable | findings with stable IDs, severity, confidence, evidence, acceptance criteria |
| `findings.json` | reviewer | immutable | the same findings, machine-readable: `{id, global_id, severity, kind, blocking, confidence, owning_adrs, title, appendix_refs}` |
| `dispositions.md` | reviewer | immutable | the initial disposition table, every row `unresolved` |
| `dispositions.jsonl` | implementer, reviewer, owner | append-only | one line per disposition change: `{ts, actor, finding_id, disposition, evidence, note}` |
| `status.json` | coordinator | replaceable; every change also appended to `LEDGER.jsonl` | `not-started`, `in-review`, `changes-requested`, `awaiting-recheck`, `reviewed-with-open-items`, `reviewed`, `unavailable` |
| `appendix/` | reviewer | immutable | inspection reports and machine-readable tables |
| `reconciliation/` | implementer | add-only (new files may be added, existing ones never edited) | implementer responses, rechecks, fix references |
| `manifest.json` | coordinator | replaced only when files are added; prior manifests kept as `manifest-<n>.json` | every file's SHA-256 and its mutability class |

Global finding IDs are `<folder>:<local id>`, for example `fable-retrospective-2026-09-08:RV-01`. Severity and original finding text never change; a reviewer revises by appending, an implementer disputes by appending, an owner rules by appending.

## Ledger index

`LEDGER.jsonl` holds one JSON object per line, append-only, in time order: `{ts, review_id, event, actor, ref, sha256, note}`. Events: `opened`, `inputs-frozen`, `findings-recorded`, `reconciliation`, `disposition`, `recheck`, `status`, `closed`, `legacy-registered`. Folders created before this schema (`legacy-v0`) are registered with their file hashes at registration time and are frozen from then on; their internal layout is not normalised.

## Verification

`tools/check_review_ledger.py` fails when an immutable file's hash differs from its manifest, when `dispositions.jsonl` or `LEDGER.jsonl` has lost or reordered lines, when a finding ID is duplicated or a disposition references an unknown ID, when a review folder is absent from the ledger, or when a legacy folder's registered hashes changed. Run it with the other register checks before any commit that touches `reports/reviews/`.

## Rules

- A review is never edited to make it agree with a later fix; the fix and the recheck are new lines and new files.
- Reviewer unavailability is recorded as `unavailable`, never as passed.
- `reviewed` never means formal maturity graduation; maturity moves only through the register's own rules.
- Snapshots of reviewed sources are not stored here; `inputs.json` carries hashes plus retrieval references to commits/blobs or externally retained snapshots. Hashes verify matching bytes but cannot reconstruct missing source or prove the code changed.

## Agent workflow and local enforcement

Use the shared [adrl-review-ledger skill](../../skills/adrl-review-ledger/SKILL.md).
`python3 tools/review_ledger_guard.py check` adds committed-HEAD comparison to the existing
consistency checker. `check --staged` checks the actual index that would be committed.
Run `install-hook` once per clone; existing hooks or hooksPath configurations are preserved
and require explicit integration rather than being overwritten. The hook is local and
bypassable, not server branch protection or actor authentication.

History comparison preserves exact committed bytes. JSONL additions start after an LF newline
boundary, with timezone-aware monotonic timestamps. CRLF conversion, removal/reordering and
Unicode line-separator reinterpretation do not excuse changing committed bytes. Legacy sealed
prefix metadata keeps its original normalization for compatibility; committed-byte comparison
is the additional history guarantee. First-commit provenance still depends on the retained
reviewer record and independently frozen inputs.

Published checkpoints contain all fixed files above. Prepare externally while incomplete;
publish a new checkpoint together with its ledger registration. Every file is classified by
its manifest (except the manifest itself). A manifest extension archives its exact previous
bytes and appends a reconciliation event. Status and disposition changes require matching new
ledger events. Reviewer rechecks use immutable/add-only artifacts and `recheck` events.

Disposition vocabulary: `unresolved`, `accepted`, `fixed-awaiting-recheck`, `verified-fixed`,
`deferred-with-reason`, `disputed-with-evidence`. Roles are `coordinator`, `implementer`,
`reviewer`, `owner`, followed by `:<identity>`. Last appended record per finding wins.
Unknown values remain unresolved in the query. `blockers` clears `verified-fixed` only for a
reviewer-labelled record with a sealed evidence reference and matching reviewer `recheck`
event. Owner deferrals need sealed evidence plus an owner `disposition` event and exact `scope`;
`blockers --scope <scope>` reports such waivers separately. This validates recorded provenance,
not whether the actor is genuine or the evidence justifies its conclusion. Historical legacy
reviews remain unknown to automated finding queries. Unresolved findings can be committed;
integrity acceptance does not approve completion or promotion.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.
