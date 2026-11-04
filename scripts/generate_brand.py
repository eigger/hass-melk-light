"""Generate Home Assistant brand images for MELK Light Bar.

The artwork is an original geometric brand mark on a dark navy rounded square:
a vertical RGB LED ambient light bar on a pedestal stand, flanked by symmetrical
light rays and golden Bluetooth signal arcs. Drawn from geometric primitives at
4x scale and downsampled, so no source image, external font file, or network
access is needed. Run with Pillow 12.3.0 for reproducible PNGs.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BRAND = Path(__file__).resolve().parents[1] / "custom_components/melk_light/brand"
SIZE = 512
SCALE = 4
NAVY = "#1b2a41"
CYAN = "#38bdf8"
WHITE = "#ffffff"
YELLOW = "#ffd23f"
GOLD = "#f2a900"
ORANGE = "#ff8c1a"
CORAL = "#ff5c77"
WORDMARK = "#0ea5e9"


def _draw_thick_line(
    d: ImageDraw.ImageDraw,
    p0: tuple[float, float],
    p1: tuple[float, float],
    width: float,
    fill: str,
) -> None:
    """Draw a line segment with round caps."""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    r = width / 2.0
    if length > 0:
        nx, ny = -dy / length * r, dx / length * r
        d.polygon(
            [
                (x0 + nx, y0 + ny),
                (x1 + nx, y1 + ny),
                (x1 - nx, y1 - ny),
                (x0 - nx, y0 - ny),
            ],
            fill=fill,
        )
    d.ellipse([x0 - r, y0 - r, x0 + r, y0 + r], fill=fill)
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=fill)


def _draw_arc_ring(
    d: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    r_in: float,
    r_out: float,
    deg_start: float,
    deg_end: float,
    fill: str,
) -> None:
    """Draw a smooth annular sector."""
    steps = 48
    a0 = math.radians(deg_start)
    a1 = math.radians(deg_end)
    pts_out = [
        (
            cx + r_out * math.cos(a0 + (a1 - a0) * i / steps),
            cy + r_out * math.sin(a0 + (a1 - a0) * i / steps),
        )
        for i in range(steps + 1)
    ]
    pts_in = [
        (
            cx + r_in * math.cos(a0 + (a1 - a0) * i / steps),
            cy + r_in * math.sin(a0 + (a1 - a0) * i / steps),
        )
        for i in range(steps + 1)
    ]
    d.polygon(pts_out + list(reversed(pts_in)), fill=fill)


def draw_icon() -> Image.Image:
    """Draw the 512px RGBA app icon."""
    s = SCALE
    image = Image.new("RGBA", (SIZE * s, SIZE * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(image)

    def box(x0: float, y0: float, x1: float, y1: float) -> list[float]:
        return [x0 * s, y0 * s, x1 * s, y1 * s]

    # 1. Dark navy rounded square background.
    d.rounded_rectangle(box(0, 0, SIZE - 1, SIZE - 1), radius=104 * s, fill=NAVY)

    # 2. Symmetrical ambient light rays radiating from left and right of the bar.
    rays = [
        ((178, 168), (114, 146), YELLOW),
        ((174, 238), (100, 238), GOLD),
        ((178, 308), (114, 330), CORAL),
        ((334, 168), (398, 146), YELLOW),
        ((338, 238), (412, 238), GOLD),
        ((334, 308), (398, 330), CORAL),
    ]
    for (x0, y0), (x1, y1), col in rays:
        _draw_thick_line(d, (x0 * s, y0 * s), (x1 * s, y1 * s), width=18 * s, fill=col)

    # 3. Vertical LED Light Bar outer diffuser shell (cyan) & segmented RGB core.
    d.rounded_rectangle(box(214, 72, 298, 384), radius=42 * s, fill=CYAN)
    d.rounded_rectangle(box(232, 92, 280, 364), radius=24 * s, fill=WHITE)

    # Segmented RGB color zones centered vertically inside the diffuser core.
    d.rounded_rectangle(box(240, 104, 272, 180), radius=16 * s, fill=YELLOW)
    d.rounded_rectangle(box(240, 190, 272, 266), radius=12 * s, fill=GOLD)
    d.rounded_rectangle(box(240, 276, 272, 352), radius=16 * s, fill=CORAL)

    # 4. Sculpted pedestal stand at the bottom with a navy knockout separator.
    d.rounded_rectangle(box(144, 396, 368, 444), radius=24 * s, fill=NAVY)
    d.rounded_rectangle(box(236, 376, 276, 418), radius=8 * s, fill=WHITE)
    d.rounded_rectangle(box(156, 406, 356, 438), radius=16 * s, fill=WHITE)
    d.rounded_rectangle(box(212, 416, 300, 428), radius=6 * s, fill=CYAN)

    # 5. Golden BLE wireless signal arcs at the upper right.
    acx, acy = 368 * s, 96 * s
    for r_in, r_out, col in (
        (26 * s, 40 * s, YELLOW),
        (50 * s, 64 * s, ORANGE),
    ):
        _draw_arc_ring(d, acx, acy, r_in, r_out, -68, 16, fill=col)

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
