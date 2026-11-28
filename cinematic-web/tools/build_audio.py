"""TERRA NOVA opening (120s) - voiceover + score for the web player.

Voices (ElevenLabs voice library):
  narrator = "Eric Dipoetra" (Indonesian accent), eleven_multilingual_v2, picked by the owner in an A/B test
  Gaia     = "Serena - Calm, Warm, Gentle" (mature, soft, expressive), eleven_v3 + tags, with an ethereal echo
Each cue is split into sentences; each sentence is one TTS clip placed inside the cue's slot with natural
pauses, so subtitle timings are exact. Tags like [sorrowful] steer delivery and are not spoken (checked
with speech-to-text). Numbers are spelled out for the voice only; subtitles keep digits.
Score = ElevenLabs Music (instrumental, 120s), ducked under speech. Master: -16 LUFS integrated.

Outputs: _build/{vo.wav, music.mp3, timings.json}, runtime/audio/{opening,accept}.{ogg,m4a}
Usage (from cinematic-web/): python tools/build_audio.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "_build")
RUNTIME = os.path.join(ROOT, "runtime", "audio")
os.makedirs(BUILD, exist_ok=True)
os.makedirs(RUNTIME, exist_ok=True)
ENV = os.path.normpath(os.path.join(ROOT, "..", "..", ".env"))
KEY = [l.split("=", 1)[1].strip().strip("\"'") for l in open(ENV, encoding="utf-8")
       if l.startswith("ELEVENLABS_API_KEY=")][-1]
SR = 48000
DUR = 120.0
MAX_TEMPO = 1.12

# Eric Dipoetra (Indonesian, standard accent), chosen by the owner from a same-text A/B against their
# reference video (Eyang sounded Malaysian). multilingual_v2 does not understand [tags], so they are stripped.
NARRATOR = dict(voice="0HgW3YEiPlysXzVQ9jON", model="eleven_multilingual_v2", language="id",
                settings={"stability": 0.5, "similarity_boost": 0.8},
                pause=0.5, min_pause=0.3, max_pause=1.1,
                fx="acompressor=threshold=0.15:ratio=2:attack=15:release=200")
GAIA = dict(voice="fpsPI3vlnQ0anCTPiHk5", model="eleven_v3",              # Serena
            settings={"stability": 0.5, "similarity_boost": 0.8, "use_speaker_boost": True},
            pause=0.85, min_pause=0.45,
            fx="highpass=f=90,aecho=0.85:0.72:55|110|190|320:0.24|0.17|0.11|0.07")

# each line: (subtitle ID, text for the voice with delivery tags, subtitle EN)
CUES = [
    dict(id="N1", who="Narator", start=0.4, end=12.4, lines=[
        ("Sejak awal, Bumi memiliki siklusnya sendiri.",
         "[slow, mysterious] Sejak awal, Bumi memiliki siklusnya sendiri.", "Earth has its own cycles."),
        ("Setiap air yang mengalir, setiap daun yang gugur, memiliki tempat dalam perjalanan kehidupan.",
         "[warm, reflective] Setiap air yang mengalir, setiap daun yang gugur, memiliki tempat dalam perjalanan kehidupan.",
         "Every flowing stream and every fallen leaf has a place in the journey of life."),
    ]),
    dict(id="N2", who="Narator", start=12.6, end=29.8, lines=[
        ("Kota tumbuh. Industri berkembang. Konsumsi meningkat.",
         "[measured] Kota tumbuh. Industri berkembang. Konsumsi meningkat.",
         "Cities grew, industries expanded, and consumption rose."),
        ("Pada tahun 2023, dunia menghasilkan sekitar 2,1 miliar ton sampah perkotaan.",
         "[grave] Pada tahun dua ribu dua puluh tiga, dunia menghasilkan sekitar dua koma satu miliar ton sampah perkotaan.",
         "In 2023, the world generated an estimated 2.1 billion tonnes of municipal solid waste."),
    ]),
    dict(id="N3", who="Narator", start=30.4, end=47.8, lines=[
        ("Namun manusia tidak tinggal diam.", "[hopeful] Namun manusia tidak tinggal diam.",
         "Yet humanity did not stand still."),
        ("Mereka memilah, membersihkan, mendaur ulang, dan mengedukasi.",
         "[warm] Mereka memilah, membersihkan, mendaur ulang, dan mengedukasi.",
         "People sorted, cleaned, recycled and educated."),
        ("Perjuangan itu membawa perubahan.", "[hopeful] Perjuangan itu membawa perubahan.",
         "Their efforts made a difference,"),
        ("Tetapi tantangan yang kita hadapi masih begitu besar.",
         "[grave] Tetapi tantangan yang kita hadapi masih begitu besar.", "but the challenge remains immense."),
    ]),
    dict(id="N4", who="Narator", start=47.9, end=65.0, lines=[
        ("Di Indonesia, lebih dari 34 juta ton sampah tercatat pada 2025.",
         "[grave] Di Indonesia, lebih dari tiga puluh empat juta ton sampah tercatat pada dua ribu dua puluh lima.",
         "In Indonesia, more than 34 million tonnes of waste were recorded in 2025."),
        ("Setiap tahun, sekitar 19 hingga 23 juta ton plastik memasuki perairan dunia.",
         "[grave] Setiap tahun, sekitar sembilan belas hingga dua puluh tiga juta ton plastik memasuki perairan dunia.",
         "Each year, an estimated 19 to 23 million tonnes of plastic waste enter aquatic ecosystems worldwide."),
        ("Masihkah ada harapan?", "[softly, mysterious] Masihkah ada harapan?", "Is there still hope?"),
    ]),
    dict(id="G1", who="Gaia", start=69.2, end=86.8, lines=[
        ("Aku adalah Gaia.", "[softly, ethereal] Aku adalah Gaia.", "I am Gaia."),
        ("Aku telah menyaksikan perjalanan peradabanmu.",
         "[wistful] Aku telah menyaksikan perjalanan peradabanmu.",
         "I have witnessed the journey of your civilization."),
        ("Aku merasakan setiap luka yang tertinggal di tanah, di sungai, dan di udara.",
         "[sorrowful] Aku merasakan setiap luka yang tertinggal di tanah, di sungai, dan di udara.",
         "I feel every wound left upon the land, in the rivers and in the air."),
    ]),
    dict(id="G2", who="Gaia", start=87.3, end=103.0, lines=[
        ("Manusia telah berusaha menyembuhkanku.", "[gently] Manusia telah berusaha menyembuhkanku.",
         "Humanity has tried to heal me."),
        ("Namun luka-lukaku terus bertambah.", "[sighs, sorrowful] Namun luka-lukaku terus bertambah.",
         "Yet my wounds keep growing."),
        ("Aku tidak membutuhkan lebih banyak janji.", "[softly, resolute] Aku tidak membutuhkan lebih banyak janji.",
         "I do not need more promises."),
        ("Aku membutuhkan tindakan.", "[firm] Aku membutuhkan tindakan.", "I need action."),
    ]),
    dict(id="G3", who="Gaia", start=103.3, end=117.8, lines=[
        ("Bukan kekayaan, kekuatan, atau kedudukanmu yang membuatku memanggilmu.",
         "[gently] Bukan kekayaan, kekuatan, atau kedudukanmu yang membuatku memanggilmu.",
         "I call you not for your wealth, power or status."),
        ("Aku masih percaya manusia dapat berubah.", "[hopeful] Aku masih percaya manusia dapat berubah.",
         "I still believe humanity can change."),
        ("Maukah engkau membantuku?", "[tenderly, pleading] Maukah engkau membantuku?", "Will you help me?"),
    ]),
]
ACCEPT = ("[warmly, grateful] Terima kasih, manusia terpilih. Perjalananmu kini dimulai. "
          "Pergilah ke kotamu. Aku akan selalu menyertaimu.")
MUSIC_PROMPT = (
    "Original two-minute cinematic environmental fantasy score, instrumental with subtle wordless choir. "
    "0:00-0:12 serene and sacred: piano, warm strings, gentle nature ambience. "
    "0:12-0:30 light rhythmic pulse with restrained industrial tension. "
    "0:30-0:48 human warmth, restrained hopeful strings. "
    "0:48-1:03 darker low drone, sparse percussion, then near silence at 1:03-1:05. "
    "1:05-1:27 soft wordless choir, harp, ethereal mystical goddess motif. "
    "1:27-1:43 intimate strings, leaving room for dialogue. "
    "1:43-2:00 hopeful orchestral crescendo resolving to a warm soft ending. "
    "No lyrics, no imitation of existing copyrighted themes, dialogue-friendly arrangement.")
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB,areverse")


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def tts(text, who):
    if who["model"] != "eleven_v3":  # only v3 understands delivery tags; other models would read them aloud
        text = re.sub(r"\[[^\]]*\]\s*", "", text).strip()
    body = {"text": text, "model_id": who["model"], "voice_settings": who["settings"]}
    if who.get("language"):
        body["language_code"] = who["language"]
    digest = hashlib.md5(json.dumps([who["voice"], body], sort_keys=True).encode()).hexdigest()[:12]
    mp3 = os.path.join(BUILD, f"tts_{digest}.mp3")
    if not os.path.exists(mp3):
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{who['voice']}", json=body, timeout=180,
                          headers={"xi-api-key": KEY, "Accept": "audio/mpeg"},
                          params={"output_format": "mp3_44100_128"})
        if r.status_code != 200:
            sys.exit(f"TTS error {r.status_code}: {r.text[:300]}")
        open(mp3, "wb").write(r.content)
    return mp3


def decode(mp3, tempo=1.0):
    raw = mp3[:-4] + f"_{tempo:.3f}.f32"
    af = TRIM + (f",atempo={tempo:.4f}" if abs(tempo - 1) > 1e-3 else "")
    run(["ffmpeg", "-y", "-i", mp3, "-af", af, "-ar", str(SR), "-ac", "1", "-f", "f32le", raw])
    return np.fromfile(raw, dtype=np.float32)


def build_cue(cue):
    who = NARRATOR if cue["who"] == "Narator" else GAIA
    slot = cue["end"] - cue["start"]
    mp3s = [tts(spoken, who) for _, spoken, _ in cue["lines"]]
    clips = [decode(m) for m in mp3s]
    speech = sum(len(c) for c in clips) / SR
    gaps = len(clips) - 1
    pause = who["pause"]
    if gaps and speech + gaps * pause > slot:
        pause = max(who["min_pause"], (slot - speech) / gaps)
    elif gaps and who.get("max_pause"):  # unhurried delivery: let pauses breathe into the free slot time
        pause = min(who["max_pause"], max(pause, (slot * 0.9 - speech) / gaps))
    tempo = 1.0
    if speech + gaps * pause > slot:
        tempo = min(MAX_TEMPO, speech / (slot - gaps * pause))
        clips = [decode(m, tempo) for m in mp3s]
    return clips, pause, tempo, who


def fx(buf, chain, name):
    raw = os.path.join(BUILD, f"{name}.f32")
    out = os.path.join(BUILD, f"{name}_fx.f32")
    buf.tofile(raw)
    run(["ffmpeg", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw, "-af", chain,
         "-ar", str(SR), "-ac", "1", "-f", "f32le", out])
    y = np.fromfile(out, dtype=np.float32)[: len(buf)]
    return np.pad(y, (0, len(buf) - len(y)))


def main():
    tracks = {"Narator": np.zeros(int(DUR * SR), dtype=np.float32), "Gaia": np.zeros(int(DUR * SR), dtype=np.float32)}
    timings = []
    for cue in CUES:
        clips, pause, tempo, who = build_cue(cue)
        vo = tracks[cue["who"]]
        t = cue["start"]
        for (sub, _, en), c in zip(cue["lines"], clips):
            i = int(t * SR)
            seg = c[: max(0, len(vo) - i)]
            vo[i:i + len(seg)] += seg
            timings.append(dict(cue=cue["id"], speaker=cue["who"], start=round(t, 3),
                                end=round(t + len(c) / SR, 3), id=sub, en=en))
            t += len(c) / SR + pause
        end = t - pause
        flag = "" if end <= cue["end"] + 1e-3 else "  <-- MELEWATI SLOT"
        print(f"{cue['id']} {cue['start']:6.2f}-{end:6.2f} (slot s/d {cue['end']:6.2f}) "
              f"tempo x{tempo:.2f} jeda {pause:.2f}s{flag}", flush=True)
    vo = fx(tracks["Narator"], NARRATOR["fx"], "narrator") + fx(tracks["Gaia"], GAIA["fx"], "gaia")
    vo_raw, vo_path = os.path.join(BUILD, "vo.f32"), os.path.join(BUILD, "vo.wav")
    vo.astype(np.float32).tofile(vo_raw)
    run(["ffmpeg", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", vo_raw, vo_path])
    json.dump(timings, open(os.path.join(BUILD, "timings.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    music = os.path.join(BUILD, "music.mp3")
    if not os.path.exists(music):
        print("menyusun musik ...", flush=True)
        r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": KEY}, timeout=900,
                          json={"prompt": MUSIC_PROMPT, "music_length_ms": 120000, "force_instrumental": True})
        if r.status_code != 200:
            sys.exit(f"Music error {r.status_code}: {r.text[:400]}")
        open(music, "wb").write(r.content)

    # music bed: fade in, hush around 63-65.6s (silence before the fiction label), fade out; ducked under speech
    env = "volume='if(between(t,63.0,65.6),0.12+0.88*abs(t-64.3)/1.3,1)':eval=frame"
    fc = (f"[1:a]aresample={SR},aformat=channel_layouts=stereo,atrim=0:{DUR},apad=whole_dur={DUR},"
          f"afade=t=in:d=1.5,afade=t=out:st={DUR - 3}:d=3,{env},volume=0.55[m];"
          f"[0:a]aformat=channel_layouts=stereo,asplit[v1][v2];"
          f"[m][v1]sidechaincompress=threshold=0.025:ratio=6:attack=30:release=450[duck];"
          f"[v2][duck]amix=inputs=2:normalize=0:dropout_transition=0,loudnorm=I=-16:TP=-1.5:LRA=9[out]")
    master = os.path.join(BUILD, "master.wav")
    run(["ffmpeg", "-y", "-i", vo_path, "-i", music, "-filter_complex", fc, "-map", "[out]",
         "-ar", str(SR), "-t", str(DUR), master])
    # second pass: measure, then set integrated loudness to -16 LUFS with a true-peak limiter
    meas = subprocess.run(["ffmpeg", "-v", "info", "-i", master, "-af", "ebur128", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    lufs = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    out = os.path.join(RUNTIME, "opening.m4a")
    run(["ffmpeg", "-y", "-i", master, "-af", f"volume={-16.0 - lufs:.2f}dB,alimiter=limit=0.85:level=false",
         "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", out])
    # Opus utama (~700 KB, anggaran opening); AAC di atas tetap jadi cadangan untuk browser tanpa Opus
    run(["ffmpeg", "-y", "-i", master, "-af", f"volume={-16.0 - lufs:.2f}dB,alimiter=limit=0.85:level=false",
         "-c:a", "libopus", "-b:a", "40k", "-vbr", "on", "-application", "audio", os.path.join(RUNTIME, "opening.ogg")])

    acc = decode(tts(ACCEPT, GAIA))
    acc = fx(np.pad(acc, (0, SR)), GAIA["fx"], "accept")
    acc_raw = os.path.join(BUILD, "accept.f32")
    acc.tofile(acc_raw)
    run(["ffmpeg", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", acc_raw,
         "-af", "loudnorm=I=-16:TP=-1.5", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart",
         os.path.join(RUNTIME, "accept.m4a")])
    run(["ffmpeg", "-y", "-i", os.path.join(RUNTIME, "accept.m4a"), "-c:a", "libopus", "-b:a", "40k",
         os.path.join(RUNTIME, "accept.ogg")])
    print("->", out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main()
