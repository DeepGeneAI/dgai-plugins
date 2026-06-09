# Gene Brief: ASS1 — Citrullinemia Type I

**Panel:** Urea Cycle Disorders Expert Panel (VCEP) · **ClinGen:** https://clinicalgenome.org/affiliation/50100/
**CSpec version:** 1.0.0 (approved January 2026) · **Prepared:** 2026-06-09
**Sources:** GeneReviews, OMIM, ClinGen/CSpec, ClinVar, PubMed

---

## Disease overview

Argininosuccinate synthetase 1 (ASS1) deficiency causes citrullinemia type I (CTLN1), an autosomal recessive urea cycle disorder.[^1] ASS1 encodes the cytosolic enzyme that condenses citrulline and aspartate to form argininosuccinate, the third step of the urea cycle. Enzyme deficiency blocks nitrogen disposal, leading to citrulline and ammonia accumulation.[^2] Presentation spans a wide spectrum: the severe neonatal form presents in the first days of life with rapidly progressing hyperammonemia, lethargy, and encephalopathy; the mild form is diagnosed incidentally or through newborn screening with minimal or no symptoms; and a subacute/adult-onset form presents with episodic hyperammonemia triggered by illness or physiological stress.[^1] CTLN1 incidence is approximately 1 in 57,000 live births in the United States based on newborn screening data, making it the third most common urea cycle disorder after OTC deficiency and ASL deficiency.[^2]

## VCEP protocol status

**CSpec version:** 1.0.0, approved January 2026.[^3] The UCD VCEP covers both OTC and ASS1 under a shared panel structure. Code modifications for ASS1 differ from OTC in two key areas: (1) no hemizygous MAF consideration, as ASS1 is autosomal; (2) the functional assay landscape for ASS1 is less mature than OTC, with the primary MAVE dataset (Landstrom et al. 2025) still a bioRxiv preprint as of June 2026 at the time of CSpec approval and at time of writing.

Gene-specific code modifications:

| Code | Standard rule | Panel modification | Source |
|------|--------------|-------------------|--------|
| PS3/BS3 | Well-established functional assay | Landstrom et al. (2025) MAVE dataset provisionally applicable pending peer review; enzyme activity <20% = PS3 moderate | [^3][^4] |
| PP3/BP4 | Multiple computational predictors | REVEL ≥0.7 = PP3 supporting; ≤0.15 = BP4 supporting (same thresholds as OTC) | [^3] |
| PP4 | Phenotype highly specific | Activated: hyperammonemia + citrulline elevation ≥10× upper limit of normal qualifies | [^3] |
| PVS1 | Null variants in LOF-disease genes | Applied broadly; no defined C-terminal exception as in OTC | [^3] |
| PM2 | Absent or extremely rare in gnomAD | Standard autosomal threshold: allele frequency <0.0001 in gnomAD non-Finnish European | [^3] |

## Evidence-code challenges

**PS3/BS3 — Functional evidence maturity**
The Landstrom et al. (2025) MAVE dataset is the primary functional reference for ASS1 missense variants, covering 2,193 substitutions.[^4] Because it was a preprint at CSpec approval, the panel incorporated it provisionally: PS3 moderate applies when the MAVE residual activity is <20% of wild-type, but the panel has not yet published a formal PS3/BS3 calibration table with sensitivity and specificity metrics. Labs applying the dataset are doing so under informal guidance. The peer-reviewed version is expected to trigger a CSpec update with clearer thresholds. Until then, labs may diverge in how they treat the 20–40% intermediate zone.

**PM1 — Hotspot definition**
Unlike some genes with structurally defined hotspot residues, ASS1 lacks a formally approved PM1 hotspot in the current CSpec.[^3] The enzyme's active site residues are well-characterized from crystal structures, but no lab has published a variant-density analysis sufficient to support formal PM1 region designation. The result: PM1 is essentially inapplicable for ASS1 today, which means moderate pathogenic evidence relies disproportionately on PS3 and PM2 — a narrower base than panels where PM1 is active.

**PP3/BP4 — Computational predictor reliability**
REVEL was calibrated primarily on autosomal dominant genes. For ASS1, where almost all pathogenic variants are recessive loss-of-function missense, REVEL's intermediate zone (0.15–0.70) captures a disproportionate number of hypomorphic alleles responsible for the mild/asymptomatic presentation. These alleles produce reduced but not absent enzyme activity; REVEL scores them in the 0.4–0.65 range, where neither PP3 nor BP4 applies. The result is a large class of variants where computational evidence is silent and functional data are needed to classify.[^5]

**PP4 — Phenotype threshold specificity**
The panel's PP4 rule requires citrulline elevation ≥10× upper limit of normal, which corresponds to the biochemical signature of severe CTLN1. Mild and asymptomatic patients identified through newborn screening may have citrulline elevations below this threshold. For these cases, PP4 does not apply, removing one of the few supporting codes available for hypomorphic alleles.[^3]

## Classification-relevant literature

1. **Landstrom et al. (2025, preprint)** — MAVE profiling of 2,193 ASS1 missense variants; identifies 547 pathogenic substitutions and 25 ClinVar VUS with reclassification support; the primary PS3/BS3 reference.[^4]
2. **Guo X et al. (2023)** — Functional characterization of novel ASS1 variants using western blot, qPCR, and ELISA; illustrates the multi-assay approach needed when MAVE data are absent.[^6]
3. **Alfadhel M et al. (2023)** — Variant analysis across ten Middle Eastern CTLN1 families; population-specific allele frequency data useful for PM2 calibration in non-European cohorts.[^7]
4. **Häberle J et al. (2019)** — International consensus on urea cycle disorders; defines clinical staging used in PP4 framing; still the reference standard for biochemical diagnostic criteria.[^8]
5. **Summar ML et al. (2013, GeneReviews)** — Foundational clinical overview of CTLN1; incidence estimates and inheritance patterns; cited for disease overview and PP4 phenotype criteria.[^1]

## Open questions

1. When will the Landstrom MAVE dataset receive peer-reviewed publication and a corresponding CSpec update, and how will the PS3 calibration table handle the 20–40% intermediate-activity zone?[^4]
2. Is there sufficient structural and variant-density data to define a PM1 hotspot for ASS1, and which active-site residues would be candidates? Resolving this would add a moderate pathogenic code to a gene currently relying almost entirely on PS3 and PM2.[^3]
3. For hypomorphic alleles identified through newborn screening — citrulline elevation below the PP4 threshold, REVEL in the neutral zone, no MAVE data yet — what combination of evidence is sufficient to move a VUS to likely pathogenic? The current CSpec does not address this explicitly, and these variants are the highest-volume source of unresolved VUS for the panel.[^3][^5]

---

## References

[^1]: GeneReviews — Citrullinemia Type I — https://www.ncbi.nlm.nih.gov/books/NBK1458/
[^2]: OMIM #215700 (citrullinemia type I) — https://omim.org/entry/215700
[^3]: ClinGen CSpec v1.0.0 — https://cspec.genome.network/cspec/Organization/id/639508902
[^4]: Landstrom et al. (2025 preprint) — https://www.biorxiv.org/content/10.1101/2025.09.17.676623
[^5]: ClinVar ASS1 gene view — https://www.ncbi.nlm.nih.gov/clinvar/?term=ASS1%5Bgene%5D
[^6]: Guo X et al. (2023) — https://pubmed.ncbi.nlm.nih.gov/37485339/
[^7]: Alfadhel M et al. (2023) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9938749/
[^8]: Häberle J et al. (2019) — https://pubmed.ncbi.nlm.nih.gov/30770613/
