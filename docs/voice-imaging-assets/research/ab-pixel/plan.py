#!/usr/bin/env python3
"""
plan.py — solve the v07 after-script so it lands inside a 60.000 s film.

The trap this avoids: you cannot space a script by feel and then discover it overruns,
because every re-spacing costs a full re-synthesis and lands somewhere new. Instead,
synthesise each line ONCE, then solve for the rates that make the whole thing fit while
keeping the per-line rate *relationships* that carry the performance (the twist cluster
stays the slowest part of the film).

    python3 plan.py              # fit rates, build the stem, print the timing
    python3 plan.py --measure    # ...and the metrics table
"""
import hashlib, json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESEARCH = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RESEARCH, "tools"))
from measure_voice import yin, read_audio  # noqa: E402

SR, DUR = 48000, 60.0
N = int(DUR * SR)
VOICE = "en-US-ChristopherNeural"
HARD_END = 59.30
STEMS = os.path.join(HERE, "v07_stems")
CACHE = os.path.join(HERE, "work_v07")

# ---------------------------------------------------------------------------
# BEFORE — reproduced from pixel/v07 assets/voice.py: 20 lines, one global rate,
# absolute start times. This is the method the Director heard.
# ---------------------------------------------------------------------------
V07 = [
    (1, 0.60, "Night two, two fourteen again."),
    (2, 4.40, "Same flat, same speaker, nothing changed."),
    (3, 7.00, "Except the walls."),
    (4, 8.50, "And the door."),
    (5, 9.80, "And the kitchen."),
    (6, 11.20, "Six rooms in this flat."),
    (7, 13.70, "Six surfaces, six microphones."),
    (8, 16.20, "So I keep it loud, all night."),
    (9, 18.50, "The radio stays on."),
    (10, 20.00, "The kettle, twice an hour."),
    (11, 21.50, "A towel under the door."),
    (12, 24.20, "It isn't listening with a microphone any more."),
    (13, 27.40, "There are seven surfaces now."),
    (14, 30.20, "I stopped making noise."),        # the twist
    (15, 32.80, "And the flat went quiet."),
    (16, 35.60, "And it was still listening."),
    (17, 46.20, "It heard the quiet."),
    (18, 49.60, "And the quiet was in the hall."),
    (19, 52.40, "Night two is over."),
    (20, 55.60, "Tomorrow, the quiet answers."),
]

# ---------------------------------------------------------------------------
# AFTER — same 96 words, 25 lines, one idea per line. `gap` is the beat before the
# line; `r` is the rate the performance wants (the solver may shift the whole set but
# keeps these relationships intact).
# ---------------------------------------------------------------------------
AFTER = [
    # i,  gap,  rate,  pitch,   text
    (1,  0.85, "-14%", "+2Hz",  "Night two."),
    (2,  0.30, "-14%", "-2Hz",  "Two fourteen, again."),
    (3,  0.32, "-16%", "-4Hz",  "Same flat."),
    (4,  0.20, "-16%", "-6Hz",  "Same speaker."),
    (5,  0.34, "-18%", "-8Hz",  "Nothing's changed."),
    (6,  0.26, "-18%", "-10Hz", "Except the walls."),
    (7,  0.20, "-16%", "-12Hz", "And the door."),
    (8,  0.20, "-16%", "-14Hz", "And the kitchen."),
    (9,  0.36, "-12%", "-3Hz",  "Six rooms in this flat."),
    (10, 0.22, "-10%", "+5Hz",  "Six surfaces."),
    (11, 0.20, "-10%", "+7Hz",  "Six microphones."),
    (12, 0.46, "-20%", "-7Hz",  "So I keep it loud."),
    (13, 0.24, "-26%", "-11Hz", "All night."),
    (14, 0.42, "-18%", "+1Hz",  "The radio stays on."),
    (15, 0.28, "-16%", "-3Hz",  "The kettle, twice an hour."),
    (16, 0.28, "-18%", "-6Hz",  "A towel under the door."),
    (17, 0.60, "-16%", "-8Hz",  "It's not listening with a microphone any more."),
    (18, 0.48, "-12%", "-5Hz",  "There are seven surfaces now."),
    (19, 1.30, "-28%", "-16Hz", "I stopped making noise."),      # <- the twist
    (20, 0.65, "-30%", "-18Hz", "And the flat went quiet."),
    (21, 0.55, "-28%", "-20Hz", "And it was still listening."),
    (22, 1.05, "-24%", "-14Hz", "It heard the quiet."),
    (23, 0.45, "-18%", "-10Hz", "And the quiet was in the hall."),
    (24, 0.75, "-20%", "-8Hz",  "Night two is over."),
    (25, 0.55, "-22%", "-10Hz", "Tomorrow, the quiet answers."),
]
TWIST = 19


def synth(text, rate, pitch, out):
    for _ in range(3):
        subprocess.run(["edge-tts", "--voice", VOICE, f"--rate={rate}", f"--pitch={pitch}",
                        "--text", text, "--write-media", out],
                       capture_output=True, text=True)
        if os.path.exists(out) and os.path.getsize(out) > 600:
            return
    raise RuntimeError(f"edge-tts failed: {text}")


def trim(x, thr_db=-42.0, keep=0.04):
    """edge-tts pads 0.3-0.5 s of tail silence onto every clip. Left in, it is counted
    twice — once as speech, once as the designed gap — and the film mysteriously overruns."""
    hop = int(0.005 * SR)
    n = len(x) // hop
    if n == 0:
        return x
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1)) + 1e-12)
    above = np.flatnonzero(db > thr_db)
    if above.size == 0:
        return x
    return x[max(0, int(above[0] * hop - keep * SR)):min(len(x), int((above[-1] + 1) * hop + keep * SR))]


def line_wav(idx, text, rate, pitch, tag):
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.sha1(f"{VOICE}|{rate}|{pitch}|{text}".encode()).hexdigest()[:12]
    path = os.path.join(CACHE, f"{tag}_{idx:02d}_{key}.wav")
    if not (os.path.exists(path) and os.path.getsize(path) > 2000):
        mp3 = path[:-4] + ".mp3"
        synth(text, rate, pitch, mp3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ar", str(SR), "-ac", "1",
                        "-c:a", "pcm_s16le", path], capture_output=True)
    with wave.open(path) as w:
        return trim(np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0)


def rates_for(items, offset):
    """Apply an integer percent offset to a rate string, clamped to a plausible band."""
    out = []
    for it in items:
        v = int(it[2].rstrip("%")) + offset
        v = max(-32, min(12, v))
        out.append(f"{v:+d}%")
    return out


def plan_and_build(mode, offset=0, gscale=1.0):
    items = V07 if mode == "before" else AFTER
    rows, segs = [], []
    if mode == "before":
        for idx, target, text in items:
            segs.append((idx, target, text, "-12%", "-4Hz", line_wav(idx, text, "-12%", "-4Hz", "b")))
    else:
        rs = rates_for(items, offset)
        gaps = shaped_gaps(gscale)
        for (idx, _gap, _r, pitch, text), rate, gap in zip(items, rs, gaps):
            segs.append((idx, gap, text, rate, pitch, line_wav(idx, text, rate, pitch, "a")))
    mix = np.zeros(N, np.float32)
    cursor = 0.0
    for idx, place, text, rate, pitch, seg in segs:
        start = max(place, cursor + 0.06) if mode == "before" else cursor + place
        end = start + len(seg) / SR
        if end > HARD_END:
            print(f"  WARN {mode} line {idx} ends {end:.2f}")
        rows.append({"i": idx, "text": text, "rate": rate, "pitch": pitch,
                     "start": round(start, 3), "end": round(end, 3),
                     "gap": round(start - cursor, 3)})
        i0 = int(start * SR)
        s = seg[:max(0, min(len(seg), N - i0))]
        mix[i0:i0 + len(s)] += s
        cursor = end
    mix *= 0.9 / (np.abs(mix).max() + 1e-9)
    os.makedirs(STEMS, exist_ok=True)
    p = os.path.join(STEMS, f"{mode}_v07_narration.wav")
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    json.dump({"lines": rows, "offset_pct": offset, "gap_scale": round(gscale, 3), "hard_end": HARD_END},
              open(os.path.join(STEMS, f"{mode}_timing.json"), "w"), indent=2)
    return rows, p


GAP_ALPHA = 1.6      # >1 sharpens the contrast: list beats stay short, pivots get long
GAP_REF = 0.20


def shaped_gaps(k, leader=1.00):
    """g -> k * (g/GAP_REF)**alpha. A uniform stretch of every gap makes each beat
    equally slow, which is its own kind of mechanical. This keeps the short beats short
    and gives the long beats the room, so the film has a rhythm instead of a tempo."""
    gaps = [k * (g / GAP_REF) ** GAP_ALPHA for _i, g, _r, _p, _t in AFTER]
    gaps[0] = min(gaps[0], leader)      # a 1.8 s cold open is a hold, not a beat
    return gaps


def solve_scale(target=58.0):
    speech = sum(len(line_wav(i, t, r, pz, "a")) / SR for i, _g, r, pz, t in AFTER)
    unit = sum((g / GAP_REF) ** GAP_ALPHA for _i, g, _r, _p, _t in AFTER)
    k = max(0.05, (target - speech) / unit)
    return k, speech, unit


def measure(rows, p, twist):
    x = read_audio(p)
    f0, voiced, _t = yin(x)
    f0 = f0[voiced]
    f0 = f0[(f0 > 70) & (f0 < 400)]
    st = 39.86 * np.log10(f0 / 100.0)
    gaps = [rows[i]["start"] - rows[i - 1]["end"] for i in range(1, len(rows))]
    rates = [len(r["text"].split()) / max(1e-6, r["end"] - r["start"]) for r in rows]
    prev_end = rows[twist - 2]["end"] if twist > 1 else 0.0
    return {
        "lines": len(rows),
        "words": sum(len(r["text"].split()) for r in rows),
        "speech_s": round(sum(r["end"] - r["start"] for r in rows), 2),
        "last_word_s": round(rows[-1]["end"], 2),
        "f0_sd_st": round(float(st.std(ddof=1)), 3),
        "f0_median_hz": round(float(np.median(f0)), 2),
        "f0_p5_st": round(float(np.percentile(st, 5)), 2),
        "f0_p95_st": round(float(np.percentile(st, 95)), 2),
        "gap_n": len(gaps), "gap_min": round(min(gaps), 3),
        "gap_median": round(float(np.median(gaps)), 3),
        "gap_mean": round(float(np.mean(gaps)), 3),
        "gap_max": round(max(gaps), 3),
        "gap_sd": round(float(np.std(gaps, ddof=1)), 3),
        "rate_cv": round(float(np.std(rates, ddof=1) / np.mean(rates)), 3),
        "rate_min": round(min(rates), 2), "rate_max": round(max(rates), 2),
        "pause_before_twist_s": round(rows[twist - 1]["start"] - prev_end, 3),
    }


if __name__ == "__main__":
    k, speech, unit = solve_scale()
    gaps = shaped_gaps(k)
    print(f"solver: speech {speech:.2f}s, gaps {sum(gaps):.2f}s "
          f"(min {min(gaps):.2f} max {max(gaps):.2f}) -> last word {speech + sum(gaps):.2f}s")
    out = {}
    for mode, tw in (("before", 14), ("after", TWIST)):
        rows, p = plan_and_build(mode, 0, k if mode == "after" else 1.0)
        out[mode] = measure(rows, p, tw)
        print(f"{mode}: {out[mode]['lines']} lines, {out[mode]['words']} words, "
              f"speech {out[mode]['speech_s']}s, last word {out[mode]['last_word_s']}s -> {p}")
    json.dump(out, open(os.path.join(HERE, "v07_metrics.json"), "w"), indent=2)
    print()
    print(f"{'metric':<24}{'BEFORE':>12}{'AFTER':>12}")
    for k in out["before"]:
        print(f"{k:<24}{str(out['before'][k]):>12}{str(out['after'][k]):>12}")
