# RECOVERY — when someone dies

Every agent in this organisation will eventually crash mid-run. That is the normal weather.

## Is it dead or done?
- A finished run ends with a **closing message in prose**.
- A crashed run ends on a **command** (`Ran commands`, `Edited files`, a screenshot read).
- Crashed ≠ done, even if the repo looks complete. Mark it INCOMPLETE, then resume it.

## Resuming a crashed agent
1. Read its last checkpoint / last push. That is the truth of where it got to.
2. Give it a continuation, not a restart: "your sandbox crashed, verify what you pushed,
   fix only what is broken, then report."
3. Do not rebuild good work. Do not reset branches.
4. Log the crash in the division board with time + last commit.

## If Manager B dies
Manager A takes over the video division **temporarily**: keep production moving, do not
redesign it. Deploy a new Manager B from `docs/ONBOARDING.md` + the Manager B brief, hand it
`video-division` and this repo. Its first task: read `docs/CURRENT.md`, the division board,
and the last week of `comms/` — then confirm it understands.

## If Manager A dies
Manager B becomes acting Manager A: it keeps infrastructure ticking (archive workflow,
heartbeat watch, roster), reports directly to the Director, and deploys a replacement A.
**The Director is then B's point of contact until a new A exists.** Neither manager should
need the other for its own ordinary work — that is the point of the split.

## If the Director is unavailable
Everything continues except: publishing to public accounts, spending money, and irreversible
external actions. Those wait.

## Standing resilience rules
- No essential knowledge in one sandbox or one conversation. Repo + archive, always.
- Every manager writes a handover block in `docs/CURRENT.md` before starting a large job.
- Heartbeats: `org/heartbeats.jsonl`, one line per agent per run. The hourly workflow turns
  silence into a visible alert.
