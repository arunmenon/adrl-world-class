# Fable workflow review

Scope: skill design only, not repository audit. Claude returned `claude-fable-5-1` main-model usage plus an auxiliary Haiku usage entry. No reviewer tools were enabled. CLI may include automatic working-directory metadata; no source-file inspection occurred. The reported dollar figure is list-price usage metadata, not proof of extra subscription billing.

The workflow is sound in intent and mostly enforceable by process discipline, but it has four material gaps.

**Material flaws**

- **Coordinator is undefined.** The packet, the frozen scope, and the "limited accessible snapshot" are assembled by an unnamed coordinator, which in practice is Codex. The implementer then controls what the reviewer sees. Fix: the reviewer gets a full repository checkout at a named commit, and any exclusion is listed in the packet so the reviewer can contest it.
- **No freeze mechanism.** The skill demands "frozen input identity" and "source hashes," but the register currently has dozens of modified and untracked files. Require a commit or tag before any post-wave review. Without it, "updates after the reviewed snapshot" cannot be detected.
- **Severity is not owner-locked.** Blocking depends on critical/high severity, but nothing says who may change it. If Codex can downgrade a finding in the register, the block disappears. Rule: reviewer severity stands until the product owner rules.
- **Status vocabulary conflicts.** "Awaiting-independent-review" appears in the reconcile section but not in the enumerated status list, which has both `unavailable` and `awaiting-recheck`. Pick one set. Also, the dated 7 to 8 September instruction will go stale inside a durable skill, which contradicts the skill's own no-hardcoding rule.

Smaller point: reviewer identity rests on metadata the coordinator records. The owner should be able to verify the session in their own Claude account history, otherwise "no relabeled subagent" is unenforceable.

**Scenarios**

1. **Tests pass, reviewer unavailable.** Wave status becomes awaiting-independent-review. Passing tests are implementer evidence, not acceptance. Codex may commit the snapshot, build the packet, and do a self-review labeled non-independent. It may not claim completion, promote maturity, or start dependent gated work. No fallback model, no relabeled subagent. Only an explicit owner override advances it, with the limitation recorded.

2. **Reviewer requests a paid experiment.** Record it as a finding with severity and what it would resolve. Disposition is deferred-with-reason or unresolved pending owner authorization. Nobody runs it or spends on it. If the finding is high severity and the experiment is the only way to resolve it, the wave stays blocked rather than passed.

3. **Implementer disputes a high finding.** Disposition is disputed-with-evidence, both positions preserved, severity unchanged. Codex supplies reproduction evidence against the finding, the reviewer gets one recheck. If it remains unresolved after the round limit, escalate to the owner with a concrete decision. The finding still blocks the completion claim throughout.

4. **Manual routing fix called RSI.** That is a mislabel and an evidence-integrity finding. A developer patch during a review wave is a development change. It does not demonstrate ADRL runtime self-improvement, adaptive routing, or D-grade readiness. Relabel it, log it in the CHANGELOG as implementer work, and exclude it from any RSI or maturity claim.
