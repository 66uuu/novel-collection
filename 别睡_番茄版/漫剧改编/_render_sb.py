# -*- coding: utf-8 -*-
import io, subprocess, os

base = r"<DESKTOP>/别睡_番茄版\漫剧改编"
skill = r"<USER_HOME>/DoubaoWork\skills\novel-storyboard\scripts\novel-storyboard.mjs"

def render(args, out):
    cmd = ["node", skill, "render", base + r"\storyboard.json"] + args + [
        "--script", base + r"\script.json",
        "--outline", base + r"\别睡-outline.json",
        "--art", base + r"\art.json",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=base)
    if r.returncode != 0:
        print("FAIL", out, r.returncode)
        print(r.stdout[-2000:])
        print(r.stderr[-2000:])
        return
    with io.open(out, "w", encoding="utf-8", newline="") as f:
        f.write(r.stdout)
    print("OK", os.path.basename(out), len(r.stdout))

render(["--md"], base + r"\别睡-storyboard.md")
render(["--html"], base + r"\storyboard-report.html")
