# Findings

## review-governance-recheck-2026-09-10:RG-04 — adrl-core CLAUDE.md duplicates AGENTS.md rules and already drifts

adrl-core CLAUDE.md restates the ownership, invariants, quality and checks sections verbatim and then imports AGENTS.md, so Claude reads them twice. The copies already differ: AGENTS.md carries the 2026-09-09 scoped FND-001 constructor-only experiment note; CLAUDE.md's invariant list omits it. The register CLAUDE.md correctly contains only the import.

Acceptance: adrl-core CLAUDE.md reduces to a title plus @AGENTS.md, or a check asserts the duplicated sections are byte-identical to AGENTS.md.

