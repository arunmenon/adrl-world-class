# Run 1: not accepted as source-bound evidence

The experiment executed, but its manifest used `source` for both the input file
hash map and synthetic provenance. The second value overwrote the first. Therefore
`run_completed: true` records execution only; it does not qualify this export as a
reproducible source-bound baseline. Original files remain intact.

The runner now uses `source_manifest` for file hashes and retains `source=synthetic`.
A regression test requires both source and configuration identities, plus the
readable report. [Run 2](../run-2/report.md) supersedes this qualification attempt.
No routing rule, gate, task case or expected route was changed in this repair.
