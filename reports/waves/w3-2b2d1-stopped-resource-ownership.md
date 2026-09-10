# W3.2b2d1: Own a stopped resource before adding launch

Frozen 8 September 2026 before code. Parent: [resource ownership](w3-2b2d-resource-ownership.md).
Codex implements and self-reviews; independent review remains unassigned. Existing authorization
covers local engineering and bounded synthetic fixtures, not live/model execution or new infrastructure.

## Bounded scope

Implement an internal primitive that creates, binds, inspects and removes a never-started local
Docker container. There is no start, exec, restart, kill, capture or workspace-release operation.
The parent packet's launch-acknowledgement, active owner-death, runtime erasure monitoring and
whole-writer/capture gates remain later slices. This closes a real preparation/recovery contract,
not the whole backend merely because metadata exists.

Use versioned Engine API 1.47 directly over an explicitly provided local Unix socket, without
ambient Docker context/proxy/registry credentials. Bound HTTP timeout/body sizes; do not follow
redirects or pull images. Bind the host-keyed endpoint/engine identity. Only Linux/cgroup-v2 and
an already-present immutable Linux/arm64 fixture image are accepted in this version.

Create intent requires a readable unexpired v2 attempt in `started`, the bound workspace and its
intact terminal grant. In one transaction, append a permanent workspace fence and authenticated
resource intent. Preserve existing group-backend fences. Record `create_issued` before one daemon
create request; only the caller that durably claims that transition may issue it.

Bind the exact returned full resource ID only after inspecting a never-started `created` object,
the intended image/name/labels and all declared security/resource controls. Save a host-keyed
digest of the complete observed Config/HostConfig/mount/command identity and its creation time.
Re-inspect that identity before returning a bound retry or removing the object. A name/label
alone, mismatched engine/configuration or saved host PID never authorizes adoption or cleanup.

If create fails or its acknowledgement/ID is lost before durable binding, leave `create_issued`
uncertain. Do not retry create, query-by-name to adopt, start or delete a candidate. If binding
committed but its acknowledgement was lost, a matching retry reads/revalidates the existing ID.
This conservative first version may leave an unstarted orphan that needs later reviewed recovery.

Removal requires an authenticated bound ID that still matches and has never started. Append
`remove_issued` before non-force deletion. If the acknowledgement is lost, absence of the exact
previously bound ID may reconcile to `removed`; an existing object must still match before a
retry. Unexpected running/exited/restarted resources refuse removal. No forced deletion or kill.
Every outcome retains the workspace fence and never claims physical/plaintext erasure.

Cancellation drains the protected worker. A cancellation during an in-flight create can leave
a bound stopped resource or an unresolved issued state, not an invented no-resource result.
Cleanup metadata is authenticated with the host HMAC key, separately from content keys; after
session erasure, a trusted local operator can inspect/remove an already-bound stopped resource
without recovering the session key. Host-key rotation or corrupt/truncated evidence blocks this
authority. Whole-database/key rollback and hostile host/daemon administration remain outside scope.

## Data, configuration and bounds

Append only an authenticated five-phase metadata history: intent, create_issued, bound,
remove_issued, removed. Stable operation/attempt/workspace/session references are keyed; engine,
request and full configuration references are keyed; resource/image IDs, versions, policy,
timestamps and chain MACs are operational metadata. No raw path, argv, environment, profile JSON,
task payload or provider credential goes into that history. Link it to the permanent fence.

`stopped-resource-policy-v1` bounds admission to at most 32 permanent resource histories per ledger,
five events of at most 4,096 bytes each. Logical maximum space is bounded; physical disk/DB failures
can still block writes. HTTP timeout defaults/maxes to 10/15 seconds and response bytes to 131,072.
Explicit per-container limits: non-root 65532, no capabilities, no-new-privileges, pinned seccomp,
no network/mounts/ports/restart/healthcheck/image-declared volumes, private namespaces, at most
32 processes, 96 MiB memory/swap and 0.5 CPU. The writable layer is synthetic-only and no command
is started. Refuse inherited image entrypoint/environment/healthcheck/volume controls that escape
the fixed preparation contract; include all accepted labels in the identity check.

Offline wire fixtures exercise real Unix-socket HTTP and failure ordering. A separate local
acceptance run may import one self-authored fixture image and create at most 16 stopped
containers, including explicit negative-control resources. No workloads execute, image pulls,
daemon settings change or unrelated resources are touched. Track full created IDs and cleanup;
stop on unresolved ownership/cleanup. At most three failed repairs per task.

## Frozen acceptance

- Correct create binds a never-started resource; retry/reopen never creates another.
- Concurrent same/different operations serialize against the permanent fence and resource quota.
- Wrong workspace/session, expiry, revocation, missing/corrupt grant or wrong engine refuses create.
- Lost create acknowledgement/failed bind stays uncertain with no adoption or second create.
- Bound-ack loss, remove-ack loss and already-removed retry preserve truthful phase/identity.
- Changed ID/image/configuration/creation-time/labels or unexpected started state refuses cleanup.
- Session erasure preserves only previously established cleanup authority, not create authority.
- Host-key change, row/MAC/gap corruption, database failure and HTTP timeout/malformed/oversized
  replies cannot invent a binding, deletion or successful outcome.
- Cancellation and owner restart leave durable pending/bound evidence; no PID-based recovery.
- Old schema-10 histories/fences survive migration unchanged; all eleven runtime checks pass.
- Inventory, owning ADRs, index/buckets/changelog and journey reflect exact tested scope; no grade changes.

Owning ADRs: OPS-001, MEM-001/002/005/010, SAF-007 and TRU-001. Existing full-B2/B3/W3 gates remain open.

## 2026-09-08 disposition and clarification

The bounded stopped-resource slice is implemented and locally validated: 49 unit cases, four
opt-in engine cases, 812 tests and eleven combined checks pass with 306 declared hashes stable.
Two engine runs created eight stopped containers under the sixteen-container ceiling; one
self-authored fixture image was imported, no image was pulled, and all resources/image were
removed and reconciled absent. No workload started. See the [report](../adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md) and
[check/source record](../research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json).

Self-review clarification of the frozen text: its phrase “corrupt/truncated evidence blocks this
authority” was too broad. Interior gaps, altered rows and invalid MACs block authority; rollback
to a valid earlier prefix or rollback of the whole database/key state is not independently
anchored by this implementation. Such rollback remains outside this qualification. HTTP timeout
and raw-chunk elapsed checks likewise are not a hard wall-clock guarantee for header dribble or
a wedged OS/daemon. Revocation and daemon create are not atomic; an admitted race can leave a
stopped synthetic object. These limits are recorded, not treated as satisfied safety gates.

Prior frozen text is retained above. No ownership-by-name, start, force removal, workspace
release, exact-close/learning eligibility or maturity promotion was introduced. The parent
[d packet](w3-2b2d-resource-ownership.md), B2/B3 and W3 remain open. Continue with the
[d2 launch/active-recovery contract](w3-2b2d2-launch-admission.md), freezing its fresh bounds
before any new daemon mutation.
