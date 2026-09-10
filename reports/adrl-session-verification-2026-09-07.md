# ADRL now records what was independently checked

**Later implementation, 2026-09-07:** the [first offline verifier comparison](adrl-improvement-experiment-2026-09-07.md)
is now applied with 549 passing tests. The baseline and candidate correctly classified 4/7
and 7/7 curated examples. This implements a bounded part of the proposed improvement workflow;
it does not automate proposal generation, adoption or recursive improvement. Earlier numbers
and roadmap statements below retain their original scope.

7 September 2026 | Applied implementation and verification of the existing pilot task

**ADRL can now place an independent test result beside the coding agent's activity, with a record of what was tested and how.** Previously, its timeline showed tool activity while our acceptance review lived outside the product. The two can now be inspected together. This is the next part of the course-correction loop you asked for: observe the work, check the result, preserve disagreement, then decide what to change.

The implementation is applied in `adrl-core`. All **532 tests** and all six required checks pass; the data inventory covers **249 fields**. The repositories remain uncommitted.

## What you can understand from a session now

Think of a session as two accounts of the same work. The harness reports the actions it took. The independent verifier reports which checks it ran on a captured copy of the code. ADRL keeps both accounts.

| Question | What ADRL now records |
|---|---|
| What did the coding agent do? | Existing tool observations, including reported failures |
| What did we independently check? | An operator-owned task reference, versioned verifier and pinned plan |
| Which code was checked? | References for the source at verification time and the executed snapshot |
| Which checking machinery was used? | Command and executable references, sandbox backend and its implementation-source digest |
| What happened? | Individual check results, elapsed time, and overall passed, failed or indeterminate |
| Did the attempt finish? | Separate started and finished records; an interrupted job can remain started |

A pass means the declared checks passed on an unchanged captured snapshot. It does not mean every requirement was checked. The task reference is supplied by the operator; this first version does not automatically prove that the snapshot was the agent's exact output at task closure.

## The concrete result

We reused the repaired dataset-validator task from the [first live observation pilot](adrl-live-observation-pilot-2026-09-07.md). We made a separate copy of that pilot's ADRL state, preserving the original experiment. No Claude session was launched and no model request or additional provider spend was needed.

The reviewed test files were copied outside the agent workspace and pinned by SHA-256. A separate operator runner loaded those copies against a fresh application snapshot. Its exit mapping distinguishes failed assertions from test or setup errors.

| Measure | Result |
|---|---|
| Distinct tasks checked | 1 existing repaired task |
| Independent verifier jobs in the final check | 2 repeated jobs on that same task |
| Test cases per job | 8, grouped into 3 commands |
| Results | All 8 passed in each job |
| Plan and snapshot identities | Identical across the two jobs |
| Original tool observations | All 18 preserved |
| New verification records | 4: started and finished for each job |
| Copied session timeline | 18 entries before; 22 after |
| Changed files in the task working copy | 0 of 13 |
| New routing decisions, internal outcome events or learning labels | 0 |
| New model requests | 0 |

The CLI wrote the receipts and a real loopback HTTP service returned them in the authenticated timeline. The checks ran through macOS Seatbelt, not a simulated sandbox. An earlier developmental run also passed; the table reports only the final two jobs. Repeated agreement on this one fixture is useful integration evidence, not a statistical estimate of verifier accuracy or a new development-task sample.

## The design changes that matter

**Verification can belong to a session without inventing a routing decision.** In subscription observation mode, ADRL does not route the model request. The old verification path required a route ID. The new path attaches receipts directly to the already authenticated session. The existing route-based verification and learning paths keep their previous semantics.

**The checking plan has its own authority.** A local operator invokes `adrl product verify` with a reviewed plan outside the task workspace. The command validates the existing local binding and exact repository. Harness-authenticated event intake still rejects verification claims. Local keystore and configuration access are part of this authority; a remote verifier role is not implemented. Code running as the same OS user remains within the trusted-host boundary.

**Uncertainty stays visible.** Missing execution support, a timeout, artifact tampering, an unclassified exit or changes to the source/snapshot produce an indeterminate result. Only exit codes explicitly declared by the operator can mean test failure. A poorly designed verifier can still misclassify its own errors, which is why reviewing its exit semantics matters.

**New evidence does not overwrite the old account.** Each run appends its own started and finished records. Rerunning creates another job. There is no automatic resume or adjudication of conflicting results yet. Receipts carry `origin=pilot` and `eligible_for_learning=false`; no label producer reads them.

**The detailed receipt follows session erasure.** It is encrypted under the existing session key. Erasure hides it and prevents new receipts from recreating that key. Raw command output is not stored in the receipt; output references are keyed hashes. The operator's plan, CLI output, exported reports and client outbox have separate retention lifecycles. This does not establish complete deletion of every evidence copy.

## Where this moves product maturity

ADRL is becoming usable as a small, inspectable product loop: a bound session receives activity observations, independent checks add results, and the timeline presents both. This makes it easier to find false-success cases and discuss a concrete decision change.

The new contract has scoped D2 test evidence and one concrete task exercise with two verifier runs. It does not promote the whole product to D3 or D4. We have not measured routing quality, economic benefit, verifier precision across tasks, or reliability across harnesses.

For the product you want, the useful design property is that the receipt format and timeline do not depend on Claude's tool vocabulary. A future OpenCode adapter should be able to use the same session/evidence services. That reuse still needs to be demonstrated; stable multi-harness support and the two-harness/two-protocol release gate remain unmet.

## Important limits we kept explicit

- The existing macOS sandbox denies network and limits writes to scratch, but permits filesystem reads beyond the snapshot except selected credential paths. Its module description was corrected to match the code. This is appropriate only for the reviewed pilot scope; it does not satisfy SAF-007's full read-isolation promise or certify arbitrary untrusted repositories.
- The snapshot excludes Git metadata, virtual environments, Python bytecode and named tool caches. Symlinks are rejected. Interpreter dependencies and the host OS are not frozen. The sandbox implementation digest versions its Python policy code, not the kernel.
- Source and snapshot consistency are checked during capture and after execution. There is no automatic task-close snapshot binding, remote attestation or comprehensive protection against another process with the same OS authority.
- A passing result does not upgrade session-wide outcome coverage from unknown, automatically accept the task, change routing policy or generate a learning label.
- The original live pilot ledger remains unchanged. The extended 22-entry timeline is in the separate verification exercise state; its service has stopped.

## What to run next

1. **Choose five new, small tasks with explicit acceptance criteria.** Pin the Claude executable, model and effort; review and freeze each verifier before the task starts. Keep subscription observation mode for this stage.
2. **Capture the output snapshot at task closure.** Join that identity to the session receipt, so we can distinguish the agent's output from later edits. This is the next implementation gap in attribution.
3. **Include known incorrect and environment-failed examples.** Check that the verifier catches the defect and treats a broken test environment as indeterminate. Repeat checks where flakiness is plausible; keep human review disagreements in the report.
4. **Exercise interrupted delivery and restart, then integrate OpenCode.** Test reuse of the same binding, observation and verification contracts before advertising cross-harness support.
5. **Disposition the evidence in the decision ledger.** For each mismatch, identify whether the task, verifier, integration or routing decision was wrong. Record the amendment and regression check under the owning ADR. Only start routing comparisons after the gateway and provider-access blockers are resolved.

Five tasks are a practical next batch, not a graduation threshold. The first useful measures are delivery completeness, verified outcomes, false-success disagreements and indeterminate results, each with its denominator. Cost and routing claims require a separate matched design.

## Where the changes live

The [product-service guide](/Users/arunmenon/projects/adrl-core/docs/product-services.md) contains the command and plan format. The core command is:

```bash
adrl product verify --connection <connection.json> \
  --workspace <registered-working-copy> --plan <operator-plan.json>
```

Use the same local configuration, ledger and keystore as the session. No running HTTP server is needed to execute checks; the service is needed to read its timeline over HTTP. This command does not start the coding agent.

The applied package changes 14 files, including two additions; all 260 untouched files in the 272-file baseline were preserved. The [implementation diff](research/adrl-session-verification-2026-09-07.patch), [validation and run manifest](research/adrl-session-verification-2026-09-07.json), and [archived operator plan and test artifacts](research/adrl-session-verifier-plan-2026-09-07.json) make the result reviewable. The initial full-suite attempt hit two host-sandbox permission restrictions; the final suite passed with normal macOS access, without weakening those tests.

The Taxonomy update covers MEM-003, MEM-001, MEM-005, MEM-010, SEM-007, TRU-001, SAF-007, LRN-001, EVL-008 and FND-005. The [register consistency check](research/adrl-session-verification-register-validation-2026-09-07.json) verifies all 77 indexed IDs, preserved prior text and matching implementation hashes. Their statuses and prior decisions are preserved. The amendments describe the implemented session application and its limits; they do not convert pilot evidence into learned authority.
