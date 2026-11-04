"""Generate Home Assistant brand images for MELK Light Bar.

The artwork preserves the original minimalist MELK Light Bar concept on a dark
navy rounded square: a sleek vertical cyan glowing light bar hovering above a
clean white horizontal base stand. Drawn from geometric primitives at 4x scale
and downsampled, so no source image, external font file, or network access is
needed. Run with Pillow 12.3.0 for reproducible PNGs.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BRAND = Path(__file__).resolve().parents[1] / "custom_components/melk_light/brand"
SIZE = 512
SCALE = 4
NAVY = "#151c28"
GLOW_OUTER = "#1c3554"
GLOW_INNER = "#20507a"
CYAN = "#38bdf8"
CYAN_BRIGHT = "#bae6fd"
STAND_WHITE = "#edf2f7"
WORDMARK = "#0ea5e9"


def draw_icon() -> Image.Image:
    """Draw the 512px RGBA app icon."""
    s = SCALE
    image = Image.new("RGBA", (SIZE * s, SIZE * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    def box(x0: float, y0: float, x1: float, y1: float) -> list[float]:
        return [x0 * s, y0 * s, x1 * s, y1 * s]

    # 1. Dark navy rounded square background.
    d.rounded_rectangle(box(0, 0, SIZE - 1, SIZE - 1), radius=104 * s, fill=NAVY)

    # 2. Subtle concentric ambient glow halos around the vertical light bar.
    d.rounded_rectangle(box(196, 56, 316, 402), radius=60 * s, fill=GLOW_OUTER)
    d.rounded_rectangle(box(212, 64, 300, 394), radius=44 * s, fill=GLOW_INNER)

    # 3. Crisp vertical cyan light bar with a bright inner diffuser core.
    d.rounded_rectangle(box(230, 72, 282, 386), radius=26 * s, fill=CYAN)
    d.rounded_rectangle(box(244, 92, 268, 366), radius=12 * s, fill=CYAN_BRIGHT)

    # 4. Clean horizontal white pill stand at the bottom (with navy separation gap).
    d.rounded_rectangle(box(172, 412, 340, 440), radius=14 * s, fill=STAND_WHITE)

    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def main() -> None:
    """Write icon.png, icon@2x.png, logo.png and logo@2x.png."""
    BRAND.mkdir(parents=True, exist_ok=True)
    icon = draw_icon()
    icon.save(BRAND / "icon@2x.png", optimize=True)
    icon.resize((256, 256), Image.Resampling.LANCZOS).save(
        BRAND / "icon.png", optimize=True
    )

    # Pillow bundles Aileron Regular, so regeneration needs no system fonts.
    font = ImageFont.load_default(size=304)
    bounds = font.getbbox("MELK Light")
    wordmark = Image.new("RGBA", (bounds[2] - bounds[0], bounds[3] - bounds[1]))
    ImageDraw.Draw(wordmark).text(
        (-bounds[0], -bounds[1]), "MELK Light", font=font, fill=WORDMARK
    )
    wordmark = wordmark.crop(wordmark.getbbox())
    gap = 96 + ((SIZE + 96 + wordmark.width) % 2)
    logo = Image.new("RGBA", (SIZE + gap + wordmark.width, SIZE))
    logo.alpha_composite(icon, (0, 0))
    logo.alpha_composite(wordmark, (SIZE + gap, (SIZE - wordmark.height) // 2))
    logo = logo.crop(logo.getbbox())
    logo.save(BRAND / "logo@2x.png", optimize=True)
    logo.resize((logo.width // 2, logo.height // 2), Image.Resampling.LANCZOS).save(
        BRAND / "logo.png", optimize=True
    )


if __name__ == "__main__":
    main()
