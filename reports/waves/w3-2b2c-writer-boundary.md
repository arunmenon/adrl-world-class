# W3.2b2c: Qualify the writer boundary before designing release

Prepared 8 September 2026 after the [coordination slice](w3-2b2b2-process-coordination.md).
Owner: Codex, implementation/self-review. Independent security review remains unassigned.
This packet authorizes only the existing program's bounded local investigation and synthetic
checks, not new infrastructure, paid services, real task payloads or release of any fence.

## Decision to make concrete

Identify what can establish that every admitted writer has stopped. The current process-group
backend explicitly cannot do that. Its permanent workspace block is an interim restriction for
disposable fixtures, not the future product workflow. Do not build a release button or accept a
caller boolean before a complete, tested boundary exists.

Inspect the existing runtime/verification implementation and available host capabilities. Record
the tested OS/tool versions and source references. Prefer existing supported mechanisms, with
their actual scope, over adding a new platform. Distinguish a process group, a filesystem access
policy, an isolated disposable workspace and an enforceable whole-writer lifetime boundary.

Before executing any additional containment experiment, freeze its failure cases and bounds:
detached descendants, supervisor death, reused process identity, late writes, open file handles,
renamed/replaced paths, external writers, partial cleanup, restart and lost acknowledgements.
Use only self-authored, self-terminating synthetic fixtures. Never signal an arbitrary saved PID.
Do not bypass the permanent fences added by B2b2 or claim that readonly permissions prove absence
of open writers. Preserve all existing erasure and terminal-capacity behavior.

## Deliverable and disposition

Produce a concrete backend recommendation with evidence, limitations, integration cost and the
precise authority it would grant. If the available environment can support a qualified bounded
backend within existing authorization, freeze its implementation packet before coding. If new
infrastructure or an explicit scope decision is necessary, prepare the reviewable choice and ask
once at that gate. The unanswered choice blocks only dependent containment/release work.

In that case, continue the independent W3 work on active plaintext lease erasure and crash-copy
recovery after freezing its packet. That work must also use synthetic captures, preserve revoked
keys and distinguish cleanup failure from erasure completion. Neither route admits real payloads
or establishes exact-close capture association before all relevant gates pass.

Keep the running journey, execution state and owning ADRs synchronized with findings. A research
or capability inventory is not an implementation test, independent review, maturity promotion
or completion of W3. No endless repair loop; retain the program limit of three failed repairs.

## Frozen local experiment, 8 September 2026

Read-only capability inspection found macOS 26.3 arm64 (25D125), hardware virtualization,
Docker client/server 27.3.1 on the existing local Unix socket, LinuxKit 6.10.11 and cgroup v2.
The daemon reports `seccomp,profile=unconfined`; do not change daemon settings or assume a
default syscall filter. No suitable cached official tiny fixture image was found. The installed
Go compiler can build a self-authored static Linux/arm64 probe without dependencies or network.

Import only that probe and empty fixture directories into a uniquely tagged scratch image on
the already-running engine. Pin the resulting image ID. Fetch and hash the Docker/Moby 27.3.1
default seccomp JSON as an explicit per-container test input; reject missing/invalid profile.
No image pulls/build dependencies, host repository/credential/socket mounts, ports or network.
Run as UID/GID 65532 with all capabilities dropped, no-new-privileges, private namespaces,
no restart, at most 32 processes, 96 MiB memory and 0.5 CPU. Commands contain only fixture text.
Write only to the image's user-owned `/work` directory. A writable container layer preserves
synthetic output after stop; this is not an approved storage design for real task payloads.

At most eight sequential containers, each self-terminating within eight seconds; each CLI call
has a 15-second deadline. At most three repair cycles. Preserve exact created container IDs,
unique ownership labels and before/after state before stopping/removing only those resources.
Do not stop the daemon, unrelated containers or arbitrary PIDs. Remove this run's image after
copying its tiny synthetic results and recording hashes. Stop on unconfirmed ownership/cleanup.

Acceptance observations:

- Fixture sees PID 1, no effective capabilities, no-new-privileges and an active seccomp filter.
- A deliberately detached child can write while namespace init stays alive; detachment is real.
- When init exits or the owned container receives SIGKILL, the detached late write does not occur;
  inspect the same container as stopped and copy only its synthetic output afterward.
- Killing the local CLI client alone is a negative control: the daemon-owned container may keep
  running. This must remain a recovery requirement, not a false owner-death guarantee.
- A read-only-mode negative control and a moved/open-file negative control on disposable host
  fixtures show why permissions/path names do not prove stopped writers.
- Scope explicitly excludes host external writers because no workspace is bind-mounted, but a
  Docker/host administrator remains trusted and could mutate or restart the container. No claim
  of container escape resistance or complete real-workload qualification follows.

Record failed probes, exact tool/kernel/image/profile/source identities and resource cleanup.
This is a research experiment, not a new runtime backend. Do not release any existing fence or
count these cases as part of the unchanged 759-test implementation baseline. Freeze a separate
implementation/recovery contract if the observations justify advancing.

## Disposition, 8 September 2026

Research observations recorded; no runtime backend is qualified. The corrected run completed
four container observations and two host-file negative controls. A first run failed after
three cases because Docker start did not support the supplied attach option; one repair resolved
it. Both runs together used the full eight-container allowance. All containers and two scratch
images were removed, with zero matching resources in final label-specific reconciliation.

Self-review found a 60-second compiler allowance in the driver despite the packet's 15-second
command limit. Actual compilations were under three seconds. The final driver lowers that
allowance to 15 seconds; a separate bounded compilation produced the same binary. Executed and
current driver hashes are distinct and retained in the evidence. No runtime code changed, and
all 300 previously tested source hashes still match the 759-test/eleven-check baseline.

The local engine supports a credible next candidate without new infrastructure. Continue the
[durable resource-ownership packet](w3-2b2d-resource-ownership.md) before runtime integration.
Client-death recovery, restart/admission sealing, full containment qualification, close/capture
binding and plaintext erasure remain gates. Existing fences stay permanent. See the
[report](../adrl-w3-2b2c-writer-boundary-2026-09-08.md) and [evidence](../research/adrl-w3-2b2c-writer-boundary-2026-09-08.json).
