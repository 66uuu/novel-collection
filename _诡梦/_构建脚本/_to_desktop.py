# -*- coding: utf-8 -*-
"""把《诡梦》成品（3 份文本 + 2 张封面）平铺到两处桌面根目录。"""
import os
import shutil

BASE = r"<DESKTOP>/提示词\05_小说_诡梦"
COV = os.path.join(BASE, "封面")

FILES = [
    os.path.join(BASE, "《诡梦》.docx"),
    os.path.join(BASE, "《诡梦》.md"),
    os.path.join(BASE, "《诡梦》.txt"),
    os.path.join(COV, "封面_v1_纯场景.png"),
    os.path.join(COV, "封面_v2_背影.png"),
]

DESTS = [r"<LOCAL_ROOT>/Desktop", r"<USER_HOME>/Desktop"]

for f in FILES:
    assert os.path.exists(f), "missing: " + f

for d in DESTS:
    for f in FILES:
        dst = os.path.join(d, os.path.basename(f))
        shutil.copyfile(f, dst)
    print("copied 5 ->", d)

print("\n=== 桌面根目录核对 ===")
for d in DESTS:
    print("\n[" + d + "]")
    for f in FILES:
        n = os.path.basename(f)
        p = os.path.join(d, n)
        print("  ", n, os.path.getsize(p) if os.path.exists(p) else "MISSING")
