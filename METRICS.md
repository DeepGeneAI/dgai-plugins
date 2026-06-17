# DeepGene Plugin KPI

Two leading indicators and one outcome indicator.
Stats are auto-generated — run `python3 scripts/update-metrics.py` to refresh METRICS.md, or `python3 scripts/update-metrics.py --sync-sheets` to also push to the [Google Sheet](https://docs.google.com/spreadsheets/d/1Sr5ccK7UQl83qPq6d7CaJVVeuxSX8PNfv9beb_vWDA8).

---

## Manual counters

Update these by hand after each send/event.

| Counter | Value |
|---|---|
| outreach_packages_sent | 0 |
| responses_received | 0 |

---

<!-- METRICS:START -->
*Last updated: 2026-06-16 08:01 UTC*

## Skills published

**8** plugins in marketplace

- outreach
- vcep-research
- dgai-hello
- dgai-clingen
- dgai-instrumentation
- invocation-log
- skill-scout
- warm-path

## Invocations — last 7 days

*No invocations recorded yet.*

<!-- METRICS:END -->

---

## Targets

| Indicator | Type | Good | Trigger review |
|---|---|---|---|
| Skills published | Leading | Growing week-over-week | Flat for 4+ weeks |
| Invocations per skill per week | Leading | Every published skill used at least once | Any skill at zero for 2 weeks |
| Outreach packages sent | Outcome | 3+ per week during active outreach | 0 in any given week |

Lagging indicators (revenue, customers acquired) are Bryce's to track.

---

## Data sources

- **Skill invocations:** `~/.claude/dgai-skill-invocations.jsonl` — written by the `dgai-instrumentation` plugin hook
- **Deduplication rule:** one counted invocation per skill per session per 60-second window
- **Skills published:** `.claude-plugin/marketplace.json`
- **Manual counters:** edited directly in this file
