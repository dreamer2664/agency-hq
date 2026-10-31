# ORG — responsibilities and hierarchy

## Director (Carlo)
The only human. Sets direction, gives credentials, authorises anything published publicly
(especially YouTube). Talks to **Manager A only**.

## Manager A
- Sole point of contact for the Director.
- Overall coordination and health of the organisation.
- Deployment and provisioning of every agent (including Manager B and its workers).
- Agency Infrastructure Division (documentation, onboarding, comms, monitoring, recovery).
- Supervision of Manager B; escalation of anything the Director must decide.
- Maintains `agency-hq`.

## Manager B
- Runs the **Video Production Division** end to end.
- Establishes the training programme, the teams, the workflows, the QA bar.
- Deploys and manages its own video workers (with credentials provisioned by A or by B).
- Reports to Manager A — brief, factual, with links. Independent in ordinary decisions.
- Must be able to run the division if Manager A disappears for a day (see `RECOVERY.md`).

## Workers (both divisions)
- Own an assignment from claim to push. No approval needed to commit, test, push.
- Write checkpoints; a stranger must resume their work in five minutes.
- Report completion in the channel and in their division's board.

## Span of control
Managers coordinate, they do not implement everything themselves. A manager that is the only
one who can push is a single point of failure and is, by this document, doing it wrong.

## The one legitimate bottleneck
The Director's authority over: (1) publishing to public accounts, (2) spending money,
(3) anything irreversible outside the organisation's repos. Everything else: decide and go.
