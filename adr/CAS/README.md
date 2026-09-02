# CAS — Execution, Cascade, Recovery

**Core question:** How is the choice executed, retried or escalated?
**Owns / does not own:** Owns dispatch, trip-wires, escalation, context transfer across models, stickiness, and fallback recording. Does not own the initial semantic classification (SEM), the rung objective (RTG), or long-term learning (LRN).

## Review summary (2026-09-02)

| ID | Title | Verdict | Maturity (claimed → recommended) | One-line reason |
|---|---|---|---|---|
| ADRL-CAS-001 | Deterministic trip-wires, with measured coverage | AMEND | D3 Shadow → D3 Shadow (thresholds flagged untuned) | "Not self-judgment" is well supported; but counters are blind to the majority failure class (incorrect-but-clean runs), so verifier outcomes become a first-class wire and the miss rate is published. |
| ADRL-CAS-002 | Typed failures, six types, measured attribution | AMEND | D2 Tested → D2 Tested | Register says four types, code has six; ambiguity must resolve away from `task_capability`; attribution precision must be measured before labels feed LRN. |
| ADRL-CAS-003 | Action boundary defined; no re-issue after side effects | AMEND | D2 Tested → D2 Tested (pending golden traces) | Boundary was undefined for parallel tool calls and streaming; the real replay hazard is a transport retry after streamed tool content, and a boundary does not undo inherited side effects. |
| ADRL-CAS-004 | Cross-model handoff: provider-pair rules | AMEND | D3 Shadow → **D2 Tested** | A single "strip reasoning" rule causes a 400 on same-family Anthropic escalation with thinking on; shadow cannot validate provider acceptance. |
| ADRL-CAS-005 | Sticky escalation within an episode | APPROVE | D2 Tested → D2 Tested | Every attack lands on a neighbouring decision (SEM-005 calibration, subagents, served-rung) or is answered by the cost model and hysteresis precedent. |
| ADRL-CAS-006 | Record the served model, not only the served rung | AMEND | D2 Tested → D2 Tested | Caches and signatures follow the model, not the rung; the record needs provenance (gateway may echo the alias) and an explicit state-loss marker. |
| ADRL-CAS-007 | Terminal failure surfaced; ADRL owns zero retries | AMEND | D2 Tested → D2 Tested | "Another automatic retry" needed a layer: ADRL zero, gateway bounded and constrained to rung/pin/streaming rules; "surfaced" must be a protocol error, never a synthetic assistant message. |
| ADRL-CAS-008 | Escalation scope under subagents | PROPOSED (new) | — → D0 Design | Q3's separate decision: per-identity scoping, constraints down at spawn, typed evidence up, budgets hierarchical; interim passthrough made explicit. |

Tally: 6 AMEND, 1 APPROVE, 0 REJECT, 1 PROPOSED. No rejection: each decision's mechanism survived; the defects were undefined boundary conditions (parallel calls, streaming, provider pairs, retry layers) that are exactly where a real flaw would live, as the register itself predicted for CAS-003.

## Cross-cutting findings

1. **The register asked for a replay trace on CAS-003; the trace found two cases, neither of which is an "escalation".** (i) A transport retry after a `tool_use` block has been streamed to the harness re-generates the same intended action with a new id — the harness executes both. (ii) With parallel tool calls, a continuation carrying a *partial* set of `tool_result`s is not a boundary, and the provider docs require all results in one message. Both are closed in CAS-003 and CAS-007 by forbidding any re-issue after first streamed tool content and by defining the boundary as "every `tool_use` id answered". Q7 must confirm the gateway obeys the same rule.

2. **The blind spot in CAS-001 is the majority failure class, quantified.** SWE-agent: 52% of unresolved runs are incorrect implementations vs 23% cascading failed edits; MAST: 21% of failures are verification failures; TheAgentCompany: agents fabricate "shortcuts" that omit the hard part. Counter-based wires cannot see these; only deterministic verification can, and only one task has strong verification today. The consequence for Q2 is direct: the local rung's permitted scope may not exceed the task classes for which a verifier exists, because there the escalation instrument is blind. Meanwhile the "not self-judgment" half is strongly confirmed (no reliable intrinsic self-correction; verbalised confidence overconfident; CoT mentions the decisive hint 25–39% of the time).

3. **Cross-model handoff is a provider-pair problem, not a stripping problem.** Anthropic requires the latest assistant turn's thinking blocks (including `redacted_thinking`) to be echoed unmodified when thinking is on, drops unreadable older-model blocks itself, and lets newer models read older blocks; OpenAI's encrypted reasoning is same-family only; LiteLLM's translation layer has open multi-turn bugs on exactly this seam. CAS-004 is amended to a versioned pair table and its maturity is recommended down to D2 because shadow mode never sends a transformed transcript to a target model.

4. **"Served" must mean model, not rung.** Stickiness exists to protect caches and avoid handoffs; both are per-model facts. A within-rung gateway failover keeps the rung and loses both. CAS-006 now records served model/provider with provenance, and RTG-008 (reviewed alongside) states the gateway contract that makes this observable. This is the concrete Q7 boundary from the CAS side: ADRL needs served identity on every response, no fallback outside rung membership or across a pin, and no retry after first byte.

5. **Retry ownership is the Q7 line.** Google's SRE guidance on multiplicative retries across layers applies exactly: harness × ADRL × gateway. CAS-007 fixes ADRL's own retry count at zero and bounds the gateway's per turn. This should be written into the gateway team agreement as config, not prose.

6. **Register/code drift:** CAS-002 names four failure types; tenet 8 names five; `outcomes.py` has six. The amended text matches the code, and a schema test is proposed so the register cannot drift again silently.

7. **Cross-bucket conflicts found:** CAS-003/007 vs FND-001/004 (a synthetic "could not complete" assistant message would violate transparency and poison the transcript) — resolved by requiring protocol-conformant errors. CAS-005 vs SEM-005 (ratchet toward always-frontier if boundaries never fire) — not a CAS defect; a ratchet-cost metric is added so SEM-005 can be tuned on evidence. CAS-008 vs SAF-002/Q5 (does a pinned child's summary pin the parent?) — flagged to SAF, not decided here.

8. **What the review could not find:** no literature on parent/child escalation semantics with budget propagation for LLM agents (CAS-008 reasons from harness docs and SRE precedent); no LLM-gateway-specific retry literature beyond vendor docs.

## Sources consulted

- Anthropic, "Thinking" (Claude platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking
- Anthropic, "Thinking in tool and multi-turn workflows" (Claude platform docs) — https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
- Anthropic, "Parallel tool use" (Claude platform docs) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use
- Anthropic, "Prompt caching" (Claude platform docs) — https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic (Chen, Benton et al.), "Reasoning models don't always say what they think" (2025) — https://www.anthropic.com/research/reasoning-models-dont-say-think
- AWS, "Understanding intelligent prompt routing in Amazon Bedrock" — https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html
- Aggarwal, Madaan et al., "AutoMix: Automatically Mixing Language Models" (NeurIPS 2024) — https://arxiv.org/abs/2310.12963
- Cemri et al., "Why Do Multi-Agent LLM Systems Fail?" (arXiv 2025) — https://arxiv.org/abs/2503.13657 ; full taxonomy — https://arxiv.org/html/2503.13657v2
- Claude Code docs, "Create custom subagents" — https://code.claude.com/docs/en/sub-agents
- Claude Code docs, "Hooks reference" — https://code.claude.com/docs/en/hooks
- Claude Code issue #5456, "Sub-agents Don't Inherit Model Configuration in Task Tool" — https://github.com/anthropics/claude-code/issues/5456
- Dekoninck et al., "A Unified Approach to Routing and Cascading for LLMs" (arXiv 2024) — https://arxiv.org/abs/2410.10347
- GitHub Docs, "About Copilot auto model selection" — https://docs.github.com/copilot/concepts/auto-model-selection
- Google, Site Reliability Engineering, "Addressing Cascading Failures" — https://sre.google/sre-book/addressing-cascading-failures/
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024) — https://arxiv.org/abs/2310.01798
- IETF, RFC 2439 "BGP Route Flap Damping" — https://www.rfc-editor.org/rfc/rfc2439
- Kadavath et al., "Language Models (Mostly) Know What They Know" (arXiv 2022) — https://arxiv.org/abs/2207.05221
- Kiro issues #8575 / #8903 (show model used in Auto mode) — https://github.com/kirodotdev/Kiro/issues/8575
- LiteLLM, "'Thinking' / 'Reasoning Content'" — https://docs.litellm.ai/docs/reasoning_content
- LiteLLM, "Anthropic" provider docs — https://docs.litellm.ai/docs/providers/anthropic
- LiteLLM issue #27946, "Anthropic → OpenAI conversion drops reasoning_content, breaks multi-turn with reasoning models" — https://github.com/BerriAI/litellm/issues/27946
- MCP blog, "Tool Annotations as Risk Vocabulary: What Hints Can and Can't Do" (2026) — https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
- OpenAI, "Reasoning models" (API docs) — https://developers.openai.com/api/docs/guides/reasoning
- OpenAI, "Prompt caching" (API docs) — https://developers.openai.com/api/docs/guides/prompt-caching
- opencode issue #29879, "encrypted content verification fails after 3-4 tool-calling turns (store: false)" — https://github.com/anomalyco/opencode/issues/29879
- OpenHands, "Stuck Detector" (SDK docs) — https://docs.openhands.dev/sdk/guides/agent-stuck-detector
- OpenHands issue #5355, "Loop detection kills agents that are waiting on long-running processes" — https://github.com/OpenHands/OpenHands/issues/5355
- OpenRouter, "Auto Router" docs — https://openrouter.ai/docs/guides/routing/routers/auto-router
- OpenTelemetry, "Gen AI" semantic-convention attribute registry — https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- Schuster et al., "Confident Adaptive Language Modeling" (NeurIPS 2022) — https://arxiv.org/abs/2207.07061 (consulted; intra-model early exit, not directly applicable to cross-model cascades)
- Stripe (Brandur Leach), "Designing robust and predictable APIs with idempotency" — https://stripe.com/blog/idempotency
- Temporal, "What is idempotency? And why it matters for durable systems" — https://temporal.io/blog/idempotency-and-durable-execution
- Xiong et al., "Can LLMs Express Their Uncertainty?" (ICLR 2024) — https://arxiv.org/abs/2306.13063
- Xu et al., "TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks" (NeurIPS 2025 D&B) — https://arxiv.org/abs/2412.14161 ; failure analysis — https://arxiv.org/html/2412.14161
- Yang et al., "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering" (NeurIPS 2024) — https://arxiv.org/html/2405.15793
