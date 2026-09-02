# OPS — Platform, Runtime, Operations

Not captured in the source pack. Known by cross-reference only: OPS-001 (multi-worker future), OPS-006 (record the served rung, not the intended one).

The 2026-09-02 review touches OPS in three places: the multi-worker blocker is the process-local session/pin dict, not SQLite (MEM-006, SAF-002, SEM-002); served identity must be model and provider, not rung (CAS-006, RTG-008); and fail-open events need rate alerting (FND-004). These should be folded into the OPS page when it is captured.
