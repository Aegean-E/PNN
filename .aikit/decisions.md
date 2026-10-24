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

### ADR-002: Normalize docking engines before consensus ranking
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: Phase 2 exports Vina, Glide and MM-GBSA scores whose native scales are not comparable; summing raw values would let one engine dominate by magnitude alone.
- **Decision**: `python -m pnn.rank` min-max scales each method within the filtered docking set, weights Vina 0.5, Glide 0.3 and MM-GBSA 0.2, renormalizes over available methods, reports coverage, and requires a Vina score for entry.
- **Consequences**: The shortlist is reproducible and transparent about missing evidence, but normalization depends on the input set, so comparisons require a fixed compound set. Consensus remains a prioritisation score, not a measured affinity.

### ADR-003: Curate libraries by provenance, exact identity and property-space caps
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: Phase 2 needs to merge several compound sources without duplicate identities or property-space clumps, but the project has no chemistry toolkit for canonicalization or scaffold analysis.
- **Decision**: `python -m pnn.curate` collapses duplicate `compound_id` values (refusing conflicting SMILES), then exact non-empty SMILES strings, screens every row with the property rules, and caps each normalized six-property bin at `--per-bin` compounds before an optional global limit. Every kept row keeps its source path and bin label; JSON reports every removal count.
- **Consequences**: The library is reproducible and auditable, and duplicate chemistry is not silently multiplied. Exact-SMILES matching misses salts, tautomers and stereochemistry variants, and bin caps approximate property-space spacing rather than guaranteeing a distance; upstream canonicalization or a chemistry toolkit is required when those distinctions matter.

### ADR-004: End-to-end Phase 2 lead selection pipeline with hashed manifest and report
- **Date**: 2026-10-24
- **Status**: Accepted
- **Context**: The Phase 2 curation, property screening, and docking consensus ranking tools existed as individual CLI steps, but generating an auditable, reproducible lead selection required manual chaining, with no unified cryptographic provenance or consolidated evidence report.
- **Decision**: Ship `pnn.selection` and `python -m pnn.pipeline` to execute the full workflow in one atomic run: curate -> screen -> consensus rank. The run emits `curated_library.csv`, `ranked_compounds.csv`, `shortlist.csv`, a Markdown `lead_report.md` (highlighting evidence gaps and G-001/G-002/G-003 triage limits), and a `manifest.json` recording SHA-256 digests for all inputs, options, stage metrics and output artifacts under schema `pnn.phase2.pipeline/1`. Shared CSV formatting logic is centralized in `pnn/tables.py`.
- **Consequences**: Lead selection is strictly reproducible, tamper-evident, and auditable across all stages. Memory is bounded by streaming SHA-256 digest computation. Triage disclaimers in generated reports prevent downstream overclaiming.

### ADR-005: Target binding-pocket profiles and Phase 3 in vitro assay qualification pipeline
- **Date**: 2026-10-24
- **Status**: Accepted
- **Context**: Virtual screening required codified receptor grid invariants for key PNN targets (PTPσ, LAR, NgR1, MMP2), and progression beyond in silico triage required an executable qualification engine to ingest experimental PNN degradation, BBB permeability, and cytotoxicity counter-screen data.
- **Decision**: Introduce `pnn.target` defining receptor pocket invariants and AutoDock Vina grid configuration exports; ship benchmark libraries in `data/compounds/` and `data/docking/` with turnkey verification runner `tools/golden_run.py`; implement `pnn.assay` to ingest fluorogenic DQ-CS degradation (EC50, max %), PAMPA-BBB / MDCK-MDR1 permeability, and CellTiter-Glo cytotoxicity (CC50, Selectivity Index) to classify candidates into CONFIRMED_HIT, QUALIFIED_LEAD, CYTOTOXIC, or INACTIVE status with Markdown reporting honoring G-001.
- **Consequences**: Structural invariants ensure reproducible receptor grid definitions, and in vitro assay datasets can be qualified objectively against standardized progression thresholds without third-party dependencies.


