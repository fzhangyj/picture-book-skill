# Picture Book Skill 使用示例

## 完整示例：创建"小明的太空冒险"

### 第一步：准备角色照片

假设你有孩子的照片，保存到：
```bash
~/.claude/skills/picture-book/assets/character/original.jpg
```

### 第二步：生成角色设定图

```bash
cd ~/.claude/skills/picture-book
export $(grep FOXTRAI_API_KEY config/.env | xargs)

uv run scripts/generate_image.py \
  --input-image "assets/character/original.jpg" \
  --prompt "Character design sheet for children's picture book. A 6-year-old boy with short black hair and round glasses, wearing a blue jacket. Show 3 expressions: happy smiling, surprised with wide eyes, gentle thinking. Warm watercolor style, soft colors, white background, no text." \
  --filename "assets/character/character-sheet.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

### 第三步：创建工作目录

```bash
mkdir -p ~/Desktop/小明的太空冒险
cd ~/Desktop/小明的太空冒险
```

### 第四步：生成每一页插画

**第1页：看星星**
```bash
export $(grep FOXTRAI_API_KEY ~/.claude/skills/picture-book/config/.env | xargs)

uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy lying on grass field at sunset, looking up at the starry sky with wonder, peaceful and dreamy atmosphere. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-01.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第2页：脚痒痒**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy lying in grass with fireflies around him, gentle glowing lights, magical and warm atmosphere. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-02.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第3页：飞起来了**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy floating up from the ground, arms spread wide, surprised and excited expression, magical moment. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-03.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第4页：飞向月亮**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy flying towards the moon through clouds, surrounded by twinkling stars, dreamy and magical atmosphere. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-04.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第5页：遇到星座恐龙**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy floating in space meeting a gentle constellation dinosaur made of stars, magical and wonder-filled atmosphere. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-05.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第6页：触摸星星**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy reaching out to touch a glowing star constellation dinosaur, warm light between them, emotional and magical moment. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-06.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第7页：回到地球**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy flying back towards Earth, waving goodbye to the stars, bittersweet and beautiful atmosphere. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-07.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

**第8页：带着星光入睡**
```bash
uv run ~/.claude/skills/picture-book/scripts/generate_image.py \
  --input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png \
  --prompt "A little boy lying on grass at night, surrounded by gentle starlight, peaceful and content, falling asleep with a smile. Warm watercolor style for children's picture book, soft lighting, no text in image." \
  --filename "page-08.png" \
  --resolution 1K \
  --aspect-ratio 16:9
```

### 第五步：组装PDF

```bash
uv run ~/.claude/skills/picture-book/scripts/create_picturebook.py \
  --title "小明的太空冒险" \
  --pages page-01.png page-02.png page-03.png page-04.png page-05.png page-06.png page-07.png page-08.png \
  --texts \
    "小明躺在草地上，数着天上的星星。一颗、两颗、三颗……" \
    "突然，他感觉脚底下痒痒的——" \
    "他飞起来了！" \
    "他穿过软绵绵的云，越过亮闪闪的月亮，一直飞进深深的宇宙里。" \
    "在那里，他遇到了一只巨大的恐龙——它的身体是用千万颗星星连成的！" \
    "小明伸出手，轻轻碰了碰星星恐龙的鼻子。哗——！无数星光像小雨一样洒下来，每一颗都是暖暖的、亮亮的。" \
    "忽然，小明飞了起来！他穿过软绵绵的云，越过亮闪闪的月亮，一直飞进了深深的宇宙里。" \
    "小明躺在山坡的草地上，望着满天的星星。星星们一闪一闪，好像在说：「来看看我们啊！」" \
  --output "小明的太空冒险.pdf"
```

### 第六步：查看结果

生成的文件：
- `小明的太空冒险.pdf` - 可打印的PDF绘本
- `小明的太空冒险.html` - 可在浏览器中预览

在浏览器中打开HTML文件预览：
```bash
open 小明的太空冒险.html  # macOS
start 小明的太空冒险.html  # Windows
xdg-open 小明的太空冒险.html  # Linux
```

---

## 图文分工示例

### ✅ 好的图文配合

**第2页**
- 画面：小男孩躺在草地上，周围有萤火虫
- 文字：「突然，他感觉脚底下痒痒的——」

→ 画面展示场景，文字说触觉（画面画不出来的）

**第6页**
- 画面：小男孩触摸星座恐龙，光芒四射
- 文字：「哗——！无数星光像小雨一样洒下来，每一颗都是暖暖的、亮亮的。」

→ 画面展示视觉，文字说声音和触觉

### ❌ 不好的图文配合

**反例**
- 画面：小男孩在飞
- 文字：「小明飞起来了」

→ 图文重复，1+1=1

---

## 批量生成技巧

如果要生成多页，可以创建一个脚本：

```bash
#!/bin/bash
# generate_all_pages.sh

SKILL_DIR=~/.claude/skills/picture-book
export $(grep FOXTRAI_API_KEY $SKILL_DIR/config/.env | xargs)

# 定义每页的prompt
declare -a prompts=(
  "A little boy lying on grass field at sunset, looking up at the starry sky with wonder"
  "A little boy lying in grass with fireflies around him, gentle glowing lights"
  "A little boy floating up from the ground, arms spread wide, surprised expression"
  # ... 更多页面
)

# 批量生成
for i in "${!prompts[@]}"; do
  page_num=$(printf "%02d" $((i+1)))
  echo "Generating page $page_num..."

  uv run $SKILL_DIR/scripts/generate_image.py \
    --input-image "$SKILL_DIR/assets/character/character-sheet.png" \
    --prompt "${prompts[$i]}. Warm watercolor style for children's picture book, soft lighting, no text in image." \
    --filename "page-$page_num.png" \
    --resolution 1K \
    --aspect-ratio 16:9

  echo "Page $page_num done!"
  sleep 2  # 避免API请求过快
done

echo "All pages generated!"
```

---

## 常见问题排查

### 问题1：API Key错误
```
Error: FOXTRAI_API_KEY not set
```

**解决**：检查 `~/.claude/skills/picture-book/config/.env` 文件是否存在且包含正确的API Key。

### 问题2：角色不一致
**原因**：没有使用 `--input-image` 参数

**解决**：每次生成插画都要带上角色设定图：
```bash
--input-image ~/.claude/skills/picture-book/assets/character/character-sheet.png
```

### 问题3：中文字体显示问题
**原因**：系统没有中文字体

**解决**：
- Windows：自动使用微软雅黑
- macOS：自动使用PingFang
- Linux：需要安装 `fonts-wqy-microhei` 或 `fonts-noto-cjk`

### 问题4：图片生成失败
**可能原因**：
1. 网络问题
2. API配额用完
3. Prompt包含敏感词

**解决**：查看错误信息，调整prompt或检查网络。

---

## 进阶技巧

### 1. 使用不同画风

在prompt中修改画风描述：
- `Warm watercolor style` → 温暖水彩
- `Cute cartoon style` → 可爱卡通
- `Dreamy fairy tale style` → 梦幻童话
- `Simple line drawing style` → 简笔画

### 2. 控制情绪氛围

在prompt中加入情绪词：
- `peaceful and calm` → 平静
- `exciting and adventurous` → 刺激冒险
- `warm and cozy` → 温暖舒适
- `magical and wonder-filled` → 魔幻惊奇

### 3. 季节和时间

- `at sunset` → 日落时分
- `at night with stars` → 星空夜晚
- `in spring with flowers` → 春天花开
- `in winter with snow` → 冬天雪景

---

## 时间估算

- 角色设定图：2-3分钟
- 每页插画：2-3分钟
- 组装PDF：10秒

**8页绘本总时间**：约20-25分钟（包括等待时间）

---

## 下一步

创建完绘本后，你可以：
1. 打印PDF，装订成实体书
2. 在iPad上给孩子看
3. 分享给家人朋友
4. 根据孩子反馈修改某些页面
5. 创建系列绘本（同一个角色的不同冒险）
