# PUSH-RUNBOOK.md — pixel/voice-imaging

**Status: committed locally, NOT pushed.** The sandbox has no GitHub write credential. Detail and
evidence of the attempt are in §2. Everything else is ready — branch rebased onto current `main`,
no collisions, no secrets.

Branch: `pixel/voice-imaging` · commit `236ebe2` · based on `main` @ `84344bc`
39 files, 2,335 insertions, all under `research/`.

---

## 1. The one command

From a clone with a working GitHub credential:

```bash
git fetch origin
git checkout -b pixel/voice-imaging origin/main
git bundle unbundle /path/to/pixel-voice-imaging.bundle    # or: git pull /path/to/pixel-voice-imaging.bundle pixel/voice-imaging
git reset --hard 236ebe2
git push -u origin pixel/voice-imaging
```

Or, if the workspace is intact on the same machine:

```bash
cd /home/user/wd && git push -u origin pixel/voice-imaging
```

The bundle is `pixel-voice-imaging.bundle`, 38 MB, thin against `origin/main` — it contains only my
commit plus the objects it needs. `git bundle verify` reports *"records a complete history"*.

---

## 2. Why I could not push it myself — the evidence

```
$ git push -u origin pixel/voice-imaging
fatal: could not read Username for 'https://github.com': terminal prompts disabled

$ git ls-remote --heads origin        # read works — the repo is public
45ebb3b...  refs/heads/cut/toolchain-map
...
84344bc...  refs/heads/main

$ ls ~/.git-credentials ~/.netrc ; git config --get-regexp credential ; env | grep -i token
no cred files
no credential config
no token env
gh not installed
```

**Read access works, write access does not.** There is no token, no credential helper, no `gh` CLI,
and no `/run/secrets` on this box. I checked all five standard locations. This is the fifth sandbox
in a row; each reset wipes any token that might have been injected earlier.

`refs/heads/pixel/voice-imaging` is **absent** from `git ls-remote` — confirming the manager's read
of the situation. `pixel/v09` is also absent from the remote, permanently: its commits `fbce812` and
`03b3a06` were destroyed by an earlier reset and cannot be recovered from here.

---

## 3. What is in the commit

| path | what |
|---|---|
| `research/voices-pixel.md` | 385 lines. Writing for synthetic speech, line splitting, rate variation. Cited, 12 sources. |
| `research/imaging-pixel.md` | 289 lines. Camera language, lighting as source, weather, negatives, composition, seeds. Cited, 6 sources. |
| `research/ELEVENLABS-LEDGER.md` | **appended** a `pixel` section to the shared ledger — did not touch reel's or grade's sections. |
| `research/tools/measure_voice.py` | the instrument. YIN tracker, validated exact on synthetic tones before any number was trusted. |
| `research/ab-pixel/plan.py` | reproduces both stems: content-hashed synth cache + pacing solver. |
| `research/ab-pixel/v07_stems/` | the two 60.000 s stems + per-line timing JSON. |
| `research/ab-pixel/before_15s.mp3`, `after_15s.mp3` | 15 s excerpts, loudness-matched. |
| `research/ab-pixel/plates_{before,after}/` | three matched pairs at 1920×1080, natives preserved. |
| `research/ab-pixel/METRICS.md` | every number in one table. |

---

## 4. The three findings, for the report line

1. **The voices were not monotone.** Both stems measure 3.94 and 3.78 semitones F0 SD — *above* the
   2.5–3.5 ST normative band for male read speech. The defect was timing: v07 put **7 of 19**
   inter-line gaps on the packer's 0.06 s floor. The re-performance puts **0 of 24** under 0.10 s and
   holds **3.63 s** before the twist against 0.975 s. Line splitting is a *timing* fix, and claiming
   otherwise would be a fabricated win.
2. **v07 has a 9.2 s hole at 37 s.** Its shot-window table gave lines 14–16 a shared window end of
   46.00 with line 17 starting at 46.20. That is not a robot defect, it is dead air in the climax,
   and it is the single most actionable bug found this round.
3. **A night plate is supposed to lose detail numbers.** The street plate scored highest on
   Laplacian variance (615.9) and looked like stock footage; the re-shot version scored 352.1 and
   looks like a photograph. lit:unlit above ~1.5 is the tell that a plate has stopped being night —
   the one metric that agreed with the eye.

**No human listened to either stem and no human judged either set of plates.** Every claim is
instrumental. That limitation is stated in both notes.

---

## 5. For next round

- **The ElevenLabs three-way comparison did not fit the cap.** 25 separate synthesis calls costs 509
  characters; 533 + 557 + 509 = 1,599 against a 1,200 cap. It is item one next round with 8,910
  characters of the monthly allowance unspent.
- **v09 must be redone or officially written off.** It is absent from the remote and its commits are
  gone. It also used the same single-global-rate construction this research indicts, so it should
  not be resurrected unmeasured.
- **Plates need a seeded generator** before they can be a build step rather than an artefact. The
  current pipeline cannot regenerate a plate deterministically; the prompt text is the only
  reproducible record.
