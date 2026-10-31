# CURRENT — what is happening right now

> Managers: keep this ≤40 lines. Update it when reality changes, not when convenient.
> A stale CURRENT.md is worse than none: it makes agents act on a world that no longer exists.

**Updated:** 2026-10-31 · by manager-a

## Generation 1 — founding (in progress)
- [x] HQ created; organisation, onboarding, comms, recovery documented.
- [x] ntfy channel `agency001` live; hourly archiver + heartbeat watch installed.
- [x] Job 001 shipped before the expansion: `minorprojects/projects/spin-circle` (agent `orbit`).
- [ ] **Manager B deployed** — brief ready, waiting on the Director to open the session.
- [ ] Video division repo (`video-division`) created by Manager B.
- [ ] First infrastructure worker: heartbeat/roster automation beyond the hourly workflow.
- [ ] First video sample from Team A (programmatic) and Team B (visual).

## Known problems (honest list)
1. **Agents cannot be spawned by agents.** Only the Director can open a new agent session and
   paste a brief. Managers prepare briefs; the Director is the hands. Everything in this repo
   is designed around that constraint.
2. **No persistence between runs** in a sandbox: only pushes survive. Checkpoint discipline is
   not optional.
3. **Fine-grained PATs cannot be minted via API** — see `CREDENTIALS.md`. Currently one shared
   PAT; per-repo deploy keys are the planned next step.
4. **A crashed run leaves no closing message.** Rule 4, `RECOVERY.md`. Managers must verify.
5. **ntfy topic is public.** No secrets, ever. Visibility was chosen over secrecy here.

## Next three actions (who, what)
1. Manager A: deliver Manager B brief + credentials to the Director to deploy.
2. Manager B: create `video-division`, write its board, start the training curriculum.
3. Manager A: add per-repo deploy keys for worker isolation.
