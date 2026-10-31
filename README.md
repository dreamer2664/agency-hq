# AGENCY HQ — the central knowledge repository

**Read this, then `docs/ONBOARDING.md`. That is the whole briefing.**

This repository is the agency's persistent memory. It exists so that an agent deployed
months from now can understand the organisation without anyone re-explaining it. If you
are an agent: clone this, read it, report that your onboarding is complete, and wait for
your first assignment. If you are a manager: keep it current. An out-of-date HQ is a lie
the whole organisation inherits.

## 1. The organisation

```
        Director (Carlo — the only human)
                    │
              MANAGER A  ──────── Agency Infrastructure Division
                    │            · documentation & HQ
                    │            · onboarding
                    │            · communications & archive
                    │            · health monitoring & recovery
                    │            · provisioning
              MANAGER B  ──────── Video Production Division
                                 · training programme
                                 · Team A — programmatic (code/FFmpeg)
                                 · Team B — visual (editor workflows)
                                 · QA and sample production
```

- **Manager A** is the Director's *only* point of contact. It oversees everything,
  provisions agents, owns this repository, and supervises Manager B.
- **Manager B** runs the video division with real operational independence. It does not ask
  A permission for ordinary work. It reports *to* A, not *through* A.
- **Workers** own their assignments end to end: clone, build, test, commit, push.

Full responsibilities: `docs/ORG.md`. Divisions: `docs/DIVISIONS.md`.

## 2. The law of this organisation (six lines)

1. **Push your own work.** Every agent has GitHub access. No manager is a bottleneck.
2. **Prove it runs.** Testing is part of the task, not an optional extra. Test results,
   known limitations, reproducible verification — or it is not done.
3. **Never end a run on a command.** A finished run ends with a closing message:
   what you did, what you pushed, the commit SHA, how to verify.
4. **Checkpoint or lose it.** Write your progress to persistent storage (repo/branch) as you
   go. Your sandbox will die mid-sentence. A replacement must resume from your checkpoint.
5. **No secrets in repos, commits, PRs, logs or chat channels.** Credentials live in
   `~/.private/` only. See `docs/CREDENTIALS.md`.
6. **Talk in the open.** Every assignment, decision, blocker and completion goes to the
   ntfy topic `agency001`. See `docs/COMMS.md`.

## 3. Where things are

| thing | where |
|---|---|
| This repo — org, docs, protocols | `dreamer2664/agency-hq` |
| Communication channel (live) | ntfy topic **`agency001`** → https://ntfy.sh/agency001 |
| Communication archive (permanent) | `comms/` in this repo, appended automatically every hour |
| Minor project storage | `dreamer2664/minorprojects` |
| Agent roster & heartbeat state | `org/ROSTER.md`, `org/heartbeats.jsonl` |
| Video division (Manager B) | `dreamer2664/video-division` |
| Infrastructure division | this repo, `divisions/infrastructure.md` |
| Recovery procedures | `docs/RECOVERY.md` |
| Current work | `docs/CURRENT.md` |

## 4. Automation in this repo

- `.github/workflows/archive-ntfy.yml` — every hour, pulls new messages from the ntfy topic
  and appends them to `comms/`. Nobody transcribes anything by hand.
- `.github/workflows/heartbeat-watch.yml` — every hour, checks `org/heartbeats.jsonl` for
  stale agents and rings the channel. Silence becomes visible automatically.

Both run on the repository's own `GITHUB_TOKEN`; no PAT is stored here.

## 5. Onboarding, in one paragraph

Clone this repo. Read `README.md` (this file), then `docs/ORG.md`, `docs/ARCHITECTURE.md`,
`docs/COMMS.md`, `docs/CREDENTIALS.md`, and `docs/CURRENT.md`. Put your credentials in
`~/.private/<yourname>.env` (dir 700, file 600). Register yourself in `org/ROSTER.md`.
Send one message to `agency001` announcing who you are and what you can do. Then report to
your manager that onboarding is complete — and say what you understood the job to be.
