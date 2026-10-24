# Bioisosteric Replacement & Metabolic Soft-Spot Optimization

## Overview

Advancing in vitro qualified leads toward clinical development requires balancing nanomolar receptor potency with metabolic stability, low clearance, and optimal blood-brain barrier permeability. The `pnn.bioisostere` module systematically applies codified medicinal chemistry transformation rules to candidate SMILES strings, recalculating continuous Pfizer CNS MPO scores and flagging optimization potential.

## Codified Transformation Rules

1. **Aromatic Fluorination (CYP Soft-Spot Block)**:
   - *Target Motif*: Monosubstituted aromatic benzene ring (`c1ccccc1`).
   - *Replacement*: Para-fluorinated ring (`c1ccc(F)cc1`).
   - *Rationale*: Blocks rapid Cytochrome P450 aromatic para-hydroxylation, increasing metabolic half-life in liver microsomes without adding significant molecular weight (+18.0 Da) or steric bulk.

2. **Trifluoromethyl Substitution (Lipophilic Shield)**:
   - *Target Motif*: Methyl group (`-CH3`).
   - *Replacement*: Trifluoromethyl group (`-C(F)(F)F`).
   - *Rationale*: Increases metabolic oxidative stability, metabolic half-life, and lipophilic binding efficiency.

3. **Cyclopropyl Amide Rigidification (Conformational Restriction)**:
   - *Target Motif*: Linear secondary amide (`C(=O)NC`).
   - *Replacement*: Cyclopropyl-constrained amide (`C(=O)NC1CC1`).
   - *Rationale*: Decreases conformational entropy of binding by rigidifying the amide linker and shielding the carbonyl from peptidase hydrolysis.

4. **Morpholine Basicity Attenuation**:
   - *Target Motif*: Morpholine heterocycle (`C1COCCN1`).
   - *Replacement*: Fluorinated morpholine (`C1C(F)OCCN1`).
   - *Rationale*: Electron-withdrawing fluorine atoms attenuate aliphatic nitrogen basicity, depressing $\text{p}K_a$ from $>8.5$ to $7.2 - 7.8$. This decreases hERG channel liability and increases the free, unbound brain fraction ($f_{u,\text{brain}}$).

5. **Deuterium Switch (Kinetic Isotope Effect)**:
   - *Target Motif*: Labile methoxy group (`-OCH3`).
   - *Replacement*: Trideuteromethoxy (`-OC([2H])([2H])[2H]`).
   - *Rationale*: Carbon-deuterium (C-D) bonds exhibit a stronger zero-point vibrational energy than C-H bonds, slowing CYP-mediated O-demethylation (primary kinetic isotope effect).

6. **Ester-to-Oxadiazole Heterocycle Replacement**:
   - *Target Motif*: Labile aliphatic ester (`C(=O)OC`).
   - *Replacement*: 1,2,4-Oxadiazole ring (`c1nc(C)no1`).
   - *Rationale*: Replaces an ester bond vulnerable to systemic carboxylesterase cleavage with a stable, planar heterocyclic bioisostere.

## Command-Line Usage

```bash
python -m pnn.bioisostere \
  --compounds data/compounds/vendor_library.csv \
  --parent PNN-101 \
  --out output/bioisosteric_analogs.csv \
  --report output/bioisostere_report.md \
  --json output/bioisostere_summary.json
```
