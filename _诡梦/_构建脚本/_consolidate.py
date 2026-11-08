# -*- coding: utf-8 -*-
"""把桌面上散落的《诡梦》成品合并进 <DESKTOP>/05_小说_诡梦。
原则：先做哈希比对，确认目标里已有完全相同的一份，才移除源副本；
      任何哈希不一致的文件一律保留，不覆盖、不删除。"""
import hashlib
import os
import shutil

DESK = r"<LOCAL_ROOT>/Desktop"
TARGET = os.path.join(DESK, "05_小说_诡梦")
COV = os.path.join(TARGET, "封面")
MENG = os.path.join(DESK, "梦")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_existing(name, size):
    """在目标目录里找同名同大小的文件，返回路径或 None"""
    for d in (TARGET, COV):
        p = os.path.join(d, name)
        if os.path.exists(p) and os.path.getsize(p) == size:
            return p
    return None


log = []
removed = []
kept = []

# 1) 桌面根目录散落的成品
loose = [
    "《诡梦》.docx",
    "《诡梦》.md",
    "《诡梦》.txt",
    "封面_v1_纯场景.png",
    "封面_v2_背影.png",
]
for name in loose:
    src = os.path.join(DESK, name)
    if not os.path.exists(src):
        log.append("跳过（桌面已无）: " + name)
        continue
    size = os.path.getsize(src)
    dst = find_existing(name, size)
    if dst and md5(src) == md5(dst):
        os.remove(src)
        removed.append(name)
        log.append("已合并并移除桌面副本: %s -> %s" % (name, dst))
    else:
        kept.append(name)
        log.append("!! 未找到一致副本，保留桌面文件: " + name)

# 2) 梦 文件夹里的三件套
if os.path.isdir(MENG):
    for name in sorted(os.listdir(MENG)):
        src = os.path.join(MENG, name)
        if not os.path.isfile(src):
            continue
        size = os.path.getsize(src)
        dst = find_existing(name, size)
        if dst and md5(src) == md5(dst):
            os.remove(src)
            removed.append(os.path.join("梦", name))
            log.append("已合并并移除: 梦\\%s -> %s" % (name, dst))
        else:
            # 目标没有的，直接搬进去
            shutil.copyfile(src, os.path.join(TARGET, name))
            os.remove(src)
            log.append("目标无此文件，已搬入: 梦\\%s" % name)
    # 清空后删目录
    try:
        os.rmdir(MENG)
        log.append("已删除空目录: 梦")
    except OSError as e:
        log.append("梦 目录非空或无法删除: %s" % e)

print("\n".join(log))
print("\n--- 最终结构 ---")
for root, dirs, files in os.walk(TARGET):
    rel = os.path.relpath(root, TARGET)
    print(("[根]" if rel == "." else "[" + rel + "]"))
    for f in sorted(files):
        print("   ", f, os.path.getsize(os.path.join(root, f)))
