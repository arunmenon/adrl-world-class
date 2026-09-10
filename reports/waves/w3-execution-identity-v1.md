# Execution identity research contract v1

Frozen 8 September 2026 before offline validation or fresh daemon mutation. Primary ownership:
OPS-001 and SAF-007; evidence attribution MEM-001/002/003, cleanup MEM-005/010, trust TRU-001.
This is a research comparator used by the synthetic driver, not a runtime launch interface.

## Rule and authority

Preserve the complete original stopped inspection and its SHA-256. Require an exact unchanged
engine profile: original engine ID and explicit socket, Docker 27.3.1, API 1.47, Linux arm64,
kernel 6.10.11-linuxkit, cgroup v2/cgroupfs, unsupported OomKillDisable, supported memory/swap/
PIDs/CPU limits, security-options list and explicit pinned seccomp digest. Unknown or malformed
profiles are rejected, including missing capability fields and numeric substitutes for booleans.

Compare the complete Config, HostConfig, Mounts, Image, Path, Args, Platform and Name fields,
plus exact Id and Created. Original OomKillDisable must be boolean false. The current value may
be boolean false or null; both project to false. Missing, true, numeric zero or other values
are refused. No other null/default normalization is allowed, including PortBindings. Canonical
JSON bytes, not Python equality, distinguish boolean, numeric and string representations.

Validate the original bytes against the retained digest before comparison. Record comparator
version, original digest, profile digest and projected digest. This binds the research result
to evidence; it is not authenticated runtime ownership. A future runtime caller must separately
authenticate the original resource event/MAC and engine binding. State, StartedAt, FinishedAt,
RestartCount and daemon-generated runtime paths are lifecycle observations outside this stable
configuration comparison. Equality does not prove never-started, stopped, sealed or exact-close.

## Offline acceptance

Use the retained second-run raw inspections with their recorded SHA-256 values. Accept unchanged
creation and the observed false-to-null transition. Reject altered original digest; profile
version/engine/socket/kernel/cgroup/capability/seccomp; identity/creation/image/name/command;
ports, mounts, capabilities, privilege, namespaces, seccomp, network, restart, logging and
resource limits; missing/malformed required fields; and unrelated default-representation drift.
Inputs must remain unchanged. A changed unknown HostConfig or Config field also fails comparison.

## Research driver accounting

Preserve the old failed driver and evidence. The changed driver records/fsyncs create intent
before one create call, returned receipt immediately, original inspection before verification,
intermediate observations before cleanup, and primary and cleanup errors independently. Count
issued creates against the allowance. A missing create acknowledgement remains uncertain,
halts further creation and is not reconciled by name discovery/adoption or reissue. An exact
receipt with failed binding remains an owned but unresolved cleanup obligation. A case is
accepted only if its assertions and exact-ID cleanup both succeed. Persist a failed case too.

Fresh engine work requires a separate finite experiment packet after these offline cases pass.
No runtime/schema/API change, physical erasure, real-harness or whole-ADR maturity follows.
