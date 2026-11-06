"""Builds an MP4 from record.mjs frames.

Plays each segment at its own speed: real speed while the user acts, fast
forward while something loads. Adds the segment captions as a subtitle track
(no drawtext needed) and writes captions.srt and captions.vtt for web pages.

Usage: python3 build.py <rec-dir> <segments.json> <out.mp4>

segments.json, times in local time on the day of the recording:
  {"day": "2026-11-06", "segments": [
    ["00:34:57", "00:36:10", 1,  "1. Ask the assistant to set up the pod"],
    ["00:36:10", "00:39:00", 20, "Fast-forward 20x: the pod starts"]
  ]}
Frames outside every segment are dropped.
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys

MAX_GAP_S = 2.0   # a longer pause between frames plays as 2 s (before speed-up)
FPS = 30

rec_dir, segments_file, out_mp4 = sys.argv[1:4]
spec = json.load(open(segments_file))
frames_dir = os.path.join(rec_dir, "frames")


def epoch(hms):
    return dt.datetime.fromisoformat(f"{spec['day']}T{hms}").timestamp()


segments = [(epoch(a), epoch(b), speed, caption) for a, b, speed, caption in spec["segments"]]
frames = sorted(f for f in os.listdir(frames_dir) if f.endswith(".jpg"))

out_t, last_kept, prev_ts = 0.0, -1.0, None
kept, caption_start = [], {}
for name in frames:
    ts = int(name.split("_")[1].split(".")[0]) / 1000
    seg = next((s for s in segments if s[0] <= ts < s[1]), None)
    if seg is None:
        continue
    if prev_ts is not None:
        out_t += min(ts - prev_ts, MAX_GAP_S) / seg[2]
    prev_ts = ts
    caption_start.setdefault(seg[3], out_t)
    if out_t - last_kept >= 1 / FPS:
        kept.append((name, out_t))
        last_kept = out_t

concat = os.path.join(rec_dir, "concat.txt")
with open(concat, "w") as f:
    for i, (name, t) in enumerate(kept):
        nxt = kept[i + 1][1] if i + 1 < len(kept) else t + 2
        f.write(f"file '{os.path.abspath(os.path.join(frames_dir, name))}'\nduration {max(nxt - t, 1 / FPS):.4f}\n")
    f.write(f"file '{os.path.abspath(os.path.join(frames_dir, kept[-1][0]))}'\n")


def srt_time(x):
    return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x % 1 * 1000):03d}"


starts = sorted(caption_start.items(), key=lambda kv: kv[1])
srt = os.path.join(rec_dir, "captions.srt")
with open(srt, "w") as f:
    for i, (caption, t0) in enumerate(starts):
        t1 = starts[i + 1][1] if i + 1 < len(starts) else out_t + 2
        f.write(f"{i + 1}\n{srt_time(t0)} --> {srt_time(t1)}\n{caption}\n\n")
vtt_text = "WEBVTT\n\n" + re.sub(r"(\d\d:\d\d:\d\d),(\d\d\d)", r"\1.\2", open(srt).read())
open(os.path.join(rec_dir, "captions.vtt"), "w").write(vtt_text)

# Even width and height for H.264; the subtitle track is mov_text, so QuickTime shows it.
subprocess.run([
    "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
    "-f", "concat", "-safe", "0", "-i", concat, "-i", srt,
    "-map", "0:v", "-map", "1:s",
    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p", "-r", str(FPS),
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
    "-c:s", "mov_text", "-metadata:s:s:0", "language=eng",
    "-movflags", "+faststart", out_mp4,
], check=True, stdin=subprocess.DEVNULL)
print(f"{out_mp4}: {len(kept)} frames, {out_t:.0f} s")
