# ADRL-SAF-002 — One-way pin, durable, lineage-scoped, audited release

| Field | Value |
|---|---|
| Bucket | SAF — Safety, Privacy, Hard Constraints |
| Status | Accepted · amended 2026-09-02 |
| Maturity | D2 Tested, review recommends D1 Code — the pin is tested as an in-memory rule, but the property the decision promises ("stays local-only") is not implemented: pin state lives in a single-process Python dict and does not survive a proxy restart, and it does not cover passthrough, utility or subagent traffic |
| Review verdict | AMEND |
| Tenets | 2, 6 |
| Related decisions | SAF-001, SAF-003, SAF-004, SAF-005, SEM-001, SEM-002, SEM-004, SEM-006, FND-004, MEM-001, MEM-005 |
| Open questions | Q5 |

## Decision

Privacy pinning is one-way for the session lineage and durable across process restarts; once local-only, every content-bearing request in that lineage — turns, continuations, utility, passthrough and descendant subagents — stays local-only, and the only release is an explicit, reason-coded, audited human action that can never be taken by ADRL, the gateway, a heuristic, a learned policy, an episode boundary or a failure fallback.

1. *Durable* means pin state is written to the ledger (MEM-001) keyed by the hashed session key before the pinning request is forwarded, and is reloaded on proxy start; a restart never unpins.
2. *Lineage* means the session key plus all descendant agent identities (SEM-006); a pin taken by a child does not pin its parent or siblings, a pin taken by a parent pins all descendants from that moment.
3. *Audited human release* mirrors push-protection practice: the developer is shown the flagged span and detector, chooses one reason (`false_positive`, `test_fixture`), the release is recorded in the ledger with actor, reason, detector and span hash, and the release applies to that finding only — a subsequent finding re-pins. Release is disabled by policy for repositories carrying a restricted data classification (SAF-008, Proposed).
4. The pinning question "did this lineage's content ever leave the machine?" is answerable from the ledger alone (SAF-009, Proposed).

## Context and rationale

One-way, because the alternative is unauditable. If a session touches something sensitive it is pinned local-only for the rest of the session and cannot be quietly released; a pin that can lift itself makes the safe state depend on a chain of later judgements. The cost is real — one flagged file can make a long session local — which is why scanner precision (SAF-003) is the highest-leverage knob.

The amendment does three things. It makes the pin *durable*, because the code reality is a single-process dict: the sentence "once local-only, it stays local-only" is currently false across a proxy restart, a crash, or a redeploy, while the harness keeps sending the same session. It makes the pin *cover the traffic that actually carries the content*: `count_tokens` bodies (the full prompt, ~72% of wire volume), compaction and title requests, and forked subagents all leave the machine under the original interims of SEM-001/004/006. And it answers Q5's second half — the security bar for release — with the industry's answer for the same trade-off: block by default, allow an audited human bypass with a reason code, never an automatic one. Session scope is kept (Q5's first half). The information-flow literature calls the over-approximation that follows from strict label propagation "label creep", and the tools that mitigate it work by identifying which inputs actually influenced an output — something that cannot be done for a transcript that will be sent whole to the next model. Once a secret is in the context window it is in every subsequent request; the transcript, not the file, is the unit that leaves the machine, and a per-file pin would be a fiction.

## Adversarial review (2026-09-02)

### Steelman
A monotone, session-scoped pin is the only design under which "did this code leave the machine?" has a one-bit answer. It is the high-water-mark policy from classical mandatory access control applied to the one object that actually crosses the boundary — the transcript — and it composes with everything else in the register because it is a pure constraint on the permitted set. Every alternative either requires trusting a later judgement (release logic) or pretends the transcript can be partially exported (per-file pins).

### Attacks
1. **The pin is not durable, so the promise is false today.** Session-to-route tracking is in a Python dict. Restart the proxy mid-session and the harness continues with the same session key against a router that has never heard of it; the next continuation carries the pinned transcript to the cloud gateway. The decision claims D2 for a property the implementation does not have.
2. **Three request classes leak around the pin.** `count_tokens` (full prompt) is passthrough "unchanged"; compaction and title generation (transcript and user text) are utility calls; forked subagents (entire conversation) are passthrough under the SEM-006 interim. All three are content-bearing and none is covered by "the session stays local-only" as implemented. A pin that covers `/v1/messages` and nothing else is a pin on the minority of bytes.
3. **Label creep is the known cost, and the register has no mitigation beyond "better scanner".** LOMAC-style floating labels and strict IFC propagation are documented to over-approximate; the permissive-IFC work on LLMs reports 56–85% label improvement is available in principle by tracking influence — but only where outputs can be regenerated from reduced contexts, which a coding harness's transcript cannot. So session scope is forced, and the only levers are scanner precision (SAF-003) and a *human* release path. The original decision closes the second lever entirely, which the register itself admits pushes developers to disable the layer.
4. **Pin survives nothing the harness does.** `/clear`, `--resume`, compaction, and a new process may change the session key or the transcript. If the key changes, the pin is orphaned; if the transcript is compacted, the secret may or may not be in the summary and nobody can check. The decision needs lineage rules (sub-clause 2) and should treat compaction as *not* a release.
5. **The gateway can un-pin by fallback.** LiteLLM context-window fallbacks can move an overflowing local request to a larger model. Unless the fallback group for pinned traffic is local-only (FND-002 as amended), the mechanical layer releases the pin without any policy deciding to.
6. **Unreleasable pins on false positives produce the worse outcome.** Secret-detection tools measured on a common benchmark range from 25% to 75% precision, with the best-recall tool at 46% precision. At session scope, roughly half of pinned sessions are pinned on a false positive. The register acknowledges the developer's rational response is to disable ADRL. GitHub push protection faced the identical trade-off and chose block-plus-audited-bypass with reason codes; Purview requires justification to downgrade a label. An unreleasable pin is not the security-maximal choice if it drives the layer off.

### Evidence
- ADRL evidence pack, `01-overview-tenets-taxonomy.md` — "Session-to-route tracking is held in a Python dict (single-process)"; bears on attack 1.
- Anthropic, "Token counting" (Claude Platform docs) — `count_tokens` carries system, tools, messages, thinking blocks; bears on attack 2 — https://platform.claude.com/docs/en/build-with-claude/token-counting
- Anthropic, "Create custom subagents" (Claude Code docs) — forks inherit the entire conversation; bears on attack 2 — https://code.claude.com/docs/en/sub-agents
- Wikipedia, "LOMAC" — low-water-mark MAC with "subject demotion via floating labels"; classical precedent for a monotone label that only ever moves one way; supports the steelman and names the drift cost (attack 3) — https://en.wikipedia.org/wiki/LOMAC
- "Permissive Information-Flow Analysis for Large Language Models" (arXiv 2410.03055, 2024) — strict propagation labels output with the most restrictive input label ("label creep"); influence-based relabelling recovers 56–85% permissiveness by regenerating on reduced contexts; bears on attack 3 — https://arxiv.org/html/2410.03055
- Costa, Köpf et al., "Securing AI Agents with Information-Flow Control" (arXiv 2505.23643, 2025) — confidentiality labels tracked dynamically through agent steps and enforced deterministically; supports per-request propagation (sub-clause 2) — https://arxiv.org/abs/2505.23643
- Basak et al., "A Comparative Study of Software Secrets Reporting by Secret Detection Tools" (arXiv 2307.00714, 2023) — precision 75% (GitHub), 46% (Gitleaks), 25% (commercial); recall 88% (Gitleaks), 67%, 52%; bears on attack 6 — https://arxiv.org/abs/2307.00714
- GitHub Docs, "About push protection" — blocks the push, allows bypass with one of `false positive`, `used in tests`, `fix later`; every bypass creates an alert, an audit-log event and owner email; bears on attack 6 and sub-clause 3 — https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection
- Microsoft Learn, "Learn about sensitivity labels" (Purview) — removing or downgrading a label requires a justification, recorded for review; label persists with the content as metadata; bears on attack 6 and Q5 — https://learn.microsoft.com/en-us/purview/sensitivity-labels
- LiteLLM, "Fallbacks (Provider Failover)" — context-window fallbacks re-route on input size; bears on attack 5 — https://docs.litellm.ai/docs/proxy/reliability

### Verdict
**AMEND.** Attacks 1 and 2 are code-reality contradictions of the decision's central promise and drive the maturity recommendation down to D1: the rule is implemented, the property is not. Attack 5 is closed by FND-002's amendment and restated here. Attacks 3 and 6 together answer Q5: session scope is forced by the transcript model, so the only honest relief valve is an audited human release with reason codes, which is what the two most widely deployed precedents (push protection, Purview) do. The "one-way" principle is preserved exactly for every automated actor; the amendment adds a human path that is *recorded*, which is the register's own criterion ("the alternative is unauditable" — an audited release is, by definition, auditable). Attack 4 is closed by lineage rules and the explicit statement that compaction does not release.

## Amendments applied

- Added "session lineage", "durable across process restarts", and the enumeration of covered request classes.
- Replaced "cannot be quietly released" (rationale) with an explicit list of actors that can never release, plus an audited human release path (sub-clause 3).
- Added sub-clause 1 (durability via ledger write-before-forward and reload on start).
- Added sub-clause 2 (lineage direction of inheritance).
- Added sub-clause 4 (ledger answerability; links to proposed SAF-009).
- Maturity recommendation lowered to D1 until durability and coverage are implemented and tested.

## Follow-ups

- [ ] Implement pin persistence: write `pinned` to the ledger keyed by hashed session key *before* forwarding the pinning request; reload on start. Fault test: pin → SIGKILL proxy → restart → next continuation is local-only.
- [ ] Golden tests for coverage: `count_tokens`, compaction, title, fork subagent, nested subagent on a pinned lineage → none reaches the gateway.
- [ ] Implement the release UI/CLI path with reason codes; ledger schema for release events (actor, reason, detector, span hash, finding id); golden test that a release does not survive a new finding.
- [ ] Policy hook: releases disabled for repositories classified restricted (blocked on SAF-008).
- [ ] Measurement: fraction of pins released as `false_positive` per detector over 30 days of shadow — this is the precision feedback loop SAF-003 needs.
- [ ] Golden test: `/clear`, `--resume`, compaction on a pinned session → pin preserved (or, if the session key changes, document how the pin follows the transcript).

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-08-27 | Accepted (Confluence register) | — |
| 2026-09-02 | Amended: durable, lineage-scoped, covers all content-bearing classes; audited reason-coded human release added; D1 recommended | "Privacy pinning is one-way for the session; once local-only, it stays local-only." |
