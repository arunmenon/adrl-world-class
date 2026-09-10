# W0: Establish the execution baseline

Packet `W0-baseline-v1`, 7 September 2026. Parent: [roadmap W0](../adrl-implementation-roadmap-2026-09-07.md).
The user's instruction to trigger the waves authorizes this local engineering work. This packet
does not expand the existing privacy, spending, review or deployment authority.

## Scope and state

- Owner: Codex, implementation and technical self-review. Product owner: Arun Menon.
- Engineering state: validated for local engineering; disposition: advance to offline W3. Reviewer-dependent graduation remains pending.
- Scope: existing local macOS/Python 3.12 build, API preview 4, current configuration and fixtures.
- Runtime exposure: offline only. No model calls, paid usage, installs, commits or deployment.
- Owning ADRs: FND-005, SEM-007, EVL-007/009, OPS-001/003. Existing architectural status and
  maturity fields remain unchanged. The tools support scoped engineering evidence, not graduation.
- Limit: one writer; at most three repair attempts for a failed task; ten minutes per check in
  the repeatable runner; at most three reviewable slices per scheduled run.
- Independent evidence/security reviewers are unassigned. Codex cannot supply an independent
  sign-off on its own work. This holds the corresponding release gate, not local implementation.

## Purpose and evidence contract

We need to know which build a test result describes and avoid carrying obsolete status claims
into later waves. A passing suite without an identifiable source/configuration, or a silently
refreshed contract, would fail this purpose. The six existing repository checks and W0's
inventory/contract/coverage requirements were fixed in the roadmap before work began. This
packet records execution details; it is not a preregistered efficacy experiment.

Before runtime edits, preserve the Git tracked and nonignored untracked regular files in both
repositories in a private directory. Compare each copy's bytes and hash with the original.
Ignored runtime data, credentials, virtual environments and Git internals are excluded; this
is a source recovery snapshot, not a payload backup or whole-machine recovery mechanism.
Never restore over the current working tree wholesale: compare paths, preserve subsequent edits,
and restore only the intended source files. The manifest identifies executable modes separately.

## Deliverables and acceptance

| Deliverable | Required observation | Evidence / state |
|---|---|---|
| Recoverable baseline | Both source copies match original bytes, existing dirty state recorded | Private baseline manifest, summarized in closure record |
| Fresh baseline | Six required checks plus inventory, learning contract and contract comparison pass | Baseline run before tool edits: 549 tests passed |
| Repeatable checks | All checks recorded; failure/timeout/missing register/stale artifact cannot pass | `tools/check_all.py` and focused fault cases |
| Input drift | Changed, added or removed declared inputs prevent a passing combined result | Source manifests and fault test |
| Accurate documentation | API services, observations, unknown-health policy and legacy path described as implemented | README, protocol boundary, known gaps and matrix below |
| Ownership coverage | Every implementation module cites existing ADRs; every register ADR has one index row | Generated map and index check; unmapped decisions remain visible |
| Next wave packet | W3 capture boundary, limits and falsifiable acceptance cases fixed before its code | [W3 packet](w3-task-capture.md) |
| Protocol risk prepared | Bounded Responses state/transport investigation has a packet | [W8A spike packet](w8a-state-transport-spike.md) |
| Register synchronization | Owning records, bucket summaries, index and changelog match evidence | Closure record and link/hash validation |

## Current support matrix

| Surface | Current evidence | Limitation / next wave |
|---|---|---|
| Native Claude Code observation | One existing pilot, 18 tool observations on one repaired task | No ADRL model routing; task-close capture W3, independent outcome quality W4 |
| Messages gateway/profile | Offline fixtures, bound product sessions and fake-gateway tests | No qualified live matrix; controls and destination receipts W6 |
| Local product API preview 4 | Session binding, durable events, idempotency, timeline and decision reads | Same-user/loopback boundary; no remote identity or child binding |
| Operator verification | Temporary separate snapshot, encrypted started/finished receipts | Verifies capture-time tree; retained task-close output W3 |
| Offline improvement experiment | Seven curated cases, repeat comparison and encrypted review-only archive | Same author wrote candidate and cases; no protected holdout or efficacy population |
| OpenCode | No registered adapter or compatibility result | Shared adapter and named real harness version W5 |
| Codex/Responses | Admission design only; no registered profile | State, transport and opaque-item custody spike W8A |
| Learned routing / RSI | Gated artifact machinery and local experiment tools | No automatic authority; policy learning W9, bounded proposals W10, recursive comparison W12 |

Capabilities continue to describe shipped code. An empty tested-harness list for model-profile
validation is compatible with a separately dated observation pilot; observation did not validate
the intercepted model protocol.

## Reconciled blockers and ownership

| Blocker / decision | Actual observation | Next action / accountable owner |
|---|---|---|
| Task output attribution | Verification re-snapshots a current workspace and discards its temporary copy | W3, Codex: retain a scoped capture and then build trusted close attribution |
| DQ3: absent identity | Removing every session signal reaches the legacy path | W6, Codex prepares enforcing-listener fix; Arun dispositions policy scope before exposure |
| DQ3: unknown health | Reader returns unknown; feasibility retains a rung with no reported member state | W6, Codex tests chosen policy; Arun dispositions it |
| DQ3: shadow class ceiling | Ceiling advisory on frontier passthrough; pins/residency remain separate | W6, policy disposition and regression matrix |
| CAS-001 restart consumption | `_verifier_consumed` remains process-local | W6, Codex: persist consumption and fault-test restart |
| OPS-001 multi-process promise | No enforced process-owner lock or complete state inventory established | W6/W8B, Codex: inventory and refuse unsupported concurrency; no D3 claim |
| OPS-003 stale design-only summary | Signed endpoint inventory and local-boundary checks already exist; development identities do not qualify production | W6, verify deployment receipts and real inventory; preserve earlier register wording with dated evidence |
| SAF-007 execution isolation | Allow-default reads, denied network and protected writes; no hostile repository qualification | W3 scoped trusted fixtures; W4/W6 independent security review before broader use |
| Credential expiry / outbox resume | Observation intake exists; automatic renewal/resume is incomplete | W5/W8B, Codex; preserve idempotency and restriction identity |
| Independent outcomes / security review | Reviewer roles not assigned | Arun appoints reviewers before their dependent gates; W4 may prepare cases without claiming independence |
| DQ4 graduation | Generic routing economics do not by themselves qualify an integration feature | Arun dispositions before formal product graduation; no self-authored score promotion |

The complete decision queue remains DQ1-DQ8 in the roadmap. Recording a blocker does not change
its policy. The maturity baseline copies all 77 existing status/maturity fields and mappings;
it is an inventory of claims, not a validation of every claim or a numerical portfolio score.

## Stop, recovery and closure

A changed source baseline, broken contract or failed check prevents closure. Preserve logs and
both source versions, diagnose within the attempt limit, and establish a fresh result after a
fix. Missing review authority blocks the relevant graduation. There is no serving behavior
change to roll back in W0. All historical source/results retain their original dates.

Closure is recorded in entry 002 of the [journey](../adrl-implementation-journey.md) and the
[W0 evidence record](../research/adrl-w0-baseline-2026-09-07.json). Full program maturity,
deployment readiness and unattended completion of future waves are not W0 outcomes.
