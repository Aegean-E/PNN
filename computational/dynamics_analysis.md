# Molecular Dynamics Trajectory & Contact Stability Analysis

## Overview

Molecular Dynamics (MD) trajectory analysis evaluates the nanosecond-scale kinetic stability of candidate ligand binding poses within perineuronal net receptor pockets (such as the Protein Tyrosine Phosphatase Sigma [PTP$\sigma$] CSPG binding pocket).

In virtual docking screening, high static affinity scores (e.g., AutoDock Vina or Glide) do not guarantee physical residence time or resistance to thermal fluctuations. The `pnn.dynamics` module evaluates time-resolved trajectories to quantify pose drift, pocket breathing, and intermolecular contact persistence.

## Key Trajectory Metrics

1. **Ligand RMSD ($\text{RMSD}_{\text{lig}}$)**:
   - Measures root-mean-square coordinate deviation of ligand heavy atoms relative to the docked starting pose over time $t$.
   - **Stable Threshold**: Mean $< 2.0$ Å, Maximum $< 3.2$ Å.

2. **RMSD Drift ($\Delta \text{RMSD}$)**:
   - Difference between the average RMSD in the final 20% of the simulation and the initial 20%.
   - Values $\ge 1.5$ Å indicate progressive translational creep or impending dissociation from the binding site.

3. **Protein Backbone RMSD ($\text{RMSD}_{\text{prot}}$)**:
   - Confirms that the target receptor fold remains stable throughout simulation ($< 2.5$ Å).

4. **Pocket Contact Persistence**:
   - Percentage of trajectory frames in which key electrostatic and hydrogen bonding interactions are preserved.
   - For PTP$\sigma$, critical basic pocket residues include:
     - **Lys201**: Core CSPG sulfate coordinator.
     - **Arg204**: Key electrostatic salt bridge.
     - **Lys207**: Outer pocket basic anchor.
     - **Arg210**: Secondary salt bridge partner.

5. **MM-GBSA Free Energy ($\Delta G_{\text{bind}}$)**:
   - Continuum electrostatic solvation binding free energy sampled across trajectory frames.
   - Optimal threshold: $\le -25.0\text{ kcal/mol}$.

## Pose Stability Classification

- **`STABLE_POSE`**: Mean ligand RMSD $< 2.0$ Å, drift $< 1.0$ Å, contact persistence $> 75\%$, protein backbone $< 2.5$ Å.
- **`MODERATE_MOBILITY`**: Mean ligand RMSD $2.0 - 3.5$ Å, contact persistence $50\% - 75\%$, or moderate drift.
- **`UNSTABLE_DRIFT`**: Mean ligand RMSD $> 3.5$ Å, contact persistence $< 50\%$, or dissociation event.

## Command-Line Usage

```bash
python -m pnn.dynamics \
  --trajectory data/dynamics/ptpsigma_md_trajectory_template.csv \
  --compound PNN-101 \
  --target PTPsigma \
  --out-dir output/dynamics \
  --report \
  --svg
```

The command generates:
- `{compound}_trajectory_metrics.csv`: Summary statistics and stability score.
- `{compound}_dynamics_summary.json`: JSON output for programmatic pipeline consumption.
- `{compound}_dynamics_report.md`: Markdown report detailing residue persistence.
- `{compound}_rmsd_trajectory.svg`: Vector time-series chart showing RMSD versus simulation time.
