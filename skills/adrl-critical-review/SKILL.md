---
name: adrl-critical-review
description: Coordinate independent Codex and Claude review of ADRL wave plans, implementation evidence, roadmap alignment and taxonomy maturity. Apply before substantive ADRL waves and before claiming completion, as well as explicit retrospective reviews.
---

# ADRL critical review

The product owner wants Codex and Claude to challenge each other throughout implementation. Codex normally owns implementation and evidence; Claude Fable 5.1 independently reviews. This is a development review process, not ADRL runtime RSI, formal human graduation, or proof of customer value.

## Ledger contract

Before publishing review artifacts or claiming findings resolved, use `adrl-review-ledger`
(`/Users/arunmenon/projects/adrl-world-class/skills/adrl-review-ledger/SKILL.md`). Its fixed
schema and append-only history rules govern storage. Initial findings/dispositions are immutable;
subsequent responses and rechecks are new records. Keep exact source snapshots outside the
review ledger and include retrieval references/hashes. Never overwrite a registered legacy folder.

## Establish the checkpoint

Read both repositories' instructions, current execution state, product roadmap, journey and owning ADRs. Register: `/Users/arunmenon/projects/adrl-world-class`; runtime: sibling `adrl-core`. Reconcile newer overlays and stale claims. Never hardcode test counts, stages or maturity in this skill.

Use three scopes:
- **Pre-wave:** challenge proposed behavior, roadmap value, owning decisions, assumptions, minimum scope, alternatives, acceptance evidence, permissions and stop conditions before substantive implementation.
- **Post-wave:** independently inspect frozen source and raw evidence before a completion claim. Include failed candidates and source hashes. Review regressions and scope of maturity claims.
- **Retrospective/milestone:** review the whole product roadmap and all ADRs. For the 7–8 September review use the existing full prompt in `reports/adrl-independent-review-prompt-2026-09-08.md` and its companion inventory. Future reviews generate fresh inventories and time windows.

Do not request another full audit for trivial wording edits. Scope routine wave review to changed behavior and dependencies, expanding if evidence reveals broader risk.

## Independent handoff

Read [references/handoff.md](references/handoff.md) for packet and invocation details. Give Claude the user intent, raw artifacts, baseline, frozen scope and required outputs. Provide author claims as hypotheses, not the expected verdict. Keep the first review independent of the implementer's proposed rebuttal. The reviewer does not edit the implementation or grade its own repairs.

Invoke the actual Claude tool/CLI, not a Codex subagent relabeled Claude. Pin the user-requested model and retain returned model/session metadata. No silent fallback if unavailable. Use existing authorized subscription access; do not switch to separately billed APIs. Keep secrets and unrelated files out of context. The user has authorized this ADRL reviewer collaboration, not unrestricted experiment execution or spending.

Use read-only tools and fresh review outputs. Exclude shell/write tools from unattended reviewer invocation unless a bounded isolated validation specifically requires and permits them. Capture response externally through the coordinator. Inspect local hooks/settings/tool exposure before source-bearing invocations; never bypass permissions. Read-only tool policy is not a filesystem sandbox. Limit the accessible snapshot and record incomplete coverage.

## Reconcile without rubber-stamping

Codex is the named coordinator and records packet provenance. Give the reviewer the complete relevant declared source snapshot, including dirty and untracked files, plus an exclusions manifest; the reviewer can challenge scope and request omitted relevant evidence. Freeze a copied snapshot with a complete hash manifest and compare hashes before/after review; a commit is optional and cannot substitute for uncommitted contents.

Persist the original review before responding. Reviewer severity and original text are immutable history. Codex cannot remove a block by downgrading severity. A reviewer may revise its assessment with evidence; unresolved contested blocking findings require an explicit product-owner disposition. For each finding record stable ID, severity, confidence, source/evidence, owning ADR, product consequence and disposition: accepted, fixed-awaiting-recheck, verified-fixed, deferred-with-reason, disputed-with-evidence, or unresolved. Preserve both positions. A reviewer recommendation is not automatically a correct finding.

Codex reproduces accepted issues and fixes them only within the authorized wave. Claude rechecks material fixes against the new snapshot and relevant regressions. Normally allow one initial review and at most two correction/review rounds per wave, constrained by any tighter existing run/repair limit. Stop churn; report unresolved disagreements to the product owner with evidence and a concrete decision. Do not endlessly optimize to the reviewer's wording.

Unresolved critical/high findings affecting privacy, correctness, evidence integrity or the wave's acceptance criterion block the affected completion/exposure claim. Nonblocking findings may be explicitly deferred with owner and gate. Reviewer unavailability means `unavailable`, not passed or waived; continue independent preparation within existing authority. Do not silently advance the gated wave. A user can explicitly override the process with the limitation recorded.

## Close the loop into the register

After reconciliation, update the owning ADRs, INDEX, overviews and CHANGELOG when behavior/evidence warrants it, following repository rules. Record review disposition and links in the journey/current state and review log. Distinguish acceptance, implemented behavior, tested scope and formal maturity. No automatic D-grade promotion, release or policy admission from model agreement.

Each wave packet and completion report should expose: pre-review state, frozen input identity, reviewer identity, findings/dispositions, post-review state, evidence limits, and next product gate. Use statuses `not-started`, `in-review`, `changes-requested`, `awaiting-recheck`, `reviewed-with-open-items`, `reviewed`, or `unavailable`; `reviewed` never means formal graduation. Updates after the reviewed snapshot invalidate the affected acceptance evidence and require proportionate recheck.

Report plainly: what Codex built, what Claude challenged, what changed because of review, what remains disputed, and what this proves for adaptive routing. Do not claim the skill is an enforced CI control, an autonomous scheduler, or an already completed review.
