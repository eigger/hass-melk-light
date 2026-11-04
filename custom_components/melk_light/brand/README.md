# MELK Light Bar brand assets

An original geometric RGB LED light bar icon drawn by
`scripts/generate_brand.py` on a dark navy rounded square, with a matching sky
blue `MELK Light` wordmark for the landscape logo. No third-party artwork is
used.

| File | Size | Purpose |
| --- | --- | --- |
| `icon.png` | 256 × 256 | Home Assistant and HACS icon |
| `icon@2x.png` | 512 × 512 | High-resolution icon |
| `logo.png` | 1071 × 256 | Landscape integration logo; README artwork |
| `logo@2x.png` | 2142 × 512 | High-resolution landscape logo |

All images are RGBA PNGs with transparent outer corners and backgrounds. These
sizes follow the [HA brand image guidelines](https://contributors.home-assistant.io/core/integrations/brands/).
Home Assistant 2026.3 and later serves these assets from the integration's local
`brand/` directory. The sky blue wordmark works against light and dark
backgrounds, so separate dark variants are not required.

## Source and permission

The icon is drawn from geometric primitives in this repository's
`scripts/generate_brand.py` and is covered by the repository's MIT license
(Copyright (c) 2026 eigger). The wordmark is rendered with Pillow's bundled
Aileron Regular via
[`ImageFont.load_default`](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.load_default).
[Aileron](https://dotcolon.net/font/aileron/) permits commercial use and is
released with no rights reserved. No font file is redistributed or loaded from
the system.

## Reproduce

Use Python 3.10 or newer and Pillow 12.3.0 (also supplied by HA 2026.10.2):

```sh
python -m pip install Pillow==12.3.0
python scripts/generate_brand.py
```

The script needs no network access and produces the same PNG bytes on every
run with that Pillow version.

SHA256 (Pillow 12.3.0):

- `icon@2x.png`: `87637f78daa21ccb46257d653305145cf32d1624ef950e3b7ec233af6e35c5a5`
- `icon.png`: `cd6a248f81c92450a3089d4e299c56a3b6f8b20ba307492f72a47f744c14705c`
- `logo@2x.png`: `ad5cc1dfbd7b0d4f10f08738f2e6cea520a1b13394dbf501003826cfe42de327`
- `logo.png`: `2681d0302f3426c2ec8d011559700cd84ade85bfbf28b0ef9320a598c0ca8908`

The local `brand/icon.png` is used by the
[HACS brands check](https://hacs.xyz/docs/publish/include/#check-brands).
These files do not imply inclusion in the HACS default list or HA brands
repository. README pages use `custom_components/melk_light/brand/logo.png`.
