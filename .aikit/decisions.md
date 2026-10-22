# Decisions

Why this project is built the way it is, oldest first. One entry per decision that changes a
contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.

<!-- Entry format:
### ADR-NNN: <decision in one line>
- **Date**: YYYY-MM-DD
- **Status**: Accepted
- **Context**: <what forced the decision>
- **Decision**: <what was decided>
- **Consequences**: <what follows, including what it costs>
-->

### ADR-001: Use a deterministic CSV property screen for Phase 2 triage
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: Phase 2 needs a reproducible way to prioritise compounds before docking, but the project has no chemistry toolkit dependency and no validated in-house BBB model.
- **Decision**: Ship a standard-library-only `pnn` package that consumes a documented CSV schema, applies the project's CNS/BBB property windows and optional ADMET limits, and emits tiered CSV/JSON output. Rules live in `pnn/rules.py`; the contract lives in `computational/screening_pipeline.md`.
- **Consequences**: Screening is reproducible and testable without third-party packages, and it cannot overstate evidence because missing values are `UNKNOWN`. The rules remain heuristics: every promoted compound still needs measured permeability and PNN-softening data, and any rule or schema change needs a new ADR and tests.
