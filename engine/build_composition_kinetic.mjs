#!/usr/bin/env node
// Kinetic composition generator — the hook-first treatment.
// Same asset contract as build_composition.mjs (timings.json, manifest.json,
// caption_timings.json, voiceover.mp3, music.mp3) but built for retention:
// sub-shot cuts every ~1.5s (data-media-start slices), white-flash hits on cuts,
// frame-one caption slam, punchy word-synced captions, bell SFX at the open.
//
// Usage: node engine/build_composition_kinetic.mjs <spec.json> [--primary --accent --bg]
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => {
  const i = process.argv.indexOf(`--${k}`);
  return i > -1 ? process.argv[i + 1] : d;
};

const specPath = process.argv[2] || path.join(__dirname, "scripts/panchang-kinetic.json");
const PRIMARY = arg("primary", "#E8A33D");
const ACCENT = arg("accent", "#F4D58D");
const BG = arg("bg", "#0d0a05");

const spec = JSON.parse(readFileSync(specPath, "utf8"));
const STILLS = !!spec.stills;
const timings = JSON.parse(readFileSync(path.join(__dirname, "voice/timings.json"), "utf8"));
const manifest = STILLS ? null : JSON.parse(readFileSync(path.join(__dirname, "broll/manifest.json"), "utf8"));
const fonts = readFileSync(path.join(__dirname, "fonts.css"), "utf8");
let alignedCaps = null;
try {
  alignedCaps = JSON.parse(readFileSync(path.join(__dirname, "voice/caption_timings.json"), "utf8"));
} catch {}

const clipFor = (id) => {
  if (STILLS) return spec.segments.find((s) => s.id === id)?.image ?? null;
  const m = manifest.clips.find((c) => c.id === id);
  return m?.clip ? path.basename(m.clip) : null;
};

const segs = timings.segments.map((t, i) => ({ ...t, idx: i, clip: clipFor(t.id) }));
const total = timings.total;

// ── One video per segment (proven media load), kinetic energy via jump-zooms ──
// Within each segment the wrapper jump-cuts between zoom levels with a white
// flash on every jump — reads as hard cuts without extra media elements.
const videoEls = segs
  .map((s, i) => {
    const track = i % 2;
    const start = i === 0 ? 0 : s.start;
    const segEnd = i < segs.length - 1 ? segs[i + 1].start : total;
    const dur = segEnd - start;
    const media = STILLS
      ? `<img class="bv" id="v-${s.id}" data-start="${start.toFixed(2)}" data-duration="${dur.toFixed(2)}" data-track-index="${track}" src="stills/${s.clip}">`
      : `<video class="bv" id="v-${s.id}" data-start="${start.toFixed(2)}" data-duration="${dur.toFixed(2)}" data-track-index="${track}" src="broll/${s.clip}" muted playsinline></video>`;
    return `      <div class="bw" id="w-${s.id}" style="z-index: ${i + 1}; opacity: ${i === 0 ? 1 : 0};">
        ${media}
      </div>`;
  })
  .join("\n");

// Jump-zoom choreography: each segment splits into 1-3 movements; every internal
// boundary gets an instant scale/rotation jump + flash. Segment changes flash too.
const shotTl = segs
  .map((s, i) => {
    const segEnd = i < segs.length - 1 ? segs[i + 1].start : total;
    const D = segEnd - s.start;
    const isCta = s.id === "cta";
    const n = isCta ? 1 : s.id === "hook" ? 3 : D > 4.4 ? 3 : D > 2.2 ? 2 : 1;
    const part = D / n;
    const lines = [];
    if (i > 0) {
      lines.push(`        tl.set("#w-${s.id}", { opacity: 1 }, ${s.start.toFixed(2)});`);
      lines.push(`        tl.fromTo("#flash", { opacity: 0.85 }, { opacity: 0, duration: 0.14, ease: "power2.out" }, ${s.start.toFixed(2)});`);
    }
    // zoom movement plan per part: [from, to, rotFrom, xFrom]
    const plans = [
      [1.03, 1.13, 0.9, -1.5],
      [1.22, 1.1, -1.1, 1.5],
      [1.02, 1.12, 0.7, -1.2],
    ];
    for (let k = 0; k < n; k++) {
      const t0 = s.start + k * part;
      const [from, to, rot, x] = isCta ? [1.0, 1.07, 0, 0] : plans[k % plans.length];
      if (k > 0) {
        lines.push(`        tl.fromTo("#flash", { opacity: 0.85 }, { opacity: 0, duration: 0.12, ease: "power2.out" }, ${t0.toFixed(2)});`);
      }
      lines.push(
        `        tl.fromTo("#w-${s.id}", { scale: ${from}, rotation: ${rot}, xPercent: ${x} }, { scale: ${to}, rotation: 0, xPercent: 0, duration: ${part.toFixed(2)}, ease: "power1.out" }, ${t0.toFixed(2)});`
      );
    }
    return lines.join("\n");
  })
  .join("\n");

const SEG_JSON = JSON.stringify(
  segs.map((s) => ({ id: s.id, start: s.start, end: s.end, captions: s.captions }))
);
const KEY = JSON.stringify(
  segs.filter((s) => s.id === "value" || s.id === "cta").map((s) => s.captions[s.captions.length - 1])
);
const CAPS = alignedCaps
  ? JSON.stringify(alignedCaps.segments.flatMap((s) => s.captions.map((c) => ({ ...c }))))
  : "null";

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
          radial-gradient(120% 80% at 50% 30%, rgba(13,10,5,0) 45%, rgba(13,10,5,0.42) 100%),
          radial-gradient(140% 60% at 50% 115%, rgba(110,30,20,0.32) 0%, rgba(13,10,5,0) 55%); }
      #flash { position: absolute; inset: 0; z-index: 25; background: #fff7e8; opacity: 0; pointer-events: none; }
      .caps { position: absolute; left: 60px; right: 60px; top: 1080px; z-index: 30; text-align: center; }
      .cap { position: absolute; left: 0; right: 0; opacity: 0; font-family: "Tiro Devanagari Hindi", serif;
        font-size: 100px; line-height: 1.22; color: #f8f0df; text-shadow: 0 4px 30px rgba(0,0,0,0.9), 0 0 60px rgba(0,0,0,0.5);
        will-change: transform, opacity; }
      .cap.key { color: ${PRIMARY}; }
      .cap.hookcap { font-size: 170px; font-weight: 700; color: ${PRIMARY};
        text-shadow: 0 6px 40px rgba(0,0,0,0.95), 0 0 90px ${PRIMARY}66; }
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
      <div id="flash"></div>
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
      <audio id="mus" data-start="0" data-duration="${total.toFixed(2)}" data-track-index="3" src="music.mp3" data-volume="0.3"></audio>
      <audio id="bell" data-start="0.05" data-track-index="4" src="sfx_bell.mp3" data-volume="0.55"></audio>

      <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
      <script>
        const SEG = ${SEG_JSON};
        const KEY = ${KEY};
        const CAPS = ${CAPS};
        const capsRoot = document.getElementById("caps");
        const capEls = [];
        const mkCap = (text, t0, t1, isFirst) => {
          const el = document.createElement("div");
          el.className = "cap" + (KEY.includes(text) ? " key" : "") + (isFirst ? " hookcap" : "");
          el.textContent = text;
          capsRoot.appendChild(el);
          capEls.push({ el, t0, t1, isFirst });
        };
        if (CAPS) {
          CAPS.forEach((c, i) => mkCap(c.text, c.start, c.end, i === 0));
        } else {
          let first = true;
          SEG.forEach((s) => {
            const n = s.captions.length, span = (s.end - s.start) / n;
            s.captions.forEach((text, i) => { mkCap(text, s.start + i * span, s.start + (i + 1) * span, first); first = false; });
          });
        }

        window.__timelines = window.__timelines || {};
        const tl = gsap.timeline({ paused: true });
${shotTl}
        capEls.forEach(({ el, t0, t1, isFirst }) => {
          if (isFirst) {
            tl.fromTo(el, { opacity: 0, scale: 2.3 }, { opacity: 1, scale: 1, duration: 0.38, ease: "back.out(1.7)" }, Math.max(0.1, t0));
            tl.to(el, { opacity: 0, scale: 0.94, duration: 0.18, ease: "power2.in" }, t1 - 0.18);
          } else {
            tl.fromTo(el, { opacity: 0, y: 26, scale: 0.86 }, { opacity: 1, y: 0, scale: 1, duration: 0.22, ease: "back.out(2.2)" }, t0 + 0.02);
            tl.to(el, { opacity: 0, y: -16, duration: 0.16, ease: "power2.in" }, t1 - 0.16);
          }
        });
        tl.fromTo("#brand", { opacity: 0, y: 14 }, { opacity: 0.9, y: 0, duration: 0.7, ease: "power2.out" }, 1.4);
        tl.to("#brand", { opacity: 0, duration: 0.4, ease: "power2.in" }, ${(total - 6).toFixed(2)});
        tl.fromTo("#bf", { opacity: 0, scale: 0.94 }, { opacity: 1, scale: 1, duration: 0.9, ease: "power3.out" }, ${(total - 3.2).toFixed(2)});
        window.__timelines["root"] = tl;
      </script>
    </div>
  </body>
</html>
`;

writeFileSync(path.join(__dirname, "index.html"), html);
console.log(`✓ kinetic composition: ${segs.length} segments (jump-zoom cuts), ${total.toFixed(1)}s → engine/index.html`);
