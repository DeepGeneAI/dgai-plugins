---
name: outreach-email
description: Draft a single research-rooted outreach email by starting from the recipient and matching one of a project-defined set of offers to their current situation. Trigger this skill whenever the user wants to write a one-off cold or warm outreach email (not a podcast guest brief or mass campaign), produce a per-recipient email rather than fill slots in a generic template, or pick which offer from a project catalog fits a specific recipient. The skill is research-first — it identifies who the recipient is, what they're working on now, and which offer fits — and produces a draft plus a research trace showing which fact backed which line. Project-specific content (recipient research procedure, offer catalog, brand voice) lives in `context/` and in companion skills, so the same logic works across different outreach contexts.
---

# Outreach Email

## What this skill does

Produces a per-recipient outreach email by researching the recipient first, not by filling slots in a generic template. The output is one email tailored to one person, with notes showing which fact backed which line.

This is the logic-only skill. It defines what a research-rooted outreach email *is*: research the recipient → match an offer from a catalog → draft using a gift-giving posture → return draft plus research trace. The catalog, the recipient research procedure, and any walkthroughs live in `context/`. Brand voice (the way the final draft should *sound*) belongs to a separate revision skill — see "Voice pass" below.

Generic context files in this skill:

- `context/recipient-research.md` — research procedure for a VCEP/ClinGen recipient
- `context/fallbacks.md` — routing table for when this skill is not the right path
- `context/sender-voice-map.md` — sender → voice skill mapping

Project-specific context (offer catalog, stage-offer-mapping, audience framing) is provided by the project context layer. For DeepGene/VCEP outreach, use the `dgai-outreach` skill which pre-loads that context.

## When to use this skill versus another path

Use this skill when:

- Writing a one-off cold or warm outreach email where research is worth doing
- The recipient is on a list where personalization matters
- You have at least 10 minutes to research the recipient before drafting

Use project templates (outside this skill) instead when:

- The relationship is warm enough that recipient research adds little value
- Running a high-volume A/B test where per-recipient research is not feasible
- The goal is preparing for an interview brief, not sending outreach

Those alternates are project-owned assets listed in `context/fallbacks.md`. Keep this skill focused on research-rooted one-off outreach.

## Inputs needed before starting

Confirm before proceeding:

- Recipient's full name and current organization
- Sender (affects voice and signature; project context defines who this can be)
- Whether a warm-intro source exists (a name to drop in the opener)
- Confirmed email address, or that finding one is part of the task

If any are missing, ask. Do not guess on sender or warm-intro source.

## Procedure

### 1. Research the recipient

Follow the procedure in `context/recipient-research.md`. The outputs that procedure produces — person background, committees, stage, gene in focus — are the inputs to step 2. If that file says "do not send via this skill," route using `context/fallbacks.md` and stop here.

### 2. Match the offer

Use the project offer catalog (provided by the project context layer) to decide:

- **How many offers to surface.** First touch with weak stage signal → surface a subset and let the recipient pick. First touch with strong stage signal, or second touch → pick one.
- **Which specific offer(s).** The catalog has a recipient-situation column. The stage-offer-mapping file has a complementary lookup if you can pin the recipient's gene-stage precisely. If both fail to give a single best-fit, fall back to the catalog's default subset.

Lift the offer language directly from the source fact sheet (or use the compressed sent versions in the catalog). Do not paraphrase it into something fuzzier; the specificity of the wording is what makes the offer credible.

If no offer fits, that is itself a signal. See "When no offer fits" in the offer catalog.

### 3. Draft the email

The posture is **gift-giving, not pitching.** You are offering something for the recipient to take or leave. The structure below is the shape; the sentence-level voice is layered in by the voice-revision skill (see step 4).

#### Structure (first-touch, multi-offer version)

- **Subject:** descriptive, plain, names the gene or panel. No punchiness, no em dashes.
- **Greeting:** `Hi [first name],` — single line.
- **Setup line:** one sentence introducing who you are if first contact, OR thanking them for prior context if mid-thread. Short.
- **No-pressure frame:** one sentence with explicit no-strings framing.
- **Hedged ask:** name the gene, then ask which of the offers (if any) would help. The "if any" hedge does real work — it lets the recipient decline without it being a "no."
- **Offers as a bullet list**, each with bolded name + one-line description. Use the compressed versions from the offer catalog.
- **Soft close:** explicit permission to decline, modify, or take any subset. Recipient sets cadence.
- **Sign-off:** plain. `Best,\n[Sender]`.

**Length target:** ~95 words including the bullets, for the canonical first-touch shape. Don't pad and don't cut for the sake of cutting.

#### Structure (second-touch, single-offer variant)

If you've reached the point where one offer is the right one (per the stage→offer mapping or the recipient's reply), the structure compresses but the posture stays the same:

- Same plain subject and greeting
- Setup line referencing prior thread
- One offer, lifted from the fact sheet
- Same soft close

The temptation in second-touch is to add urgency or close harder. Resist it. The gift-giving frame holds.

#### Structure (cold outreach, no prior relationship or warm intro)

When there is no warm intro source and no prior contact, compress to the Ferriss shape:

- **Subject:** specific — names the gene, panel, or exact issue. Nothing clever.
- One sentence on who you are.
- One sentence showing specific homework: a named variant, a recent ClinVar deposit, a paper they authored. Not "your fascinating work" — a fact.
- One small, frictionless ask. The Ferriss principle: make it so small it's almost rude to decline. Two options — (a) a one-sentence answerable question ("do you think a ClinVar discrepancy report would be useful for your OTC work?"), or (b) a specific time with a built-in out ("15 minutes Thursday — or a one-line reply with a better time"). Never "could we talk sometime."
- Plain sign-off.

**Length target:** 3–5 sentences. No bullet list. No no-pressure frame needed — the brevity does that work.

Use the full first-touch structure (above) when a warm intro exists or the relationship is warm enough to warrant more context. Default to the Ferriss shape when genuinely cold.

### 4. Voice pass

Pass the draft through the brand-voice revision skill that matches the sender. The sender-to-skill mapping lives in the project context layer — check `context/sender-voice-map.md` for the relevant voice skill path. The voice skill applies sender-specific patterns (which anti-ai-ese phrases are allowed in this voice, which sentence shapes are signature, and which closes are off-limits even though they sound polite).

Do not bake voice rules into this skill. A draft produced here should be structurally correct for any sender; the voice skill makes it sound like the specific person.

### 5. Anti-ai-ese pass

**MUST.** Do not return a draft without completing this step. Load `style-guide.md` from the root of this repo and apply every rule in it to the draft. The voice skill will have explicitly carved out exceptions for its sender; everything else in the style guide still applies.

Common failures in outreach drafts:

- Em dashes for mid-sentence emphasis
- Three-word staccato sentences
- "It's not X, it's Y" patterns
- Generic praise ("your fascinating work")
- Banned words: leverage, robust, comprehensive, delve, meticulous

## Output format

Return the email plus a short research trace. The trace's exact fields come from the recipient-research procedure — see the "Research trace template" section in `context/recipient-research.md`. The general shape is:

```
SUBJECT: [subject line]

[email body]

---
RESEARCH TRACE
[fields from the research procedure, each with source]
- Offer chosen: [line from source fact sheet]
- Why this offer: [one sentence — cite catalog row or stage-mapping row]
- Voice pass: [skill applied]
```

The trace exists so the sender can audit any single line. If a fact came from a guess, mark it `[unverified]` rather than dropping it silently.

## Iteration loop

After each email, capture what worked or did not. Updates that are project-specific (a new gene-stage row, a corrected committee source, a recipient who didn't fit any offer) belong in the relevant `context/` file in the project context layer. Updates that are about the *shape* of an outreach email (a new structural variant, a sequencing rule, a missing-data fallback) belong in this SKILL.md.

The split exists so the same logic can be reused for a different project by swapping the project context layer and the voice skill. Resist the pull to bake project content back into the skill itself.
