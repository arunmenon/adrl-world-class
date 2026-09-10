# W3.2b2a: Reserve capacity before admitting an attempt

Packet `W3.2b2a-terminal-capacity-v1`, frozen 8 September 2026 before code changes.
Parent: [process ownership and admission](w3-2b-process-ownership.md).
Entry: [W3.2b1](../adrl-w3-2b1-process-ownership-2026-09-08.md), 669 passing tests.
Owner: Codex, implementation/self-review. Independent review remains unassigned.

## Problem and bounded change

The v1 journal can consume its last event slot or remaining byte quota before recording
an interruption. A newly lowered journal limit can also block a final record. Correct this
quota failure without treating a journal event as evidence that processes stopped.

New starts use `operator-attempt-policy-v2`. Atomically append the initial event and a
capacity grant that reserves one terminal event slot and a versioned byte allowance.
The allowance counts encrypted payload and nonce bytes, matching the existing history
quota, and must be large enough for every permitted terminal reason before admission.
The policy permits at least two event slots, a 1,024 to 4,096-byte terminal allowance
(default 1,024), and retains the existing maximums of eight events, three attempts per
session, 8 MB per event and 32 MB of history. Limits may be lower within those bounds.

All appends account for stored bytes plus every pending capacity grant. A start or close
request cannot spend another attempt's allowance. A terminal event consumes its own grant;
the original append-only grant remains for audit. No deletion, mutable counter or reclamation
of stored history is introduced. Grant plus initial event, and terminal append plus inferred
consumption, are single ledger transactions. Duplicate requests do not charge twice.

An active grant's recorded history ceiling constrains later admissions, even when another
caller offers a larger budget. A newly lowered caller ceiling can deny new/nonterminal work
but does not revoke an existing v2 terminal grant. Terminal appends must remain within that
original grant and all other active commitments. This is a versioned admission contract,
not permission to exceed the existing maximum or silently change historical policy.

Schema 9 adds an authenticated capacity-version header to attempt events and a small
append-only grant table. The six new stored fields must be inventoried. Verify grant/header
consistency, one start per grant, and grant values against the owning encrypted policy.
Reject missing/malformed grants where required. No global rollback/hostile database writer
protection is claimed; metadata is an internal accounting surface, not new signal authority.

V1 records remain readable, retain their original quota contract and can be retried with
their original policy. A new v1 start is refused. Do not retrofit a grant, rewrite old events
or claim that old attempts had capacity reserved. V1 continuations also respect pending v2
grants. API preview 4 and all eligibility fields are unchanged.

## Explicit exclusions and next pieces

This slice reserves logical quota; it cannot reserve physical disk space or guarantee an
append after disk/database failure, key erasure, expired credentials or corruption. Erasing
a pending attempt leaves its quota commitment and journal reservation visible and blocked.
No key resurrection, automatic workspace release, process launch, capture association or
change to erasure/privacy policy is authorized here.

W3.2b2b must coordinate process ownership, erasure, outstanding capacity and reservation
release before real supervised execution. Complete writer containment remains unqualified;
the group-only backend cannot grant exact close. W3.2b3 capture association and active-copy/
crash recovery gates remain open. All fixtures here are synthetic and disposable.

Owning clauses: MEM-001 append-only/atomic evidence, MEM-002 attempt lifecycle/provenance,
MEM-005 accounting metadata inventory, MEM-010 erasure semantics, OPS-001 shared admission.
Preserve all architectural statuses, maturity fields and prior decision wording.

## Acceptance cases and stop limits

| Case | Required observation |
|---|---|
| Start fits but start plus terminal reserve does not | Refuse atomically; no event/grant |
| Event budget leaves only its terminal slot | Close request denied; cancellation/incomplete can append |
| Close request would spend the terminal bytes | Deny close; terminal still fits |
| Other session/caller has a larger budget | Cannot consume an active smaller-ceiling commitment |
| Caller lowers budget after start | New work may be denied; original bounded terminal grant remains usable |
| Two workspaces race for scarce history space | Serialized admission charges grants; no over-admission |
| Restart, duplicate start/terminal, lost acknowledgement | Original records and charges preserved, no double grant |
| Transaction fails after initial event or terminal append | Rollback leaves no partial admission/consumption |
| Grant/header missing or inconsistent | Read/transition rejects owning corruption; structural inconsistencies deny admission |
| Erasure or expired credential | No terminal bypass; pending commitment is retained |
| Existing schema-8 v1 attempt | Migrates/read/retry/transition without invented reservation |
| All terminal variants | Fit reserved bytes; no success/quiescence/learning authority |

One implementation writer. At most three failed repairs per task. Run required checks and
all inventory/map/API/index checks, preserve unrelated source, publish a source/evidence
manifest and update the journey/owning register before closing b2a. Full W3 remains open.

## Disposition, 8 September 2026

B2a is locally validated: 28 new capacity cases, 697 passing tests and eleven passing
checks, with schema 9 and 279 inventoried fields. The first focused run had four fixture
failures (incorrect example budgets and manifest setup); corrections retained the frozen
contract. The final focused run passed all 68 cases. Five owning ADRs retain prior wording
and all 77 status/maturity fields remain unchanged.

See the [report](../adrl-w3-2b2a-terminal-capacity-2026-09-08.md),
[evidence](../research/adrl-w3-2b2a-terminal-capacity-2026-09-08.json) and
[source diff](../research/adrl-w3-2b2a-terminal-capacity-2026-09-08.patch).
Coordinated erasure/process/reservation release is W3.2b2b. Erased pending grants remain
charged; no exact-close or safe workspace-reuse claim follows. Full W3 stays open.
