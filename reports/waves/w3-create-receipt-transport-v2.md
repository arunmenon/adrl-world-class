# W3.2 create receipt and execution transport correction, v2

Frozen 8 September 2026 before runtime edits. Scope: offline Unix-socket fault tests and
transport correction only. No Docker invocation or new engine allowance in this packet.
Primary OPS-001; linked MEM-001/002/003/005/010, SAF-007 and TRU-001 retain their decisions.

## Evidence and hypothesis

Both retained engine snapshots set the stopped owner's request budget to two seconds before
creation so the execution constructor will accept that same client. The earlier stopped-only
policy default is ten seconds. The second batch's first create produced a never-started object
but lost the original client receipt. No underlying error type or exact per-create timing was
retained then. The 2.76 seconds between batch issue and daemon Created includes pytest/setup
work and cannot prove a two-second request timeout. Timeout remains a hypothesis.

## Frozen correction

- Keep stopped-resource-policy-v1 and its existing bounded preparation settings (default ten
  seconds, maximum fifteen). Do not increase these or retry creation. The original client alone
  supplies the full returned ID; only validated original receipt/inspection can bind it.
- Introduce isolated-fixture-execution-v2 with explicit active_request_seconds, default two,
  range 0.1 to two seconds. Use a separately validated, tighter transport view for every active
  request, including profile, inspection, start, kill, discard and recovery. Never mutate the
  owner's preparation policy. Keep the selected socket, seccomp pin and all other controls.
- Read v1 histories with their original profile version and old coupled <=2-second requirement.
  Its new default field is fixed at two; do not reinterpret old engine HMACs or rewrite rows.
  Recovery must use the authenticated event's transport profile, including when a v2 coordinator
  opens a v1 history. Schema 12 and public API preview 4 stay unchanged.
- Classify transport failures using a closed set of safe causes (read/connect/write/pool timeout,
  HTTP transport failure or socket failure). Keep the generic ResourceError message and owner
  uncertainty behavior. Retain only the bounded cause in private fixture diagnostics, never raw
  exception messages or a new product-ledger field. Existing response-format/size/encoding codes
  remain bounded. Check elapsed response budget on empty responses as well as chunks.
- These are HTTP phase timeouts with elapsed-response rejection, not a hard wall-clock watchdog
  for a sequence of requests. The existing independent fixture lifetime remains essential.
- Keep permanent workspace and launch fences, original-ID-only ownership, one create and one
  start, cancellation draining, false exact-close/learning eligibility and strict identity checks.
  No new automatic adoption, storage erasure promise, real payload, harness or routing exposure.

## Required offline tests and stop rules

Reproduce delayed original create response both within a preparation budget and beyond an active
budget using the local Unix-socket fixture. Show that response loss can coexist with a created
object, without a second create, binding, start or adoption. Cover malformed/missing-ID/oversized/
encoded response, connection loss and elapsed body rejection. Verify active requests keep their
own bound and the owner stays unchanged. Exercise legacy authenticated history recovery, invalid
policy refusal and the existing engine-test unreceipted-create halt with bounded cause retention.
Retain failed attempts; at most three failed repairs for this bounded task. Run all eleven checks,
freeze tested input hashes and synchronize the owning ADRs, index, buckets, changelog, journey
and state. Preserve all 77 architectural status/maturity fields and unrelated dirty files.

## Completion boundary

This packet can establish a supported offline correction. It cannot retrospectively identify the
old failure or qualify the new engine workflow. A later finite packet must begin with stopped
create/receipt/cleanup alone and use fail-fast plus the fixture uncertainty guard. Any uncertain
original receipt stops that engine batch. Full d2/B2/B3/W3 remains open.
