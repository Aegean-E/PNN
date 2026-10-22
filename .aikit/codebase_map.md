# Codebase Map & Symbol Catalog 🗺️

> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.

---

## 📊 Codebase Metrics
- **Total Python Modules**: `11`
- **Total Classes**: `10`
- **Total Top-Level Functions**: `39`
- **Total Class Methods**: `39`
- **Total Source Lines**: `1128`

---

## 📦 Modules & Exported Symbols

### [`pnn/__init__.py`](pnn/__init__.py)
> *Phase 2 CNS/BBB property screening for the PNN research project.*

**Size**: `14` lines (`372` bytes)

---

### [`pnn/__main__.py`](pnn/__main__.py)
> *Run the PNN screening pipeline as `python -m pnn`.*

**Size**: `6` lines (`137` bytes)

---

### [`pnn/cli.py`](pnn/cli.py)
> *Command-line entry point for the PNN Phase 2 screening pipeline.*

**Size**: `189` lines (`6271` bytes)

**Functions:**
- `def build_parser()`
- `def _row(result)`
- `def _atomic_write(path)`
- `def _finish_write(path, handle)`
- `def _write_csv(path, results)`
- `def _write_json(path, report)`
- `def _filter(results, min_tier)`
- `def _report(results, kept, source, out)`
- `def _failure(what, why, fix)`
- `def main(argv)`

---

### [`pnn/compounds.py`](pnn/compounds.py)
> *Compound records and CSV ingestion for the PNN screening pipeline.*

**Size**: `231` lines (`7874` bytes)

**Classes:**
- `class CompoundError` - *Raised when input cannot be interpreted as a compound record.*
- `class Compound` - *One candidate with the properties the screening rules consume.*

**Functions:**
- `def normalize_field(name)` - *Map one CSV header to its canonical field name, or None when the column is not used.*
- `def _number(value, field, where)`
- `def _optional_number(values, field, where)`
- `def _charge(raw)`
- `def _build_compound(values, where)`
- `def parse_compounds(rows, source)` - *Turn raw CSV rows into compound records; raise CompoundError on the first bad row.*
- `def load_compounds(path)` - *Read a UTF-8 CSV file and return its compound records.*

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

### [`tests/test_docs.py`](tests/test_docs.py)
> *Regression shield for the PNN research documents (PRINCIPLE-005, PRINCIPLE-014).*

**Size**: `50` lines (`1880` bytes)

**Classes:**
- `class ProjectDocsTest`
  - Method `.test_required_documents_exist()`
  - Method `.test_readme_tree_lists_only_existing_paths()`

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
