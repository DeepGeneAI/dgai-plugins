---
name: dgai-gene-brief
description: DeepGene context layer on top of the gene-brief skill. Produces the cover document that ships with each Gene Report Card. Takes a gene, a panel, and a pain-point type (conflicts, reclassification, or vus) and returns a gene-brief with a DeepGene framing section that ties the open questions and evidence-code challenges directly to the specific report deliverable being sent. Use this skill when producing a cover doc for a delivered Gene Report. Use the generic gene-brief skill when producing a standalone research briefing without a specific Gene Report context.
---

# DeepGene Gene Brief (DG layer)

## What this skill does

This is the DeepGene context layer on top of `skills/gene-brief/SKILL.md`. It adds one input and two output modifications:

**Additional input:** `pain_point` — one of `conflict_summary`, `reclassification_candidates`, or `vus_triage`. These match the `requested_reports` enum in `intake/schema.yaml`. If the user provides the pain point (or you have the intake record), use it. If not, infer it from the open questions and evidence-code challenges section of the gene-brief output: whichever section has the highest density of unresolved issues is the most defensible pain point to lead with.

**Output modification 1 — Opening framing paragraph.** Before the disease overview, add a one-paragraph framing statement that ties the brief to the delivered report. The paragraph identifies the panel by name, names the specific Gene Report deliverable, and states in one sentence what the brief covers. It should read like a cover letter paragraph — direct and specific, not promotional.

Template:
> This brief accompanies the [deliverable type] Gene Report for [GENE] prepared for the [Panel name]. It covers the disease biology, current VCEP protocol, the evidence-code areas most relevant to the reported findings, and the open questions the report is designed to address. Prepared by DeepGene, [date].

Adjust the wording to fit the deliverable type:
- `conflict_summary`: "the ClinVar discrepancy report for [GENE]"
- `reclassification_candidates`: "the reclassification candidates report for [GENE]"
- `vus_triage`: "the VUS triage queue for [GENE]"

**Output modification 2 — Pain-point callout in open questions.** In the open questions section, add a brief callout — one to two sentences — connecting the first open question to the specific deliverable. The callout is introduced with "**This report addresses:**" and names the specific finding or analysis from the Gene Report that bears on that question.

Leave the rest of the gene-brief output unchanged. Do not add marketing language, product references, or calls to action. The cover doc is a scientific document, not a sales document.

## Procedure

1. Load all context files from `skills/gene-brief/` in the gene-brief plugin.
2. Load `context/pain-point-framing.md` from this skill directory.
3. Run the full `gene-brief` procedure for the target gene and panel. Pass the `pain_point` as the pain point hint so the gene-brief's evidence-code challenges and open questions sections are weighted appropriately.
4. Prepend the opening framing paragraph.
5. In the open questions section, add the pain-point callout after the first open question.
6. Apply `style-guide.md` to the framing paragraph and callout. The gene-brief body is already styled; do not re-process it.
7. Return the complete document.

## What not to add

- Do not add a Qorus description, platform pitch, or discovery call CTA. The cover doc ships with the report; the recipient has already agreed to receive it. It is not a sales email.
- Do not add a "next steps" section. If Bryce wants a follow-up hook, it goes in the follow-up email (the `dgai-followup` skill), not in the cover doc.
- Do not change the gene-brief's citation discipline. Every added sentence needs a footnote if it makes a factual claim.
