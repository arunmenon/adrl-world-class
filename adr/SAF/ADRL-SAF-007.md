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
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Superseded: post-hoc path check replaced by OS-enforced sandbox with no egress, snapshot execution and command allow-list; check retained as evidence; D2→D0/D1 | "Verification commands are constrained by protected paths and execution policy." |
