# -*- coding: utf-8 -*-
"""把 正文.md 渲染成排版好的 docx（书名已改为《诡梦》）。"""
import os
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

BASE = r"<DESKTOP>/提示词\05_小说_诡梦"
SRC = os.path.join(BASE, "正文.md")
TITLE = "诡梦"


def set_font(run, name="宋体", size=11, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), name)
    rfonts.set(qn("w:ascii"), name)
    rfonts.set(qn("w:hAnsi"), name)


def build(dst):
    raw = open(SRC, encoding="utf-8").read()
    lines = [l.rstrip() for l in raw.split("\n")]
    paras = [l for l in lines if l.strip()]

    doc = Document()
    sec = doc.sections[0]
    from docx.shared import Cm
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(3.0)

    # 标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(TITLE)
    set_font(r, "黑体", 26, bold=True)

    # 副标题
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    r = p.add_run("午睡醒来，鞋底沾着广西老家的泥")
    set_font(r, "楷体", 11, bold=False)
    r.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    # 正文（跳过首行原标题）
    body = paras[1:] if paras and paras[0] == TITLE else paras
    for line in body:
        txt = line.strip()
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = 1.5
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        # 小节号：纯数字 + 点
        is_sec = txt.endswith(".") and txt[:-1].isdigit()
        if is_sec:
            pf.space_before = Pt(14)
            pf.space_after = Pt(6)
            r = p.add_run(txt)
            set_font(r, "黑体", 13, bold=True)
        else:
            pf.first_line_indent = Pt(22)
            r = p.add_run(txt)
            set_font(r, "宋体", 11)

    doc.save(dst)
    return dst


if __name__ == "__main__":
    out = os.path.join(BASE, "《诡梦》.docx")
    build(out)
    print("saved:", out, os.path.getsize(out))
