#!/usr/bin/env python3
"""
ab_render.py — the v07 passage performed twice, so the difference can be measured and heard.

BEFORE  reproduces the v07 method exactly: the text as it was written, one synthesis call per
        *block* of lines (which is how a script like that is usually fed to a TTS engine: paste the
        narration, generate, cut to length), global --rate=-12%, no deliberate gaps. This is the
        "single long generation" failure the research describes: prosody is predicted over a limited
        window, the model loses the arc, and the result is flat and even.

AFTER   the same words rewritten for speech, split into one synthesis call per line, each line
        rendered at its own rate, placed on the timeline with a gap chosen for its meaning
        (short for a list, long before the turn), and given a breath of room noise between lines
        instead of digital silence.

Both are written to research/ab-pixel/ as 15 s stems plus a 15 s samples with the bed underneath,
and both get the same measurement pass (research/tools/measure_voice.py).

Only the passage's *delivery* changes between the two: same story, same beat order, same landing.
"""
import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np

SR = 48000
VOICE = "en-US-ChristopherNeural"
PITCH = "-4Hz"

HERE = Path(__file__).resolve().parent
OUT = HERE
WORK = HERE / "work_ab"
DUR = 15.0
N = int(DUR * SR)


# ---------------------------------------------------------------- BEFORE
# v07's narration, exactly as committed (assets/voice.py on pixel/v07). One block, one rate.
BEFORE_TEXT = (
    "Night two, two fourteen again. Same flat, same speaker, nothing changed. "
    "Except the walls. And the door. And the kitchen. Six rooms in this flat. "
    "Six surfaces, six microphones. So I keep it loud, all night."
)
BEFORE_RATE = "-12%"


# ---------------------------------------------------------------- AFTER
# Rewritten for the ear. Shorter units, contractions, numerals spelled out as they are said,
# one idea per line. (index, rate, gap_before_s, text)
AFTER_LINES = [
    (1, "-16%", 0.00, "Night two."),
    (2, "-14%", 0.42, "Two fourteen. Same flat. Same speaker."),
    (3, "-12%", 0.30, "Nothing's changed."),
    (4, "-18%", 0.55, "Except the walls."),
    (5, "-12%", 0.20, "And the door."),
    (6, "-12%", 0.20, "And the kitchen."),
    (7, "-8%", 0.30, "Six rooms in this flat."),
    (8, "-6%", 0.24, "Six surfaces."),
    (9, "-6%", 0.18, "Six microphones."),
    (10, "-20%", 0.60, "So I keep it loud."),
    (11, "-24%", 0.34, "All night."),
]


def sh(args):
    return subprocess.run(args, capture_output=True, text=True)


def synth(text, rate, mp3):
    for _ in range(3):
        r = sh(["edge-tts", "--voice", VOICE, f"--rate={rate}", f"--pitch={PITCH}",
                "--text", text, "--write-media", str(mp3)])
        if mp3.exists() and mp3.stat().st_size > 600:
            return
        print("  retry:", r.stderr.strip()[:120])
    raise RuntimeError(f"synth failed: {text!r}")


def dur(path):
    r = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(path)])
    return float(r.stdout.strip())


def trim_bounds(path):
    """Cut edge-tts's padding: ~0.2 s lead-in, 0.7-1.1 s tail. Regex only, never field position."""
    total = dur(path)
    r = sh(["ffmpeg", "-v", "info", "-i", str(path), "-af", "silencedetect=n=-45dB:d=0.12",
            "-f", "null", "-"])
    t = r.stderr
    starts = [float(m.group(1)) for m in __import__("re").finditer(r"silence_start:\s*(-?[0-9.]+)", t)]
    ends = [float(m.group(1)) for m in __import__("re").finditer(r"silence_end:\s*(-?[0-9.]+)", t)]
    s = ends[0] if (starts and starts[0] < 0.02 and ends) else 0.0
    e = total
    if starts:
        last = max(starts)
        if last > s and (total - last) > 0.05:
            e = last
    return max(0.0, s - 0.08), min(total, e + 0.10)


def read_mono(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ar", str(SR), "-ac", "1",
                        "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def write_wav(path, x):
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def floor_noise(n, level_db=-62.0):
    """Room tone instead of digital silence between lines: silence reads as a dropout."""
    rng = np.random.default_rng(31)
    nz = rng.normal(0, 1, n).astype(np.float32)
    # gentle low-pass so it sounds like a room, not hiss
    a = math.exp(-2 * math.pi * 1200 / SR)
    y = np.empty_like(nz)
    acc = 0.0
    for i, v in enumerate(nz):
        acc = a * acc + (1 - a) * v
        y[i] = acc
    y /= (np.abs(y).max() + 1e-9)
    return y * (10 ** (level_db / 20.0))


def build_before():
    WORK.mkdir(parents=True, exist_ok=True)
    mp3 = WORK / "before.mp3"
    if not mp3.exists():
        synth(BEFORE_TEXT, BEFORE_RATE, mp3)
    s, e = trim_bounds(mp3)
    wav = OUT / "before_after_stems" / "before_15s_v07_method.wav"
    sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", str(mp3),
        "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(wav)])
    x = read_mono(wav)[:N]
    x = np.pad(x, (0, N - len(x))) if len(x) < N else x
    write_wav(wav, x)                       # exactly 15.000 s
    return {"mode": "before", "rate": BEFORE_RATE, "lines": 1, "text": BEFORE_TEXT}


def build_after():
    WORK.mkdir(parents=True, exist_ok=True)
    (OUT / "before_after_stems").mkdir(parents=True, exist_ok=True)
    bed = floor_noise(N, -64.0)
    mix = bed.copy()
    rows, cursor = [], 0.0
    for idx, rate, gap, text in AFTER_LINES:
        mp3 = WORK / f"after_{idx:02d}.mp3"
        if not mp3.exists():
            synth(text, rate, mp3)
        s, e = trim_bounds(mp3)
        tmp = WORK / f"after_{idx:02d}.wav"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", str(mp3),
            "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(tmp)])
        seg = read_mono(tmp)
        start = cursor + gap
        end = start + len(seg) / SR
        rows.append({"i": idx, "text": text, "rate": rate, "start": round(start, 3),
                     "end": round(end, 3), "dur": round(len(seg) / SR, 3), "gap_before": gap})
        i0 = int(start * SR)
        seg = seg[: max(0, min(len(seg), N - i0))]
        mix[i0:i0 + len(seg)] += seg
        cursor = end
        if cursor >= DUR - 0.2:
            break
    mix *= 0.85 / (np.abs(mix).max() + 1e-9)
    stem = OUT / "before_after_stems" / "after_line_split_reperformed.wav"
    write_wav(stem, mix)
    return {"mode": "after", "lines": rows}


def build_samples():
    """15 s of each with a low bed under it, so the comparison is heard in film conditions."""
    t = np.arange(N) / SR
    bed = (0.05 * np.sin(2 * np.pi * 55 * t) + 0.03 * np.sin(2 * np.pi * 82.5 * t + 0.6) +
           0.018 * np.sin(2 * np.pi * 110 * t + 1.2)).astype(np.float32)
    bed += floor_noise(N, -58.0) * 0.9
    for name, src in (("before_15s", "before_15s_v07_method.wav"),
                      ("after_15s", "after_line_split_reperformed.wav")):
        x = read_mono(OUT / "before_after_stems" / src)[:N]
        y = x * 0.92 + bed[:len(x)]
        y *= 0.82 / (np.abs(y).max() + 1e-9)
        write_wav(OUT / f"{name}.wav", y)
        # and an mp3 twin so it plays anywhere
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(OUT / f"{name}.wav"),
                        "-c:a", "libmp3lame", "-b:a", "192k", str(OUT / f"{name}.mp3")])


def main():
    (OUT / "before_after_stems").mkdir(parents=True, exist_ok=True)
    b = build_before()
    a = build_after()
    build_samples()
    meta = {"before": b, "after": a}
    (OUT / "ab_manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta["after"]["lines"], indent=2))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
