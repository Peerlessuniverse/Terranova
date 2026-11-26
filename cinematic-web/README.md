# TERRA NOVA — Opening Cinematic (web runtime)

A 120-second opening, *The Calling of Gaia*, following `Asset/TERRA_NOVA_Opening_Cinematic_Master_v1.3.md`.
It plays in real time in the browser: a 2D canvas draws all 23 shots (A01–H01) from WebP stills, clocked by one
AAC audio track. There is no video file, so the whole thing is about **3.6 MB** (the 4K MP4 render in
`../cinematic-motlab/out/` is 326 MB).

## Run locally

    run-cinematic.bat

or `python -m http.server 8790 --bind 127.0.0.1` inside `runtime/`, then open http://127.0.0.1:8790/.
Opening `index.html` straight from disk (`file://`) does not work, because browsers block ES modules there.

## What is in `runtime/` (what you deploy)

| File | Purpose |
|---|---|
| `index.html`, `css/player.css`, `js/player.js` | Player: start screen, controls, captions, H02 ending |
| `js/engine.js`, `js/scenes.js` | Scene renderer (generated from `cinematic-motlab`, do not edit by hand) |
| `img/*.webp` | Shot stills (20 files, ~2.1 MB) |
| `audio/opening.m4a` | Voice-over + score, AAC 96 kb/s, -16 LUFS (~1.4 MB) |
| `audio/accept.m4a` | Gaia's acceptance line, played after the CTA |
| `captions.json`, `subtitle-id.vtt`, `subtitle-en.vtt`, `transcript-id.md` | Captions and transcript |
| `manifest.json` | Version, duration, scenes, file sizes |

## Player behaviour (§8–9 of the master script)

- Explicit start (so audio can play); **Lewati** on the start screen and in the controls jumps to the H02 ending.
- Subtitles on by default: ID → EN → off (`C`). Mute (`M`), play/pause (`Space`/`K`), fullscreen (`F`),
  skip (`S`/`Esc`), seek ±5 s (arrow keys).
- **Gerak / Statis** button: static mode shows one still frame per shot; it is the default when the system asks
  for reduced motion.
- The whole 16:9 frame is always visible on a dark ground; in portrait, captions move below the frame.
- Pauses when the tab is hidden. If a shot's image is still downloading, the clock holds and a spinner shows.
- Canvas resolution follows the screen and drops automatically on slow devices.
- Images are fetched in timeline order; the start button is enabled once the first 24 s and the audio are ready.

## Game handoff

The player emits DOM events on `window` and, when embedded in an iframe, `postMessage` to the parent:

- `terranova:intro-ended` `{ skipped, at }`: the film finished or was skipped (H02 is showing).
- `terranova:intro-accepted`: the player pressed **Aku menerima panggilanmu**.

`localStorage.tn_intro_seen_at` stores when the intro was last seen (local draft only, no database change).
The login link defaults to `../`; override it with `?login=/path`. `window.__terranova` exposes
`start()`, `play()`, `pause()`, `seek(t)`, `skip()` and `time` for the shell and QA.
Skip and replay never grant anything; initialisation stays with the game.

## Rebuild

    python tools/build_audio.py   # ElevenLabs voices + score, mix to -16 LUFS
    python tools/build_web.py     # stills -> WebP, bundle scenes, captions, manifest

Voices (ElevenLabs voice library):

- **Narrator:** "Eric Dipoetra" (Indonesian, standard accent), model `eleven_multilingual_v2`. The owner chose it
  from a same-text A/B test against their reference video, because "Eyang" sounded Malaysian. v2 ignores delivery
  tags, so `build_audio.py` strips them for this voice; pauses widen up to 1.1 s to fill each slot calmly.
- **Gaia:** "Serena – Calm, Warm, Gentle" (mature, soft, expressive), model `eleven_v3` with per-line delivery tags
  such as `[sorrowful]`, plus an ethereal echo.

**Replacing a still:** put the new image in `overrides/` with the same name (e.g. `overrides/G02_yard.webp`);
`build_web.py` uses it instead of the cinematic-motlab source and never overwrites it. Do not drop files straight
into `runtime/img/`: the next build overwrites them. Current overrides: `G02_yard`, `E04_portrait`, `F03_determined`
(full 16:9 shots, so `RENDER_PATCH` in `build_web.py` draws E04 and F03 full-frame) and `ending-bg` (H02 backdrop).

`build_audio.py` caches every TTS clip and the score in `_build/`, so re-runs cost no credits unless a line
changes. Narration timing follows the master script slots; numbers are spelled out for the voice only.

## Still open

- Statistics follow register v1.1 and still need editorial approval before publication (§7).
- Asset licences (stills, logo) must be reviewed before release.
- Not yet tested on physical devices (2 GB Android, iOS Safari) or on the 1.6 Mbps profile.
