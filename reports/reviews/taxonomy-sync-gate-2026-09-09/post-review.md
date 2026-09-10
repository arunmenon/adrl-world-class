**Disposition: not yet accepted.** The mechanism is sound and B2, B3, B5 and B7 are resolved as written, but four items block recording this review as accepted. Nothing here changes maturity, status or verdict.

## Blocking findings, in priority order

- **1. Both ADR changelog rows sit outside their tables.** In FND-005 and EVL-009 the new dated row follows a blank line after the table, so it renders as a stray fragment, and in EVL-009 it also breaks the newest-first order. The checker accepts any line beginning with a pipe, so the mechanical gate passed on a defective register edit. Move each row into the table, then tighten the check so the marker row must be adjacent to other table rows.

- **2. The maturity guard covers ADR tables only.** Status, Maturity and Verdict cells in INDEX and bucket rows can change with no human record, because those files are only hash-pinned and marker-scanned. The B6 resolution promised exact-value protection. Either diff the owning rows' cells against the baseline, or state this limit explicitly in the skill, both ADR sections and the report. I saw only post-change rows. Supply the pre-change INDEX and bucket rows for FND-005 and EVL-009 so I can confirm no grade cell moved.

- **3. B1 needs one verifiable fact.** The pending check got past the schema, scope, roots and fields comparisons. That means bootstrap-baseline.json carries a scope dictionary identical to the final constant and a fields map produced by the same parser. Either the scope and parser were frozen before the first edit, which is fine, or the baseline was regenerated later, which contradicts the preserved-bytes claim. Provide the baseline-source script hash, its location outside both scanned trees, and its capture time against the first edit. Missing material, not a defect yet.

- **4. Report wording overstates three things.** "Core runtime unchanged" is true only relative to this wave's baseline; say so. The B4 promise to compare runtime inputs against the recorded manifest is not evidenced, and that manifest was already superseded by the 2026-09-08 W7.0a run. The report says a receipt lives "in this directory", but a receipt cannot be inside the repository; call it a copy. Installed-mirror parity has never been exercised in a real run because the check fails before reaching it, so "installed identically" is currently an assertion. Fix the report, re-pin its hash, rerun.

## Non-blocking findings

- **Fragile links.** Both ADR sections link the checker and tests through the parent directory by name. Use the two-level relative path to the register's own tools directory.
- **Test gaps.** The field-change test passes on a KeyError, not on validation logic. Add a positive test with a valid human record, a test for baseline scope mismatch, and a CLI test for the receipt-outside-repository and existing-output rules.
- **Register rendering.** The two CHANGELOG lines run together as one paragraph; add list markers or blank lines.
- **Ownership wording.** The two ADR sections are byte-identical boilerplate. EVL-009's section should say concretely what blocker-style behavior the checker exhibits, namely named nonzero failures that are never aggregated.
- **Coverage never fully exercised.** Global INDEX coverage and the FND/EVL bucket checks did run, since the pending failure is late in the sequence. The CAS-009 gap stays open and disclosed, which is correct.

## Accepted as resolved

B2 closure schema, B3 outside-repository receipt with excluded evidence directory, B5 register-hosted stdlib harness, and B7 stray-ADR rejection all match the code and tests. The scoped B6 disclaimer is acceptable subject to finding 2.

## Required sequence before acceptance

Fix items 1, 2 and 4, supply the material for 2 and 3, refresh the pinned evidence and source hashes, then request a material-fix recheck from me. Only that recheck can move the closure to accepted with this record pinned. Do not set accepted on the basis of an authored resolution of these findings. Pending remains pending.