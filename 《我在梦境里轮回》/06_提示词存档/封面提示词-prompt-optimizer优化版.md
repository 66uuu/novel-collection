# 《我在梦境里轮回》封面提示词（prompt-optimizer 优化版）

> 优化日期：2026-10-21
> 走通道 A（对话内直接优化），模板 `image-general-optimize`（text2image 族）
> 输入：用户原话需求 + 两张《诡梦》参考封面的风格证据
> 输出：可直接喂给 ImageGen 的英文提示词

---

## 一、用户原话需求（采集阶段，未加工）

- 「我感觉你给的小说正文太乱了」→ 章节拆分（另办）
- 「小说的封面其实还是不行，我希望你重新再设计一个小说的封面」
- 「你需要去参考一下我这两个小说封面」
- 「把那种不幸、恐怖、绝望、诡异而又孤独绝望的那种氛围给渲染出来」
- 「就参考这两个小说封面重新去做」
- 「根据我所说的这些要求，先用提示词工具先过一遍，将我所说的话用提示词过一遍，生成更完整的提示词，最后再交给AI去生成」

## 二、参考封面风格证据（从两张《诡梦》封面提取）

### 参考图 1（门 + 泥沼）
- 中央主体：一根独立的旧水泥门框，门开着，门内全黑，门板上贴红「福」
- 门楣题字「家是梦的起点」
- 前景大片红泥沼，一串血红脚印从画面底部一直延伸到门槛
- 门槛边放着一双旧帆布鞋
- 背景：龟裂的压低乌云、远处喀斯特山影、右侧一盏路灯 + 湿路反光、零星城市灯火
- 配色：近单色暗蓝灰黑，**唯一饱和色是血红**
- 大字毛笔标题压顶部，暗红色，破损质感；小字副标语；底部中央作者名
- 四角重度暗角，中景起雾

### 参考图 2（人 + 门洞 + 轮回）
- 中央主体：一个背影男人正跨过门槛，走进黑暗巷子
- 门框有对联「他乡亦是故乡」、门楣「家是梦的尽头」
- 左侧竖排小字「有些路 走了很远 才发现 一直在原地」
- 男人的轮廓被重复成三四道半透明重影（轮回母题）
- 湿地面上血红脚印 + 血红拖痕
- 左侧高楼黑影，门洞外是夜街、路灯、雨雾
- 配色与图 1 完全一致

### 两条封面的共同视觉语言（本次必须复现）
1. 竖版，主体居中，大标题压顶
2. 近乎单色的暗蓝灰黑 + 唯一饱和色血红
3. 中央必有「门 / 门槛 / 通道」母题
4. 地面必有血红脚印，湿滑反光
5. 氛围：雨雾、湿气、暗角、远处一点人造光
6. 孤独感：空景（只留一双鞋）或单个渺小背影
7. 标题毛笔大字 + 副标语 + 底部作者名

## 三、本书核心视觉母题（要换进去的新内容）

- 一扇半开的旧木门，门内是**三层叠套的景象**：商场扶梯 / 老宅木楼梯 / 台风夜酒店走廊（呼应「同一栋楼的四重时空」）
- 血红脚印从画面底部一直走进门里（红泥 + 指甲缝干血的开篇钩子）
- 天空龟裂（承接参考图 1 的裂天）
- 单个背影 + 半透明重影（轮回）
- 远处一盏路灯（孤独绝望）
- 不讲出来的主题：门是入口也是出口

## 四、优化后的提示词（交付给 ImageGen）

A vertical horror book cover composition. At the exact center stands a weathered old wooden doorframe, half open, its paint peeled to bare grey, the door itself ajar with only blackness behind it; the doorframe stands alone in a shallow pool of black water mixed with dark red mud, and a trail of wet blood-red footprints leads from the bottom edge of the frame straight through the doorway. Seen from behind, a small lone man in a dark jacket stands motionless at the threshold, his silhouette repeated three times as faint ghostly after-images layered behind him, each copy slightly more transparent, suggesting the same walk happening over and over. Through the open door, three scenes are stacked inside the darkness: an escalator with metal treads climbing upward, a narrow wooden staircase turning away, and a rain-streaked hotel corridor lit by a single cold lamp, all three rendered in desaturated grey so they read as one building's overlapping floors. Above, the sky is a mass of low bruised storm clouds split by a thin crack of cold white light; far off on the right a single dim streetlamp glows over an empty wet road, the only point of distant light in the frame. The whole image is nearly monochrome in cold blue-grey and black, with saturated dried-blood red reserved only for the footprints, the crack in the sky, and the doorframe's peeling paint; heavy fog flattens the middle distance, the corners fall into deep vignette shadow, and the ground holds mirror-like reflections of the doorframe and the lamp. No text, no letters, no watermark, no people other than the lone silhouetted man, no bright colors other than the red accents.

---

## 五、负面约束（生图时作为负面清单另行使用）

- 不出现任何文字、字母、数字、水印、logo
- 不出现除孤独背影外的其他人物
- 不出现血红以外的饱和色（尤其黄、绿、紫、亮橙）
- 不出现明亮晴天光、金色阳光、暖色调主光
- 不出现可爱、卡通、Q 版、鲜艳、喜庆元素
- 不出现镜头参数式描述（85mm / 浅景深 / bokeh / 体积光 / 电影级）——本次靠画面证据描述，不靠相机术语

## 六、参数

| 项 | 值 |
|---|---|
| 尺寸 | 1024×1536（番茄竖版封面） |
| quality | high |
| background | opaque |
| 生成方式 | t2i 文生图（参考图仅作风格证据提取，不作 i2i 输入，避免构图互相污染） |

## 七、返工预案

| 现象 | 处理 |
|---|---|
| 红色不够饱和 / 被稀释 | 在提示词里把 "saturated dried-blood red reserved only for" 改成 "vivid arterial red used boldly for" |
| 门内三层景象糊成一团 | 把三段拆成更短的分号句，每段只留一个主体名词 |
| 整体太亮、恐怖感不足 | 加 "the entire frame is swallowed by darkness except three points of light" |
| 出现多余人物 | negative 里加 "crowd, groups of people, faces" |
| 重影不明显、轮回感弱 | 把 "repeated three times as faint ghostly after-images" 改成 "repeated four times, each copy more transparent and more blurred" |
