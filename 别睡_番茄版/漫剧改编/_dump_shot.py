# -*- coding: utf-8 -*-
import io, json

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
with io.open(base + r"\storyboard.json", encoding="utf-8-sig") as f:
    sb = json.load(f)

want = {
    3: ["E03-01", "E03-19"],
    4: ["E04-06", "E04-16"],
    5: ["E05-01", "E05-13"],
    6: ["E06-02", "E06-05", "E06-20"],
}
for ep in sb["episodes"]:
    if ep["ep"] in want:
        for seg in ep["segments"]:
            if seg["id"] in want[ep["ep"]]:
                print("=== %s ===" % seg["id"])
                for i, c in enumerate(seg["cuts"], start=1):
                    print("  cut%d seconds=%.2f chars=%s" % (i, c["seconds"], c.get("characters")))
                    print("    frame: %s" % c["frame"])
                    print("    shot : %s" % c["shot"])
