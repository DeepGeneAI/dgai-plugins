# Fallbacks (outside research-rooted path)

Use this file when the recipient should not go through the full research-rooted outreach flow in `outreach-email`.

## Purpose

This is a routing table for project-owned alternatives:

- low-context outreach templates
- warm-contact templates
- coordinator or high-volume campaign templates
- non-email alternatives (if this is not an outreach email case)

Keep `SKILL.md` logic-only by storing concrete fallback assets here instead of hardcoding paths in the skill.

## Current project fallbacks

**Warm intro request (Bryce asking a connector to intro him)**
- Asset: `archive/v1-2026-04-15/the-curation-table/outreach/introduction_request_email.md` in `deepgene-operations`
- Three scenarios: Amanda as connector, Tier 1 contacts (Rehm/Haendel/Saliba/Milosovich), post-recording double intro (chair → their coordinators).
- When to use: you have a known mutual connection and want them to make a specific, named intro rather than sending direct outreach.
- Note: templates reference The Curation Table podcast as the CTA. Update the ask to Gene Report Card / discovery call before sending.

**Warm-contact direct (Lisa voice, newsletter-first)**
- Asset: Google Drive — "Email Template/Outreach Strategy Brief"
- Template: Lisa introduces Bryce's gene newsletter, asks which genes the recipient wants to track. No call required.
- When to use: relationship is warm enough that a brief, low-ask newsletter offer is more natural than a researched email.

**High-volume / no per-recipient research**
- Asset: Google Drive — "DeepGene_VCEP_Emails_GeneReportCard" (April 2026 revision)
- 4-email cadence (Day 1 / 5 / 12 / 21). Leads with free Gene Report Card, no call required up front. Gene name personalization in Email 2 is the only required customization.
- When to use: sending to a large list (100+) where per-recipient research is not feasible.

**Cold, no warm intro, short**
- No separate template needed. Use the Ferriss-shape structure in `SKILL.md` (section: "Structure — cold outreach, no prior relationship or warm intro").
- When to use: genuinely cold outreach where the Ferriss shape (3–5 sentences, one specific fact, one small ask) is more appropriate than a researched multi-offer email.

**Non-email (LinkedIn)**
- Asset: `skills/linkedin-message/` — not yet built; see Issue #1 in `SCOUTED.md`.
- When to use: recipient is active on LinkedIn and a DM is the better first-touch channel.

## How to maintain

- Update asset paths if files move.
- If a fallback is retired, remove it and add the replacement.
- If the podcast CTA in the intro-request archive is ever rewritten for the Gene Report Card path, update the note on that row.
