# Findings

## review-governance-pre-2026-09-10:RG-P01 — Deleted folders and added legacy files pass

main() iterates existing dirs only; a removed registered folder yields no problem. Legacy branch iterates recorded rels, so new files pass.

Acceptance: HEAD path set under reports/reviews is a subset of index path set; legacy folder path set equals registered set. Tests for both.

## review-governance-pre-2026-09-10:RG-P02 — Manifest rehash and legacy bypass

Checker trusts manifest.json bytes; a legacy folder gaining manifest.json skips legacy hash checks.

Acceptance: If manifest.json differs from HEAD, HEAD manifest bytes exist as manifest-<n>.json, every HEAD entry keeps class and sha256, sealed line counts never decrease, old prefix still verifies. legacy-registered is terminal regardless of manifest.

## review-governance-pre-2026-09-10:RG-P03 — Append prefix semantics ambiguous

prefix_sha256 hashes "\n".join(splitlines()[:n]), dropping trailing newline, CR and Unicode separators; a byte-prefix guard can disagree with it.

Acceptance: One rule: HEAD bytes are a byte prefix of staged bytes and the boundary falls on a newline. Tests cover CRLF, missing trailing newline, U+2028.

## review-governance-pre-2026-09-10:RG-P04 — Unlisted files and status changes unchecked

Files absent from manifest are ignored; status.json replacement needs no LEDGER event despite README.

Acceptance: Every staged file in a v1 folder has a manifest class; status.json change requires a same-commit LEDGER status line carrying its sha256.

## review-governance-pre-2026-09-10:RG-P05 — Finding IDs only locally unique

Duplicate check is per folder; global_id never compared with folder name.

Acceptance: global_id equals <folder>:<id>, unique across all findings.json; dispositions resolve to a known finding.

## review-governance-pre-2026-09-10:RG-P06 — Blockers query lacks vocabulary and precedence

README gives record fields but no disposition or actor enum; actor is self-declared.

Acceptance: Fixed enums; last line in file order wins; cleared only by reviewer recheck with evidence or owner disposition scoped to that finding; unknown values stay unresolved; output states no actor authentication.

## review-governance-pre-2026-09-10:RG-P07 — Hook chaining and index reads

Existing checker reads the worktree, not the index; core.hooksPath or an existing pre-commit may exist.

Acceptance: Guard reads git show :path; installer chains existing hooks, honors hooksPath, is idempotent; both skill copies byte-identical and tested.

