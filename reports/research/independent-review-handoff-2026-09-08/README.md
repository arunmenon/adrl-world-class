# Review evidence map

Window: 7–8 September 2026 IST through manifest timestamp. This map is author-prepared navigation, not independent verification. `manifest.json` records current files, hashes and source scopes, including untracked files. It does not prove change dates or complete review coverage.

## Read first

- `reports/adrl-independent-review-prompt-2026-09-08.md`: full assignment.
- `AGENTS.md` in both repositories; `INDEX.md`; `adr/EVL/ADRL-EVL-007.md`.
- `reports/adrl-product-roadmap-2026-09-08.md`, `reports/adrl-implementation-roadmap-2026-09-07.md`, `design/adrl-experiment-lab-plan-2026-09-08.md`: three plans to reconcile.
- `reports/adrl-implementation-journey.md`, `reports/research/adrl-execution-state.json`, `reports/ADRL-NOW.md`: claims to verify, including all 21 journey entries. Earlier 7 September work predates entry 001.

## Workstream entry points

| Area | Entry points in register; follow references into runtime/raw evidence |
|---|---|
| Baseline and research | 3 September product report/research critique; 7 September independent research review, register sync, course-correction plan; `reports/research/adrl-maturity-baseline-2026-09-07.json`; source ledgers and historical `source/` |
| Product APIs and harnesses | `design/adrl-multi-harness-product-contract-2026-09-07.md`; product-foundation, product-services, session-verification, live-observation-pilot and claude-subscription-pilot reports dated 7 September; `profiles/` |
| Early improvement evidence | adaptive-improvement-proposal and improvement-experiment reports dated 7 September; matching raw evidence; runtime `docs/verifier-experiments.md` |
| W0 and W3 | All `reports/adrl-w3-*.md`, `reports/waves/w3-*.md`, W0 packet/baseline and matching research patches, manifests, logs and failed attempts. Include writer custody, launch failures, transport diagnosis and unfinished active-copy packet |
| Visible routing | routing-in-action report and `reports/research/routing-demonstration-2026-09-08/` |
| Lab | lab-first-run report; lab-a-routing-experiment packet; `reports/research/routing-lab-2026-09-08/` including run-1 qualification and run-2; runtime runner, suite, tests and docs |
| Routing correction | routing-correction report; routing-decision-quality packet; `reports/research/routing-correction-2026-09-08/` including before, candidate-1, failed checks, after-final, final checks and lab-final; features/app/version contract code |
| Product and RSI | product roadmap, startup-investment-brief, adaptive-routing-rsi-blueprint; context-graph proposal; lab plan; corresponding source ledgers/validation |
| Planning deliverables | `design/adrl-lab-planning-and-assessment-2026-09-08.md`; `reports/lab/planning-starter-v1/`; `reports/waves/lab-planning-deliverables.md` |
| Leadership visibility | executive-review report, `output/adrl-executive-2026-09-08/`, ADRL-NOW, progress skill and journey; inspect deck contents rather than inferring from filenames |
| Process addition after implementation | current review prompt, critical-review skill in Codex and Claude, register AGENTS checkpoint addition. These were added during handoff preparation and are not evidence that earlier waves were independently reviewed |

## Current claims requiring independent verification

The execution state reports W7.0a complete in offline scope, 911 passing tests, 8 skipped engine tests, 11 checks and 322 runtime inputs. These are archived claims; reconcile current hashes and logs. Prior engine qualification has a different scope. The 16-cell lab is synthetic, planning packs prepared but not executed, and no maturity promotion is claimed for the latest routing repair. Check these statements rather than accepting this map as proof.

Source backups are referenced by execution state and historical evidence. Inventory lists discovered backup manifests separately; their snapshot contents are not included or exhaustively hashed here. Inspect only relevant authorized source snapshots. Dates and Git alone cannot reconstruct the whole two-day delta.

## Coverage boundaries

The inventory includes register ADRs/design/profiles/reports/source/output, selected root instructions/indexes, declared runtime input directories/root files, and the two relevant personal skills. It excludes Git internals, caches, private runtime data, keys, credentials, unrelated personal configuration, `_to_delete`, `.project`, chart scratch folders and bulk hidden build snapshots. Exclusion is not evidence of irrelevance: reviewers should identify needed missing historical material using cited manifests. Generated renderings can be marked duplicate only after establishing what source they represent.

The workflow smoke test, if successful, is only Claude's evaluation of the new review instructions; it is not the requested full repository review. Keep that distinction in all reporting.
