#!/usr/bin/env python3
"""
Pexels real cinematic B-roll fetcher (FREE).
Reads PEXELS_API_KEY from env (or archana-reels/.env).

For each script segment, searches Pexels for vertical (portrait) HD video,
picks the best clip, downloads it. This is the single biggest lever for
killing the "AI-slop" feel — real footage, not generated stills.

Usage:  python engine/broll_pexels.py engine/scripts/panchang.json
Out:    engine/broll/<segment_id>.mp4  +  engine/broll/manifest.json
"""
import os, sys, json
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "engine", "broll")
SEARCH_URL = "https://api.pexels.com/videos/search"


def _load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _pick_portrait_hd(videos: list, used_ids: set, min_secs: float = 0) -> tuple[int, str] | None:
    """Best portrait clip not already used. Prefers ~1080 wide, HD, long enough. (id, link)."""
    best, best_id, best_score = None, None, -1
    for vid in videos:
        vid_id = vid.get("id")
        if vid_id in used_ids:
            continue
        dur = vid.get("duration") or 0
        if min_secs and dur and dur < min_secs:
            continue  # too short for the segment (MPT-style duration match)
        for f in vid.get("video_files", []):
            w, h = f.get("width") or 0, f.get("height") or 0
            if not w or not h or h < w:  # portrait only
                continue
            score = 1000 - abs(1080 - w) + (200 if f.get("quality") == "hd" else 0)
            if h > 2400:  # avoid huge files
                score -= 300
            if score > best_score:
                best, best_id, best_score = f.get("link"), vid_id, score
    return (best_id, best) if best else None


def _search(query: str, key: str):
    resp = requests.get(
        SEARCH_URL,
        headers={"Authorization": key},
        params={"query": query, "orientation": "portrait", "size": "medium", "per_page": 8},
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Pexels HTTP {resp.status_code}: {resp.text[:200]}")
    return resp.json().get("videos", [])


def _download(url: str, dest: str):
    r = requests.get(url, stream=True, timeout=120)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(1 << 16):
            f.write(chunk)


def fetch(script_path: str) -> dict:
    _load_env()
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        raise RuntimeError("PEXELS_API_KEY not set — add it to archana-reels/.env (see .env.example)")
    os.makedirs(OUT_DIR, exist_ok=True)
    spec = json.load(open(script_path))

    manifest = []
    used_ids: set = set()  # dedupe clips across segments (no repeated footage)
    for seg in spec["segments"]:
        b = seg.get("broll", {})
        dest = os.path.join(OUT_DIR, f"{seg['id']}.mp4")
        need = float(seg.get("duration_hint", 0) or 0)
        # MPT-style: try the phrase, then the fallback, then each keyword on its own, then a generic
        terms = [b.get("query"), b.get("fallback")]
        if b.get("query"):
            terms += [w for w in b["query"].split() if len(w) > 3][:4]
        terms.append("indian temple spiritual")
        picked = None
        for q in [t for t in dict.fromkeys(terms) if t]:  # de-dupe terms, keep order
            print(f"  [{seg['id']}] searching: {q}")
            vids = _search(q, key)
            picked = _pick_portrait_hd(vids, used_ids, min_secs=need)
            if not picked:  # relax duration if nothing long enough
                picked = _pick_portrait_hd(vids, used_ids, min_secs=0)
            if picked:
                break
        if not picked:
            print(f"  [{seg['id']}] ⚠ no clip found")
            manifest.append({"id": seg["id"], "clip": None})
            continue
        vid_id, link = picked
        used_ids.add(vid_id)
        _download(link, dest)
        manifest.append({"id": seg["id"], "clip": os.path.relpath(dest, ROOT),
                         "motion": b.get("motion", "gentle-ken-burns")})
        print(f"  [{seg['id']}] ✓ {os.path.relpath(dest, ROOT)} (clip {vid_id})")

    json.dump({"clips": manifest}, open(os.path.join(OUT_DIR, "manifest.json"), "w"), indent=2)
    return {"clips": manifest}


if __name__ == "__main__":
    fetch(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "engine/scripts/panchang.json"))
