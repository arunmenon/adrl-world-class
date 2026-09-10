# Identity and launch experiment v2

Frozen 8 September 2026 after 101 offline identity/reporting cases passed. The old two-run
experiment is closed and preserved. This batch changes the identified OOM comparison and
failure recording; it does not extend the old allowance or add production execution authority.

Use [execution identity v1](w3-execution-identity-v1.md) and the changed
[research driver](../research/execution-identity-2026-09-08/run_probe.py). Record the exact source
hashes and passing offline output before import. One writer, no agents. Stop at the first new
failure or unresolved cleanup; no engine repair/retry under this packet. A subsequent run
requires a new diagnosed cause and disposition, never unused container headroom alone.

## Fixed bounds

Exactly two permitted stage invocations: one identity case, followed only on its success and
confirmed cleanup by one six-case lifecycle stage. At most seven create-issued records, one
image import, eight successful synthetic start requests (including one restart negative
control), and no pull/build/install/daemon-setting change/network/host mount/model call/real
task payload. Each case observer bound is 15 seconds; HTTP I/O 2 seconds/131072 response bytes;
forwarding gate 5 seconds, client subprocess 3 seconds, import 15 seconds. The self-authored
fixture has its independent seven-second exit timer, subject to OS scheduling. Bounds are not
hard real-time guarantees. Original receipts govern cleanup, and every issued create counts.

The existing pinned tar has SHA-256
`6e555bb7c8d3457826f87d1146b43a5c8b490490986eba69b82247e467dadd7b` and exactly work/probe members;
the executable digest is `74085cef493ac7e62755cdcc650ef9f1c3856d05a5b9016e2cc8978eb4949e07`.
Import one uniquely tagged and labelled image through the explicit local socket. Record import
intent and exact returned ID; uncertainty stops the batch without name adoption or retry.
Retain d1's non-root, explicit pinned seccomp, no-capability, no-network/no-mount, private
namespace, no-restart and resource-limit configuration. Research-only forced removal applies
solely to these originally receipted disposable resources. Runtime d1 remains non-force/no-start.

## Acceptance in order

1. Create/start/readiness/inspect/kill/exit/inspect: only the pinned OOM false-to-null projection
   changes; every other stable identity/configuration field matches; cleanup confirms absence.
2. Kill while a start is held: kill refuses created state; releasing start still produces a
   late write. Stopping too early is not a future-start barrier.
3. Remove while start is held: exact absence precedes forwarding; delayed start receives 404.
4. Lose start reply: daemon accepted it and resource is running; discard confirms absence;
   a subsequent start receives 404.
5. Known start/kill/observed exit: two bounded reads across the scheduled late-write delay stay
   unchanged; fixture context shows seccomp filtering, no new privileges and zero effective caps.
6. Explicit restart after exit: StartedAt changes and a late write occurs. Record RestartCount;
   the frozen negative-control hypothesis expects zero across manual starts.
7. Disposable client exits abruptly after acknowledged start: resource is still running;
   only the self-authored fixture's independent termination brings it to exit within eight
   measured seconds. No arbitrary harness watchdog or owner-death recovery is qualified.

Each accepted case needs its durable assertion record plus successful exact-ID cleanup. Raw
initial/intermediate observations and separate primary/cleanup failures survive failures. Never
make an erased output, a successful task outcome or learning eligibility from these observations.
All seven exact IDs and the single image must be confirmed absent before batch closure.

## Data and limits

Private mode-0700 batch storage holds synthetic raw inspections, returned IDs, engine/socket
profile, create bodies, comparison digests, timestamps, case/error records and source hashes.
These are linkable local research records, not encrypted product payloads or ledger entries.
Keep them for review; this experiment makes no physical/backup erasure claim. Public evidence
contains references/hashes and summarized fixture results. Runtime metadata inventory stays at
325 checked fields/328 documented entries because runtime storage does not change.

Success supports the proposed lifecycle's engineering assumptions only. Runtime launch claims,
permanent denial markers, admission seals, authenticated recovery, active-copy erasure, B3
capture and a real Claude task remain implementation/qualification gates. Preserve all 77 ADR
status and maturity fields and synchronize scoped evidence with the journey after disposition.
