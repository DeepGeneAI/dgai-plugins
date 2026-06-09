---
name: followup-email
description: Draft a follow-up email after a deliverable has been sent. References something specific from what was delivered, proposes one next step, and makes a single clear ask. Use this skill whenever the goal is moving a relationship forward after delivery — not introducing yourself, not re-pitching, not checking in generically. Project-specific context (what was delivered, what the next steps are, brand voice) lives in a companion context layer. For DeepGene post-report follow-ups, use the dgai-followup skill which pre-loads that context.
---

# Follow-Up Email

## What this skill does

Produces a short, specific follow-up email after a deliverable has been sent. The structural requirement is that it references something concrete from the delivery — not "I sent you a report" but what the report found, what changed, what the recipient said they needed. That specificity is what makes a follow-up land rather than read as a check-in.

This is the logic-only skill. It defines what a post-delivery follow-up email is: load what was delivered → extract a specific reference → identify the right next step → draft with a single ask. Project context (what was delivered, the next-step menu, brand voice) belongs to the project context layer.

## When to use this skill versus another path

Use this skill when:

- A deliverable has been sent and the relationship needs a next step
- You have specific content from the deliverable to reference
- The goal is one ask, not a re-introduction or a new offer

Do not use this skill for:
- First-touch outreach (use outreach-email)
- Re-introducing after a long gap with no prior delivery (use outreach-email)
- Sending a second follow-up when the first went unanswered (that is a separate shape — see project context for guidance)

## Inputs needed before starting

Confirm before drafting:

- Recipient name, email, and their role
- What was delivered: the specific product, when it was sent
- At least one specific finding or observation from the delivery — a count, a named item, a threshold. Not "the report" — something in it.
- The proposed next step (from the project context layer's next-steps catalog)
- Sender

If the specific finding is missing, ask before drafting. A generic reference ("I hope the report was useful") is worse than no follow-up.

## Procedure

### 1. Load the delivery context

Identify:

- What was delivered and when
- One specific, concrete thing from that deliverable. Examples: "flagged 4 variants within one evidence criterion of LP," "3 ClinVar conflicts with published papers that may resolve them," "15 VUS in the top tier of the triage queue." The more specific, the better.
- Whether the recipient has replied or engaged (shapes the ask)

### 2. Identify the next step

Use the project context layer's next-steps catalog. The catalog maps delivery type + recipient state to a set of appropriate next steps. Pick one. Do not offer a menu of next steps in a follow-up — one ask only.

### 3. Draft the email

The posture is **peer-to-peer, not following up to see if you read my email.** You have something specific to say. Say it.

#### Structure

- **Subject:** names the gene and the action — not "following up." Something like "ASS1 reclassification flags — worth a look" or "OTC report ready."
- **Greeting:** `Hi [first name],` — single line.
- **Specific reference:** one sentence naming something concrete from the delivery. No "I hope the report was useful." Name a number, a variant, a finding, a section that's particularly relevant to their situation.
- **Next step:** one sentence proposing the specific next action from the catalog. Keep it frictionless.
- **Single ask:** one sentence. One ask. Not two options nested in a hedge — one clear ask with a built-in out. Examples: "Would a 20-minute call be useful?" or "Want me to queue up OTC next?"
- **Sign-off:** `Best,\n[Sender]`

**Length target:** 50–75 words. Shorter than first-touch outreach. The relationship exists; you don't need to re-establish it.

Do not add:
- A re-pitch of what the product does
- An apology for following up
- Urgency signals ("just wanted to check in before the end of the week")
- More than one ask

### 4. Voice pass

Apply the voice skill for the sender (from the project context layer's sender-voice map). Same step as in outreach-email.

### 5. Anti-ai-ese pass

**MUST.** Load `style-guide.md` from the repo root and apply it. Common failure modes in follow-up emails:

- "I wanted to follow up on..." — cut it, start with the specific reference
- "I hope this finds you well" — never
- "Just checking in" — not a reason to email someone
- Generic praise for their work as a warm-up — skip it, they know you already

## Output format

```
SUBJECT: [subject line]

[email body]

---
CONTEXT USED
- Delivered: [product name, date]
- Specific reference: [the finding cited in the email]
- Next step chosen: [from catalog — one line]
- Voice pass: [skill applied]
```
