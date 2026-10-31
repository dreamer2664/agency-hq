# ROSTER

One line per agent. Append yourself when you onboard (that is Step 2 of `docs/ONBOARDING.md`).
`last_seen` is also fed by `org/heartbeats.jsonl`; the hourly workflow alerts on silence > 3h.

| name | role | division | manager | caps | status | last_seen |
|---|---|---|---|---|---|---|
| manager-a | Manager A | infrastructure + oversight | Director | provisioning, docs, GitHub, browser automation via Director, ntfy | active | 2026-10-31T14:20Z |
| orbit | worker | minor projects (job 001) | manager-a | single-file front-end, canvas, playwright | idle / warm | 2026-10-31T13:19Z |
| manager-b | Manager B | video production | manager-a | TBD on deployment | not deployed | — |

## Conventions
- Name: lowercase, one word, unique.
- `status`: `active`, `idle`, `blocked`, `presumed-dead`, `retired`.
- A `presumed-dead` agent keeps its history; do not reuse the name for a different agent
  without noting it here.
