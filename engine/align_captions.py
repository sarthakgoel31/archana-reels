#!/usr/bin/env python3
"""Word-level caption timing (MPT-borrowed technique).

Instead of dividing each segment's captions evenly across its time window, we run
Whisper with word timestamps on the voiceover and snap each caption to the words
actually being spoken — so captions land on the beat of the narration.

Usage: python engine/align_captions.py
Reads:  engine/voice/voiceover.mp3, engine/voice/timings.json
Writes: engine/voice/caption_timings.json  → [{id, captions:[{text,start,end}]}]
"""
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICE = ROOT / "engine" / "voice"


def _whisper_words(audio: str, model_name: str = "base") -> list[dict]:
    import whisper
    model = whisper.load_model(model_name)
    res = model.transcribe(audio, word_timestamps=True, fp16=False)
    words = []
    for seg in res.get("segments", []):
        for w in seg.get("words", []):
            words.append({"w": (w.get("word") or "").strip(), "start": float(w["start"]), "end": float(w["end"])})
    return words


def align(model_name: str = "base") -> dict:
    timings = json.load(open(VOICE / "timings.json"))
    audio = str(VOICE / "voiceover.mp3")
    if not os.path.exists(audio):
        print("no voiceover.mp3 — run voice_sarvam.py first", file=sys.stderr)
        return {}

    print(f"  aligning captions to spoken words (whisper {model_name})…")
    words = _whisper_words(audio, model_name)

    out = []
    for seg in timings["segments"]:
        caps = seg.get("captions", [])
        s, e = float(seg["start"]), float(seg["end"])
        # words spoken inside this segment's window
        seg_words = [w for w in words if w["start"] >= s - 0.15 and w["end"] <= e + 0.15]
        timed = []
        if caps and seg_words:
            n = len(caps)
            per = max(1, len(seg_words) // n)
            for i, text in enumerate(caps):
                grp = seg_words[i * per:(i + 1) * per] if i < n - 1 else seg_words[i * per:]
                if not grp:
                    # fall back to even split for this caption
                    span = (e - s) / n
                    timed.append({"text": text, "start": round(s + i * span, 3), "end": round(s + (i + 1) * span, 3)})
                else:
                    timed.append({"text": text, "start": round(grp[0]["start"], 3), "end": round(grp[-1]["end"], 3)})
        else:
            # no words detected → even split
            n = max(1, len(caps))
            span = (e - s) / n
            timed = [{"text": c, "start": round(s + i * span, 3), "end": round(s + (i + 1) * span, 3)} for i, c in enumerate(caps)]
        out.append({"id": seg["id"], "captions": timed})

    result = {"segments": out}
    json.dump(result, open(VOICE / "caption_timings.json", "w"), ensure_ascii=False, indent=2)
    print(f"  ✓ caption_timings.json ({sum(len(s['captions']) for s in out)} captions word-aligned)")
    return result


if __name__ == "__main__":
    align(sys.argv[1] if len(sys.argv) > 1 else "base")
