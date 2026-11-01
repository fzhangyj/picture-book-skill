---
name: picture-book
description: 为孩子创建定制化AI绘本：孩子是主角，互动编故事，生成角色一致的插画，输出HTML和PDF绘本。当用户提到"做绘本"、"儿童绘本"、"故事书"、"picture book"、"给孩子做书"时使用。
---

# AI 定制绘本创作工作流

> **核心理念：** 让每个孩子都能拥有一本真正属于自己的绘本——他的故事，他是主角。

---

## Skill 路径

脚本路径：`~/.claude/skills/picture-book/scripts/`

---

## 工作流程

### Step 1: 收集信息

与用户互动，收集以下信息：

1. **孩子信息**
   - 姓名（用于故事中）
   - 年龄（影响故事复杂度）
   - 性别
   - 外貌特征（头发、眼镜、常穿衣服等）

2. **照片上传**（可选但强烈推荐）
   - 请用户上传孩子的照片到 `assets/character/original.jpg`
   - 如果没有照片，根据描述生成角色

3. **故事主题**
   - 让孩子自己说想要什么故事
   - 或者从以下主题选择：
     - 太空冒险
     - 海底探险
     - 魔法世界
     - 动物朋友
     - 勇敢成长
     - 自定义主题

4. **画风选择**
   - 温暖水彩（推荐，适合儿童）
   - 可爱卡通
   - 梦幻童话
   - 简笔插画

---

### Step 2: 互动编故事

**重要原则：让孩子参与创作过程**

1. 根据主题生成故事大纲（8-12页）
2. 展示大纲给孩子/家长确认
3. 询问：
   - 想加入什么角色？（朋友、宠物、家人）
   - 想去什么地方？
   - 想遇到什么有趣的事？
4. 根据反馈调整故事

**故事结构：**
- 开场：介绍主角（孩子）
- 发展：遇到问题/开始冒险
- 高潮：解决问题/重要发现
- 结尾：温暖收尾，传递正向价值

**每页内容包含：**
- 页码
- 画面描述（详细的视觉场景）
- 文字内容（简短，只说画面说不出的）

---

### Step 3: 生成角色设定图

如果用户上传了照片，生成角色设定图：

```bash
cd ~/.claude/skills/picture-book
export $(grep FOXTRAI_API_KEY config/.env | xargs) && \
uv run scripts/generate_image.py \
  --input-image "assets/character/original.jpg" \
  --prompt "Character design sheet for children's picture book. A [年龄]-year-old [性别] child with [外貌特征]. Show 3 expressions: happy smiling, surprised with wide eyes, gentle thinking. Warm watercolor style, soft colors, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

如果没有照片，直接根据描述生成：

```bash
uv run scripts/generate_image.py \
  --prompt "Character design sheet for children's picture book. A [年龄]-year-old [性别] child with [外貌特征]. Show 3 expressions: happy smiling, surprised with wide eyes, gentle thinking. Warm watercolor style, soft colors, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

生成后用 Read 工具展示给用户确认。

---

### ⚠️ 重要：角色一致性保障

**问题诊断：**
如果在生成过程中看到以下警告：
```
File upload failed: 500
Warning: Failed to upload reference image, proceeding without it
```

这意味着参考图片上传失败，AI将在没有参考图的情况下生成图片，**会导致人物形象不一致**。

**解决方案：**

1. **在每一页的prompt中手动添加详细的角色描述**
   - 创建一个"角色描述模板"，在每页prompt开头使用
   - 示例模板：`A [年龄]-year-old [性别] with [发型描述], wearing [眼镜描述] and [服装描述]`
   - 具体示例：`A 15-year-old boy with black messy hair, wearing stylish glasses and black outfit`

2. **在prompt末尾强调一致性**
   - 添加：`Consistent character design, same character throughout, [画风] style`
   - 示例：`Consistent character design, same character throughout, Japanese manga style`

3. **分批检查**
   - 每生成3-4页后，用Read工具展示给用户
   - 让用户确认人物形象是否一致
   - 如果不一致，立即调整prompt重新生成

4. **记录角色特征**
   - 在开始生成前，将角色的关键特征记录下来
   - 每一页都使用相同的描述词汇

**标准Prompt结构（文字融入画面版 - 灵活背景框）：**
```
Children's picture book illustration. [角色完整描述], [场景和动作描述].
In the [位置] area, there is a [背景框形状描述] with gentle blurred watercolor edges,
and Chinese text '[文字内容]' is written in a cute rounded handwritten children's book
font style on this background. The text and background are naturally integrated as
part of the illustration. Warm watercolor and cute cartoon style, consistent character design.
```

**位置选择（每页不同）：**
- `upper-left` / `upper-right` / `top-center`
- `lower-left` / `lower-right` / `bottom-center`

**背景框形状根据场景灵活选择：**
| 场景类型 | 推荐背景框形状 |
|---------|-------------|
| 室内温馨/夜晚 | `soft cloud-shaped white semi-transparent bubble` |
| 魔法/奇幻 | `soft glowing magical star-shaped semi-transparent light patch` |
| 森林/自然 | `soft organic leaf-shaped semi-transparent white patch` |
| 冒险/跳跃 | `soft irregular splash-shaped semi-transparent white area` |
| 夜空/星光 | `soft crescent moon-shaped semi-transparent white glow` |
| 花园/温柔 | `soft petal-shaped semi-transparent white background` |
| 通用 | `soft irregularly shaped semi-transparent white watercolor wash` |

**关键要点：**
1. 背景框形状与场景风格匹配，每页不同，避免单调
2. 手写风格字体：`cute rounded handwritten children's book font style`
3. 自然融入：`naturally integrated as part of the illustration`
4. 边缘柔和：`gentle blurred watercolor edges`

---

### Step 4: 逐页生成插画

**核心方法论：图文分工**

- **图画**：负责视觉呈现（场景、动作、表情）
- **文字**：只说画面画不出来的（触觉、声音、内心感受）
- **留白**：情感最浓的地方，文字要退场

**生成命令：**

```bash
cd ~/.claude/skills/picture-book
export $(grep FOXTRAI_API_KEY config/.env | xargs) && \
uv run scripts/generate_image.py \
  --input-image "assets/character/character-sheet.png" \
  --prompt "[画面描述]. Warm watercolor style for children's picture book, soft lighting, dreamy atmosphere, no text in image." \
  --filename "page-[NN].png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**Prompt 编写原则：**
1. **首要原则：角色描述必须详细且一致**
   - 每一页都要包含完整的角色描述（年龄、性别、发型、眼镜、服装等）
   - 使用相同的描述词汇，确保一致性
   - 示例：`A 15-year-old boy with black messy hair, wearing stylish glasses and black outfit`
2. 描述场景和情绪，不要约束具体颜色、构图
3. 保持简短但完整（3-4句话，包含角色描述）
4. 强调画风一致性和角色一致性
5. 明确说明"no text in image"（图片中不要文字）
6. 在prompt末尾添加：`consistent character design, same character throughout`

**示例：**
- ❌ 错误prompt（缺少角色描述）："A boy lying on grass field at sunset, looking up at the starry sky."
- ✅ 正确prompt（包含完整角色描述）："A 15-year-old boy with black messy hair, wearing stylish glasses and black outfit, lying on grass field at sunset, looking up at the starry sky, peaceful and dreamy. Consistent character design, same character throughout."

每生成3-4页，展示给用户确认，询问是否需要调整。

---

### Step 5: 组装绘本

使用 `create_picturebook.py` 脚本组装：

```bash
cd ~/.claude/skills/picture-book
uv run scripts/create_picturebook.py \
  --title "[绘本标题]" \
  --pages page-01.png page-02.png page-03.png ... \
  --texts "第1页文字" "第2页文字" "第3页文字" ... \
  --output "[孩子名字]的绘本.pdf"
```

脚本会生成：
1. **PDF文件**：可打印的绘本
2. **HTML预览**：可在浏览器中查看

---

### Step 6: 交付与迭代

1. 用 Read 工具展示部分页面预览
2. 告知用户文件位置
3. 询问是否需要调整某些页面
4. 如需调整，重新生成对应页面，重新组装

---

## 配置文件

### config/.env

```
FOXTRAI_API_KEY=<SET_IN_ENV>
FOXTRAI_BASE_URL=https://www.foxtrai.com/api/generate
```

---

## 目录结构

```
picture-book/
├── SKILL.md                    # 本文件
├── config/
│   └── .env                    # API配置
├── scripts/
│   ├── generate_image.py       # 图片生成脚本
│   └── create_picturebook.py   # PDF组装脚本
├── assets/
│   └── character/
│       ├── original.jpg        # 用户上传的照片
│       └── character-sheet.png # 生成的角色设定图
└── references/
    └── story-templates.md      # 故事模板参考

工作目录（每次创作时创建）：
~/Desktop/[孩子名字]的绘本/
├── page-01.png
├── page-02.png
├── ...
├── [孩子名字]的绘本.pdf
└── preview.html
```

---

## 注意事项

1. **角色一致性（最重要！）**：
   - ⚠️ **关键问题**：参考图片上传可能失败（500错误），导致人物形象不一致
   - ✅ **解决方案**：
     - 在prompt中详细描述角色特征（年龄、性别、发型、眼镜、服装颜色等）
     - 每一页的prompt都要包含完整的角色描述
     - 示例：`A 15-year-old boy with black messy hair, wearing stylish glasses and black outfit`
     - 在prompt末尾强调：`consistent character design, same character throughout`
   - 📋 **检查清单**：
     - 生成后检查日志，如果看到"Failed to upload reference image"警告
     - 必须在每页prompt中手动添加详细角色描述
     - 生成3-4页后展示给用户，确认人物一致性
     - 如果不一致，重新生成时加强角色描述

2. **图文分工**：文字要克制，不要重复画面内容
3. **孩子参与**：让孩子全程参与，这是他的故事
4. **情感留白**：最感人的时刻，少说话，让画面说话
5. **分辨率选择**：1K足够打印A4尺寸，生成速度快

---

## 故事质量标准

参考绘本大师的方法论：

- **松居直**：图文是相乘关系，不是相加
- **Nikolajeva & Scott**：图文反衬力量最强，对称是浪费
- **Molly Bang**：构图形状传递情感（水平线=平静，对角线=冒险）

---

## 协作模式

- **Full Auto**：家长提供信息，AI全自动生成
- **Guided**（推荐）：关键节点确认（故事大纲、角色设定、每3-4页）
- **Collaborative**：逐页与孩子互动，完全定制
