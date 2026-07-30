# Action item (`ai`) schema

`data.json` → key `ai` is a list of action items shown in the Briefing tab's
"Action Items" box. The front-end (`Rental-briefing`) groups these into three
sections: **Current** (due today / overdue), **Upcoming** (due in the
future), and **Completed / FYI** (informational, not actionable).

## Current shape (as of 2026-07-30)

```json
{
  "target": "luke",
  "color": "#ef9f27",
  "html": "<b>Luke Smith</b> — in progress, returns 2:45 PM Sat Aug 1. Tier 3 check-in due tomorrow eve (Thu Jul 31, 5 PM)."
}
```

The front-end currently has to *infer* the section and due date from `color`
(a coarse red/orange/green urgency bucket) and by regex-scraping the last
"Mon D" date out of `html`. That's fragile — it breaks on wording changes and
can't reliably distinguish "today" from "2 days from now" (both are orange).

## Requested shape (new fields, additive)

Add three fields so the front-end never has to infer anything:

```json
{
  "target": "luke",
  "name": "Luke Smith",
  "category": "current",
  "dueDate": "2026-07-31",
  "color": "#ef9f27",
  "html": "<b>Luke Smith</b> — in progress, returns 2:45 PM Sat Aug 1. Tier 3 check-in due tomorrow eve (Thu Jul 31, 5 PM)."
}
```

- **`name`** (string) — the person's display name, as its own field. Replaces
  parsing it out of the `<b>Name</b> —` prefix in `html`.
- **`category`** (string enum: `"current" | "upcoming" | "fyi"`) — which
  section the item belongs in.
  - `current` — needs action today, or is overdue.
  - `upcoming` — due at a specific future point, not yet actionable today.
  - `fyi` — informational only (e.g. "returned, trip complete, moved to Past
    Rentals"); not a to-do.
- **`dueDate`** (ISO date string `"YYYY-MM-DD"`, or `null`) — the concrete
  due date for the action, if there is one. `null` for items with no
  single actionable date (most `fyi` items, and any `current`/`upcoming`
  item where a date doesn't cleanly apply).

`color` and `html` should still be included — the dot color and prose body
are still rendered as before. `color`/`html` are just no longer the *source
of truth* for section/date; `category`/`dueDate` are.

## Why

See `Rental-briefing` PR #4 (Current/Upcoming/FYI split) and the follow-up
that consumes these fields directly instead of the color/regex heuristic.
The heuristic works today but is fragile to prose wording changes — this
schema removes the need for it entirely.
