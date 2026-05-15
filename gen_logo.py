#!/usr/bin/env python3
"""Generate logo with rounded corners, purple shadow & glow effect baked into PNG."""

from PIL import Image, ImageDraw, ImageFilter

SRC = "/Users/zhiyang/Desktop/Scanners-Box/logo.png"
DST = "/Users/zhiyang/Desktop/Scanners-Box/logo.png"

# Config - matching original CSS intent
TARGET_WIDTH = 600
RADIUS = 32
SHADOW_OFFSET = (10, 10)
SHADOW_BLUR = 20
GLOW_BLUR = 35
PADDING = 40

# Purple theme colors (matching CSS: rgba(99,102,241,0.35), rgba(139,92,246,0.2), rgba(167,139,250,0.3))
SHADOW_COLOR = (99, 102, 241, 100)
GLOW_OUTER = (139, 92, 246, 45)
GLOW_INNER = (167, 139, 250, 70)


def round_corner_mask(size, radius):
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size[0] - 1, size[1] - 1)], radius=radius, fill=255)
    return mask


def apply_rounded_corners(img, radius):
    mask = round_corner_mask(img.size, radius)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result


def add_shadow_and_glow(img):
    iw, ih = img.size
    cw = iw + PADDING * 2 + SHADOW_OFFSET[0] + SHADOW_BLUR
    ch = ih + PADDING * 2 + SHADOW_OFFSET[1] + SHADOW_BLUR
    
    canvas = Image.new("RGBA", (cw, ch), (255, 255, 255, 0))
    
    alpha = img.split()[3]
    
    # Outer glow
    glow = Image.new("RGBA", (iw, ih), GLOW_OUTER)
    glow.putalpha(alpha)
    gb = glow.filter(ImageFilter.GaussianBlur(GLOW_BLUR))
    off = PADDING + GLOW_BLUR // 2
    canvas.paste(gb, (off, off), gb)
    
    # Inner glow (brighter, tighter)
    gi = Image.new("RGBA", (iw, ih), GLOW_INNER)
    gi.putalpha(alpha)
    gib = gi.filter(ImageFilter.GaussianBlur(GLOW_BLUR // 2))
    o2 = PADDING + GLOW_BLUR // 4
    canvas.paste(gib, (o2, o2), gib)
    
    # Drop shadow
    shadow = Image.new("RGBA", (iw, ih), SHADOW_COLOR)
    shadow.putalpha(alpha)
    sb = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
    sx = PADDING + SHADOW_OFFSET[0]
    sy = PADDING + SHADOW_OFFSET[1]
    canvas.paste(sb, (sx, sy), sb)
    
    # Original image on top
    canvas.paste(img, (PADDING, PADDING), img)
    
    return canvas


img = Image.open(SRC).convert("RGBA")
aspect = img.height / img.width
new_size = (TARGET_WIDTH, int(TARGET_WIDTH * aspect))
img = img.resize(new_size, Image.LANCZOS)

img = apply_rounded_corners(img, RADIUS * 2)
result = add_shadow_and_glow(img)

result.save(DST, "PNG")
print(f"Done! {result.size[0]}x{result.size[1]} -> {DST}")
