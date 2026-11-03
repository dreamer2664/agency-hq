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
