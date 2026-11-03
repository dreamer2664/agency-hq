#!/usr/bin/env python3
"""
measure_voice.py — the instrument behind the voice numbers in research/voices-pixel.md.

Everything the order asks for is computed here from a WAV/FLAC file and nothing else, so any
number in the report can be reproduced by anyone with the stem and this script.

Metrics
  F0 SD (semitones)   the anti-robot number. A monotone delivery has a flat one. Computed with YIN
                      (de Cheveigné & Kawahara 2002), voiced frames only, in semitones so it is
                      comparable across speakers. Reference points from the literature:
                      male read/spontaneous speech typically sits at 2.5-3.5 ST (Traunmüller &
                      Eriksson's Swedia data: 59 % of young male speakers fall in that band).
  F0 range            p5-p95 in semitones, robust to tracker outliers.
  pitch reset         mean absolute F0 jump across utterance boundaries, in semitones. Humans
                      reset pitch at the start of each thought; a single long generation does not.
  rate per line       words/second, then the coefficient of variation across lines. Global -12 %
                      gives one rate for the whole film; performance gives a spread.
  inter-line gaps     every gap between the end of one line and the start of the next: min, median,
                      mean, max, SD. A single fixed gap is the signature of stitched TTS.
  longest pre-twist   the largest gap anywhere before the turn.

Usage:  python3 measure_voice.py file.wav --lines timing.json
"""
import json
import math
import subprocess
import sys
import wave

import numpy as np

SR_TARGET = 48000
F0_MIN, F0_MAX = 70.0, 320.0
WIN = 0.040          # 40 ms analysis window
HOP = 0.010          # 10 ms hop
YIN_THRESHOLD = 0.15
SILENCE_DB = -45.0


def read_audio(path):
    """Decode anything ffmpeg understands to mono float32 at 48 kHz."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ar", str(SR_TARGET),
                        "-ac", "1", "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-400:])
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


def yin(x, sr=SR_TARGET):
    """
    YIN F0 tracker (de Cheveigné & Kawahara 2002), vectorised with an FFT autocorrelation.

    d(tau) = sum_j (x_j - x_{j+tau})^2 over a window of W samples, evaluated via
             d(tau) = e0 + e_tau - 2*r(tau), with r from FFT autocorrelation.
    Then the cumulative-mean-normalised difference picks the first dip under the threshold, with
    parabolic interpolation for sub-sample lag accuracy. Validated against pure tones before use.
    """
    n_win = int(WIN * sr)
    n_hop = int(HOP * sr)
    tau_min = max(2, int(sr / F0_MAX))
    tau_max = int(sr / F0_MIN)
    W = n_win - tau_max               # overlap region used by every lag
    n_frames = max(0, (len(x) - n_win) // n_hop)

    f0 = np.zeros(n_frames, dtype=np.float32)
    voiced = np.zeros(n_frames, dtype=bool)
    times = np.arange(n_frames) * HOP

    nfft = 1
    while nfft < n_win * 2:
        nfft *= 2

    for i in range(n_frames):
        a = x[i * n_hop: i * n_hop + n_win]
        if np.sqrt((a * a).mean()) < 1e-4:
            continue
        a = a - a.mean()

        head = a[:W]
        e0 = float((head * head).sum())
        if e0 <= 0:
            continue

        # r[tau] = sum_{j<W} head[j] * a[j+tau], computed as irfft(conj(H)*A)[tau].
        # It MUST be summed over exactly the same W samples as e0 and e_tau, otherwise
        # d(tau) = e0 + e_tau - 2r is biased and every estimate comes out sharp.
        H = np.fft.rfft(head, nfft)
        A = np.fft.rfft(a, nfft)
        r = np.fft.irfft(np.conj(H) * A, nfft)[:tau_max + 1]

        # running energy of the shifted window
        cum = np.concatenate(([0.0], np.cumsum(a * a)))
        e_tau = cum[W: W + tau_max + 1] - cum[0: tau_max + 1]

        d = np.maximum(e0 + e_tau - 2.0 * r, 0.0)
        d[0] = 0.0

        # cumulative mean normalised difference
        dsum = np.cumsum(d)
        taus = np.arange(len(d), dtype=np.float64)
        with np.errstate(divide="ignore", invalid="ignore"):
            cmnd = np.where(taus > 0, d * taus / np.maximum(dsum, 1e-12), 1.0)
        cmnd[0] = 1.0

        lo, hi = tau_min, min(tau_max, len(cmnd) - 2)
        if hi <= lo:
            continue

        # YIN step 3: take the FIRST local minimum under the threshold. d(tau) is >= 0 and deepest
        # at small lags for periodic signals, so a global argmin would always return lag~0.
        cand = None
        for tau in range(lo + 1, hi):
            if cmnd[tau] < YIN_THRESHOLD and cmnd[tau] <= cmnd[tau - 1] and cmnd[tau] <= cmnd[tau + 1]:
                while tau + 1 < hi and cmnd[tau + 1] < cmnd[tau]:
                    tau += 1
                cand = tau
                break
        if cand is None:
            # fall back to the deepest dip below a looser bound, else unvoiced
            seg = cmnd[lo:hi]
            k = int(np.argmin(seg)) + lo
            if cmnd[k] > 0.55:
                continue
            cand = k
        if not (lo < cand < hi):
            continue

        # sub-sample peak: fit a parabola to d (not cmnd — dividing by the running sum skews the
        # vertex and biases every estimate by a constant factor) and take its minimiser
        d0, d1, d2 = d[cand - 1], d[cand], d[cand + 1]
        denom = 2.0 * (d0 - 2.0 * d1 + d2)
        shift = (d0 - d2) / denom if abs(denom) > 1e-12 else 0.0
        shift = float(np.clip(shift, -0.5, 0.5))

        f0[i] = sr / (cand + shift)
        voiced[i] = True

    return f0, voiced, times


def rms_db(x):
    return 20 * math.log10(max(1e-9, float(np.sqrt((x ** 2).mean()))))


def describe(v):
    v = np.asarray(v, dtype=float)
    if len(v) == 0:
        return dict(n=0)
    return dict(n=int(len(v)), min=round(float(v.min()), 3), p25=round(float(np.percentile(v, 25)), 3),
                median=round(float(np.median(v)), 3), mean=round(float(v.mean()), 3),
                p75=round(float(np.percentile(v, 75)), 3), max=round(float(v.max()), 3),
                sd=round(float(v.std(ddof=1)) if len(v) > 1 else 0.0, 3))


def measure(path, lines=None, twist_index=None):
    x = read_audio(path)
    dur = len(x) / SR_TARGET

    f0, voiced, times = yin(x)
    # gate: only frames that are voiced AND above the silence floor
    frame_db = np.array([rms_db(x[int(t * SR_TARGET): int(t * SR_TARGET) + int(WIN * SR_TARGET)])
                         for t in times]) if len(times) else np.array([])
    keep = voiced & (frame_db > SILENCE_DB)
    f_keep = f0[keep]
    f_keep = f_keep[(f_keep > F0_MIN) & (f_keep < F0_MAX)]

    st = 12.0 * np.log2(f_keep / 100.0) if len(f_keep) else np.array([])
    out = {
        "file": str(path),
        "duration_s": round(dur, 4),
        "voiced_frames": int(keep.sum()),
        "f0_hz": dict(median=round(float(np.median(f_keep)), 2) if len(f_keep) else None,
                      mean=round(float(f_keep.mean()), 2) if len(f_keep) else None),
        "f0_sd_semitones": round(float(st.std(ddof=1)), 3) if len(st) > 1 else None,
        "f0_range_p5_p95_st": round(float(np.percentile(st, 95) - np.percentile(st, 5)), 3) if len(st) else None,
    }

    if lines:
        with open(lines) as f:
            meta = json.load(f)
        rows = meta["lines"] if isinstance(meta, dict) else meta
        starts = [r["start"] for r in rows]
        ends = [r["end"] for r in rows]

        # gaps between consecutive lines
        gaps = [round(starts[i + 1] - ends[i], 3) for i in range(len(rows) - 1)]
        out["lines"] = len(rows)
        out["inter_line_gaps"] = describe(gaps)

        # rate per line: words per second inside that line's own speech span
        rates = []
        for r in rows:
            nw = len(r["text"].split())
            span = r["end"] - r["start"]
            rates.append(round(nw / span, 3) if span > 0 else 0.0)
        out["rate_wps"] = describe(rates)
        out["rate_cv"] = round(float(np.std(rates, ddof=1) / np.mean(rates)), 3) if len(rates) > 1 else None

        # pitch reset across utterance boundaries: F0 at the first voiced frame of a line minus
        # F0 at the last voiced frame of the previous line, in semitones. Human speech resets the
        # pitch contour at each new thought; a single long generation does not.
        def last_voiced(end_t, back=0.30):
            i = int(end_t / HOP)
            j = max(0, int((end_t - back) / HOP))
            for k in range(i, j - 1, -1):
                if 0 <= k < len(f0) and voiced[k]:
                    return float(f0[k])
            return None

        def first_voiced(start_t, fwd=0.20):
            i = int(start_t / HOP)
            j = min(len(f0), int((start_t + fwd) / HOP))
            for k in range(max(0, i), j):
                if voiced[k]:
                    return float(f0[k])
            return None

        jumps = []
        for i in range(len(rows) - 1):
            fa = last_voiced(ends[i])
            fb = first_voiced(starts[i + 1])
            if fa and fb and fa > 0 and fb > 0:
                jumps.append(abs(12 * math.log2(fb / fa)))
        out["pitch_reset_st"] = describe(jumps)

        ti = twist_index if twist_index is not None else max(range(len(rows)),
                                                            key=lambda k: starts[k] if k else 0)
        out["pre_twist_gap_s"] = round(starts[ti] - ends[ti - 1], 3) if ti > 0 else None
        out["longest_gap_s"] = max(gaps) if gaps else None

    return out


if __name__ == "__main__":
    path = sys.argv[1]
    lines = None
    twist = None
    if "--lines" in sys.argv:
        lines = sys.argv[sys.argv.index("--lines") + 1]
    if "--twist" in sys.argv:
        twist = int(sys.argv[sys.argv.index("--twist") + 1]) - 1   # CLI takes 1-based line numbers
    print(json.dumps(measure(path, lines, twist), indent=2))
