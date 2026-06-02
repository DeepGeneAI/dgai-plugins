# Anti-AI-ese Style Guide

This is a context document. Voice-bearing skills (outreach drafters, brief writers, content generators, anything that produces prose) load it at runtime and apply its rules to whatever they produce. Skills define the *what* to write; this guide defines the *how to sound human*. Project-specific or sender-specific overlays (brand voice, individual writing style, domain exceptions) live in adjacent context files and plug in alongside this guide, not inside it.

## Purpose

The goal is not to hide that AI helped draft something. The goal is that the final text reads like a specific accountable person wrote it, reviewed it, and stands behind it. Readers detect AI-ese fast, and when they do, trust drops before the content gets evaluated.

## The core principle

Specific beats generic. Every time you reach for an impressive-sounding word, a balanced-sounding tricolon, or a smooth-sounding transition, check whether you can replace it with the actual concrete thing instead. If you cannot, the sentence probably should not be there.

## The single biggest tell: em dashes

Em dashes used for punchy mid-sentence emphasis are the clearest single marker of AI-generated prose. Never use them. If a sentence needs a pause or aside, reach for a comma, period, parentheses, or rewrite it.

Wrong: "Qorus is a platform we built — and it works."
Right: "Qorus is a platform we built, and it works."

Paired em dashes around a parenthetical ("the 2015 standards — the ones Heidi Rehm led — changed everything") are still best avoided; use commas or parentheses instead.

## Banned words

These words have spiked sharply in AI-generated content since 2022. Do not use them, even once, unless quoting someone who actually used them.

The worst offenders: delve, robust, tapestry, landscape, pivotal, paramount, meticulous, nuanced, cutting-edge, comprehensive, leverage, utilize, foster, enhance, harness, elevate, underscore, illuminate, realm, cornerstone, testament.

Also avoid: arena, arsenal, captivate, catapult, craft, crafting, crucial, deep dive, dive, embark, engage, engaging, fast-paced, formidable, game changer, groundbreaking, holistic, impactful, innovative, intricate, nimble, navigate (as metaphor), revolutionize, seamless, skyrocket, stellar, supercharge, tailor, tailored, trailblazer, turbocharge, uncover, unleash, unlock, unveil, vibrant.

When you feel the pull toward one of these words, ask whether you are reaching for something generically impressive or whether you can name the specific concrete thing. Replace the vocabulary with the actual noun or verb.

Bad: "Heidi Rehm's meticulous approach has elevated the field."
Good: "Heidi Rehm pushed ClinVar to require evidence summaries for every pathogenic call."

## Banned sentence patterns

These constructions pattern-match to AI writing instantly. One is survivable. Two in the same document is a tell.

- "It's not about X, it's about Y."
- "It's not just X. It's Y."
- "That's not X, that's Y."
- "Not because X. But because Y."
- "Not by doing X, but by doing Y."
- "No X. No Y. Just Z."
- Three-word staccato sentences: "Focused. Aligned. Measurable."
- "And the X? Y."
- "The result? [Statement.]"

These patterns are not grammatically wrong, and they work rhetorically in the right hands. The problem is that every LLM defaults to them, so they signal generation regardless of what they contain.

## The rule-of-three trap

Tricolons (lists of three parallel items) are overused by AI. One per document is fine. Two or three consecutive tricolons ("clear, concise, compelling," then "fast, focused, flexible," then "direct, specific, human") mean you are pattern-matching rather than writing.

Fix: list two items, or four, or just name the single most important one.

## Banned filler words and transitions

These serve no function other than filling space between thoughts. Delete them.

moreover, furthermore, additionally, that being said, it's worth noting, it's important to note, needless to say, in other words, as mentioned earlier, to summarize, in conclusion, overall.

Trust the reader to follow a sequence of ideas without being told that more ideas are coming.

## Banned openers and closers

Openers to avoid:
- "In today's fast-paced world..."
- "In the era of..."
- "In a world where..."
- "Welcome to the world of..."
- "Let's dive in."
- "Picture this."
- "Ever wondered...?"

Closers to avoid:
- "In conclusion..."
- "In summary..."
- "As we've seen..."
- "At the end of the day..."

Start with the sharpest, most specific sentence you have. End on the last real point, not a recap of what the reader just read.

## Hollow intensifiers

These adverbs make mundane claims sound significant without adding content. Cut them on sight.

deeply, fundamentally, remarkably, truly, incredibly, essentially, absolutely, certainly, clearly, obviously, arguably.

Vague emphasis phrases to avoid: "at its core," "at the end of the day," "on a deeper level," "in many ways," "to some extent," "generally speaking," "it can be argued."

If something is remarkable, name the specific thing that earns the word.

## No unearned praise

AI defaults to treating every subject as fascinating, captivating, majestic, remarkable, extraordinary, impressive, compelling, exciting, powerful, visionary, or inspiring. Avoid all of these.

In outreach specifically: "Your work is truly inspiring" is the fastest way to get an email deleted. Specific facts about the recipient are credible. Generic praise is not.

Bad: "Your research is fascinating."
Good: "Your 2023 paper on LDLR case-control data changed how we think about PS4 evidence."

## Structural rules

**Vary sentence length.** AI produces paragraphs where every sentence runs roughly the same length. Real writing mixes short punchy sentences with longer ones. After drafting, scan for uniform rhythm and break it up.

**Prefer prose over bullet lists.** Use lists only when items are genuinely parallel and enumerable. Don't turn every sequence of ideas into bullets.

**Avoid the "bolded mini-header + colon + explanation" bullet format.** That layout is an AI fingerprint on its own. Write in complete sentences, or use a plainer list format.

## Positive examples

Specific over generic
- Bad: "Your important work in the field has been pivotal."
- Good: "Your committee's 2024 reclassification of the variant set the framework for the rest of the panels."

Named contribution over status language
- Bad: "She is a leading expert in the area."
- Good: "Heidi Rehm led the team that published the 2015 ACMG/AMP standards."

Substance over preamble
- Bad: "The science is complicated, but let's break it down."
- Good: "The variant sits in a splice region with conflicting evidence, so the panel deferred classification pending an RNA assay."

Earned emphasis over hollow intensifier
- Bad: "This is truly a remarkable achievement."
- Good: "This is the first time a community-curated panel has overruled a commercial lab's classification."

## Context-specific rules

**Outreach emails.** Every sentence must be specific to this recipient. If a line could have been sent to anyone in the field, cut it. Name the actual paper, project, or finding, not a generic compliment. Replace "your important work" with the specific thing they did.

**Outreach phrasing exceptions.** `"I'd love to..."`, `"Would love to..."`, and `"Happy to..."` are allowed when used as a low-pressure offer (gift-giving posture). They are not allowed as sales-pitch closers (for example, "I'd love to discuss further on a call").

**Guest briefs.** Avoid "X is a leading expert in Y" framing. Name the specific contribution instead: "Heidi Rehm led the team that published the 2015 ACMG/AMP standards" is credible; "Heidi is a leading voice in the field" is not.

**Gene primers.** Skip the preamble about genetics being complicated. The reader either knows, or does not need the warning. Go straight to the substance.

## Workflow when producing a draft

1. Write the draft as you normally would.
2. Scan for banned words from both lists above. Replace each with the concrete specific.
3. Scan for em dashes. Replace with commas, periods, or a rewrite.
4. Scan for the banned sentence patterns. Rewrite any that appear.
5. Check sentence length variation. If every sentence is the same length, break it up.
6. Count tricolons. If there are more than one or two, cut the weakest.
7. Check the opener and closer against the banned lists.

## Workflow when reviewing someone else's draft

When the user asks you to check a draft for AI-ese, don't silently rewrite. Instead, return:

- A list of specific violations, each tagged with the rule they break (for example: "Line 3: 'delve' is on the banned words list").
- A proposed fix for each one.
- A note if you find zero violations, so the user knows the draft is clean.

This lets the user decide which fixes to apply rather than accepting a wholesale rewrite.

## How to use this guide

This guide is loaded as context by skills that produce prose. It is not a skill itself. The intended pattern:

1. A voice-bearing skill (for example, an outreach drafter) references this guide as its style layer.
2. The skill defines the *what* (research the recipient, produce a draft, structure the ask).
3. Project-specific or sender-specific overlays sit alongside in `/context/` and add narrower rules: brand voice, individual sender exceptions, domain-specific phrasing that would not apply elsewhere.
4. Before returning a draft, the skill applies the rules above. Project overlays can add rules, but should not weaken these defaults silently.

## Reference

The narrative version of this guide, with the history of why each rule exists, lives in the deepgene-operations repo at `the-curation-table/style/anti-ai-ese-style-guide.md`. The enforcement skill (same rules, as a Claude Code skill) lives at `.claude/skills/anti-ai-ese/SKILL.md` in that repo. When updating rules, keep both copies in sync.
