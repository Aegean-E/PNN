# PNN Project: Oral BBB-Penetrant Agents for Hypothalamic PNN Softening

Oral, blood-brain barrier-penetrant agents that soften hypothalamic perineuronal nets to restore insulin signaling in obesity.

## ⚡ 30-Second Cold-Start Quick Reference

- **Runtime Prerequisites**: Python 3.10+ (standard library only, for the screening pipeline and AIKit verification) and git 2.30+ (for version control).
- **Canonical Regression Shield Gate**:
  ```bash
  python -m unittest discover -s tests -t .
  ```
  Run it from this project root; AIKit runs the same command as part of `python aikit.py check PNN`.

### 🛠️ AIKit Commands (run from the AIKit workspace root)
| Role | Command |
|---|---|
| Status, task and gates | `python aikit.py status PNN` |
| Delivery check (clean tree + map) | `python aikit.py check PNN --strict` |
| Repair memory and map, then check | `python aikit.py fix PNN` |
| Resume an interrupted task | `python aikit.py resume PNN` |

## Mission Statement
**Ultimate Goal**: Fix insulin signaling in the hypothalamus to resolve obesity by developing oral, blood-brain barrier (BBB)-penetrant agents that soften perineuronal nets (PNNs) in the hypothalamus.

## 📦 What's Inside

```text
PNN/
├── README.md                      <- This file - project overview
├── .gitignore                     <- AIKit transient-state baseline
├── literature_review.md           <- Comprehensive literature findings
├── research_framework.md          <- Methodology & experimental design
├── .aikit/                        <- AIKit memory: guidelines, decisions, ledger, project record
├── agent_design/                  <- Agent design specifications
│   ├── target_profiles.md         <- Target protein profiles
│   ├── bbb_penetration_rules.md   <- BBB penetration guidelines
│   └── oral_bioavailability.md    <- Oral drug design principles
├── computational/                 <- Computational approaches
│   ├── docking_protocols.md       <- Molecular docking procedures
│   ├── docking_ranking.md         <- Docking consensus contract and normalization
│   ├── library_curation.md        <- Merge, dedupe and property-space diversity rules
│   └── screening_pipeline.md      <- Phase 2 property screening contract and rules
├── experimental/                  <- Experimental validation
│   └── experimental_protocols.md  <- In vitro/in vivo assay protocols
├── data/                          <- Data storage
│   ├── compounds/                 <- Compound libraries
│   │   └── screening_template.csv  <- Input header for the screening pipeline
│   ├── docking/                   <- Docking results
│   │   └── scores_template.csv    <- Input header for the consensus ranker
│   ├── assays/                    <- Assay results (empty until populated)
│   └── literature/                <- Extracted literature data (empty until populated)
├── docs/                          <- Documentation
│   ├── cold_start_guide.md        <- AI cold-start instructions
│   └── reproducibility.md         <- Reproducibility standards
├── pnn/                           <- Phase 2 pipeline (standard library only)
│   ├── __init__.py                <- Public API
│   ├── __main__.py                <- `python -m pnn` entry point
│   ├── cli.py                     <- Screening command contract
│   ├── compounds.py               <- Compound record and CSV ingestion
│   ├── curate.py                  <- `python -m pnn.curate` library command
│   ├── curation.py                <- Merge, dedupe and property-space caps
│   ├── docking.py                 <- Docking ingestion and consensus normalization
│   ├── rank.py                    <- `python -m pnn.rank` shortlist command
│   ├── reports.py                 <- Atomic CSV/JSON writers
│   ├── rules.py                   <- CNS/BBB property rules
│   └── screen.py                  <- Tiering, scoring and ranking
└── tests/                         <- Regression shield (docs and pipeline behaviour)
    ├── __init__.py                <- Makes the test package importable
    ├── test_cli.py                <- Screening command contract
    ├── test_curation.py           <- Merge, dedupe, bins and CLI contract
    ├── test_docking.py            <- Docking ingestion and normalization
    ├── test_docs.py               <- Required docs and README tree paths
    ├── test_rank.py               <- Consensus shortlist and CLI contract
    ├── test_rules.py              <- Rule boundaries
    └── test_screen.py             <- Tiering, ranking and CSV ingestion
```

## Phase 2: Property Screening Pipeline

`pnn` applies the project's CNS/BBB design windows to a compound CSV and ranks the
candidates into tiers `A`, `B`, `C` and `Reject`. It is a triage step, not a
permeability or efficacy model: tier labels decide which compounds reach docking
and assays, never whether a compound is claimed to be BBB-penetrant.

```bash
python -m pnn data/compounds/screening_template.csv --out ranked_compounds.csv
python -m pnn compounds.csv --out ranked.csv --json summary.json --min-tier B
```

The required columns are `compound_id`, `mw`, `logp`, `tpsa`, `hbd`, `hba` and
`rotatable_bonds`; optional ADMET and efficacy fields are listed with the full
rule table in [computational/screening_pipeline.md](computational/screening_pipeline.md).
Missing optional values become `UNKNOWN` and are never treated as passes.

## Phase 2: Docking Consensus Shortlist

`python -m pnn.rank` joins per-target docking results and ranks compounds by a
normalized Vina/Glide/MM-GBSA consensus. Raw engine scores are min-max scaled
within the run and renormalized for missing methods; only rows with a Vina score
enter the shortlist.

```bash
python -m pnn.rank data/docking/scores_template.csv \
    --screen ranked_compounds.csv \
    --out shortlist.csv --json shortlist_summary.json --max-rmsd 2.0
```

`--min-tier` (default `B`) keeps compounds that passed property triage, and
`coverage` shows whether Vina, Glide and MM-GBSA were all available. The contract,
weights and limits are in [computational/docking_ranking.md](computational/docking_ranking.md).

## Phase 2: Library Curation

`python -m pnn.curate` merges compound CSVs, resolves duplicate IDs and exact
SMILES, applies the screening-tier floor, and caps each six-property bin so the
screening set is diverse in property space.

```bash
python -m pnn.curate vendor_a.csv vendor_b.csv \
    --out curated_library.csv --json curation_summary.json \
    --min-tier B --per-bin 25 --max-compounds 200000
```

Every kept row retains its `source` path and `property_bin`; the JSON summary
reports duplicate, tier and cap removals. Exact-SMILES matching is not chemical
canonicalization; see [computational/library_curation.md](computational/library_curation.md).

## Core Scientific Hypothesis
Hypothalamic PNNs (primarily composed of chondroitin sulfate proteoglycans - CSPGs) create a physical and signaling barrier that:
1. **Impairs insulin receptor accessibility** on POMC/NPY neurons
2. **Disrupts insulin signaling cascades** (IRS-PI3K-AKT pathway)
3. **Contributes to leptin/insulin resistance** in diet-induced obesity
4. **Softening PNNs restores insulin sensitivity** and normalizes energy homeostasis

## Key Molecular Targets

### Primary Targets (PNN Degradation/Softening)
| Target | Function | Modality | BBB Penetration Strategy |
|--------|----------|----------|-------------------------|
| **ChABC** (Chondroitinase ABC) | Degrades CSPG GAG chains | Enzyme/Protein | Fusion with BBB shuttle (Angiopep-2, TfR) |
| **MMP-2/9** | Endogenous CSPG cleavage | Small molecule activators | Lipophilic prodrugs |
| **PTPσ** (RPTPσ) | CSPG receptor mediating inhibition | Antagonists/antibodies | Peptide mimetics |
| **LAR** (Leukocyte common antigen-related) | CSPG receptor | Antagonists | Small molecules |
| **NgR1/3** (Nogo receptors) | CSPG co-receptors | Antagonists | Cyclic peptides |

### Secondary Targets (Insulin Signaling Restoration)
| Target | Role | Strategy |
|--------|------|----------|
| **Insulin Receptor (IR)** | Primary insulin sensor | Allosteric modulators |
| **IRS-1/2** | Downstream adaptors | Phosphatase inhibitors (PTP1B) |
| **PI3K** | Signal transduction | Activators |
| **AKT/PKB** | Metabolic effector | Activators |
| **mTORC1** | Nutrient sensing | Modulators |
| **PTEN** | Negative regulator | Inhibitors |

## BBB Penetration Strategies for Oral Agents

### Physicochemical Rules (Modified Lipinski for CNS)
- **MW**: 200-450 Da (optimal 300-400)
- **logP**: 1.5-3.5 (optimal 2-3)
- **TPSA**: <70 Å² (optimal <60)
- **HBD**: ≤3
- **HBA**: ≤7
- **Rotatable bonds**: ≤7
- **pKa**: 7-9 (for basic amines) or 3-5 (for acids)
- **Charge**: Neutral or weakly basic at pH 7.4

### Transporter-Mediated Strategies
1. **LAT1** (Large neutral amino acid transporter) - amino acid mimetics
2. **MCT1** (Monocarboxylate transporter) - carboxylic acid prodrugs
3. **GLUT1** - glucose conjugates
4. **Nucleoside transporters** - nucleoside analogs

### Receptor-Mediated Transcytosis (RMT)
- **Transferrin Receptor (TfR)** - anti-TfR antibodies/peptides
- **Insulin Receptor** - insulin/peptide conjugates
- **LRP1** - Angiopep-2, ApoE mimetics
- **Dipyridamole-sensitive nucleoside transporter**

## Recursive Language Model Compatibility

This project is designed to work identically across AI cold starts through:

1. **Structured Documentation**: All knowledge captured in markdown with consistent formatting
2. **Explicit Protocols**: Step-by-step procedures for every computational/experimental task
3. **Version-Controlled Data**: Compound libraries, assay results, literature extractions
4. **Deterministic Pipelines**: Computational workflows with fixed parameters/seeds
5. **Self-Contained Context**: Each document contains sufficient context for independent use

### Cold-Start Protocol
When an AI agent starts fresh on this project:
1. Read `README.md` → `literature_review.md` → `research_framework.md`
2. Load `agent_design/target_profiles.md` for target specifications
3. Follow `computational/docking_protocols.md` for virtual screening
4. Reference `docs/cold_start_guide.md` for session initialization
5. All outputs saved to structured directories for continuity

## Literature Search Strategy

### Primary Databases
- PubMed/MEDLINE
- Embase
- Web of Science
- Scopus
- ChEMBL (compound bioactivity)
- BindingDB (binding affinities)
- PDB (structural data)

### Key Search Terms
```
("perineuronal net" OR "PNN" OR "chondroitin sulfate proteoglycan" OR "CSPG")
AND ("hypothalamus" OR "arcuate nucleus" OR "POMC" OR "NPY" OR "AgRP")
AND ("insulin signaling" OR "insulin resistance" OR "obesity" OR "energy homeostasis")
AND ("blood-brain barrier" OR "BBB" OR "CNS penetration" OR "oral bioavailability")
AND ("chondroitinase" OR "MMP" OR "PTPσ" OR "LAR" OR "NgR" OR "small molecule")
```

### Inclusion Criteria
- Peer-reviewed publications (2010-present priority)
- In vivo rodent/primate studies
- Human genetic association studies
- Structural biology data (cryo-EM, X-ray)
- Quantitative BBB penetration data (logBB, Kp,uu)

## Success Metrics

### Computational
- [ ] Virtual screening library >1M compounds
- [ ] Docking validation: ROC-AUC >0.85 on known actives
- [ ] MD simulations: >100ns stability for top 50 hits
- [ ] BBB prediction: >80% accuracy on test set

### In Vitro
- [ ] PNN degradation assay: EC50 <100 nM
- [ ] BBB permeability (PAMPA/MDCK): Pe >5 × 10⁻⁶ cm/s
- [ ] Insulin signaling rescue: >2-fold pAKT increase
- [ ] Cytotoxicity: CC50 >50 μM

### In Vivo
- [ ] Oral bioavailability: F >20%
- [ ] Brain/plasma ratio: >0.3
- [ ] Hypothalamic PNN reduction: >50% (WFA staining)
- [ ] Insulin sensitivity: >30% improvement (hyperinsulinemic-euglycemic clamp)
- [ ] Body weight reduction: >15% in DIO mice

## Timeline & Milestones

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Phase 1: Literature & Target Validation** | Months 1-3 | Comprehensive review, target prioritization |
| **Phase 2: Computational Discovery** | Months 3-6 | 50 lead compounds with predicted BBB penetration |
| **Phase 3: In Vitro Validation** | Months 6-12 | 10 compounds with confirmed PNN softening + BBB penetration |
| **Phase 4: In Vivo Proof-of-Concept** | Months 12-18 | 3 candidates with oral efficacy in DIO mice |
| **Phase 5: Lead Optimization** | Months 18-24 | 1 clinical candidate with IND-enabling package |

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| BBB penetration failure | High | Critical | Multiple parallel strategies (passive + active transport) |
| PNN softening causes plasticity side effects | Medium | High | Titratable dosing, intermittent regimens |
| Compensatory mechanisms | Medium | Medium | Combination therapy (PNN + insulin sensitizer) |
| Species translation | High | High | Human iPSC-derived hypothalamic organoids |
| Oral bioavailability | High | Critical | Prodrug strategies, formulation optimization |

## References Management
All references stored in `data/literature/references.bib` (BibTeX format) with tags:
- `#PNN_structure` - PNN composition/biology
- `#hypothalamus_insulin` - Hypothalamic insulin signaling
- `#BBB_penetration` - BBB transport mechanisms
- `#oral_CNS_drugs` - Successful oral CNS drug case studies
- `#chondroitinase` - ChABC and variants
- `#CSPG_receptors` - PTPσ, LAR, NgR biology
- `#obesity_models` - DIO, genetic obesity models

---

*Last Updated: 2026-10-22*
*Version: 1.3.0*
*Compatible with: Recursive Language Model cold starts*