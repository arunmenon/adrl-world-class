# ADRL wave execution packet

Template v1, 7 September 2026. This is a planning/checklist artifact, not an executable approval or deployment system. Use it for one wave or one bounded slice of the [roadmap](adrl-implementation-roadmap-2026-09-07.md).

## Identity, scope and authority

| Field | Fill before execution |
|---|---|
| Packet ID and parent wave | Stable ID, version, predecessor packet |
| Engineering state | proposed / ready / implementing / validated / closed |
| Disposition | advance / repeat / narrow / amend / defer / stop; separate from engineering state |
| Outcome in user language | One behavior a user can now rely on |
| Owner / reviewer | Named implementation owner, evidence reviewer and relevant security/release authority |
| Existing authorization | Link the instruction or decision that authorizes the work; do not ask again for the same authority |
| Scope tuple | Harness/version, profile/version, transport, deployment, repository class, integration mode, task family |
| Current and target maturity | Per ADR behavior, exact versions and population; current evidence, missing gates and required reviewer. Target is not a promotion |
| Runtime exposure | offline / observation / shadow / constrained live; never infer live approval from code completion |
| Owning decisions | Exact ADR IDs, clauses and any proposed amendment |
| Dependencies | Evidence records for prerequisite gates; missing data stays missing |
| Explicit exclusions | Unsupported states, untested populations and data not permitted to leave the machine |

## Problem and falsifiable hypothesis

State the problem, a concrete example, current behavior and desired behavior. Name what observation would make us reject the proposed change. Classify the question as implementation defect, parameter choice, architecture assumption, compatibility, measurement or product scope.

Record any decision conflict before coding around it. If no existing ADR owns the behavior, propose ownership rather than inventing a hidden contract. Keep routine restoration of an existing invariant distinct from changing that invariant.

## Inputs frozen before the comparison

- Source snapshot/commit and dirty-worktree manifest; dependency, environment and configuration versions.
- Native harness/protocol/provider versions and approved credentials, recorded without exposing secrets.
- Initial task state, task/attempt lineage, output-capture boundary and verifier plan/artifact hashes.
- Evidence origin, verification quality, eligibility and permitted storage/access/retention.
- Development, selection and fresh assessment partitions; related-task grouping and holdout access owner.
- Baseline/candidate identities, primary outcome, minimum worthwhile gain or allowed quality loss.
- Analysis, uncertainty method, stopping rule, minimum exposure and treatment of multiple candidates/interim looks.

Expected outcomes must be set independently of the candidate where independence is claimed. Freeze numeric thresholds before release assessment; any later change creates a new evaluation version and fresh assessment requirement. A curated fixture may validate mechanics without qualifying an efficacy claim.

## Deliverables and bounded execution

List the smallest implementation slices and their expected files or contracts. Include contract compatibility, migrations, data inventory, documentation and diagnostics in scope where needed. Every module in `adrl-core` names its primary ADR.

| Limit | Approved value / measurement |
|---|---|
| Task attempts / repair attempts | Explicit cap, including the stop behavior |
| Model calls / tokens / turns | Cap across arms, repetitions and in-flight work |
| Dollar ceiling | Explicit approved amount for paid usage; null means not established, never unlimited |
| Runtime / per-command timeout | Include cancellation behavior and in-flight ambiguity |
| Snapshot / evidence storage | File/byte limits, retention and cleanup |
| Concurrency | Maximum simultaneous tasks and budget reservations |
| Allowed actions and destinations | Tools, files, repositories and provider destinations permitted by the packet |

For an offline-only coding packet, state that no model-service calls or new infrastructure are included. If exact billing enforcement is unavailable, state the conservative alternative limits and residual uncertainty. Record costs for failed and discarded candidates.

## Acceptance, fault cases and advancement

For each promised behavior, specify an observable case, expected result, artifact and owner. Include negative cases, restart, cancellation, malformed/missing inputs, credential/identity boundaries, ledger/key failure and erasure where applicable.

| Gate | Frozen threshold or expected behavior | Evidence link | Outcome |
|---|---|---|---|
| Entry prerequisites | Actual prerequisite evidence | | not assessed |
| Functional conformance | Named cases and expected results | | not assessed |
| Critical invariants | No forbidden dispatch/authority leak/duplicate effect/erasure resurrection in required cases | | not assessed |
| Outcome quality | False accept/reject, uncertainty and repair metrics; declared population | | not assessed |
| Reliability / budget | All-attempt denominator, limits and failure accounting | | not assessed |
| Rollback / recovery | Measured recovery within stated target, preserving restrictions | | not assessed |
| Register and compatibility | Owning ADRs/index/buckets/changelog, schema and client compatibility | | not assessed |
| Release / maturity authority | Separate human decision and signature where required | | not assessed |

Use passed, failed, insufficient, not assessed or explicitly scoped not applicable. “Not applicable” needs a reason tied to a removed claim; it cannot waive a critical invariant of an advertised feature. Passing a development gate grants no new deployment authority.

## Required implementation checks

Run from `adrl-core` in its recorded environment:

```bash
.venv/bin/python -m ruff check src tests tools
.venv/bin/python -m ruff format --check src tests tools
.venv/bin/python -m mypy
.venv/bin/python -m pytest -q
.venv/bin/python tools/check_ledger_discipline.py
.venv/bin/python -m adrl.cli.main config check
```

Also run data inventory, learning-contract, contract-export compatibility and ADR module-map checks when affected. Include the relevant adversarial and real-harness cases before claiming those properties. Publish skipped/unsupported cases and failures. Documentation-only synchronization can rely on unchanged verified source hashes under the repository instructions.

## Stop, rollback and continued work

Name immediate stop triggers, who can stop admission, what happens to in-flight work, the compatible recovery version, and how pins, erasure records and evidence survive rollback. Do not use a direct cloud bypass as recovery from a restriction failure. If safe rollback is unavailable, stop the affected path.

After the agreed attempt limit or a material new contradiction, produce a failure packet. Continue useful independent work within existing authorization, while withholding the dependent exposure. A failed hypothesis can close a packet honestly; it must not be turned into a passed gate.

## Closure and decision-ledger update

Record the actual result versus the original hypothesis, all attempts and exclusions, costs, checks, artifact hashes, disagreements and remaining risks. Choose keep, tune, amend, replace or defer, explaining why. Preserve prior ADR wording and stable IDs; synchronize the index, bucket overviews, changelog and support matrix. Verify links and applied source hashes.

End with a user-facing account: what changed, what was proven, what remains unproved, whether maturity or deployment authority changed, and the next concrete action. Capture the reviewer/release decision separately from the implementation author's recommendation.

## Required taxonomy-sync closure receipt

Use the repo-owned `adrl-taxonomy-sync` skill. Capture the before-edit baseline; map changed
inputs to ADRs; add dated evidence links to the ADRs, INDEX rows, affected bucket rows and
CHANGELOG. Supply pinned evidence and the independent semantic review, then run the
register's `tools/check_taxonomy_sync.py check`. Record the receipt path/hash here.
Missing/failed/stale receipt means synchronization incomplete, not implementation complete.
A passing receipt is scoped mechanical evidence plus reviewer attestations, never automatic
maturity or a substitute for runtime validation.
