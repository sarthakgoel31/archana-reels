"""
AI image generation for scene backgrounds.

Pipeline:
  1. Generate image (FLUX.2 1024x1024 square → crop 9:16, or Pollinations 9:16 direct)
  2. AI upscale 2x with Real-ESRGAN (HuggingFace Space, free)
  3. Downscale to 1080x1920 (sharp, no pixelation)

All free, no API keys needed.
"""

import os
import hashlib
import requests
import urllib.parse
import time
import shutil
import tempfile
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "bg_cache")
TARGET_SIZE = (1080, 1920)
TARGET_RATIO = 9 / 16  # 0.5625

SCENE_PROMPTS = {
    "hook": [
        "ancient hindu temple interior dark dramatic lighting golden diyas burning spiritual atmosphere cinematic 4k",
        "dark dramatic hindu temple corridor oil lamps flickering golden light ancient stone pillars 4k cinematic",
        "close up of burning brass diya lamps in dark temple warm golden glow spiritual atmosphere 4k",
    ],
    "panchang": [
        "hindu temple silhouette at golden sunrise orange sky temple bells morning spiritual atmosphere 4k photography",
        "sunrise through ancient hindu temple archway golden light marigold garlands morning prayers 4k",
        "peaceful hindu temple courtyard at dawn golden sunlight brass bells flowers spiritual 4k photography",
    ],
    "deity": [
        "ornate golden hindu temple sanctum sanctorum divine golden light rays incense smoke spiritual sacred 4k",
        "ancient hindu temple inner chamber golden idol divine radiance flower offerings spiritual atmosphere 4k",
        "sacred hindu shrine golden decorations marigold garlands divine light devotional atmosphere 4k",
    ],
    "info": [
        "peaceful hindu temple garden courtyard marigold flowers oil lamps warm golden afternoon light 4k",
        "beautiful hindu temple verandah with carved pillars warm sunlight filtering through ancient architecture 4k",
        "serene hindu temple prayer hall brass bells flower garlands warm ambient light spiritual calm 4k",
    ],
    "data": [
        "intricate hindu temple ceiling golden carvings mandala patterns ornate warm light closeup 4k",
        "ornate hindu temple wall carvings golden patterns ancient architecture detail warm lighting 4k",
        "hindu temple floor with rangoli pattern marigold petals brass lamps warm golden light 4k",
    ],
    "cta": [
        "grand hindu temple entrance at twilight warm golden lamps silhouette devotees spiritual evening 4k",
        "majestic hindu temple steps at dusk warm lights evening sky devotional atmosphere grand 4k",
        "hindu temple gopuram tower at sunset golden hour warm spiritual grandeur 4k photography",
    ],
}

MYTHOLOGY_SUFFIX = ", hyperdetailed digital painting, cinematic lighting, volumetric fog, epic scale, concept art, trending on artstation, 8k ultra HD"

# ── Aspect ratio helpers ─────────────────────────────────────

def _crop_to_vertical(img: Image.Image) -> Image.Image:
    """Center-crop to 9:16 without stretching. Only used for square/landscape sources."""
    w, h = img.size
    current_ratio = w / h
    if abs(current_ratio - TARGET_RATIO) < 0.02:
        return img
    if current_ratio > TARGET_RATIO:
        new_w = int(h * TARGET_RATIO)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / TARGET_RATIO)
        top = (h - new_h) // 2
        return img.crop((0, top, w, top + new_h))


# ── AI Upscaler ──────────────────────────────────────────────

_UPSCALER_BROKEN = False  # Skip for session if upscaler is down


def _ai_upscale(img: Image.Image) -> Image.Image:
    """Upscale 2x with Real-ESRGAN via HuggingFace Spaces. Tries multiple, returns original on failure."""
    global _UPSCALER_BROKEN
    if _UPSCALER_BROKEN:
        return img

    try:
        from gradio_client import Client, handle_file
    except ImportError:
        return img

    # Save to temp file for upload
    tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
    img.save(tmp.name, "JPEG", quality=95)
    tmp.close()

    upscalers = [
        ("Hockman", "Hockman/real-esrgan-upscaler", "/process_and_get_output",
         lambda hf: {"img": hf(tmp.name)}),
        ("kotchu", "kotchu/real-esrgan", "/predict",
         lambda hf: {"filename": hf(tmp.name), "model": "realesrgan-x4plus", "scale": 2, "tta": False}),
    ]

    for name, space_id, api_name, args_fn in upscalers:
        try:
            client = Client(space_id, verbose=False)
            kwargs = args_fn(handle_file)
            result = client.predict(**kwargs, api_name=api_name)

            # Extract path from result
            if isinstance(result, (list, tuple)):
                result = result[0]
            path = result.get("path") if isinstance(result, dict) else str(result)

            if path and os.path.exists(path):
                upscaled = Image.open(path)
                if upscaled.size[0] > img.size[0]:
                    print(f"    -> ESRGAN ({name}): {img.size[0]}x{img.size[1]} → {upscaled.size[0]}x{upscaled.size[1]}")
                    os.unlink(tmp.name)
                    return upscaled
        except Exception as e:
            msg = str(e)
            if "GPU quota" in msg or "RUNTIME_ERROR" in msg or "PAUSED" in msg:
                continue  # Try next upscaler
            print(f"    -> ESRGAN ({name}): {str(e)[:80]}")

    # All upscalers failed
    _UPSCALER_BROKEN = True
    print(f"    -> All upscalers unavailable (skipping for session)")
    try:
        os.unlink(tmp.name)
    except:
        pass
    return img


def _finalize_image(img: Image.Image, needs_crop: bool = False) -> Image.Image:
    """Crop (if needed) → AI upscale → downscale to 1080x1920 → sharpen."""
    # Step 1: Crop to 9:16 if source is square (FLUX.2)
    if needs_crop:
        img = _crop_to_vertical(img)

    # Step 2: AI upscale 2x with Real-ESRGAN
    upscaled = _ai_upscale(img)

    # Step 3: Downscale to 1080x1920 (from ~1152x2048 or similar)
    if upscaled.size != TARGET_SIZE:
        final = upscaled.resize(TARGET_SIZE, Image.LANCZOS)
    else:
        final = upscaled

    # Step 4: Light sharpen + contrast (less aggressive since ESRGAN already sharpens)
    if upscaled.size[0] > img.size[0]:
        # ESRGAN worked — light touch only
        final = ImageEnhance.Contrast(final).enhance(1.03)
    else:
        # ESRGAN failed, fallback upscale — stronger enhancement
        final = final.filter(ImageFilter.UnsharpMask(radius=2.0, percent=130, threshold=3))
        final = ImageEnhance.Contrast(final).enhance(1.08)
        final = ImageEnhance.Color(final).enhance(1.05)

    return final


# ── Cache ────────────────────────────────────────────────────

def _get_cache_path(prompt: str, seed: int) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = hashlib.md5(f"{prompt}_{seed}_v3".encode()).hexdigest()[:12]
    return os.path.join(CACHE_DIR, f"{key}.jpg")


# ── Providers ────────────────────────────────────────────────

_EXHAUSTED_PROVIDERS = set()


def _generate_flux2_dev(prompt: str, seed: int) -> tuple[Image.Image | None, bool]:
    """FLUX.2-dev: 1024x1024 square (needs crop). Returns (image, needs_crop)."""
    if "flux2-dev" in _EXHAUSTED_PROVIDERS:
        return None, False
    try:
        from gradio_client import Client
        client = Client("black-forest-labs/FLUX.2-dev", verbose=False)
        result = client.predict(
            prompt=prompt, input_images=[], seed=seed, randomize_seed=False,
            width=1024, height=1024, num_inference_steps=30,
            guidance_scale=4.0, prompt_upsampling=True, api_name="/infer",
        )
        img_info = result[0]
        path = img_info.get("path") if isinstance(img_info, dict) else str(img_info)
        if path and os.path.exists(path):
            return Image.open(path), True
    except Exception as e:
        if "GPU quota" in str(e):
            _EXHAUSTED_PROVIDERS.add("flux2-dev")
            print(f"    -> FLUX.2-dev: GPU quota exhausted (skipping for session)")
        else:
            print(f"    -> FLUX.2-dev failed: {e}")
    return None, False


def _generate_flux2_klein(prompt: str, seed: int) -> tuple[Image.Image | None, bool]:
    """FLUX.2-klein: 1024x1024 square (needs crop). Returns (image, needs_crop)."""
    if "flux2-klein" in _EXHAUSTED_PROVIDERS:
        return None, False
    try:
        from gradio_client import Client
        client = Client("black-forest-labs/FLUX.2-klein-9B", verbose=False)
        result = client.predict(
            prompt=prompt, input_images=[], mode_choice="Distilled (4 steps)",
            seed=seed, randomize_seed=False, width=1024, height=1024,
            num_inference_steps=4, guidance_scale=1.0,
            prompt_upsampling=True, api_name="/generate",
        )
        img_info = result[0]
        path = img_info.get("path") if isinstance(img_info, dict) else str(img_info)
        if path and os.path.exists(path):
            return Image.open(path), True
    except Exception as e:
        if "GPU quota" in str(e):
            _EXHAUSTED_PROVIDERS.add("flux2-klein")
            print(f"    -> FLUX.2-klein: GPU quota exhausted (skipping for session)")
        else:
            print(f"    -> FLUX.2-klein failed: {e}")
    return None, False


def _generate_pollinations(prompt: str, seed: int) -> tuple[Image.Image | None, bool]:
    """Pollinations: 9:16 direct (576x1024, no crop needed). Returns (image, needs_crop)."""
    try:
        encoded = urllib.parse.quote(prompt)
        # Request 9:16 directly — Pollinations returns 576x1024
        url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&seed={seed}&nologo=true"
        resp = requests.get(url, timeout=180, stream=True)
        if resp.status_code == 200:
            return Image.open(BytesIO(resp.content)), False  # Already 9:16, no crop
    except Exception as e:
        print(f"    -> Pollinations failed: {e}")
    return None, False


# ── Main API ─────────────────────────────────────────────────

def generate_image(scene_type: str, seed: int = 42, variant: int = 0,
                   custom_prompt: str = None, provider: str = None) -> str:
    """Generate scene background: provider → crop → ESRGAN upscale → 1080x1920."""
    if custom_prompt:
        prompt = custom_prompt
        if not any(kw in prompt.lower() for kw in ["4k", "8k", "cinematic", "concept art"]):
            prompt += MYTHOLOGY_SUFFIX
    else:
        prompts = SCENE_PROMPTS.get(scene_type, SCENE_PROMPTS["info"])
        prompt = prompts[variant % len(prompts)]

    cache_path = _get_cache_path(prompt, seed)
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 50000:
        return cache_path

    print(f"    Generating {scene_type} background...")

    if provider == "pollinations":
        providers = [("Pollinations", _generate_pollinations)]
    elif provider == "flux2":
        providers = [("FLUX.2-dev", _generate_flux2_dev), ("FLUX.2-klein", _generate_flux2_klein)]
    else:
        providers = [
            ("FLUX.2-dev", _generate_flux2_dev),
            ("FLUX.2-klein", _generate_flux2_klein),
            ("Pollinations", _generate_pollinations),
        ]

    raw_img = None
    needs_crop = False
    for name, gen_fn in providers:
        print(f"    -> Trying {name}...")
        start = time.time()
        raw_img, needs_crop = gen_fn(prompt, seed)
        elapsed = time.time() - start
        if raw_img:
            print(f"    -> {name}: {raw_img.size[0]}x{raw_img.size[1]} in {elapsed:.0f}s")
            break

    if raw_img is None:
        print(f"    -> All providers failed for {scene_type}")
        return None

    # Crop (if square) → AI upscale → downscale → sharpen
    final = _finalize_image(raw_img, needs_crop=needs_crop)
    final.save(cache_path, "JPEG", quality=95)
    size_kb = os.path.getsize(cache_path) / 1024
    print(f"    -> Final {TARGET_SIZE[0]}x{TARGET_SIZE[1]}, {size_kb:.0f}KB")
    return cache_path


def generate_scene_backgrounds(scenes: list, date_seed: int = 42,
                               story_data: dict = None, provider: str = None) -> list:
    """Generate background images for all scenes."""
    paths = []
    mythology_scene_idx = 0

    for i, scene in enumerate(scenes):
        custom_prompt = None
        if scene.scene_type == "mythology" and story_data and "scenes" in story_data:
            if mythology_scene_idx < len(story_data["scenes"]):
                custom_prompt = story_data["scenes"][mythology_scene_idx].get("image_prompt")
                mythology_scene_idx += 1

        path = generate_image(
            scene_type=scene.scene_type, seed=date_seed + i * 7,
            variant=i, custom_prompt=custom_prompt, provider=provider,
        )
        paths.append(path)
    return paths
