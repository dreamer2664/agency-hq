# ab-pixel — evidence for the voice and imaging research

Two research notes live one directory up: [`../voices-pixel.md`](../voices-pixel.md) and
[`../imaging-pixel.md`](../imaging-pixel.md). This directory holds everything they cite.

## Voice — the v07 narration, performed two ways

| file | what | length |
|---|---|---|
| `v07_stems/before_v07_narration.wav` | v07 method: 20 lines, one global `--rate=-12%`, absolute start times | 60.000 s |
| `v07_stems/after_v07_narration.wav` | line-split method: 25 lines, designed gap before each, per-line rate and pitch | 60.000 s |
| `v07_stems/{before,after}_timing.json` | per-line start, end, gap, rate, pitch, text | — |
| `before_15s.mp3` / `after_15s.mp3` | 15 s excerpts, **loudness-matched** with `loudnorm` (−16 LUFS) so the comparison is not a volume trick | 15.0 s |
| `before_after_stems/*.wav` | the same excerpts, uncompressed | 15.0 s |

**Listen to `before_15s.mp3` and `after_15s.mp3` back to back.** The difference is not pitch — it is
that the second one takes a breath.

The 15 s samples are the *open* of the film, which is where the gap design is least dramatic. The
held beat before the twist (3.63 s) is at 36.7 s and is **not** in the excerpt. The full stems are
the complete evidence.

## Plates — three matched before/after pairs

`plates_before/` is the naive prompt (`dramatic lighting, moody, 8K, hyperrealistic`);
`plates_after/` is the camera-language prompt (lens, aperture, shutter, film stock, one located
practical source, texture, scene-specific negatives). Same subject in both, so only the craft differs.

| subject | before | after |
|---|---|---|
| kitchen at 2 a.m. | `plates_before/plate1_kitchen.png` | `plates_after/plate1_kitchen.png` |
| hallway with a door ajar | `plates_before/plate2_hall.png` | `plates_after/plate2_hall.png` |
| wet residential street | `plates_before/plate3_street.png` | `plates_after/plate3_street.png` |

All six are normalised to **1920×1080** (native ~1376×768, centre-cropped to 16:9, Lanczos). The
natives are kept in `plates_*/native/` because Laplacian variance is scale-dependent and anyone
re-running this should measure the natives at a common resolution.

## The tables

- `METRICS.md` — everything in one place: voice metrics, plate metrics, ElevenLabs.
- `v07_metrics.json` — raw `measure_voice.py` output for both full stems.
- `plate_metrics.json` — raw `plate_metrics.py` output.

## Rebuild

```bash
export PATH="$HOME/bin:$PATH" && pip install edge-tts     # ffmpeg + edge-tts

cd research
python3 ab-pixel/plan.py                                   # both stems, ~60 s, uses a content-hashed cache
python3 tools/measure_voice.py ab-pixel/v07_stems/before_v07_narration.wav \
        --lines ab-pixel/v07_stems/before_timing.json --twist 14
python3 tools/measure_voice.py ab-pixel/v07_stems/after_v07_narration.wav \
        --lines ab-pixel/v07_stems/after_timing.json --twist 19
cd ab-pixel && python3 plate_metrics.py
```

`plan.py` caches every synthesised line by a SHA-1 of `voice|rate|pitch|text`, so re-timing the film
costs seconds and no characters. That cache is what made the timing solvable at all — before it,
every spacing adjustment meant a full re-synthesis of 45 clips.

## Honest status

- **No human listened to either stem and no human judged either set of plates.** Every number here
  is instrumental. The Director's ear is the only preference data in this project and it says the
  old voices are unacceptable.
- The ElevenLabs comparison is **two conditions inside a single call each**, not 25 separate calls.
  The 1,200-character cap could not cover three conditions; see `../ELEVENLABS-LEDGER.md`.
- These plates come from a generator with **no seed parameter**. They cannot be regenerated
  deterministically. The prompt text is the only reproducible artefact.
