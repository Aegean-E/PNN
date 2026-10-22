"""Command-line merge and diversity curation of PNN compound libraries."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .compounds import CompoundError, load_compounds
from .curation import (
    Candidate,
    CurationError,
    curate,
    deduplicate,
    prepare_candidates,
    property_bin,
)
from .reports import write_csv, write_json

CURATED_FIELDS = (
    "compound_id",
    "name",
    "smiles",
    "source",
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
    "property_bin",
    "failed_criteria",
    "unknown_criteria",
)


def _positive_int(text: str) -> int:
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return value


def _bin_width(text: str) -> float:
    value = float(text)
    if not 0.0 < value <= 1.0:
        raise argparse.ArgumentTypeError("must be greater than 0 and at most 1")
    return value


def _row(candidate: Candidate, width: float) -> dict:
    compound = candidate.compound
    return {
        "compound_id": compound.compound_id,
        "name": compound.name,
        "smiles": compound.smiles,
        "source": candidate.source,
        "tier": candidate.result.tier,
        "score": f"{candidate.result.score:.4f}",
        "mw": compound.mw,
        "logp": compound.logp,
        "tpsa": compound.tpsa,
        "hbd": compound.hbd,
        "hba": compound.hba,
        "rotatable_bonds": compound.rotatable_bonds,
        "pka": "" if compound.pka is None else compound.pka,
        "charge": compound.charge,
        "property_bin": "-".join(str(cell) for cell in property_bin(compound, width)),
        "failed_criteria": ";".join(candidate.result.failed_criteria()),
        "unknown_criteria": ";".join(candidate.result.unknown_criteria()),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pnn.curate",
        description=(
            "Merge compound CSVs, remove duplicate IDs and SMILES, filter by screening tier, "
            "and cap each property-space bin."
        ),
    )
    parser.add_argument("inputs", nargs="+", help="one or more compound CSVs")
    parser.add_argument("--out", default="curated_library.csv", help="curated CSV path")
    parser.add_argument("--json", dest="json_path", help="optional JSON summary path")
    parser.add_argument(
        "--min-tier",
        choices=("A", "B", "C"),
        default="B",
        help="keep this screening tier and better (default: B)",
    )
    parser.add_argument("--per-bin", type=_positive_int, default=25, help="maximum compounds per property bin")
    parser.add_argument("--bin-width", type=_bin_width, default=0.1, help="normalized bin width (0-1)")
    parser.add_argument("--max-compounds", type=_positive_int, help="optional global size limit")
    return parser


def _failure(what: str, why: str, fix: str) -> int:
    print(f"What: {what}", file=sys.stderr)
    print(f"Why: {why}", file=sys.stderr)
    print(f"Fix: {fix}", file=sys.stderr)
    return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    out = Path(args.out)
    try:
        inputs = [
            (str(Path(path)), load_compounds(Path(path), allow_duplicates=True)) for path in args.inputs
        ]
        candidates = prepare_candidates(inputs)
        unique, counts = deduplicate(candidates)
        selected, summary = curate(
            unique,
            min_tier=args.min_tier,
            per_bin=args.per_bin,
            bin_width=args.bin_width,
            max_compounds=args.max_compounds,
        )
        if not selected:
            return _failure(
                "no compounds survived curation.",
                "every input compound was rejected by the tier floor or the input set was empty.",
                "add better-characterized compounds or relax --min-tier.",
            )
        write_csv(out, CURATED_FIELDS, [_row(candidate, args.bin_width) for candidate in selected])
        if args.json_path:
            write_json(
                Path(args.json_path),
                {
                    "output": str(out),
                    "inputs": {source: len(compounds) for source, compounds in inputs},
                    "input_rows": len(candidates),
                    **counts,
                    **summary,
                },
            )
    except (CompoundError, CurationError) as exc:
        return _failure(
            str(exc),
            "curation needs readable compound CSVs with consistent IDs and the required property columns.",
            "check the screening contract in computational/screening_pipeline.md and the curation rules "
            "in computational/library_curation.md.",
        )
    except OSError as exc:
        return _failure(
            str(exc),
            "the curated CSV or JSON summary could not be written.",
            "choose a writable --out/--json path and rerun.",
        )
    print(
        f"Curated {summary['selected']} of {summary['eligible']} eligible compound(s) "
        f"from {len(candidates)} input row(s) -> {out}"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())