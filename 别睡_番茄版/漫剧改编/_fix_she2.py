# -*- coding: utf-8 -*-
import io, json

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
with io.open(base + r"\storyboard.json", encoding="utf-8-sig") as f:
    sb = json.load(f)

for ep in sb["episodes"]:
    for seg in ep.get("segments", []):
        for c in seg.get("cuts", []):
            s = c.get("shot", "")
            if seg["id"] == "E06-03" and "白衣身影看着她" in s:
                c["shot"] = s.replace("白衣身影看着她", "白衣身影看着年轻女子")
            if seg["id"] == "E06-04" and "年轻女子眼泪一下下来了，她点头" in s:
                c["shot"] = s.replace("年轻女子眼泪一下下来了，她点头", "年轻女子眼泪一下下来了，用力点头")

with io.open(base + r"\storyboard.json", "w", encoding="utf-8", newline="") as f:
    json.dump(sb, f, ensure_ascii=False, indent=2)

# final verify
bad = []
for ep in sb["episodes"]:
    for seg in ep.get("segments", []):
        for i, c in enumerate(seg.get("cuts", []), start=1):
            s = c.get("shot", "")
            for tok in ["她", "苏晚", "晚晚", "妈妈", "张秀兰", "苏建国", "父亲", "<d>"]:
                if tok in s:
                    bad.append((seg["id"], i, tok))
print("remaining:", len(bad), bad[:10])
