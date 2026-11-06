// Records the last tab of a running Chromium through a CDP screencast.
// Each frame is saved as <index>_<epoch-ms>.jpg, so build.py can time it.
// Stop the recording by creating the STOP file in the output folder.
//
// Usage: node record.mjs <cdp-url> <out-dir>
//   node record.mjs http://localhost:9334 ./rec
// Needs the `playwright` package (only to connect over CDP).
import { chromium } from "playwright";
import fs from "node:fs";
import path from "node:path";

const [cdpUrl = "http://localhost:9222", outDir = "./rec"] = process.argv.slice(2);
const framesDir = path.join(outDir, "frames");
const stopFile = path.join(outDir, "STOP");
fs.mkdirSync(framesDir, { recursive: true });
fs.rmSync(stopFile, { force: true });

const browser = await chromium.connectOverCDP(cdpUrl);
const context = browser.contexts()[0];
const page = context.pages().at(-1);
const session = await context.newCDPSession(page);

let count = 0;
session.on("Page.screencastFrame", async (frame) => {
  const name = `${String(count++).padStart(6, "0")}_${Math.round(frame.metadata.timestamp * 1000)}.jpg`;
  fs.writeFileSync(path.join(framesDir, name), Buffer.from(frame.data, "base64"));
  await session.send("Page.screencastFrameAck", { sessionId: frame.sessionId }).catch(() => {});
});
await session.send("Page.startScreencast", { format: "jpeg", quality: 85, everyNthFrame: 1 });
console.log(`recording ${page.url()} -> ${framesDir}`);

while (!fs.existsSync(stopFile)) await new Promise((r) => setTimeout(r, 1000));
await session.send("Page.stopScreencast").catch(() => {});
console.log(`stopped after ${count} frames`);
process.exit(0);
