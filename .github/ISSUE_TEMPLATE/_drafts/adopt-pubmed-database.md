# Adopt: K-Dense PubMed-database skill as the research-briefing data layer

**Source:** https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/pubmed-database
**License:** MIT (repo-level; verify per-skill metadata in the skill's SKILL.md frontmatter)
**Verdict:** Adopt
**Scout entry:** SCOUTED.md, Reviewed Candidate 3

## Why this one

Sprint 3's `vcep-research` skill (T3.3) needs structured PubMed access. The current outreach plugin shells out to a homegrown `guest_brief_generator.py` for the same purpose. K-Dense's `pubmed-database` skill is a maintained, well-documented wrapper around the same NCBI E-utilities API with MeSH terms, Boolean operators, and field tags built in. Adopting it lets us delete custom code, gain sibling skills (OpenAlex, Crossref, Semantic Scholar, bioRxiv/medRxiv) for free, and inherit upstream maintenance.

Direct match for our stack — no DeepGene-specific customization required. Lowest-risk adoption in the T1.4 candidate pool.

## Installation plan

1. **Verify per-skill license.** Open the skill's SKILL.md frontmatter. The repo is MIT but K-Dense uses per-skill licensing. If anything other than MIT/Apache/BSD, escalate to Bryce before adopting.
2. **Add as a marketplace dependency.** Two options:
   - **Option A (preferred):** Add K-Dense as a second marketplace via `/plugin marketplace add K-Dense-AI/claude-scientific-skills`. Install only the `pubmed-database` skill; do not bulk-install the 128-skill collection. Pin the marketplace to a commit hash if possible.
   - **Option B (fork):** Fork the skill into `deepgene-plugins/plugins/pubmed-research/`. Use only if Option A's commit pinning isn't viable.
3. **Wire into `vcep-research`.** When T3.3 is built, the `vcep-research` skill calls `pubmed-database` for the literature-search step instead of the homegrown generator.
4. **Retire `guest_brief_generator.py`'s PubMed code path.** Leave the script for now (it covers ORCID too); strip the PubMed branch once `vcep-research` ships.

## Integration with logic/context separation

The PubMed skill is pure logic — no DeepGene context belongs in it. The DG-specific layer goes in:
- `vcep-research` skill: which queries to run for a VCEP coordinator (gene name + phenotype + curation keywords).
- `context/gene-report-fact-sheet.md`: the gene-specific knowledge that shapes which PubMed results matter.

This is exactly the split Bryce called for on 4/30 — generic skill, DG context layered on top.

## Acceptance criteria

- [ ] License verified at the per-skill level.
- [ ] Marketplace added or skill forked into `deepgene-plugins`.
- [ ] `pubmed-database` skill installable via `/plugin install`.
- [ ] Test query for "OTC variant pathogenicity" returns ≥10 valid PubMed records.
- [ ] `SCOUTED.md` updated with adoption date and any deviations from the install plan.
- [ ] If forked, fork rationale documented in `plugins/pubmed-research/README.md`.

## Risks and what we'll do about them

- **Per-skill license is non-permissive.** Mitigation: verify upfront; escalate if so.
- **K-Dense stops maintaining it.** Mitigation: pin to a commit hash. If repo goes dark for 6 months, fork.
- **NCBI E-utilities rate limits.** Mitigation: respect upstream rate-limit handling. If we need higher throughput, register an NCBI API key.

## Out of scope for this issue

- Adopting other K-Dense skills (OpenAlex, Crossref, etc.). Re-scout when Sprint 3 needs them.
- Writing the `vcep-research` skill itself. That's T3.3.
