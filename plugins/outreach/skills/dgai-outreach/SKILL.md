---
name: dgai-outreach
description: Draft a DeepGene outreach email to a VCEP coordinator or chair. Wraps the generic outreach-email skill with DeepGene-specific context — the Gene Report offer, VCEP audience framing, and Bryce's voice. Trigger this skill when the recipient is a ClinGen VCEP or GCEP chair, coordinator, or curator and the goal is to introduce Qorus or offer a Gene Report Card. Do not use for non-VCEP recipients or for follow-up emails after a report has been delivered (use dgai-followup for those).
---

# DeepGene Outreach Email (DG layer)

## What this skill does

This is the DeepGene context layer on top of `skills/outreach-email/`. It pre-loads the offer catalog, audience framing, and voice so the generic skill can run without the drafter manually sourcing that context. The logic — research the recipient, match the offer, draft, voice pass, anti-ai-ese pass — is entirely in `outreach-email/SKILL.md`. Read that skill first.

## Context files to load before running

Load these before invoking the generic skill:

- `context/vcep-coordinator-framing.md` — who the recipient is, how to talk to them, what they care about
- `context/gene-report-ask.md` — the offer: what the Gene Report Card is, the four deliverables, how to frame the ask
- `context/offer-catalog.md` — which offer fits which recipient situation
- `context/stage-offer-mapping.md` — gene-stage → offer heuristics
- `../outreach-email/context/recipient-research.md` — research procedure
- `../outreach-email/context/sender-voice-map.md` — sender → voice skill mapping

## Procedure

Follow `skills/outreach-email/SKILL.md` exactly, with these DG-specific notes:

**On the offer:** The Gene Report Card is the primary ask. Surface the three standard offers (ClinVar discrepancy report, reclassification candidates, VUS triage queue) as a menu on first touch unless you can pin the recipient's gene-stage precisely, in which case pick one. Do not invent new offers. Do not describe Qorus as a platform or product — lead with what the report delivers, not what the software does.

**On the ask:** No call required on first touch. The Gene Report Card is the entry point; the discovery call is the natural next step after they engage with the report. If they haven't replied to a first-touch email, do not escalate to a call ask — use `skills/dgai-followup/` instead.

**On the sender:** All outreach goes out under Bryce's name from bryce@deepgene.us. See `../outreach-email/context/sender-voice-map.md`.
