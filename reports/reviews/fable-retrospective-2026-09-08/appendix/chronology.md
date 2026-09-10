# ADRL change chronology, 7 to 8 September 2026 (Asia/Kolkata)

Inspector reconstruction from the frozen snapshot at `adrl-review-fable-2026-09-08/snapshot`, read-only git on the originals, and the on-disk execution-state backups under `/Users/arunmenon/projects/.adrl-execution-state`. Times are IST unless marked Z. Every time below comes from a manifest, validation record, check manifest or backup directory name, not from file modification time, except where I say "mtime". The companion ledger is `appendix/changes.csv` (48 rows, ids C01 to C48).

## 1. How the window was reconstructed

Git cannot establish the delta. The register has one commit (1c172c9, 2 September 2026 14:18Z) and shows 46 tracked files modified (+2840 / -61 lines) plus 30 untracked paths. The runtime repository has no commits at all. I therefore used four independent clocks and stitched them together:

- The pre-W0 manifests chain by README hash. Course-correction baseline records README `461c98eb`; product foundation maps `461c98eb` to `4b6907ba`; services maps to `debb84f5`; observation mode to `1b46f3f2`; session verification to `f56ac99f`; the improvement experiment to `88ef3a97`; W0 maps `88ef3a97` to `2c63a528`. That chain fixes the order of the six 7 September implementation packages without any timestamps.
- Timestamps inside those manifests. Three carry pytest junit timestamps with a `+05:30` offset (foundation 14:18, services 15:46, observation 16:12). Two carry UTC (session verification 11:09Z, improvement 12:45Z). The naive reading of the journey's "2026-09-08" dates for entries 003 to 007 only works once you notice those slices ran between 19:39Z and 23:41Z on 7 September, which is 01:09 to 05:11 IST on 8 September.
- The 15 backup directory names under `.adrl-execution-state` (for example `w3-1-20260907T191740Z`) and the three `.codex-executive-build/*-backup` manifests. The check manifests inside them carry `started_at` and a `tests.log`, and their sha256 values match the `check_manifest_sha256` fields recorded in the register manifests.
- The register validation records for every 8 September pass (blueprint 06:40Z, roadmap 07:37Z, lab plan 08:05Z, lab 08:28Z, correction 08:45Z, planning packs 10:35Z) and the inventory manifest at 10:48:41Z.

The W0 baseline (18:14Z on 7 September, 23:44 IST) is therefore not the start of the window. Roughly ten hours of 7 September work precede journey entry 001.

## 2. Ordered narrative

### 7 September, morning to early evening: research, contract, product APIs

The earliest dated artifact is the independent research review (C01). Its manifest says `review_date 2026-09-07`; the PDF in `output/pdf` has an mtime of 11:09 IST, and the project telemetry shows Claude invocations at 10:31 and 12:33 IST, which is consistent but weak. The accompanying artifact-source-check compared all 77 decision bodies of the 3 September critique with the published artifact (77 match) and could not open the product artifact.

The course-correction plan (C02) came next: a read-only baseline of 39 focused tests and a nine-check configuration validation, with README still at `461c98eb`. The multi-harness product contract design (C03) is referenced by that plan as its companion and has no manifest of its own.

Then four implementation packages landed in about two and a half hours by their pytest timestamps: product foundation at 14:18 (463 tests, 25 files, +2830 lines; an import cycle found by a post-application smoke check and fixed with three fresh-process regressions; two sandbox permission failures on the first run), register synchronization (C05, documentation only, 19 register documents, register `AGENTS.md` created), product services at 15:46 (506 tests, 25 files, migration 0003, loopback HTTP smoke; two defects fixed on the way: ADRL credential pass-through to the gateway and a cancellable ledger writer), and observation mode at 16:12 (511 tests, migration 0004, patch +1212 / -970).

Between services and observation mode the subscription pilot was prepared (C07): nine dataset-validator files copied to a temp workspace, baseline two passing and two `KeyError` tests, Claude Code 2.1.260 with `loggedIn: false` in the sandboxed environment, zero model calls. The live pilot (C09) then ran two real Claude Code sessions. The first, native Sonnet fix passed the four existing tests but was rejected by independent compatibility review because it regressed the formatter. This is the window's first recorded failed candidate. The repair session on 2.1.263 passed eight tests; 18 tool events reconciled with one native failure and zero hook failures. Harness-reported API-equivalent cost was $0.2921. The 8-line task patch is retained in the register.

Session verification (C10) followed at 16:39 (11:09Z): migration 0005, `adrl product verify`, two verifier jobs adding four receipts to a copied timeline, 532 tests. The improvement experiment (C12) ran at 18:15 (12:45Z): migration 0006, seven curated cases times two repeats, baseline 4/7 versus candidate 7/7, 549 tests. The manifest states plainly that the same assistant authored the proposal and the fixtures and that no holdout exists. The adaptive improvement proposal (C11) precedes it by its overlay banner.

The 84KB implementation roadmap (C13) with twelve waves, the wave packet template and the DQ1 to DQ8 decision queue was validated against 280 unchanged runtime hashes and the 549-test figure, so it sits between 18:16 and the W0 backup at 23:44.

### 7 September, 23:44 to 8 September, 11:19: the heartbeat chain

Journey entry 001 (C14) records the user triggering the waves and the creation of an hourly continuation. The first automation create was rejected for a missing destination; the second succeeded. From that point the backup directory names show a cadence of roughly one slice per hour: 19:17Z, 20:21Z, 21:25Z, 22:20Z, 23:22Z, 00:22Z, 01:20Z, 02:24Z, 03:17Z, 04:02Z, 04:17Z, 05:22Z.

W0 (C15) established the repeatable eleven-check runner, verified backups (278 runtime and 161 register files), an AST fix for the ADR module map, and reconciled stale README and protocol docs. The on-disk `baseline-checks/tests.log` reads `549 passed` and `engineering-checks-01/tests.log` reads `556 passed`. The W3 capture packet and the W8A Responses spike packet were frozen during W0 (C16); the W8A spike was never executed in the window.

Then eight W3 slices in sequence, each with a manifest, a patch, a register validation and a plain-language report: W3.1 captures (593 tests, 01:09 IST), W3.2a attempt journal (631, 02:13), W3.2b1 process ownership (669, 03:15), W3.2b2a terminal capacity (697, 04:07), W3.2b2b1 key revocation (724, 05:11), W3.2b2b2 coordination (759, 06:12), W3.2b2c writer-boundary research (runtime unchanged, 07:10), W3.2b2d1 stopped-resource ownership (812, 08:28). Every test count in that chain matches the tail of the on-disk `tests.log`, and every recorded `check_manifest_sha256` from W3.2b1 onward matches the on-disk manifest.

The failures and repairs inside that chain, in order:

- W3.2a: one documentation patch was rejected atomically for a missing context line and reapplied.
- W3.2b1: self-review found a cleanup Task that could be cancelled during loop shutdown before its worker thread stopped; replaced with a protected executor Future. A deliberately detached child survives group cleanup; recorded as a limitation, not waived.
- W3.2b2a: first focused run 62 passed / 4 failed (two fixture budgets above the boundary, two migration fixtures mistaking a digest for a manifest); corrected to 68 / 0.
- W3.2b2b1 is itself a course correction. A disposable fault probe showed the keystore removed the wrapped key before the shred audit; restoring the file made the old key readable and a new key could be created for the same session. The slice was split out to repair that before wiring more machinery to erasure.
- W3.2b2b2: three focused repair cycles (27/3, 32/3, 34/1, then 35/0) fixing a stale process report, a transaction-breaking fault fixture, the child interpreter and a revocation-versus-authority-loss distinction. A console-only diagnostic run was not retained. The first source backup at 00:21:59Z was rejected by the backup filter and redone at 00:22:27Z; the earlier directory still exists on disk and is not listed in the handoff manifest.
- W3.2b2c: Docker probe run 1 completed three container cases then failed with "container readiness not observed" because the driver used an unsupported `docker start` flag; run 2 completed six observations. A post-run correction reduced the compiler timeout from 60 to 15 seconds; the recompiled binary was identical. Eight containers and two images were created and confirmed removed.
- W3.2b2d1: no behaviour repair cycle; lint and type formatting only.

### 8 September, 08:47 to 11:19: launch failures and recovery

W3.2b2d2 began as a bounded launch/recovery experiment (C25). Both allowed runs failed in the first case: cleanup rejected a full configuration mismatch. The first repair tried an empty-PortBindings hypothesis, which was insufficient. The second retained before/after inspection pair showed a single difference, `HostConfig.OomKillDisable` false before start and null after. Zero of six lifecycle cases were accepted; the two-run allowance closed; both fixtures were removed by exact receipt. The pinned Moby 27.3.1 source files were fetched from raw.githubusercontent.com at 03:37Z with hashes recorded, which is network use during a window otherwise described as offline. An execution contract v1 was written.

The identity sub-step (C26) resolved that offline: 101 research cases (first run 93/1 because a negative fixture had assigned an unchanged value), then a fresh engine batch that passed one identity and six lifecycle cases on first invocation; seven containers created and confirmed absent.

The isolated launch runtime prototype (C27) is the messiest slice and the manifest is candid about it. Focused offline run 1 was 39/1 (a test misusing the journal API). Real-engine run 1 was 3/1 because the relaunch-denial assertion expected `ValueError` but got `LedgerAppendFailure`. Run 2 was 3/1 because the original stopped-create reply never arrived; the underlying exception was not retained and timeout remains a hypothesis. The runner lacked fail-fast and executed three more cases after the unreceipted create. Eight creates produced seven client receipts; the eighth container was found never-started and removed under an explicit one-off operator exception. Then the combined check run failed on a stale schema-11 assertion (`test_existing_binding_survives_mode_migration`, 747 passed / 1 failed / 8 skipped on disk), an edit guard refused a two-occurrence edit, an unchanged check run started and was cancelled (checks-02 on disk shows tests `cancelled`), and checks-03 passed with 861 passed and 8 skipped. Those 8 skips are the four parametrized cases in `test_resource_engine.py` and four in `test_launch_engine.py`, which skip whenever the `ADRL_RESOURCE_*` environment is unset.

The transport-receipts slice (C28) split preparation from active execution (policy v2), reproduced the lost-reply mechanism offline (a 2.25s reply fails a 2s budget), and passed fresh engine stages: offline 887 passed / 8 skipped, then combined engine run 895 passed / 0 skipped at 05:43Z. Thirteen creates, thirteen receipts, thirteen absence confirmations. The historical cause of the lost create reply is still recorded as unknown. The active-copy custody packet (C29) was prepared but never entered.

### 8 September, 11:31 to 14:15: deck, demonstration, planning, lab, correction

The executive deck (C30) was built between 11:31 and 11:39 in a scratch directory the snapshot excludes (`.codex-executive-build`): a journey summary refresh at 06:05:45Z, two pptx finalization passes (first-final, then v2) and a content review at 06:09:22Z claiming 895 tests and 18 pilot events. The journey has no numbered entry for this work; entry 015 later says the deck "blurred" the routing versus infrastructure distinction.

The routing demonstration (C31) ran from 06:19Z to 06:30Z: 240 decisions, two review hypotheses failed (rename-redesign and explain-implement both routed local), 135 targeted tests, rule-health demotion demonstrated with 20 invented outcomes in a temporary ledger. The report says the first driver invocation failed for a missing event-schema argument; no log of that failed invocation is retained. At 06:29:47Z the heartbeat was paused and the state switched to planning-only, with W3.2b2e recorded as deferred (C32). The roadmap gained an amendment section moving W7.0 ahead of W3 completion.

Planning then ran for about two hours: the RSI blueprint and 77-decision taxonomy map (validated 06:40Z), the startup product roadmap, investment brief and context-graph proposal (backup 07:18Z; validation attempt 1 failed at 07:36Z on two dangling links to a validation file not yet written, passed at 07:37Z), and the experiment lab plan (validated 08:05Z). The product roadmap validation also recomputed the illustrative economics, which show a negative net saving at 25% coverage.

Lab A.1 (C36) restarted implementation as a bounded foreground slice at 08:18Z. Four runtime files were added. Run 1 at 08:23:30Z executed all 16 cells but its manifest used the key `source` both for the file-hash map and for the provenance string, so the hash map was overwritten; I confirmed the run-1 manifest is 6.4KB with no `source_manifest` while run-2 is 61KB with 320 hashes. Run 1 is retained and disqualified; run 2 at 08:24:09Z is the accepted export. Checks: 894 passed / 8 skipped on 320 inputs.

W7.0a (C37 to C39) froze a contract at 08:36:57Z. Candidate 1 changed features.py, app.py, docs and one new test file; its matrix ran at 08:39Z and its full checks failed at 08:40:55Z with 910 passed / 1 failed / 8 skipped. The failing test is the sticky-cascade case: after escalation to cheap cloud, "Now fix the second typo" was routed frontier instead of staying at cheap cloud. The candidate also over-routed "add a flag". I hashed the five candidate-1 files and they equal the checks-1 manifest exactly; three of the five differ from the final. The final version adds ordinal qualifiers and small-edit span overlap logic, passed 159 focused tests and 911 / 8 with all eleven checks at 08:43Z, and was validated at 08:45:32Z. The 322 `source_after` hashes in the final check manifest match the frozen runtime file for file.

### 8 September, 14:15 to 16:26: planning packs and handoff

After the correction, ADRL-NOW and the correction report were written (C40), the lab planning-and-assessment design was added without any validation record (C41), and three planning task packs plus a delivery packet were prepared and validated at 10:35:54Z on metadata only (C42). Journey entry 021 and the execution state (updated 10:36:28Z) followed (C43). The handoff set (review prompt, evidence-map README, dispositions, two paid Claude smoke calls to review the new skill, and the 691-entry inventory at 10:48:41Z) closed the window (C44). The snapshot was frozen at 10:56:20Z.

## 3. Counts reconciled

| Claim | Backing artifact | Source hashes versus frozen snapshot |
|---|---|---|
| 911 tests passed, 8 skipped | `routing-correction-2026-09-08/checks-final/tests.log` ("911 passed, 8 skipped in 57.59s"); identical on disk at `routing-fix-20260908T083657Z/checks-final` | The manifest's 322 `source_after` hashes match the frozen runtime 322 of 322; manifest sha `a1b576e7...` matches the execution-state pointer |
| 8 skipped engine tests | Four `fault` parametrizations in `tests/integration/test_resource_engine.py` and four in `test_launch_engine.py`, skipped when `ADRL_RESOURCE_*` env is unset | n/a; last engine run with 0 skips was 05:43Z (895 passed) |
| 11 checks | `checks-final/manifest.json` lists lint, format, types, tests, ledger, config, inventory, learning, api_contract, adr_map, register_index, all passed | same manifest |
| 322 runtime inputs | `source_scope` = src, tests, tools, config, docs, api, artifacts plus six root files; `source_before == source_after`, no changed inputs | 322 / 322 match |
| 720 synthetic decisions | `before.json` (original 24x5x2 = 240 plus fresh 12x5x2 = 120) and `after-final.json` (same) = 720. `after.json` (candidate 1) is a third 360 not counted | Ordinary counts: before local 9 / frontier 15; final local 8 / frontier 16 |
| 240 demonstration decisions | `routing-demonstration-2026-09-08/results.json` `stress_matrix.decision_evaluations = 240`, 2 review hypothesis failures, 0 invariant failures | `runtime-baseline.json`: 316 inputs, 0 mismatches versus transport-receipts manifest |
| 895 / 0 skipped | on disk `w3-receipt-20260908T052217Z/checks-engine-01/tests.log` "895 passed" | 313 / 316 match frozen (three files later changed by W7.0a) |
| Test chain 549, 556, 593, 631, 669, 697, 724, 759, 812, 861, 887, 894, 911 | Each from an on-disk `tests.log` tail (see ledger rows C15 to C39) | Older manifests match the frozen runtime for all files not touched by later slices (268/280 for W0 up to 317/320 for the lab) |
| Pre-W0 chain 463, 506, 511, 532, 549 | Manifest junit blocks (463, 506, 511, 549); 532 only from report text | Not comparable to frozen state; verified only via manifest before/after hashes |

Everything in the table was read from the artifacts named; I did not run any tests or tools.

## 4. Failed candidates, repair cycles, disqualified runs and abandoned approaches

1. Live pilot native fix (7 Sep): passed 4 tests, rejected by compatibility review; repaired in a second session.
2. Product foundation: import cycle masked by import order; two sandbox-permission environment failures on the first run.
3. Services: credential pass-through and writer cancellation defects found and fixed inside the slice.
4. Improvement experiment: exit code 2 versus 1 confusion fixed.
5. W0: first automation create rejected; ADR-map regex false negative.
6. W3.2a: documentation patch rejected atomically once.
7. W3.2b1: cancellable cleanup Task replaced after self-review; detached child limitation accepted.
8. W3.2b2a: 62/4 focused run, fixtures corrected.
9. W3.2b2b1: pre-change probe reproduced key resurrection; slice split out as a prerequisite repair.
10. W3.2b2b2: three repair cycles; one unretained console-only diagnostic; one rejected backup attempt.
11. W3.2b2c: Docker run 1 failed on an unsupported CLI flag; compiler timeout corrected post-run.
12. W3.2b2d2 launch experiment: two runs failed; PortBindings hypothesis abandoned; zero of six accepted; approach changed to an offline comparator.
13. Execution identity: offline first run 93/1.
14. Isolated launch: focused 39/1; engine run 1 wrong exception class; engine run 2 lost create reply with unretained cause; runner lacked fail-fast; operator cleanup exception; checks-01 failed on stale schema-11 assertion; checks-02 cancelled.
15. Executive deck: two finalization passes (first-final then v2).
16. Routing demonstration: first driver invocation failed (asserted, no log).
17. Product roadmap validation attempt 1 failed on two dangling links.
18. Lab A.1 run 1 disqualified (source key collision).
19. W7.0a candidate 1 failed the sticky-cascade test and over-routed "add a flag".
20. Never started: W8A Responses spike, W3.2b2e active-copy custody, all three planning packs.

## 5. Work omitted from the author's evidence map, and other discoveries

- The execution state's `latest_evidence` list starts at W0. None of the eleven 7 September pre-W0 manifests, patches or validations appear there, although the handoff README does point to their reports.
- The executive deck build scratch (`.codex-executive-build`) with its content review, two finalization validations, sources.json and a journey-before copy is outside the snapshot and outside the inventory scope; it is the only record of when the deck was built.
- The `w3-2b2b2-20260908T002159Z` backup directory exists on disk but is absent from the manifest's 35 backup paths.
- The w3-launch `checks-01` (failed) and `checks-02` (cancelled) manifests are referenced only inside the slice manifest's `combined_attempts`; the journey mentions them in prose.
- `design/adrl-lab-planning-and-assessment-2026-09-08.md` and `reports/ADRL-NOW.md` are covered by no validation record.
- The skill smoke review and recheck were two paid `claude-fable-5-1` calls ($0.312 and $0.288 list-price usage metadata). Every register validation reports `model_calls: 0`, which is true of the ADRL runtime but not of the window as a whole. The launch-contract slice also fetched Moby source over the network.
- The pre-window register baseline is only partly knowable: 26 ADR files (EVL, OPS, TRU, CAS-009, SEM-007) and the 3 September reports are untracked, so the 2 September commit does not represent the state at the start of 7 September.

## 6. Changes after the inventory timestamp 2026-09-08T10:48:41Z

The freeze at 10:56:20Z compared 695 files: 691 matched the inventory, 0 mismatched, 0 missing. The four extras were the inventory manifest itself (written at the inventory instant, so post-inventory by construction), runtime `.python-version`, and the two dev signing `.key` files, which were hashed but not copied. I found nothing in the snapshot that postdates 10:48:41Z. Within the window's last hour, hash comparison against the 08:45:32Z validation shows exactly seven register documents were edited afterwards: LRN and RTG bucket READMEs, INDEX, CHANGELOG, the journey, the product roadmap and the lab plan, plus the new planning-pack, packet, design, NOW and handoff files. The execution state itself is not hashed by any author validation. The on-disk git status at review time is identical to the status recorded in the inventory.

## 7. Open questions and missing evidence

- No artifact dates the research review, course-correction plan, product contract, improvement proposal, register sync or roadmap to the hour; only ordering is established.
- The 532-test figure for session verification appears only in report text; the manifest's pytest output was not fully inspected by me.
- The failed first routing-demonstration invocation and the W3.2b2b2 console-only diagnostic have no retained log.
- The historical cause of the lost stopped-create reply in the isolated launch slice is unknown by the author's own record.
- The Claude session traces for the live pilot are not in the snapshot; costs and model identities are harness-reported.
- The hourly automation object and its run history are not in the snapshot; cadence is inferred from backup directory names.
- The 320 to 322 input growth and the 316 to 320 growth are explained (four lab files, two W7.0a files), but the frozen `.python-version` and dev keys are outside every declared source scope.
- Whether the executive deck's slide text matches evidence was reviewed by the author only; I did not open the pptx.
- The three `.codex-executive-build` planning backups are not hashed by the inventory.

## 8. Files opened versus skimmed

Opened in full or in the relevant section (register paths relative to snapshot/register unless noted): reports/adrl-implementation-journey.md; reports/research/adrl-execution-state.json; reports/research/routing-correction-2026-09-08/{validation.json, contract.md, route-changes-final.md, checks-final/manifest.json, checks-final/tests.log (tail), checks-1/tests.log, checks-1/manifest.json, after.log, lab-after.log, lab-final.log}; candidate-1/src/adrl/routing/features.py (diffed against runtime); before.json, after.json, after-final.json (counts); reports/research/routing-demonstration-2026-09-08/{results.json (structure), run.log, targeted-tests.log, runtime-baseline.json, validation.json}; reports/research/routing-lab-2026-09-08/{validation.json, run-1/manifest.json, run-2/manifest.json, run-1/QUALIFICATION.md, run-2/report.md, focused-1.log, focused-2.log, run-1.log}; all thirteen W0/W3 manifests (scalar fields and hash sets); all sixteen 7 September research JSON files listed in the ledger; reports/research/adaptive-routing-blueprint-2026-09-08/{validation.json, sources.json}; product-roadmap-2026-09-08/{validation.json, validation-attempt-1.json}; experiment-lab-planning-2026-09-08/validation.json; independent-review-handoff-2026-09-08/{manifest.json (structure), README.md, skill-dispositions.md, skill-recheck.md, skill-recheck.json, skill-smoke-review.md, skill-smoke-review.json, skill-smoke-metadata.json}; reports/lab/planning-starter-v1/{manifest.json, validation.json, tasks.json}; reports/research/dataset-validator-pilot-fix-2026-09-07.patch; CHANGELOG.md (all 7 and 8 September entries); REVIEW-LOG.md (tail); AGENTS.md (both repositories, head); runtime/docs/{engineering-checks.md, routing-lab.md, routing-features.md}; runtime/tests/integration/test_resource_engine.py and test_launch_engine.py (skip and parametrize lines); inputs.json and coverage.csv of the review directory; on disk: every `tests.log` tail and manifest status under `.adrl-execution-state`, w3-launch engine-focused logs, w3-2b2c and w3-2b2d2 probe results, `.codex-executive-build/{content-review.json, journey-summary-update.json, validation-v2.json, validation.json, sources.json (head)}`, routing-review-backup state checkpoint, `.project/telemetry/*.jsonl`, git log and diff --stat of both originals.

Skimmed (head or headings only): reports/adrl-independent-research-review-2026-09-07.md; adrl-course-correction-plan-2026-09-07.md; adrl-adaptive-improvement-proposal-2026-09-07.md; adrl-claude-subscription-pilot-2026-09-07.md; adrl-register-sync-2026-09-07.md; adrl-product-foundation-implementation-2026-09-07.md; adrl-product-services-implementation-2026-09-07.md; adrl-session-verification-2026-09-07.md; adrl-live-observation-pilot-2026-09-07.md; adrl-improvement-experiment-2026-09-07.md; adrl-implementation-roadmap-2026-09-07.md; adrl-product-roadmap-2026-09-08.md; adrl-adaptive-routing-rsi-blueprint-2026-09-08.md; adrl-executive-review-2026-09-08.md; adrl-startup-investment-brief-2026-09-08.md; adrl-independent-review-prompt-2026-09-08.md; ADRL-NOW.md; adrl-lab-first-run-2026-09-08.md; adrl-routing-in-action-2026-09-08.md; adrl-routing-correction-2026-09-08.md; all five design/*.md; waves/{w0-baseline, w3-task-capture, w8a-state-transport-spike, routing-decision-quality, lab-a-routing-experiment, lab-planning-deliverables, w3-active-copy-custody, w3-2b2d-resource-ownership}.md; the seventeen patches (file lists and line counts only); reports/research/adrl-roadmap-plan-2026-09-07.json; writer-boundary README; the three SKILL.md heads. Not opened: the W3 plain-language reports beyond their manifests, the remaining wave packets, ADR bodies (only date-mention counts), the pptx and PDF outputs, preview.html, events.jsonl, taxonomy-map.*, sources of the research review.
