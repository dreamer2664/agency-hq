# CREDENTIALS — the rules, and the honest limits

## What exists
1. **GitHub access** for every agent, so each can clone/branch/commit/push without a manager.
2. **Agent application cookies** (arena.ai) for each manager, so it can deploy and manage its
   own workers.
3. **ntfy** — no credentials; the topic is public by design.

## The rules
- Credentials are stored **only** in `~/.private/<name>.env`, directory `700`, file `600`.
- Never in a repository, a commit, a PR, a branch name, a screenshot, a chat log, an ntfy
  message, or a doc in this repo. Not even "temporarily".
- Never print a credential in your output, including in error messages. Use `${GH_TOKEN}`.
- If you believe a token has leaked: say so in the channel immediately, and tell Manager A.
  Rotation beats silence.
- Prefer the narrowest access that lets you do the job.

## Honest limits (recorded so nobody pretends otherwise)
- **Fine-grained PATs cannot be created through the GitHub API.** GitHub has no endpoint for
  minting tokens. Per-agent fine-grained tokens must be created by hand in the web UI, so the
  practical options are:
  - *Shared PAT (current)*: one token with admin on the agency's repos, provisioned to each
    agent. Simple, works today, but every agent can touch everything and rotation means
    rotating everywhere.
  - *Per-repo deploy keys (SSH)*: creatable via API, individually revocable, scoped to a
    single repo with write access. Good next step for worker isolation — a worker on the
    video repo cannot touch `minorprojects`.
  - *Fine-grained PATs (manual)*: the correct end state if the Director wants per-agent scope;
    requires the Director to mint them in the UI. Ask; do not silently proceed.
- **Arena cookies are a full account session.** Any agent holding them is the Director for
  that application. Treat them as root. Rotate after major generations.
