"""Unit tests for bioisosteric replacement and metabolic soft-spot optimizer."""

import tempfile
import unittest
from pathlib import Path

from pnn.bioisostere import (
    BioisostereError,
    generate_bioisosteres,
    main,
    render_bioisostere_report,
    run_bioisostere_pipeline,
)


class TestBioisostere(unittest.TestCase):
    def test_generate_bioisosteres(self) -> None:
        # Test SMILES with benzene and amide motifs
        smiles = "c1ccccc1C(=O)NC1CCOCC1"
        analogs = generate_bioisosteres(
            parent_id="TEST-01",
            smiles=smiles,
            mw=250.0,
            logp=2.1,
            tpsa=45.0,
            hbd=1,
            hba=3,
            rotb=3,
            pka=7.5,
        )
        self.assertGreater(len(analogs), 0)
        self.assertEqual(analogs[0].parent_id, "TEST-01")
        self.assertTrue(analogs[0].analog_id.startswith("TEST-01-BIO"))
        self.assertTrue(any("FAVORABLE" in a.optimization_verdict for a in analogs))

        row = analogs[0].as_row()
        self.assertIn("analog_smiles", row)
        self.assertIn("cns_mpo_score", row)

    def test_run_bioisostere_pipeline_missing_file_raises(self) -> None:
        with self.assertRaises(BioisostereError):
            run_bioisostere_pipeline(Path("non_existent_library.csv"))

    def test_run_bioisostere_pipeline_vendor_lib(self) -> None:
        vendor_csv = Path("data/compounds/vendor_library.csv")
        if not vendor_csv.is_file():
            return

        analogs = run_bioisostere_pipeline(vendor_csv, target_parent_id="PNN-101")
        self.assertGreater(len(analogs), 0)
        for a in analogs:
            self.assertEqual(a.parent_id, "PNN-101")
            self.assertGreater(a.mw, 0.0)

    def test_render_bioisostere_report(self) -> None:
        smiles = "c1ccccc1C(=O)NC1CCOCC1"
        analogs = generate_bioisosteres(
            parent_id="PNN-101",
            smiles=smiles,
            mw=320.0,
            logp=2.4,
            tpsa=50.0,
            hbd=1,
            hba=3,
            rotb=4,
        )
        report = render_bioisostere_report(analogs, "PNN-101")
        self.assertIn("Bioisosteric Replacement", report)
        self.assertIn("PNN-101", report)
        self.assertIn("Synthetic Priority Recommendations", report)

    def test_bioisostere_cli(self) -> None:
        vendor_csv = Path("data/compounds/vendor_library.csv")
        if not vendor_csv.is_file():
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_csv = Path(tmp_dir) / "analogs.csv"
            out_md = Path(tmp_dir) / "report.md"
            out_json = Path(tmp_dir) / "summary.json"

            exit_code = main([
                "--compounds", str(vendor_csv),
                "--parent", "PNN-101",
                "--out", str(out_csv),
                "--report", str(out_md),
                "--json", str(out_json),
            ])
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_csv.is_file())
            self.assertTrue(out_md.is_file())
            self.assertTrue(out_json.is_file())


if __name__ == "__main__":
    unittest.main()
