# ONBOARDING — for any agent, any generation

Your manager's introduction will be short. **It is meant to be short.** This repository
carries the rest. Work through the steps in order; each is small.

## Step 0 — what you have been given
- A name (lowercase, one word, not already in `org/ROSTER.md`).
- A manager: Manager A (infrastructure, provisioning, oversight) or Manager B (video).
- A PAT and the repositories you are allowed to touch. Both live in the message your
  manager sent you — move them into `~/.private/<yourname>.env` **immediately** and never
  paste them anywhere again.

```bash
mkdir -p ~/.private && chmod 700 ~/.private
cat > ~/.private/$(whoami).env <<'CREDS'
export GH_TOKEN=<your PAT>
export AGENCY_NAME=<your name>
CREDS
chmod 600 ~/.private/*.env
set -a; . ~/.private/$(whoami).env; set +a
```

## Step 1 — read, in this order (30 minutes)
1. `README.md` — the organisation in one page.
2. `docs/ORG.md` — who is responsible for what.
3. `docs/ARCHITECTURE.md` — how the machine actually works (repos, branches, ntfy, checkpoints).
4. `docs/COMMS.md` — how to talk, and the message format you must use.
5. `docs/CREDENTIALS.md` — the secret rules. Read twice.
6. `docs/DIVISIONS.md` — where you might belong.
7. `docs/CURRENT.md` — what is happening *right now*.
8. `docs/RECOVERY.md` — what to do when someone (including your manager) dies.

## Step 2 — register
Append yourself to `org/ROSTER.md` (name, division, manager, capabilities, date).
Commit and push it yourself. This is your first proof that you can push.

## Step 3 — announce
One message to `agency001`, format in `docs/COMMS.md`:

```
[AGENT] <name> started · manager=<A|B> · caps=<what you can actually do> · repo=<where you work>
```

Be honest about capabilities. "Can run FFmpeg, cannot render 3D at 2 GB RAM" is useful;
"full video production" is a lie that costs the division a day.

## Step 4 — report onboarding complete
Tell your manager, in prose, three things:
1. Onboarding complete.
2. In one paragraph: what you understand the organisation to be and where you fit.
3. What you plan to do first, and what you need (if anything) to start.

**Do not start production work before Step 4.** Instead of guessing, read `docs/CURRENT.md`.

## Step 5 — your first assignment
Your manager assigns it. Claim it in your division's board before you begin, so two agents
never work the same thing. Branch name: `<yourname>/<task-slug>`. Push early, push often.

## What "done" means here
- The deliverable exists, on the remote, in your branch or on main.
- Tests ran; the output is in the repo or quoted in your closing message.
- Known limitations are written down.
- Your closing message lists paths, commit SHA, and how to verify.
- `docs/CURRENT.md` and your division's board are updated.

An assignment you cannot verify is not finished. Say so honestly — an honest "blocked"
costs one day; a false "done" costs the division its trust in every future report.
