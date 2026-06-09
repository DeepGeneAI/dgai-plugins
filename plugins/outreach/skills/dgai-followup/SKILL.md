---
name: dgai-followup
description: Draft a DeepGene follow-up email after a Gene Report has been delivered to a VCEP coordinator or chair. Wraps the generic followup-email skill with DeepGene-specific context — what each report product surfaces, the next-steps catalog for the VCEP pipeline, and Bryce's voice. Use this skill when a Gene Report (reclassification candidates, conflict summary, VUS triage, or per-paper summaries) has been sent and the relationship needs a next step. Do not use for first-touch outreach (use dgai-outreach) or for follow-ups before a report has been delivered.
---

# DeepGene Follow-Up Email (DG layer)

## What this skill does

This is the DeepGene context layer on top of `skills/followup-email/`. It pre-loads the report content framing, next-steps catalog, and voice so the generic skill can run without the drafter manually sourcing that context. The logic — load delivery context, extract a specific reference, pick a next step, draft, voice pass, anti-ai-ese pass — is entirely in `followup-email/SKILL.md`. Read that skill first.

## Context files to load before running

- `context/report-content-framing.md` — how to write specific references for each of the four report products
- `context/next-steps-catalog.md` — what to propose based on delivery type and recipient state
- `../outreach-email/context/sender-voice-map.md` — sender → voice skill mapping

Also load the intake record for this recipient if available (`deepgene-operations/intake/examples/` or the pipeline tracker). The intake record tells you which reports were requested, which genes are pending, and any curation stage context.

## Inputs

The `/dgai-followup` command takes a customer name as the argument. Before drafting, confirm:

- **Customer name** (from argument)
- **Gene** — which gene the delivered report covers
- **Report product(s) delivered** — which of the four products were sent
- **Delivery date** — when it was sent
- **Specific finding** — at least one concrete item from the report (count, variant name, paper). Pull from the report itself; do not invent.
- **Recipient state** — have they replied? What did they say?

If the specific finding is not available (report not yet in hand), fill the template with bracketed placeholders and mark the draft clearly. Do not send without substituting real content.

## Procedure

Follow `skills/followup-email/SKILL.md` exactly, with these DG-specific notes:

**On the specific reference:** Use `context/report-content-framing.md` to shape the reference line. Each report product has a template. Use it.

**On the next step:** Use `context/next-steps-catalog.md`. Check whether additional genes are pending (from the intake record or prior thread) — if so, offering to queue the next gene by name is almost always the right move. It's the highest-value next step because it extends the engagement without requiring a call.

**On the ask:** One ask. If the recipient has additional genes pending, the ask is "want me to queue up [GENE] next?" If not, the ask is a short call to walk through findings. Never both.

**On the sender:** All outreach goes under Bryce's name from bryce@deepgene.us. See `../outreach-email/context/sender-voice-map.md`.

**On length:** 50–75 words. Shorter than the first-touch email. The relationship exists.

## Scheduling the follow-up

If a report has been logged as delivered in the pipeline tracker, the follow-up should go out five business days later. To set a reminder:

1. Note the delivery date from the intake record or tracker.
2. Use the `/schedule` skill to create a one-time scheduled task: "Draft and send dgai-followup for [customer] — [gene] report delivered [date]."
3. Set the trigger to five business days after the delivery date.

The scheduled task prompts the drafter to run this skill; it does not send the email automatically.

## Example

See `examples/ass1-amanda.md` for a test draft against the ASS1/Amanda scenario.
