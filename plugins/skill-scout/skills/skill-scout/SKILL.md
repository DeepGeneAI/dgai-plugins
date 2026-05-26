---
name: skill-scout
description: Runs a pre-build search to find existing skills or agents before writing a new one. Trigger this skill whenever you are about to write a new SKILL.md, define a new agent, or build any reusable automation. Also trigger when the user says "search before building", "scout for a skill", "does something like this exist", "find an existing skill for", or "check before we build." The skill delegates to the skill-scout sub-agent (constrained to Read, Glob, Grep, WebFetch, WebSearch) and returns a scored candidate table plus a recommendation.
---

# Skill Scout

## What this skill does

Searches external sources for existing skills or agents that match a described capability before any new SKILL.md gets written. The scout runs as a constrained sub-agent (no write access, no shell) so it cannot create anything — it can only find and score.

The output is a scored table and a single recommendation: USE AS-IS, ADAPT, or BUILD FROM SCRATCH.

## When to use

Use this skill **before** writing any new SKILL.md or agent definition. The search-before-build rule from 2026-04-28 architecture principles applies to every new capability, no exceptions.

Do not skip the scout because the capability "feels unique." The recommendation might still be BUILD FROM SCRATCH — but running the search is what makes that conclusion defensible.

## Inputs needed

Before invoking the scout, confirm:

1. **Capability description** — one sentence describing what the skill should do. Be specific: "revise a draft email into Bryce's voice" is better than "voice skill."
2. **Fit context** (optional) — if the skill is for a non-standard runtime or stack, say so. Default assumption is Claude Code + Python, DeepGene operations repo.
3. **Additional sources** (optional) — any specific repos or URLs beyond the defaults. Drop them in if you have them.

If the capability description is missing or too vague, ask before invoking.

## How to invoke

Spawn the scout as a sub-agent using the Task tool:

```
Task: skill-scout
Prompt: [capability description] [fit context if non-default] [additional sources if any]
```

The scout's constrained tool list is: Read, Glob, Grep, WebFetch, WebSearch. It cannot write files or run shell commands. It will search the default source list (Anthropic repos, awesome-claude-code, internal scouted.md, plugin marketplaces) and return a scorecard.

## Scorecard columns

| Column | What it measures | Scale |
|--------|-----------------|-------|
| Docs | Inputs, stop conditions, and what not to use are findable without a sync | 1–5 |
| Recency | Latest commit or update date | 1–5 |
| License | Explicit license file present | 1–5 |
| Fit | Works in Claude Code + Python ops workflow without significant changes | 1–5 |
| Install | Effort to wire in cold | 1–5 |

Total is out of 25. Internal files score License as 3 by default (no license = private internal, not a blocker).

## Acting on the recommendation

**USE AS-IS** — Copy or reference the file directly. Add a note to `notes/scouted.md` with the source, score, and date so future scouts find it faster.

**ADAPT** — The scout's Reason block will name the specific file and what to change. Make only those changes; don't expand scope. When done, add the adapted skill to `notes/scouted.md` with a note on what was changed and why.

**BUILD FROM SCRATCH** — The scout found a real gap. Proceed with the new SKILL.md. When shipped, add it to `notes/scouted.md` as a new internal row so the next scout finds it.

In all three cases, update `notes/scouted.md`. The file is the accumulating inventory of what has been scouted; its value compounds over time only if every scout pass writes its findings back.

## What to do with the scorecard

The scorecard comes back from the Task tool result. Review it before proceeding:

- If total score ≥ 18 and recommendation is USE AS-IS: proceed immediately.
- If ADAPT: read the Reason block carefully. The edit scope is usually small. If it turns out larger than described, start a new scout pass for the adapted version.
- If BUILD FROM SCRATCH: note the GAPS WORTH FILING section — if the scout flagged a gap worth contributing upstream, log it in `notes/scouted.md` under a "Gaps" section.

Do not skip the scorecard review and jump straight to building. The whole point is the pause.
