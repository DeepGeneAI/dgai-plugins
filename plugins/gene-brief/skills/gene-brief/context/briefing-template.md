# Gene brief template

The `gene-brief` skill returns this structure. Fill every section from verified sources; mark anything unresolvable as `unknown`. Apply `style-guide.md` to all prose before returning.

```markdown
# Gene Brief: <GENE> — <Disease name>

**Panel:** <Panel name> (<VCEP|GCEP>) · **ClinGen:** <affiliation url>
**CSpec version:** <version> (approved <date>) · **Prepared:** <YYYY-MM-DD>
**Sources:** GeneReviews, OMIM, ClinGen/CSpec, ClinVar, PubMed<, gnomAD>

---

## Disease overview

<One to two paragraphs. Inheritance pattern. Clinical presentation spectrum — severe/neonatal to mild/adult-onset. Key biochemistry: what the gene encodes, what the deficiency disrupts. Population frequency from GeneReviews or OMIM. No padding.>

## VCEP protocol status

**CSpec version:** <version, approval date>[^1]

Gene-specific code modifications:

| Code | Standard rule | Panel modification | Source |
|------|--------------|-------------------|--------|
| <e.g. PS3/BS3> | <one line> | <one line> | [^1] |
| … | | | |

<If no approved CSpec exists, state which codes are most in need of specification and why.>

## Evidence-code challenges

<For each challenging code — typically 4–6 — write 2–4 sentences: what the standard rule says, why it is hard to apply for this gene, what data exist, what the panel has done or not done. Only include codes where there is something specific to say about this gene.>

**<Code (e.g. PS3/BS3) — Functional evidence>**
<Analysis. Source footnotes inline.>

**<Code (e.g. PM2) — Allele frequency>**
<Analysis.>

**<Code (e.g. PP3/BP4) — Computational predictors>**
<Analysis.>

… (continue for each relevant code)

## Classification-relevant literature

<Five to seven entries. For each: author, year, one sentence on why it matters for classification. Include PMID or DOI link.>

1. **<First Author et al., Year>** — <one sentence on classification relevance>.[^N]
2. …

## Open questions

<Three to five specific unresolved tensions a curator would immediately recognize. Framed as questions. Not generic ("how do we handle VUS?"); specific to this gene.>

1. <Question>[^N]
2. …

---

## References

[^1]: ClinGen/CSpec — <url>
[^2]: <source> — <url>
…
```

## Rules

- **No more than three pages.** If it runs longer, the evidence-code challenges section has too many entries or the prose is padded.
- **Every fact footnoted.** Same standard as vcep-research.
- **Only include a code if there's something specific to say about this gene.** The challenges section should not be a generic ACMG walkthrough.
- **Open questions must be specific.** If a question could apply to any gene, cut it.
- **Style guide applies.** No em-dash asides, no banned vocabulary, no tricolon padding.
