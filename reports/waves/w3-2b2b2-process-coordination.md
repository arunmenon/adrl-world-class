# W3.2b2b2: Stop coordination and durable workspace blocking

Packet `group-attempt-coordination-v1`, frozen 8 September 2026 before code.
Parent: [process ownership](w3-2b-process-ownership.md). Owner: Codex, implementation and
self-review; Arun Menon, product owner. Independent security review remains unassigned.
Only disposable synthetic fixtures, one implementation writer, no paid/model calls or new
infrastructure. At most three failed repairs per task; preserve all unrelated dirty source.

## Contract

Add an internal coordinator around the existing journal and owned process-group runner.
Admission requires a bound, unexpired, readable v2 attempt still in `started`, its original
terminal grant, and the same canonical workspace as the process request. Commit an append-only
workspace fence before attempting launch. Concurrent coordinators serialize admission through
the ledger. An existing fence refuses replay, even when an acknowledgement was lost. A new
journal start also honors that fence after a terminal event, erasure or restart.

Every admitted workspace remains blocked in this backend, including prelaunch aborts. There is
no release operation, caller-supplied quiescence proof, successful close, capture association,
PID recovery or launch retry. This deliberately conservative slice tests coordination while
whole-writer containment remains unqualified. It uses disposable workspaces; it is not a usable
real-task execution release. A future qualified backend needs its own reviewed release contract.

A dedicated monitor checks persistent revocation, credential expiry and journal state during
execution. A close/cancel/incomplete event, loss of readable authority or check failure requests
stop through the in-memory owner. Direct keystore revocation and another erasure-service instance
are covered by observation, without depending on a callback from one particular service. This
is eventual observation, not atomic exclusion of launch with erasure. Poll interval is versioned
(default 0.05 seconds, range 0.01 to 1 second); OS, disk and scheduling delays prevent a hard bound.
Erasure never waits for process cleanup or an encrypted terminal append to revoke access.

Cancellation requests stop and drains the owning worker before propagating, even under repeated
cancellation. When cleanup finishes, try to append `incomplete/quiescence_unavailable` using the
original terminal grant. Preserve any already-terminal event. Expiry, erasure, database failure
or corruption may prevent this append; report unavailable and retain the durable fence. Journal
terminal quota and workspace reuse are separate facts. Process reports are ephemeral in this
slice; a restart recovers the block, not a fabricated process outcome.

Persist only four keyed identifiers, the host HMAC key ID, a timestamp and the bounded versioned coordination policy.
No PID, raw path, command, environment, output or plaintext payload is stored in the fence.
The v1 policy admits at most 128 permanent fences per ledger (configurable downward). Old
schema-9 histories migrate without fences; old journal-only semantics remain unless execution
was fenced. Refuse new admission if existing fences use another host HMAC key ID; hostile database/key rollback, renamed/replaced
directories, detached/unrelated writers, active plaintext leases and crash-copy cleanup are not
qualified. No routing or privacy-pin policy changes.

Owning ADRs: OPS-001, MEM-001/002/003/005/010, SAF-007 and TRU-001. Keep all architecture status
and maturity fields unchanged; this adds scoped local evidence only.

## Frozen acceptance cases

- A bounded real fixture exits or times out; group report remains ineligible and workspace blocked.
- Direct revocation, erasure service, expiry, close/cancel, unreadable journal or monitor error
  requests cleanup; no key recreation and no workspace release.
- Normal completion, cancellation and failed terminal append preserve the admission fence.
- Two coordinators, replay and post-restart attempts cannot launch through the same fence.
- Prelaunch validation/admission failure launches nothing; lost admission acknowledgement may
  leave a fence and never authorizes automatic replay.
- Missing/corrupt grant, wrong workspace/session, legacy policy and already-closed attempts reject.
- Concurrent erasure and terminal writing either preserve an honest terminal record or expose
  unavailable; neither outcome means that all writers stopped.
- Faulted fence insert is atomic; fence count is bounded; migration retains old encrypted history.
- Persisted fence contains only inventoried metadata; public API and learned authority stay unchanged.
- All eleven required checks pass; source hashes, ADR prior wording, links and all 77 grades verify.

Full B2, B3 and W3 remain open. Next qualify a complete writer boundary and resolve active-copy
erasure/crash leftovers before actual task payloads or exact-close capture binding.

## Disposition, 8 September 2026

Locally validated: 35 new coordination cases, 759 total passing tests and eleven checks.
Schema 10 has seven additional fields, API preview 4 is unchanged, and all 77 status/maturity
fields are preserved. Three retained diagnostic failures led to a stale-report fix and corrected
fault/transaction/interpreter/contention fixtures; the final focused and first combined runs pass.
No invariant was waived. See the [report](../adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[evidence](../research/adrl-w3-2b2b2-process-coordination-2026-09-08.json) and [source diff](../research/adrl-w3-2b2b2-process-coordination-2026-09-08.patch).

Close this bounded coordination slice only. Permanent blocks have no release path, including
admitted prelaunch failures. Full B2, B3 and W3 remain open. Continue the
[writer-boundary packet](w3-2b2c-writer-boundary.md); if a material backend decision is needed,
prepare it and continue independent active-plaintext/crash-copy work under its own packet.
