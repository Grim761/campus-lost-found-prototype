from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMG = Image.new("RGB", (1500, 560), "#eee9dd")
draw = ImageDraw.Draw(IMG)
font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 25)
font_bold = ImageFont.truetype(r"C:\Windows\Fonts\STSONG.TTF", 34)
small = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 20)

def text_center(text, x, y, width, height, use_font, fill):
    box = draw.textbbox((0, 0), text, font=use_font)
    tw, th = box[2] - box[0], box[3] - box[1]
    draw.text((x + (width - tw) / 2, y + (height - th) / 2 - box[1]), text, font=use_font, fill=fill)

def node(label, x, y, accent=False):
    fill = "#172f42" if accent else "#fffdf7"
    outline = "#172f42" if accent else "#c6c9c0"
    color = "#fffdf7" if accent else "#203646"
    draw.rounded_rectangle((x + 4, y + 4, x + 234, y + 82), radius=7, fill="#d4d0c5")
    draw.rounded_rectangle((x, y, x + 230, y + 78), radius=7, fill=fill, outline=outline, width=2)
    text_center(label, x, y, 230, 78, font, color)

def arrow(x, y):
    draw.line((x, y, x + 40, y), fill="#c96642", width=4)
    draw.polygon([(x + 40, y - 9), (x + 56, y), (x + 40, y + 9)], fill="#c96642")

draw.rounded_rectangle((34, 28, 1466, 260), radius=8, fill="#f7f3e9", outline="#d9d7cb", width=2)
draw.rounded_rectangle((34, 300, 1466, 532), radius=8, fill="#f7f3e9", outline="#d9d7cb", width=2)
draw.rectangle((34, 28, 42, 260), fill="#c96642")
draw.rectangle((34, 300, 42, 532), fill="#607f94")
draw.text((64, 51), "流程一 · 寻找与领取", font=font_bold, fill="#172f42")
draw.text((64, 323), "流程二 · 发布与状态更新", font=font_bold, fill="#172f42")

for y, labels in [
    (133, ["进入首页", "浏览或搜索信息", "查看物品详情", "联系并核对", "找回或归还"]),
    (405, ["进入发布页面", "选择寻物/招领", "填写物品信息", "确认发布", "成功后改状态"]),
]:
    for i, label in enumerate(labels):
        x = 60 + i * 285
        node(label, x, y, accent=i == 4)
        if i < 4:
            arrow(x + 232, y + 39)

draw.text((60, 236), "核对特征后线下交接，避免冒领。", font=small, fill="#6c7b80")
draw.text((60, 508), "找到或归还后及时标记完成，减少无效联系。", font=small, fill="#6c7b80")
IMG.save(ROOT / "使用流程图.png")
IMG.save(ROOT / "flowchart.png")
