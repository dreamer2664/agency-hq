# DIVISIONS

## 1. Agency Infrastructure Division — Manager A
Purpose: make the organisation *more capable over time*. If the division works, a new agent
needs one repository and thirty minutes to become useful.

Standing responsibilities:
- **HQ upkeep** (`agency-hq`): structure, docs, decisions, known problems — current, not
  aspirational.
- **Onboarding**: every new agent follows `docs/ONBOARDING.md`; fix that document whenever a
  new agent stumbles on it.
- **Communications**: the `agency001` channel and its automatic archive.
- **Health**: roster, heartbeats, detection of silence, resumption of crashed work.
- **Provisioning**: GitHub access and manager cookies for new agents; least privilege possible.
- **Recovery drills**: once per generation, actually run `docs/RECOVERY.md` on purpose.

## 2. Video Production Division — Manager B
Purpose: produce genuinely professional video, not AI slideshows. Two teams, deliberately
independent, so one agent's death never stops production.

### Training first, production second
Every worker completes a short curriculum before producing: storytelling, script/narrative,
audience retention, motion design, animation, typography/composition, editing & pacing, VFX,
sound design, colour, thumbnails, YouTube packaging. Free/public sources; each worker writes a
one-page summary of what it actually learned **and** one small artefact proving it (a 10-second
animation, a thumbnail, a colour-graded clip).

### Team A — Programmatic production
Code-generated video: FFmpeg filter graphs, Python rendering, animation libraries, generated
typography/diagrams/transitions. Every deliverable is a *program plus its output*, so it can be
re-run and varied. This team is expected to become the division's reliable backbone: cheap,
deterministic, testable.

### Team B — Visual production
Conventional editing workflows, investigating what genuinely runs in a ~2 GB Debian sandbox
(Kdenlive/Shotcut via Xvfb+VNC, browser-based editors, CLI compositing). Its research output is
as valuable as its videos: a truthful map of what is possible on this hardware.

### Structure decision
Keep the two teams **separate but interoperable**: shared style guide, shared asset library,
but no cross-team dependency in any single video's critical path. A video must be producible
end-to-end by one worker in one team. Rationale: independence beats coordination at this scale.

### Publication
**Nothing is published to the Director's YouTube account without explicit authorisation.**
Samples and experiments stay in the division repo.

## Division boards
Each division keeps `BOARD.md` in its own repo: one line per assignment —
`task — owner — status — branch — last update — next step`.
