"""
Scene renderer — renders HTML templates to 1080x1920 PNGs using Playwright.
Supports AI-generated background images via data URL embedding.
"""

import os
import base64
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
VIEWPORT = {"width": 1080, "height": 1920}

# Icons for data items (rotated per item)
ITEM_ICONS = ["🪔", "📿", "🔱", "🙏", "⭐", "🕉️", "💫", "🌺"]


def _image_to_data_url(image_path: str) -> str:
    """Convert a local image file to a base64 data URL."""
    if not image_path or not os.path.exists(image_path):
        return ""
    ext = os.path.splitext(image_path)[1].lower()
    mime = {"jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    mime_type = mime.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:{mime_type};base64,{b64}"


def _render_scene_html(scene, template_env, bg_image_path=None) -> str:
    """Render a scene to HTML string using Jinja2 template."""
    template = template_env.get_template("scene.html")

    # Extract rashi symbol if present in title
    rashi_symbol = ""
    title = scene.title_hi
    if scene.scene_type == "deity" and len(title) > 0 and ord(title[0]) > 9000:
        rashi_symbol = title[0]
        title = title[2:].strip() if len(title) > 2 else title

    # Convert background image to data URL for embedding
    bg_data_url = _image_to_data_url(bg_image_path) if bg_image_path else ""

    return template.render(
        scene_type=scene.scene_type,
        bg_style=scene.bg_style,
        title_hi=title,
        subtitle_hi=scene.subtitle_hi or "",
        body_hi=scene.body_hi or "",
        caption_hi=scene.caption_hi if hasattr(scene, 'caption_hi') else "",
        items=scene.items or [],
        item_icons=ITEM_ICONS,
        rashi_symbol=rashi_symbol,
        bg_image_url=bg_data_url,
    )


def render_scenes(scenes: list, output_dir: str, bg_images: list = None) -> list:
    """
    Render all scenes to PNG images.

    Args:
        scenes: list of Scene objects
        output_dir: directory to save PNGs
        bg_images: optional list of background image paths (same length as scenes)

    Returns: list of PNG file paths
    """
    os.makedirs(output_dir, exist_ok=True)
    template_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    png_paths = []

    if bg_images is None:
        bg_images = [None] * len(scenes)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport=VIEWPORT, device_scale_factor=1)

        for i, scene in enumerate(scenes):
            bg_img = bg_images[i] if i < len(bg_images) else None
            html_content = _render_scene_html(scene, template_env, bg_image_path=bg_img)

            page.set_content(html_content, wait_until="networkidle")
            page.wait_for_timeout(1500)

            png_path = os.path.join(output_dir, f"scene_{i:02d}.png")
            page.screenshot(path=png_path, full_page=False)
            png_paths.append(png_path)

            bg_label = "AI bg" if bg_img else "gradient"
            print(f"  Scene {i+1}/{len(scenes)}: {scene.scene_type} ({bg_label})")

        browser.close()

    return png_paths
