"""Render clean, readable blog figures from the Slicerflow screen definitions.

The Slicerflow canvas export shows navigation wires over the screens. These
figures rebuild the same nine screens without those editing overlays.
"""

from pathlib import Path
import math

import yaml
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATA = yaml.safe_load((ROOT / "拾见校园.slicerflow.yaml").read_text(encoding="utf-8"))
SCREENS = DATA["screens"]
FONT = "C:/Windows/Fonts/msyh.ttc"
BOLD = "C:/Windows/Fonts/msyhbd.ttc"
SERIF = "C:/Windows/Fonts/STSONG.TTF"

S = 1.22
PHONE_W = round(390 * S)
PHONE_H = round(790 * S)
PAD = 38
LABEL_H = 60
CELL_W = PHONE_W + 2 * PAD
CELL_H = PHONE_H + LABEL_H + PAD
BG = "#eee9dd"
INK = "#203646"
DEEP = "#172f42"
MUTED = "#6c7b80"
ACCENT = "#c96642"
PAPER = "#fffdf7"
LINEN = "#f7f3e9"
BORDER = "#d9d7cb"


def px(n):
    return round(n * S)


def font(size, bold=False, serif=False):
    return ImageFont.truetype(SERIF if serif else BOLD if bold else FONT, px(size))


def text_width(draw, string, f):
    box = draw.textbbox((0, 0), string, font=f)
    return box[2] - box[0]


def lines_for(draw, string, f, max_width):
    output = []
    for raw in str(string).split("\n"):
        line = ""
        for char in raw:
            if line and text_width(draw, line + char, f) > max_width:
                output.append(line)
                line = char
            else:
                line += char
        output.append(line)
    return output


def draw_lines(draw, string, x, y, max_width, f, fill=INK, line_height=None, align="left"):
    line_height = line_height or round(f.size * 1.52)
    for line in lines_for(draw, string, f, max_width):
        w = text_width(draw, line, f)
        tx = x + (max_width - w) // 2 if align == "center" else x
        draw.text((tx, y), line, font=f, fill=fill)
        y += line_height


def draw_screen(screen_key, label):
    image = Image.new("RGB", (CELL_W, CELL_H), BG)
    d = ImageDraw.Draw(image)
    d.text((PAD, 15), label, font=font(20, serif=True), fill=INK)
    d.text((CELL_W - PAD - 38, 20), screen_key.upper(), font=font(10, True), fill=ACCENT, anchor="ra")

    ox, oy = PAD, LABEL_H
    d.rounded_rectangle((ox + 8, oy + 9, ox + PHONE_W + 8, oy + PHONE_H + 9), radius=px(42), fill="#d4d0c5")
    d.rounded_rectangle((ox, oy, ox + PHONE_W, oy + PHONE_H), radius=px(40), fill="#1c2d36")
    ix, iy = ox + px(9), oy + px(9)
    iw, ih = PHONE_W - px(18), PHONE_H - px(18)
    d.rounded_rectangle((ix, iy, ix + iw, iy + ih), radius=px(34), fill=LINEN)
    d.rounded_rectangle((ix + iw // 2 - px(42), iy + px(6), ix + iw // 2 + px(42), iy + px(26)), radius=px(12), fill="#1c2d36")
    d.text((ix + px(20), iy + px(15)), "9:41", font=font(10, True), fill=INK)
    d.rounded_rectangle((ix + iw - px(40), iy + px(19), ix + iw - px(20), iy + px(29)), radius=px(2), outline=MUTED, width=px(1))
    d.rounded_rectangle((ix + iw // 2 - px(45), iy + ih - px(13), ix + iw // 2 + px(45), iy + ih - px(9)), radius=px(3), fill="#69747e")

    def box(item):
        x = ix + px(item.get("x", 24))
        y = iy + px(item.get("y", 0))
        w = px(item.get("w", 342))
        h = px(item.get("h", 46))
        return x, y, w, h

    for item_key, item in SCREENS[screen_key]["items"].items():
        kind = item["widget"]
        x, y, w, h = box(item)
        value = item.get("text", "")
        if kind == "navbar":
            d.rectangle((ix, iy + px(33), ix + iw, iy + px(67)), fill=PAPER)
            d.line((ix + px(1), iy + px(67), ix + iw - px(1), iy + px(67)), fill=BORDER, width=px(1))
            d.line((ix + iw // 2 - px(13), iy + px(67), ix + iw // 2 + px(13), iy + px(67)), fill=ACCENT, width=px(2))
            title = item.get("title", "")
            d.text((ix + iw // 2, iy + px(38)), title, font=font(16, True), fill=INK, anchor="mt")
            if item.get("back"):
                d.text((ix + px(22), iy + px(37)), "‹", font=font(29), fill=INK, anchor="mt")
        elif kind == "heading":
            draw_lines(d, value, x, y, w, font(22, serif=True), align=item.get("align", "left"))
        elif kind == "paragraph":
            draw_lines(d, value, x, y, w, font(14), MUTED, px(25))
        elif kind == "text":
            draw_lines(d, value, x, y, w, font(14), INK, px(22))
        elif kind == "searchbar":
            d.rounded_rectangle((x, y, x + w, y + px(44)), radius=px(6), fill=PAPER, outline="#bcc7c4", width=px(1))
            cx, cy, rr = x + px(22), y + px(20), px(5)
            d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=ACCENT, width=px(2))
            d.line((cx + px(4), cy + px(4), cx + px(10), cy + px(10)), fill=ACCENT, width=px(2))
            d.text((x + px(43), y + px(12)), value or item.get("placeholder", ""), font=font(13), fill=MUTED)
        elif kind == "segmented":
            options = item.get("items", [])
            d.line((x, y + px(39), x + w, y + px(39)), fill=BORDER, width=px(1))
            seg = w / len(options)
            d.line((x + px(3), y + px(39), x + seg - px(3), y + px(39)), fill=ACCENT, width=px(3))
            for i, name in enumerate(options):
                d.text((x + seg * (i + .5), y + px(10)), str(name), font=font(13, i == 0), fill=INK if i == 0 else MUTED, anchor="mt")
        elif kind == "button":
            button_h = h if "h" in item else px(48)
            if item_key.startswith("card_") or item_key.startswith("result_"):
                lost = str(value).startswith("寻物")
                d.rounded_rectangle((x + px(4), y + px(5), x + w + px(4), y + button_h + px(5)), radius=px(5), fill="#dedbd1")
                d.rounded_rectangle((x, y, x + w, y + button_h), radius=px(5), fill=PAPER, outline=BORDER, width=px(1))
                d.rectangle((x, y + px(3), x + px(4), y + button_h - px(3)), fill="#607f94" if lost else ACCENT)
                rows = str(value).split("\n")
                d.text((x + px(17), y + px(11)), rows[0], font=font(15, serif=True), fill=DEEP)
                for j, row in enumerate(rows[1:]):
                    d.text((x + px(17), y + px(41 + 19 * j)), row, font=font(11), fill=MUTED)
                serial = int(item_key.rsplit("_", 1)[1])
                d.text((x + w - px(15), y + px(13)), "NO." + str(serial).zfill(3), font=font(9, True), fill=ACCENT, anchor="ra")
            else:
                d.rounded_rectangle((x + px(3), y + px(4), x + w + px(3), y + button_h + px(4)), radius=px(6), fill="#ced7d1")
                d.rounded_rectangle((x, y, x + w, y + button_h), radius=px(6), fill=DEEP)
                f = font(14, True)
                rows = lines_for(d, value, f, w - px(28))
                total = len(rows) * px(21)
                start = y + (button_h - total) // 2
                for j, row in enumerate(rows):
                    d.text((x + w // 2, start + j * px(21)), row, font=f, fill=PAPER, anchor="mt")
        elif kind == "badge":
            d.rounded_rectangle((x, y, x + w, y + px(28)), radius=px(3), fill="#fff3e9", outline="#edc3af", width=px(1))
            d.text((x + w // 2, y + px(5)), value, font=font(12, True), fill="#a65434", anchor="mt")
        elif kind == "card":
            if item_key == "picture":
                d.rounded_rectangle((x, y, x + w, y + h), radius=px(5), fill="#e7e7dc", outline="#c7c9be", width=px(1))
                d.ellipse((x + w // 2 - px(60), y + px(16), x + w // 2 + px(60), y + px(136)), outline="#cbd1c8", width=px(1))
                d.rounded_rectangle((x + w // 2 - px(35), y + px(38), x + w // 2 + px(35), y + px(108)), radius=px(5), fill=PAPER, outline=ACCENT, width=px(2))
                d.text((x + w // 2, y + px(54)), "卡", font=font(36, serif=True), fill=DEEP, anchor="mt")
                d.text((x + w // 2, y + px(124)), "物品照片示意", font=font(10, True), fill=MUTED, anchor="mt")
            else:
                d.rounded_rectangle((x, y, x + w, y + h), radius=px(5), fill=PAPER, outline=BORDER, width=px(1))
                d.rectangle((x, y + px(3), x + px(4), y + h - px(3)), fill=ACCENT)
                draw_lines(d, value, x + px(15), y + px(18), w - px(30), font(14), INK, px(24))
        elif kind == "alert":
            d.rectangle((x, y, x + w, y + px(54)), fill="#f8eadf")
            d.rectangle((x, y, x + px(3), y + px(54)), fill=ACCENT)
            draw_lines(d, value, x + px(12), y + px(14), w - px(24), font(13), "#85543c")
        elif kind in {"input", "dropdown", "datepicker", "textarea"}:
            d.text((x, y), item.get("label", ""), font=font(12, True), fill=MUTED)
            field_y = y + px(24)
            field_h = px(55) if kind == "textarea" else px(42)
            d.rounded_rectangle((x, field_y, x + w, field_y + field_h), radius=px(5), fill=PAPER, outline="#becbc8", width=px(1))
            placeholder = item.get("placeholder", "")
            if kind == "dropdown":
                placeholder = str(item.get("items", [""])[0])
                cx, cy = x + w - px(20), field_y + px(22)
                d.polygon([(cx - px(5), cy - px(2)), (cx + px(5), cy - px(2)), (cx, cy + px(4))], fill=MUTED)
            elif kind == "datepicker":
                placeholder = "选择日期"
                cx, cy = x + w - px(22), field_y + px(13)
                d.rectangle((cx - px(6), cy, cx + px(6), cy + px(13)), outline=MUTED, width=px(1))
                d.line((cx - px(6), cy + px(4), cx + px(6), cy + px(4)), fill=MUTED, width=px(1))
            draw_lines(d, placeholder, x + px(12), field_y + px(11), w - px(24), font(12), MUTED, px(20))
        elif kind == "icon":
            d.ellipse((x, y, x + w, y + w), fill="#f8e7d9", outline=ACCENT, width=px(2))
            d.line([(x + px(16), y + px(32)), (x + px(27), y + px(43)), (x + px(49), y + px(20))], fill=ACCENT, width=px(5), joint="curve")
    return image


LABELS = {
    "home": "01  首页 · 浏览信息",
    "search": "02  搜索物品",
    "results": "03  搜索结果",
    "detail": "04  信息详情",
    "contact": "05  领取方式",
    "publish": "06  发布信息",
    "success": "07  发布成功",
    "mine": "08  我的发布",
    "closed": "09  状态更新",
}


def montage(names, filename, title):
    cols = 2
    rows = math.ceil(len(names) / cols)
    margin = 28
    heading = 90
    out = Image.new("RGB", (cols * CELL_W + (cols + 1) * margin, heading + rows * CELL_H + (rows + 1) * margin), BG)
    d = ImageDraw.Draw(out)
    d.text((margin + 8, 24), title, font=font(25, True), fill=INK)
    for i, name in enumerate(names):
        r, c = divmod(i, cols)
        out.paste(draw_screen(name, LABELS[name]), (margin + c * (CELL_W + margin), heading + margin + r * (CELL_H + margin)))
    out.save(ROOT / filename, optimize=True)


montage(["home", "search", "results", "detail", "contact"], "screens-discovery.png", "拾见校园 · 浏览与搜索")
montage(["publish", "success", "mine", "closed"], "screens-publishing.png", "拾见校园 · 发布与状态管理")
montage(list(SCREENS), "storyboard-clean.png", "拾见校园 · 九页原型总览（无导航连线）")
