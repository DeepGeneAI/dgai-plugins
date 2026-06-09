# Gene Brief: OTC — Ornithine Transcarbamylase Deficiency

**Panel:** Urea Cycle Disorders Expert Panel (VCEP) · **ClinGen:** https://clinicalgenome.org/affiliation/50100/
**CSpec version:** 1.0.0 (approved January 2026) · **Prepared:** 2026-06-09
**Sources:** GeneReviews, OMIM, ClinGen/CSpec, ClinVar, PubMed, gnomAD

---

## Disease overview

OTC deficiency is an X-linked disorder of the urea cycle caused by loss-of-function variants in the OTC gene, which encodes ornithine transcarbamylase.[^1] The enzyme catalyzes the second step of the urea cycle, condensing ornithine and carbamoyl phosphate to form citrulline in hepatic mitochondria. Deficiency leads to ammonia accumulation and citrulline deficiency.[^2] Clinical severity follows a bimodal distribution: hemizygous males with severe variants typically present in the neonatal period with encephalopathy, hyperammonemia, and high mortality without early intervention, while those with hypomorphic alleles may present in adulthood with episodic hyperammonemia. Heterozygous females show the widest range, from entirely asymptomatic to recurrent hyperammonemic crises, depending on X-inactivation patterns in the liver.[^1] OTC deficiency is the most common urea cycle disorder, with an estimated incidence of approximately 1 in 56,000 live births, though population surveys suggest this is an undercount due to underdiagnosis of mild female carriers.[^2]

## VCEP protocol status

**CSpec version:** 1.0.0, approved January 2026.[^3] The panel's published specifications are among the most complete in the UCD VCEP portfolio, with approved rules for 10 of the 12 applicable ACMG/AMP codes.

Gene-specific code modifications:

| Code | Standard rule | Panel modification | Source |
|------|--------------|-------------------|--------|
| PS3/BS3 | Well-established functional assay showing damaging/benign effect | MAVE dataset (Lo RS et al. 2023) accepted as PS3 moderate for variants with residual activity <20% of wild-type; BS3 supporting for >50% | [^3][^4] |
| PM2 | Absent or extremely rare in gnomAD | Hemizygous male gnomAD counts accepted; MAF threshold set at <0.001 for hemizygous males | [^3] |
| PP3/BP4 | Multiple computational predictors support | REVEL ≥0.7 = PP3 supporting; REVEL ≤0.15 = BP4 supporting; SpliceAI delta ≥0.2 for splice predictors | [^3] |
| PP4 | Phenotype highly specific | Activated: neonatal hyperammonemia with elevated glutamine + low/absent citrulline qualifies | [^3] |
| PVS1 | Null variants in LOF-disease genes | Applied to most null types; C-terminal truncations after residue 322 require downgrade to strong due to residual activity | [^3] |

## Evidence-code challenges

**PS3/BS3 — Functional evidence**
The Lo RS et al. (2023) MAVE dataset covers ~1,570 OTC missense variants and provides residual enzymatic activity scores, giving the panel a quantitative PS3/BS3 framework unavailable for most genes.[^4] The main unresolved tension is where to set the intermediate zone: variants with 20–50% residual activity lack a clear rule in the current CSpec and fall into a gray region where PS3 and BS3 both apply at supporting strength. Late-onset presentations are enriched in this zone. Additional calibration against clinical outcomes for intermediate-activity variants is ongoing.[^4]

**PVS1 — Null variant scope**
For most null variant types (nonsense, canonical splice ±1/2, frameshift), PVS1 applies at very strong strength. The exception is C-terminal truncations beyond residue 322: the OTC protein retains partial activity when the C-terminus is truncated within the last ~50 amino acids, and the panel has specified a downgrade to PVS1 strong for this subset.[^3] Splice region variants beyond ±2 require SpliceAI delta score support before invoking PVS1; the CSpec threshold is 0.2.[^3]

**PM2 — Allele frequency in hemizygous males**
gnomAD hemizygous male counts for X-linked genes are sparser than autosomal observations, making PM2 harder to invoke cleanly for common-in-heterozygotes variants. The panel uses a hemizygous MAF threshold of <0.001 (rather than the default <0.0001) to account for this, but borderline variants with 1–3 hemizygous observations in gnomAD remain a source of inter-lab disagreement.[^5]

**PP3/BP4 — Computational predictors**
The panel has adopted REVEL ≥0.7 for PP3 supporting and ≤0.15 for BP4 supporting, consistent with ClinGen SVI recommendations.[^3] The boundary zone (REVEL 0.15–0.70) is neither PP3 nor BP4 — a wider neutral zone than many panels use. For splicing predictions, SpliceAI delta ≥0.2 activates PP3 at supporting; there is no approved upgrade to moderate for this gene. Inter-lab variation in PP3 application remains the most common source of conflicting ClinVar submissions for OTC missense variants.

## Classification-relevant literature

1. **Lo RS et al. (2023)** — High-throughput functional profiling of 1,570 SNV-accessible OTC missense variants; directly applicable as PS3/BS3 evidence under the approved CSpec.[^4]
2. **Staufner C et al. (2025/2026)** — Biochemical and enzymatic characterization of the c.-106C>A promoter variant across multiple families; supports Pathogenic classification for late-onset OTC deficiency using PS3 + PS4 + PP4 + PP1.[^6]
3. **Caldovic L et al. (2015)** — Comprehensive missense variant function study using COS-7 and patient-derived cell lines; historical baseline for PS3 evidence before MAVE data were available; still cited by labs lacking MAVE scores.[^7]
4. **Yuen CT et al. (2021)** — ClinVar analysis of OTC variants submitted across 14 labs; documents systematic PP3 disagreement and highlights the REVEL boundary zone as the primary source of VUS-to-likely pathogenic discordance.[^8]
5. **Ah Mew N et al. (2023, GeneReviews update)** — Current clinical management and diagnostic criteria; relevant for PP4 calibration, particularly the biochemical phenotype criteria the panel uses.[^1]

## Open questions

1. How should variants with 20–50% residual activity in the Lo RS MAVE dataset be classified when the only other evidence is PP3 supporting? The current CSpec does not give these a clear rule, and labs are handling them inconsistently.[^4]
2. For heterozygous females with skewed X-inactivation and clinical hyperammonemia, does PP4 apply at supporting strength, or does variable X-inactivation disqualify it? The CSpec activates PP4 for the biochemical phenotype but does not address whether PP4 persists when the clinical picture is X-inactivation-dependent.[^3]
3. Which ClinVar submitters have active expert-panel conflicts with the UCD VCEP's OTC calls, and what evidence would resolve them? The most common conflict type is PP3-driven likely pathogenic vs. VCEP's VUS for REVEL 0.5–0.7 variants.[^5]

---

## References

[^1]: GeneReviews — Ornithine Transcarbamylase Deficiency — https://www.ncbi.nlm.nih.gov/books/NBK154378/
[^2]: OMIM #311250 (OTC deficiency) — https://www.omim.org/entry/311250 · OMIM *300461 (OTC gene) — https://omim.org/entry/300461
[^3]: ClinGen CSpec v1.0.0 — https://cspec.genome.network/cspec/Organization/id/639508902
[^4]: Lo RS et al. (2023) — https://pubmed.ncbi.nlm.nih.gov/37146589/
[^5]: ClinVar OTC gene view — https://www.ncbi.nlm.nih.gov/clinvar/?term=OTC%5Bgene%5D
[^6]: Staufner C et al. (2025/2026) — https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12808918/
[^7]: Caldovic L et al. (2015) — https://pubmed.ncbi.nlm.nih.gov/25736269/
[^8]: Yuen CT et al. (2021) — https://pubmed.ncbi.nlm.nih.gov/33772528/
