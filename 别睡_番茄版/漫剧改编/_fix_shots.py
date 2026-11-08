# -*- coding: utf-8 -*-
import io, json, re

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
with io.open(base + r"\storyboard.json", encoding="utf-8-sig") as f:
    sb = json.load(f)

def clean_shot(shot):
    # remove <d>...</d> blocks (with content) and speaker tags
    s = re.sub(r"<d>.*?</d>", "", shot, flags=re.DOTALL)
    s = re.sub(r"\(S\d+(?:, [^)]*)?\)", "", s)
    # clean leftover colons / commas / spaces around removed blocks
    s = re.sub(r"\s*：\s*", "：", s)
    s = re.sub(r"[：,，]\s*$", "", s)
    s = re.sub(r"\s{2,}", " ", s)
    s = s.replace("： ", "：")
    s = s.replace(" ，", "，").replace(" 。", "。")
    return s.strip()

def ident_for(cut):
    chars = cut.get("characters", [])
    if "C02" in chars: return "白衣身影"
    if "C03" in chars: return "中年女人"
    if "C04" in chars: return "中年男人"
    if "C05" in chars: return "护士"
    if "C01" in chars: return "年轻女子"
    return None

names = {"苏晚": "年轻女子", "妈妈": "中年女人", "张秀兰": "中年女人", "父亲": "中年男人"}

fixed_shots = 0
for ep in sb["episodes"]:
    for seg in ep.get("segments", []):
        for c in seg.get("cuts", []):
            if "shot" not in c:
                continue
            orig = c["shot"]
            s = clean_shot(orig)
            for k, v in names.items():
                s = s.replace(k, v)
            if s != orig:
                c["shot"] = s
                fixed_shots += 1

# E06-20 h3: remove the on-screen Chinese text
for ep in sb["episodes"]:
    if ep["ep"] == 6:
        for seg in ep["segments"]:
            if seg["id"] == "E06-20":
                seg["h3Prompt"] = seg["h3Prompt"].replace(
                    " a green message goes out: “到家了妈”.",
                    " a green message bubble goes out.")
                seg["h3Prompt"] = seg["h3Prompt"].replace(
                    "on the WeChat interface a green message goes out: “到家了妈”.",
                    "on the WeChat interface a green message bubble goes out.")

# E03-19 cut2: 2.9 -> 3.0, fix h3 alignment for shot3
for ep in sb["episodes"]:
    if ep["ep"] == 3:
        for seg in ep["segments"]:
            if seg["id"] == "E03-19":
                seg["cuts"][1]["seconds"] = 3.0
                seg["h3Prompt"] = seg["h3Prompt"].replace(
                    "Picture 3 (from Shot 3) aligns with the 5.40-second mark",
                    "Picture 3 (from Shot 3) aligns with the 5.50-second mark")
                seg["h3Prompt"] = seg["h3Prompt"].replace(
                    "[Shot 3] At 00:05.400, the camera cuts",
                    "[Shot 3] At 00:05.500, the camera cuts")

with io.open(base + r"\storyboard.json", "w", encoding="utf-8", newline="") as f:
    json.dump(sb, f, ensure_ascii=False, indent=2)

print("fixed shots:", fixed_shots)

# dump remaining "她" occurrences in shot
remaining = []
for ep in sb["episodes"]:
    for seg in ep.get("segments", []):
        for i, c in enumerate(seg.get("cuts", []), start=1):
            if "她" in c.get("shot", ""):
                remaining.append((seg["id"], i, c.get("characters"), c["shot"]))
print("remaining 她 in shot:", len(remaining))
for segid, i, chars, shot in remaining:
    print(" - %s#%d chars=%s : %s" % (segid, i, chars, shot))
