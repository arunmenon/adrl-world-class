# ADRL Decision Register — RTG, CAS

All decisions **Status: Accepted**. Source: Confluence bucket pages, updated Aug 27 2026.

---

## RTG — Routing Intelligence and Economics

| ID | Decision | Maturity |
|---|---|---|
| ADRL-RTG-001 | The policy reasons over three capability/cost rungs: local, cheap cloud, and frontier. | D3 Shadow |
| ADRL-RTG-002 | Within hard constraints, select the cheapest healthy rung likely to complete the task. | D2 Tested |
| ADRL-RTG-003 | Deterministic rules own clear cases; learned intelligence is reserved for the ambiguous middle. | D3 Shadow |
| ADRL-RTG-004 | Local-first is conditional and is used only when a controlled cascade remains feasible. | D2 Tested |
| ADRL-RTG-005 | Runtime optimisation uses expected verified quality, retry risk, latency and cost rather than difficulty alone. | D3 Shadow |
| ADRL-RTG-006 | The current LLM classifier is a fail-safe middle-band advisor, not a safety authority or final learned router. | D3 Shadow |
| ADRL-RTG-007 | The target learned decision is the marginal utility of frontier versus local, with calibrated uncertainty and abstention. | **D0 Design** |
| ADRL-RTG-008 | Capability-rung selection is separate from endpoint/provider selection inside a rung. | D2 Tested |

### In plain terms

**RTG-001 — three rungs, because two is too blunt and five is unmeasurable.** Local (free, private, limited context and capability), cheap cloud, frontier. Two rungs would force every "medium" task into one extreme. Each additional rung needs its own measured capability boundary and its own evidence. Three is what we can actually defend.

**RTG-002 — the load-bearing words are "likely to complete."** Not "cheapest." If the policy optimised for cost alone it would send everything local and rely on escalation to clean up — the developer waits through a failed attempt first. "Likely to complete" makes this a quality decision wearing a cost decision's clothes.

**RTG-003 — most decisions are not close calls.** "Fix this typo" and "design our multi-region failover" do not need a model to adjudicate. Measured on real traffic, only a small minority of turns are genuinely ambiguous. That sets a ceiling on how much a learned router can ever add.

**RTG-004 — never route local into a dead end.** Local is chosen only when, if it fails, we can still escalate cleanly. If a task is already at the edge of the local context window, an escalation later would have nowhere to go. The question is not just "can local probably do this?" but "if local is wrong, is recovery still possible?"

**RTG-005 — difficulty is not the objective; it is one input.** A hard task on a cheap rung fails, retries, and costs more than going straight to frontier. An easy task in a huge, already-cached session may be cheaper to keep where it is than to move. Policy weighs expected verified quality, retry risk, latency and cost. Cache: cheapest-per-turn can be more expensive per session, because switching cloud models breaks prompt-cache reuse exactly when the transcript is largest.

**RTG-006 — there is an LLM in the path today, and it is deliberately not in charge.** It advises on the ambiguous middle only. It cannot open a gate, cannot override a pin, and is not the learned router of RTG-007. Failure mode is "fall back to the deterministic rule."

**RTG-007 — the real target: not "how hard is this?" but "how much does frontier actually buy?"** A classifier that imitates today's heuristics can never beat them. A utility estimator asks: for this task, what is the expected gain from spending frontier tokens? Needs calibrated uncertainty and abstention. None of it is built — D0.

**RTG-008 — "frontier" is a capability, not a model name.** ADRL picks the rung; the gateway picks which model, which provider, and what retry behaviour serves it. FND-002 restated where it bites.

### Scrutinise / Open items
- RTG-002 + RTG-004 together are the guard against local-at-all-costs.
- RTG-005 — challenge whether expected verified quality and retry risk are measurable enough today to route on.
- RTG-006 — confirm you are comfortable with an advisory LLM in the hot path at all.
- RTG-007 is the D0 item and the subject of Q4.
- Prompt-cache economics need to be inside the objective, not reported alongside it.
- The local rung's permitted scope depends on measured capability, not optimism (Q2).

Code map: RTG-001 `router/policy.py`, `router/live_router.py`, runtime registry (local/cheap_cloud/frontier). RTG-002 `router/policy.py` orders feasible routes by cheapest level likely to finish. RTG-003 `router/features.py` (quick features), `router/policy.py` (clear bands), `router/llm_classifier.py` (middle only). RTG-004 `router/policy.py`, `router/live_router.py`. RTG-005 `router/outcomes.py`, `router/telemetry.py`, `reports/p1-utility-shadow.md` — "D3 Shadow, partial target: measurement exists; a complete learned utility predictor does not." RTG-006 `router/llm_classifier.py`, `router/backends.py`, `router/shadow_classifier.py` (bake-off and shadow reports). RTG-007 `router/learning_contract.py`, `config/learning-contract-v1.json` only. RTG-008 `router/backends.py` maps roles to endpoints.

---

## CAS — Execution, Cascade, Recovery

| ID | Decision | Maturity |
|---|---|---|
| ADRL-CAS-001 | Escalation is triggered by deterministic post-call trip-wires, not free-form model self-judgment. | D3 Shadow |
| ADRL-CAS-002 | Failures are typed as task difficulty, model dialect/capability, infrastructure, or policy so each signal reaches the correct owner. | D2 Tested |
| ADRL-CAS-003 | Escalation occurs only at a controlled action boundary so partial tool execution is not replayed blindly. | D2 Tested |
| ADRL-CAS-004 | Cross-model continuation preserves tool IDs/results, removes private reasoning, and adds a short handoff note. | D3 Shadow |
| ADRL-CAS-005 | Escalation is sticky within an episode; only a conservative episode boundary may lower the rung. | D2 Tested |
| ADRL-CAS-006 | Sticky state records the rung that actually served the response, including transport fallback. | D2 Tested |
| ADRL-CAS-007 | Failure at the top rung, or on a privacy-pinned route, is surfaced rather than hidden by another automatic retry. | D2 Tested |

### In plain terms

**CAS-001 — we watch what the model does, not what it says about itself.** Escalation fires on mechanical signals: the same tool call issued repeatedly, schema-invalid tool calls, tool-error loops, repeated failed test runs, no progress across many actions. We deliberately do not ask the model "are you struggling?" — self-assessment is unreliable in both directions and adds a paid call. Blind spot: a methodical-but-wrong run that never errors may never trip a failure counter.

**CAS-002 — "the local model failed" is usually four different statements.** Bad answer (difficulty). Could not emit the exact-string edit format (dialect/capability). Endpoint down (infrastructure). Privacy pin blocked the route (policy). If all recorded as "task too hard for local," the training signal in MEM/LRN is poisoned at the source.

**CAS-003 — you cannot escalate in the middle of a tool call.** If the local model has just issued a write, the write has executed, and the result is coming back, switching models there means the new model inherits a world where side effects already happened but its own reasoning did not produce them. Escalation waits for a clean action boundary. Most safety-critical decision on the page: get it wrong and you get duplicated writes or migrations applied twice.

**CAS-004 — hand over the chart, not the patient's story again.** On escalation, the stronger model receives tool IDs and tool results already gathered. Exclusions: previous model's private reasoning is stripped (thinking blocks and encrypted reasoning items do not transfer across providers and would be rejected), and a short handoff note is added.

**CAS-005 — escalate up, stay up, and only come down on a real boundary.** Without stickiness you get flapping — paying the switch cost repeatedly and destroying the cache each time.

**CAS-006 — record what happened, not what you asked for.** The router may choose "cheap cloud," the transport layer may fail over elsewhere. If sticky state stores intent, the next continuation is routed at a rung that is not actually serving. Runtime twin of OPS-006.

**CAS-007 — at the end of the ladder, tell the truth.** If frontier fails, or a privacy-pinned route fails, surface the failure instead of quietly retrying.

### Scrutinise / Open items
- CAS-003 is where a real flaw would live. Trace an escalation through a tool-call sequence and try to construct a case where a side effect could be replayed.
- CAS-001's blind spot — methodical-but-wrong runs. Is a failure-counting trip-wire the right instrument for reasoning models?
- CAS-002 is the seam with MEM.
- CAS-004's stripping rule — confirm removing private reasoning is sufficient for cross-provider handoff, and the handoff note is enough context.
- Escalation safety under subagents — parent and child in flight concurrently (Q3).
- No live pilot: all tested or shadowed, never exercised under real escalation pressure.
- Trip-wire thresholds have not been tuned against reasoning-model behaviour.

Code map: CAS-001 `router/tripwires.py`, `router/escalation_controller.py`, proxy. CAS-002 `router/outcomes.py`, `router/tripwires.py`, `router/rule_health.py`. CAS-003 `router/escalation_controller.py` + proxy wait for clean action boundary. CAS-004 `router/escalate.py`. CAS-005 `router/state.py`, `router/episode.py`, escalation controller. CAS-006 proxy observes transport fallback, updates `router/state.py`; `tests/test_router_proxy.py`. CAS-007 `router/escalation_controller.py`, `router/live_router.py`, proxy.
