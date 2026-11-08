# -*- coding: utf-8 -*-
import io, json, re

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
def load(p):
    with io.open(p, encoding="utf-8-sig") as f:
        return json.load(f)

sb = load(base + r"\storyboard.json")
a = load(base + r"\_sb-ep6a.json")
b = load(base + r"\_sb-ep6b.json")
segs = a + b

ep6 = None
for ep in sb["episodes"]:
    if ep["ep"] == 6:
        ep6 = ep
        break
assert ep6 is not None, "ep6 not found"

errors = []

# 1. segment ids consecutive
ids = [s["id"] for s in segs]
expect = ["E06-%02d" % i for i in range(1, len(segs)+1)]
if ids != expect:
    errors.append("segment ids not consecutive: %s" % ids)

# 2. cut seconds 2-5, segment total <=15
scene_map = {}
for s in segs:
    tot = sum(c["seconds"] for c in s["cuts"])
    if not (0 < tot <= 15.001):
        errors.append("%s total %.2f out of range" % (s["id"], tot))
    for c in s["cuts"]:
        if not (2 <= c["seconds"] <= 5.001):
            errors.append("%s cut %.2fs out of 2-5" % (s["id"], c["seconds"]))
    scene_map.setdefault(s["sceneIndex"], []).append(s)

# 3. beats coverage vs seedScenes
seed = ep6.get("seedScenes")
if seed is None:
    errors.append("ep6 seedScenes missing")
else:
    for si, scene in enumerate(seed, start=1):
        sbeats = list(scene.get("beats", []))
        claimed = []
        for s in scene_map.get(si, []):
            for c in s["cuts"]:
                claimed.append(c["beats"])
        flat = []
        for lo, hi in claimed:
            flat.extend(range(lo, hi+1))
        if flat != list(range(1, len(sbeats)+1)):
            errors.append("scene %d beats claimed %s vs seed %d beats" % (si, claimed, len(sbeats)))
        for s in scene_map.get(si, []):
            for c in s["cuts"]:
                lo, hi = c["beats"]
                sp = sum(bb.get("seconds", 0) for bb in sbeats[lo-1:hi] if bb.get("kind") == "line")
                if sp > c["seconds"] + 0.001:
                    errors.append("%s cut beats %s speech %.2f > cut %.2f" % (s["id"], c["beats"], sp, c["seconds"]))

# 4. h3 alignment
for s in segs:
    cuts = s["cuts"]
    nshots = len(cuts)
    h3 = s["h3Prompt"]
    shotlines = re.findall(r"\[Shot (\d+)\]", h3)
    if len(shotlines) != nshots:
        errors.append("%s h3 has %d [Shot] vs %d cuts" % (s["id"], len(shotlines), nshots))
    else:
        for k in range(1, nshots+1):
            if str(k) not in shotlines:
                errors.append("%s missing [Shot %d]" % (s["id"], k))
    acc = 0.0
    for k, c in enumerate(cuts, start=1):
        if k == 1:
            m = re.search(r"Picture 1 \(from Shot 1\) aligns with the ([\d.]+)-second mark", h3)
            if not m or abs(float(m.group(1)) - 0.0) > 0.001:
                errors.append("%s align pic1 %s" % (s["id"], m.group(1) if m else "missing"))
        else:
            acc += cuts[k-2]["seconds"]
            pat = r"Picture %d \(from Shot %d\) aligns with the ([\d.]+)-second mark" % (k, k)
            m = re.search(pat, h3)
            if not m or abs(float(m.group(1)) - acc) > 0.005:
                errors.append("%s align pic%d %s want %.3f" % (s["id"], k, m.group(1) if m else "missing", acc))
            if not re.search(r"\[Shot %d\] At 00:%02d\.\d{3}," % (k, int(acc)), h3):
                errors.append("%s missing cut-time Shot %d at %.3f" % (s["id"], k, acc))
    if nshots == 1 and "For the target video, at 0.00 seconds" not in h3:
        errors.append("%s single-shot missing official I2VA line" % s["id"])

# 5. lines verbatim in <d>
script = load(base + r"\script.json")
ep6s = [e for e in script["episodes"] if e["ep"] == 6][0]
beatmap = {}
for si, sc in enumerate(ep6s["scenes"], start=1):
    beatmap[si] = list(sc["flow"])
for s in segs:
    flow = beatmap[s["sceneIndex"]]
    for c in s["cuts"]:
        lo, hi = c["beats"]
        for idx in range(lo-1, hi):
            bb = flow[idx]
            if "speaker" in bb:
                line = bb["line"]
                if ("<d>[Chinese]" + line + "</d>") not in s["h3Prompt"]:
                    errors.append("%s beats %s line not verbatim: %s" % (s["id"], c["beats"], line[:14]))

# --- apply ---
ep6["segments"] = segs
del ep6["seedScenes"]
with io.open(base + r"\storyboard.json", "w", encoding="utf-8", newline="") as f:
    json.dump(sb, f, ensure_ascii=False, indent=2)

print("segments:", len(segs), "total seconds: %.1f" % sum(sum(c["seconds"] for c in s["cuts"]) for s in segs))
print("errors:", len(errors))
for e in errors[:50]:
    print(" -", e)
