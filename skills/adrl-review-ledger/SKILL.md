---
name: adrl-review-ledger
description: Create and reconcile ADRL review records, query outstanding findings, and check review-history integrity before completion or commits. Use whenever an ADRL agent publishes reviews, dispositions, rechecks or review-status claims.
---

# ADRL review ledger governance

Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`.
Read the canonical [schema](/Users/arunmenon/projects/adrl-world-class/reports/reviews/README.md).
Use `adrl-critical-review` for independent criticism and `adrl-taxonomy-sync` for architecture
closure. This skill governs their records; it does not grant execution, spend or graduation.

## Before work or a completion claim

From the register run:

```sh
python3 tools/review_ledger_guard.py check
python3 tools/review_ledger_guard.py blockers
```

Read the actual findings and their append-only dispositions for the applicable wave/ADRs.
Do not assume a constant number of blockers. Legacy reviews are explicitly unknown to the
machine-readable query, not approved or fully accounted for. A later prose report does not
silently supersede an unresolved structured finding; append a linked reconciliation first.
A failure blocks the affected integrity/completion claim. Preserve the evidence and fix the
current record; never repair history by rehashing an edited original.

## Publish a checkpoint

Serialize ledger mutations through one coordinator; never run parallel writers. Prepare
externally, use collision-free new names, and stop on a publication conflict.

- Use a new `<slug>-<YYYY-MM-DD>` folder per independent checkpoint. Prepare externally while
  incomplete, then publish the fixed schema files together. Pre-wave and post-wave reviews
  are separate checkpoints; a recheck may be a new add-only reconciliation artifact.
- Freeze `packet.md` and `inputs.json` before review. Include source paths, hashes, revisions,
  dirty/untracked scope and exclusions. A hash cannot reconstruct source: retain an exact
  external snapshot or retrievable commit/blob, and record its location. Keep secrets out.
  Do not add source copies to this ledger; preserve already registered legacy copies unchanged.
- Retain the actual reviewer output and invocation/model metadata. `findings.json` and
  `findings.md` must describe the same reviewer findings with stable IDs. Global IDs are
  `<review_id>:<local_id>`. The initial immutable `dispositions.md` records unresolved findings.
  Do not invent reviewer findings, approval or identity. Record coordinator normalization.
- Publish `dispositions.jsonl`, `status.json` and `manifest.json`. Classify every file;
  `manifest.json` excludes itself. Original evidence is immutable, reconciliation files are
  add-only, dispositions are append-only, and status is replaceable with an accompanying event.
- Append timestamped actor/ref/hash events to `LEDGER.jsonl`. Publish new files and registration
  together; run the guard before claiming integrity. Never backdate a new event into history.

## Reconcile without rewriting

Append one disposition per change with `ts`, `actor`, local `finding_id`, `disposition`,
`evidence`, and `note`. Use actual roles (`implementer:`, `reviewer:`, `owner:`, `coordinator:`).
Actors are provenance labels, not authenticated signatures. Link the retained original action;
never attribute an implementer's conclusion to the reviewer or owner.

`accepted`, `fixed-awaiting-recheck` and `disputed-with-evidence` do not close a blocking finding.
`verified-fixed` needs reviewer recheck evidence. `deferred-with-reason` needs an owner ruling
with an explicit `scope`; it is not a fix. The blockers command conservatively keeps deferrals
visible unless called with that exact `--scope`, and reports scoped waivers separately.
Unsupported evidence or self-verification remains blocking. Existing authorization may supply
the owner ruling; do not manufacture new approval requirements or ask twice.

Add fixes/rechecks under new `reconciliation/` filenames; never replace an earlier response.
Before extending a manifest, retain its exact previous bytes as `manifest-<n>.json`, classify
the archive immutable, and preserve existing classifications and sealed evidence. Append a
reconciliation event linking the new manifest. Status changes also need a new status event.
Legacy folders remain frozen: reconcile them in a new checkpoint linked to the original.

## Before committing

Run both the existing checker and the new staged guard:

```sh
python3 tools/check_review_ledger.py
python3 tools/review_ledger_guard.py check --staged
```

The staged guard compares the proposed Git index with committed HEAD. A clean working copy
cannot excuse a tampered staged file. Use the local hook installed by
`python3 tools/review_ledger_guard.py install-hook` in new clones; never overwrite an existing
hook or hooksPath configuration to force installation. Report setup conflicts.

Also complete the applicable taxonomy-sync receipt and independent review. This integrity
check permits honest unresolved reviews to be committed; it does not approve a wave or clear
its blockers. Do not use `--no-verify`, remove the hook, or weaken validation to get a commit
through without an explicit user override recorded with its scope.

## Honest enforcement claims

The installed local Git hook blocks ordinary commits on this checkout. It is bypassable and
is not remote branch protection. Committed-baseline checks cannot prove that a brand-new
record was never edited before its first commit. Manifests prove consistency, not truthful
claims, authenticated actors, code fixes, test quality or graduation. New clones need hook
installation; remote required checks are a separate deployment. Report exactly which checks
ran, review state, unresolved scope and the next gate.

Reviewer recheck events must list the exact global finding IDs in `finding_ids`; a recheck of one finding cannot clear another. Newly appended disposition rows must use the documented roles and states. Unknown historical states remain unresolved.
