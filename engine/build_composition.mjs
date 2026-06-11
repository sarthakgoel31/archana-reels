#!/usr/bin/env node
// Composition generator — emits a HyperFrames index.html from a script-spec + real assets.
// This is the generalized version of the hand-tuned panchang reel: feed it any
// segments/captions/brand and it produces the same cinematic-devotional treatment.
//
// Usage: node engine/build_composition.mjs <spec.json> [--primary #E8A33D --accent #F4D58D --bg #0d0a05]
// Reads: engine/voice/timings.json, engine/broll/manifest.json, engine/fonts.css
// Writes: engine/index.html
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => {
  const i = process.argv.indexOf(`--${k}`);
  return i > -1 ? process.argv[i + 1] : d;
};

const specPath = process.argv[2] || path.join(__dirname, "scripts/panchang.json");
const PRIMARY = arg("primary", "#E8A33D");
const ACCENT = arg("accent", "#F4D58D");
const BG = arg("bg", "#0d0a05");

const spec = JSON.parse(readFileSync(specPath, "utf8"));
const timings = JSON.parse(readFileSync(path.join(__dirname, "voice/timings.json"), "utf8"));
const manifest = JSON.parse(readFileSync(path.join(__dirname, "broll/manifest.json"), "utf8"));
const fonts = readFileSync(path.join(__dirname, "fonts.css"), "utf8");
// Optional: word-aligned caption timings (from align_captions.py). Precise > even-split.
let alignedCaps = null;
try {
  alignedCaps = JSON.parse(readFileSync(path.join(__dirname, "voice/caption_timings.json"), "utf8"));
} catch {}

const clipFor = (id) => {
  const m = manifest.clips.find((c) => c.id === id);
  return m?.clip ? path.basename(m.clip) : null;
};

const segs = timings.segments.map((t, i) => ({ ...t, idx: i, clip: clipFor(t.id) }));
const total = timings.total;

// Per-segment video clips: alternate tracks for 0.5s crossfade overlap.
const videoEls = segs
  .map((s, i) => {
    const track = i % 2;
    const start = i === 0 ? 0 : s.start;
    const dur = (i < segs.length - 1 ? segs[i + 1].start - s.start : total - s.start) + 0.6;
    const z = i + 1;
    const op = i === 0 ? "" : " opacity: 0;";
    return `      <div class="bw" id="w-${s.id}" style="z-index: ${z};${op}">
        <video class="bv" id="v-${s.id}" data-start="${start.toFixed(2)}" data-duration="${dur.toFixed(2)}" data-track-index="${track}" src="broll/${s.clip}" muted playsinline></video>
      </div>`;
  })
  .join("\n");

// GSAP: ken burns + crossfade per segment.
const kb = ["1.0,1.09", "1.08,1.0", "1.0,1.1", "1.06,1.0"];
const videoTl = segs
  .map((s, i) => {
    const dur = (i < segs.length - 1 ? segs[i + 1].start - s.start : total - s.start) + 0.6;
    const [from, to] = kb[i % kb.length].split(",");
    let t = `        tl.fromTo("#w-${s.id}", { scale: ${from} }, { scale: ${to}, duration: ${dur.toFixed(2)}, ease: "none" }, ${s.start.toFixed(2)});`;
    if (i > 0) t = `        tl.fromTo("#w-${s.id}", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power2.out" }, ${s.start.toFixed(2)});\n` + t;
    return t;
  })
  .join("\n");

const SEG_JSON = JSON.stringify(
  segs.map((s) => ({ id: s.id, start: s.start, end: s.end, captions: s.captions }))
);
// highlight the final caption of value + cta segments
const KEY = JSON.stringify(
  segs.filter((s) => s.id === "value" || s.id === "cta").map((s) => s.captions[s.captions.length - 1])
);
// Word-aligned captions (flattened) if available — else null → in-page even-split fallback.
const CAPS = alignedCaps
  ? JSON.stringify(alignedCaps.segments.flatMap((s) => s.captions.map((c) => ({ ...c }))))
  : "null";

const topline = spec.segments.find((s) => s.supporting_panchang)?.supporting_panchang?.join(" · ");
const brandFinalSub = "असली मंदिर · आपके नाम से";

const html = `<!doctype html>
<html lang="hi">
  <head>
    <meta charset="utf-8" />
    <style>
${fonts}

      #root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: ${BG}; font-family: "Inter", sans-serif; }
      .bw { position: absolute; inset: 0; will-change: transform, opacity; }
      .bv { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .scrim { position: absolute; inset: 0; z-index: 20; pointer-events: none;
        background:
          radial-gradient(120% 80% at 50% 30%, rgba(13,10,5,0) 35%, rgba(13,10,5,0.55) 100%),
          radial-gradient(140% 60% at 50% 115%, rgba(110,30,20,0.45) 0%, rgba(13,10,5,0) 55%); }
      .topline { position: absolute; top: 130px; left: 0; right: 0; z-index: 30; text-align: center;
        font-family: "Tiro Devanagari Hindi", serif; font-size: 40px; letter-spacing: 2px; color: ${ACCENT};
        opacity: 0; text-shadow: 0 2px 18px rgba(0,0,0,0.7); }
      .caps { position: absolute; left: 80px; right: 80px; top: 1180px; z-index: 30; text-align: center; }
      .cap { position: absolute; left: 0; right: 0; opacity: 0; font-family: "Tiro Devanagari Hindi", serif;
        font-size: 92px; line-height: 1.28; color: #f6eedd; text-shadow: 0 3px 26px rgba(0,0,0,0.85); }
      .cap.key { color: ${PRIMARY}; }
      .ul { display: block; height: 5px; width: 180px; margin: 22px auto 0; border-radius: 3px;
        background: linear-gradient(90deg, ${ACCENT}00, ${ACCENT}, ${ACCENT}00); transform: scaleX(0); transform-origin: 50% 50%; }
      .brand { position: absolute; bottom: 90px; left: 0; right: 0; z-index: 40; display: flex; align-items: center; justify-content: center; gap: 14px; opacity: 0; }
      .brand svg { width: 30px; height: 30px; }
      .brand span { font-family: "Inter", sans-serif; font-weight: 600; font-size: 38px; letter-spacing: 1px; color: #f6eedd; }
      .bf { position: absolute; inset: 0; z-index: 45; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; opacity: 0; }
      .bf .big { font-family: "Inter", sans-serif; font-weight: 700; font-size: 84px; color: #f6eedd; text-shadow: 0 0 40px ${PRIMARY}99; }
      .bf .sub { font-family: "Tiro Devanagari Hindi", serif; font-size: 40px; color: ${ACCENT}; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="root" data-start="0" data-duration="${total.toFixed(2)}" data-width="1080" data-height="1920">
${videoEls}
      <div class="scrim"></div>
${topline ? `      <div class="topline" id="topline">${topline}</div>` : ""}
      <div class="caps" id="caps"></div>
      <div class="brand" id="brand">
        <svg viewBox="0 0 24 24" fill="none" stroke="${PRIMARY}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 14c1.6 2 4.6 3 8 3s6.4-1 8-3" /><path d="M5 14h14" />
          <path d="M12 12c-1.3-1.2-1.1-3.1 0-4.2.3 1 .9 1.3 1.3 2.1.6 1.3-.1 2.8-1.3 2.1z" fill="${PRIMARY}" stroke="none" />
        </svg>
        <span>myarchana.in</span>
      </div>
      <div class="bf" id="bf"><div class="big">myarchana.in</div><div class="sub">${brandFinalSub}</div></div>
      <audio id="vo" data-start="0" data-duration="${total.toFixed(2)}" data-track-index="2" src="voice/voiceover.mp3" data-volume="1"></audio>
      <audio id="mus" data-start="0" data-duration="${total.toFixed(2)}" data-track-index="3" src="music.mp3" data-volume="0.16"></audio>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        const SEG = ${SEG_JSON};
        const KEY = ${KEY};
        const CAPS = ${CAPS};  // word-aligned [{text,start,end}] or null
        const capsRoot = document.getElementById("caps");
        const capEls = [];
        const mkCap = (text, t0, t1) => {
          const el = document.createElement("div");
          el.className = "cap" + (KEY.includes(text) ? " key" : "");
          el.innerHTML = text + '<span class="ul"></span>';
          capsRoot.appendChild(el);
          capEls.push({ el, ul: el.querySelector(".ul"), t0, t1 });
        };
        if (CAPS) {
          // precise: captions snapped to spoken words
          CAPS.forEach((c) => mkCap(c.text, c.start, c.end));
        } else {
          // fallback: even split within each segment
          SEG.forEach((s) => {
            const n = s.captions.length, span = (s.end - s.start) / n;
            s.captions.forEach((text, i) => mkCap(text, s.start + i * span, s.start + (i + 1) * span));
          });
        }

        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
${videoTl}
${topline ? `        tl.fromTo("#topline", { opacity: 0, y: -16 }, { opacity: 0.92, y: 0, duration: 0.6, ease: "power3.out" }, ${(segs[1]?.start + 0.4 || 4).toFixed(2)});
        tl.to("#topline", { opacity: 0, duration: 0.5, ease: "power2.in" }, ${(segs[2]?.start - 0.4 || 10).toFixed(2)});` : ""}
        capEls.forEach(({ el, ul, t0, t1 }) => {
          tl.fromTo(el, { opacity: 0, y: 34 }, { opacity: 1, y: 0, duration: 0.36, ease: "power3.out" }, t0 + 0.05);
          tl.fromTo(ul, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, t0 + 0.12);
          tl.to(el, { opacity: 0, y: -20, duration: 0.28, ease: "power2.in" }, t1 - 0.3);
        });
        tl.fromTo("#brand", { opacity: 0, y: 14 }, { opacity: 0.9, y: 0, duration: 0.7, ease: "power2.out" }, 1.2);
        tl.to("#brand", { opacity: 0, duration: 0.4, ease: "power2.in" }, ${(total - 6).toFixed(2)});
        tl.fromTo("#bf", { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.9, ease: "power3.out" }, ${(total - 3.5).toFixed(2)});
        window.__timelines["root"] = tl;
      </script>
    </div>
  </body>
</html>
`;

writeFileSync(path.join(__dirname, "index.html"), html);
console.log(`✓ composition built: ${segs.length} segments, ${total.toFixed(1)}s → engine/index.html`);
