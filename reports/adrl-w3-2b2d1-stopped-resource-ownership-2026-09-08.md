# ADRL can now establish ownership before a job runs

W3.2b2d1 implementation report, 8 September 2026.

**ADRL now has a tested way to create a stopped execution container, record exactly which
container belongs to an attempt, recover that relationship after reopening its store, and
remove the container safely within this contract.** It still cannot run a workload through
this new component. The result is a stronger preparation step, not a completed execution backend.

All **812 tests and eleven engineering checks pass**. Seven owning architecture decisions
record the result. Their status and maturity grades, and those of the other 70 decisions,
remain unchanged. The [journey](adrl-implementation-journey.md) places this slice in the roadmap.

## Why this step matters

The previous experiment showed that a container can provide a useful boundary around writers.
It also showed that killing the local Docker client can leave the actual work running. ADRL
therefore needs an answer to a basic question: *which resource do I own, and what do I know
actually happened to it?*

Imagine submitting a job and losing the confirmation message. Submitting it again might create
a duplicate. Deleting something with a similar name might affect the wrong job. ADRL now records
its intent before asking for a container and binds the exact returned identifier to the engine,
creation time and complete inspected configuration. A similar name or label is insufficient.

| What ADRL knows | What it can do |
|---|---|
| Intent exists; no create request was claimed | Revalidate authority before claiming one create request |
| Create was issued; its returned identity was not durably bound | Keep the operation unresolved and the workspace blocked |
| Exact identity and configuration are durably bound | Re-inspect the same stopped object; a matching retry creates nothing new |
| Removal was issued; its acknowledgement was lost | Check absence of that previously bound exact ID before recording removal |

This deliberately favors a visible unresolved operation over an invented success. An uncertain
create may leave a stopped orphan for later reviewed recovery. This first implementation has
no name-based adoption, start, restart, exec, kill, capture or workspace-release operation.

## What changed in the product foundation

An internal owner connects the existing bound session and v2 attempt journal to an explicitly
selected local Docker engine. A readable start and intact terminal grant are required. Session
authority, attempt state and the grant are rechecked immediately before the durable create claim.
A permanent workspace block and the initial ownership intent commit together.

Five append-only metadata events describe intent, issued create, bound identity, issued removal
and confirmed removal. These events carry no raw workspace path, command or task payload.
Cleanup evidence uses host authentication separately from session content keys. After session-key
erasure, a trusted local operator can still remove a previously bound stopped container without
recovering the erased content key. Every result retains the workspace block and is ineligible
for exact task closure or learning.

Schema 11 adds this metadata. The inventory now checks **325 fields**, with **328 documented
entries** including earlier filesystem metadata. Public API preview 4 and routing behavior are
unchanged. Docker remains an optional backend candidate behind shared product contracts;
this is not a new mandatory installation for every harness.

## What the tests establish

There are **49 new unit cases** using a real local Unix-socket HTTP fixture. They cover duplicate
and concurrent requests, changed identity/configuration, expired or erased access, invalid grants,
pending-intent revalidation, quota limits, corrupted evidence, database failures, repeated
cancellation and migration from a schema-10 database shape. Fault injection checks that an
append failure cannot silently cross the create or removal boundary.

Four additional acceptance cases use the existing Docker 27.3.1 engine on macOS arm64. They
exercise normal ownership/reopen/erasure cleanup and deliberately lost create, bind and removal
acknowledgements. These four cases passed both alone and inside the full suite. **Eight stopped
containers and one self-authored fixture image were created in total; all were removed and
the exact container IDs were rechecked as absent. None was started.** There were no image pulls,
model calls, real task payloads, new paid usage or daemon setting changes.

The complete run passed on its first attempt, with **all 306 declared source hashes stable**.
Focused behavior runs also passed. Preflight lint/type issues were corrected. Self-review added
the second admission check and tightened HTTP response handling before the final suite.
Implementation and review were performed by Codex; this was not independent security review.

## What this does not establish yet

Ownership metadata is only one part of reliable execution. Launching once, stopping all writers,
preventing later restarts, capturing the final output and erasing active/plaintext copies remain
open. Inspecting a stopped container's settings does not prove runtime enforcement. Container
removal does not prove physical disk, snapshot or backup erasure.

The new authenticated history detects changed rows, invalid MACs and interior gaps. It does not
have an independent record of the latest sequence: restoring a valid earlier prefix or the
whole database/key state is not covered. This corrects overly broad “truncated evidence” wording
in the frozen packet. HTTP limits are also bounded I/O checks, not a hard real-time watchdog.
Revocation and the daemon create request are not one atomic transaction; a race can leave a
stopped synthetic object. Cleanup metadata remains linkable and needs its own real-data retention
disposition before a real harness pilot.

## Maturity, RSI and the next step

The evidence is stronger for the specific ownership behavior. It does not demonstrate improved
routing, another harness, successful real tasks or automatic self-improvement. No ADR grade rises
merely because its new component passes tests. Full W3, including task-close and capture binding,
remains open.

For RSI, the benefit is foundational: future course correction should use output from the
correct attempt, with a defensible completion record. This slice helps establish that chain of
identity. It does not train a router, change a policy or approve its own improvement proposal.

Next, the [launch and active-recovery packet](waves/w3-2b2d2-launch-admission.md) freezes the
contract for one-shot launch, lost acknowledgements, stopping, owner death, revocation and
preventing new writers. Only then should a bounded synthetic start capability be introduced.
Safe capture and erasure follow; real-harness credentials, network access and retention keep
their separate roadmap gates.

## Review trail

- [Frozen slice and disposition](waves/w3-2b2d1-stopped-resource-ownership.md),
  [parent ownership packet](waves/w3-2b2d-resource-ownership.md),
  [check/source evidence](research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json),
  [source diff](research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.patch).
- [Runtime contract](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md),
  [owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py),
  [transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
  [unit cases](/Users/arunmenon/projects/adrl-core/tests/unit/test_resource_owner.py),
  [local engine cases](/Users/arunmenon/projects/adrl-core/tests/integration/test_resource_engine.py).

The versioned HTTP create/inspect/delete contract was checked against the official
[Engine API 1.47 reference](https://docs.docker.com/reference/api/engine/version/v1.47/) and
[Moby 27.3.1 API schema](https://raw.githubusercontent.com/moby/moby/v27.3.1/api/swagger.yaml).
These documents describe the API; the test record above establishes what was exercised locally.
