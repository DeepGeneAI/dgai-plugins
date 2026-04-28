---
description: "Research a single VCEP/ClinGen outreach target and produce a per-recipient email rooted in their specific committees, current stage, and gene in focus. Trigger this skill whenever the user wants to write a one-off cold or warm outreach email to a coordinator, chair, or curator (not a podcast guest brief), pick which Qorus Gene Report offer from docs/gene-report-fact-sheet.md fits a specific recipient, or research a target person before drafting. The skill starts from the person, not from a template: it identifies which committees they chair, what stage each panel is at, which gene the panel is currently working on, and matches one of the four Gene Report deliverables (Conflict & Discrepancy Summary, Reclassification Candidates, VUS Triage Queue, or Per-Paper Evidence Summaries) to the recipient's situation. Companion to anti-ai-ese (style) and guest_brief_generator.py (podcast guest research)."
---

# Outreach Research

## What this skill does

Produces a per-recipient outreach email by researching the recipient first, not by filling slots in a generic template. The output is one email tailored to one person, with notes showing which fact backed which line. The two biggest decisions the skill makes are: (1) which Qorus Gene Report offers from `docs/gene-report-fact-sheet.md` to surface (one or three, depending on stage signal), and (2) whether the recipient is a fit for the gene-report path at all. Amanda's reply to Bryce showed that the answer to the first question is different per gene, which is why first-touch surfaces three offers and lets the recipient pick.

This replaces the template-pick approach in `the-curation-table/outreach/coordinator_outreach_email.md` for any recipient where research is worth doing.

## When to use this skill versus another path

Use this skill when:

- Writing a one-off cold or warm outreach email to a VCEP coordinator, chair, or curator
- You have at least 10 minutes to research the recipient before drafting
- The recipient is on the wave-1 list or any later list where personalization matters

Use the existing templates instead when:

- Sending to a Tier 1 warm contact where the relationship carries the email (use `the-curation-table/outreach/warm_contact_outreach_email.md`)
- Running a high-volume A/B test where per-recipient research is not feasible (use `the-curation-table/outreach/coordinator_outreach_email.md`)

Use `guest_brief_generator.py` instead when:

- The goal is preparing for a podcast interview, not sending an email
- You need a full publication history and recent ClinVar work, not a single offer

## Inputs needed before starting

Confirm before proceeding:

- Recipient's full name and current organization
- Sender (Abby or Bryce; affects voice and signature)
- Whether a warm-intro source exists (a name to drop in the opener)
- Confirmed email address, or that finding one is part of the task

If any are missing, ask. Do not guess on sender or warm-intro source.

## Procedure

### 1. Person background

Run the existing brief generator to populate publications and current affiliation:

```bash
python3 the-curation-table/tools/guest_brief_generator.py "First Last" "ClinGen"
```

Output lands in `the-curation-table/output/raw/`. From it, extract:

- Current title and institution (ORCID employments)
- Three to five recent publications relevant to variant curation
- Whether the recipient has a meaningful PubMed presence at all (low count is a real signal)

If ORCID returns nothing, do not block. Note it and proceed. Some curators publish under varying name forms or not at all.

### 2. Committees they chair or co-chair

The brief generator does not extract committee roles cleanly. For now, this is a manual lookup against:

- ClinGen affiliate directory: https://clinicalgenome.org/curation-activities/variant-pathogenicity/expert-panels/
- The recipient's institutional bio or LinkedIn
- Committee notes in `docs/gene-report-fact-sheet.md` if Bryce has logged them there

Capture each VCEP with the role explicit. A chair line lands differently than a member line. A coordinator across five panels lands differently than a chair of one. Be precise.

A future `committee_research.py` script will automate this step. Until then, do the lookup by hand.

### 3. Stage of each committee

For each VCEP from step 2, identify the stage:

- **Active curation**: submitting variants now, recent ClinVar activity from the panel
- **Protocol development**: published rules, not curating at volume yet
- **Recruiting**: early formation, building the panel
- **Dormant**: published rules but ClinVar activity has stopped
- **Unknown**: cannot tell from public sources

Stage shapes which offer fits. A panel in active curation has different needs than one in protocol development. Capture stage even when the answer is "unknown."

### 4. Gene in focus

Within the panel, which gene is the recipient currently working on? This is the per-gene angle Amanda's reply turned on. Sources, in order of preference:

1. Direct knowledge from a prior conversation (if Amanda said OTC, that is the answer)
2. The recipient's most recent first-author or senior-author paper if it names a single gene
3. A recent ClinVar submission cluster for the panel

If no single gene is identifiable, name the panel's gene set and note the gene in focus as unknown. Step 5 will fall back to a panel-level offer.

### 5. Match the offer

The Qorus Gene Report (`docs/gene-report-fact-sheet.md`) ships four named deliverables. The skill's job here is to know which subset to surface to the recipient, but the *number* you surface depends on what you know about them.

**First touch where you can't pin panel-stage and gene-stage precisely.** Surface a subset of offers and let the recipient pick. This matches Bryce's actual sent voice (see the Amanda thread, Apr 21–23, 2026, and the Ljubica/Nicholas email). His three-offer ask to Amanda earned a per-gene reply that is the source of the soft mapping below — i.e., listing options is a *data-collection move*, not a hedge.

The default subset is the three Bryce surfaced: **ClinVar discrepancy report**, **Reclassification candidates**, **VUS triage queue**. **Per-Paper Evidence Summaries** is typically held back on first contact because it's the heaviest deliverable and can read as overpromising. This is a soft default, not a rule — surface Per-Paper if the recipient's situation specifically calls for it (e.g., they've said literature review is the bottleneck, or their panel's gene has a known evidence-extraction problem the other three offers don't address).

**Second touch, or first touch with strong stage signal.** Pick one. The choice becomes the work; the wrong one wastes the recipient's attention. Use the soft mapping below to choose.

Either way, lift the offer language directly from the fact sheet (or use Bryce's compressed sent versions in Step 6). The specificity of the wording is what makes the offer credible.

**Offer catalog**

| Offer | Best fit when the recipient... |
|---|---|
| **Conflict & Discrepancy Summary** | Chairs an active-curation panel where ClinVar shows their Expert Panel record disagreeing with other submitters, or where multi-submitter disagreements are common in the gene |
| **Reclassification Candidates** | Sits on a panel with curated variants near classification thresholds, especially recessive disease genes where compound-het evidence accumulates across papers |
| **VUS Triage Queue** | Has a backlog of VUS in their gene and limited bandwidth to decide which to look at first; this is the "variant spectrum / where do I start" answer |
| **Per-Paper Evidence Summaries** | Tells you literature review is the bottleneck, especially for functional, segregation, or phenotype-specificity evidence |

Lift the offer language directly from the fact sheet. Do not paraphrase it into something fuzzier; the specificity of the fact-sheet wording is what makes the offer credible.

If no offer in the catalog fits, treat it as a real signal:

- Either the fact sheet needs a new line (flag for Bryce)
- Or this recipient is not a fit for the gene-report path right now (consider a different CTA from `coordinator_outreach_email.md`)

#### Stage → offer soft mapping (Amanda Thomas-Wilson reply, 2026-04-23)

This is a starting hypothesis, not a hard rule. It comes from a single signal: Amanda's per-gene response to Bryce's three-offer ask, where she gave granular feedback on which offer fit which gene at which stage of UCD VCEP work. Treat it as a draft heuristic until at least three more replies confirm or revise it. Update the table inline as new data comes in.

| Recipient's stage on the gene in focus | Most likely best offer | Signal from Amanda's reply |
|---|---|---|
| Pilot variant list complete, specs near final, next gene already queued | Conflict & Discrepancy Summary | "ClinVar discrepancy report would be really helpful for our next gene." |
| Specs early or in heated debate (e.g., the CPS1 case) | None yet, hold or send a panel-level note | Amanda flagged CPS1 as too early for a specific offer. Don't force one. |
| Building a pilot variant list from scratch | Reclassification Candidates | "Could also be very helpful in developing an ASS1 pilot variant list." High-evidence VUS / LB / LP candidates are good pilot targets. |
| Step 4 approved, actively depositing variants into ClinVar | Reclassification Candidates | "Every variant you deposit as a VUS, Likely Pathogenic, or Likely Benign has to be re-curated every two years." Surfacing variants with new evidence speeds the cycle. |
| Step 4, easy LOF variants done, VUS or conflicting backlog forming | All three of (VUS Triage Queue, Conflict & Discrepancy Summary, Reclassification Candidates), ranked best-fit-first | Amanda on OTC: "having VUS or conflicting variants triaged and prioritized would make this quite a bit faster." |

Source: forwarded thread from Bryce, Apr 23 2026, subject "Re: amaze amaze amaze."

How to use this table: if you can pin the recipient's gene-stage precisely (from a paper, a recent ClinVar deposit pattern, a public VCEP status note, or a prior email), look up the row and use it as your prior. If the gene-stage is not pinnable, fall back to the offer catalog above. Either way, log which path you used in the research trace so we can tell later whether the stage-mapping reads land better than the situation-mapping reads.

### 6. Draft the email

The posture is **gift-giving, not pitching.** You are offering something for the recipient to take or leave. Bryce's sent voice across the Amanda thread (Apr 21–23, 2026) and the Ljubica/Nicholas email is the model.

#### Structure (first-touch, three-offer version)

- **Subject:** descriptive, plain, names the gene or panel. No punchiness, no em dashes. Examples from sent threads: `amaze amaze amaze` (where the relationship allowed informality), or for cold-warm contacts something like `DDC support, no strings`.
- **Greeting:** `Hi [first name],` — single line.
- **Setup line:** one sentence introducing who you are if first contact, OR thanking them for prior context if mid-thread. Short. *"I'm building tooling for VCEP curation,"* or *"Thank you again for the conversation."*
- **No-pressure frame:** one sentence with explicit no-strings framing. Bryce's reusable phrase: *"I'd like to offer something to you and your team, no strings attached, no expectations."*
- **Hedged ask:** name the gene, then ask which of the offers (if any) would help. Bryce's pattern: *"For [gene], what would be most valuable at your current stage?"* The "if any" hedge does real work — it lets the recipient decline without it being a "no."
- **Three offers as a bullet list**, each with bolded name + one-line description. Use Bryce's compressed sent versions:
  - **ClinVar discrepancy report**: conflicting submissions that are likely resolvable with evidence already in the literature
  - **Reclassification candidates**: variants where existing evidence may support a classification update
  - **VUS triage queue**: ranked by evidence completeness so you know where to focus first
- **Soft close (verbatim):** *"Happy to put together whichever would be most useful, or all three if that's helpful. Just let me know."* Three layers of permission to decline or modify, baked in.
- **Sign-off:** `Best,\nBryce` or `Best,\nAbby` — plain.

**Length target:** Bryce's offer email runs ~95 words including the bullets. Don't pad and don't cut for the sake of cutting.

#### Voice patterns to keep

- Short paragraphs, often one sentence.
- Parenthetical asides for the specific observation. The polite frame goes in the main clause; the substance goes in parens. *"Wow! Super impressive amount of work your committee has done (looks like you've carried a lot yourself)."*
- *"Would love to..."* and *"Happy to..."* are kept. Both appear in his sent voice and serve the gift-giving frame. They are not banned in this skill despite the parent anti-ai-ese skill flagging them.
- *"If any"* hedges baked into asks. *"Which, if any, of the following would be valuable?"*
- No assumptive time anchors. Don't propose a slot. Recipient sets cadence via *"Just let me know."*
- Recipient's vocabulary, untranslated. NAGS, CPS1, VCEP, SVI, step 4 — use the shorthand they use.
- Honest naming of confusion when it happens. *"Strange, I selected inborn errors of metabolism but the survey indicates no groups are seeking variant curators."* Don't paper over puzzles.

#### Voice patterns to avoid

- Em dashes for emphasis or aside.
- Three-word staccato sentences.
- "It's not X, it's Y" / "Not because X, but because Y" patterns.
- Generic praise (*"fascinating work,"* *"incredible research"*). Specific praise with parenthetical anchors is fine.
- Banned words from `.claude/skills/anti-ai-ese/SKILL.md`: leverage, robust, comprehensive, delve, meticulous, pivotal, etc.
- Assumptive time anchors (*"20 minutes Tuesday?"*). Recipient picks the slot.
- Sales-pitch closers (*"Looking forward to hearing from you,"* *"Would love to discuss further"*). Bryce's close is *"Just let me know."*

#### Second-touch / single-offer variant

If you've reached the point where one offer is the right one (per the stage→offer mapping or the recipient's reply), the structure compresses but the posture stays the same:

- Same plain subject and greeting
- Setup line referencing prior thread
- One offer, lifted from the fact sheet
- Same soft close (*"Happy to put it together if it'd help. Just let me know."*)

The temptation in second-touch is to add urgency or close harder. Resist it. The gift-giving frame holds.

### 7. Anti-ai-ese pass

Before returning the draft, run it through `.claude/skills/anti-ai-ese/SKILL.md`. Common failures in outreach drafts:

- Em dashes for mid-sentence emphasis
- Three-word staccato sentences
- "It's not X, it's Y" patterns
- Generic praise ("your fascinating work")
- Banned words: leverage, robust, comprehensive, delve, meticulous

**Skill-specific exceptions to the parent anti-ai-ese rules.** The parent skill bans *"happy to"* and *"would love to"* as filler. For outreach written in Bryce's voice, these phrases are kept — they appear repeatedly in his sent emails and serve the gift-giving frame (see Step 6). Do not flag them in this context.

## Output format

Return the email plus a short research trace:

```
SUBJECT: [subject line]

[email body]

---
RESEARCH TRACE
- Person: [title, institution] (source)
- Committees: [VCEPs with roles] (source)
- Stage: [stage per panel]
- Gene in focus: [gene] (source)
- Offer chosen: [line from factsheet]
- Why this offer: [one sentence]
```

The trace exists so Bryce can audit any single line. If a fact came from a guess, mark it `[unverified]` rather than dropping it silently.

## Walkthrough (sourced from the Amanda thread, Apr 21–23, 2026)

Recipient: Amanda Thomas-Wilson, NYGC. The actual sent email is reproduced here as the canonical voice example for first-touch, three-offer drafts.

1. **Person background**: existing collaborator; UCD VCEP chair; recent papers on urea cycle variant interpretation. Bryce's first message in the thread (Apr 21, 4:09 PM) is a reaction to seeing her curation work — short, specific, with parenthetical observation: *"Wow! Super impressive amount of work your committee has done (looks like you've carried a lot yourself)."*
2. **Committees**: chair, UCD VCEP.
3. **Stage**: active curation; "step 4 approved and depositing variants into ClinVar," per Amanda's own description on Apr 23.
4. **Gene in focus**: CPS1 at the time of the offer email (NAGS specs being wrapped up). Source: Amanda's reply, Apr 21, *"moving on to CPS1."*
5. **Offers surfaced**: three of four — Per-Paper Evidence Summaries held back. Stage signal hadn't yet been pinned to a single offer.
6. **Sent email** (Bryce, Apr 23, 2026, 7:28 AM, in reply to Amanda):

   > Sounds good, thanks!
   >
   > For your work on CPS1, which, if any, of the following would be valuable?
   >
   > - **ClinVar discrepancy report**: conflicting submissions that are likely resolvable with evidence already in the literature
   > - **Reclassification candidates**: variants where existing evidence may support a classification update
   > - **VUS triage queue**: ranked by evidence completeness so you know where to focus first
   >
   > Happy to put together whichever would be most useful, or all three if that's helpful. Just let me know.

7. **Reply outcome**: Amanda gave per-gene granular feedback (CPS1 too early, ASS1 needs Reclassification Candidates, OTC needs all three triaged). That reply is what generated the soft mapping in Step 5.
8. **Anti-ai-ese pass**: clean. Note that *"happy to"* appears and is kept (see Step 7 exception).

## What to do when data is missing

- **No ORCID, sparse PubMed**: skip publication references in the opener; lead with the panel instead
- **Cannot identify any committee**: do not send via this skill. The skill assumes committee membership is knowable. Switch to the coordinator template.
- **Stage is unknown**: pick the offer that is panel-stage-agnostic, not the one that requires "active curation."
- **No gene in focus**: write a panel-level email, not a gene-level email. Mark the trace.
- **No offer in fact sheet fits**: flag for Bryce. Do not invent one.

## Iteration loop

After each email, capture what worked or did not into this skill, not into the individual email file. Examples of skill-level updates:

- "Step 2 missed that Sarah Elsea co-chairs three panels; added LinkedIn as a fallback source"
- "The 80-word target ran long for chairs; cut to 60"
- "Recipients with no PubMed presence replied at a higher rate than expected; note in step 1"

Wave-1 lessons feed wave-2 directly. The point of putting them here is so wave-2 starts smarter than wave-1 did.
