#!/usr/bin/env node
// Loop content engine — one reel, end to end.
// voice (Sarvam) → b-roll (Pexels) → dense re-encode → compose (generator) → render (HyperFrames)
//
// Usage: node engine/make.mjs <spec.json> --out <name> [--primary #..] [--accent #..] [--bg #..]
//                              [--jobs-file <path> --job-id <id>]   (optional: live job updates)
import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const arg = (k, d) => { const i = process.argv.indexOf(`--${k}`); return i > -1 ? process.argv[i + 1] : d; };

const spec = process.argv[2];
const out = arg("out", "reel");
const primary = arg("primary", "#E8A33D");
const accent = arg("accent", "#F4D58D");
const bg = arg("bg", "#0d0a05");
const jobsFile = arg("jobs-file");
const jobId = arg("job-id");

function updateJob(patch) {
  if (!jobsFile || !jobId || !existsSync(jobsFile)) return;
  try {
    const jobs = JSON.parse(readFileSync(jobsFile, "utf8"));
    const j = jobs.find((x) => x.id === jobId);
    if (j) { Object.assign(j, patch); writeFileSync(jobsFile, JSON.stringify(jobs, null, 2)); }
  } catch {}
}

function run(cmd, args, opts = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, args, { cwd: ROOT, stdio: "inherit", ...opts });
    p.on("close", (code) => (code === 0 ? resolve() : reject(new Error(`${cmd} ${args.join(" ")} → exit ${code}`))));
  });
}

const PY = path.join(ROOT, ".venv", "bin", "python");

async function main() {
  const start = Date.now();
  try {
    updateJob({ status: "voicing", step: "Sarvam voiceover" });
    await run(PY, ["engine/voice_sarvam.py", spec]);

    // MPT-borrowed: word-align captions to the spoken voiceover (precise sync).
    // Purge any previous alignment FIRST — a stale file from another script would
    // burn that script's captions onto this reel if alignment fails.
    updateJob({ step: "aligning captions" });
    try { unlinkSync(path.join(ROOT, "engine/voice/caption_timings.json")); } catch {}
    try { await run(PY, ["engine/align_captions.py"]); }
    catch (e) { console.log("  caption align skipped:", e.message); }

    const specObj = JSON.parse(readFileSync(path.resolve(ROOT, spec), "utf8"));
    if (!specObj.stills) {
      updateJob({ status: "broll", step: "Pexels footage" });
      await run(PY, ["engine/broll_pexels.py", spec]);

      // dense-keyframe re-encode for smooth motion (+ trim long clips)
      updateJob({ step: "optimizing footage" });
      const manifest = JSON.parse(readFileSync(path.join(ROOT, "engine/broll/manifest.json"), "utf8"));
      for (const c of manifest.clips) {
        if (!c.clip) continue;
        const f = path.join(ROOT, c.clip);
        const tmp = f.replace(/\.mp4$/, "_kf.mp4");
        await run("ffmpeg", ["-y", "-i", f, "-t", "16", "-c:v", "libx264", "-r", "30", "-g", "30",
          "-keyint_min", "30", "-crf", "21", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", tmp],
          { stdio: "ignore" });
        await run("mv", [tmp, f], { stdio: "ignore" });
      }
    }

    updateJob({ status: "rendering", step: "composing + rendering" });
    const generator = specObj.treatment === "kinetic"
      ? "engine/build_composition_kinetic.mjs"
      : "engine/build_composition.mjs";
    await run("node", [generator, spec, "--primary", primary, "--accent", accent, "--bg", bg]);
    const outPath = path.join("engine/out", `${out}.mp4`);
    await run("npx", ["--yes", "hyperframes@latest", "render", "--output", `out/${out}.mp4`], { cwd: path.join(ROOT, "engine") });

    const durationSec = Math.round((Date.now() - start) / 1000);
    updateJob({ status: "done", step: undefined, outputPath: `archana-reels/${outPath}`, durationSec, costInr: 0 });
    console.log(`\n✓ ${out} done in ${durationSec}s → ${outPath}`);
  } catch (e) {
    updateJob({ status: "failed", error: String(e.message || e) });
    console.error(`\n✗ failed: ${e.message || e}`);
    process.exit(1);
  }
}
main();
