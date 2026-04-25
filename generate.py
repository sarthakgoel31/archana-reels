#!/usr/bin/env python3
"""
Archana Reels — AI spiritual content pipeline.
Generates ready-to-post Instagram reels from myarchana.in data.

Usage:
  python generate.py --type panchang
  python generate.py --type rashifal --rashi mesh
  python generate.py --type temple
  python generate.py --type pooja
  python generate.py --type navgrah
  python generate.py --type all
"""

import argparse
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))

from pipeline.content import ContentEngine
from pipeline.scriptwriter import ScriptWriter
from pipeline.tts import generate as generate_tts
from pipeline.images import generate_scene_backgrounds
from pipeline.scenes import render_scenes
from pipeline.video import assemble

PROJECT_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output")
MUSIC_DIR = os.path.join(PROJECT_DIR, "assets", "music")


def find_music() -> str:
    """Find a background music file if available."""
    if os.path.exists(MUSIC_DIR):
        for f in sorted(os.listdir(MUSIC_DIR)):
            if f.endswith((".mp3", ".wav", ".m4a")):
                return os.path.join(MUSIC_DIR, f)
    return None


def generate_reel(reel_type: str, rashi_slug: str = None, target_date: date = None, skip_images: bool = False, provider: str = None):
    """Generate a single reel end-to-end."""
    d = target_date or date.today()
    engine = ContentEngine()
    writer = ScriptWriter()

    print(f"\n{'='*60}")
    print(f"  Generating: {reel_type} reel for {d.isoformat()}")
    print(f"{'='*60}")

    # Step 1: Get content
    print("\n[1/6] Picking content...")
    if reel_type == "panchang":
        content = engine.get_panchang(d)
        script = writer.write_panchang(content)
    elif reel_type == "rashifal":
        content = engine.get_rashifal(d, rashi_slug)
        script = writer.write_rashifal(content)
    elif reel_type == "temple":
        content = engine.get_temple(d)
        script = writer.write_temple(content)
    elif reel_type == "pooja":
        content = engine.get_pooja(d)
        script = writer.write_pooja(content)
    elif reel_type == "navgrah":
        content = engine.get_navgrah(d)
        script = writer.write_navgrah(content)
    elif reel_type == "mythology":
        content = engine.get_mythology(d, rashi_slug)  # rashi_slug doubles as story_slug
        script = writer.write_mythology(content)
    else:
        print(f"Unknown type: {reel_type}")
        return

    print(f"  Hook: {script.scenes[0].title_hi}")
    print(f"  Scenes: {len(script.scenes)}")

    reel_dir = os.path.join(OUTPUT_DIR, f"{d.isoformat()}_{reel_type}")
    os.makedirs(reel_dir, exist_ok=True)

    # Save script
    script_path = os.path.join(reel_dir, "script.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"Type: {reel_type}\nDate: {d.isoformat()}\n")
        f.write(f"Hook: {script.scenes[0].title_hi}\n\n")
        f.write(f"--- VOICEOVER ---\n{script.voiceover_hi}\n\n")
        f.write(f"--- SCENES ---\n")
        for i, s in enumerate(script.scenes):
            f.write(f"\nScene {i+1} ({s.scene_type}, {s.duration_sec}s, bg={s.bg_style}):\n")
            f.write(f"  Title: {s.title_hi}\n")
            if s.body_hi:
                f.write(f"  Body: {s.body_hi}\n")
            if s.subtitle_hi:
                f.write(f"  Subtitle: {s.subtitle_hi}\n")
            if s.items:
                f.write(f"  Items: {s.items}\n")

    # Step 2: Generate TTS (1.5x speed)
    print("\n[2/6] Generating voiceover (1.5x speed)...")
    tts_result = generate_tts(
        text=script.voiceover_hi,
        output_dir=reel_dir,
        filename="voiceover",
        voice="male",
    )
    print(f"  Audio: {tts_result['duration_sec']:.1f}s")

    # Step 3: Generate AI background images
    bg_images = None
    if not skip_images:
        print("\n[3/6] Generating AI backgrounds (FLUX.2 → Pollinations fallback)...")
        date_seed = int(d.strftime("%Y%m%d"))
        story_data = content.story if reel_type == "mythology" else None
        bg_images = generate_scene_backgrounds(script.scenes, date_seed=date_seed, story_data=story_data, provider=provider)
        generated = sum(1 for img in bg_images if img)
        print(f"  Generated: {generated}/{len(script.scenes)} backgrounds")
    else:
        print("\n[3/6] Skipping AI backgrounds (--no-images)")

    # Step 4: Render scenes (with AI backgrounds)
    print("\n[4/6] Rendering scenes...")
    scenes_dir = os.path.join(reel_dir, "scenes")
    scene_images = render_scenes(script.scenes, scenes_dir, bg_images=bg_images)

    # Step 5: Assemble video (captions rendered into scene images)
    print("\n[5/5] Assembling video...")
    scene_durations = [s.duration_sec for s in script.scenes]
    music_path = find_music()
    if music_path:
        print(f"  Music: {os.path.basename(music_path)}")

    output_mp4 = os.path.join(reel_dir, f"{reel_type}.mp4")
    assemble(
        scene_images=scene_images,
        scene_durations=scene_durations,
        voiceover_path=tts_result["audio_path"],
        output_path=output_mp4,
        music_path=music_path,
    )

    print(f"\n  Done! -> {output_mp4}")
    print(f"{'='*60}\n")
    return output_mp4


def main():
    parser = argparse.ArgumentParser(description="Archana Reels Generator")
    parser.add_argument("--type", "-t", required=True,
                        choices=["panchang", "rashifal", "temple", "pooja", "navgrah", "mythology", "all"],
                        help="Type of reel to generate")
    parser.add_argument("--rashi", "-r", default=None,
                        help="Rashi slug for rashifal, or story slug for mythology")
    parser.add_argument("--date", "-d", default=None,
                        help="Target date (YYYY-MM-DD)")
    parser.add_argument("--no-images", action="store_true",
                        help="Skip AI image generation (use gradient backgrounds)")
    parser.add_argument("--provider", "-p", default=None,
                        choices=["flux2", "pollinations"],
                        help="Force image provider (skip cascade)")

    args = parser.parse_args()
    target_date = date.fromisoformat(args.date) if args.date else date.today()

    if args.type == "all":
        for t in ["panchang", "rashifal", "temple", "pooja", "navgrah", "mythology"]:
            try:
                generate_reel(t, target_date=target_date, skip_images=args.no_images, provider=args.provider)
            except Exception as e:
                print(f"  ERROR generating {t}: {e}")
                import traceback
                traceback.print_exc()
    else:
        generate_reel(args.type, rashi_slug=args.rashi, target_date=target_date, skip_images=args.no_images, provider=args.provider)


if __name__ == "__main__":
    main()
