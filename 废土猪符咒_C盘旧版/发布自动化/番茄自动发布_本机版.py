# -*- coding: utf-8 -*-
"""
《废土：我只有一块猪符咒》番茄作家助手 · 自动发布脚本（本机版）
=================================================================
适用：在你自己的 Windows 电脑上运行（需已安装 Python + playwright + chromium，
      且 Chrome 已登录番茄作家助手网页版）。

为什么在本机跑而不是让 AI 跑：
  - AI 运行在命令行沙箱，无 GUI、无浏览器引擎、pip 被网络策略拦截，物理上发不了；
  - 本脚本用 launch_persistent_context 复用你本机已登录的 Chrome 会话，
    因此【不需要你的密码、也不需要复制 cookie】，登录态始终留在你机器上。

安全开关：
  - DRY_RUN = True  （默认）：只打印"将要做什么"，不点任何发布按钮。
    第一次务必用 True 跑一遍，肉眼确认章节/标题都正确，再改 False。
  - DRY_RUN = False：执行真实发布。请在 DRY_RUN 验证通过、且你已确认选择器无误后使用。

注意：发布点击部分的选择器（按钮/输入框）需要你本机首次 DRY_RUN 时，
       对照作家助手网页版的实际 DOM 填进去（脚本已用中文注释标出待填处）。
       我（AI）在此沙箱无浏览器，无法替你校准这些选择器。
=================================================================
"""
import os, sys, time, datetime, getpass
from playwright.sync import sync_playwright

# ========================= 配置区（按你的情况改） =========================
BASE_URL = "https://writer.fanqienovel.com"      # 作家助手网页版；若打不开，改成你登录后地址栏里的实际地址
MATDIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "发布物料")  # 含 30 章 txt
DRY_RUN  = True                                 # ★ 第一次务必 True；确认无误改 False
PER_DAY  = 2                                     # 每天发布章数（你要的是 2）
START    = datetime.date(2026, 10, 1)            # 第一天发布日期（改成你想要的）
CHROME_USER_DATA = r"C:/Users/%s/AppData/Local/Google/Chrome/User Data" % getpass.getuser()  # 本机 Chrome 用户数据目录

# 作品元信息（从 发布物料/发布清单.md 复制而来，已填好）
BOOK = {
    "title":   "废土：我只有一块猪符咒",
    "author":  "（在此填你的笔名）",
    "intro": ("林野一睁眼，穿成了废土矿场里最底层的编号戊-37。\n"
              "别人穿越，金手指是系统、老爷爷、神级血脉。他只有一块从2026年顺手带来的破石头——能从眼睛里射激光。\n"
              "问题是，这石头不是发电机，是换能器。射一次，抽一次他的命。\n"
              "出多少力，收多少命。这账，是分档的：一档点亮，五档透支烧寿元。\n"
              "不到万不得已不放；要放，就放能解决问题的那一下。\n"
              "从矿场活下来，到走出矿区，到搞懂这个世界的真相——他一边算账，一边把命往长了活。\n"
              "【轻松搞笑 · 群像 · 异能废土 · 信息差拉满】"),
    "tags":    ["穿越", "废土", "异能", "系统", "群像", "轻松", "搞笑", "热血"],
}
# ============================================================================

def log(*a):
    print("[发布]", *a, flush=True)

def load_chapters(matdir):
    chs = []
    for fn in sorted(os.listdir(matdir)):
        if fn.endswith(".txt") and fn[:2].isdigit():
            p = os.path.join(matdir, fn)
            title = fn.split("_", 1)[1].rsplit(".", 1)[0]
            body = open(p, encoding="utf-8").read().strip()
            chs.append((title, body))
    return chs

def main():
    chs = load_chapters(MATDIR)
    log("加载章节 %d 篇 | DRY_RUN=%s | 每天%d章 | 起始%s" % (len(chs), DRY_RUN, PER_DAY, START))
    if not chs:
        log("未发现章节 txt，请确认 发布物料/ 目录路径。退出。"); return

    with sync_playwright() as pw:
        log("启动复用本机 Chrome（持久会话）：%s" % CHROME_USER_DATA)
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=CHROME_USER_DATA, headless=False, args=["--no-sandbox"])
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(BASE_URL, wait_until="networkidle", timeout=30000)

        # 登录态检测：若被踢到登录页，停下让用户手动登录
        if "登录" in page.title() or page.url.rstrip("/") in (BASE_URL, BASE_URL + "/"):
            log("⚠ 未检测到登录态。请在弹出的浏览器里登录番茄作家助手，登录完成后回到此处按回车。")
            input("登录后按回车继续……")
            page.reload(wait_until="networkidle")

        # 发布流程
        if DRY_RUN:
            log("========== DRY RUN（不真实发布）==========")
            log("书名：%s" % BOOK["title"])
            log("简介字数：%d | 标签：%s" % (len(BOOK["intro"]), "、".join(BOOK["tags"])))
            for i, (title, body) in enumerate(chs):
                day = START + datetime.timedelta(days=i // PER_DAY)
                log("  第%02d章《%s》[%d字] -> 发布于 %s" % (i + 1, title, len(body), day.isoformat()))
            log("============================================")
            log("DRY RUN 完成，未做任何真实操作。")
            log("请确认：① 章节/标题/日期无误；② 打开作家助手网页版，按 F12 核对下列选择器；")
            log("        ③ 把 DRY_RUN 改为 False 再跑。")
            browser.close()
            return

        # ===== 真实发布（需你本机填选择器）=====
        # —— 下方选择器是占位，请对照你浏览器 F12 的实际 DOM 修改 ——
        # 1) 新建作品：点击"写新作品/新建"按钮
        #    page.click("text=新建作品")   # ← 改成页面实际文字或 CSS 选择器
        # 2) 填写书名/简介/标签
        #    page.fill("input[placeholder*='书名']", BOOK["title"])
        #    page.fill("textarea[placeholder*='简介']", BOOK["intro"])
        #    for t in BOOK["tags"]: page.fill("input[placeholder*='标签']", t); page.press(..., "Enter")
        # 3) 逐章创建并粘贴
        #    for i,(title,body) in enumerate(chs):
        #        page.click("text=写新章")
        #        page.fill("input[placeholder*='章节名']", title)
        #        page.fill("div.editor, textarea", body)   # ← 改成正文编辑器实际选择器
        #        day = START + timedelta(days=i//PER_DAY)
        #        # 设定时发布（若网页版支持）：填写发布时间 = day
        #        page.click("text=定时发布")
        #        page.fill("input[type=datetime-local]", day.isoformat()+"T09:00")
        #        page.click("text=保存并定时")
        #        time.sleep(1.5)
        log("⚠ 真实发布逻辑的选择器尚未填充（见上方注释占位）。")
        log("请在 DRY_RUN 通过后，按你浏览器实际 DOM 填好选择器，再设 DRY_RUN=False 执行。")
        browser.close()

if __name__ == "__main__":
    main()
