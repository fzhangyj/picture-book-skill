#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "reportlab>=4.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Create a picture book PDF from images and text.

Usage:
    uv run create_picturebook.py --title "书名" --pages page-01.png page-02.png --texts "文字1" "文字2" --output book.pdf

Optional per-page text position (default: bottom-left):
    --positions "bottom-left" "top-right" ...
    Choices: top-left, top-right, bottom-left, bottom-right, top-center, bottom-center
"""

import argparse
import sys
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader


# ── Constants ──────────────────────────────────────────────────────────────
FONT_SIZE   = 36          # unified font size for all pages
PADDING     = 18          # inner padding inside the text box
MARGIN      = 40          # distance from image edge to text box
BOX_RADIUS  = 16          # rounded corner radius
BOX_COLOR   = (255, 255, 255, 190)   # white, semi-transparent
TEXT_COLOR  = (40, 40, 40, 255)      # dark grey, fully opaque
MAX_TEXT_WIDTH_RATIO = 0.55          # text box max width = 55% of image width
PAGE_MARGIN  = 20                    # page margin in points (keep image away from edges)


# ── Font helpers ───────────────────────────────────────────────────────────
def find_pil_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "<PROJECT_PATH>",
        "<PROJECT_PATH>",
        "<PROJECT_PATH>",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def register_reportlab_font() -> str:
    candidates = [
        "<PROJECT_PATH>",
        "<PROJECT_PATH>",
        "<PROJECT_PATH>",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                pdfmetrics.registerFont(TTFont("Chinese", path))
                print(f"Using font: {path}")
                return "Chinese"
            except Exception:
                continue
    print("Warning: No Chinese font found, using Helvetica")
    return "Helvetica"


# ── Text wrapping (PIL-based) ──────────────────────────────────────────────
def wrap_text_pil(text: str, font: ImageFont.FreeTypeFont,
                  max_width_px: int) -> list[str]:
    """Wrap text by character (works for Chinese & English)."""
    lines, current = [], ""
    dummy = ImageDraw.Draw(PILImage.new("RGBA", (1, 1)))
    for char in text:
        test = current + char
        w = dummy.textlength(test, font=font)
        if w <= max_width_px:
            current = test
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


# ── Rounded rectangle helper ──────────────────────────────────────────────
def draw_rounded_rect(draw: ImageDraw.ImageDraw,
                      xy: tuple, radius: int, fill: tuple):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)


# ── Core: bake text box onto image ────────────────────────────────────────
def bake_text_onto_image(img: PILImage.Image, text: str,
                         position: str = "bottom-left") -> PILImage.Image:
    """Draw a semi-transparent rounded text box onto the image."""
    if not text.strip():
        return img

    img = img.convert("RGBA")
    W, H = img.size

    font = find_pil_font(FONT_SIZE)
    max_text_w = int(W * MAX_TEXT_WIDTH_RATIO)
    lines = wrap_text_pil(text, font, max_text_w)

    dummy_draw = ImageDraw.Draw(PILImage.new("RGBA", (1, 1)))
    line_h = int(FONT_SIZE * 1.45)
    text_w = max(int(dummy_draw.textlength(l, font=font)) for l in lines)
    text_h = len(lines) * line_h

    box_w = text_w + PADDING * 2
    box_h = text_h + PADDING * 2

    # Clamp box so it never exceeds image bounds
    box_w = min(box_w, W - MARGIN * 2)
    box_h = min(box_h, H - MARGIN * 2)

    # Determine top-left corner of box based on position
    pos = position.lower()
    if "left" in pos:
        bx = MARGIN
    elif "right" in pos:
        bx = W - MARGIN - box_w
    else:  # center
        bx = (W - box_w) // 2

    if "top" in pos:
        by = MARGIN
    else:  # bottom
        by = H - MARGIN - box_h

    # Draw overlay layer
    overlay = PILImage.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_rounded_rect(draw, (bx, by, bx + box_w, by + box_h),
                      BOX_RADIUS, BOX_COLOR)

    # Draw text lines
    for i, line in enumerate(lines):
        lw = int(draw.textlength(line, font=font))
        tx = bx + PADDING + (text_w - lw) // 2   # center within box
        ty = by + PADDING + i * line_h
        draw.text((tx, ty), line, font=font, fill=TEXT_COLOR)

    result = PILImage.alpha_composite(img, overlay)
    return result.convert("RGB")


# ── Scale & crop image to exact page size ─────────────────────────────────
def fit_image_to_page(img: PILImage.Image,
                      page_w: float, page_h: float) -> PILImage.Image:
    """Scale image to fit fully within page margins (contain mode, no cropping)."""
    avail_w    = page_w - 2 * PAGE_MARGIN
    avail_h    = page_h - 2 * PAGE_MARGIN
    img_ratio  = img.width / img.height
    avail_ratio = avail_w / avail_h
    if img_ratio > avail_ratio:
        new_w = int(avail_w)
        new_h = int(avail_w / img_ratio)
    else:
        new_h = int(avail_h)
        new_w = int(avail_h * img_ratio)
    return img.resize((new_w, new_h), PILImage.LANCZOS)


# ── PDF page builders ──────────────────────────────────────────────────────
def create_cover_page(c, title: str, width: float, height: float,
                      font_name: str):
    c.setFillColorRGB(0.95, 0.95, 0.98)
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFont(font_name, 36)
    c.setFillColorRGB(0.2, 0.2, 0.4)
    tw = c.stringWidth(title, font_name, 36)
    c.drawString((width - tw) / 2, height / 2, title)
    c.showPage()


def create_content_page(c, image_path: str, text: str,
                        width: float, height: float,
                        position: str = "bottom-left"):
    # White background
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    img = PILImage.open(image_path).convert("RGB")
    img = fit_image_to_page(img, width, height)
    img = bake_text_onto_image(img, text, position)

    # Center image on page within margins
    img_w, img_h = img.size
    x = (width  - img_w) / 2
    y = (height - img_h) / 2
    c.drawImage(ImageReader(img), x, y, img_w, img_h)
    c.showPage()


# ── HTML preview ──────────────────────────────────────────────────────────
def create_html_preview(pages, texts, title, output_html):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: "Microsoft YaHei", sans-serif;
               background: linear-gradient(135deg,#667eea,#764ba2);
               margin:0; padding:40px 20px; }}
        .container {{ max-width:1200px; margin:0 auto; }}
        h1 {{ text-align:center; color:white; font-size:48px;
              margin-bottom:60px; text-shadow:2px 2px 4px rgba(0,0,0,.3); }}
        .page {{ background:white; border-radius:20px; padding:40px;
                 margin-bottom:40px; box-shadow:0 10px 40px rgba(0,0,0,.2); }}
        .page-number {{ color:#999; font-size:14px; margin-bottom:20px; }}
        .page img {{ width:100%; border-radius:10px; }}
    </style>
</head>
<body><div class="container"><h1>{title}</h1>
"""
    for i, (page_path, text) in enumerate(zip(pages, texts), 1):
        html += f"""
        <div class="page">
            <div class="page-number">第 {i} 页</div>
            <img src="{Path(page_path).name}" alt="Page {i}">
        </div>
"""
    html += "</div></body></html>"
    output_html.write_text(html, encoding="utf-8")
    print(f"HTML preview created: {output_html}")


# ── CLI ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Create a picture book PDF")
    parser.add_argument("--title",     "-t", required=True)
    parser.add_argument("--pages",     "-p", nargs="+", required=True)
    parser.add_argument("--texts",     "-x", nargs="+", required=True)
    parser.add_argument("--output",    "-o", required=True)
    parser.add_argument("--positions", "-pos", nargs="*", default=[],
                        help="Per-page text position (default: bottom-left). "
                             "Choices: top-left top-right bottom-left "
                             "bottom-right top-center bottom-center")
    args = parser.parse_args()

    if len(args.pages) != len(args.texts):
        print("Error: pages and texts count must match", file=sys.stderr)
        sys.exit(1)

    for page in args.pages:
        if not Path(page).exists():
            print(f"Error: image not found: {page}", file=sys.stderr)
            sys.exit(1)

    # Pad positions list with default
    positions = list(args.positions)
    while len(positions) < len(args.pages):
        positions.append("bottom-left")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    font_name  = register_reportlab_font()
    page_w, page_h = landscape(A4)
    c = canvas.Canvas(str(output_path), pagesize=landscape(A4))

    print(f"Creating picture book: {args.title}")
    print(f"Pages: {len(args.pages)}")

    create_cover_page(c, args.title, page_w, page_h, font_name)

    for i, (page_path, text, pos) in enumerate(
            zip(args.pages, args.texts, positions), 1):
        print(f"  Processing page {i}/{len(args.pages)}: "
              f"{Path(page_path).name}  [{pos}]")
        create_content_page(c, page_path, text, page_w, page_h, pos)

    c.save()
    print(f"\nPDF created: {output_path.resolve()}")

    html_path = output_path.with_suffix(".html")
    create_html_preview(args.pages, args.texts, args.title, html_path)
    print(f"Preview:     {html_path.resolve()}")


if __name__ == "__main__":
    main()
