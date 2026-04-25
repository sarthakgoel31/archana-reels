"""
AI Talking Head generator — uses free HuggingFace Spaces.
Takes face image + audio → lip-synced video.

Requires: pip install --upgrade gradio_client

Spaces (ranked by quality, with fallback):
1. SkyReels A1 (Skywork/skyreels-a1-talking-head) — L40S GPU, highest quality
2. MoDA (multimodalart/MoDA-fast-talking-head) — ZeroGPU, emotion control
3. SadTalker API (akin23/SadTalker-API) — simplest, /predict endpoint
4. SadTalker (kevinwang676/SadTalker) — CPU, fn_index=0
"""

import shutil
import time
from pathlib import Path


def generate_talking_head(
    image_path: str,
    audio_path: str,
    output_path: str = "talking_head.mp4",
    timeout: int = 600,
) -> str:
    """
    Generate a talking head video with automatic fallback across HF Spaces.

    Args:
        image_path: Path to face image (PNG/JPG, frontal face recommended)
        audio_path: Path to audio file (WAV/MP3, max ~60s per call)
        output_path: Where to save the output MP4
        timeout: Max seconds to wait per space

    Returns: Path to the generated video

    Tips:
        - Frontal face photo, neutral expression, good lighting
        - WAV audio more reliable than MP3
        - For >60s, split audio into chunks, generate clips, concat with ffmpeg
    """
    try:
        from gradio_client import Client, handle_file
    except ImportError:
        raise ImportError("pip install --upgrade gradio_client")

    # --- Provider 1: SadTalker API (most reliable, simple API) ---
    try:
        print("  Trying SadTalker API...")
        start = time.time()
        client = Client("akin23/SadTalker-API", verbose=False)
        result = client.predict(
            source_image=handle_file(image_path),
            driven_audio=handle_file(audio_path),
            api_name="/predict",
        )
        elapsed = time.time() - start

        video_path = _extract_video_path(result)
        if video_path and Path(video_path).exists():
            shutil.copy2(video_path, output_path)
            print(f"  -> SadTalker API: {elapsed:.0f}s -> {output_path}")
            return output_path
    except Exception as e:
        print(f"  -> SadTalker API failed: {e}")

    # --- Provider 2: SadTalker (CPU, fn_index=0) ---
    try:
        print("  Trying SadTalker...")
        start = time.time()
        client = Client("kevinwang676/SadTalker", verbose=False)
        result = client.predict(
            image_path,           # source_image (path)
            audio_path,           # input_audio (path)
            "crop",               # preprocess mode
            False,                # still_mode
            False,                # gfpgan enhancer
            2,                    # batch_size
            "256",                # face_model_resolution
            0,                    # pose_style
            fn_index=0,
        )
        elapsed = time.time() - start

        video_path = _extract_video_path(result)
        if video_path and Path(video_path).exists():
            shutil.copy2(video_path, output_path)
            print(f"  -> SadTalker: {elapsed:.0f}s -> {output_path}")
            return output_path
    except Exception as e:
        print(f"  -> SadTalker failed: {e}")

    # --- Provider 3: SkyReels A1 (GPU, highest quality) ---
    try:
        print("  Trying SkyReels A1...")
        start = time.time()
        client = Client("Skywork/skyreels-a1-talking-head", verbose=False)
        result = client.predict(
            handle_file(image_path),
            handle_file(audio_path),
            3.0,    # cfg_scale
            10,     # steps
        )
        elapsed = time.time() - start

        video_path = _extract_video_path(result)
        if video_path and Path(video_path).exists():
            shutil.copy2(video_path, output_path)
            print(f"  -> SkyReels A1: {elapsed:.0f}s -> {output_path}")
            return output_path
    except Exception as e:
        print(f"  -> SkyReels A1 failed: {e}")

    # --- Provider 4: MoDA (ZeroGPU) ---
    try:
        print("  Trying MoDA...")
        start = time.time()
        client = Client("multimodalart/MoDA-fast-talking-head", verbose=False)
        result = client.predict(
            handle_file(image_path),
            handle_file(audio_path),
            "None",    # emotion
            1.2,       # emotion_scale
        )
        elapsed = time.time() - start

        video_path = _extract_video_path(result)
        if video_path and Path(video_path).exists():
            shutil.copy2(video_path, output_path)
            print(f"  -> MoDA: {elapsed:.0f}s -> {output_path}")
            return output_path
    except Exception as e:
        print(f"  -> MoDA failed: {e}")

    raise RuntimeError("All HF Spaces failed. Try again later.")


def _extract_video_path(result) -> str | None:
    """Extract video file path from various gradio result formats."""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        # {video: filepath, subtitles: ...} or {path: ..., url: ...}
        return result.get("video") or result.get("path")
    if isinstance(result, (list, tuple)):
        # First element is usually the video
        item = result[0]
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return item.get("video") or item.get("path")
    return None
