# -*- coding: utf-8 -*-
"""把《诡梦》三份交付文件同步到两处桌面，并整理封面目录。
策略：先把旧名文件 mv 成新名（不做删除），再用新内容覆盖。"""
import os
import shutil

BASE = r"<DESKTOP>/提示词\05_小说_诡梦"
OLD = "《午睡醒来，鞋底沾着广西老家的泥》"
NEW = "《诡梦》"
SRC_MD = os.path.join(BASE, "正文.md")

DEST_DIRS = [r"<DESKTOP>/梦", r"<USER_HOME>/Desktop"]


def read_paras():
    raw = open(SRC_MD, encoding="utf-8").read()
    return [l.strip() for l in raw.split("\n") if l.strip()]


def write_md(path, paras):
    body = "\n\n".join(paras)
    with open(path, "w", encoding="utf-8-sig", newline="\n") as f:
        f.write("# " + NEW.strip("《》") + "\n\n" + body + "\n")


def write_txt(path, paras):
    with open(path, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(paras[0] + "\n\n")
        f.write("\n".join(paras[1:]) + "\n")


def main():
    paras = read_paras()
    assert paras[0] == "诡梦", paras[0]

    # 1) 工作目录内的 md / txt
    md_work = os.path.join(BASE, NEW + ".md")
    txt_work = os.path.join(BASE, NEW + ".txt")
    write_md(md_work, paras)
    write_txt(txt_work, paras)
    docx_work = os.path.join(BASE, NEW + ".docx")
    assert os.path.exists(docx_work)

    # 2) 两处桌面：先改名，再覆盖
    for d in DEST_DIRS:
        os.makedirs(d, exist_ok=True)
        for ext in (".docx", ".md", ".txt"):
            old_p = os.path.join(d, OLD + ext)
            new_p = os.path.join(d, NEW + ext)
            if os.path.exists(old_p) and not os.path.exists(new_p):
                os.rename(old_p, new_p)
                print("renamed:", new_p)
        shutil.copyfile(docx_work, os.path.join(d, NEW + ".docx"))
        shutil.copyfile(md_work, os.path.join(d, NEW + ".md"))
        shutil.copyfile(txt_work, os.path.join(d, NEW + ".txt"))
        print("copied 3 files ->", d)

    # 3) 封面目录整理
    cov = os.path.join(BASE, "封面")
    plan = [
        ("Chinese_web_novel_cover__minim_2026-10-20T17-34-56.png", "封面_v1_纯场景.png"),
        ("Chinese_web_novel_cover__minim_2026-10-20T17-36-04.png", "封面_v2_背影.png"),
    ]
    for src, dst in plan:
        sp = os.path.join(cov, src)
        if os.path.exists(sp):
            os.replace(sp, os.path.join(cov, dst))
            print("cover ->", dst)
    # 清掉自己生成的临时裁切图和旧书名废稿
    for fn in os.listdir(cov):
        if fn.startswith("_check_") or fn.startswith("_sub_") or fn.startswith("Chinese_web_novel_cover_design_2026-10-20T17-28-43"):
            os.remove(os.path.join(cov, fn))
            print("removed temp:", fn)

    # 4) 封面提示词存档（与图同名 .prompt.txt）
    src_prompt = r"<DESKTOP>/提示词\04_输出\封面提示词_诡梦_优化版.md"
    if os.path.exists(src_prompt):
        shutil.copyfile(src_prompt, os.path.join(cov, "封面_v1_纯场景.prompt.md"))
        shutil.copyfile(src_prompt, os.path.join(cov, "封面_v2_背影.prompt.md"))
        print("prompt archived")

    print("\n=== 结果 ===")
    for d in [BASE, os.path.join(BASE, "封面")] + DEST_DIRS:
        print("\n[" + d + "]")
        for fn in sorted(os.listdir(d)):
            if fn.endswith((".png", ".docx", ".md", ".txt")):
                print("  ", fn, os.path.getsize(os.path.join(d, fn)))


if __name__ == "__main__":
    main()
