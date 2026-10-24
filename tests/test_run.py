import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pnn.runner import (
    RunnerError,
    execute_turnkey_pipeline,
    main,
    print_run_banner,
)


class TestTurnkeyRunner(unittest.TestCase):
    def test_missing_vendor_library_raises(self) -> None:
        with self.assertRaises(RunnerError):
            execute_turnkey_pipeline(
                vendor_csv=Path("non_existent_vendor.csv"),
                repurposing_csv=None,
                docking_csv=Path("data/docking/multi_target_scores.csv"),
                degradation_csv=None,
                permeability_csv=None,
                cytotoxicity_csv=None,
                pk_csv=None,
                pd_csv=None,
                out_dir=Path("tmp_out"),
            )

    def test_execute_turnkey_pipeline_success(self) -> None:
        vendor_csv = Path("data/compounds/vendor_library.csv")
        repurposing_csv = Path("data/compounds/repurposing_library.csv")
        docking_csv = Path("data/docking/multi_target_scores.csv")
        degradation_csv = Path("data/assays/degradation_template.csv")
        permeability_csv = Path("data/assays/permeability_template.csv")
        cytotoxicity_csv = Path("data/assays/cytotoxicity_template.csv")
        pk_csv = Path("data/preclinical/pk_timecourse_template.csv")
        pd_csv = Path("data/preclinical/pd_metabolic_template.csv")

        if not vendor_csv.is_file() or not docking_csv.is_file():
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "output"
            summary = execute_turnkey_pipeline(
                vendor_csv=vendor_csv,
                repurposing_csv=repurposing_csv,
                docking_csv=docking_csv,
                degradation_csv=degradation_csv,
                permeability_csv=permeability_csv,
                cytotoxicity_csv=cytotoxicity_csv,
                pk_csv=pk_csv,
                pd_csv=pd_csv,
                out_dir=out_dir,
            )
            self.assertGreater(summary.curated_count, 0)
            self.assertGreater(summary.shortlisted_count, 0)
            self.assertGreater(summary.scaffolds_count, 0)
            self.assertTrue((out_dir / "shortlist.csv").is_file())
            self.assertTrue((out_dir / "lead_report.md").is_file())
            self.assertTrue((out_dir / "qualified_hits.csv").is_file())
            self.assertTrue((out_dir / "preclinical_candidates.csv").is_file())
            self.assertTrue((out_dir / "sar_clusters.csv").is_file())
            self.assertTrue((out_dir / "studio.html").is_file())

            # Verify banner printing without UnicodeEncodeError
            print_run_banner(summary)

    def test_runner_cli_execution_no_browser(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "run_out"
            rc = main(["--no-browser", "--out-dir", str(out_dir)])
            self.assertEqual(rc, 0)
            self.assertTrue((out_dir / "studio.html").is_file())

    @patch("webbrowser.open_new_tab")
    def test_runner_cli_execution_auto_opens_browser(self, mock_open) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_dir = Path(tmp_dir) / "run_out"
            rc = main(["--out-dir", str(out_dir)])
            self.assertEqual(rc, 0)
            self.assertTrue(mock_open.called)
            call_arg = mock_open.call_args[0][0]
            self.assertIn("studio.html", call_arg)


if __name__ == "__main__":
    unittest.main()
