# W3.2b2d: Durable ownership of isolated execution resources

Prepared 8 September 2026 after the [writer-boundary investigation](w3-2b2c-writer-boundary.md).
Owner: Codex, implementation/self-review. Independent security review remains unassigned.
The existing local Docker engine is available; this packet does not authorize another engine,
VM installation, image pull, real task payload, model call, public API or live deployment.

## Why this comes next

The local experiment established a useful PID-namespace candidate, and also showed that killing
the CLI client leaves daemon-owned work running. Before an execution backend can be trusted,
ADRL needs durable ownership, failure ordering and recovery. Do not connect a generic `docker
kill` command to an arbitrary caller-supplied container name or persisted host PID.

## First bounded implementation slice to freeze

Inspect the existing execution fences, attempt journal, key revocation and process ownership
code. Freeze a v1 admission/ownership policy, data inventory and fault table before editing.
Name existing owning ADRs rather than creating new IDs. The target is an internal synthetic
resource-owner primitive with real daemon interactions, not a placeholder public interface.

- Restrict to an explicitly bound local engine. Verify engine identity, immutable fixture image
  identity and the exact admitted security/resource configuration before start. No inherited
  mounts, capabilities, privileged/host namespaces, restart policy or network shortcuts.
- Persist create intent before creating a resource; bind returned full resource ID, operation
  identity and configuration evidence before start. Stable retries must reconcile ambiguous
  creation acknowledgements without duplicate launch or unintended adoption.
- Define what establishes recovery authority after restart. A full ID plus a matching name or
  label alone is insufficient; bind engine, original creation intent and configured resource
  evidence. Mismatch, missing evidence or failed inspection preserves uncertainty and blocks use.
- Keep cleanup authority separable from erased prompt/content keys without creating a key-
  resurrection path. Inventory all durable identifiers and control metadata. Erasure must not
  wait indefinitely for an encrypted terminal record or a stopped-process claim.
- Bound creation, observation, resource use and cleanup. Preserve unresolved state after client
  death, timeout, daemon unavailability or partial database failure. Do not restart/recreate a
  workload just because an acknowledgement is missing. No global daemon restart or broad prune.
- Preserve every existing permanent group-backend fence. This slice grants no workspace release,
  exact-close, captured/verified outcome, learning authority or automatic promotion. A later
  backend needs a complete stop/admission-sealing and artifact-capture contract.

Frozen acceptance must cover concurrent admission, lost acknowledgement before/after create and
start, owner/client death, daemon loss, altered identity/configuration, wrong engine, stale
records, revoked session keys, quota/disk failures and cleanup ownership. Use self-authored
bounded fixtures, the existing explicit seccomp profile, and no host repository or credential
mount. Keep all created resources scoped and reconcile cleanup before closure.

Do not assert a hard real-time deadline for unbounded OS/daemon behavior; define the blocked
state and independent cleanup/recovery responsibility. Exact-copy capture will also need safe
archive extraction, durable output identity and a clear boundary against restart/new writers.

## Gates and alternatives

The recommendation is an optional isolated backend behind shared product contracts. Native
observation remains available at its existing declared scope; Docker does not become a mandatory
dependency for all harnesses merely because this primitive exists. A real harness/image/network/
credential profile and additional plaintext retention need their own concrete packet and
applicable product decisions. This slice cannot settle those choices with synthetic evidence.

If a material host/infrastructure decision blocks the actual primitive, prepare the concrete
choice and continue independent W3 active-plaintext lease/crash-copy work after freezing its
contract. Do not retry an unchanged blocker. Keep one writer, at most three failed repairs,
the full required check suite for runtime changes, ADR synchronization and the running journey.

## 2026-09-08 decomposition and current disposition

The first implementation was narrowed and frozen as [d1 stopped ownership](w3-2b2d1-stopped-resource-ownership.md):
create/bind/inspect/non-force-remove, with no start or active lifecycle. It is validated by
812 tests and eleven checks; [evidence](../research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json) preserves exact scope and
limitations. Lost create acknowledgement stays unresolved without adoption; authenticated bound
removal can reconcile absence. All fixture resources were removed. No grade or release promotion.

The parent acceptance involving start, active owner/client death, runtime erasure observation,
full stopping and prevention of new writers remains open. [d2](w3-2b2d2-launch-admission.md)
prepares the next lifecycle/fault contract before code or another bounded fixture run. This
subdivision does not mark the parent, B2/B3 or W3 complete.
