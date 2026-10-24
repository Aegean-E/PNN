# Codebase Map & Symbol Catalog 🗺️

> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.

---

## 📊 Codebase Metrics
- **Total Python Modules**: `23`
- **Total Classes**: `28`
- **Total Top-Level Functions**: `88`
- **Total Class Methods**: `92`
- **Total Source Lines**: `3165`

---

## 📦 Modules & Exported Symbols

### [`pnn/__init__.py`](pnn/__init__.py)
> *Phase 2 CNS/BBB property screening for the PNN research project.*

**Size**: `37` lines (`908` bytes)

---

### [`pnn/__main__.py`](pnn/__main__.py)
> *Run the PNN screening pipeline as `python -m pnn`.*

**Size**: `6` lines (`137` bytes)

---

### [`pnn/cli.py`](pnn/cli.py)
> *Command-line entry point for the PNN Phase 2 screening pipeline.*

**Size**: `91` lines (`3406` bytes)

**Functions:**
- `def build_parser()`
- `def _filter(results, min_tier)`
- `def _report(results, kept, source, out)`
- `def _failure(what, why, fix)`
- `def main(argv)`

---

### [`pnn/compounds.py`](pnn/compounds.py)
> *Compound records and CSV ingestion for the PNN screening pipeline.*

**Size**: `234` lines (`8036` bytes)

**Classes:**
- `class CompoundError` - *Raised when input cannot be interpreted as a compound record.*
- `class Compound` - *One candidate with the properties the screening rules consume.*

**Functions:**
- `def normalize_field(name)` - *Map one CSV header to its canonical field name, or None when the column is not used.*
- `def _number(value, field, where)`
- `def _optional_number(values, field, where)`
- `def _charge(raw)`
- `def _build_compound(values, where)`
- `def parse_compounds(rows, source, allow_duplicates)` - *Turn raw CSV rows into compound records; raise CompoundError on the first bad row.*
- `def load_compounds(path, allow_duplicates)` - *Read a UTF-8 CSV file and return its compound records.*

---

### [`pnn/curate.py`](pnn/curate.py)
> *Command-line merge and diversity curation of PNN compound libraries.*

**Size**: `114` lines (`4217` bytes)

**Functions:**
- `def _positive_int(text)`
- `def _bin_width(text)`
- `def build_parser()`
- `def _failure(what, why, fix)`
- `def main(argv)`

---

### [`pnn/curation.py`](pnn/curation.py)
> *Merge, deduplicate and diversify compound libraries for PNN Phase 2.*

**Size**: `170` lines (`6038` bytes)

**Classes:**
- `class CurationError` - *Raised when libraries cannot be merged or curated safely.*
- `class Candidate` - *A compound with its source file and screening verdict.*

**Functions:**
- `def _preference(candidate)`
- `def _merge(left, right)` - *Keep the better record, filling a blank SMILES/name from the other source.*
- `def prepare_candidates(inputs)` - *Screen every input compound while keeping its source provenance.*
- `def deduplicate(candidates)` - *Collapse duplicate IDs first, then exact non-empty SMILES strings.*
- `def property_bin(compound, width)` - *Bin the six core properties on a normalized 0..1 grid.*
- `def _validate(min_tier, per_bin, bin_width, max_compounds)`
- `def curate(candidates, min_tier, per_bin, bin_width, max_compounds)` - *Filter by tier, cap each property bin, then apply the global size limit.*

---

### [`pnn/docking.py`](pnn/docking.py)
> *Docking-score ingestion and consensus ranking for PNN Phase 2.*

**Size**: `273` lines (`10305` bytes)

**Classes:**
- `class DockingError` - *Raised when docking input cannot be interpreted.*
- `class DockingScore` - *One docking result for one compound against one target.*
- `class DockingRank` - *A docking score with its normalized consensus quality.*
- `class CompoundRank` - *The best target row for one compound and how many targets it reached.*

**Functions:**
- `def _token(name)`
- `def _field(name)`
- `def _number(raw, field, where)`
- `def _optional(values, field, where)`
- `def _build(values, where)`
- `def parse_docking_scores(rows, source)` - *Turn raw CSV rows into docking records; refuse duplicates and unusable rows.*
- `def load_docking_scores(path)` - *Read a UTF-8 docking CSV.*
- `def load_screen_table(path)` - *Read the screening ranked CSV into a compound_id keyed table.*
- `def filter_scores(scores, max_rmsd, min_vina)` - *Drop rows without Vina or outside the optional RMSD/Vina limits.*
- `def normalize_scores(scores)` - *Scale each scoring method to 0..1 and combine available methods by weight.*
- `def aggregate_best(ranks)` - *Keep each compound's highest-consensus target and count its docked targets.*

---

### [`pnn/pipeline.py`](pnn/pipeline.py)
> *Command-line end-to-end Phase 2 lead selection for the PNN project.*

**Size**: `137` lines (`4489` bytes)

**Functions:**
- `def _positive_int(text)`
- `def _bin_width(text)`
- `def build_parser()`
- `def _failure(what, why, fix)`
- `def main(argv)`

---

### [`pnn/rank.py`](pnn/rank.py)
> *Command-line consensus ranking of docking results for PNN Phase 2.*

**Size**: `245` lines (`8401` bytes)

**Classes:**
- `class ShortlistRow` - *One ranked compound ready for CSV output.*
  - Method `.as_row()`

**Functions:**
- `def _property_score(info)`
- `def _selected(best, screen, min_tier)` - *Filter aggregated compounds by screening evidence and sort them by consensus.*
- `def build_shortlist(scores, screen, min_tier, max_rmsd, min_vina)` - *Return shortlist rows and a summary of what each filter removed.*
- `def build_parser()`
- `def _failure(what, why, fix)`
- `def main(argv)`

---

### [`pnn/reports.py`](pnn/reports.py)
> *Atomic CSV, JSON and text report writers shared by the PNN command line tools.*

**Size**: `68` lines (`2038` bytes)

**Functions:**
- `def _open_temp(path)`
- `def _finish(path, handle)`
- `def write_csv(path, fieldnames, rows)` - *Write `rows` as CSV to a temporary file, then replace `path` atomically.*
- `def write_json(path, report)` - *Write `report` as JSON to a temporary file, then replace `path` atomically.*
- `def write_text(path, text)` - *Write `text` to a temporary file, then replace `path` atomically.*

---

### [`pnn/rules.py`](pnn/rules.py)
> *Property rules that turn the PNN BBB/CNS design criteria into verdicts.*

**Size**: `219` lines (`7784` bytes)

**Classes:**
- `class CriterionResult` - *One rule's verdict for one compound.*

**Functions:**
- `def _range(name, value, low, high, optimal_low, optimal_high, unit)`
- `def _ceiling(name, value, limit, optimal, unit)`
- `def _physicochemical(compound)`
- `def _pka(compound)`
- `def _charge(compound)`
- `def _logbb(compound)`
- `def _brain_plasma(compound)`
- `def _oral_bioavailability(compound)`
- `def _cyp3a4(compound)`
- `def _herg(compound)`
- `def _pnn_ec50(compound)`
- `def evaluate(compound)` - *Return every rule verdict for `compound` in a stable order.*
- `def weight(criterion_name)` - *Core design properties outweigh optional measured/ADMET properties.*

---

### [`pnn/screen.py`](pnn/screen.py)
> *Tiering and ranking for the PNN Phase 2 property screen.*

**Size**: `79` lines (`3049` bytes)

**Classes:**
- `class ScreenResult` - *A compound, its verdicts, and the resulting triage tier.*
  - Method `.failed_criteria()`
  - Method `.unknown_criteria()`

**Functions:**
- `def _weighted_score(criteria)`
- `def _tier(criteria, score)`
- `def evaluate_compound(compound)` - *Evaluate every rule for one compound and assign its tier.*
- `def screen_compounds(compounds)` - *Evaluate and rank compounds by tier, then score (highest first), then ID.*
- `def summarize(results)` - *Count tiers and report the scored average, including rejected compounds.*

---

### [`pnn/selection.py`](pnn/selection.py)
> *End-to-end Phase 2 lead selection for the PNN project.*

**Size**: `336` lines (`12882` bytes)

**Classes:**
- `class PipelineError` - *Raised when a Phase 2 run cannot produce a defensible lead set.*
- `class LeadSelection` - *The selected compounds and the audit counts for one Phase 2 run.*
- `class LeadRun` - *A completed run: selected compounds, written artifacts and the manifest.*

**Functions:**
- `def _digest(path)` - *Return the SHA-256 hex digest of a file without loading it whole.*
- `def _load_inputs(paths)`
- `def _screen_table(results)`
- `def select_leads(inputs, docking, min_tier, per_bin, bin_width, max_compounds, max_rmsd, min_vina)` - *Curate, screen and rank one lead set from compound and docking CSVs.*
- `def _options(min_tier, per_bin, bin_width, max_compounds, max_rmsd, min_vina)`
- `def _manifest(selection, outputs, options)`
- `def render_lead_report(selection, options, top_n)` - *Render a comprehensive Markdown lead report honoring G-001, G-002, and G-003.*
- `def run_pipeline(inputs, docking, out_dir, min_tier, per_bin, bin_width, max_compounds, max_rmsd, min_vina, top_n_report)` - *Run the three Phase 2 stages and write their artifacts, report and manifest.*

---

### [`pnn/tables.py`](pnn/tables.py)
> *CSV row contracts shared by the PNN Phase 2 command line tools.*

**Size**: `108` lines (`3053` bytes)

**Functions:**
- `def _optional(value)`
- `def curated_row(candidate, width)` - *Return one curated-library row, including source and property bin.*
- `def screen_row(result)` - *Return one ranked-screening row for a screened compound.*

---

### [`tests/__init__.py`](tests/__init__.py)
**Size**: `0` lines (`0` bytes)

---

### [`tests/test_cli.py`](tests/test_cli.py)
> *Integration tests for the `python -m pnn` CLI contract.*

**Size**: `84` lines (`3719` bytes)

**Classes:**
- `class CliTest`
  - Method `.setUp()`
  - Method `.run_main(*argv)`
  - Method `.read_rows(path)`
  - Method `.test_writes_ranked_csv_and_json_summary()`
  - Method `.test_min_tier_filters_lower_tiers_and_rejects()`
  - Method `.test_invalid_input_returns_one_with_a_remediation_triad()`
  - Method `.test_missing_input_returns_one()`
  - Method `.test_help_exits_zero_and_unknown_flag_exits_two()`

---

### [`tests/test_curation.py`](tests/test_curation.py)
> *Unit and CLI tests for compound-library curation.*

**Size**: `181` lines (`6910` bytes)

**Classes:**
- `class DeduplicationTest`
  - Method `.test_duplicate_id_keeps_the_better_candidate()`
  - Method `.test_better_record_keeps_smiles_from_the_other_source()`
  - Method `.test_same_id_with_different_smiles_is_refused()`
  - Method `.test_same_smiles_with_different_ids_is_collapsed()`
  - Method `.test_blank_smiles_do_not_collapse_distinct_ids()`
  - Method `.test_prepare_candidates_keeps_sources()`
- `class CurationTest`
  - Method `.test_tier_filter_removes_rejected_candidates()`
  - Method `.test_per_bin_cap_keeps_one_best_per_property_cell()`
  - Method `.test_max_compounds_truncates_and_reports()`
  - Method `.test_property_bin_is_deterministic()`
  - Method `.test_invalid_bin_width_is_refused()`
- `class CurateCliTest`
  - Method `.setUp()`
  - Method `.run_main(*argv)`
  - Method `.read_rows(path)`
  - Method `.test_merges_deduplicates_and_filters()`
  - Method `.test_conflicting_id_returns_one()`
  - Method `.test_no_eligible_compounds_returns_one()`

**Functions:**
- `def compound(compound_id, smiles, **overrides)`
- `def candidate(compound_id, source, smiles, **overrides)`

---

### [`tests/test_docking.py`](tests/test_docking.py)
> *Unit tests for docking ingestion and consensus normalization.*

**Size**: `113` lines (`4470` bytes)

**Classes:**
- `class DockingIngestionTest`
  - Method `.test_aliases_units_and_optional_columns()`
  - Method `.test_row_needs_a_score()`
  - Method `.test_row_needs_target()`
  - Method `.test_duplicate_compound_target_is_refused()`
  - Method `.test_non_finite_score_is_refused()`
  - Method `.test_negative_rmsd_is_refused()`
- `class ConsensusTest`
  - Method `.test_vina_only_is_normalized_to_zero_and_one()`
  - Method `.test_multiple_methods_are_weighted_and_coverage_is_reported()`
  - Method `.test_best_target_is_kept_and_targets_are_counted()`
  - Method `.test_filters_drop_missing_vina_and_limit_breakers()`

---

### [`tests/test_docs.py`](tests/test_docs.py)
> *Regression shield for the PNN research documents (PRINCIPLE-005, PRINCIPLE-014).*

**Size**: `50` lines (`1880` bytes)

**Classes:**
- `class ProjectDocsTest`
  - Method `.test_required_documents_exist()`
  - Method `.test_readme_tree_lists_only_existing_paths()`

---

### [`tests/test_pipeline.py`](tests/test_pipeline.py)
> *Unit and CLI integration tests for the end-to-end Phase 2 lead selection pipeline.*

**Size**: `206` lines (`8185` bytes)

**Classes:**
- `class PipelineTest`
  - Method `.setUp()`
  - Method `.read_rows(path)`
  - Method `.run_cli(*argv)`
  - Method `.test_select_leads_end_to_end()`
  - Method `.test_select_leads_raises_on_empty_input()`
  - Method `.test_select_leads_raises_when_curation_empties_set()`
  - Method `.test_select_leads_raises_when_no_shortlist_survives()`
  - Method `.test_render_lead_report_guidelines_and_evidence()`
  - Method `.test_run_pipeline_produces_all_artifacts_and_hashed_manifest()`
  - Method `.test_cli_execution_success()`
  - Method `.test_cli_execution_failure_triad()`
  - Method `.test_cli_help()`

---

### [`tests/test_rank.py`](tests/test_rank.py)
> *Unit and CLI tests for the docking consensus shortlist.*

**Size**: `158` lines (`6522` bytes)

**Classes:**
- `class ShortlistTest`
  - Method `.test_tier_filter_and_consensus_order()`
  - Method `.test_rmsd_filter_removes_a_target_row()`
  - Method `.test_vina_filter_removes_weak_rows()`
  - Method `.test_compound_missing_from_screen_is_skipped()`
  - Method `.test_docking_only_mode_has_no_tier()`
- `class RankCliTest`
  - Method `.setUp()`
  - Method `.run_main(*argv)`
  - Method `.read_rows(path)`
  - Method `.test_cli_writes_shortlist_and_json()`
  - Method `.test_cli_returns_one_when_filters_remove_everything()`
  - Method `.test_cli_returns_one_for_invalid_docking()`
  - Method `.test_screen_table_loader_reads_tier_and_score()`
  - Method `.test_module_entry_point_runs_main()`

**Functions:**
- `def screen_table()`
- `def scores()`

---

### [`tests/test_rules.py`](tests/test_rules.py)
> *Unit tests for the property rules (PRINCIPLE-014: failing-first boundaries).*

**Size**: `89` lines (`3378` bytes)

**Classes:**
- `class PropertyRuleTest`
  - Method `.test_ideal_compound_passes_every_rule()`
  - Method `.test_molecular_weight_boundaries()`
  - Method `.test_tpsa_and_rotor_ceilings()`
  - Method `.test_missing_optional_properties_are_unknown()`
  - Method `.test_basic_pka_outside_window_fails()`
  - Method `.test_unrecognized_charge_is_unknown()`
  - Method `.test_oral_bioavailability_accepts_fraction_and_percent()`
  - Method `.test_hard_liabilities_fail()`

**Functions:**
- `def ideal(**overrides)`
- `def by_name(compound)`

---

### [`tests/test_screen.py`](tests/test_screen.py)
> *Unit tests for tiering, ranking and CSV ingestion.*

**Size**: `167` lines (`6535` bytes)

**Classes:**
- `class TierTest`
  - Method `.test_complete_ideal_compound_is_tier_a()`
  - Method `.test_property_only_compound_cannot_be_tier_a()`
  - Method `.test_acceptable_compound_is_tier_b()`
  - Method `.test_two_core_failures_are_tier_c()`
  - Method `.test_three_core_failures_are_rejected()`
  - Method `.test_hard_liability_rejects_even_an_optimal_profile()`
- `class RankingTest`
  - Method `.test_ranking_orders_by_tier_then_score()`
- `class CsvIngestionTest`
  - Method `.setUp()`
  - Method `.write_csv(text)`
  - Method `.test_aliases_and_blank_optionals_are_supported()`
  - Method `.test_duplicate_ids_are_refused()`
  - Method `.test_bad_number_names_the_row()`
  - Method `.test_missing_field_is_refused()`
  - Method `.test_non_finite_number_is_refused()`
  - Method `.test_negative_property_is_refused()`
  - Method `.test_fractional_count_is_refused()`
  - Method `.test_missing_file_is_refused()`
  - Method `.test_header_only_file_is_refused()`
  - Method `.test_non_utf8_file_is_refused()`

**Functions:**
- `def ideal(compound_id, **overrides)`
- `def acceptable(compound_id, **overrides)`

---
