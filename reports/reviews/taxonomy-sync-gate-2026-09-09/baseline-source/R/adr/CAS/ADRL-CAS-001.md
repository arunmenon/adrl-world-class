# ADRL-CAS-001 — Deterministic trip-wires, with measured coverage

| Field | Value |
|---|---|
| Bucket | CAS — Execution, Cascade, Recovery |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D3 Shadow, review recommends D3 Shadow (trip-wires have post-call shadow evidence; the amendment adds a coverage measurement and a verifier-backed wire that are D2 work, and notes thresholds are untuned for reasoning models) |
| Review verdict | AMEND |
| Tenets | 5, 8 |
| Related decisions | CAS-002, CAS-003, CAS-007, RTG-004, MEM-002, MEM-003, SAF-007, LRN-001 |
| Open questions | Q2, Q3 |

## Current implementation evidence, 2026-09-08: routing diagnostic

Invented repeated-tool observations fired the existing tripwire in a real-controller demonstration. This confirms the tested signal path only; it measures neither organic failure coverage nor task recovery quality. The broader W7.0 matrix tests routing input sensitivity, not live tool execution.

[Report](../../reports/adrl-routing-in-action-2026-09-08.md) · [raw traces](../../reports/research/routing-demonstration-2026-09-08/results.json) · [next correction packet](../../reports/waves/routing-decision-quality.md). The focused 135 routing/cascade/learning tests pass; all 316 runtime inputs match the previous full build. Architectural status, maturity and decision wording are unchanged.

## Decision

Escalation is triggered by deterministic post-call trip-wires, not free-form model self-judgment — where the trip-wire set includes deterministic verification outcomes (failed tests, lint, protected-path violations) alongside loop, schema and tool-error counters, thresholds are versioned and tuned per rung, and the miss rate of the set against verified failures is measured and published as the instrument's known blind spot.

1. Wire classes: (a) repeated identical or alternating tool calls; (b) schema-invalid or dialect-invalid tool calls (typed `harness_dialect`, CAS-002); (c) tool-error repetition; (d) attempt-budget exhaustion with no verifiable progress (RTG-004 clause 1c); (e) deterministic verifier failure where a verifier exists for the task (MEM-003, SAF-007). Class (e) is the only wire that can catch a methodical-but-wrong run and is therefore first-class, not enrichment.
2. Thresholds are per rung and per wire, versioned in policy config, recorded on the outcome row when they fire, and tuned against reasoning-model traces (long thinking, few tool calls) as well as chatty local traces before any live exposure.
3. Coverage: the fraction of `closed_final` verified failures on which no wire fired is reported on the scorecard as the trip-wire miss rate; the local rung's permitted scope (Q2) may not exceed task classes for which class (e) verification exists, because there the instrument is blind.
4. Signals from the harness are admissible as wires when mechanical (e.g. Claude Code `PostToolUseFailure` hooks, MCP `is_error` tool results); model-authored text (confidence statements, "I am done") is never a wire.

## Context and rationale

We watch what the model does, not what it says about itself. Escalation fires on mechanical signals: the same tool call issued repeatedly, schema-invalid tool calls, tool-error loops, repeated failed test runs, no progress across many actions. We deliberately do not ask the model "are you struggling?" — self-assessment is unreliable in both directions and adds a paid call. The literature is now firm on the second point: models do not reliably self-correct without external feedback, verbalised confidence is overconfident, and reasoning models omit decisive information from their chain of thought most of the time. The amendment addresses the register's own stated blind spot — the methodical-but-wrong run — with the only mechanical instrument that can see it: the deterministic verifier. SWE-agent's error analysis puts a number on the blind spot: about half of unresolved runs are *incorrect implementations*, not loops or failed edits. A counter-only trip-wire set is therefore structurally blind to the largest failure class, which is acceptable only when that blindness is measured and the local rung's scope is drawn where verification exists.

## Adversarial review (2026-09-02)

### Steelman
Mechanical wires are explainable, testable with fixtures, immune to prompt injection, and cost nothing per turn. Production agents (OpenHands' stuck detector, SWE-agent's linting guard) use exactly these signals. The alternative — asking the model — is contradicted by the self-evaluation literature and adds a paid, unfaithful call.

### Attacks
1. **The blind spot is the majority failure class, not an edge case.** SWE-agent: 52.0% of unresolved instances are Incorrect or Overly-Specific Implementation; cascading failed edits are 23.4%. MAST across 1,600 multi-agent traces: task-verification failures are 21.3%, step repetitions 17.1%. Counters catch the loop class; they do not catch the run that edits the wrong function cleanly, passes no tests because it ran none, and stops. TheAgentCompany reports agents that "create fake 'shortcuts' that omit the hard part of a task" — a clean, error-free failure.
2. **Reasoning models change the signal profile.** A model with a large thinking budget issues fewer, more deliberate tool calls; loops become rarer, silent wrong answers relatively commoner. The register admits "trip-wire thresholds have not been tuned against reasoning-model behaviour". Thresholds tuned on chatty local traces will under-fire on frontier and over-fire on local, inverting the intended asymmetry.
3. **Counter wires false-positive on legitimate repetition.** OpenHands issues #5355 and #10350: loop detection "kills agents that are waiting on long-running processes" — polling a build, re-running a flaky test, repeatedly reading a log file. A false escalation is a paid rung switch with a cold cache (RTG-009) and a handoff (CAS-004); the rate must be measured.
4. **Verification is listed in the plain-terms text but is not a decision-level wire.** The decision sentence says "post-call trip-wires"; "repeated failed test runs" appears only in the explanation, and only *repeated* failures — a single verifier failure on a task with a deterministic check is the strongest signal the system has and should fire on its own. Only ONE task currently has strong test-based verification, so today this wire covers almost nothing.
5. **Self-judgment is rejected, but harness-mechanical signals are not admitted.** Claude Code exposes `PostToolUseFailure` and `Stop` hooks with `tool_name`, `tool_input`, and (inside subagents) `agent_id`; MCP tool results carry `is_error`. These are deterministic signals ADRL's proxy may not see on the wire (a hook runs in the harness), yet the decision does not say whether they count.

### Evidence
- Yang et al., "SWE-agent" (NeurIPS 2024) — 52.0% of unresolved instances Incorrect/Overly-Specific Implementation; 23.4% cascading failed edits; linting guard prevents error propagation (attacks 1, 4) — https://arxiv.org/html/2405.15793
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2025) — MAST: step repetitions 17.14%; task-verification failures 21.30% (premature termination 7.82%, no/incomplete verification 6.82%, incorrect verification 6.66%) (attack 1) — https://arxiv.org/html/2503.13657v2
- Xu et al., "TheAgentCompany" (NeurIPS 2025 D&B) — agents "create fake 'shortcuts' that omit the hard part of a task" (attack 1) — https://arxiv.org/html/2412.14161
- OpenHands, "Stuck Detector" — action-observation 4+, action-error 3+, monologue 3+, alternating 6+; semantic comparison ignoring ids/timestamps (steelman, attack 2) — https://docs.openhands.dev/sdk/guides/agent-stuck-detector
- OpenHands issue #5355, "Loop detection kills agents that are waiting on long-running processes" (attack 3) — https://github.com/OpenHands/OpenHands/issues/5355
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024) — "LLMs struggle to self-correct their responses without external feedback, and at times, their performance even degrades" (steelman) — https://arxiv.org/abs/2310.01798
- Xiong et al., "Can LLMs Express Their Uncertainty?" (ICLR 2024) — verbalised confidence is overconfident; no elicitation method consistently better (steelman) — https://arxiv.org/abs/2306.13063
- Chen et al. / Anthropic, "Reasoning Models Don't Always Say What They Think" (2025) — Claude 3.7 Sonnet verbalised the hint it used 25% of the time, DeepSeek R1 39%; CoT is not a reliable monitor (steelman, attack 2) — https://www.anthropic.com/research/reasoning-models-dont-say-think
- Kadavath et al., "Language Models (Mostly) Know What They Know" (2022) — P(True) self-evaluation is calibrated in-distribution for large models but "struggle[s] with calibration of P(IK) on new tasks" — the strongest case *for* self-signals, and still not a mechanical wire (steelman caveat) — https://arxiv.org/abs/2207.05221
- Claude Code, "Hooks reference" — `PostToolUseFailure`, `Stop`, `SubagentStart/Stop`; hooks run inside subagents with `agent_id` (attack 5) — https://code.claude.com/docs/en/hooks
- Aggarwal, Madaan et al., "AutoMix" (NeurIPS 2024) — few-shot self-verification is "noisy" and needs a POMDP router to be usable; the paper is the best case for self-verification and still treats it as a noisy observation, not a trigger (steelman) — https://arxiv.org/abs/2310.12963

### Verdict
**AMEND.** The "not self-judgment" half is strongly supported and stands. Attack 1 lands hard: the blind spot is not marginal, and the decision must promote deterministic verification from enrichment to a first-class wire and publish the miss rate — otherwise the local rung is being widened (Q2) on an instrument that cannot see half of its failures. Attacks 2 and 3 land as tuning obligations (clause 2, follow-ups). Attack 4 is the concrete form of attack 1. Attack 5 lands: mechanical harness signals should be admissible, and the text now says which are and which are not.

## Amendments applied
- Added: trip-wire set includes deterministic verification outcomes; thresholds versioned and per rung; miss rate measured and published.
- Added clauses 1–4 (wire classes incl. verifier; per-rung thresholds tuned on reasoning traces; coverage gate tied to Q2; harness-mechanical signals admissible, model text never).

## Follow-ups
- [ ] Wire `verifier.py` / `live_verification.py` failure into `tripwires.py` as class (e); golden test: single verifier failure → escalation offered at the next action boundary.
- [ ] Report trip-wire miss rate (verified failures with no wire fired) and false-fire rate (wire fired, turn later `closed_final` success) on the shadow scorecard, split by rung.
- [ ] Replay the shadow corpus with a reasoning-model trace subset; tune per-rung thresholds; record the tuning run id in policy config.
- [ ] Add a long-running-command allowance (same command, changing observation) to avoid the OpenHands #5355 false positive.
- [ ] Decide whether Claude Code hook events are ingested (sidecar) as wires; if yes, add `PostToolUseFailure` fixtures to `tests/fixtures/handshakes`.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: verifier outcomes made a first-class wire; per-rung versioned thresholds; miss rate published; harness-mechanical signals admissible | "Escalation is triggered by deterministic post-call trip-wires, not free-form model self-judgment." |
| 2026-09-08 | Added scoped offline routing-diagnostic evidence and limitations; behaviour and grades unchanged | Decision wording retained unchanged; prior implementation/research notes preserved. |
