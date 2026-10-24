"""Unit tests for human allometric dose projection and IND regulatory dossier generator."""

import tempfile
import unittest
from pathlib import Path

from pnn.ind import (
    HumanDoseProjection,
    IndError,
    calculate_allometric_scaling,
    compile_ind_dossier,
    load_candidate_records,
    main,
    project_clinical_candidates,
    render_ind_dossier,
)


class TestIndProjection(unittest.TestCase):
    def test_calculate_allometric_scaling(self) -> None:
        (
            hed,
            daily_mg,
            cl_h,
            vd_h,
            t12_h,
            noael,
            noael_hed,
            mrsd,
        ) = calculate_allometric_scaling(
            animal_dose_mg_kg=10.0,
            mouse_cl_l_h_kg=1.8,
            mouse_vd_l_kg=5.2,
        )
        # HED = 10 * (3 / 37) = 0.8108...
        self.assertAlmostEqual(hed, 0.811, places=2)
        # Daily mg = 0.8108 * 60 = 48.65...
        self.assertAlmostEqual(daily_mg, 48.6, places=1)
        self.assertGreater(cl_h, 0.0)
        self.assertGreater(vd_h, 0.0)
        self.assertGreater(t12_h, 0.0)
        self.assertEqual(noael, 50.0)
        self.assertAlmostEqual(mrsd, (noael_hed / 10.0) * 60.0, places=3)

    def test_project_clinical_candidates(self) -> None:
        compounds = [
            {"compound_id": "PNN-101", "name": "Compound 101"},
            {"compound_id": "PNN-102", "name": "Compound 102"},
        ]
        pk_data = {
            "PNN-101": {"dose_mg_kg": 10.0, "brain_kp": 0.45, "oral_f": 35.0},
            "PNN-102": {"dose_mg_kg": 15.0, "brain_kp": 0.35, "oral_f": 25.0},
        }
        projections = project_clinical_candidates(compounds, pk_data)
        self.assertEqual(len(projections), 2)
        self.assertEqual(projections[0].compound_id, "PNN-101")
        self.assertGreater(projections[0].phase1_mrsd_mg, 0.0)
        self.assertGreater(projections[0].therapeutic_index, 1.0)
        row = projections[0].as_row()
        self.assertIn("human_total_daily_dose_mg", row)

    def test_load_candidate_records_missing_file_raises(self) -> None:
        with self.assertRaises(IndError):
            load_candidate_records(Path("non_existent_compounds.csv"))

    def test_compile_ind_dossier_and_render(self) -> None:
        vendor_csv = Path("data/compounds/vendor_library.csv")
        pk_csv = Path("data/preclinical/pk_timecourse_template.csv")
        if not vendor_csv.is_file():
            return

        projections, dossier_md = compile_ind_dossier("PNN-101", vendor_csv, pk_csv)
        self.assertGreater(len(projections), 0)
        self.assertIn("Investigational New Drug (IND)", dossier_md)
        self.assertIn("PNN-101", dossier_md)
        self.assertIn("ICH S7A/S7B", dossier_md)
        self.assertIn("Phase 1 Clinical Protocol Architecture", dossier_md)

    def test_ind_cli(self) -> None:
        vendor_csv = Path("data/compounds/vendor_library.csv")
        pk_csv = Path("data/preclinical/pk_timecourse_template.csv")
        if not vendor_csv.is_file():
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_csv = Path(tmp_dir) / "doses.csv"
            out_md = Path(tmp_dir) / "dossier.md"
            out_json = Path(tmp_dir) / "summary.json"

            exit_code = main([
                "--compounds", str(vendor_csv),
                "--candidates", str(pk_csv),
                "--out", str(out_csv),
                "--dossier", str(out_md),
                "--json", str(out_json),
            ])
            self.assertEqual(exit_code, 0)
            self.assertTrue(out_csv.is_file())
            self.assertTrue(out_md.is_file())
            self.assertTrue(out_json.is_file())


if __name__ == "__main__":
    unittest.main()
