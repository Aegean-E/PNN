# Human Allometric Dose Projection & IND Regulatory Candidate Dossier

## Overview

The `pnn.ind` module implements standard FDA (CDER) and ICH guidance for translating preclinical pharmacokinetic (PK) and pharmacodynamic (PD) parameters into first-in-human starting doses and compiling an Investigational New Drug (IND) regulatory candidate dossier.

## Allometric Dose Scaling Equations

1. **Human Equivalent Dose (HED)**:
   Per FDA Guidance for Industry (Estimating the Maximum Safe Starting Dose in Initial Clinical Trials):
   $$\text{HED}\ (\text{mg/kg}) = \text{Animal Dose}\ (\text{mg/kg}) \times \left( \frac{\text{Animal } K_m}{\text{Human } K_m} \right)$$
   For mouse to human conversion:
   $$\frac{K_{m,\text{mouse}}}{K_{m,\text{human}}} = \frac{3}{37} \approx 0.08108$$

2. **Total Human Daily Dose**:
   $$\text{Total Daily Dose}\ (\text{mg}) = \text{HED}\ (\text{mg/kg}) \times 60.0\text{ kg}$$

3. **Interspecies Clearance ($CL$) and Volume ($V_d$) Scaling**:
   Based on empirical allometric body weight exponents:
   $$CL_{\text{human}} = CL_{\text{mouse}} \times W_{\text{mouse}} \times \left( \frac{60.0}{0.02} \right)^{0.75}$$
   $$V_{d,\text{human}} = V_{d,\text{mouse}} \times W_{\text{mouse}} \times \left( \frac{60.0}{0.02} \right)^{1.0}$$

4. **Projected Human Elimination Half-Life ($t_{1/2}$)**:
   $$t_{1/2,\text{human}} = \frac{\ln(2) \times V_{d,\text{human}}}{CL_{\text{human}}}$$

5. **Maximum Recommended Starting Dose (MRSD)**:
   Starting from the animal No Observed Adverse Effect Level (NOAEL, typically set at $5 \times$ efficacious dose):
   $$\text{NOAEL}_{\text{HED}} = \text{NOAEL}_{\text{mouse}} \times 0.08108$$
   Applying standard ICH M3(R2) 10-fold safety factor:
   $$\text{MRSD}\ (\text{mg}) = \frac{\text{NOAEL}_{\text{HED}}}{10.0} \times 60.0\text{ kg}$$

## Safety Pharmacology & Protocol Checklist

- **ICH S7A/S7B Core Safety Battery**:
  - Central Nervous System: Modified Irwin screen / Functional Observational Battery (FOB).
  - Cardiovascular System: In vitro hERG automated patch clamp and telemetry ECG (QTc interval).
  - Respiratory System: Whole-body plethysmography (tidal volume and respiratory rate).
- **Phase 1 Trial Architecture**:
  - Single Ascending Dose (SAD) with modified Fibonacci dose escalation cohorts in healthy adult volunteers.
  - Multiple Ascending Dose (MAD) 14-day intermittent pulsatile dosing evaluating CSF-to-plasma drug partition ($K_{p,\text{CSF}}$) and insulin sensitivity biomarkers.

## Command-Line Usage

```bash
python -m pnn.ind \
  --compounds data/compounds/vendor_library.csv \
  --candidates data/preclinical/pk_timecourse_template.csv \
  --out output/human_dose_projections.csv \
  --dossier output/ind_dossier.md \
  --json output/ind_summary.json
```
