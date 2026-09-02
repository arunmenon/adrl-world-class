# ADRL — Open Questions for Review (Aug 27 2026)

Q1 — Build vs. buy. Amazon Kiro ships an auto-router across Bedrock models; vendors converging on routing. Lean: keep local decision + one-way privacy pin in-house; open to external router for cloud-to-cloud choices. Ask: where is the boundary between commodity routing and our differentiator?

Q2 — Local rung's safe zone. Savings case leans on local; pressure to widen. Local-model reliability on realistic files not established. Lean: draw by capability AND risk — mechanical, low-risk, small-context, small-diff only; nothing security-sensitive; nothing touching deployment; verified non-inferior to cheap-cloud on that slice first. Ask: categories never allowed on local regardless of accuracy?

Q3 — Escalation under subagents. Parent and subagents in flight simultaneously; escalating one risks split-brain; escalating both multiplies cost. Lean: v1 passthrough, shadow-log, nested escalation as a separate decision. Ask: does passthrough leave an unacceptable gap? cleaner parent/child identity model?

Q4 — Is marginal utility the right objective? Deterministic rules own most decisions; ambiguous band is a minority. Lean: keep objective simple and cache-aware first; earn complexity with evidence. Ask: bar for adding a learned component at all?

Q5 — Session-scoped one-way privacy pin. Too coarse → one flagged file forces whole long session local → developers disable the layer. Too fine → leakage across boundary. Lean: keep one-way + session; invest in scanner precision; surface conflicts. Ask: is session the right unit? security bar for ever releasing a pin?

Q6 — Evidence before live routing. Representativeness, not volume, is binding. Lean: verified cause-clean labels on representative traffic; non-inferior vs always-local, always-frontier, current heuristics; cost measured after prompt-cache effects. Ask: what would you need to see?

Q7 — Ownership boundary with the gateway (LiteLLM; gateway team). Overlap on health, retries, fallback, spend controls. Lean: semantic policy in ADRL, mechanical execution in gateway; shared telemetry and model access. Ask: where to draw the line on retry and fallback ownership?
