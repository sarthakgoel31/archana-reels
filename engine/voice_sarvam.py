#!/usr/bin/env python3
"""
Sarvam AI (Bulbul) Hindi voiceover — natural Indic TTS.
Reads SARVAM_API_KEY from env (or archana-reels/.env).

Generates one voice clip per script segment, concatenates into a single
voiceover, and writes per-segment timings the HyperFrames composition uses
to sync captions + B-roll.

Usage:  python engine/voice_sarvam.py engine/scripts/panchang.json
Out:    engine/voice/voiceover.mp3  +  engine/voice/timings.json
"""
import os, sys, json, base64, subprocess, tempfile
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "engine", "voice")
SARVAM_URL = "https://api.sarvam.ai/text-to-speech"


def _load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _tts(text: str, speaker: str, pace: float, pitch: float, out_wav: str):
    key = os.environ.get("SARVAM_API_KEY")
    if not key:
        raise RuntimeError("SARVAM_API_KEY not set — add it to archana-reels/.env (see .env.example)")
    resp = requests.post(
        SARVAM_URL,
        headers={"api-subscription-key": key, "Content-Type": "application/json"},
        json={
            "inputs": [text],
            "target_language_code": "hi-IN",
            "speaker": speaker,
            "pitch": pitch,
            "pace": pace,
            "loudness": 1.0,
            "speech_sample_rate": 22050,
            "enable_preprocessing": True,
            "model": "bulbul:v2",
        },
        timeout=60,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Sarvam HTTP {resp.status_code}: {resp.text[:200]}")
    audio_b64 = resp.json()["audios"][0]
    with open(out_wav, "wb") as f:
        f.write(base64.b64decode(audio_b64))


def _duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True,
    )
    return float(out.stdout.strip() or 0)


def generate(script_path: str) -> dict:
    _load_env()
    os.makedirs(OUT_DIR, exist_ok=True)
    spec = json.load(open(script_path))
    v = spec.get("voice", {})
    speaker = v.get("speaker", "vidya")
    pace = float(v.get("pace", 1.0))
    pitch = float(v.get("pitch", 0))

    seg_wavs, timings, cursor = [], [], 0.0
    for seg in spec["segments"]:
        wav = os.path.join(OUT_DIR, f"{seg['id']}.wav")
        seg_pace = float(seg.get("pace", pace))
        print(f"  voicing [{seg['id']}] (pace {seg_pace}) …")
        _tts(seg["voice_hi"], speaker, seg_pace, pitch, wav)
        dur = _duration(wav)
        seg_wavs.append(wav)
        timings.append({"id": seg["id"], "start": round(cursor, 3), "end": round(cursor + dur, 3),
                        "duration": round(dur, 3), "captions": seg.get("captions", [])})
        cursor += dur

    # concat all segment wavs → single mp3
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for w in seg_wavs:
            f.write(f"file '{w}'\n")
        listfile = f.name
    final_mp3 = os.path.join(OUT_DIR, "voiceover.mp3")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                    "-c:a", "libmp3lame", "-q:a", "2", final_mp3],
                   capture_output=True)
    os.unlink(listfile)

    result = {"voiceover": os.path.relpath(final_mp3, ROOT), "total": round(cursor, 3), "segments": timings}
    json.dump(result, open(os.path.join(OUT_DIR, "timings.json"), "w"), ensure_ascii=False, indent=2)
    print(f"  ✓ voiceover {result['total']}s → {result['voiceover']}")
    return result


if __name__ == "__main__":
    generate(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "engine/scripts/panchang.json"))
