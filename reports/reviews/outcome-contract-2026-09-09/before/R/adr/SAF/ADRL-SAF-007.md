# ADRL-SAF-007 — Verification runs sandboxed, then diffed

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Superseded 2026-09-02 (see replacement) |
| Maturity | D2 Tested, review recommends D1 Code for the post-hoc diff check that exists and D0 Design for the OS-enforced sandbox that the replacement requires; the D2 claim describes a detective control while the decision text describes a preventive one |
| Review verdict | REJECT |
| Tenets | 2, 8 |
| Related decisions | MEM-003, LRN-001, CAS-001, SAF-001, EVL-004 |
| Open questions | Q2 |

## Decision

Verification commands execute inside an OS-enforced sandbox with no network egress, read access limited to the repository snapshot, write access limited to a scratch directory, and protected paths denied at the kernel boundary; a post-execution diff of protected paths and task scope is recorded as evidence but is not the control.

1. The sandbox reuses the harness's own runtime where available (Claude Code's Bash sandbox: Seatbelt on macOS, bubblewrap plus the optional seccomp filter on Linux/WSL2) with `allowUnsandboxedCommands: false`, an empty `network.allowedDomains`, `denyRead` on credential files and `denyWrite` outside the scratch tree; where the harness sandbox is unavailable, verification does not run and the outcome is labelled `unverifiable` (MEM-004), never "verified".
2. Verification runs against a copy (worktree or snapshot) of the working tree at the action boundary, so that a test that mutates files cannot mutate the thing being measured; results are attached to the outcome under MEM-003's enrich-not-overwrite rule.
3. The command set is an allow-list per repository (test runner, linter, type checker, build), not an arbitrary shell; the model's own proposed verification commands are never executed by ADRL's verifier.

## Session verification implementation, 2026-09-07

The session verifier reuses the existing OS runner, captures a separate snapshot and hashes the sandbox driver/policy source in each receipt. Source or snapshot drift is indeterminate; verifier artifacts are pinned and supplied outside the workspace. Real local checks exercised macOS Seatbelt. Its existing profile denies network and limits writes to scratch, but permits other reads except selected credential paths. The module description now matches that implementation.

The full read-isolation requirement in this decision is still unmet. The pilot uses reviewed repository code, not arbitrary untrusted repositories. The interpreter dependency graph, OS/kernel and all external reads are not captured by the snapshot or driver digest. No protective control was weakened and no general sandbox graduation follows.

See the [implementation and maturity report](../../reports/adrl-session-verification-2026-09-07.md),
[validation/source manifest](../../reports/research/adrl-session-verification-2026-09-07.json), and
[operator command guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md).
The applied 14-file package passes 532 tests and all required checks. This is scoped evidence;
architectural status and general D3/D4 maturity remain unchanged.

## Offline verifier improvement implementation, 2026-09-07

The experiment reuses the existing snapshot executor and macOS Seatbelt runner without weakening controls. Real execution ran both reviewed verifier plans on separate captures of each fixed example. Source identity must match the frozen-input scan; artifact and sandbox references are recorded and drift is indeterminate.

The profile still permits many reads beyond the snapshot while denying network and restricting writes to scratch. Keeping plans and state outside case directories is not a confidentiality boundary against arbitrary code. There is no protected secret holdout, frozen dependency graph or untrusted-repository qualification. Full read isolation remains unmet.

See the [plain-language experiment report](../../reports/adrl-improvement-experiment-2026-09-07.md),
[validation and applied source manifest](../../reports/research/adrl-improvement-experiment-2026-09-07.json),
and [operator guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
This is scoped implementation evidence; the architectural status and broader maturity claim
remain unchanged. Prior decision text and dated research findings are preserved below.

## W3.1 retained operator captures, 2026-09-08

The retained-capture scanner uses directory-relative no-follow opens and rejects symlinks, special files, hard links, traversal and observed drift. A directory-swap fault case cannot redirect capture through a symlink. Materialization uses a private disposable directory and non-writable files, with cleanup on normal exit, exceptions and Python cancellation. This is a trusted local capture boundary, not a new hostile-code sandbox or atomic close proof. Startup leftover cleanup and active-copy erasure coordination must precede real capture; no sandbox maturity promotion follows.

See the [plain-language slice report](../../reports/adrl-w3-1-operator-captures-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-1-operator-captures-2026-09-08.json),
[internal implementation](/Users/arunmenon/projects/adrl-core/src/adrl/ledger/capture.py) and
[boundary and remaining work](/Users/arunmenon/projects/adrl-core/docs/operator-captures.md).
All 593 tests and eleven engineering checks pass for the recorded build. This is scoped offline
evidence. Prior decision wording, architectural status and maturity fields remain unchanged.

## W3.2b1 owned process groups, 2026-09-08

W3.2b1 tests cleanup of an owned POSIX process group, including a same-group child that outlives its direct parent. It does not replace the verifier runner or implement this decision's sandbox. A deliberate short-lived detached writer survives cleanup; unrelated writers and outstanding kernel work remain outside the boundary. Every report is ineligible for exact-close attribution and learning. No network/read isolation, hostile-code containment, credential boundary or real task capture is established.

See the [plain-language report](../../reports/adrl-w3-2b1-process-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b1-process-ownership-2026-09-08.json),
[runner](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_owner.py),
[launcher](/Users/arunmenon/projects/adrl-core/src/adrl/core/process_anchor.py),
[tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_process_owner.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/process-ownership.md).
All 669 tests and eleven checks pass on the recorded Darwin build. This is scoped offline
evidence; prior wording, architectural status and maturity fields are preserved. Full W3
and exact task-close attribution remain open.

## W3.2b2b2 process coordination, 2026-09-08

The group-only runner is now connected to a v2 attempt for disposable synthetic execution, with a permanent prelaunch workspace fence and loss-of-authority monitoring. Group cleanup, an erasure marker or a terminal journal entry never grants release or exact task closure. Detached/unrelated writers, path aliases/replacement and active plaintext remain outside this qualification. A stronger whole-writer boundary must be evidenced before real task execution or release.

See the [plain-language report](../../reports/adrl-w3-2b2b2-process-coordination-2026-09-08.md),
[check/source evidence](../../reports/research/adrl-w3-2b2b2-process-coordination-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/attempt_coordinator.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_attempt_coordinator.py) and
[boundary guide](/Users/arunmenon/projects/adrl-core/docs/attempt-coordination.md).
All 759 tests and eleven engineering checks pass, including 35 coordination cases. This is
scoped local evidence with synthetic fixtures and no model calls. Prior wording, architectural
status and maturity remain unchanged. Full W3, safe workspace reuse and real payload capture remain open.

## W3.2b2c writer-boundary research, 2026-09-08

In a constrained synthetic fixture on the existing Docker/LinuxKit engine, a detached child wrote while PID-namespace init remained alive, but its late write stayed absent after init exit or owned-container SIGKILL. Explicit seccomp was observed active despite an unconfined daemon default. This supports an isolated-container candidate, not a complete sandbox or all-workload writer qualification. Host/daemon administration, escapes, nested-namespace/failure recovery and real task profiles remain outside the experiment.

See the [plain-language report](../../reports/adrl-w3-2b2c-writer-boundary-2026-09-08.md),
[experiment and source evidence](../../reports/research/adrl-w3-2b2c-writer-boundary-2026-09-08.json),
[fixture source](../../reports/research/writer-boundary-2026-09-08/probe.go),
[frozen packet](../../reports/waves/w3-2b2c-writer-boundary.md) and
[next ownership packet](../../reports/waves/w3-2b2d-resource-ownership.md).
The corrected research run completed six bounded observations, including negative controls.
The previously passing 759-test/eleven-check runtime source is unchanged; all 300 declared
hashes were reverified, not rerun. This research changes no runtime behavior, architectural
status, maturity, release authority or whole-W3 completion claim. Prior wording is retained.

## W3.2b2d1 stopped resource ownership, 2026-09-08

The optional local container preparation primitive inspects a pinned Linux/arm64 image and requested non-root, no-capability, explicit-seccomp, no-network/no-mount/private-namespace configuration before binding a never-started resource. It refuses a changed or unexpectedly started object during cleanup and exposes no start/exec/restart/kill API. Eight stopped fixture containers were accounted for and removed across two acceptance runs. Inspection does not prove runtime enforcement or sandbox security, and this is not independent security review or qualification for untrusted repositories.

See the [plain-language report](../../reports/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.md),
[checks and source evidence](../../reports/research/adrl-w3-2b2d1-stopped-resource-ownership-2026-09-08.json),
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[unit cases](/Users/arunmenon/projects/adrl-core/tests/unit/test_resource_owner.py),
[local engine cases](/Users/arunmenon/projects/adrl-core/tests/integration/test_resource_engine.py)
and [runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
All 812 tests and eleven engineering checks pass, with 306 declared source hashes unchanged
during the run. This supports the scoped tested behavior only. Prior decision wording,
architectural status and maturity fields remain unchanged; full B2/B3 and W3 remain open.

## W3.2b2d2 launch-contract research and identity gate, 2026-09-08

The retained second create/start pair changed only HostConfig.OomKillDisable from false to null. The selected Docker 27.3.1/API 1.47/Linux/cgroup-v2 engine reports this control unsupported, and pinned Moby source explains the transformation. A capability-specific execution comparison must be tested before introducing start; do not ignore arbitrary configuration changes or weaken the stopped-only check. Both bounded runs failed, zero lifecycle cases are accepted, and no active sandbox or independent security qualification follows.

See the [plain-language progress report](../../reports/adrl-w3-2b2d2-launch-contract-2026-09-08.md),
[failed-run/source evidence](../../reports/research/adrl-w3-2b2d2-launch-contract-2026-09-08.json),
[proposed execution contract](../../reports/waves/w3-isolated-execution-contract-v1.md),
[next identity packet](../../reports/waves/w3-2b2d2-identity-compatibility.md), and the unchanged
[owner](/Users/arunmenon/projects/adrl-core/src/adrl/core/resource_owner.py) and
[runtime limits](/Users/arunmenon/projects/adrl-core/docs/stopped-resource-ownership.md).
No runtime source changed: the 812-test/eleven-check baseline is reused with all 306 declared
hashes verified. No new passing runtime run is claimed. Prior wording, architectural status
and maturity remain unchanged. Active launch, full d/B2/B3 and W3 remain open.

## W3.2 execution identity and launch research, 2026-09-08

The narrowly pinned execution comparator accepts only the observed unsupported OomKillDisable false/null transformation; all other stable controls remain exact. Offline unsafe-control cases and seven bounded engine observations passed. One stopped-output observation verified seccomp filtering, no new privileges and zero effective capabilities. This is synthetic boundary evidence, not independent sandbox security, arbitrary workload containment or a real-harness qualification.

See the [plain-language report](../../reports/adrl-w3-execution-identity-2026-09-08.md),
[research evidence](../../reports/research/adrl-w3-execution-identity-2026-09-08.json),
[comparator](../../reports/research/execution-identity-2026-09-08/execution_identity.py),
[offline cases](../../reports/research/execution-identity-2026-09-08/test_execution_identity.py),
[driver](../../reports/research/execution-identity-2026-09-08/run_probe.py) and
[next runtime packet](../../reports/waves/w3-isolated-launch-runtime.md).
101 offline research cases and seven engine observations pass. The unchanged runtime's
812-test/eleven-check baseline is reused with 306 verified hashes. Prior decision text and
all status/maturity fields are preserved; no grade promotion, independent review or full-W3
completion follows.

## W3.2 one-shot fixture runtime prototype, 2026-09-08

The active prototype admits only the pinned self-authored image layer and fixed command on the specific supported engine/profile, with explicit seccomp and resource controls. It preserves d1 raw binding and accepts only the tested unsupported OOM false/null projection. Offline fault cases pass and three current-runtime engine fault cases passed; normal current-build qualification remains incomplete because stopped creation lost a reply. No arbitrary workload, real-harness or independent sandbox-security qualification follows.

See the [report](../../reports/adrl-w3-isolated-launch-2026-09-08.md),
[checks and failed-run evidence](../../reports/research/adrl-w3-isolated-launch-2026-09-08.json),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[pinned transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[permanent markers](/Users/arunmenon/projects/adrl-core/src/adrl/core/launch_markers.py),
[fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_isolated_execution.py),
[runtime guide](/Users/arunmenon/projects/adrl-core/docs/isolated-execution.md) and
[next diagnosis packet](../../reports/waves/w3-launch-create-receipt-diagnosis.md).
Final offline validation: 861 passed, eight opt-in engine cases skipped, all eleven checks;
315 declared hashes stable. Two engine invocations each had three passes and one failure.
The allowance is closed and all eight fixtures/image are absent. All prior wording and
77 status/maturity fields are preserved. No independent review, grade promotion or full-W3
completion follows.

## W3.2 receipt correction and pinned-engine validation, 2026-09-08

The same fixed synthetic image layer, command, explicit seccomp and engine/capability controls pass the current normal/failed-start/erasure/owner-death workflow. The only transport change separates preparation from <=2-second active I/O; no resource/security limits, identity comparison, permitted workload or network authority are widened. Arbitrary workloads and independent sandbox qualification remain outside scope.

See the [plain-language report](../../reports/adrl-w3-transport-receipts-2026-09-08.md),
[checks and cleanup evidence](../../reports/research/adrl-w3-transport-receipts-2026-09-08.json),
[transport](/Users/arunmenon/projects/adrl-core/src/adrl/core/container_control.py),
[versioned execution policy](/Users/arunmenon/projects/adrl-core/src/adrl/core/execution_control.py),
[coordinator](/Users/arunmenon/projects/adrl-core/src/adrl/core/isolated_execution.py),
[receipt fault tests](/Users/arunmenon/projects/adrl-core/tests/unit/test_create_receipt.py) and
[next custody packet](../../reports/waves/w3-active-copy-custody.md).
Final validation: 895 passed, zero skipped, all eleven checks, 316 stable source inputs;
13 original create receipts and absence confirmations, one image removed. The bounded d2
synthetic lifecycle slice closes. Full B2/B3/W3, real-harness and independent qualification
remain open. Prior wording and all 77 architectural status/maturity fields are preserved.

## Context and rationale

The verifier is code execution, so it gets a leash. Deterministic verification runs tests and checks — arbitrary execution. Unconstrained, it could touch protected paths or mutate the thing it measures. The original decision said verification is "constrained by protected paths and execution policy"; the code reality is that `verifier.py` "checks protected files not changed and changes stayed inside task scope" — that is, it *detects after the fact* whether a protected path was touched. A check that runs after the command has run does not constrain the command; a test suite that exfiltrates the repository over the network, or writes a `~/.claude/settings.json` that widens its own permissions next run, passes the protected-path check cleanly. The decision claimed a preventive property and shipped a detective one, and the D2 label certified the mismatch.

The replacement is built on what the harness already provides. Claude Code's sandboxed Bash tool enforces filesystem and network isolation at the OS level "for every Bash command and its child processes", supports `denyRead`/`denyWrite` rules where a deny holds inside a wider allow, supports a strict mode that ignores the model's `dangerouslyDisableSandbox` escape hatch, and documents the exact failure the original decision missed: with filesystem isolation off, "a sandboxed command can write files that later commands run or read … and use them to widen its own access on the next run". The verifier at the company runs on repositories that include payments code; a test harness with network access and a writable home directory is not a verifier, it is an agent with a different name.

## Adversarial review (2026-09-02)

### Steelman
Verification is the most valuable thing in the evidence pipeline — it is what turns "the model said done" into a cause-clean label (LRN-001) — and it necessarily executes repository code. Naming protected paths and an execution policy is the minimum leash, it is cheap to implement as a post-run check, and the D2 label honestly reflects that the check has tests. The decision is right that the verifier must be constrained; it simply describes the constraint at the policy level and leaves the mechanism to the code.

### Attacks
1. **Detective, not preventive.** `verifier.py` checks *after* execution that protected files were not changed and the diff stayed in scope. By then the command has run with whatever privileges the ADRL process has: read every file on the machine, open network connections, write outside the repository. "Constrained by protected paths" is not what the code does; "audited against protected paths" is.
2. **Network egress is the exfiltration path, and it is unconstrained.** A repository's test suite (or a dependency's post-install hook, or a `conftest.py` the model just wrote) can `curl` the working tree to an external host. Nothing in the decision or code mentions network. For a privacy layer whose entire purpose is to keep code on the machine, a verifier with unrestricted egress is a hole larger than every routing leak in this review combined.
3. **Self-widening writes.** Claude Code's own documentation warns that a command with write access to shell startup files, `$PATH` executables or `~/.claude/settings.json` can widen its access on the next run. A verifier that runs repeatedly in the same environment with a writable home directory is exactly that scenario.
4. **Measuring a moving target.** Tests that mutate fixtures, migrate a local database, or regenerate files change the tree that MEM-003 is about to record as "the state that was verified". Without a snapshot, the verified diff and the recorded diff can differ, and MEM-003's "enrich without overwriting" records an enrichment of the wrong observation.
5. **Who chooses the command?** If the verification command is the one the model proposed in its transcript ("run `pytest -k new_feature`"), the verifier executes model-authored shell. CAS-001 refuses to trust model self-judgement for escalation; the verifier should not trust model-authored commands for evidence either.
6. **"D2 Tested" for an unbuilt control.** The pack states only ONE task has strong test-based verification and automatic verification is not connected to every eligible task. The check that exists is tested; the constraint the decision names is not implemented. The maturity label certified the text, not the behaviour — the failure FND-005 exists to prevent.

### Evidence
- Anthropic, "Configure the sandboxed Bash tool" (Claude Code docs) — OS-enforced filesystem and network isolation (Seatbelt; bubblewrap + socat + optional seccomp); `denyRead`/`denyWrite` with deny-inside-allow semantics; `allowUnsandboxedCommands: false` strict mode; explicit warning that with filesystem isolation off a command can widen its own access on the next run; credential `deny`/`mask` modes; bears on attacks 1, 2, 3 and supports the replacement — https://code.claude.com/docs/en/sandboxing
- Anthropic, "Create custom subagents" (Claude Code docs) — `isolation: worktree` runs an agent in an isolated repository copy with commands restricted to that worktree; precedent for sub-clause 2 — https://code.claude.com/docs/en/sub-agents
- ADRL evidence pack, `02-register-FND-SEM-SAF.md` and `01-overview-tenets-taxonomy.md` — "`verifier.py` checks protected files not changed and changes stayed inside task scope"; "Only ONE task has strong test-based verification"; "Automatic verification not connected to every eligible task"; bears on attacks 1, 6.
- Costa, Köpf et al., "Securing AI Agents with Information-Flow Control" (arXiv 2505.23643) — enforcement must be deterministic and occur *before* the action, not by post-hoc inspection; bears on attack 1 — https://arxiv.org/abs/2505.23643
- Northflank, "How to sandbox AI agents in 2026: MicroVMs, gVisor & isolation strategies" (blog; title from search, not fetched) — survey of sandbox mechanisms for agent code execution; background for the replacement's mechanism choice — https://northflank.com/blog/how-to-sandbox-ai-agents

### Verdict
**REJECT.** Attacks 1, 2 and 6 are each sufficient. The decision as written promises a constraint; the implementation performs an audit; the maturity label certified the promise. For an optimisation layer that would be an amendment; for the *privacy* layer's only component that executes arbitrary repository code with network access, it is a rejection, because the gap is the exfiltration path the rest of SAF exists to close. The replacement does not invent anything: it adopts the harness's own OS-enforced sandbox in strict mode, snapshots the tree (attack 4), and refuses model-authored commands (attack 5). The post-hoc check is retained as evidence — it is useful — but demoted from control to record. The steelman's point that the post-hoc check "has tests" is exactly why the maturity split matters: D1/D2 for the check, D0 for the control.

## Amendments applied

- Replaced "constrained by protected paths and execution policy" with an OS-enforced sandbox specification: no network egress, read limited to snapshot, write limited to scratch, protected paths denied at the kernel boundary.
- Demoted the post-execution protected-path/scope diff from control to recorded evidence.
- Added sub-clause 1 (reuse harness sandbox in strict mode; `unverifiable` when unavailable), sub-clause 2 (snapshot/worktree; MEM-003 attachment), sub-clause 3 (per-repository command allow-list; no model-authored commands).
- Maturity recommendation split: D1 for the existing diff check, D0 for the sandbox control.

## Follow-ups

- [ ] Implement verifier execution via the sandbox runtime (`@anthropic-ai/sandbox-runtime` or equivalent bubblewrap/Seatbelt profile) with: empty `allowedDomains`, `denyRead` for `~/.aws`, `~/.ssh`, `~/.claude`, `.env*`; `denyWrite` outside the scratch tree; `allowUnsandboxedCommands: false`. Fault tests: `curl` to an external host fails; write to `~/.bashrc` fails; read of `~/.aws/credentials` fails.
- [ ] Snapshot: run verification in a git worktree created at the action boundary; assert the recorded diff equals the snapshot diff after a test that mutates fixtures.
- [ ] Per-repository allow-list file for verification commands; CI check that `verifier.py` refuses any command not in the list; golden test that a model-proposed command in the transcript is not executed.
- [ ] Label every outcome where the sandbox was unavailable as `unverifiable`; measurement of the `unverifiable` rate per platform (native Windows is unsupported by the harness sandbox).
- [ ] Re-issue SAF-007's maturity as D0 (control) / D1 (check) in the register; do not use MEM-003 or LRN-001 labels from unsandboxed verification runs as "verified" for graduation gates (EVL-004).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-08 | Recorded versioned creation/active transport separation and passing pinned-engine lifecycle acceptance | Prior decision/evidence preserved; bounded d2 closes, full W3 and grades unchanged |
| 2026-09-08 | Recorded W3.2 fixture launch prototype, offline checks, engine failures and operator cleanup exception | Prior decision/evidence preserved; engine workflow remains unqualified, no status/maturity promotion |
| 2026-09-08 | Recorded W3.2 identity correction and seven accepted bounded launch observations | Prior wording and failed evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d2 failed launch probes, source-explained identity gate and proposed lifecycle | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2d1 stopped ownership, acknowledgement recovery and explicit limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b2c bounded writer-boundary observations and proposed isolated-backend gates | Prior decision wording and evidence preserved; no runtime change or status/maturity promotion |
| 2026-09-08 | Recorded W3.2b2b2 stop coordination, permanent workspace blocking and failure evidence | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.2b1 process ownership and tested cleanup limits | Prior decision wording and evidence preserved; no architectural-status or maturity promotion |
| 2026-09-08 | Recorded W3.1 retained operator capture application, tests and limits | Prior decision wording and evidence preserved; no maturity or architectural-status promotion |
| 2026-09-07 | Recorded applied offline verifier experiment and its limits | Prior decision and evidence preserved; no versioned verifier comparison had been recorded |
| 2026-09-07 | Recorded applied session verification and its tested limits | Prior decision and evidence preserved; the observation pilot had no session-scoped verifier receipts |
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Superseded: post-hoc path check replaced by OS-enforced sandbox with no egress, snapshot execution and command allow-list; check retained as evidence; D2→D0/D1 | "Verification commands are constrained by protected paths and execution policy." |
