# W3.2b2d2 bounded launch/recovery experiment

Frozen 8 September 2026 before daemon mutations. This supports the
[launch contract packet](w3-2b2d2-launch-admission.md); it does not add runtime launch authority.
Runtime source remains at the verified 812-test/306-input baseline unless a separately frozen
implementation slice is undertaken. Owner/reviewer: Codex; no independent review claim.

## Questions and exact cases

Use the existing explicitly selected local Docker 27.3.1/API 1.47 engine and the previously
self-authored Linux/arm64 `/probe` binary. Its accepted modes terminate independently within
the programmed seven-second watchdog, subject to OS scheduling; there are no real task payloads.

1. Hold a start request at a local Unix-socket forwarding fixture. Issue kill against the
   still-created resource, observe its refusal, then forward start. Check whether work begins
   and the synthetic late writer writes. A stop-before-start must not count as closure.
2. Hold the same start, remove its originally receipted exact resource, confirm absence, then
   forward start. Check that this delayed request cannot start the removed resource.
3. Forward start but deliberately lose its client acknowledgement. Inspect the original exact
   resource, abort by forced removal, confirm absence and check that a new start is refused.
4. Acknowledge start, observe fixture readiness, kill the exact resource before its scheduled
   late write, and read two bounded copies of the synthetic output after observed exit. Check
   whether the output stays unchanged without removing its layer until fixture cleanup.
5. After an acknowledged start/kill/exit, explicitly start the same resource again as a negative
   control. Compare StartedAt and RestartCount. An exited state or a zero restart count alone
   must not be treated as proof that no later work can start.
6. Have a disposable host client start a bounded fixture, then exit abruptly without stopping
   it. Observe that the client is gone while the container is active, then measure the fixture's
   independent natural/watchdog termination. This qualifies only this self-authored fixture.

## Frozen bounds and ownership

Import at most one fresh uniquely labelled image from the already-retained self-authored tar;
verify the tar contents, binary hash and explicit seccomp profile hash before import. No pull,
build dependency, install, model call, network, daemon settings, host repository/credential/socket
mounts, public API, real workload or workspace release. Use d1's non-root, no-capability,
explicit-seccomp, no-network/no-mount/private-namespace/resource-limited configuration unchanged.

At most 12 containers in total, six per full run and at most two full runs; stop after a failed
run to inspect the cause, within the program's three-repair ceiling. Each probe has a 15-second
observer deadline; each HTTP I/O operation has a 2-second timeout and a 131,072-byte response
limit. The forwarding gate waits at most five seconds. These are failure bounds, not hard
real-time OS/daemon guarantees. Never abandon a live request without recording uncertainty.

Record and flush the full ID returned by each original create before testing. Fixtures may
inspect/kill/remove only these exact owned IDs after checking engine/image/name/configuration;
no discovery-by-name adoption, broad kill/prune, unrelated resource inspection or deletion.
All new resources use a unique test identity. Force removal is authorized only for these
disposable synthetic fixtures, explicitly to investigate the proposed abort path; production
StoppedResourceOwner retains its non-force/no-start contract.

Keep archive reads in memory, bounded, and limited to named synthetic `/work` files. Never
extract daemon tar members to a host path. Always reconcile exact IDs as absent and remove the
one owned image before closing the slice. Stop on unresolved ownership or cleanup. Retain
failed observations separately and do not relabel them as passing acceptance evidence.

## Deliverable

Produce a versioned launch/seal/stop/abort lifecycle and fault table informed by source inspection
and observations. Distinguish known completion of an API request from durable acknowledgement,
observed resource state, stopped writers and product eligibility. State proposed code changes,
compatibility, metadata, independent stop responsibility and remaining gates. Synchronize the
owning ADRs/index/buckets/changelog/journey/state without changing any maturity/status field.

## 2026-09-08 repair before second run

The first run stopped on its first container after a full-configuration mismatch at cleanup.
Its original create receipt identified the exact owned object. It had independently exited;
engine, image, name, command and every explicitly requested security/resource control matched.
It was removed non-force and confirmed absent before any new fixture was admitted. The first
run remains failed, with zero completed observations; its raw inspection and failed log survive.

The second and final permitted full run will retain raw create and post-start inspections. It
may normalize only an empty HostConfig.PortBindings representation (`null` or `{}`), requiring
both to contain no ports and every other configuration field to match exactly. This is a
research hypothesis to test, not a runtime comparison change or permission to ignore arbitrary
configuration drift. No nonempty binding is accepted. The original runtime stays unchanged.

## 2026-09-08 final disposition: experiment stopped at its two-run limit

The second run also failed in the first case; zero of six cases has an accepted record.
Its retained raw create/post-start pair differs only in HostConfig.OomKillDisable false to null.
The engine reports the control unsupported. Pinned Moby source explains this normalization.
The empty-PortBindings hypothesis did not resolve the failure and is not carried into runtime.

Both started self-authored fixtures independently exited. Original create receipts, exact
engine/image/name/command and every declared control were verified before non-force removal;
both exact IDs and the one imported image are confirmed absent. No third run is permitted
under this packet. The remaining ten-container numerical headroom does not override that limit.

Primary-versus-cleanup failure recording and a narrow versioned execution identity comparison
are now explicit prerequisites in the [next packet](w3-2b2d2-identity-compatibility.md). The
[proposed lifecycle](w3-isolated-execution-contract-v1.md) remains unimplemented and the six
cases remain outstanding. No runtime check was weakened, no runtime launch was added, and no
maturity or full-wave completion was claimed.
