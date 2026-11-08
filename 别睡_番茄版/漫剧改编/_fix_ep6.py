# -*- coding: utf-8 -*-
import io, json, re

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
with io.open(base + r"\storyboard.json", encoding="utf-8-sig") as f:
    sb = json.load(f)

ep6 = [e for e in sb["episodes"] if e["ep"] == 6][0]
segs = ep6["segments"]
byid = {s["id"]: s for s in segs}

def fix_cut(seg, idx, newsec, h3_old, h3_new):
    seg["cuts"][idx]["seconds"] = newsec
    if h3_old and h3_new:
        seg["h3Prompt"] = seg["h3Prompt"].replace(h3_old, h3_new)

# E06-02: shot2 (拍5) 1.1 -> 2.0 ; cut-point unchanged (2.50)
s = byid["E06-02"]
s["cuts"][1]["seconds"] = 2.0

# E06-12: shot2 (拍9) 1.6 -> 2.0 ; shot3 starts 4.10 -> 4.50
s = byid["E06-12"]
s["cuts"][1]["seconds"] = 2.0
s["h3Prompt"] = s["h3Prompt"].replace(
    "Picture 3 (from Shot 3) aligns with the 4.10-second mark",
    "Picture 3 (from Shot 3) aligns with the 4.50-second mark")
s["h3Prompt"] = s["h3Prompt"].replace(
    "[Shot 3] At 00:04.100, the camera cuts",
    "[Shot 3] At 00:04.500, the camera cuts")

# E06-21: shot2 (拍2) 1.8 -> 2.0 ; shot3 starts 4.30 -> 4.50
s = byid["E06-21"]
s["cuts"][1]["seconds"] = 2.0
s["h3Prompt"] = s["h3Prompt"].replace(
    "Picture 3 (from Shot 3) aligns with the 4.30-second mark",
    "Picture 3 (from Shot 3) aligns with the 4.50-second mark")
s["h3Prompt"] = s["h3Prompt"].replace(
    "[Shot 3] At 00:04.300, the camera cuts",
    "[Shot 3] At 00:04.500, the camera cuts")

with io.open(base + r"\storyboard.json", "w", encoding="utf-8", newline="") as f:
    json.dump(sb, f, ensure_ascii=False, indent=2)

total = sum(sum(c["seconds"] for c in s["cuts"]) for s in segs)
print("fixed. EP6 total seconds: %.1f" % total)
