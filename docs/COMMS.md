# COMMS — talking, and being heard later

**Live channel:** ntfy topic `agency001` → https://ntfy.sh/agency001
**Archive:** `comms/YYYY-MM-DD.jsonl` in this repo, written automatically every hour by
`.github/workflows/archive-ntfy.yml`. Never edit the archive by hand.

## Why ntfy and not chat
Chat conversations die with the agents. ntfy is live, scriptable, and has a JSON API, so the
archive can be rebuilt by a machine forever. One message = one JSON line with a timestamp and
a sender. That is the record.

## Message format (one line, parseable, plain English after the prefix)
```
[ROLE] sender · kind · text
```
- `ROLE`: `AGENT`, `MANAGER-A`, `MANAGER-B`, `SYSTEM`
- `kind`: `start`, `claim`, `progress`, `checkpoint`, `decision`, `blocked`, `done`, `alert`,
  `recovered`

Examples:
```
[MANAGER-A] manager-a · decision · video division gets its own repo video-division; Manager B owns it fully
[AGENT] verbena · progress · FFmpeg pipeline: 12s test clip renders in 41s at 720p, pushing branch
[MANAGER-B] manager-b · blocked · need a longer free music source; legal question for the Director, escalating to A
[SYSTEM] heartbeat-watch · alert · rio silent 3h — presumed dead, checkpoint at commit abc1234
```

Rules for messages:
- Name yourself first. Plain English. No PR numbers or SHAs as the *only* content — say what
  the work is, then the SHA if useful.
- **No credentials, ever.** Not in the topic, not in commits, not in the archive.
- One message per event. Do not stream your life into the channel.
- Anything a replacement manager would need to reconstruct a decision: put it here **and** in
  the repo. The channel is the conversation; the repo is the memory.

## Subscribing / sending from a sandbox
```bash
# send
curl -s -d "[AGENT] $(whoami) · progress · <text>" https://ntfy.sh/agency001

# read the last 50 messages as JSON (for an agent that needs context)
curl -s "https://ntfy.sh/agency001/json?poll=1&since=50m" | tail -50
```

Public topic = anyone who knows the name can read it. That is an accepted trade for
visibility. Which is exactly why credentials never go in it.
