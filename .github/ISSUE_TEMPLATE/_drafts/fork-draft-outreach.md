# Fork: anthropics/knowledge-work-plugins `draft-outreach` as the structural base for Sprint 3 outreach refactor

**Source:** https://github.com/anthropics/knowledge-work-plugins/tree/main/sales
**License:** Apache 2.0
**Verdict:** Fork
**Scout entry:** SCOUTED.md, Reviewed Candidate 1

## Why this one

The `draft-outreach` skill in Anthropic's official `sales` plugin implements the exact structural pattern the Sprint 3 outreach refactor needs: research the prospect first, then generate personalized outreach with multiple angles. Bryce's 4/30 critique of the v1 outreach skill was that it skipped the research step and sent generic AI-flavored asks. Forking from a maintained, official Anthropic implementation gives us the right bones to build on.

The connectors are wrong (HubSpot/Close/Clay/Slack/M365 — we email VCEP coordinators, not B2B SaaS leads), but the skill *logic* is reusable. Strip the connectors, replace the data sources with the K-Dense PubMed adoption (#issue-link) plus a small ClinGen MCP server (T2.5), and the result is a generic outreach skill with DG-specific context layered on top — exactly the separation principle that anchors the marketplace.

## Installation plan

1. **Fork into `deepgene-plugins/plugins/outreach-email/`** as a generic skill (no DG context). The fork is the *generic logic layer* — what an outreach email is, the research-first pattern, the multi-angle drafting structure.
2. **Strip CRM dependencies.** Remove `.mcp.json` connector definitions for HubSpot, Close, Clay, Slack, M365. Replace with explicit tool calls to:
   - K-Dense `pubmed-database` (publication history)
   - ClinGen MCP server (panel and chair lookups, T2.5)
   - WebFetch (institutional bio scraping)
3. **Pull DG-specific content into a paired plugin** `dgai-outreach-context`:
   - VCEP coordinator framing
   - Gift-giving voice patterns from Bryce's sent emails (Amanda thread, Apr 21–23 2026)
   - Anti-AI-ese skill cross-reference
   - Gene-report-fact-sheet integration
4. **Combined invocation.** `/dgai-outreach <name>` calls the generic `outreach-email` skill with the DG context layer applied. Matches T3.2's two-plugin design.
5. **Migrate existing `plugins/outreach/` content.** Most of it becomes the DG context layer. The structure-as-procedure parts (steps 1–7 in the existing SKILL.md) move into the generic fork as anonymized procedure.

## Integration with logic/context separation

Generic plugin (`outreach-email`):
- Research-first procedure (person → committees → stage → focus → offer → draft → polish)
- Generic offer-matching framework (catalog + signal mapping)
- Generic structural template (greeting, setup, no-pressure frame, hedged ask, offers, soft close)

DG context plugin (`dgai-outreach-context`):
- Qorus Gene Report offer catalog
- Bryce's voice patterns and verbatim phrases
- VCEP-specific stage definitions
- Amanda thread soft-mapping table
- ClinGen / PubMed query templates for gene-of-interest research

Acceptance check (matches v2 design constraint #1): drop `dgai-outreach-context`, and `outreach-email` still produces a valid generic B2B-ish first-touch email. The current outreach skill fails this test — that's the refactor's reason for being.

## Acceptance criteria

- [ ] `plugins/outreach-email/` exists with full attribution to upstream (`UPSTREAM.md` linking the source commit).
- [ ] No DeepGene-specific strings in the generic plugin (ClinGen, Qorus, VCEP, gene names — none of these appear).
- [ ] No CRM connector dependencies in the generic plugin.
- [ ] `plugins/dgai-outreach-context/` ships separately and references `outreach-email`.
- [ ] `/dgai-outreach Amanda Thomas-Wilson` produces a draft Bryce reviews and signs off on, matching the gift-giving voice.
- [ ] Generic `/outreach-email` against a fictional B2B target produces a draft that does not mention ClinGen, VCEP, or Qorus.
- [ ] Existing `plugins/outreach/` archived to `archive/v1-outreach-2026-05/` with a one-paragraph migration note.
- [ ] Apache 2.0 attribution preserved in `plugins/outreach-email/LICENSE` and `NOTICE`.

## Risks and what we'll do about them

- **Upstream changes break our fork.** Mitigation: pin to a commit hash. Re-scout quarterly; rebase deliberately, not automatically.
- **Refactor scope creeps.** Mitigation: this issue closes when the two-plugin split ships and Bryce signs off on one real send. Voice tuning iterates after.
- **Apache 2.0 attribution requirements missed.** Mitigation: include `LICENSE` and `NOTICE` in the fork; reference upstream commit in `UPSTREAM.md`.

## Out of scope for this issue

- Building the `dgai-outreach-package` dispatch pipeline (T3.5).
- Implementing the ClinGen MCP server (T2.5).
- The follow-up email skill (T3.8).
