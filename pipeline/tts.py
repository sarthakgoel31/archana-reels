"""
Text-to-Speech wrapper using edge-tts.
Generates Hindi voiceover audio + SRT subtitles.
"""

import asyncio
import os
import json
import edge_tts

# Hindi neural voices
VOICES = {
    "male": "hi-IN-MadhurNeural",       # calm male narrator
    "female": "hi-IN-SwaraNeural",       # female narrator
}

DEFAULT_VOICE = "male"
DEFAULT_RATE = "+0%"    # normal 1x speed
DEFAULT_PITCH = "-2Hz"  # slightly deeper


async def _generate_async(
    text: str,
    output_audio: str,
    output_srt: str = None,
    voice: str = None,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> dict:
    """Generate audio and optional SRT subtitles from Hindi text."""
    voice_id = VOICES.get(voice or DEFAULT_VOICE, voice or VOICES[DEFAULT_VOICE])

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice_id,
        rate=rate,
        pitch=pitch,
    )

    # Generate audio
    submaker = edge_tts.SubMaker()
    audio_chunks = []

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            submaker.feed(chunk)

    # Write audio
    with open(output_audio, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    # Write SRT subtitles
    if output_srt:
        srt_content = submaker.get_srt()
        with open(output_srt, "w", encoding="utf-8") as f:
            f.write(srt_content)

    # Get audio duration using ffprobe
    duration = _get_duration(output_audio)

    return {
        "audio_path": output_audio,
        "srt_path": output_srt,
        "duration_sec": duration,
        "voice": voice_id,
    }


def _get_duration(audio_path: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    try:
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", audio_path],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def generate(
    text: str,
    output_dir: str,
    filename: str = "voiceover",
    voice: str = None,
    rate: str = DEFAULT_RATE,
) -> dict:
    """
    Synchronous wrapper for TTS generation.

    Returns: dict with audio_path, srt_path, duration_sec
    """
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.join(output_dir, f"{filename}.mp3")
    srt_path = os.path.join(output_dir, f"{filename}.srt")

    result = asyncio.run(_generate_async(
        text=text,
        output_audio=audio_path,
        output_srt=srt_path,
        voice=voice,
        rate=rate,
    ))

    return result
