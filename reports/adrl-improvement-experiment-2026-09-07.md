# ADRL: the first measured improvement experiment

ADRL can now test whether a proposed change makes its verifier better, preserve the
comparison, and give us a result to review. The first experiment found three defects
that the current verifier missed. The candidate detected all three and retained the
correct classifications on the other examples.

This is a useful first step toward an adaptive product. It is an operator-run experiment
with an assistant-authored proposal. ADRL does not yet generate proposals itself or
install its own changes. The candidate remains a reviewed experiment artifact; it has
not replaced the verifier used for the earlier Claude pilot.

## What changed in plain language

The earlier work gave ADRL two abilities: observe Claude Code doing a task, and run
separate checks on the resulting code. That raised the next question: **how do we know
those checks are good enough?** A weak verifier can approve broken code and make later
routing experiments look successful when they are not.

This increment lets us compare the existing verifier with a proposed improvement on
the same prepared examples. We tell ADRL the expected answer before execution, freeze
the inputs, and retain every result.

```text
A gap in the checks
        |
        v
Record a proposed change and the improvement it must show
        |
        v
Run the current and proposed checks on the same fixed examples
        |
        v
Keep every result, including uncertainty and disagreement
        |
        v
Recommend review and update the decision ledger
        |
        v
A later human decision may adopt the change
```

The comparison mechanism is implemented. The proposal and examples in this run were
prepared by me; the last adoption step has not happened automatically.

## The experiment we actually ran

We reused the small template-rendering task repaired during the Claude Code pilot. Its
current verifier has eight tests. I proposed three additional tests covering Python
representation conversion, dictionary field lookup, and preservation of the required
literal JSON schema in a supplied prompt template. These requirements follow from the
existing task contract; they do not require a new model call.

I prepared seven separate code examples. Two are correct implementations, including one
that uses a different but equivalent implementation. Four contain deliberate defects.
The last is a broken environment with a missing configuration file. Its proper result
is “cannot determine,” so an environment problem is not confused with a failed assertion.

| Prepared example | Expected classification | Current verifier: 8 tests | Candidate: 11 tests |
|---|---|---|---|
| Existing correct repair | Pass | Pass | Pass |
| Equivalent correct implementation | Pass | Pass | Pass |
| Escaped braces substitute accidentally | Fail | Fail | Fail |
| Representation conversion loses required quotes | Fail | **Incorrectly passes** | Fail |
| Field lookup returns the whole dictionary | Fail | **Incorrectly passes** | Fail |
| Required JSON schema key is changed | Fail | **Incorrectly passes** | Fail |
| Configuration missing from the environment | Cannot determine | Cannot determine | Cannot determine |

**The current verifier classified 4 of 7 examples correctly; the candidate classified
7 of 7 correctly.** The required gain was set to three additional correct examples before
execution, and the candidate met it. It produced no false acceptance or false rejection
on these examples. Both repetitions agreed, with no integrity or execution blockers.

The comparison ran on actual macOS Seatbelt snapshots: seven examples, two verifiers,
two repetitions, **28 verifier trials and 98 command executions**. These are seven
curated variants of one task family, not seven new coding tasks. Repetition does not
increase the distinct-example count. No model calls were made by this experiment.

The result is `candidate_supported`, which means this candidate merits review on this
fixture set. It is not a measured accuracy rate for future tasks. I designed both the
candidate and the visible examples, so this is a mechanism exercise with known defects,
not an independent blind assessment. The next evidence should come from fresh examples
whose expected behavior is reviewed independently of the candidate.

## What is now part of the product

The applied package provides a versioned local proposal and assessment format, a
baseline/candidate runner, an encrypted experiment archive, and CLI commands to prepare,
run, inspect and erase that archive. The callable Python workflow is reusable without
Claude-specific hooks; a public cross-harness experiment API is still future work.

The proposal identifies its predecessor, author/version, hypothesis, affected ADRs,
verifier versions, fixed suite, minimum gain and admitted execution budget. Every trial
records the executable, operator artifacts, source/snapshot and sandbox references.
The comparison also pins its evaluator and snapshot-executor source. Changed inputs,
changed evaluator files, incomplete trials, inconsistent repeats and unavailable
execution cannot be averaged into a successful recommendation.

Execution now shares the same snapshot runner as bound-session verification. The
standalone experiment creates no fake session or routing decision. I also corrected
`product verify` so invalid setup returns exit 2, consistently distinguishing it from
assertion failure, which returns exit 1. The public product API stays at preview 4.

Migration 0006 adds an append-only encrypted archive with a separate experiment key.
This run produced **30 records: one start, 28 trials and one final assessment**. A new
CLI process read the full history successfully. Erasure was tested on a separate copy:
all 30 record skeletons remained, their payloads became unreadable, and the original
archive stayed readable. Exported reports, fixtures and backups have separate retention.

The private experiment archive contains zero product sessions, product events, session
verification rows, routing decisions or outcome events. All assessment results remain
explicitly excluded from learning. Nothing installs a routing policy or changes privacy
rules.

## How this moves maturity

| Capability | Before this increment | Now | What remains to prove |
|---|---|---|---|
| Run independent checks | Available for a bound pilot session | Shared snapshot execution supports sessions and experiments | Automatic binding to the exact task-close output |
| Improve a verifier | Ad hoc manual strengthening | Versioned comparison with complete retained evidence | Fresh task families and independently reviewed expectations |
| Control adoption | Architectural requirement | CLI produces review-only recommendations; no deployment path | A deliberate adoption process and later rollback evidence |
| Learn from experience | Designed and gated | This experiment stays outside training | Appropriate evidence admission and routing comparisons |
| Work across harnesses | Product direction, Claude observation exercised | Experiment logic has no harness dependency | OpenCode reuse, Responses runtime and the stable API gate |

The package passes **549 tests**, up from 532, plus all six required engineering checks.
The field inventory covers **256 persisted fields**. The 13 changed/new files were applied
only after checking the 274-file original source manifest; 267 untouched original files
remained identical. This supports scoped implementation confidence, not general D3/D4
maturity or a production-ready adaptive router. Owning ADR statuses are unchanged.

## Where this sits in the adaptive roadmap

We have implemented an early part of the improvement process: **propose a bounded change,
compare it, preserve evidence, and require review**. The system has not demonstrated
recursive self-improvement: it did not improve the mechanism that generates improvements,
and the candidate has not been promoted automatically.

The next work should proceed in this order:

1. **Bind evidence to the exact completed task.** Preserve the code snapshot at task close
   and link verification to it, so later edits cannot be mistaken for the agent's output.
2. **Challenge the candidate with fresh examples.** Add different tasks, failure modes and
   independently reviewed expected results before adopting it more broadly. Use a protected
   held-out set only once the execution environment can actually keep it protected.
3. **Repeat the observation and verification path with OpenCode.** That tests whether the
   shared product contracts travel across harnesses without a second implementation.
4. **Compare routing choices only once outcomes are trustworthy.** Apply the full routing
   evaluation and graduation decisions, including task quality, costs, latency and privacy
   constraints. This small verifier report does not satisfy those gates.
5. **Automate proposal creation after the evaluation process is dependable.** Proposals
   may then improve tests, thresholds or other bounded artifacts. Improving the proposer
   itself would need its own comparison and evidence; that is the later recursive element.

The current OS sandbox limits writes and denies network, but permits many reads outside
the snapshot. Interpreter dependencies and OS state are not frozen. Accordingly, this
workflow is suitable for these reviewed local examples; it does not establish isolation
for arbitrary hostile code or protect a secret holdout. Interrupted runs may leave partial
histories, and there is no resume protocol yet.

## Report navigation and evidence

Start with the seven-row result table above, then the maturity table. For implementation
or audit detail, use:

- [Operator command guide](/Users/arunmenon/projects/adrl-core/docs/verifier-experiments.md).
- [Validation, applied source hashes and results](research/adrl-improvement-experiment-2026-09-07.json).
- [Frozen proposal, fixtures and verifier source](research/adrl-improvement-inputs-2026-09-07.json).
- [Complete exported experiment history](research/adrl-improvement-history-2026-09-07.json).
- [Implementation diff](research/adrl-improvement-experiment-2026-09-07.patch).
- [Input reconstruction tool](research/reproduce-verifier-experiment.py).
- [Register synchronization validation](research/adrl-improvement-register-validation-2026-09-07.json).

The decision ledger records this as a scoped application of
[EVL-006](../adr/EVL/ADRL-EVL-006.md), with version lineage under
[LRN-005](../adr/LRN/ADRL-LRN-005.md), review authority under
[LRN-007](../adr/LRN/ADRL-LRN-007.md), verifier semantics under
[MEM-003](../adr/MEM/ADRL-MEM-003.md), and the evidence, erasure and evaluation limits in
the related owning records. Prior decision text and research findings are preserved.
