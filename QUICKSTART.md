# Picture Book Skill - 快速入门指南

## 🎯 这个Skill能做什么？

为孩子创建一本专属的AI绘本：
- ✅ 孩子是主角
- ✅ 角色形象一致（每页都是同一个孩子）
- ✅ 互动编故事（让孩子参与创作）
- ✅ 图文完美配合（不是简单的图+文字）
- ✅ 输出PDF和HTML（可打印、可在线看）

## 🚀 三种使用方式

### 方式1：通过Claude Code（推荐）

最简单的方式，只需说：
```
"我想给孩子做一本绘本"
```

Claude会自动引导你完成整个流程。

### 方式2：手动使用脚本

如果你想自己控制每一步，可以直接使用命令行脚本。

### 方式3：批量生成

适合已经有完整故事大纲的情况。

---

## 📋 准备工作

### 1. 确认Skill已安装

检查目录是否存在：
```bash
ls ~/.claude/skills/picture-book
```

应该看到：
```
SKILL.md  README.md  config/  scripts/  assets/  references/
```

### 2. 准备孩子的照片（可选）

如果有照片，复制到：
```bash
~/.claude/skills/picture-book/assets/character/original.jpg
```

没有照片也可以，根据描述生成角色。

### 3. 确认API配置

检查配置文件：
```bash
cat ~/.claude/skills/picture-book/config/.env
```

应该看到：
```
FOXTRAI_API_KEY=<SET_IN_ENV>
FOXTRAI_BASE_URL=https://www.foxtrai.com/api/generate
```

---

## 🎨 快速体验（5分钟）

让我们创建一个简单的3页绘本来测试：

### Step 1: 创建工作目录
```bash
mkdir -p ~/Desktop/测试绘本
cd ~/Desktop/测试绘本
```

### Step 2: 生成角色（无需照片）
```bash
export $(grep FOXTRAI_API_KEY ~/.claude/skills/picture-book/config/.env | xargs)

uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --prompt "Character design sheet for children's picture book. A 6-year-old happy child with short hair. Show 3 expressions: smiling, surprised, thinking. Warm watercolor style, white background, no text." \
  --filename "character.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

等待2-3分钟，会生成 `character.png`

### Step 3: 生成3页插画
```bash
# 第1页
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image "character.png" \
  --prompt "A child in a garden with butterflies, sunny day, happy atmosphere. Warm watercolor style, no text." \
  --filename "page-01.png" \
  --resolution 1K \
  --aspect-ratio 16:9

# 第2页
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image "character.png" \
  --prompt "A child discovering a magical flower glowing, wonder and surprise. Warm watercolor style, no text." \
  --filename "page-02.png" \
  --resolution 1K \
  --aspect-ratio 16:9

# 第3页
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image "character.png" \
  --prompt "A child sitting under a tree, peaceful and content. Warm watercolor style, no text." \
  --filename "page-03.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

每页等待2-3分钟。

### Step 4: 组装PDF
```bash
uv run ~/.claude/skills/picture-book/scripts/create_picturebook.py \
  --title "我的第一本绘本" \
  --pages page-01.png page-02.png page-03.png \
  --texts \
    "小朋友在花园里玩耍，蝴蝶在身边飞舞。" \
    "突然，他发现了一朵会发光的花！" \
    "他坐在树下，想着今天的奇妙冒险。" \
  --output "我的第一本绘本.pdf"
```

10秒内完成！

### Step 5: 查看结果
```bash
# Windows
start 我的第一本绘本.html

# macOS
open 我的第一本绘本.html

# Linux
xdg-open 我的第一本绘本.html
```

---

## 📚 完整工作流程

### 1. 收集信息阶段

需要确定：
- 孩子的姓名
- 年龄（影响故事复杂度）
- 外貌特征（头发、眼镜、常穿衣服）
- 故事主题（太空、海底、魔法森林等）

### 2. 生成角色设定图

这是确保角色一致性的关键！

**有照片的情况：**
```bash
uv run scripts/generate_image.py \
  --input-image "assets/character/original.jpg" \
  --prompt "Character design sheet for children's picture book. A [年龄]-year-old [性别] with [外貌特征]. Show 3 expressions: happy, surprised, thinking. Warm watercolor style, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K
```

**无照片的情况：**
```bash
uv run scripts/generate_image.py \
  --prompt "Character design sheet for children's picture book. A [年龄]-year-old [性别] with [外貌特征]. Show 3 expressions: happy, surprised, thinking. Warm watercolor style, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K
```

### 3. 编写故事大纲

参考 `references/story-templates.md` 中的模板。

建议结构（8-10页）：
1. 开场：介绍主角
2. 触发：遇到问题/发现新世界
3. 冒险：3-4页的冒险过程
4. 高潮：关键时刻
5. 结尾：温暖收尾

### 4. 逐页生成插画

**重要**：每页都要带上 `--input-image "character-sheet.png"`

```bash
uv run scripts/generate_image.py \
  --input-image "character-sheet.png" \
  --prompt "[场景描述]. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-XX.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**Prompt编写技巧：**
- 简短（2-3句话）
- 描述场景和情绪
- 不要约束颜色、构图细节
- 必须加 "no text in image"

### 5. 组装PDF

```bash
uv run scripts/create_picturebook.py \
  --title "绘本标题" \
  --pages page-01.png page-02.png ... \
  --texts "第1页文字" "第2页文字" ... \
  --output "绘本名称.pdf"
```

---

## 💡 核心技巧

### 1. 角色一致性

**关键**：生成角色设定图 + 每次都用它作为参考

```bash
# 第一次：生成设定图
--prompt "Character design sheet..."
--filename "character-sheet.png"

# 后续每页：带上设定图
--input-image "character-sheet.png"
--prompt "场景描述..."
```

### 2. 图文分工

**文字负责**（画面画不出来的）：
- 触觉：「草地痒痒的」
- 声音：「哗啦哗啦」
- 内心：「他有点害怕，但更多的是兴奋」

**画面负责**：
- 场景、动作、表情
- 色彩、氛围

**留白**：
- 最感人的时刻，只有画面，没有文字

### 3. 让孩子参与

在编故事时问孩子：
- "你想遇到什么动物？"
- "你觉得接下来会发生什么？"
- "如果是你，你会怎么做？"

---

## ⚠️ 常见问题

### Q1: 角色每页都不一样怎么办？

**原因**：没有使用角色设定图

**解决**：
1. 先生成角色设定图
2. 每次生成插画都带上 `--input-image "character-sheet.png"`

### Q2: 图片生成失败

**可能原因**：
- 网络问题
- API配额用完
- Prompt包含敏感词

**解决**：
- 检查网络连接
- 查看错误信息
- 简化prompt

### Q3: PDF中文字显示不正常

**原因**：系统缺少中文字体

**解决**：
- Windows：自动使用微软雅黑
- macOS：自动使用PingFang
- Linux：安装 `sudo apt install fonts-wqy-microhei`

### Q4: 生成速度慢

**正常情况**：
- 角色设定图：2-3分钟
- 每页插画：2-3分钟
- 8页绘本总计：20-25分钟

**加速技巧**：
- 使用1K分辨率（足够打印A4）
- 简化prompt
- 批量生成时加sleep避免API限流

---

## 📖 学习资源

### 文档
- `SKILL.md` - 完整工作流文档
- `README.md` - 项目说明
- `references/story-templates.md` - 故事模板
- `references/usage-examples.md` - 详细示例

### 故事主题
- 太空冒险
- 海底探险
- 魔法森林
- 勇敢的一天
- 动物朋友

### 年龄适配
- 3-4岁：6-8页，简单情感
- 5-6岁：8-10页，冒险友谊
- 7-9岁：10-12页，成长责任

---

## 🎉 下一步

1. **快速体验**：按照上面的"快速体验"创建一个3页测试绘本
2. **完整创作**：为孩子创建一本8-10页的完整绘本
3. **打印装订**：把PDF打印出来，装订成实体书
4. **分享反馈**：给孩子看，根据反馈调整

---

## 🆘 需要帮助？

在Claude Code中说：
```
"我想用picture-book skill做绘本"
```

Claude会引导你完成整个流程！
