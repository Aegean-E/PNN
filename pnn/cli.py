"""Command-line entry point for the PNN Phase 2 screening pipeline."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence

from .compounds import CompoundError, load_compounds
from .rules import CORE_CRITERIA, HARD_REJECT_CRITERIA
from .screen import TIER_ORDER, ScreenResult, screen_compounds, summarize

CSV_FIELDS = (
    "compound_id",
    "name",
    "smiles",
    "tier",
    "score",
    "mw",
    "logp",
    "tpsa",
    "hbd",
    "hba",
    "rotatable_bonds",
    "pka",
    "charge",
    "logbb",
    "brain_plasma_ratio",
    "oral_bioavailability",
    "cyp3a4_inhibition",
    "herg_liability",
    "pnn_ec50_nm",
    "failed_criteria",
    "unknown_criteria",
)
_TIER_CEILING = {"A": 0, "B": 1, "C": 2}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pnn",
        description=(
            "Screen compound properties against the PNN Phase 2 CNS/BBB design rules "
            "and write a ranked CSV."
        ),
    )
    parser.add_argument("input", help="CSV with compound_id, mw, logp, tpsa, hbd, hba, rotatable_bonds")
    parser.add_argument("--out", default="ranked_compounds.csv", help="ranked CSV path")
    parser.add_argument("--json", dest="json_path", help="optional JSON summary path")
    parser.add_argument(
        "--min-tier",
        choices=("A", "B", "C"),
        help="keep only this tier and better (A, A+B, or A+B+C); rejected compounds are dropped",
    )
    return parser


def _row(result: ScreenResult) -> dict:
    compound = result.compound
    return {
        "compound_id": compound.compound_id,
        "name": compound.name,
        "smiles": compound.smiles,
        "tier": result.tier,
        "score": f"{result.score:.4f}",
        "mw": compound.mw,
        "logp": compound.logp,
        "tpsa": compound.tpsa,
        "hbd": compound.hbd,
        "hba": compound.hba,
        "rotatable_bonds": compound.rotatable_bonds,
        "pka": "" if compound.pka is None else compound.pka,
        "charge": compound.charge,
        "logbb": "" if compound.logbb is None else compound.logbb,
        "brain_plasma_ratio": "" if compound.brain_plasma_ratio is None else compound.brain_plasma_ratio,
        "oral_bioavailability": "" if compound.oral_bioavailability is None else compound.oral_bioavailability,
        "cyp3a4_inhibition": "" if compound.cyp3a4_inhibition is None else compound.cyp3a4_inhibition,
        "herg_liability": "" if compound.herg_liability is None else compound.herg_liability,
        "pnn_ec50_nm": "" if compound.pnn_ec50_nm is None else compound.pnn_ec50_nm,
        "failed_criteria": ";".join(result.failed_criteria()),
        "unknown_criteria": ";".join(result.unknown_criteria()),
    }


def _atomic_write(path: Path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", newline="", delete=False, dir=str(path.parent), prefix=f".{path.name}."
    )
    return path, handle


def _finish_write(path: Path, handle) -> None:
    handle.flush()
    os.fsync(handle.fileno())
    handle.close()
    try:
        os.replace(handle.name, path)
    except OSError:
        Path(handle.name).unlink(missing_ok=True)
        raise


def _write_csv(path: Path, results: Sequence[ScreenResult]) -> None:
    destination, handle = _atomic_write(path)
    try:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for result in results:
            writer.writerow(_row(result))
    except BaseException:
        handle.close()
        Path(handle.name).unlink(missing_ok=True)
        raise
    _finish_write(destination, handle)


def _write_json(path: Path, report: dict) -> None:
    destination, handle = _atomic_write(path)
    try:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    except BaseException:
        handle.close()
        Path(handle.name).unlink(missing_ok=True)
        raise
    _finish_write(destination, handle)


def _filter(results: Sequence[ScreenResult], min_tier: Optional[str]) -> List[ScreenResult]:
    if min_tier is None:
        return list(results)
    ceiling = _TIER_CEILING[min_tier]
    return [result for result in results if TIER_ORDER[result.tier] <= ceiling]


def _report(results: Sequence[ScreenResult], kept: Sequence[ScreenResult], source: str, out: Path) -> dict:
    return {
        "input": source,
        "output": str(out),
        "summary": summarize(results),
        "emitted": len(kept),
        "rules": {"core": list(CORE_CRITERIA), "hard_reject": list(HARD_REJECT_CRITERIA)},
    }


def _failure(what: str, why: str, fix: str) -> int:
    print(f"What: {what}", file=sys.stderr)
    print(f"Why: {why}", file=sys.stderr)
    print(f"Fix: {fix}", file=sys.stderr)
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    out = Path(args.out)
    try:
        compounds = load_compounds(Path(args.input))
        results = screen_compounds(compounds)
        kept = _filter(results, args.min_tier)
        _write_csv(out, kept)
        if args.json_path:
            _write_json(Path(args.json_path), _report(results, kept, args.input, out))
    except CompoundError as exc:
        return _failure(
            str(exc),
            "the screen needs a readable UTF-8 CSV with the required property columns.",
            "check the input contract in computational/screening_pipeline.md, then rerun with a valid CSV.",
        )
    except OSError as exc:
        return _failure(
            str(exc),
            "the ranked CSV or JSON summary could not be written.",
            "choose a writable --out/--json path and rerun.",
        )
    summary = summarize(results)
    counts = summary["by_tier"]
    kept_note = f" (emitted {len(kept)} of {len(results)})" if len(kept) != len(results) else ""
    print(
        f"Screened {len(results)} compound(s): A={counts['A']} B={counts['B']} "
        f"C={counts['C']} Reject={counts['Reject']}{kept_note} -> {out}"
    )
    return 0
