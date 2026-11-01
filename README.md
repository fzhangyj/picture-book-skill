# Picture Book Skill - AI定制绘本创作工具

为孩子创建专属的AI绘本，孩子是主角，互动编故事，生成角色一致的插画。

## 快速开始

### 1. 触发Skill

在Claude Code中说：
- "我想给孩子做一本绘本"
- "帮我创建一个儿童故事书"
- "做一本picture book"

### 2. 准备照片（可选但推荐）

将孩子的照片保存到：
```
~/.claude/skills/picture-book/assets/character/original.jpg
```

### 3. 跟随引导

Claude会引导你：
1. 收集孩子信息（姓名、年龄、外貌）
2. 选择故事主题
3. 互动编故事
4. 生成角色设定图
5. 逐页生成插画
6. 组装成PDF和HTML

## 目录结构

```
picture-book/
├── SKILL.md                    # Skill工作流文档
├── README.md                   # 本文件
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
```

## 技术栈

- **图片生成**: Foxtrai AI Drawing API
- **PDF生成**: ReportLab + Pillow
- **Python**: 3.10+

## 依赖安装

脚本使用 `uv` 自动管理依赖，无需手动安装。

如果需要手动安装：
```bash
pip install reportlab pillow httpx
```

## 手动使用脚本

### 生成角色设定图
```bash
cd ~/.claude/skills/picture-book
export $(grep FOXTRAI_API_KEY config/.env | xargs)

uv run scripts/generate_image.py \
  --input-image "assets/character/original.jpg" \
  --prompt "Character design sheet for children's picture book. A 6-year-old boy with short black hair and glasses. Show 3 expressions: happy smiling, surprised with wide eyes, gentle thinking. Warm watercolor style, soft colors, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

### 生成单页插画
```bash
uv run scripts/generate_image.py \
  --input-image "assets/character/character-sheet.png" \
  --prompt "A little boy lying on grass field at sunset, looking up at the starry sky, peaceful and dreamy. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-01.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

### 组装PDF
```bash
uv run scripts/create_picturebook.py \
  --title "小明的太空冒险" \
  --pages page-01.png page-02.png page-03.png \
  --texts "小明躺在草地上，数着天上的星星。" "突然，他感觉脚底痒痒的——" "他飞起来了！" \
  --output "小明的太空冒险.pdf"
```

## 核心特性

### 1. 角色一致性
通过"角色设定图 + 垫图机制"确保每页的主角都是同一个孩子。

### 2. 图文分工
- **图画**：负责视觉呈现
- **文字**：只说画面说不出的（触觉、声音、内心感受）
- **留白**：情感最浓的地方，文字退场

### 3. 孩子参与
让孩子全程参与创作，这是真正属于他的故事。

## 故事主题

内置模板：
- 太空冒险
- 海底探险
- 魔法森林
- 勇敢的一天
- 动物朋友
- 自定义主题

详见 `references/story-templates.md`

## 适用年龄

- **3-4岁**: 6-8页，简单情感
- **5-6岁**: 8-10页，冒险友谊
- **7-9岁**: 10-12页，成长责任

## 输出格式

1. **PDF**: 可打印的绘本（A4横版）
2. **HTML**: 可在浏览器中预览

## 配置

API配置在 `config/.env`：
```
FOXTRAI_API_KEY=<SET_IN_ENV>
FOXTRAI_BASE_URL=https://www.foxtrai.com/api/generate
```

## 注意事项

1. 图片分辨率选择1K足够打印A4尺寸
2. 每次生成插画都要带上角色设定图确保一致性
3. 文字要克制，每页控制在3句以内
4. 让孩子参与故事创作过程

## 示例工作流

```
用户: "我想给我儿子做一本太空冒险的绘本"
  ↓
Claude: 收集信息（姓名、年龄、照片）
  ↓
Claude: 生成故事大纲，与孩子互动调整
  ↓
Claude: 生成角色设定图
  ↓
Claude: 逐页生成插画（每3-4页确认一次）
  ↓
Claude: 组装PDF和HTML
  ↓
交付: 完整的绘本文件
```

## 常见问题

**Q: 没有孩子的照片怎么办？**
A: 可以根据描述生成角色，效果也很好。

**Q: 可以修改某一页吗？**
A: 可以，重新生成那一页的插画，然后重新组装PDF。

**Q: 支持哪些语言？**
A: 目前主要支持中文，文字会自动使用中文字体。

**Q: 生成一本绘本需要多久？**
A: 8-10页的绘本大约需要15-20分钟（包括互动时间）。

## 参考资料

- 松居直《绘本之力》：图文相乘理论
- Nikolajeva & Scott《How Picturebooks Work》：图文关系分类
- Molly Bang《Picture This》：构图与情感

## 版本

- v1.0.0 (2026-03-11): 初始版本

## 作者

基于Claude Code创建，灵感来源于"小和和飞向宇宙"项目。
