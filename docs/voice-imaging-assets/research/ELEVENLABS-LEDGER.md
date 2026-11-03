# ELEVENLABS API LEDGER — all agents, shared 70,000-character monthly pool

Keys are never recorded here. One section per agent per round.

---

## reel

# ElevenLabs API ledger — reel voice research

Round limit: **1,200 text characters maximum**. Reserve characters before each POST and count every attempted synthesis against the limit, even if the server result is ambiguous. No credentials belong in this file. The benchmark passage is `ab-reel/benchmark.txt`.

| UTC | Request | Characters reserved | Status | Notes |
|---|---|---:|---|---|
| 2026-11-01T14:38:44+00:00 | GET `/v1/voices` | 0 | 200 | Discover an available premade reference voice. |
| 2026-11-01T14:39:18+00:00 | POST `/v1/text-to-speech/{voice_id}/with-timestamps` | 201 | 200 | One benchmark passage, model `eleven_multilingual_v2`, premade male Roger; the reservation is counted even if the outcome is unknown. |

**Total reserved this round: 201 / 1,200.** Account monthly usage is shared with others and is not assumed to be exclusively available to this experiment.

---

## grade

# ElevenLabs API Character Ledger

Shared accounting ledger for division ElevenLabs TTS synthesis calls (`70,000` characters/month division pool across 7 keys; `10,000` characters/month per key; `1,200`-character cap for the Wave-6 voice quality research order).

> **Security rule:** Never commit, log, or paste API keys (`sk_...`) anywhere in this repository, commit messages, or PR descriptions. All benchmark outputs are committed under `research/ab-grade/audio/` so `python3 research/build_ab_benchmark.py` runs **100% offline at `0` character cost**.

## Call Log

| Date (UTC) | Agent | Model | Characters | Voice (`voice_id`) | Request ID | Purpose |
| :--- | :--- | :--- | ---: | :--- | :--- | :--- |
| `2026-11-01` | `grade` | `n/a (GET /v1/user/subscription)` | `0` | `n/a` | `metadata` | Pre-experiment character quota check (`0 / 10,000` initial). |
| `2026-11-01` | `grade` | `n/a (GET /v1/voices)` | `0` | `n/a` | `metadata` | Enumerate premade deep male documentary voices (`Brian`, `Bill`, `Daniel`, `Roger`). |
| `2026-11-01` | `grade` | `eleven_multilingual_v2` | `191` | `Brian` (`nPczCjzI2devNBz1zQrb`) | `JOVRzJfD6WGGAzH8xogy` | High-stability A/B control (`stability=0.78, similarity_boost=0.75, style=0.00, speed=0.90, seed=20261101`) on exact 3 `v07` (*MARK SIX*) narration sentences (`Turn 06 + Turn 09 + Turn 12`). Saved to `research/ab-grade/audio/sources/el_v2_brian_highstab.mp3`. |
| `2026-11-01` | `grade` | `eleven_multilingual_v2` | `191` | `Brian` (`nPczCjzI2devNBz1zQrb`) | `EqSN1MlTZX2lENRQIykF` | Primary expressive baritone A/B test (`stability=0.35, similarity_boost=0.78, style=0.18, speed=0.89, seed=20261101`) on the identical 191-character 3-sentence `v07` script against local `edge-tts` + `vocal_chain.py`. Saved to `research/ab-grade/audio/sources/el_v2_brian_expressive.mp3`. |
| `2026-11-01` | `grade` | `eleven_multilingual_v2` | `194` | `Bill` (`pqHfZKP75CvOlQylNhV4`) | `4aNBHrVTgYzSLFKfRc7J` | Weathered documentary timbre + punctuation-directed pause test (`stability=0.38, similarity_boost=0.80, style=0.15, speed=0.88, seed=20261101`) on the same 3 `v07` sentences with ellipsis (`...`) and em-dash (`—`) clause cues. Saved to `research/ab-grade/audio/sources/el_v2_bill_documentary.mp3`. |
| `2026-11-01` | `grade` | `n/a (GET /v1/user/subscription)` | `0` | `n/a` | `metadata` | Post-experiment server verification (`576 / 10,000` cumulative billed). |

## Round Summary (`grade` · `grade/voice-imaging`)

- **Total paid TTS API calls:** `3` (plus `0`-character metadata checks to `GET /v1/voices` and `GET /v1/user/subscription`)
- **Total characters billed (verified via `character-cost` header & `/v1/user/subscription`):** **`576 / 1,200`** (`48.0%` of round cap; `624` characters unspent)
- **Remaining monthly balance on assigned key:** **`9,424 / 10,000`** characters

---

## pixel

# ElevenLabs ledger — pixel voice+imaging research

Round cap: **1,200 characters**. Key never written to this repo, any document, any PR, or any
prompt: passed as an environment variable inside a single shell invocation, read with
`os.environ`, and discarded when the process exits. There is no `.env`, no config file, no CI
secret. Both calls below were made in one `python3` process from that environment.

Test design: the v07 script, re-written under the writing rules in `research/voices-pixel.md`
(25 lines, 96 words), delivered two ways through **one API call each** so the two are directly
comparable. Voice: premade **Daniel** (`onwK4e9ZLuTAKqWW03F9`), model `eleven_multilingual_v2`,
settings identical across both conditions: `stability=0.45, similarity_boost=0.75, style=0.00,
use_speaker_boost=true`.

| Date (UTC) | Agent | Model | Voice | Characters | Request ID | Purpose | Outcome |
| :--- | :--- | :--- | :--- | ---: | :--- | :--- | :--- |
| `2026-11-01` | `pixel` | `eleven_multilingual_v2` | Daniel (`onwK4e9ZLuTAKqWW03F9`) | `533` | `rXtAN21mBne1bDjwuADy` | Condition 1 — the 25-line script as **one uninterrupted block**, no line breaks. | `200` · 671,285 bytes · 41.89 s · `research/ab-pixel/elevenlabs/el_block.mp3` |
| `2026-11-01` | `pixel` | `eleven_multilingual_v2` | Daniel (`onwK4e9ZLuTAKqWW03F9`) | `557` | `zIPZkk6PPMD3o3h2pGV1` | Condition 2 — the same 25 lines, one per line with double newlines, **one call**. | `200` · 669,195 bytes · 41.75 s · `research/ab-pixel/elevenlabs/el_split.mp3` |

## Round Summary (`pixel` · `pixel/voice-imaging`)

- **Paid TTS calls:** `2`. **Characters billed: `1,090 / 1,200`** (90.8 % of round cap; `110` unspent).
- **Remaining monthly balance on this key: `8,910 / 10,000`.**
- Both outputs committed under `research/ab-pixel/elevenlabs/` so measurement re-runs offline at
  **zero character cost**.

## What the cap bought, and what it did not

**Tested:** one call with the script as a block versus one call with 25 newline-separated lines.
This is the *weaker* form of splitting — the model still plans prosody across the whole request.

**Not tested:** 25 **separate synthesis calls** placed on a timeline with designed gaps, which is
the direct parallel to the local-model test and the thing that would actually answer the question.
That costs a further `509` characters: `533 + 557 + 509 = 1,599`, over the cap. The cap bought two
comparable conditions instead of three. **The three-way comparison is item one next round**
(`509` chars, leaves `8,910` of the monthly allowance).

## Measured result

| condition | duration | F0 SD | F0 median | pauses >= 0.15 s | median pause | longest pause |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| block (1 call) | 41.89 s | **4.349 ST** | 132.8 Hz | 29 | 0.50 s | 0.85 s |
| newline-split (1 call) | 41.75 s | **4.913 ST** | 133.6 Hz | 31 | 0.47 s | 0.73 s |

1. **The only condition in this whole investigation where splitting raised F0 SD** (+0.564 ST,
   +13 %). On the local model it did nothing (`4.079 -> 3.779` ST) and even cost a little.
2. **The premium model does not need line breaks to produce pauses** — 29 pauses >= 0.15 s with a
   0.50 s median from an uninterrupted block, against the local model's **seven 0.06 s joins** on
   the same script. The difference is not abstract quality: the premium model **paces itself**.
3. **Newline hints bought no extra pause and shortened the longest one** (0.85 -> 0.73 s). If the
   film needs a 3.6 s hold before the twist, no number of newlines produces it. Only separate
   calls on a timeline do.

**Conclusion:** for a premium model, line splitting is a **control** technique (exact gap
placement, re-rolling one line without re-paying for the film, a deterministic timeline), not an
**expressiveness** one. The expressiveness is already in the model. For the local model it is both.

Both stems are reference listens only — 41.9 s of speech with no designed gaps and no timeline, so
neither is a candidate for a film. They answer one question: does splitting help a premium model as
much as the local one? For pauses, no. For pitch variance, slightly.
