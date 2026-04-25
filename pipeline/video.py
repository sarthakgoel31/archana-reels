"""
Video assembler — combines scene PNGs + audio + music + captions into a 1080x1920 MP4 reel.
Uses FFmpeg for Ken Burns zoom, concatenation, audio mixing, and caption overlay.
"""

import os
import subprocess
import tempfile


def _get_duration(path: str) -> float:
    """Get media duration in seconds."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", path],
            capture_output=True, text=True,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def _scene_to_video(png_path: str, duration: float, output_path: str, zoom_direction: str = "in"):
    """Convert a single PNG to a video clip with Ken Burns zoom effect."""
    if zoom_direction == "in":
        zoom_expr = "1+0.15*on/(25*{dur})".format(dur=duration)
    else:
        zoom_expr = "1.08-0.15*on/(25*{dur})".format(dur=duration)

    fps = 25
    frames = int(duration * fps)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", png_path,
        "-vf", (
            f"scale=8000:-1,"
            f"zoompan=z='{zoom_expr}'"
            f":x='iw/2-(iw/zoom/2)'"
            f":y='ih/2-(ih/zoom/2)'"
            f":d={frames}:s=1080x1920:fps={fps},"
            f"format=yuv420p"
        ),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-t", str(duration),
        output_path,
    ]

    subprocess.run(cmd, capture_output=True, check=True)


def _concat_videos(video_paths: list, output_path: str):
    """Concatenate video clips using FFmpeg concat demuxer."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for path in video_paths:
            f.write(f"file '{path}'\n")
        concat_file = f.name

    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            output_path,
        ]
        subprocess.run(cmd, capture_output=True, check=True)
    finally:
        os.unlink(concat_file)


def _mix_audio(video_path: str, voiceover_path: str, music_path: str, output_path: str):
    """Mix voiceover + background music onto video."""
    if music_path and os.path.exists(music_path):
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", voiceover_path,
            "-i", music_path,
            "-filter_complex", (
                "[1:a]volume=1.0[vo];"
                "[2:a]volume=0.25,aloop=loop=-1:size=2e+09[bgloop];"
                "[bgloop]atrim=0:{dur}[bg];"
                "[vo][bg]amix=inputs=2:duration=first:dropout_transition=2[a]"
            ).format(dur=_get_duration(voiceover_path) + 2),
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path,
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", voiceover_path,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_path,
        ]

    subprocess.run(cmd, capture_output=True, check=True)


def _burn_captions(video_path: str, ass_path: str, output_path: str):
    """Burn ASS subtitles onto video."""
    if not ass_path or not os.path.exists(ass_path):
        return video_path

    # Copy ASS to a simple temp path to avoid FFmpeg filter escaping issues
    temp_ass = os.path.join(os.path.dirname(video_path), "subs.ass")
    import shutil
    shutil.copy2(ass_path, temp_ass)

    # Need to re-encode video to burn subtitles
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"ass={temp_ass}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "copy",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(temp_ass)

    if result.returncode != 0:
        print(f"  Caption burn failed: {result.stderr[-300:]}")
        # Fallback: copy without captions
        shutil.copy2(video_path, output_path)

    return output_path


def assemble(
    scene_images: list,
    scene_durations: list,
    voiceover_path: str,
    output_path: str,
    music_path: str = None,
) -> str:
    """
    Assemble final reel from scene images + audio.

    Args:
        scene_images: list of PNG paths
        scene_durations: duration in seconds for each scene
        voiceover_path: path to voiceover audio
        output_path: final MP4 output path
        music_path: optional background music path

    Returns: path to final MP4
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = os.path.join(output_dir, "_temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Adjust scene durations to match voiceover length
    voiceover_duration = _get_duration(voiceover_path)
    total_scene_duration = sum(scene_durations)

    if voiceover_duration > 0 and total_scene_duration > 0:
        scale = voiceover_duration / total_scene_duration
        scene_durations = [d * scale for d in scene_durations]

    # Step 1: Convert each scene PNG to video clip with Ken Burns
    print("  Rendering scene clips...")
    clip_paths = []
    for i, (img, dur) in enumerate(zip(scene_images, scene_durations)):
        clip_path = os.path.join(temp_dir, f"clip_{i:02d}.mp4")
        zoom = "in" if i % 2 == 0 else "out"
        _scene_to_video(img, dur, clip_path, zoom_direction=zoom)
        clip_paths.append(clip_path)
        print(f"    Clip {i+1}/{len(scene_images)}: {dur:.1f}s")

    # Step 2: Concatenate all clips
    print("  Concatenating clips...")
    concat_path = os.path.join(temp_dir, "concat.mp4")
    _concat_videos(clip_paths, concat_path)

    # Step 3: Mix audio
    print("  Mixing audio...")
    audio_mix_path = os.path.join(temp_dir, "with_audio.mp4")
    _mix_audio(concat_path, voiceover_path, music_path, audio_mix_path)

    # Step 4: Copy final output
    import shutil
    shutil.copy2(audio_mix_path, output_path)

    # Cleanup temp files
    for f in os.listdir(temp_dir):
        os.unlink(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    duration = _get_duration(output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"  Final: {output_path} ({duration:.1f}s, {size_mb:.1f}MB)")

    return output_path
