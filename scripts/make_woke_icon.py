"""Gera o ícone do aplicativo WOKE em ICO e PNG."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def draw_icon(size: int = 512) -> Image.Image:
    image = Image.new("RGBA", (size, size), "#f8fafc")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((20, 20, size - 20, size - 20), radius=110, fill="#0f766e")
    draw.ellipse((300, -40, 560, 220), fill="#be185d")
    try:
        font = ImageFont.truetype("segoeuib.ttf", 210)
    except OSError:
        font = ImageFont.load_default()
    draw.text((58, 135), "W", font=font, fill="white", stroke_width=2)
    for x, y in ((340, 330), (410, 275), (430, 395)):
        draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill="#fef3c7")
    draw.line((340, 330, 410, 275, 430, 395, 340, 330), fill="#fef3c7", width=7)
    return image


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    image = draw_icon()
    image.save(ASSETS / "woke.png")
    image.save(ASSETS / "woke.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == "__main__":
    main()
