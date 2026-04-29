# Archana Reels

**AI-powered spiritual content pipeline for Instagram reels -- zero cost, fully automated.**

Archana Reels generates ready-to-post Instagram reels from Hindu spiritual content. Give it a content type (panchang, rashifal, temple, pooja, navgrah, mythology), and it produces a complete video with Hindi script, AI-generated backgrounds, text-to-speech narration, and animated scene compositions.

Built as the content engine for [myarchana.in](https://myarchana.in).

## Content Types

| Type | Description |
|---|---|
| **Panchang** | Daily Hindu calendar -- tithi, nakshatra, deity of the day, recommended pooja |
| **Rashifal** | Daily horoscope for each rashi with lucky color, number, and action item |
| **Temple** | Featured temple spotlight with history and significance |
| **Pooja** | Pooja explainer -- benefits, procedure, best timing |
| **Navgrah** | Planetary influence for the day with remedial poojas |
| **Mythology** | Short mythology stories tied to deities and festivals |

## Pipeline

```
Content Selection --> Script Writing --> TTS Voiceover --> AI Image Generation --> Scene Rendering --> Video Assembly
```

Each stage is a separate module:

1. **ContentEngine** -- Picks today's content using date-based rotation across temples, poojas, and rashis
2. **ScriptWriter** -- Generates Hindi scripts with hooks, scene breakdowns, and CTAs
3. **TTS** -- Converts scripts to speech using edge-tts (free, no API key required)
4. **Images** -- Generates scene backgrounds via Pollinations.ai (free, no API key required)
5. **Scenes** -- Renders text overlays and compositions using HTML templates + Playwright screenshots
6. **Video** -- Assembles final reel from scenes, voiceover, captions, and background music

## Project Structure

```
archana-reels/
  generate.py          -- CLI entry point
  pipeline/
    content.py         -- Content engine (date-based rotation)
    scriptwriter.py    -- Hindi script generation
    tts.py             -- Text-to-speech via edge-tts
    images.py          -- AI image generation via Pollinations.ai
    scenes.py          -- HTML template rendering with Playwright
    video.py           -- FFmpeg video assembly
    captions.py        -- Subtitle generation
    talking_head.py    -- Talking head overlay (experimental)
    data.py            -- Content database (temples, poojas, rashis, hooks, CTAs)
  templates/
    scene.html         -- Jinja2 template for scene rendering
  assets/
    music/             -- Background music tracks
  output/              -- Generated reels (date_type/ directories)
  data/                -- Supplementary content data
```

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3 |
| TTS | edge-tts (Microsoft Edge, free) |
| Image Generation | Pollinations.ai (free, no key) |
| Scene Rendering | Playwright + HTML/Jinja2 templates |
| Video Assembly | FFmpeg |
| Image Processing | Pillow |

Total API cost: **$0/month**

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Generate a panchang reel for today
python generate.py --type panchang

# Generate a rashifal reel for a specific rashi
python generate.py --type rashifal --rashi mesh

# Generate all content types
python generate.py --type all
```

Output lands in `output/YYYY-MM-DD_<type>/` with the final video, individual scenes, and voiceover audio.

## Usage

```bash
# Specific content types
python generate.py --type temple
python generate.py --type pooja
python generate.py --type navgrah
python generate.py --type mythology

# Custom date
python generate.py --type panchang --date 2026-05-01

# Skip image generation (use placeholders)
python generate.py --type panchang --skip-images
```

---

Built with [Claude Code](https://claude.ai/code)
