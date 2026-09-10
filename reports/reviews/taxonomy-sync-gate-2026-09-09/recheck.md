**Disposition: accepted, scoped.** All four blockers are resolved as embedded. Acceptance is conditional on the final run reproducing this material exactly. No maturity, status or verdict changes.

## Blocking findings, verified

- **1. Changelog rows.** Both dated rows now sit directly under the header separator, newest first. The checker walks back from the marker row over contiguous pipe lines and requires a Date header and separator. The standalone-row test inserts the blank line and fails. Resolved.

- **2. Display-grade guard.** The snapshot now records verdict and maturity cells from the owning INDEX and bucket rows, and the check compares them to baseline and demands a record carrying display_before and display_after. The supplied before/after cells for FND-005 and EVL-009 are identical in all four positions, and the post-change rows shown append only to the evidence column. Positive and negative tests exist. Resolved, with the wording caveat below.

- **3. B1 provenance.** The original bootstrap has no parsed fields, its hash is recorded, capture preceded the first tool-file birth by about three minutes, and all 422 preserved inputs byte-match. The derivative baseline adds fields from those preserved bytes with the current parser. The inline-command history is disclosed honestly and no script hash is asserted. That is the verifiable chain I asked for. Resolved as host evidence, not attestation, which the artifact states.

- **4. Report wording.** Baseline-relative phrasing, copy-of-receipt wording, the 323-of-324 manifest comparison with path and hash, and installed parity stated as measured rather than exercised are all corrected. Resolved.

## Non-blocking residuals

- **Guard scope wording.** Only owning rows are compared, but display cells for every ADR are already captured. Either compare the whole dictionary or add the word "owning" in the skill and both ADR sections.
- **CHANGELOG rendering.** The two lines still run together as one paragraph.
- **Baseline location.** Both baseline artifacts sit inside the register under the excluded reports tree, which the new begin command would now refuse. Disclosed, acceptable, but note it in the report.
- **Historical changelog order.** FND-005 still lists 2026-08-27 before 2026-09-02. Preexisting, not this wave.
- **Field-change test.** Still accepts KeyError. The positive test covers the logic, so this is hygiene only.

## Acceptance conditions

Record this recheck as the pinned review record with status accepted and an empty blocking list. Then rerun the check and require all of the following:

1. The 19 tests pass with output matching the pinned tests.log.
2. Every after-hash in closure.json, including the three evidence hashes and the review-inputs hash, matches the recheck source hashes unchanged.
3. The mirror check passes in the real run for the first time, and the receipt copy states this.
4. Any subsequent source, evidence or report edit returns the closure to pending.

If the final report is edited to add the residuals above, re-pin its hash before the run. That is a routine evidence update within existing authority.