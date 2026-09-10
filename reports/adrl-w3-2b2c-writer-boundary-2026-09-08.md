# A clearer boundary around an ADRL task

8 September 2026 | W3.2b2c | Research experiment completed; runtime backend still unqualified

**An isolated container is a credible next execution backend for ADRL on this machine.** In
bounded local experiments, a detached child could keep writing while its container was alive,
but could not make its scheduled late write after the container's initial process exited or
the container was terminated. This gives us a stronger candidate than the existing process-group
runner. It does not yet establish safe real-task execution or permission to release a workspace.

The practical question is simple: **when ADRL says a task has stopped, could something still
change the files we are about to judge?** We now have better evidence about how to answer it.

## What we found on this machine

The host is macOS 26.3 on Apple silicon. The existing local Docker engine is already running:
client/server 27.3.1, LinuxKit 6.10.11, cgroup v2. No infrastructure installation or image download
was needed. Apple Container, bubblewrap and the inspected alternative VM/container CLIs were not
available on PATH; that is a host inventory, not a claim that those approaches are impossible.

The Docker daemon reports its default syscall filter as unconfined. We did not change that
setting. Each fixture used an explicit, hashed Moby 27.3.1 seccomp profile, ran as a non-root user
with no effective capabilities and no-new-privileges, and had its own PID namespace. The fixture
observed an active filter. A seccomp filter limits system calls; it does not by itself prove
container isolation or stop all writers. [Docker seccomp documentation](https://docs.docker.com/engine/security/seccomp/).

We compiled one tiny, self-authored Go program into a static Linux binary with dependency/network
fetching disabled, then imported it into an otherwise empty scratch image. Each container had
no network, repository/credential/socket mounts, restart policy or published ports, and was
limited to 32 processes, 96 MiB and half a CPU. Only synthetic text was written inside its own
writable layer. This layer is an experiment convenience, not an approved place to retain real
task data after erasure.

## Six observations, including three important limits

| Experiment | Observed result | Meaning for ADRL |
|---|---|---|
| Detached writer, container kept alive | Child created its own process group and completed its late write | The positive control establishes that the fixture really could write after detaching |
| Initial container process exits | Detached child left no late write, including after its scheduled write time | A PID-namespace lifetime boundary is stronger than a process group for this fixture |
| Owned container receives SIGKILL | Container became stopped; the detached late write remained absent | Explicit container termination is a useful candidate control |
| Local Docker client is killed | Container stayed running and the detached child wrote | Losing the client is not proof that daemon-owned work stopped |
| Host file changed to mode 0400 after opening | Existing write handle still changed the file | Read-only permission bits do not revoke an already-open writer |
| Host file renamed after opening | Existing handle changed the renamed file, while a replacement occupied the old name | A path disappearing or being replaced does not prove that its previous writer stopped |

The kernel documentation explains the mechanism behind the container observations: termination
of a PID namespace's initial process causes the kernel to kill processes within that namespace.
Docker's default kill operation targets the container's main process with SIGKILL. These sources
support the mechanism; our results qualify only the particular fixture and configuration we ran.
[Linux PID namespaces](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html),
[Docker container kill](https://docs.docker.com/reference/cli/docker/container/kill/).

The stopped output was copied from the same recorded container identity and checked again after
the late-write deadline. Docker supports copying files from stopped containers. This is useful
for a future capture path, but a stopped container can still be manipulated through trusted
daemon administration; ADRL needs its own ownership and no-restart contract.
[Docker container copy](https://docs.docker.com/reference/cli/docker/container/cp/).

## The product direction this supports

My recommendation is to keep two explicit integration modes. This is a proposal for the next
backend packet, not a shipped capability or a new mandatory Docker dependency.

```text
Chosen harness -> Shared ADRL identity, task and evidence contracts
                         |
               +---------+----------+
               |                    |
        Native observation    Optional isolated execution
               |                    |
        Record what we see    Work in a disposable private copy
               |                    |
        Declare the gaps      Stop owned execution, prevent restart
                                    |
                             Capture and verify the output
                             [remaining implementation gates]
```

Native observation remains the easier starting point for harnesses that run on the host. It
must retain its declared attribution gaps. The stronger mode runs the admitted task inside a
private execution workspace; it must not silently bind-mount the developer's editable repository
and then claim that outside writers cannot affect it. Docker bind mounts deliberately expose
host files to a container, so excluding such mounts is a material part of this proposed boundary.
[Docker bind-mount documentation](https://docs.docker.com/engine/storage/bind-mounts/).

Both modes should use the same product contracts. A harness adapter supplies identity and
observations; an execution backend states what it can control and prove. Changing a backend
must not change the meaning of “observed,” “incomplete,” “captured” or “verified.” No second
harness or public endpoint is added by these experiments.

| Candidate | Current disposition |
|---|---|
| macOS process group plus current Seatbelt runner | Keep its existing scoped uses. Current code does not establish a whole-writer completion barrier; group fences remain permanent |
| Existing Docker engine with private PID/filesystem scope | Recommended next prototype, based on local availability and these bounded observations; ownership, recovery and capture are still missing |
| Direct Linux cgroup-v2 backend | Credible later backend. The kernel provides subtree kill and populated-state reporting, but ADRL would need controlled admission, delegation and filesystem isolation; not tested directly here |
| Per-task virtual machine | A stronger isolation option to assess if required by the threat model. Apple documents a per-container VM design, but that backend was not installed or tested here |

The latter two are source-backed candidates, not experimental results. See the
[Linux cgroup-v2 contract](https://docs.kernel.org/admin-guide/cgroup-v2.html) and
[Apple Containerization design](https://github.com/apple/containerization).

## What must be built before real tasks

The next packet focuses on **durable resource ownership and recovery**. Before creating or
starting a container, ADRL must record its intent; afterward, it must bind the exact resource,
engine and configuration identities. A lost acknowledgement or client crash must leave an
honest pending state. Recovery may act only on a resource it can establish it owns, including
when the session's content key has been revoked. A name, label or saved host PID alone is not
sufficient authority.

Subsequent gates still include preventing restart/new writers during closure, capturing the
right stopped output, safe archive extraction, output integrity/durability, active-copy erasure,
crash leftovers and an approved image/network/credential profile for a real harness. Container
files live in another storage area, so host-ledger key shredding does not erase that plaintext.
Independent security/evaluation review remains unassigned. Docker administration and a hostile
host/kernel are outside these fixture claims. No stronger privacy or maturity claim follows.

## Evidence, corrections and maturity

The first run completed three container observations, then the client-death case failed because
the driver used a flag supported by `docker attach` but not this version's `docker start`.
The fixture never started in that case. We corrected the invocation; the second run completed
all six observations. Eight containers and two scratch images were created across both runs,
within the frozen limit, and all were removed. Label-specific reconciliation found none remaining.

Self-review also found that the driver had configured a 60-second compiler timeout while the
packet specified 15 seconds for commands. Actual compilations took under three seconds. We
lowered that timeout to 15 seconds and compiled again within it, producing exactly the same
binary. The executed driver and its final one-line correction are recorded separately; no new
container experiment was needed for that deadline correction.

**The implementation remains at its previously verified 759 tests and eleven checks.** We
verified all 300 declared runtime source hashes and did not rerun an unchanged runtime suite.
These six research observations are not added to that test count. No runtime code, API, schema,
workspace fence, routing policy or privacy rule changed. Eight owning ADRs now record the
finding/proposal with prior text and all 77 status/maturity fields preserved. No grade rises.

This moves us from an unspecified containment gap to a concrete candidate and a tested list of
failure modes. It strengthens the path toward trustworthy outcomes for later course correction
and RSI; it does not demonstrate automatic improvement. **Full W3 remains open.**

See the [journey](adrl-implementation-journey.md), [frozen packet](waves/w3-2b2c-writer-boundary.md),
[evidence](research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[probe source](research/writer-boundary-2026-09-08/probe.go),
[driver](research/writer-boundary-2026-09-08/run_probe.py) and
[next packet](waves/w3-2b2d-resource-ownership.md).
