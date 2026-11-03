# Pixel: voice and imaging research

Original measured research recovered from commit `b328e489e91b148573ae830b9320f6523e77ae6e`. Supporting audio, timing data, scripts, plate pairs and the research ledger are preserved in [voice-imaging-assets/research](voice-imaging-assets/research/). The native-resolution plate generations are not included in this HQ copy; the 1920×1080 measured plates are included. Internal paths in the original notes refer to the original video-division repository layout.

No human listening test was conducted as part of this measurement. Pitch, timing and image statistics cannot establish perceived quality. ElevenLabs usage was 1,090 characters; no new calls were made for this delivery.

---

# voices-pixel.md — why the narration sounded like a robot, and what I can actually prove

**Author:** pixel · **Branch:** `pixel/voice-imaging` · **Date:** 2026-11-01
**Trigger:** the Director's verdict on the v07/v09 narration — *"The voices are just horrible. Sounds like a robot talking."*

Everything below is measured. Where a measurement showed no improvement I say so, because a
research note that only reports wins is worth nothing on the second read.

---

## 0. The short version

The Director heard something real, but it was not what I assumed. It was **not** a flat, monotone
voice. Both stems are already *more* pitch-variable than the human norm for read speech.

What he heard was a voice with **no rests and no turn-taking**: a line delivered, then the next
line immediately on top of it, with the same fixed beat every time. Lip-sync-through-the-whole-film
delivery. That is a timing defect, and I can measure it and fix it. It is not a "liveliness"
defect, and I cannot manufacture liveliness by splitting lines.

| metric | v07 method (before) | line-split re-performance (after) | verdict |
|---|---|---|---|
| lines | 20 | 25 | +5 break points |
| words | 96 | 96 | same script |
| speech, s | 35.50 | 37.97 | **+2.47 s of pure split overhead** |
| last word, s | 57.77 | 57.16 | both fit 60.000 s |
| **F0 SD, semitones** | **3.939** | **3.779** | **no improvement — actually 0.16 ST worse** |
| F0 p5–p95 range, ST | 12.688 | 12.558 | no improvement |
| inter-line gaps, n | 19 | 24 | — |
| gaps sitting on the 0.06 s floor | **7 of 19** | **0 of 24** | the robot tell |
| gap median / max, s | 0.685 / 9.20 | 0.445 / 3.63 | — |
| gap SD, s | 2.060 | 0.822 | a *designed* beat, not a script accident |
| distinct gap values | 13 of 19 | 20 of 25 | — |
| rate CV (words/s across lines) | 0.253 | 0.293 | +16 % more rate range |
| **pause before the twist** | **0.975 s** | **3.630 s** | **the change he will actually hear** |
| longest gap in the film | 9.20 s (a hole) | 3.63 s (the twist hold) | the hole is a bug, see §5 |

**The claim I am willing to defend:** line splitting is a **timing and turn-taking** intervention.
It buys designed rests, a real held beat before the turn, and more rate range. It does **not**
raise F0 variance, and anyone who measures only F0 SD will correctly report that it did nothing.

---

## 1. What the sources actually say

### 1.1 Writing for synthetic speech

The engines do not interpret; they perform punctuation. A comma is a breath, a period is a stop,
and a subordinate clause placed before its main clause makes the model guess the shape of the
sentence before it has enough information to know.

- **Write like a speaker, not like a document.** Fragments are fine. Contractions are mandatory —
  "it isn't" is one gesture, "it is not" is three. No leading subordinate clauses. Keep sentences
  under 25 words. Punctuation exists for the narrator, not for the reader. [1]
- **Punctuation as a performance script.** A period, comma or ellipsis is a timing instruction;
  commas want roughly 100–300 ms, a topic change 400–600 ms. Vary sentence length or the delivery
  locks into one gear. Numerals and abbreviations must be written out in spoken form. [2]
- **Phrase breaks with real durations:** 120–300 ms between phrases, 400–700 ms for a dramatic
  break. Cap a sentence at two independent clauses. Run-on sentences make the engine **rush and
  merge clauses** — which is exactly the "delivery" tell. [3]
- **Vary sentence length for pace, periods to separate thoughts, spoken-form numbers**, and keep
  each utterance to one idea. [4]

What the v07 script did wrong against all four: `"Same flat, same speaker, nothing changed."` is
three ideas and two commas in one breath; `"So I keep it loud, all night."` fuses a statement to
its qualifier; and `"Night two, two fourteen again."` is a time and a date run together. Each one
is a place where the model has to invent a shape.

### 1.2 Line splitting — one synthesis call per line

This is the core technique, and the sources are unusually consistent about it.

- **Chunk to one or two sentences before synthesis.** Long paragraphs degrade prosody because the
  model loses context across them. The documented pitfall is *stitching artefacts* when the silence
  between chunks is not handled deliberately. [5]
- **For anything over a paragraph, synthesise sentence by sentence** and assemble with deliberate
  silences. You get consistent prosody, the ability to re-roll one bad line without re-doing the
  film, and **exact control of every pause**. The result is "edited rather than recited". Long
  passages lose track of where the emphasis belongs, because prosody is predicted over a limited
  window. [6]
- **Gaps must differ by function.** Continuation 150–250 ms, topic shift 400–600 ms, longer after
  complex material; always split on semantic boundaries, never mid-clause. **Concatenating
  identical gaps is the uncanny valley.** [7]
- **SSML is not an option.** ElevenLabs' own docs state that the current models do not support
  `<break>` tags and that too many breaks cause instability — pause has to come from text
  structure. Separate calls are therefore the *only* reliable way to pace these models. [8]

That last point settles a design question in advance: I cannot buy pacing by inserting break tags
into one long request. The film has to be built line by line.

### 1.3 Rate variation as a performance, not a setting

v07 applied `--rate=-12%` to all twenty lines. That is a tempo, not a performance: every line
moves at the same speed for the same reason, so the listener hears one gear. The guidance above is
consistent that pace should follow the material — faster inside a list, slower on the reveal, and
slowest on the last line of a section. [3][6]

I also measured this, and it is weaker than I expected: **rate CV rose only from 0.253 to 0.293**.
So rate variation is real but modest, and it is not the thing that fixes the robot problem on its
own. It works *with* the gaps, not instead of them.

### 1.4 The anti-robot number, and its limit

F0 standard deviation in semitones is the standard liveliness metric: it significantly predicts
listener-rated expressiveness (β = 3.62, p < 0.001), with σ in semitones computed as
σ_ST = 39.86 · log10((E + σ)/E). [9] Normalised F0 SD is used as the liveliness measure in speech
technology, computed over a moving window with a log transform for cross-speaker comparison, and
monotone delivery is documented as both disliked and harmful to recall. [10][11] For forensic
benchmarking, normative male read speech sits around **σ ≈ 15–25 Hz, with 59 % of speakers between
2.5 and 3.5 semitones**. [12]

**My stems measure 3.94 and 3.78 semitones.** Both are *above* the normative band. The v07 voice
was never monotone, and reporting "we made it less monotone" would be a fabricated win. The metric
that describes what actually went wrong is not F0 SD at all. It is the gap distribution.

---

## 2. The instrument

`research/tools/measure_voice.py` — YIN pitch tracker (de Cheveigné & Kawahara 2002) with an FFT
autocorrelation, the first-local-minimum rule from YIN step 3, and parabolic interpolation on the
difference function.

```bash
python3 tools/measure_voice.py ab-pixel/v07_stems/after_v07_narration.wav \
        --lines ab-pixel/v07_stems/after_timing.json --twist 19
```

- **Validation:** exact to **0.00 Hz** on synthetic tones at 85, 98, 110, 147, 175, 220 and 260 Hz.
  110 Hz with added noise measures within 0.172 semitones. Three bugs were found and fixed before
  any result in this document was trusted.
- Reports: F0 SD in semitones, F0 p5–p95 range, pitch reset across each line boundary, inter-line
  gap distribution, per-line rate and rate CV, and the pause before a given line.
- `--twist N` takes a **1-based** line number (the CLI converts; `measure()` itself is 0-based).
  This cost me a wrong reading once: the reported "pause before the twist" was measuring the line
  *after* the twist. Verify the line you are pointing at, not just the number.

---

## 3. The before / after, written out

Same story, same 96 words, same twist. The difference is where the breaks are and what the paces are.

### 3.1 Before — the v07 method

One global rate, one global pitch, absolute start times typed around the previous delivery.

```python
V07 = [
    (1,  0.60, "Night two, two fourteen again."),
    (2,  4.40, "Same flat, same speaker, nothing changed."),
    (3,  7.00, "Except the walls."),
    (4,  8.50, "And the door."),
    (5,  9.80, "And the kitchen."),
    (6, 11.20, "Six rooms in this flat."),
    (7, 13.70, "Six surfaces, six microphones."),
    (8, 16.20, "So I keep it loud, all night."),
    (9, 18.50, "The radio stays on."),
    (10,20.00, "The kettle, twice an hour."),
    (11,21.50, "A towel under the door."),
    (12,24.20, "It isn't listening with a microphone any more."),
    (13,27.40, "There are seven surfaces now."),
    (14,30.20, "I stopped making noise."),      # the twist
    (15,32.80, "And the flat went quiet."),
    (16,35.60, "And it was still listening."),
    (17,46.20, "It heard the quiet."),
    (18,49.60, "And the quiet was in the hall."),
    (19,52.40, "Night two is over."),
    (20,55.60, "Tomorrow, the quiet answers."),
]
RATE, PITCH = "-12%", "-4Hz"        # every line, no exceptions
```

Note column 2: these are *absolute start times*, so if a line runs long, the next line is pushed
and the schedule silently drifts. Seven of the nineteen gaps ended up **0.06 s** — the packer's
minimum — because the previous line had already eaten the space. That is the robot: not the pitch,
the fact that the film never takes a breath.

### 3.2 After — one idea per line, a designed beat before each

```python
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
    (19, 1.30, "-28%", "-16Hz", "I stopped making noise."),      # the twist
    (20, 0.65, "-30%", "-18Hz", "And the flat went quiet."),
    (21, 0.55, "-28%", "-20Hz", "And it was still listening."),
    (22, 1.05, "-24%", "-14Hz", "It heard the quiet."),
    (23, 0.45, "-18%", "-10Hz", "And the quiet was in the hall."),
    (24, 0.75, "-20%", "-8Hz",  "Night two is over."),
    (25, 0.55, "-22%", "-10Hz", "Tomorrow, the quiet answers."),
]
```

Column 2 is now the **gap before the line**, not an absolute time. The timeline is derived by
packing. That single change is the whole method: the gap list *is* the performance, and the
measured gap distribution is the design rather than an accident of the schedule.

The gap vocabulary, from [3], [6] and [7]:

| function | written gap | used for |
|---|---|---|
| inside a list | 0.20–0.26 s | "And the door." / "And the kitchen." |
| new sentence, same beat | 0.30–0.40 s | "Same flat." / "Same speaker." |
| new idea | 0.42–0.60 s | "So I keep it loud." |
| topic shift | 0.60–0.75 s | "It's not listening with a microphone any more." |
| **the turn** | **1.30 s** | **"I stopped making noise."** |
| landing | 0.55 s | last line |

### 3.3 The pacing solver — why the beats got longer than written

`ab-pixel/plan.py` synthesises each line **once**, into a content-hashed cache, then solves the
timeline. Two things it fixes that cost me most of a day to learn:

1. **edge-tts pads 0.3–0.5 s of tail silence onto every clip.** Left in, that silence is counted
   twice — once as speech duration and again as the designed gap — so a 25-line film silently
   gains about 10 s of phantom time and overruns. Trim to the last sample above −42 dBFS and keep
   a 40 ms tail so consonants survive.
2. **You cannot space by feel and then discover the overrun**, because every re-spacing costs a
   full re-synthesis. Instead: synthesise once, measure, then solve.

The solver keeps every per-line **rate** exactly as written (rate is the performance) and scales
the **gap set**, with a power law so short beats stay short and the pivots get the room:

```
g' = k · (g / 0.20)^1.6          k solved so the last word lands at 58.0 s
```

A uniform stretch of every gap was tried first and rejected: it makes every beat equally slow,
which is its own kind of mechanical. The power law produces a rhythm instead of a tempo. Result:
list beats land at 0.18–0.21 s, the twist hold at 3.63 s, last word at 57.16 s.

---

## 4. The results

### 4.1 The gap distribution — this is the finding

```
v07 method      gaps (s): 1.41  0.06  0.06  0.06  0.22  0.86  0.06  0.06  0.06  0.06
                          0.50  0.69  0.98  1.00  1.20  9.20  2.15  1.16  1.92
                → 7 of 19 sit on the 0.06 s floor. The voice never rests.

line-split      gaps (s): 1.00  0.35  0.39  0.18  0.43  0.28  0.18  0.18  0.47  0.21
                          0.18  0.69  0.24  0.60  0.31  0.31  1.05  0.74  3.63  1.20
                          0.92  2.58  0.67  1.51  0.92
                → 0 of 24 under 0.10 s. 20 distinct values in 25 gaps.
```

Seven hard-cut joins in a 60-second film is a machine reading a list. Zero is a person telling a
story. That is the defect the Director heard, stated in numbers.

### 4.2 Pitch resets across line boundaries

| | v07 method | line-split |
|---|---|---|
| n | 17 | 22 |
| mean | 7.242 ST | 5.515 ST |
| median | 7.977 ST | 5.921 ST |
| min / max | 0.079 / 10.443 ST | 0.217 / 9.883 ST |

Because each line is a fresh synthesis call, every line starts on a fresh pitch contour and lands
on its own terminal fall. The before has a *larger* mean reset, but that number is inflated by the
0.06 s joins, where the tracker catches a terminal fall immediately followed by a new onset. The
after's resets are structural and evenly distributed. Either way this is not a metric to sell: I
report it because it is the mechanism, not because it flatters the method.

### 4.3 What it costs

Splitting the same 96 words into 25 lines instead of 20 added **2.47 s of speech** with no words
added — fresh onsets, fresh terminal falls, and the sentence-final lengthening that each separate
call performs. That is a real tax on a 60-second film, and it is why the script had to be rewritten
tighter rather than just re-punctuated. Anyone copying this method should budget **about 100 ms per
added line**.

---

## 5. One more thing this exposed — the 9.2 s hole in v07

The v07 script carried shot-window end times, and lines 14–16 all shared `window_end = 46.00`, with
line 17 starting at 46.20. The result is a **9.20-second hole** in the narration between
"And it was still listening." (ends 37.00 s) and "It heard the quiet." (starts 46.20 s).

I did not design that, and it is not a robot defect — it is silence in the middle of a climax,
which is worse. The line-split version has no hole: its longest gap is the 3.63 s held beat before
the turn, which is deliberate. If anything in this note is worth acting on beyond the voice itself,
it is this: **the v07 film has a nine-second dead air pocket at 37 s**, and every measurement I ran
inherited it until I looked at the gap list.

---

## 6. What I did not measure

- **No human listened to either stem.** I have no listener panel, no ABX test and no MOS score.
  Every claim in this document is acoustic measurement, not preference. The Director's ear is the
  only preference data in this project and it currently says both are bad.
- The F0 metrics use voiced frames only and exclude 70–400 Hz outliers; unvoiced consonants,
  breath and creak are not represented in σ.
- The 15 s samples are cut from one performance each, loudness-matched by `loudnorm`, so the
  comparison is not a volume trick — but a 15 s excerpt shows the *open* of the film, where the
  gap design is at its least dramatic. The 3.63 s twist hold is at 36.7 s and is not in the sample.
- **This applies to v09 as well.** v09 used the same single-global-rate pattern as v07
  (12 lines, all at −12 %). The finding here is not a v07-only defect; v09's voice has the same
  flat-rate construction, and its 12 lines have even fewer break points than v07's 20. It is
  unmeasured, but nothing in its method differs in the way that matters.

---

## 7. Files

| path | what |
|---|---|
| `research/tools/measure_voice.py` | the instrument (validated exact on pure tones) |
| `research/ab-pixel/plan.py` | v07 re-performance: cache → measure → solve → build |
| `research/ab-pixel/v07_stems/before_v07_narration.wav` | v07 method, 48 kHz mono, 60.000 s |
| `research/ab-pixel/v07_stems/after_v07_narration.wav` | line-split method, 48 kHz mono, 60.000 s |
| `research/ab-pixel/v07_stems/{before,after}_timing.json` | per-line start/end/rate/pitch/text |
| `research/ab-pixel/v07_metrics.json` | machine output of both full-stem measurements |
| `research/ab-pixel/before_after_stems/` | the two 15 s excerpts |
| `research/ab-pixel/before_15s.mp3`, `after_15s.mp3` | listen to these, loudness-matched |

Reproduce:

```bash
export PATH="$HOME/bin:$PATH" && pip install edge-tts
cd research && python3 ab-pixel/plan.py
python3 tools/measure_voice.py ab-pixel/v07_stems/after_v07_narration.wav \
        --lines ab-pixel/v07_stems/after_timing.json --twist 19
```

---

## Sources

1. CDC, *Audio Script Writing Guide* — write like a speaker; fragments and contractions; no leading
   subordinate clauses; 25-word cap. https://tools.cdc.gov/medialibrary/docs/AudioScriptWritingGuide.pdf
2. freetts.org, *How to make text-to-speech sound natural* — punctuation as a performance script;
   100–300 ms after commas, 400–600 ms between topics; numbers written out.
   https://freetts.org/how-to-make-text-to-speech-sound-natural
3. voice.ai, *How to make text-to-speech sound less robotic* — 120–300 ms phrase breaks, 400–700 ms
   dramatic breaks; max two independent clauses; run-on sentences cause rushing.
   https://voice.ai/hub/tts/how-to-make-text-to-speech-sound-less-robotic/
4. Inworld AI docs, *Generating speech — best practices* — vary sentence length for pace; periods
   separate thoughts; spoken-form numbers. https://docs.inworld.ai/tts/best-practices/generating-speech
5. Bland.ai, *How to make text-to-speech sound more natural* — chunk to 1–2 sentences; long
   paragraphs degrade prosody; stitching artefacts when silence is not normalised.
   https://www.bland.ai/blog/how-to-make-text-to-speech-sound-more-natural
6. zooop.ai, *Text-to-speech* — synthesise sentence by sentence over a paragraph and assemble with
   deliberate silences; "edited rather than recited"; prosody is predicted over a limited window.
   https://zooop.ai/glossary/ai-generation/text-to-speech
7. Ivy J. Su, *Making two TTS voices sound like an actual conversation* — vary inter-turn gaps by
   function (continuation 150–250 ms, topic shift 400–600 ms); split on semantic boundaries;
   identical concatenated gaps are the uncanny valley.
   https://dev.to/ivyjsu/making-two-tts-voices-sound-like-an-actual-conversation-3hn7
8. ElevenLabs docs, *Text to speech — best practices* — current models do not support SSML
   `<break>`; too many breaks cause instability; pace via text structure.
   https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices
9. *Acoustic correlates of listener-rated expressiveness* — F0 SD predicts expressiveness
   (β = 3.62, p < 0.001); semitone formula σ_ST = 39.86·log10((E+σ)/E).
   https://pmc.ncbi.nlm.nih.gov/articles/PMC12337113/
10. *Normalised F0 SD as a liveliness measure* (SLaTE 2009) — moving-window SD, log transform for
    cross-speaker comparison; monotone delivery harms recall and is disliked.
    http://www.eee.bham.ac.uk/SLaTE2009/papers/SLaTE2009-03-v2.pdf
11. *F0 statistics and liveliness* (SP2010) — "the higher the SD, the more livelier the voice";
    IQR more robust than raw range. https://sprosig.org/sp2010/papers/100440.pdf
12. *Preliminary F0 statistics and forensic phonetics* — normative male read speech σ ≈ 15–25 Hz;
    59 % of speakers 2.5–3.5 semitones.
    https://www.researchgate.net/publication/251306660_Preliminary_F0_statistics_and_forensic_phonetics


---

# imaging-pixel.md — what makes a generated night plate read as a real frame

**Author:** pixel · **Branch:** `pixel/voice-imaging` · **Date:** 2026-11-01
**Scope:** plate generation for MARK FOUR / MARK FIVE register — 1920×1080, 30 fps, photographic,
night, weather. This note covers the prompt craft and the three measurements that tell you whether
a plate reads as a frame or as a render.

---

## 0. The short version

A night plate reads as real when three things are true at once:

1. **The light is a physical source with a colour temperature and a falloff**, described by where it
   is and what it lands on — not by the mood it creates.
2. **The frame is mostly dark and the darkness is allowed to be dark.** The lit area carries the
   subject; the unlit area carries the dread. A night plate that is 65 % lit is a day plate.
3. **The camera is a specific camera.** Focal length, aperture, shutter, ISO, film stock. These are
   not decoration: they tell the model how to compress space, how much depth of field to leave,
   and how much grain to add.

The measured result, on three matched pairs (§4): **texture and tonal range rose on two pairs and
fell on the third, and the third is the one that looks most like a real photograph.** That is the
most useful finding in this note, and it is the opposite of what a single-number quality metric
would tell you.

| plate | laplacian var | contrast SD | lit % | lit:unlit | read |
|---|---|---|---|---|---|
| kitchen — before | 83.9 | 39.2 | 34.4 | 0.52 | too dark and too flat to read as a room |
| **kitchen — after** | **128.5 (×1.53)** | **59.8 (+20.6)** | **48.5** | **0.94** | **reads as a photograph** |
| hall — before | 46.7 | 29.2 | 32.4 | 0.48 | worst of the six: flat, mush, no texture |
| **hall — after** | **115.6 (×2.48)** | **49.7 (+20.5)** | **51.5** | **1.06** | **reads as a photograph** |
| street — before | 615.9 | 57.0 | 66.2 | **1.96** | highest "quality" numbers, looks like stock video |
| **street — after** | **352.1 (×0.57)** | **48.2 (−8.8)** | **42.2** | **0.73** | **reads as a photograph** |

---

## 1. Camera language — describe the lens, not the quality

The single biggest failure mode in the "before" prompts was the word **"8K, hyperrealistic,
ultra-detailed"**. Every source on the subject says the same thing: those words push a model toward
an over-sharpened, over-defined, synthetic look. Realism comes from describing **the photograph**,
not the resolution. [1][4]

The formula that the sources converge on:

```
[realism trigger] + subject + [camera, lens, shutter, aperture] + [light source]
+ texture + colour + composition + grain + [negatives]
```

Specific pieces of it:

- **Focal length tells the model how to compress and separate space.** 35 mm renders a room the
  way an eye remembers it; 24–28 mm pushes the background away and exaggerates the foreground;
  50–85 mm compresses and isolates. Naming the lens is not decoration, it changes the geometry. [4]
- **Aperture sets the depth of field** and therefore how the fore/mid/background separates. A night
  interior at f/1.4 has a foreground that falls out of focus within a metre — and that blur is one
  of the strongest authenticity cues.
- **Shutter and ISO control motion and grain.** At 1/15 s in a hallway, a person moving would smear;
  the room does not, because the room is not moving. At ISO 6400 the grain is coarse and coloured,
  which is what a real 2 a.m. frame looks like.
- **Name the film stock or the sensor.** Kodak Portra, CineStill 800T, Vision3 500T — each carries a
  colour response, a grain structure and a highlight roll-off the model has seen paired with the
  word "photograph" thousands of times. [5]
- **Lens artefacts are the brain's authenticity cues.** Chromatic aberration at the frame edges,
  mild barrel distortion, halation around a hot source, a slight vignette. The brain uses the
  imperfections of a lens to decide a frame is a photograph. [5][2]
- **Fewer hype words, more physics.** "8K / ultra-detailed / hyperrealistic" moves a model toward
  the statistical average of retouched stock photography — which is exactly the plastic look the
  Director rejects. [1][4]

**What I actually used:** `35mm lens at f/1.4, 1/30 s, ISO 3200, Kodak Portra 800 pushed two stops`
for the kitchen; `50mm at f/2, 1/15 s, ISO 6400, CineStill 800T` for the hall; `28mm at f/2, 1/60 s,
ISO 1600, Kodak Vision3 500T` for the street. Three different lenses for three different rooms —
because a film shot by one person in one night uses whatever glass they have, and the variety is
itself a realism signal.

---

## 2. Lighting — describe a source, never a mood

"**Dramatic lighting, moody, atmospheric**" was in all three before prompts and it is the most
damaging phrase in the set. It asks the model for the *look* of drama without telling it where any
light comes from, so the model invents a soft, sourceless, low-contrast wash — which is what the
before plates show, and what the low contrast numbers confirm (29.2 and 39.2 versus 49.7 and 59.8).

A directional named light beats "dramatic lighting" every time. [4] Every light must be:

- **located**: "a 2700K tungsten bulb in a bare pendant above the sink, hanging low"
- **bounded**: "casting a hard pool of light on damp laminate and falling off to black within a metre"
- **motivated**: it must be the reason the visible surfaces are visible. If a surface is lit and no
  source in the frame could reach it, the brain registers a compositing error. [5]

### One practical light per frame

The house rule is **one practical light per frame** — a source that exists inside the world of the
shot, that the viewer could point at. Everything else is either its spill, its reflection, or
darkness. This does three things for a night film:

1. It gives the grade a single anchor to protect, so the 33³ LUT does not have to guess.
2. It gives the frame a **colour temperature contrast** — the warm practical against a cold spill
   or a cold window — which is what "cinematic night" actually means optically. My after plates use
   a 2700K practical against a 4000–6500K secondary, never two lights of the same temperature.
3. It creates the lit:unlit boundary that composition lives on.

**The secondary light is what a real night frame actually has:** a phone screen turned away from
camera (kitchen), a sliver of warm light under a door (hall), a sodium streetlamp through rain
(street). Each is a 1 %-of-frame element doing 30 % of the work.

---

## 3. Weather, texture and negatives

**Weather as atmosphere, not as decoration.** Rain has to be *in* the frame in a way that interacts
with the light: "rain on the window above the sink, backlit by a sodium streetlamp outside, streaks
on the glass", "rain falling, visible as streaks against the lamp's cone, **not against the dark**".
That last clause matters — rain is only visible where it crosses a bright source, and a prompt that
asks for rain everywhere produces a texture overlay rather than weather. In the house style rain is
already a compositing layer; the plate's job is to establish *where the light is* so the rain layer
knows where to be visible.

**Texture is the proof of a surface.** Damp laminate, beaded steel, chipped grout, scuffed plaster,
worn floorboards, crumbs. The before plates are smooth; the after plates have a surface you could
touch. This is what the Laplacian variance measures, and it is why that number doubled on the hall
(46.7 → 115.6): the before hall had no texture anywhere in the lit area.

**Negative prompts — the library that mattered:** `cartoon, CGI, 3D render, illustration, painting,
plastic skin, airbrushed, HDR, oversaturated, perfect symmetry, text, watermark, lens flare` plus a
scene-specific set that names the *failure in this particular photograph*: `dry surfaces` and
`dry ground` (a night rain plate with dry ground is a lie), `dry air`, `neon signage` (fights the
one-practical rule), `smooth skin`, `clean cleanliness`. [3][2]

A negative should name the specific wrongness, not a general category. "No illustration" is weak;
"dry ground" is strong, because it is the one thing that would make the street plate impossible.

---

## 4. The measurement, and where it disagrees with the eye

### 4.1 What was measured

Every plate is exactly **1920×1080** — the native generations were 1408×768 and 1376×768, centre
cropped to 16:9 and Lanczos-scaled up, because Laplacian variance is scale-dependent and comparing
plates at different resolutions is meaningless. Native files are kept alongside in
`plates_*/native/` so the upscale can be audited.

- **Laplacian variance** — Var(∇²luma) on 0–255 luma. The standard acuity/texture measure.
- **Contrast** — standard deviation of luma, 0–255.
- **Lit : unlit** — fraction of frame above 10 % of full scale (25.5/255), and the ratio.

### 4.2 The results

```
plates_before                    lapvar   contrast   mean    lit%    L:U
plate1_kitchen.png                 83.9       39.2    31.1    34.4   0.523
plate2_hall.png                    46.7       29.2    23.5    32.4   0.480
plate3_street.png                 615.9       57.0    60.9    66.2   1.957

plates_after
plate1_kitchen.png                128.5       59.8    52.1    48.5   0.942
plate2_hall.png                   115.6       49.7    46.1    51.5   1.062
plate3_street.png                 352.1       48.2    36.8    42.2   0.729
```

### 4.3 The awkward part

**The street plate got worse on every number and better as a photograph.** Laplacian variance fell
×0.57, contrast fell 8.8, mean luma fell 24. The before street is a busy, bright, high-detail
commercial street with a shopfront sign reading "THE DAILY STOP" — the highest detail numbers in the
set (615.9), and it looks like stock footage or a taxi-rank advertisment. The after street is a
quiet residential road seen from a first-floor window through rain, mostly dark, with one sodium
lamp — and it is the most convincing photograph of the six.

This is the important result, and it generalises: **a night plate is supposed to lose detail
numbers.** Detail is what daylight has. What a night frame has instead is a *narrow lit zone with
high local contrast inside it* and a large area of legibility-free black. The before street scored
well because it was lit like a day scene with a blue cast — an error the metrics rewarded.

So the metrics are not acceptance criteria on their own. What they are good for:

- **Laplacian variance is a texture floor, not a target.** Hall before = 46.7 was *too low*: the
  lit area was smooth mush with no surface. Kitchen after = 128.5 is healthy. There is no "higher is
  better" above roughly 150 for a night plate — the street before's 615.9 is a warning sign, not a
  win.
- **Contrast SD above ~45** is where a night plate starts to have a real tonal range. Both after
  interiors clear it; both before interiors do not.
- **Lit:unlit between 0.5 and 1.1** is the useful band for a night interior — roughly a third to a
  half of the frame carries information and the rest is allowed to be black. **Above 1.5 the plate
  has stopped being a night plate.** The before street at 1.957 fails on this alone, which is the
  one metric that *did* predict the eye's verdict correctly.

**The rule I would put in the style guide:** lit:unlit is a hard gate (0.5–1.1 for interiors,
≤0.8 for exteriors); Laplacian variance is a floor (≥90 at 1920×1080 on a night interior);
contrast SD is a floor (≥45). None of them is a target to maximise.

---

## 5. Composition

Non-negotiable per the house style, and visible in all three after plates:

- **Fore / mid / ground, all three occupied.** Kitchen: out-of-focus worktop edge → sink → doorway.
  Hall: out-of-focus coat rack → floorboards and shoes → the door. Street: wet windowsill → road and
  car → the receding row of houses. The foreground element is always *defocused*, which is the
  cheapest way to buy depth.
- **One leading line.** The skirting board, the kerb, the edge of the worktop. Stated in the prompt
  explicitly ("the kerb is a leading line from bottom-right to the lamp") rather than hoped for.
- **One practical light**, placed off-centre. All three after plates put the source on the left or
  upper-left and the subject on the right, so the frame has a direction of light rather than a
  symmetrical wash.
- **The subject is not centred.** Nothing in a real 2 a.m. phone-shot or handheld frame is centred,
  and centring is one of the tells that reads as "generated".

---

## 6. Seeds and reproducibility — what I can and cannot guarantee

- **The generator used here does not accept a seed.** I have no seed parameter, no sampler control
  and no reproducibility guarantee from the same prompt. That is a real limitation and I am not
  going to pretend otherwise: **these plates cannot be regenerated deterministically.**
- What *is* reproducible is the **prompt text**, which is why every after prompt is written as a
  fixed, verbatim, reusable block — same style block, same negative library, only the subject and
  the scene-specific negatives change. Copying a style block unchanged across a batch is the
  documented way to hold consistency without a seed, and seed locking alone is reported to give only
  ~60 % consistency anyway. [2]
- Practical position for this project: **treat the plate as a plate.** Once a frame is chosen it is
  committed to the repo and the render references the committed file, never the prompt. The prompt
  is documentation of intent, not a build step. Any future work that needs a repeatable plate
  pipeline has to move to a generator with a seed and a pinned model version.

---

## 7. What I did not do

- **No human judged these plates either.** I looked at all six side by side; that is one person, and
  it is not evidence. The "reads as a photograph" column above is my judgement and is labelled as
  such.
- No perceptual metric (LPIPS, CLIP-IQA) was run — with n = 3 pairs, any such number would be noise
  dressed as rigour.
- The plates were not passed through the 33³ LUT or the grain layer; they are raw generations
  measured before grade. A graded plate will move every one of these numbers, and the thresholds in
  §4.3 apply to **ungraded** plates.
- Up-scaling from ~1376 px to 1920 px is not free. It lifts Laplacian variance slightly on its own
  (the Lanczos kernel adds acutance), which is why the native files are preserved — if anyone wants
  to re-run this, measure the natives at a common resolution instead.

---

## 8. Files

| path | what |
|---|---|
| `research/ab-pixel/plates_before/` | three plates, "dramatic lighting / 8K / moody" prompts, 1920×1080 |
| `research/ab-pixel/plates_after/` | three plates, camera-language prompts, 1920×1080 |
| `research/ab-pixel/plates_*/native/` | the un-cropped native generations |
| `research/ab-pixel/plate_metrics.py` | the three measurements + the table |
| `research/ab-pixel/plate_metrics.json` | machine output |

```bash
cd research/ab-pixel && python3 plate_metrics.py
```

---

## Sources

1. AI Photography, *Photorealistic AI prompts* — brief like a photographer (subject → lens →
   aperture → light direction); **fewer** hype words; "8K / hyperrealistic / ultra-detailed" push
   toward over-sharpened artificial renders.
   https://www.aiprophotography.com/ai-tools-and-generation/photorealistic-ai-prompts/
2. Sozee, *Make AI photos look like real photography* — a fixed verbatim style block across a batch;
   every prompt needs a directional source with colour temperature and diffusion quality; seed
   locking alone gives ~60 % consistency; flaws read as real.
   https://www.sozee.ai/resources/make-ai-photos-real-photography/
3. AI Video Bootcamp, *Photorealistic AI prompts guide* — the realism formula; negative library
   (no cartoon, no CGI, no 3D render, no plastic skin, no text/watermark, no HDR).
   https://aivideobootcamp.com/blog/photorealistic-ai-prompts-guide-2026/
4. Envato, *Prompts for realistic AI images* — models default to the statistical average of
   retouched stock; 35/50/85 mm tells the model how to compress and separate; a directional named
   light beats "dramatic lighting".
   https://elements.envato.com/learn/prompts-for-realistic-ai-images
5. AI-Inspo, *How to create realistic AI photos* — name the film stock/sensor, focal length, shutter,
   aperture; link every light source to the subject's illumination or the brain registers a
   compositing error; lens artefacts are the authenticity cues.
   https://www.ai-inspo.com/blogs/image/how-to-create-realistic-ai-photos
6. Make AI Photos, *Best AI prompt for realistic photos* — night/rain exemplar: 35 mm f/1.4, neon in
   wet asphalt, visible rain streaks, ISO 3200, grain; negatives: dry ground, oversaturated neon,
   illustration, render. https://www.makeaiphotos.com/blog/best-ai-prompt-for-realistic-photos/
