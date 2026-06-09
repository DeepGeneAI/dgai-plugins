# Evidence-code reference

Quick reference for the ACMG/AMP codes most commonly customized at the gene level. Use this as a checklist when writing the evidence-code challenges section. Only include a code if there is something specific to say about the target gene.

## Pathogenic codes

**PVS1 — Null variant (very strong pathogenic)**
Standard: predicted null variants (nonsense, frameshift, splice ±1/2, initiation, exon deletion) in genes where LOF is a known mechanism of disease.
Gene-specific issues: Not all null variants are equivalent — some genes have alternative start codons, out-of-frame exons, or C-terminal truncations that preserve function. The panel must define which null variant types qualify and whether PVS1 should be downgraded to strong, moderate, or supporting based on variant location relative to functional domains.
Data sources: CSpec NMD escaping exon boundaries; gnomAD pLoF constraint score (pLI).

**PS3 — Functional studies (strong pathogenic)**
Standard: well-established functional studies showing damaging effect consistent with disease mechanism.
Gene-specific issues: Which assay types count? What is the evidence threshold (positive control range, negative control range)? MAVE/saturation genome editing datasets provide quantitative support for many genes — does the panel have a calibrated PS3 score? What is the published sensitivity/specificity for the assay?
Data sources: MAVE scores, published functional studies, ClinGen SVI calibration papers.

**PS4 — Prevalence in affecteds (strong pathogenic)**
Standard: variant prevalence in affected individuals significantly greater than controls.
Gene-specific issues: For rare disorders, case counts are small. The panel may have lowered the PS4 threshold or allowed PS4 supporting for a single well-documented proband. Check whether the CSpec defines case count minimums.

**PM1 — Mutational hotspot (moderate pathogenic)**
Standard: variant in a mutational hotspot or well-established functional domain without benign variation.
Gene-specific issues: Is a hotspot defined for this gene? What domain boundaries does the panel use? Does the CSpec list specific exons or amino acid ranges that qualify for PM1?

**PM2 — Absent from controls (moderate pathogenic; often downgraded to supporting)**
Standard: absent or extremely rare in population databases (gnomAD, etc.).
Gene-specific issues: Hemizygous genes (X-linked) require gnomAD hemizygous counts, which are sparse. AR genes may have a different MAF threshold than AD genes. ClinVar allele frequency interpretation varies. What has the panel specified for this gene?
Data sources: gnomAD gene page; ClinGen allele frequency working group guidance.

**PP3 — Computational evidence (supporting pathogenic)**
Standard: multiple lines of computational evidence support deleterious effect.
Gene-specific issues: Which predictors does the panel accept? REVEL, BayesDel, SpliceAI each have gene-specific calibration issues. What threshold has the panel set? Is there a calibrated REVEL score for this gene's variant class? Does the CSpec restrict PP3 to missense only, or also apply it to synonymous/intronic variants via splicing predictors?
Data sources: REVEL scores, BayesDel scores, SpliceAI delta scores, published calibration papers.

**PP4 — Phenotype specificity (supporting pathogenic)**
Standard: patient phenotype or family history highly specific for a disease with a single genetic etiology.
Gene-specific issues: Applicable only when the disease phenotype is specific enough to be clinically diagnostic on its own (e.g., OTC deficiency with hyperammonemia + low citrulline). Not applicable for nonspecific phenotypes. Does the CSpec activate or restrict PP4?

## Benign codes

**BS3 — Functional studies (strong benign)**
Paired with PS3: same assay, benign result. Same gene-specific issues apply.

**BS4 — Non-segregation (strong benign)**
Rarely invoked in small-family studies. Note if the panel has guidance on minimum LOD or family size.

**BP4 — Computational evidence (supporting benign)**
Paired with PP3. Same predictor and threshold questions apply.

**BA1 — Allele frequency (stand-alone benign)**
Standard: allele frequency above 5% in population databases.
Gene-specific issues: Some genes have disorder-specific MAF thresholds below 5% (e.g., for dominant genes with incomplete penetrance). Has the panel modified the BA1 threshold?

## Frequently contested combinations

- **PS3 + BS3 conflict**: When assay data and case reports disagree. Especially common for hypomorphic alleles.
- **PM2 + gnomAD hemizygote count**: For X-linked genes, how to handle male hemizygotes in gnomAD.
- **PP3 strength**: Many panels have moved PP3 from supporting to moderate for variants with high REVEL scores. Check CSpec for any up-classification rule.
- **PVS1 + functional assay**: If a predicted null variant shows residual function in a MAVE, should PVS1 be downgraded? Few CSpecs address this explicitly.
