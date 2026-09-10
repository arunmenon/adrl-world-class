# ADR register and maturity audit

Inspector: rv-adr-maturity (Fable 5.1). Inputs: frozen snapshot at `adrl-review-fable-2026-09-08/snapshot/{register,runtime}` plus read-only `git show HEAD:` on the original register. Companion table: `appendix/adr-maturity.csv` (77 rows, 16 columns). No tests were run, no repository was written to. Test counts quoted from the register are author claims read from validation manifests; I did not reproduce them.

## 1. Count reconciliation

| Source | Count | Notes |
|---|---|---|
| ADR files under `adr/<BUCKET>/ADRL-*.md` | 77 | FND 5, SEM 7, SAF 9, RTG 9, CAS 9, MEM 10, LRN 8, TRU 3, EVL 9, OPS 8 |
| INDEX.md rows | 77 distinct | every file appears exactly once; none extra |
| Handoff manifest `adr_ids` | 77 | `reports/research/independent-review-handoff-2026-09-08/manifest.json` |
| 7 September maturity baseline records | 77 | `reports/research/adrl-maturity-baseline-2026-09-07.json`, dated 2026-09-07, hashes taken before the W0 note |
| ADR files in the 2 September commit | 55 | 49 originals plus 6 proposed on 2 September; 22 files (CAS-009, SEM-007, TRU x3, EVL x9, OPS x8) were created on 3 September and are untracked |
| Module map decisions with code | 74 of 77 | EVL-001, EVL-008, RTG-007 intentionally unmapped; 111 modules in the map equal 111 non-init modules on disk; no phantom citations |
| Test files citing an ADR id | 47 ADRs | 85 test modules in total; 30 ADRs are covered only indirectly |
| INDEX verdict tally | 38 + 8 + 28 + 3 = 77 | consistent |

The only pre-window baseline is the 2 September commit, and it covers 55 files. Against it, seven files changed their Status field on 3 September (proposed amendments and supersessions) and one changed both fields: MEM-010's maturity moved from "D0 Design, nothing exists" to "historical D0 plus scoped D2" on 7 September. Every other Maturity field is byte-identical between the 2 September commit, the 7 September baseline and the current tree.

For all 77 decisions the current Status and Maturity fields are verbatim identical to the 7 September baseline. The claim repeated in CHANGELOG, INDEX and every wave report that "all 77 status and maturity fields are preserved" is true. There were zero promotions in the window, formal or informal.

## 2. Assessment summary

Assessed per EVL-007 for the scope adrl-core actually tests. Because adrl-core has never carried organic traffic through its router (the 7 September pilot was observation-only with no routing decision), nothing in it can be D3 by EVL-007's own definition. The register says this in the INDEX preamble.

| Assessment versus the recorded claimed level | ADRs |
|---|---|
| agree | 36 |
| recorded higher than evidence | 16 |
| recorded lower than evidence | 25 |

### 2a. Recorded maturity higher than the evidence supports

None of these were promoted in the window; they are historical claims carried in the Maturity field. Because the field is the value the baseline preserved and a reader of the file sees first, the effect persists.

| ADR | Recorded | Assessed for adrl-core | Why |
|---|---|---|---|
| FND-001 | D3 Shadow | D2 Messages boundary, D0 Responses | old-repository shadow evidence; INDEX column already says D2 scoped |
| FND-003, SEM-001, SEM-002 (derivation), RTG-001, RTG-003, RTG-006, CAS-001, SAF-003, MEM-008 | D3 Shadow | D2 | fixture tests only; no adrl-core shadow window, no published precision (SAF-003), no classifier run (RTG-006), no shadow metric (MEM-008) |
| FND-004 | D4 Pilot (review: D3) | D2 | fault matrix is synthetic |
| FND-005 | D3 governance | D2 tooling; rule not gradable | field itself concedes the scale fits poorly |
| SEM-004, RTG-005, CAS-004 | D3 (review: D2) | D2 | agrees with the review's recommendation |
| SAF-007 | D2 Tested (review: D1/D0) | D2 for the tested sandbox subset and the synthetic container lifecycle; D1 for the decision as written | read isolation, command allow-list and `unverifiable` labelling remain unmet after fourteen W3 sections |

### 2b. Meaningful tested progress the record does not describe in its Maturity field

| ADR | Field says | What the code and tests show | Window |
|---|---|---|---|
| SAF-008, SAF-009, CAS-009, TRU-002, TRU-003, OPS-002, OPS-003, OPS-005, OPS-007, RTG-009, LRN-006 | D0, "nothing built" or describes the 2 September defect | implemented and unit or adversarially tested since 3 September (`gates/workload.py`, `gates/deployments.py`, `routing/side_effects.py`, `ledger/anchoring.py`, `learning/abstention.py`, `routing/cost.py`); `docs/known-gaps.md` "Closed on 2026-09-03" table records the closures | pre-window; never corrected on 7 or 8 September |
| LRN-003, LRN-008 | "nothing is built" / "nothing exists" | `learning/estimator.py` (S/T/X learners, bootstrap) and `learning/explore.py` (propensity logging, doubly robust OPE) exist and are tested; the 8 September sections in the same files describe them | field contradicts the file's own 8 September text |
| LRN-004 | "enforcement mechanisms do not exist" | features-v2 snapshot on decision rows, temporal session-grouped splits, exact version rejection, composition guard; 159 focused tests | W7.0a, 8 September |
| EVL-005 | D1, "no scorecard separates them yet" | Lab A.1 export labels every cell synthetic, T4 and learning-ineligible; 7 runner tests; separate report | Lab A.1, 8 September |
| TRU-001 | D0 in the file | signed launcher assertion binding, unknown is local-only, adversarial TRU suite; INDEX column already says "D2 scoped local binding" | 7 September, plus 11 W3 sections |
| MEM-005 | replacement clauses "have no implementation" | field-level inventory (381 entries) enforced by a check, per-session encryption of all new W3 metadata, retroactive pin shredding test | 7 and 8 September |
| MEM-001 | amended clauses "D0 until a test exists" | migrations 0003 to 0012 with upcasters, idempotency tests for intake, captures, attempts, launch history | 7 and 8 September |
| SEM-006 | D0 overall | constraint-inheritance half (lineage from headers, pin inheritance) is tested; the review demanded D2 for that half | pre-window |
| EVL-002, EVL-003, EVL-004, EVL-006, EVL-007, EVL-009, OPS-004, OPS-008, LRN-007 | D0 or D1 | unit tests exist for the mechanism each names; EVL-006's offline comparison was actually run on 7 September | 7 September or earlier |

These are cases where the body sections are honest and the field table is stale. The body/field split is the register's chosen convention ("scoped evidence without promotion"), but eleven fields still describe a defect the same repository records as closed five days ago.

## 3. INDEX, overview and CHANGELOG synchronisation defects

1. **INDEX evidence column lags the files for every 8 September slice after W3.2b2c.** The rows for MEM-001, MEM-002, MEM-003, MEM-005, MEM-010, OPS-001, SAF-007 and TRU-001 stop at the W3.2b2c writer-boundary research; the W3.2b2d1, W3.2b2d2, execution identity, one-shot prototype and receipt-correction sections (five slices, each with its own file section and changelog row) are absent from `INDEX.md` lines 160, 202 to 211, 234 and 260. The CHANGELOG entries for those slices each claim "index" was synchronised.
2. **INDEX rows carry none of the 8 September routing evidence.** RTG-002, RTG-003, RTG-006, LRN-003, LRN-004, LRN-005, LRN-008, FND-002, CAS-001, CAS-003, CAS-005, EVL-005 and SEM-007 have dated sections for the routing diagnostic, Lab A.1 or W7.0a; their INDEX rows (lines 129, 140 to 146, 170 to 176, 186 to 190, 219 to 226, 248) end at the 2 September or 7 September wording. The preamble paragraphs mention the work; the per-decision rows do not. The W7.0a CHANGELOG entry says "Updated RTG-002/003/006, LRN-004/005/008, FND-002, overviews, index".
3. **Maturity column versus file field.** For FND-001, FND-005, SEM-002 and TRU-001 the INDEX maturity column carries a scoped statement ("Historical D3; extracted Messages boundary D2", "D2 scoped local binding") that the file's Maturity field does not. For TRU-001 the file says D0 and the INDEX says D2. Only SEM-007 and MEM-010 had their fields rewritten on 7 September to match.
4. **Bucket overview verdict tables are frozen at 2 September.** All ten `adr/<BUCKET>/README.md` tables still read "claimed to recommended" from the review. The SEM table has no SEM-007 row and its finding 8 still says SEM-007 was "not written as a file in this review" (`adr/SEM/README.md` line 100); the CAS table has no CAS-009 row and the file does not mention CAS-009 at all. Dated banners above the tables are current, so the overview contradicts itself within one page.
5. **Sections added without changelog rows.** MEM-007, MEM-008 and LRN-004 received a "Context-graph planning note, 2026-09-08" and EVL-005 and LRN-005 an "Experiment-lab planning note, 2026-09-08" with no matching changelog row, breaking the register's own rule that every change is logged. The CHANGELOG entries for those planning passes describe the notes, so the omission is per-file only.
6. **CHANGELOG is complete for runtime slices.** Every 7 and 8 September runtime change I could name from patches or validation manifests has a CHANGELOG entry with report, evidence and diff links. The 2 September "Recommended 10 maturity changes" line and the current README both remain accurate.
7. **Broken links.** All register-internal and register-to-runtime links resolve once the snapshot layout is mapped back to the original sibling directories. Three links carry a `:line` suffix that does not resolve as a path (`reports/adrl-course-correction-plan-2026-09-07.md` to `gates/cli.py:224`; `reports/adrl-independent-research-review-2026-09-07.md` to `learning/artifacts.py:116` and `proxy/pipeline.py:508`). Cosmetic.
8. **Runtime documentation lags the register.** `adrl-core/README.md` and `docs/known-gaps.md` open with "W3.2b2d1 current context" although the register records three later slices (identity research, one-shot prototype, receipt correction) as complete. The register's forward references into the runtime therefore point at docs that describe an older state.

## 4. Forward traceability (behaviour change without an owning update)

I cross-checked every runtime file named in the 7 and 8 September patches and validation manifests against ADR changelogs.

- W3.1 through W3.2 receipt correction (ten patches): each touched `ledger/capture.py`, `ledger/attempts.py`, `core/process_owner.py`, `core/attempt_coordinator.py`, `ledger/keystore.py`, `api/store.py`, `core/resource_owner.py`, `core/container_control.py`, `core/execution_control.py`, `core/isolated_execution.py`, `core/launch_markers.py`, migrations 0007 to 0012 and their tests. Every module's primary and secondary owners received a dated section and changelog row. No omission found.
- Lab A.1 added `tools/run_routing_lab.py`, `tests/unit/test_routing_lab.py`, `artifacts/lab/routing-suite-v1.json` and `docs/routing-lab.md`; EVL-005, RTG-002, MEM-001 and SEM-007 record it. No runtime behaviour changed (validation `runtime_behavior_changed: false`).
- W7.0a changed `routing/features.py`, `app.py`, `tests/unit/routing/test_mixed_intent.py` and `docs/routing-features.md`; RTG-002, RTG-003, RTG-006, LRN-004, LRN-005, LRN-008 and FND-002 record it with the failed candidate retained.
- Two defect fixes inside W3 (restored-key reads after a failed audit; engine-info 404 read as resource absence) are recorded in MEM-010, MEM-001 and OPS-001 sections. Good.
- **Gap (minor, 7 September):** `PostToolUseFailure` hook ingestion as a product observation is a harness-mechanical signal under CAS-001 clause 4. CAS-001 has no 7 September section or changelog row; the fact lives only in `docs/known-gaps.md`.
- **Gap (minor):** features-v2 changes the `features_version` recorded on every decision row. MEM-001 and CAS-006, whose decision-context schema carries it, have no W7.0a note; the data-inventory check passed, so the field pre-existed.
- **Over-attribution rather than omission:** SEM-006 received W3.2b1 and W3.2b2c sections about process-group cleanup although the sections themselves say OS ancestry is not agent lineage and nothing about subagent routing changed.

## 5. Reverse traceability (claim without code or qualifying evidence)

- **Module map:** all 111 modules exist; 74 of 77 mapping verified from docstrings; unmapped set matches the baseline. Holds.
- **Test-count claims:** 911 passed / 8 skipped / 322 inputs (W7.0a), 894 / 8 / 320 (Lab A.1) and 895 / 0 / 316 (receipt correction) are present in the corresponding validation manifests. I did not rerun them; treat as unverified by this review.
- **Engine qualification drift:** the only zero-skip run (895 tests) was on 316 inputs. Both later validations skipped the eight engine cases "without a fresh allowance". So the current 322-input source has not been shown to pass the engine cases. The register states this in each entry; the executive review (`reports/adrl-executive-review-2026-09-08.md` line 32) presents "895 tests, no skipped tests" as "the latest full validation", which was true when written and is now stale.
- **TRU-001 D2 (INDEX):** resolves to `api/auth.py`, `gates/workload.py`, `tests/adversarial/test_tru_suite.py` and `tests/integration/e2e/test_product_services.py`. Code exists; the inconsistency is between the file field and the INDEX, not between claim and code.
- **OPS-001 ownership:** eight W3 execution modules cite OPS-001 as primary owner, so the map shows OPS-001 with thirteen modules while its own three clauses (state inventory, startup lock, second-worker refusal) have no code. The field honestly says D1; the map overstates coverage.
- **SEM-006 W3 sections:** resolve to `tests/unit/test_process_owner.py`, which does not exercise the decision.
- **EVL-007 follow-ups:** the dev-key refusal golden test for graduation records is not present (dev-key refusal is tested only for checkpoint keys in `tests/unit/ledger/test_anchoring.py`); the follow-up box is correctly unchecked.
- **RTG-007 as blueprint anchor:** the 8 September blueprint and roadmap anchor the target architecture in RTG-007 and propose disposing its pending amendment; the file is unchanged and unmapped. Acceptable as planning, but the anchor decision has no dated note.

## 6. What improved in the two days without a grade change, by bucket

- **MEM:** the largest concrete gain. Encrypted retained captures (0007), attempt journal with terminal-capacity grants (0008, 0009), execution fences (0010), authenticated resource history (0011) and launch history (0012); persistent key revocation before mutation closing a reproduced resurrection hole; inventory grown from 256 to 381 entries with a check. Tested only on synthetic fixtures; no capture is bound to a verifier receipt and no attempt has a successful close.
- **OPS and SAF-007:** a pinned synthetic container lifecycle (create, bind, one-shot launch, seal, stop, discard, recover after key erasure or owner death) passed the engine once with zero skips; two earlier engine runs failed and are retained. This is the second-largest gain and the least connected to any ADR's own promise, because it is filed under OPS-001 and SAF-007 whose clauses it does not implement.
- **RTG and LRN-004:** the router's first behavioural correction. features-v2 fixes two mixed-intent masking cases through the real Messages path, with a failed first candidate retained, 720 before/after component decisions published, and conservative false positives on quotes and negation disclosed. Exploration is now refused when the learning contract (still features-v1) mismatches live features. Still no model completion, calibration or economics.
- **EVL-005 and SEM-007:** a repeatable synthetic workbench with an immutable manifest, append-only journal, a disqualified first export and a corrected one. Diagnostic capability, not routing quality.
- **TRU-001:** every new internal API consumes the authenticated local principal; no new trust boundary, no SCM corroboration.
- **FND, SEM (other), CAS, RTG-007, EVL (other), OPS (other):** planning notes, diagnostic mentions and bucket banners only.

## 7. Findings

**F1. INDEX evidence column is stale for 21 decisions (medium severity, high confidence).** Claim: each 8 September CHANGELOG entry states the index was synchronised. Observation: INDEX rows omit the five latest W3 slices for eight ADRs and all routing-window evidence for thirteen ADRs (section 3, items 1 and 2). Acceptance: a script that, for every ADR, lists dated `##` sections and asserts each has a matching link in its INDEX row; zero misses across 77 rows.

**F2. Eleven Maturity fields describe defects the repository records as closed on 3 September (medium, high).** Claim: fields for SAF-008, SAF-009, CAS-009, TRU-002, TRU-003, OPS-002, OPS-003, OPS-005, OPS-007, RTG-009, LRN-006 say nothing is built or describe the 2 September defect. Observation: `docs/known-gaps.md` closed table, module map and citing tests show implementation. Acceptance: each field states "historical D0; scoped D2 for <named behaviour> (date)" in the same form used for MEM-010 and SEM-007, with a changelog row.

**F3. File field and INDEX column disagree on maturity for four decisions (medium, high).** FND-001, FND-005, SEM-002, TRU-001. Acceptance: one source of truth; the INDEX column is generated from the field or the field carries the scoped text.

**F4. Bucket overview tables are two-day-stale and two rows are missing (low, high).** Acceptance: every bucket README table has one row per file in that bucket and its maturity cell matches the file field; the SEM finding 8 note is dated and corrected.

**F5. Five planning notes lack changelog rows (low, high).** MEM-007, MEM-008, LRN-004, EVL-005, LRN-005. Acceptance: every `##` section carrying a date has a changelog row with the same date.

**F6. Sixteen historical D3/D4 claims remain the first thing a reader sees (medium, high).** EVL-007 rule two says a new implementation inherits no level above D2, and the INDEX preamble states it; the EVL-007 follow-up to record it per decision is unchecked. Acceptance: each affected Maturity field opens with the adrl-core level its own tests support and relegates the old-repository level to "historical".

**F7. Engine-case qualification does not cover the current source (low, medium).** The 322-input build has only been validated with the eight engine cases skipped. Acceptance: one bounded engine run on the final W7.0a source with zero skips, or an explicit statement in INDEX and the executive review that engine qualification is at the 316-input source.

**F8. Ownership drift in the W3 execution backend (low, high).** Thirteen modules cite OPS-001 and thirteen cite SAF-007 as owner although neither decision's text covers container execution; no ADR owns "internal isolated execution" as a decision. Acceptance: either an explicit clause added to OPS-001/SAF-007 by amendment or a new proposed decision, so that the roadmap DQ on "exact output and model-path controls" has an owner.

**F9. Executive review cites a superseded validation as current (low, high).** Acceptance: leadership documents carry the validation date and input count next to every test count.

## 8. Files opened versus skimmed

Opened in full: all 77 ADR files' field tables and changelog tables (programmatic extraction) and full text of FND-002, RTG-002, RTG-003, RTG-006, LRN-003, LRN-004, LRN-005, LRN-008, CAS-001, CAS-003, CAS-005, EVL-005, EVL-007, MEM-001, MEM-002, MEM-003, MEM-005, MEM-007, MEM-008, MEM-010, OPS-001, SAF-007, SEM-002, SEM-006, SEM-007, TRU-001; INDEX.md; CHANGELOG.md; README.md; source/01-overview-tenets-taxonomy.md; reports/adrl-register-sync-2026-09-07.md; reports/adrl-routing-correction-2026-09-08.md; reports/adrl-lab-first-run-2026-09-08.md; reports/adrl-routing-in-action-2026-09-08.md; reports/adrl-w3-transport-receipts-2026-09-08.md; reports/adrl-executive-review-2026-09-08.md; reports/adrl-independent-review-prompt-2026-09-08.md; reports/waves/routing-decision-quality.md, lab-planning-deliverables.md, w3-active-copy-custody.md; reports/research/independent-review-handoff-2026-09-08/README.md and manifest.json (keys); the maturity baseline JSON; routing-lab and routing-correction validation.json; adrl-execution-state.json; runtime docs/adr-module-map.md, routing-features.md, routing-lab.md, engineering-checks.md, known-gaps.md, isolated-execution.md, operator-captures.md; runtime README.md and AGENTS.md (first 80 lines); tests/unit/routing/test_mixed_intent.py (first 40 lines).

Skimmed or extracted programmatically: REVIEW-LOG.md (truncated read); the ten bucket READMEs (verdict tables and banner lines extracted, prose not read); the remaining 12 W3 reports (ADR mentions and maturity lines only); the product roadmap (sections 6 and 10 read, rest skimmed); the journey (headings and current-position section); the other 50 ADR bodies (field tables, dated headings and changelog only); all wave patches (file lists only); runtime source (grep-level checks on pin.py, cost.py, estimator.py, abstention.py, explore.py, checks.py, controller.py, anchoring.py, identity.py, check_learning_contract.py; docstring ADR citations for all 111 modules and 85 test modules).

Not opened: design/ documents, the blueprint, the investment brief, the lab plan, the context-graph proposal, output/ decks, the remaining runtime docs (attempt-lifecycle, attempt-coordination, key-revocation, process-ownership, stopped-resource-ownership, data-inventory, product-services, verifier-experiments, protocol-boundary, responses-admission, egress-anchoring), and the raw evidence JSON bodies beyond the fields quoted above.
