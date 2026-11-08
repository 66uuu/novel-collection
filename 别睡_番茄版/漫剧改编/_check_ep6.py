# -*- coding: utf-8 -*-
import io, json, re

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
def load(p):
    with io.open(p, encoding="utf-8-sig") as f:
        return json.load(f)

sb = load(base + r"\storyboard.json")
script = load(base + r"\script.json")
ep6 = [e for e in sb["episodes"] if e["ep"] == 6][0]
segs = ep6["segments"]
ep6s = [e for e in script["episodes"] if e["ep"] == 6][0]

errors = []

ids = [s["id"] for s in segs]
if ids != ["E06-%02d" % i for i in range(1, len(segs)+1)]:
    errors.append("ids not consecutive")

scene_map = {}
for s in segs:
    tot = sum(c["seconds"] for c in s["cuts"])
    if not (0 < tot <= 15.001):
        errors.append("%s total %.2f" % (s["id"], tot))
    for c in s["cuts"]:
        if not (2 <= c["seconds"] <= 5.001):
            errors.append("%s cut %.2fs" % (s["id"], c["seconds"]))
    scene_map.setdefault(s["sceneIndex"], []).append(s)

beatmap = {}
for si, sc in enumerate(ep6s["scenes"], start=1):
    beatmap[si] = list(sc["flow"])

for si, flow in beatmap.items():
    claimed = []
    for s in scene_map.get(si, []):
        for c in s["cuts"]:
            claimed.append(c["beats"])
    flat = []
    for lo, hi in claimed:
        flat.extend(range(lo, hi+1))
    if flat != list(range(1, len(flow)+1)):
        errors.append("scene %d beats %s vs %d" % (si, claimed, len(flow)))

for s in segs:
    cuts = s["cuts"]
    n = len(cuts)
    h3 = s["h3Prompt"]
    # count distinct [Shot k] tokens in body (after the alignment line)
    body = h3.split("integrated_multimodal_description:")[-1]
    toks = re.findall(r"\[Shot (\d+)\]", body)
    if toks != [str(k) for k in range(1, n+1)]:
        errors.append("%s body shot tokens %s" % (s["id"], toks))
    # alignment
    if n == 1:
        if "For the target video, at 0.00 seconds" not in h3:
            errors.append("%s single-shot missing I2VA line" % s["id"])
    else:
        acc = 0.0
        m = re.search(r"Picture 1 \(from Shot 1\) aligns with the ([\d.]+)-second mark", h3)
        if not m or abs(float(m.group(1))-0.0) > 0.001:
            errors.append("%s pic1 align" % s["id"])
        for k in range(2, n+1):
            acc += cuts[k-2]["seconds"]
            pat = r"Picture %d \(from Shot %d\) aligns with the ([\d.]+)-second mark" % (k, k)
            m = re.search(pat, h3)
            if not m or abs(float(m.group(1)) - acc) > 0.005:
                errors.append("%s pic%d align got %s want %.3f" % (s["id"], k, m.group(1) if m else "-", acc))
            if not re.search(r"\[Shot %d\] At 00:%02d\.\d{3}," % (k, int(acc)), h3):
                errors.append("%s cuttime Shot %d %.3f" % (s["id"], k, acc))
    # lines verbatim
    flow = beatmap[s["sceneIndex"]]
    for c in cuts:
        lo, hi = c["beats"]
        for idx in range(lo-1, hi):
            bb = flow[idx]
            if "speaker" in bb:
                if ("<d>[Chinese]" + bb["line"] + "</d>") not in s["h3Prompt"]:
                    errors.append("%s line not verbatim: %s" % (s["id"], bb["line"][:14]))
        sp = sum(bb.get("seconds", 0) for bb in flow[lo-1:hi] if "speaker" in bb)
        if sp > c["seconds"] + 0.001:
            errors.append("%s speech %.2f > cut %.2f" % (s["id"], sp, c["seconds"]))
    # camera words per own shot
    for k, c in enumerate(cuts, start=1):
        seg = "[Shot %d]" % k
        idx = h3.find(seg, h3.find("integrated_multimodal_description:"))
        nxt = h3.find("[Shot %d]" % (k+1), idx+1) if k < n else h3.find("overall_soundscape:", idx+1)
        chunk = h3[idx:nxt] if nxt > idx else h3[idx:]
        cam = c["camera"].lower()
        # static shot -> "static shot" should appear; else camera word
        if cam not in chunk.lower():
            errors.append("%s shot%d camera '%s' not in its segment" % (s["id"], k, c["camera"]))
    # chars subset of scene chars
    flow_chars = set(ep6s["scenes"][s["sceneIndex"]-1].get("characters", []))
    for c in cuts:
        for ch in c.get("characters", []):
            if ch not in flow_chars:
                errors.append("%s char %s not in scene %d chars" % (s["id"], ch, s["sceneIndex"]))
    # frame has size word
    for c in cuts:
        zw = {"extreme-wide": "大远景", "wide": "全景", "medium": "中景", "close": "特写", "extreme-close": "大特写"}[c["size"]]
        if zw not in c["frame"]:
            errors.append("%s frame lacks %s" % (s["id"], zw))
    # h3 body no char names
    for nm in ["苏晚", "张秀兰"]:
        if nm in body:
            errors.append("%s h3 body contains name %s" % (s["id"], nm))
    # six composition fields
    for c in cuts:
        for fld in ["lens", "cameraPosition", "composition", "eyeline", "focus", "stability"]:
            if fld not in c or not c[fld]:
                errors.append("%s missing %s" % (s["id"], fld))

total = sum(sum(c["seconds"] for c in s["cuts"]) for s in segs)
print("EP6 segments:", len(segs), "total: %.1f" % total)
print("errors:", len(errors))
for e in errors[:50]:
    print(" -", e)
