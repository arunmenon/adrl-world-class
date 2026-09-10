# Writer-boundary research fixture

Primary: ADRL-SAF-007 and ADRL-OPS-001. This directory is research input, not an ADRL runtime
backend or part of its default tests. See the [packet](../../waves/w3-2b2c-writer-boundary.md)
and [report](../../adrl-w3-2b2c-writer-boundary-2026-09-08.md) before considering another run.

The recorded experiment used Go 1.25.6, Docker 27.3.1 on the already-running local engine,
LinuxKit 6.10.11, cgroup v2, and the explicit
[Moby 27.3.1 seccomp profile](https://raw.githubusercontent.com/moby/moby/v27.3.1/profiles/seccomp/default.json).
Profile SHA-256: `9c1025c88ccaa517b648da571961838744ea2137f176bfe6a48b21294cae9c76`.
No model calls, remote Docker endpoint, downloaded image or user workspace contents are involved.

`probe.go` is a self-contained static Linux/arm64 fixture. `run_probe.py` cross-compiles with
dependency/network fetching disabled, imports a scratch image, tests four container cases and
two disposable host-file cases, records source/resource identities, and removes only resources
created by that invocation. Use a new private output directory and an explicit local Unix socket.
Any new run needs a new bounded resource allowance: the recorded packet's eight-container limit
was fully used by its two runs. Do not silently repeat it or treat research scripts as a product API.

The final driver differs from the fully executed second-run driver only by reducing the Go
compiler timeout from 60 to 15 seconds. A separate compile completed within 15 seconds and
produced the identical binary. Both driver hashes and that correction are in the evidence.
Do not conflate current source, executed source, successful observations and remaining gates.
