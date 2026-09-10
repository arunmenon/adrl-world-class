# Handoff: ADRL review session (Claude Fable 5.1)

Written 2026-09-08 IST during the 7 to 8 September retrospective review. Claude Code session ID: `session_011qFLwZ3EjPPrB3QqneJa63` (https://claude.ai/code/session_011qFLwZ3EjPPrB3QqneJa63). Model requested and self-reported: `claude-fable-5-1`; self-description is provenance, not attestation. No credentials or secrets appear in this file; secret-category files (keys, keystores, .env) were hashed but never read or copied.

Section 3 is refreshed at the end of the review; if it still says "in progress", the appendices under `appendix/` and `status.json` are the current truth.

## 1. Product intent, preferences and constraints (the user's, in their words where possible)

Intent
- ADRL is a transparent control layer between a coding harness and a model gateway that chooses a capability rung (local, cheap cloud, frontier) per user turn with a one-way privacy pin, deterministic escalation and an append-only evidence ledger. The user wants to "reposition ADRL as a product offering we can leverage across teams within the company", "something which can be hooked into any of these harnesses", starting with Claude Code and then another harness.
- The user's standing concern: "are all these decisions grounded on latest / cutting bleeding edge research". They asked for research-backed for and against critiques, not agreement.
- The central review question the user set for 7 to 8 September (via the prompt file): are we building a useful, context-aware adaptive routing product, or accumulating infrastructure and documents without proving better routing and customer value.
- Three improvements must stay distinct: an engineer or agent changes a rule; an offline learner derives a better checkpoint; RSI improves the process that creates checkpoints. None proves the next. A manual repair is not RSI.

Preferences and working constraints
- Never use em dashes in anything written. No adjectives in file names. Descriptive names. No mock implementations (real code or a TODO naming the owning ADR).
- Commit only when asked. Both repositories are deliberately uncommitted; preserve uncommitted work. In adrl-core, private keys are gitignored, but do not `git add .` without looking. In the register keep `.project/telemetry` and `_to_delete/` out.
- Build-then-validate: the user wants independent review before any completion claim, and wanted defects reproduced, not asserted. The operating model in the register's AGENTS.md: Codex implements and records evidence, Claude Fable 5.1 reviews independently, dispositions are recorded, reviewer absence is pending, never approval.
- This retrospective must not implement fixes, promote maturity, run paid model calls, mutate engines or containers, restart the paused hourly automation, or touch either repository. Outputs go to `/Users/arunmenon/projects/adrl-review-fable-2026-09-08/`.
- Model and effort: the user pinned Fable 5.1 at high effort for all sessions.

## 2. Decisions agreed, rejected alternatives and why

User decisions (explicit)
- 2026-09-02: build a brand-new Python implementation of the reviewed register rather than extend `~/projects/adrl`. Location: new sibling repo `~/projects/adrl-core`. Scope: all five phases in one run. Rejected: building inside `adrl-world-class/impl/` (mixes review artefacts with source) and replacing `~/projects/adrl` in place (superseded structure would linger).
- 2026-09-03: after an external review confirmed three P0 control failures, the user chose "code fixes and register drafts", rejecting code-only (leaves the register describing rung labels) and register-only (leaves the leak in place).
- 2026-09-03: produce two deliverables, a technical product report and a research critique of every ADR, published as pages and saved under `reports/`.
- 2026-09-07 (recorded by Codex in `reports/research/adrl-execution-state.json`, not witnessed in this session): the user requested triggering the waves, a running journey report and unattended execution adhering to the plan. Automation is now paused.
- 2026-09-08: run this full retrospective via `/adrl-critical-review` with the existing prompt and inventory, review both repositories, roadmap alignment and all 77 ADRs, produce findings without fixes or promotion.

My recommendations that the user has not yet dispositioned (not decisions)
- Register additions of 2026-09-03, all Proposed and pending the owner's disposition: TRU bucket (TRU-001 authenticated workload identity, TRU-002 permitted deployment set, TRU-003 egress anchoring), SEM-007 protocol profiles, CAS-009 action-effect provenance, first captures of EVL-001 to 009 and OPS-001 to 008, in-place amendments to FND-002, RTG-001, RTG-007, CAS-003, MEM-005, MEM-010, and SAF-008/009 marked superseded pending disposition. Register total 77.
- Stack choices in `adrl-world-class/design/implementation-stack.md`: Starlette plus httpx rather than FastAPI (FastAPI's route validation would re-serialise bodies and break the byte-exact frontier path); stdlib sqlite3 event store with one writer thread rather than an ORM (an ORM hides UPDATE and the register forbids it); detect-secrets (same library LiteLLM uses, so the ruleset diff is a config comparison); one package per ADR bucket.
- A documented carve-out from the byte-exact rule: after an escalation whose source turn carried no thinking blocks, the thinking parameter is stripped from frontier-bound requests until the next user turn. This needs a register amendment (FND-001 or CAS-004); it is recorded in adrl-core `AGENTS.md`, `README.md` and `docs/known-gaps.md`.
- Product surface: four integration depths (L0 passthrough with egress accounting, L1 gated passthrough, L2 routed, L3 routed with hooks); Codex requires a Responses-API profile before anything beyond the Claude family; Cursor, Kiro and vendor-hosted agents cannot be gatewayed and are hook-fed only.

## 3. Findings, evidence paths and unresolved disagreements

Status of this section: COMPLETE. The review is written: `review.md` (main report), `findings.md` (40 findings, stable IDs RV-01 to RV-40), `dispositions.md` (all rows `unresolved`, awaiting Codex), `changes.csv` (48 items), `roadmap.csv` (42 rows), `adr-maturity.csv` (77 rows), `coverage.csv` (695 files), `review-manifest.json`, and seven inspection appendices under `appendix/`.

Verdict in one paragraph: ADRL is a well-instrumented control layer with a keyword router in front of it and a learning stack behind a broken pipe. The evidence discipline is the asset. The two days advanced process more than routing; roughly half the engineering went into a container backend no product stage needs.

Headline findings (my findings, not user decisions):
- RV-01 critical: cascade writes outcome events typed by state; every consumer reads `event_type == "outcome"`; no organic decision can become a label (`C/src/adrl/cascade/controller.py:278,320,361,637` versus `ledger/outcomes.py:81`, `labels.py:145`, `readiness.py:60`, `learning/tiers.py:342`). Confirmed statically by me and by an offline drive.
- RV-02 high: in the ambiguous band `_advise` discards the estimator selection when no classifier exists (`routing/router.py:220-244`); cheap cloud chosen on merit in 0 of 720 decisions.
- RV-03, RV-04 high: lab evidence and the 911-test result are bound to the author's absolute path via the workload assertion and dev manifest; the lab reaches live dispatch through a shadow-mode bundle load not disclosed in reports.
- RV-10, RV-30 high: the isolated backend cannot host a real harness; the next stated W3 step does not lead to a real-task demonstration; a narrower safe path exists (native observation plus W3.1 capture plus snapshot verifier).
- RV-12, RV-13 high: historical D3/D4 grades displayed as current for 13 to 16 ADRs; no independent reviewer named across 21 journey entries, so every "validated" is self-review.
- RV-15, RV-16 high: the improvement experiment and routing-correction summaries overstate what their bodies concede.

Found sound: all evidence hash chains, all test counts to logs, failed candidates retained, guardrail flags false with code proof, heartbeat paused, skill copies identical, the 7 September research corrections survive re-fetching.

Unresolved disagreements: all 40 findings await Codex's response; the strategic disagreements (lexical over-routing without a budget, destructive vocabulary as capability signal, path-bound dev config as product config, adapter abstraction ahead of evidence, learning built ahead of the pipe, diversity from author prompts) are recorded as such. Carried from before: 22 Proposed register items and 17 contested ADRs undispositioned; the Handoff Tax versus RTG-004/CAS-004/CAS-005 disagreement.
## 4. Context from this conversation not captured in the repositories

- The 2026-09-02 build was done by this session with five parallel package builders against a shared stage contract, an integration pass, an independent conformance review that found a critical leak (pin write failure forwarded a secret to the cloud), and ten fixes re-verified. The reviewer and fix agents were Claude subagents, not Codex. The user was not watching in real time; approvals were given through explicit questions.
- Two published pages exist: product report https://claude.ai/code/artifact/5b4f62b4-4899-4254-b1ae-e377c62b066e and research critique https://claude.ai/code/artifact/cb4057aa-2d94-460b-a0ef-7e93579a04ba (private unless shared).
- Memory files for future sessions live at `~/.claude/projects/-Users-arunmenon-projects-adrl-world-class/memory/` (`adrl-repo-context.md`, `adrl-core-build.md`, `adrl-product-positioning.md`).
- `~/projects/adrl` is the older Python implementation (last commit around 2026-07-14) that the 2 September review referred to as `cc-local`; it is the source of the scrubbed handshake fixtures and utility fingerprints.
- On 2026-09-07 the user stopped 13 background agents from earlier phases; nothing of theirs was pending. Two other Claude sessions sent connectivity greetings only.
- Codex's 7 to 8 September waves ran outside this session; this review's only knowledge of them is the frozen evidence. The critical-review skill and the register AGENTS checkpoint were added during handoff preparation and are not evidence that earlier waves were reviewed.
- Codex's skill smoke test (`skill-smoke-review.md`, `skill-recheck.md`) is Claude's evaluation of the review instructions, not a repository review.

## 5. Current work status and exact next action

Status: `changes-requested` (see `status.json`): review complete, 40 findings outstanding, blocking findings listed in the manifest. Zero drift between freeze and close. No repository file was modified; no maturity promoted; no scheduler, engine, container, paid call or real payload touched.

Exact next action for whoever continues:
1. Product owner reads `review.md` sections 1, 5 and 8, then decides: (a) whether to accept the three proposed slices in that order, (b) how to treat the twenty-one self-assigned "validated" labels retroactively, (c) the disposition of the closed W3.2b2d2 slice with its recorded stop-rule deviations, (d) authorisation for slice 3 (subscription use for ten runs, a named evaluation reviewer, a named security reviewer).
2. Codex fills `dispositions.md` per finding with evidence; fixes only within an authorised wave; never edits `findings.md`.
3. Fable rechecks material fixes against a NEW frozen snapshot (repeat the freeze script from `inputs.json` provenance), at most two correction rounds, then updates `status.json` to `reviewed-with-open-items` or `reviewed`; `reviewed` never means graduation.
4. Register updates that behaviour or evidence warrant (INDEX rows, maturity fields with scoped adrl-core levels, EVL-007 historical-grade rule applied per decision) follow the register's AGENTS rules and are the implementer's to make, not the reviewer's.
