# Pain-point framing

The Gene Report Card has three primary deliverables. When writing the DG context layer on a gene-brief, use the pain-point type to weight which evidence-code challenges and open questions to foreground, and to write the opening framing paragraph and callout.

## conflict_summary — ClinVar discrepancy report

**What it delivers:** Conflicting ClinVar submissions for this gene that are likely resolvable with evidence already in the literature. Identifies which submissions conflict with the panel's calls and what evidence would resolve each discrepancy.

**Framing paragraph hook:** "... accompanies the ClinVar discrepancy report for [GENE] ..."

**Weight in evidence-code challenges:** Foreground codes where inter-lab disagreement is documented: PP3/BP4 (predictor threshold differences), PM2 (MAF threshold differences), PS3 (assay scope disagreements). Lead with the code where the most ClinVar conflicts originate.

**Weight in open questions:** Lead with the question about which submitters have active conflicts and what evidence resolves them.

**Pain-point callout template:**
> **This report addresses:** [number] conflicting submissions for [GENE] in ClinVar, including [brief description of the most common conflict type, e.g., "PP3-driven likely pathogenic vs. VUS for REVEL 0.5–0.7 variants"]. The discrepancy analysis is in Section [N] of the accompanying report.

## reclassification_candidates — Reclassification candidates report

**What it delivers:** Variants currently designated VUS or likely pathogenic/likely benign in ClinVar where existing evidence (functional data, case counts, computational scores) may support an upgrade or downgrade.

**Framing paragraph hook:** "... accompanies the reclassification candidates report for [GENE] ..."

**Weight in evidence-code challenges:** Foreground PS3/BS3 (functional assay availability and thresholds), PP3/BP4 (predictor score cutoffs), and any code where the MAVE dataset or published functional studies provide evidence that ClinVar submitters have not yet applied.

**Weight in open questions:** Lead with the question about the intermediate-zone variants — those where functional data exist but classification rules do not yet cover the result cleanly.

**Pain-point callout template:**
> **This report addresses:** [number] variants in [GENE] with available functional or literature evidence that may support reclassification. The candidates are ranked by evidence completeness in Section [N] of the accompanying report.

## vus_triage — VUS triage queue

**What it delivers:** All current VUS for this gene in ClinVar, ranked by evidence completeness — which ones are closest to reclassification and where to focus curator effort first.

**Framing paragraph hook:** "... accompanies the VUS triage queue for [GENE] ..."

**Weight in evidence-code challenges:** Foreground the codes where VUS burden is highest: typically the codes that are hardest to apply (PM1 if undefined, PS3 if assay data are sparse, PP3 in the neutral REVEL zone). Also foreground any code where new data (a MAVE dataset, a large case series) could reclassify a batch of VUS at once.

**Weight in open questions:** Lead with the question about the largest unresolved VUS category — the variant class that is structurally hardest to classify with current evidence.

**Pain-point callout template:**
> **This report addresses:** the [number] VUS currently in ClinVar for [GENE], ranked by evidence completeness. The triage queue is in Section [N] of the accompanying report, with the top [number] candidates flagged for immediate curator attention.
