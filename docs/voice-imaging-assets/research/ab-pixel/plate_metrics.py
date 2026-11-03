#!/usr/bin/env python3
"""
plate_metrics.py — measure what makes a generated plate read as a photograph.

Three numbers per plate, on the 1920x1080 film frame:

  laplacian_var   Var(Laplacian(luma)) on 0-255 luma. The standard focus/acuity measure.
                  It rewards real texture and punishes soft mush — but it is scale- and
                  content-dependent, so it is only comparable between plates of the same
                  scene, which is exactly how it is used here.
  contrast_sd     Standard deviation of luma, 0-255. The spread of the tonal range.
  lit_unlit       Fraction of the frame above 10 % of full scale (25.5/255), and the ratio.
                  This is the composition measure that matters for night plates: how much
                  of a dark frame is actually lit, and how much is allowed to be black.

    python3 plate_metrics.py
"""
import json, os
import numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view

HERE = os.path.dirname(os.path.abspath(__file__))
K = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], np.float32)
LIT_THRESHOLD = 25.5          # 10 % of full scale


def metrics(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im, dtype=np.float64)
    luma = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]      # 0-255
    lap = (sliding_window_view(luma, (3, 3)) * K).sum(axis=(-1, -2))
    lit = float((luma > LIT_THRESHOLD).mean())
    return {
        "size": f"{im.size[0]}x{im.size[1]}",
        "laplacian_var": round(float(lap.var()), 1),
        "contrast_sd": round(float(luma.std()), 1),
        "mean_luma": round(float(luma.mean()), 1),
        "lit_pct": round(lit * 100, 1),
        "unlit_pct": round((1 - lit) * 100, 1),
        "lit_unlit_ratio": round(lit / max(1 - lit, 1e-6), 3),
    }


def main():
    out = {}
    for d in ("plates_before", "plates_after"):
        out[d] = {}
        for f in sorted(os.listdir(os.path.join(HERE, d))):
            if f.endswith(".png"):
                out[d][f] = metrics(os.path.join(HERE, d, f))
    json.dump(out, open(os.path.join(HERE, "plate_metrics.json"), "w"), indent=2)

    hdr = f"{'plate':<20}{'lapvar':>9}{'contrast':>10}{'mean':>7}{'lit%':>7}{'L:U':>7}"
    for d in ("plates_before", "plates_after"):
        print("\n" + d)
        print(hdr)
        for f, m in out[d].items():
            print(f"{f:<20}{m['laplacian_var']:>9}{m['contrast_sd']:>10}"
                  f"{m['mean_luma']:>7}{m['lit_pct']:>7}{m['lit_unlit_ratio']:>7}")

    print("\nchange (after vs before)")
    for f in out["plates_before"]:
        b, a = out["plates_before"][f], out["plates_after"][f]
        print(f"  {f:<20} lapvar x{a['laplacian_var'] / b['laplacian_var']:.2f}"
              f"   contrast {a['contrast_sd'] - b['contrast_sd']:+.1f}"
              f"   mean {a['mean_luma'] - b['mean_luma']:+.1f}"
              f"   L:U {b['lit_unlit_ratio']:.2f} -> {a['lit_unlit_ratio']:.2f}")


if __name__ == "__main__":
    main()
