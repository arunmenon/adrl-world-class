# ADRL-CAS-009 - Action-effect provenance and authorization boundary (Proposed)

| Field | Value |
|---|---|
| Bucket | CAS - Execution, Cascade, Recovery |
| Status | Proposed 2026-09-03 (new, from external review) |
| Maturity | D0 Design, review recommends D0 Design (the 2026-09-02 implementation trusts MCP hints unconditionally and classifies compound shell commands by their first word) |
| Review verdict | PROPOSED (new) |
| Tenets | 5, 8 |
| Related decisions | CAS-003 (amended), CAS-004, CAS-001, RTG-004, SAF-007, MEM-004, TRU-001 |
| Open questions | Q2, Q3 |

## Decision

The side-effect class of an action is established by a provenance rule that trusts only sources outside the model's and the tool server's control: built-in harness tools are classified by a versioned table; MCP tool annotations are accepted only from servers on an OPS allow-list and are otherwise ignored; shell commands are parsed (operators, pipes, redirections, substitutions) and classified by the most severe component; any action whose class cannot be established is `destructive`; every executed call, including read-only ones, is enumerated in the side-effect record; and the handoff note is untrusted context for the receiving model, never an instruction with authority.

1. *Provenance table*: `action-provenance-v1` lists, per harness and tool name, the class and the evidence source (`builtin_table`, `attested_annotation`, `parsed_command`, `unknown`). MCP annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`) count as `attested_annotation` only when the server id is on the allow-list; the MCP specification itself says clients must treat annotations as untrusted unless the server is trusted.
2. *Command parsing*: a Bash or shell action is split on `&&`, `||`, `;`, `|`, newlines, subshells and command substitution; each component is classified; redirections that write (`>`, `>>`, `tee`) and network clients (`curl`, `wget`, `ssh`, `scp`, `nc`, package publishers) are `destructive`; an unparseable command is `destructive`.
3. *Closed world*: unknown tools and unknown commands are `destructive` for RTG-004's cascade feasibility and for the CAS-003 record; there is no read-only default.
4. *Full enumeration*: the side-effect record lists every executed call with its class and provenance source; read-only calls are recorded, not omitted, because a mis-classified read-only call is exactly the one the next model needs to see.
5. *Handoff is data*: the CAS-004 note is inserted as delimited context and the receiving model is told it is a mechanical record; nothing in the note may be phrased as an instruction, and ADRL's own control decisions (rung, escalation, boundaries) never read the note. This is the CaMeL separation of control flow from untrusted data.

## Context and rationale

CAS-003 clause 3 said side-effect class "is derived mechanically from tool name / MCP annotations, not from model text". The implementation did exactly that and the external review showed the consequence: `echo $TOKEN > /tmp/leak` was read-only because it starts with `echo`; `git status && touch owned` was read-only because it starts with `git status`; and an MCP tool named `delete` with `readOnlyHint: true` was read-only because the hint was trusted. Read-only calls were then omitted from the handoff record, so a stronger model inherited mutations and egress that ADRL said never happened. ADRL does not execute tools, so this does not cause an action; it invalidates the "clean cascade" claim of RTG-004 and the inheritance claim of CAS-003, both of which feed the local rung's permitted scope (Q2). The fix is a provenance rule: mechanical is necessary but not sufficient; the mechanism must be one the model and the tool server cannot shape.

## Adversarial review (2026-09-03)

### Steelman
This is the action-plane counterpart of TRU-001: a classification is only as trustworthy as the source it reads, and the two sources CAS-003 read (tool text, server annotations) are both under the control of parties the register treats as untrusted. Parsing commands and closing the world costs some local-first eligibility (more actions look destructive); that is the correct direction for a rung whose reliability is unmeasured.

### Attacks (self-applied)
1. **Shell parsing is undecidable in general.** Mitigation: the parser is conservative; anything it cannot classify is destructive; the table is versioned and its false-destructive rate is a published metric.
2. **Closed world makes local-first rare.** Mitigation: that is a measurement, not a defect; RTG-004 feasibility already excludes destructive first actions, and the Q2 slice (mechanical, small-diff) is mostly reads and edits the built-in table classifies.
3. **Allow-listing MCP servers is an OPS burden.** Mitigation: the list starts empty; unlisted servers are simply unattested, which is the MCP specification's own default.
4. **The note is still text the model reads.** Mitigation: clause 5 removes authority, not visibility; a model that follows an instruction inside a delimited record is a model failure the trip-wires (CAS-001) are designed to catch, not a control failure.

### Evidence
- ADRL external implementation review, 2026-09-03, finding P1-4, verified: `side_effects.py` returns `read_only` on `readOnlyHint` before any inspection; `startswith` prefix matching on commands; read-only calls skipped in the record.
- Model Context Protocol, "Tools" (specification 2025-06-18): annotations are hints and clients must treat them as untrusted unless the server is trusted - https://modelcontextprotocol.io/specification/2025-06-18/server/tools (cited by the 2026-09-03 external review; not independently fetched)
- Debenedetti et al., CaMeL (arXiv 2503.18813): control flow from trusted sources, untrusted data carries no capability - https://arxiv.org/abs/2503.18813 (cited by the 2026-09-03 external review; not independently fetched)
- ADRL-CAS-003 clause 3 and ADRL-RTG-004 clause (d) (this register).

### Verdict
**PROPOSED (new).** CAS-003 clause 3 is amended in place to cite this decision. Recommended for acceptance at D0 with the parser and table as the D1 exit.

## Amendments applied

New decision; no prior text. CAS-003 amended in place on 2026-09-03.

## Follow-ups

- [ ] Publish `action-provenance-v1` (built-in tool table for Claude Code; MCP allow-list format) and the conservative shell parser with a golden corpus of commands and expected classes, including the three review examples.
- [ ] Record provenance source per call on the outcome row; publish the false-destructive rate per rung.
- [ ] Rewrite the CAS-004 note template so no line is imperative; add a test that the note is never consumed by any control path.

## Changelog

| Date | Change | Text before change |
|---|---|---|
| 2026-09-03 | Proposed (external review) | none |
