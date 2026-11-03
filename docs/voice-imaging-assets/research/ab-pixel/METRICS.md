# ab-pixel — the measured table

Everything below is produced by `measure_voice.py` from the committed stems in
`v07_stems/`. Regenerate with `python3 plan.py` then the two `measure_voice.py` calls
in `../voices-pixel.md` §7.

| metric | v07 method (before) | line-split (after) |
|---|---|---|
| lines | 20 | 25 |
| words | 96 | 96 |
| speech, s | 35.5 | 37.97 |
| last word, s | 57.775 | 57.16 |
| F0 SD, semitones | 3.939 | 3.779 |
| F0 p5-p95 range, ST | 12.688 | 12.558 |
| F0 median, Hz | 109.25 | 107.45 |
| inter-line gaps, n | 19 | 24 |
| gap median, s | 0.685 | 0.445 |
| gap max, s | 9.2 | 3.63 |
| gap SD, s | 2.06 | 0.822 |
| gaps at 0.06 s floor | 7 | 0 |
| rate CV | 0.253 | 0.293 |
| pause before twist, s | 0.975 | 3.63 |
| longest gap in film, s | 9.2 | 3.63 |
| pitch reset, mean ST | 7.242 | 5.515 |

## Plate metrics (1920x1080, ungraded)

| plate | laplacian var | contrast SD | lit % | lit:unlit |
|---|---|---|---|---|
| plate1_kitchen — before | 83.9 | 39.2 | 34.4 | 0.523 |
| plate2_hall — before | 46.7 | 29.2 | 32.4 | 0.48 |
| plate3_street — before | 615.9 | 57.0 | 66.2 | 1.957 |
| plate1_kitchen — after | 128.5 | 59.8 | 48.5 | 0.942 |
| plate2_hall — after | 115.6 | 49.7 | 51.5 | 1.062 |
| plate3_street — after | 352.1 | 48.2 | 42.2 | 0.729 |

## ElevenLabs (see ../ELEVENLABS-LEDGER.md)

| condition | chars | duration | F0 SD | pauses >=0.15 s | longest pause |
|---|---|---|---|---|---|
| block, 1 call | 533 | 41.89 s | 4.349 ST | 29 | 0.85 s |
| newline-split, 1 call | 557 | 41.75 s | 4.913 ST | 31 | 0.73 s |
