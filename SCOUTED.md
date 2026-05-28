# SCOUTED.md

T1.4 scout pass. Five candidates, two picks. Scouted 2026-05-07 across `anthropics/skills`, `anthropics/knowledge-work-plugins`, `awesome-claude-code`, claudemarketplaces.com, and buildwithclaude.com. Focus: outreach, research briefing, content generation.

## Scoring criteria

Each candidate gets 1–5 on five criteria. Total is informational. The verdict sentence is the call.

1. **Docs** — can someone other than the author install and run it without guessing.
2. **Maint** — last commit, issue triage, signs of life in the last 90 days.
3. **License** — MIT, Apache, BSD = 5. Restrictive or missing = lower.
4. **Fit** — how directly it maps to outreach, guest briefs, or gene primers.
5. **Install** — how much work between finding it and having it run. Less work scores higher.

Verdicts: **Adopt** (drop in), **Fork** (good outline, needs DG content), **Reference** (study, don't install), **Skip**.

---

## Candidates

### 1. anthropics/knowledge-work-plugins, `sales` plugin

Link: https://github.com/anthropics/knowledge-work-plugins/tree/main/sales
Last commit: 2026-05-06
License: Apache 2.0

Docs 5 / Maint 5 / License 5 / Fit 3 / Install 2 = **20/25**

**Fork.** The "research the person, then draft" structure inside `draft-outreach` is a pattern that could work for our outreach skill. We don't use HubSpot or Close, so we can keep the SKILL.md and drop the connector config.

### 2. coreyhaines31/marketingskills, `cold-email` skill

Link: https://github.com/coreyhaines31/marketingskills/tree/main/skills/cold-email
Last commit: 2026-04-24 (v1.9.0), 258 commits on main
License: MIT

Docs 5 / Maint 5 / License 5 / Fit 2 / Install 5 = **22/25**

**Reference.** B2B SaaS conversion voice is the opposite of how we write to VCEP coordinators. Worth reading for the follow-up sequencing logic. Adopting it would push us in the wrong direction.

### 3. K-Dense-AI/scientific-agent-skills, `pubmed-database` skill

Link: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/scientific-skills/pubmed-database
Last commit: 2026-05-01 (v2.38.0), 448 commits on main
License: MIT at repo level; per-skill license in SKILL.md frontmatter (verify before adopting)

Docs 4 / Maint 5 / License 5 / Fit 5 / Install 5 = **24/25**

**Adopt.** Direct replacement for the PubMed step inside `guest_brief_generator.py`. No DG-specific changes needed since it's just doing the PubMed lookup. Other skills in the same repo (OpenAlex, Crossref, Semantic Scholar) are worth looking at later.

### 4. ComposioHQ/awesome-claude-skills, `lead-research-assistant`

Link: https://github.com/ComposioHQ/awesome-claude-skills/tree/master/lead-research-assistant
Last commit: within ~1 week of scout (verify on commit history)
License: per-skill; verify SKILL.md before adopting

Docs 4 / Maint 4 / License 3 / Fit 3 / Install 3 = **17/25**

**Reference.** The shape (research, then structured output, then draft) is what I want for `dgai-outreach-package`. The qualification logic is B2B sales stuff (revenue, buying signals), which doesn't translate to ranking VCEP chairs. Read it when we're laying out the outreach flow.

### 5. anthropics/skills, `internal-comms`

Link: https://github.com/anthropics/skills/tree/main/skills/internal-comms
Last commit: 2026-04-07
License: MIT

Docs 5 / Maint 5 / License 5 / Fit 3 / Install 5 = **23/25**

**Reference.** Clean official example of separating generic skill logic from filled-in `examples/`. Read before authoring `gene-brief` and `cover-brief` skills. The `examples/` directory pattern is how we should keep DG-specific content next to generic skills.

---

## Picks

**Adopt: K-Dense `pubmed-database`.** Safest pick. Fills a real gap and comes with other maintained skills in the same repo.

**Fork: knowledge-work-plugins `draft-outreach`.** Outline for the Sprint 3 outreach refactor. Drop the connector config and point the research step at the K-Dense PubMed skill plus a small ClinGen MCP (T2.5). Rewrite the voice section to sound like us.

Both filed as GitHub issues with installation plans (`.github/ISSUE_TEMPLATE/_drafts/`).

---

## Skipped

- **Overloop CLI** (from `awesome-claude-code` issue #1278): paid contact DB, API key required.
- **BrianRWagner/cold-outreach-sequence**: tiered signal-strength idea is interesting but coreyhaines31 covers similar ground.
- **knowledge-work-plugins `productivity` (workplace memory)**: per-coordinator memory is interesting, but only after we have outreach volume.
- **anthropics/skills `brand-guidelines`**: same logic-vs-context pattern as `internal-comms`, but `internal-comms` is the closer fit.
- **sociilabs/claude-content-writer, aaddrick/written-voice-replication**: voice-rewriting is real but lower priority than research and structure gaps. Re-scout when T2.2 is ready.

---

Re-scout quarterly, or when something interesting lands in `anthropics/knowledge-work-plugins` or `K-Dense-AI/scientific-agent-skills`.

---

## T2.1 scout pass: output styles

Scouted 2026-05-18.

### 1. hesreallyhim/awesome-claude-code-output-styles-that-i-really-like

Link: https://github.com/hesreallyhim/awesome-claude-code-output-styles-that-i-really-like
Stars/Fork: 41 / 1

**Skip.** No structural technique to borrow.

