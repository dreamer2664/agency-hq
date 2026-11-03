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
