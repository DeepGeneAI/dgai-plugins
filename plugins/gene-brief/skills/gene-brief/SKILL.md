---
name: gene-brief
description: Produce a practitioner-level cover document for a gene being reviewed or reported on. The brief covers disease biology, VCEP protocol status, evidence-code challenges specific to this gene, classification-relevant literature, and open questions. It is deeper than a vcep-research briefing (which covers panel metadata and recent ClinVar activity) and is intended to ship as the cover document of a Gene Report, or to prepare for a call with a panel coordinator or chair. Generic logic only — no DeepGene framing. The DG context layer lives in the dgai-gene-brief skill.
---

# Gene Brief

## What this skill produces

A practitioner-level document — roughly two to three pages of Markdown — that a clinical geneticist or VCEP coordinator can read before a call or alongside a delivered report. It assumes the reader knows what variant classification is; it does not explain ACMG/AMP from scratch.

The five sections are:

1. **Disease overview** — clinical presentation spectrum, inheritance, key biochemistry or molecular mechanism, population frequency. Sourced from GeneReviews and OMIM.
2. **VCEP protocol status** — what the panel has published or approved, which CSpec version is current, and which evidence codes have gene-specific modifications.
3. **Evidence-code challenges** — where the standard codes need calibration for this gene: which codes are underspecified, which have functional data available, which are contested among panels. This is the analytically rich section.
4. **Classification-relevant literature** — five to seven recent papers bearing on variant classification for this gene. Preferentially functional studies, allele frequency analyses, and VCEP-specific publications over disease management papers.
5. **Open questions** — what remains unresolved: where VUS burden is highest, which code assignments are actively disputed, what the V4 Bayesian framework transition is likely to change.

## How this differs from vcep-research

The `vcep-research` skill produces a one-page panel briefing: who runs it, what stage it is at, recent ClinVar activity, and a short reference list. It answers "what is this panel and is it active?"

This skill answers "what does a curator actually need to know about classifying variants in this gene?" It is downstream of vcep-research, not a replacement for it. If you need both, run vcep-research first for panel metadata, then this skill for the scientific layer.

## Dependencies

- **GeneReviews** (NCBI Bookshelf) — disease overview and inheritance.
- **OMIM** — phenotype entry, allele frequency data where available. Use the API if `OMIM_API_KEY` is set; otherwise cite the OMIM entry page.
- **ClinGen/CSpec** — the panel's published criteria specification. Pull from `cspec.genome.network` for the current approved version.
- **ClinVar** — variant counts and classification breakdown. Use E-utilities or direct query.
- **PubMed** — literature search. Use `pubmed-database` skill if installed; otherwise use NCBI E-utilities with the recipes in `context/evidence-code-reference.md`.
- **gnomAD** — population frequency context where relevant to PM2/BA1 calibration.

## Inputs

- A gene symbol (e.g. `OTC`, `ASS1`, `FBN1`). If a panel name is given instead, resolve to the primary gene before starting.
- Optional: a specific CSpec version to target (defaults to the current approved version).
- Optional: a pain point hint (`conflicts`, `reclassification`, `vus`) that sharpens which open questions to foreground. If provided, weight the evidence-code challenges and open questions sections toward that framing. If absent, cover all three neutrally.

## Procedure

Run in order. Capture source URLs as you go — every claim needs a footnote.

**1. Resolve the gene and pull the CSpec.**
Look up the gene's ClinGen panel. Pull the current approved CSpec document from `cspec.genome.network`. Note the version, approval date, and which codes have gene-specific rule modifications. The CSpec is the authoritative source for sections 2 and 3.

**2. Write the disease overview.**
One to two paragraphs. Cover: inheritance pattern (X-linked, AR, AD, etc.), clinical presentation spectrum from severe to mild, key biochemical or molecular mechanism (what the protein does, what goes wrong in deficiency), and population frequency (incidence or prevalence from GeneReviews or OMIM). Do not pad this with historical context unless it directly bears on classification.

**3. Write the protocol status section.**
List the CSpec version and approval date. Then enumerate the gene-specific code modifications — the places where the panel has departed from or narrowed the generic ACMG/AMP rules. Use the taxonomy in `context/evidence-code-reference.md` to organize this. For each modified code, note the modification and its source in the CSpec. If the panel is still in development and has no approved CSpec, say so plainly and note which codes are most in need of specification based on the gene's variant landscape.

**4. Write the evidence-code challenges section.**
This is the most analytically demanding section. For each evidence code that poses a genuine classification challenge for this gene, write two to four sentences: what the standard rule says, why it is hard to apply here, what data sources exist that could resolve it, and what the panel has done (if anything). Focus on codes where classification outcomes differ across labs — these are the codes where curator effort is concentrated and where a Gene Report's functional or literature analysis adds the most value.

Reference the standard code categories in `context/evidence-code-reference.md` as a checklist. Not all codes will be challenging for every gene; only include a code if there is something specific to say about this gene. Four to six codes is a typical range. A section with eight codes is probably too long.

**5. Pull and filter literature.**
Search PubMed for: gene symbol + variant classification terms (variant interpretation, variant curation, pathogenicity, functional, MAVE, deep mutational scan, ACMG). Date range: last three to five years. Sort by relevance. Keep five to seven papers that bear directly on variant classification — functional studies, population analyses, VCEP-specific publications, MAVE datasets. Drop disease management and treatment papers unless they contain classification-relevant variant data. For each paper, write one sentence on why it matters for classification.

**6. Write open questions.**
List three to five unresolved issues that a curator or panel coordinator would immediately recognize as the live problems. Frame these as questions, not statements. Examples of good open questions:
- "How should PM2 be calibrated for the X-linked hemizygous case when gnomAD hemizygous counts are sparse?"
- "What REVEL or BayesDel threshold has the panel settled on for PP3/BP4, and is it consistent with the MAVE data?"
- "Which ClinVar submitters have conflicting expert-panel records for this gene, and what evidence resolves them?"

Bad open questions are generic ("How do we handle VUS?") or answered by the CSpec ("Is PVS1 applicable?" — check the spec). Open questions should name the specific unresolved tension.

## Output format

Follow `context/briefing-template.md`. Apply the repo `style-guide.md` to all prose before returning: no em-dash asides, no banned vocabulary, no tricolon padding. Every factual claim carries a footnote. Mark any field you could not fill as `unknown` rather than guessing.

## Citation discipline

Same standard as vcep-research: every factual line, a footnote. A claim without a source is a claim to cut or source. The References section at the bottom lists every footnote with its full URL.
