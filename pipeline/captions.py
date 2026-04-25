"""
Animated caption generator — creates ASS subtitles for FFmpeg overlay.
Splits voiceover text into timed phrases and generates styled subtitle file.
"""

import os
import re


# ASS header with spiritual styling
ASS_HEADER = """[Script Info]
Title: Archana Reel Captions
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans Devanagari,52,&H00FFFFFF,&H000000FF,&H00000000,&HA0000000,-1,0,0,0,100,100,0,0,3,3,0,2,60,60,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _split_into_phrases(text: str, max_chars: int = 60) -> list:
    """Split text into readable phrases for captions."""
    # Split on sentence boundaries
    sentences = re.split(r'[।\.\?!]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    phrases = []
    for sentence in sentences:
        if len(sentence) <= max_chars:
            phrases.append(sentence)
        else:
            # Split long sentences on comma, dash, or mid-point
            parts = re.split(r'[,—–]+', sentence)
            current = ""
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if len(current) + len(part) + 2 <= max_chars:
                    current = f"{current}, {part}" if current else part
                else:
                    if current:
                        phrases.append(current)
                    current = part
            if current:
                phrases.append(current)

    return phrases


def _format_ass_time(seconds: float) -> str:
    """Format seconds to ASS timestamp (H:MM:SS.cc)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def generate_captions(
    voiceover_text: str,
    audio_duration: float,
    output_path: str,
    fade_ms: int = 200,
) -> str:
    """
    Generate an ASS subtitle file with animated captions.

    Args:
        voiceover_text: the Hindi voiceover text
        audio_duration: total audio duration in seconds
        output_path: where to save the .ass file
        fade_ms: fade in/out duration in milliseconds

    Returns: path to generated .ass file
    """
    phrases = _split_into_phrases(voiceover_text)

    if not phrases:
        return None

    # Calculate timing: distribute proportionally by character count
    total_chars = sum(len(p) for p in phrases)
    # Leave 0.5s gap at start and end
    usable_duration = audio_duration - 1.0
    start_offset = 0.5

    lines = []
    current_time = start_offset

    for phrase in phrases:
        # Duration proportional to character count, with min 1.5s
        char_ratio = len(phrase) / total_chars
        duration = max(1.5, char_ratio * usable_duration)

        start = current_time
        end = current_time + duration

        # ASS fade effect: {\fad(fade_in_ms, fade_out_ms)}
        fade_tag = f"{{\\fad({fade_ms},{fade_ms})}}"
        escaped = phrase.replace("\\", "\\\\")

        line = f"Dialogue: 0,{_format_ass_time(start)},{_format_ass_time(end)},Default,,0,0,0,,{fade_tag}{escaped}"
        lines.append(line)

        # Small gap between phrases
        current_time = end + 0.15

    # Write ASS file
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        f.write("\n".join(lines))
        f.write("\n")

    print(f"  Captions: {len(phrases)} phrases, {output_path}")
    return output_path
