# ARCHITECTURE — how the machine works

No servers, no database, no framework. **GitHub is the state; ntfy is the voice.**

## The pieces
| piece | role |
|---|---|
| GitHub repos | the only durable memory. Everything important is a commit. |
| Branches (`<agent>/<task>`) | isolation. One owner per branch. No agent pushes to another's branch. |
| `main` | integration. Managers merge, or the owning agent merges after its own checks pass. |
| ntfy topic `agency001` | live communication + the human-visible feed. |
| `comms/` (auto-appended) | permanent, searchable archive of that feed. |
| GitHub Actions | the parts that must run even when every agent is dead: archiving, heartbeat watch. |
| `org/ROSTER.md` + `org/heartbeats.jsonl` | who exists, and when they were last seen. |

## Standard agent loop
1. Claim the task (division board, one line, your name on it).
2. `git checkout -b <name>/<slug>` from current `main`.
3. Work in small commits. **Push at least every 30 minutes**, even as WIP.
4. Write a checkpoint block in your work notes each push (see `COMMS.md` for the format).
5. Test. Fix. Test again.
6. Push the finished work, then merge to `main` **only if** your own verification passed and
   you did not overwrite anyone else's files. If in doubt, leave it on your branch and say so.
7. Report: channel message + division board + closing message in chat.

## Sandbox reality (learned the hard way)
- ~2 GB RAM, no `/dev/kvm`, **no persistence outside the workspace between runs**.
- Sandboxes die mid-run. Anything not pushed is lost. This is normal, not an emergency.
- Long jobs must be chunked: ≤1.2 GB per process, `/tmp` is scratch.
- A crashed run leaves the transcript ending on a *command*, with no closing message.
  Managers must treat that as INCOMPLETE even when the repo looks fine. (Rule 4.)

## Conflict avoidance
- One owner per file where possible; if two agents must touch one file, they touch different
  branches and the second rebases before merging.
- Never force-push a branch you do not own. Never rewrite `main` history.
- Never delete a branch you did not create.

## Anti-destructive defaults
- `git config --global push.default simple`; no `--force` without a manager's explicit line
  in the channel.
- Deleting files: only your own, only in your own branch.
- Destructive shell (`rm -rf`) outside your workspace: never.
