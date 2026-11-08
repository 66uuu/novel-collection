# 《别睡》AI 漫剧 · 全资产交接包

> 本包由上一个 AI（豆包办公 MainAgent）在 2026-10-18 制作，用于把项目完整交接给下一个 AI 接力。
> 一切以包内 JSON 为准；本 README 只做索引与状态说明。

---

## 0. 项目一句话

把用户原创小说《别睡》（番茄版，约 10 万字）改编成 **AI 漫剧**：电影写实悬疑风，**6 集 × 每集约 3 分钟**。制作管线已全部走完（大纲 → 角色 → 美术 → 剧本 → 分镜 → 角色参考图 → EP1 出片），当前处于 **EP1 成片推进中**。

---

## 1. 目录结构（本包 = 原 `<DESKTOP>/别睡_番茄版\漫剧改编\` 全量）

| 路径 | 内容 |
|---|---|
| `别睡-原文.txt` | 小说 docx 提取的全文（唯一文本源） |
| `别睡-outline.json` / `别睡-outline.md` / `outline-report.html` | 6 集改编大纲（14 道门全过） |
| `别睡-cast.json` / `别睡-cast.md` / `cast-report.html` | 5 张角色卡 |
| `art.json` / `别睡-art.md` / `art-report.html` | 美术设定集：4 场景 + 6 道具（含出图提示词） |
| `script.json` / `别睡-script.md` / `script-report.html` | 6 集 19 场 124 句剧本 |
| `storyboard.json` / `别睡-storyboard.md` / `storyboard-report.html` | 6 集 111 段 295 镜分镜；**每段 h3Prompt（含逐字台词与切点）在此** |
| `character-refs.html` | 角色参考图总报告 |
| `character-refs\`（5 个角色目录） | 每角色 asset.json + 4 视图 PNG（20 张参考图） |
| `images\s01~s04.png` | 4 张场景设定图（16:9） |
| `images\p01~p06.png` | 6 张道具设定图（白底、无人无手） |
| `E01-01\` | EP1 第 1 段：4 张分镜帧 + **E01-01.mp4（13 秒成片样片）** |
| `E01-02\` ~ `E01-13\` | EP1 其余 12 段分镜帧（共 36 张，已全部出齐） |
| `_ep1_h3.md` | EP1 全部 13 段的完整 h3Prompt（出片直接用） |
| `card-*.json` / `*-intake.json` / `_*.py` / `_*.mjs` / `_*.json` | 中间产物与工具脚本（可忽略或复用） |

---

## 2. 角色 / 场景 / 道具 ID（出片时挂参考图用）

**角色（character-refs\<角色名>\default\ 下）：**
- C01 苏晚（26 岁，黑眼圈、憔悴）
- C02 白衣的她（与苏晚同一张脸，湿透青白衬衫、垂头看不见脸）
- C03 张秀兰（妈妈）｜C04 苏晚父亲｜C05 ICU 护士

**场景（images\）：** S01 出租屋卧室（EP1 全部 13 段都在此）｜S02 楼道｜S03 ICU病房｜S04 ICU走廊

**道具（images\）：** P01 手机（02:00 三格电）｜P02 床头水杯｜P03 便利贴 1 与 17｜P04 衣柜镜「别回头」｜P05 水果刀｜P06 青白旧衬衫

---

## 3. 出片状态（关键）

| 项目 | 状态 |
|---|---|
| EP1 分镜帧 | ✅ 13 段 40 张全部落盘（E01-01~13） |
| EP1 视频 | 🔶 仅 E01-01 已生成（13s，`E01-01\E01-01.mp4`）；**E01-02~13 共 12 段待生成** |
| EP2~EP6 视频 | ⬜ 未开始（分镜与提示词均已就绪） |

**为什么中断：** 2026-10-05~06 提交 E01-02/03 时视频生成额度用完（近 7 天额度耗尽，提示预计 10-12 恢复）。接替者应先试调一次 `image_to_video` 确认额度已恢复。

---

## 4. 出片参数口径（已与用户确认过）

- 模型：`seedance_2.0_fast`；比例 `16:9`；图生视频（`image_to_video`）
- 每段时长 = 该段 cuts 秒数之和，取整（见 storyboard.json 每段 cuts.seconds）：
  E01-02=8s ｜ E01-03=9s ｜ E01-04=13s ｜ E01-05=11s ｜ E01-06=14s ｜ E01-07=13s ｜ E01-08=10s ｜ E01-09=15s ｜ E01-10=12s ｜ E01-11=12s ｜ E01-12=14s ｜ E01-13=13s
- 每段 prompt 直接用 `_ep1_h3.md` 里该段的 h3Prompt（官方英文结构：对齐指令 + 镜头正文 + 台词逐字 + 声景 + 配乐）
- 参考图：把该段每切的分镜帧按序传入 `image_reference_url_list`（本地帧先上传成 URL 再传）
- 一次最多 2 个视频/批；出完立即交付并做 QC

**EP1 各段帧文件与对应 URL（2026-10-05 上传，可能已过期，过期就重新上传）：**
```
E01-02: f1=aQ4Ex9TgNo f2=EFkVI4m4q0
E01-03: f1=cgObirSrZR f2=SFsEVT9wiE f3=XBlCV2HDek
E01-04: f1=L3X6iuF562 f2=bUdXQvWOOv f3=UrxyGOTfUy
E01-05: f1=HVn85IAanp f2=Vey4Ic6oUa f3=U3QRTauDQS
E01-06: f1=TIebO9JdDj f2=y08UT5Wrco f3=Jq8DhilF6U
E01-07: f1=hld4MPqcSK f2=JaC6kObmUl f3=GKJzfEYTn6 f4=v4sBCpU6sX
E01-08: f1=LQGqo6WvBH f2=YXaKUOCZem
E01-09: f1=foGqpkSh0k f2=D1vehqwfG0 f3=vyj0c4I7eZ f4=J8o9RCNm9L
E01-10: f1=2CqH2TMqzN f2=kfDvUeSjEL f3=JDuqsgplUc f4=g9foVuVidx
E01-11: f1=rLQeQWGYmv f2=rcSfpKfoS4 f3=8zfJZhScka
E01-12: f1=jACVGDqI7K f2=vYxwFMNUQq f3=HK1EC3yvcM f4=MVaFQPdeQH
E01-13: f1=cfU1WXAO4K f2=IRWSA5PF2V f3=LGSbmohzUu f4=fqZuUPh38O
```

**资产参考图 URL（角色/场景/道具，2026-10-05 记录）：**
- 苏晚 front-full=`IIGXFTEfYN`，face-front=`VJYlzLckmR`；白衣的她 front-full=`vBOIaPPUaa`
- S01=`njbHTdbsYE` ｜ P01=`m14qLXGSZm` ｜ P02=`bOlEkgME0y` ｜ P03=`Ua6UCLkC4K` ｜ P04=`KpUC8uf4fb` ｜ P05=`Y5c6XTMcRq` ｜ P06=`6FWMplinxt`
- 完整列表见 `character-refs.html` 与各 `asset.json`（URL 前缀均为 `https://aka.doubaocdn.com/s/`）

---

## 5. 用户硬性要求（QC 标准）

1. **不要有逻辑问题**：剧情动作、台词、切点与 storyboard.json 逐字一致；画面人物/道具状态与该镜 frame 一致。
2. **不要有物理问题**：光穿体（白衣身影是虚体，光/枕头要穿过她）、水滴下落、杯垫水痕等超自然现象按设定来，但普通物理（重力、手持、移动）不许穿帮。
3. 分镜帧出图时**只挂画面里出现的角色**，防止模型脑补多余人物（已踩过：E01-04 切1 多出第三人、E01-11 切2 混入男性）。
4. 台词逐字保留（`<d>[Chinese]…</d>` 内原文一个标点不许动）。

---

## 6. 踩坑记录（避免重蹈）

- **出图污染**：纯白底道具图会被模型脑补电子秤/电子设备（P02/P05/P06 首轮全中），重出时提示词加 `Absolutely no weighing scale, no electronic device` 或改用 image_edit 移除。
- **分镜帧多余人物**：双人镜头提示词末尾加「画面里只有 X 和 Y，没有第三个人」。
- **Windows 环境**：无 Bash，命令走 PowerShell；node ESM 导入 Windows 绝对路径需 `file:///` 前缀；python 读 JSON 用 `encoding='utf-8-sig'`、写用 `utf-8`（Out-File 默认 BOM 会坏 node JSON）。
- **中文画面文字**：生成时用拼音+英文释义（如 `bie hui tou (do not look back)`）。
- **出片额度**：视频生成有周额度上限，连续大批量出片前先小批量试探；拦截提示"不要自动重试"。
- **角色图出图后端**：本机 ComfyUI / codex 均不可用（已逐一验证），实际用内置 image_gen/image_edit 直出，asset.json 的 model 字段记 `doubao-image`。

---

## 7. 给下一个 AI 的下一步动作（建议顺序）

1. 试调 `image_to_video`（E01-02 段）确认额度已恢复；成功则继续。
2. 按第 4 节参数逐段出 E01-02 → E01-13（每批 ≤2 条），每段出完立即交付并 QC（对照第 5 节）。
3. 全部 13 段齐后，用 byted-mediakit-editing 等工具按切点拼接成 EP1 完整成片（每段内部已是多镜，段间顺序拼接即可，必要时加转场）。
4. 向用户交付 EP1 成片，确认后再推进 EP2~EP6（分镜/提示词已就绪，只差出帧与出片）。
5. EP2~EP6 分段提示词在 `storyboard.json` 各集 `segments[i].h3Prompt`，分镜帧需要逐段重新出（挂对应场景/角色/道具参考图，规则见 novel-storyboard 的 frame.md）。

---

*打包时间：2026-10-18 ｜ 打包人：豆包办公 MainAgent（上一任）*
