---
name: anti-ai-ese
description: Enforces The Curation Table's anti-AI-ese writing style on any content written for DeepGene or The Curation Table. Trigger this skill whenever writing or editing outreach emails, guest briefs, gene primers, cold emails, social posts, newsletters, or any document that will go out under a human name. Also trigger when the user asks Claude to review text for AI-generated writing patterns, check for "AI-ese," make a draft sound more human, or remove words like "delve" or "leverage." The skill specifies banned words, banned phrases, banned sentence patterns (em dashes for emphasis, "it's not X, it's Y," three-word staccato lists), and structural rules so the final output reads like a specific human wrote it rather than a language model.
---

# Anti-AI-ese

## What this skill does

Constrains Claude's writing to match the voice expected for The Curation Table podcast and DeepGene operations. The goal is not to hide that AI assisted in drafting. The goal is that the final text reads like the specific person whose name is on it actually wrote and owns it.

Apply every rule below to any draft before returning it to the user. When the user asks you to review someone else's text for AI-ese, flag violations with the specific rule they break rather than silently rewriting.

The full style rules are in `style-guide.md` at the root of this repo. The sections below are the enforcement checklist; the style guide has the reasoning and positive examples.

## The single biggest tell: em dashes

Em dashes used for punchy mid-sentence emphasis are the clearest single marker of AI-generated prose. Never use them. If a sentence needs a pause or aside, reach for a comma, period, parentheses, or rewrite it.

Wrong: "Qorus is a platform we built — and it works."
Right: "Qorus is a platform we built, and it works."

## Banned words

The worst offenders: delve, robust, tapestry, landscape, pivotal, paramount, meticulous, nuanced, cutting-edge, comprehensive, leverage, utilize, foster, enhance, harness, elevate, underscore, illuminate, realm, cornerstone, testament.

Also avoid: arena, arsenal, captivate, catapult, craft, crafting, crucial, deep dive, dive, embark, engage, engaging, fast-paced, formidable, game changer, groundbreaking, holistic, impactful, innovative, intricate, nimble, navigate (as metaphor), revolutionize, seamless, skyrocket, stellar, supercharge, tailor, tailored, trailblazer, turbocharge, uncover, unleash, unlock, unveil, vibrant.

## Banned sentence patterns

- "It's not about X, it's about Y."
- "It's not just X. It's Y."
- "That's not X, that's Y."
- "Not because X. But because Y."
- "No X. No Y. Just Z."
- Three-word staccato sentences: "Focused. Aligned. Measurable."
- "And the X? Y." / "The result? [Statement.]"

## Banned filler transitions

moreover, furthermore, additionally, that being said, it's worth noting, it's important to note, needless to say, in other words, as mentioned earlier, to summarize, in conclusion, overall.

## Hollow intensifiers — cut on sight

deeply, fundamentally, remarkably, truly, incredibly, essentially, absolutely, certainly, clearly, obviously, arguably.

Vague phrases: "at its core," "at the end of the day," "on a deeper level," "in many ways."

## No unearned praise

"Your work is truly inspiring" gets emails deleted. Specific facts are credible. Generic adjectives are not.

## Structural rules

- Vary sentence length. Uniform rhythm is an AI fingerprint.
- Prefer prose over bullet lists.
- Avoid the "**bolded mini-header:** explanation" bullet format.
- One tricolon per document maximum.

## Context-specific rules

**Outreach emails.** Every sentence must be specific to this recipient. If a line could have been sent to anyone in the field, cut it.

**Outreach phrasing exceptions.** `"I'd love to..."`, `"Would love to..."`, and `"Happy to..."` are allowed as low-pressure offers (gift-giving posture). Not allowed as sales-pitch closers.

**Guest briefs.** Name the specific contribution, not the status. "Heidi Rehm led the team that published the 2015 ACMG/AMP standards" — not "Heidi is a leading expert."

**Gene primers.** Skip the preamble about genetics being complicated. Go straight to the substance.

## Enforcement checklist

Run this before returning any draft:

1. Scan for banned words. Replace each with the concrete specific.
2. Scan for em dashes. Replace with commas, periods, or a rewrite.
3. Scan for banned sentence patterns. Rewrite any that appear.
4. Check sentence length variation. Break up uniform rhythm.
5. Count tricolons. Cut down to one if there are more.
6. Check the opener and closer against the banned lists.

## Reviewing someone else's draft

Don't silently rewrite. Return:
- A list of specific violations, each tagged with the rule they break.
- A proposed fix for each one.
- A note if zero violations found.

## Reference

Full style rules with reasoning and examples: `style-guide.md` at the root of this repo.
