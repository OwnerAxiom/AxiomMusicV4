# AxiomMusic/utils/thumbnails.py

import os
import random
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# ============ PATHS ============
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "AxiomMusic", "assets")

FONT_TITLE = os.path.join(ASSETS_DIR, "f.ttf")
FONT_NORMAL = os.path.join(ASSETS_DIR, "cfont.ttf")

# ============ COLORS ============
GREEN_PRIMARY = (76, 175, 80)
GREEN_LIGHT = (144, 202, 148)
GREEN_DARK = (46, 125, 50)
GREEN_ACCENT = (102, 187, 106)
GREEN_WAVEFORM = (60, 160, 65)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)

# ============ CARD DIMENSIONS ============
THUMB_WIDTH = 1280
THUMB_HEIGHT = 720
CARD_X = 140
CARD_Y = 50
CARD_W = 1000
CARD_H = 620
CARD_RADIUS = 45


def _load_font(path, size):
    """Load font safely, fallback to default"""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()


def _draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw rounded rectangle"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _create_rounded_image(img, radius):
    """Make image corners rounded"""
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=radius, fill=255)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result


def _draw_waveform(draw, x, y, width, height, color, progress=0.35, num_bars=90):
    """Draw audio waveform bars"""
    bar_w = max(2, (width - num_bars * 2) // num_bars)
    gap = 2
    random.seed(123)

    for i in range(num_bars):
        bx = x + i * (bar_w + gap)
        # Waveform shape: higher in middle, lower at edges
        center_factor = 1.0 - abs(i - num_bars / 2) / (num_bars / 2)
        base_h = random.randint(10, height)
        bar_h = int(base_h * (0.25 + 0.75 * center_factor ** 1.5))
        by = y + (height - bar_h) // 2

        if i / num_bars <= progress:
            draw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=color)
        else:
            faded = tuple(max(0, c - 100) for c in color)
            draw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=faded)


def _draw_progress_bar(draw, x, y, width, progress, color, handle_color):
    """Draw progress bar with handle"""
    track_h = 6
    track_y = y - track_h // 2
    # Background track
    draw.rounded_rectangle([x, track_y, x + width, track_y + track_h], radius=3, fill=(200, 200, 200))
    # Progress fill
    pw = int(width * progress)
    if pw > 0:
        draw.rounded_rectangle([x, track_y, x + pw, track_y + track_h], radius=3, fill=color)
    # Handle
    hx = x + pw
    draw.ellipse([hx - 11, y - 11, hx + 11, y + 11], fill=handle_color, outline=WHITE, width=2)


def _draw_volume_bar(draw, x, y, width, volume, color):
    """Draw volume bar"""
    track_h = 6
    track_y = y - track_h // 2
    draw.rounded_rectangle([x, track_y, x + width, track_y + track_h], radius=3, fill=(200, 200, 200))
    vw = int(width * volume)
    if vw > 0:
        draw.rounded_rectangle([x, track_y, x + vw, track_y + track_h], radius=3, fill=color)
    hx = x + vw
    draw.ellipse([hx - 10, y - 10, hx + 10, y + 10], fill=WHITE, outline=GREEN_LIGHT, width=2)


def _draw_play_triangle(draw, cx, cy, size, color):
    """Draw play triangle"""
    h = size * 0.866
    pts = [
        (cx - size * 0.4, cy - h * 0.5),
        (cx - size * 0.4, cy + h * 0.5),
        (cx + size * 0.5, cy),
    ]
    draw.polygon(pts, fill=color)


def _draw_skip_triangle(draw, cx, cy, size, color, direction=1):
    """Draw skip forward/backward triangle"""
    h = size * 0.7
    if direction == 1:
        pts = [(cx - h * 0.4, cy - h * 0.5), (cx - h * 0.4, cy + h * 0.5), (cx + h * 0.5, cy)]
    else:
        pts = [(cx + h * 0.4, cy - h * 0.5), (cx + h * 0.4, cy + h * 0.5), (cx - h * 0.5, cy)]
    draw.polygon(pts, fill=color)
    # Vertical bar
    bar_x = cx + h * 0.55 if direction == 1 else cx - h * 0.55 - 4
    draw.rectangle([bar_x, cy - h * 0.5, bar_x + 4, cy + h * 0.5], fill=color)


def _draw_shuffle_icon(draw, cx, cy, size, color):
    """Draw shuffle icon (crossed arrows)"""
    s = size * 0.4
    # Two crossing lines with arrow heads
    draw.line([cx - s, cy - s, cx + s, cy + s], fill=color, width=3)
    draw.line([cx - s, cy + s, cx + s, cy - s], fill=color, width=3)
    # Arrow heads
    draw.polygon([(cx + s, cy + s), (cx + s - 6, cy + s - 2), (cx + s - 2, cy + s - 6)], fill=color)
    draw.polygon([(cx - s, cy - s), (cx - s + 6, cy - s + 2), (cx - s + 2, cy - s + 6)], fill=color)


def _draw_repeat_icon(draw, cx, cy, size, color):
    """Draw repeat icon (circular arrows)"""
    r = size * 0.35
    # Draw two curved arrows
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=30, end=150, fill=color, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=210, end=330, fill=color, width=3)
    # Arrow heads
    draw.polygon([(cx + r * 0.5, cy - r * 0.86), (cx + r * 0.3, cy - r * 0.7), (cx + r * 0.7, cy - r * 0.6)], fill=color)
    draw.polygon([(cx - r * 0.5, cy + r * 0.86), (cx - r * 0.3, cy + r * 0.7), (cx - r * 0.7, cy + r * 0.6)], fill=color)


def _draw_button_pill(draw, x, y, w, h, radius, icon_char, label, font_icon, font_label, bg_color, text_color):
    """Draw pill button with icon and label"""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg_color, outline=(255, 255, 255, 60), width=1)
    # Icon
    icon_bbox = draw.textbbox((0, 0), icon_char, font=font_icon)
    icon_w = icon_bbox[2] - icon_bbox[0]
    icon_x = x + 18
    icon_y = y + (h - (icon_bbox[3] - icon_bbox[1])) // 2 - icon_bbox[1]
    draw.text((icon_x, icon_y), icon_char, fill=text_color, font=font_icon)
    # Label
    label_x = icon_x + icon_w + 10
    label_y = y + (h - (font_label.getbbox(label)[3] - font_label.getbbox(label)[1])) // 2 - font_label.getbbox(label)[1]
    draw.text((label_x, label_y), label, fill=text_color, font=font_label)


def _create_greenery_background():
    """Create a lush green nature background"""
    img = Image.new("RGB", (THUMB_WIDTH, THUMB_HEIGHT), (30, 80, 30))
    draw = ImageDraw.Draw(img)

    # Base gradient - dark green at bottom, lighter at top
    for y in range(THUMB_HEIGHT):
        ratio = y / THUMB_HEIGHT
        r = int(20 + 40 * (1 - ratio))
        g = int(60 + 100 * (1 - ratio * 0.5))
        b = int(20 + 30 * (1 - ratio))
        draw.line([(0, y), (THUMB_WIDTH, y)], fill=(r, g, b))

    # Add some texture/noise for grass-like feel
    random.seed(42)
    for _ in range(3000):
        x = random.randint(0, THUMB_WIDTH)
        y = random.randint(0, THUMB_HEIGHT)
        shade = random.randint(40, 120)
        draw.point((x, y), fill=(shade, shade + 60, shade))

    # Blur for soft background
    img = img.filter(ImageFilter.GaussianBlur(radius=8))

    return img.convert("RGBA")


def _add_light_beam(base_img):
    """Add light beam effect from top center"""
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx = THUMB_WIDTH // 2
    for y in range(0, 400):
        alpha = int(50 * (1 - y / 400) ** 2)
        beam_w = int(80 + y * 1.2)
        draw.line([(cx - beam_w, y), (cx + beam_w, y)], fill=(255, 255, 240, alpha))

    return Image.alpha_composite(base_img, overlay)


def _add_card_shadow(base_img, card_x, card_y, card_w, card_h, radius):
    """Add 3D drop shadow under card"""
    shadow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    # Multiple shadow layers for depth
    for offset in range(15, 0, -1):
        alpha = int(60 * (1 - offset / 15))
        draw.rounded_rectangle(
            [card_x + offset, card_y + offset + 5, card_x + card_w + offset, card_y + card_h + offset + 5],
            radius=radius,
            fill=(0, 0, 0, alpha),
        )
    return Image.alpha_composite(base_img, shadow)


def _create_card_base():
    """Create the glassmorphism card base"""
    card = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)

    # Main card background - translucent green-white
    card_bg_color = (220, 235, 220, 200)
    draw.rounded_rectangle([0, 0, CARD_W - 1, CARD_H - 1], radius=CARD_RADIUS, fill=card_bg_color)

    # Inner highlight (top light)
    for y in range(0, 150):
        alpha = int(60 * (1 - y / 150))
        draw.line([(10, y), (CARD_W - 10, y)], fill=(255, 255, 255, alpha))

    # Border
    draw.rounded_rectangle([2, 2, CARD_W - 3, CARD_H - 3], radius=CARD_RADIUS - 2, outline=(255, 255, 255, 80), width=2)

    # Bottom subtle shadow inside card
    for y in range(CARD_H - 100, CARD_H - 2):
        alpha = int(30 * ((y - (CARD_H - 100)) / 100))
        draw.line([(10, y), (CARD_W - 10, y)], fill=(0, 0, 0, alpha))

    return card


def get_thumb(videoid, title, duration, channel="OwnerAxiom", views="1.2M views",
              album_art_path=None, profile_pic_path=None):
    """
    Generate music player thumbnail.

    Args:
        videoid: YouTube video ID (used for caching/filename)
        title: Song/Video title
        duration: Duration string (e.g., "03:45")
        channel: Channel name
        views: View count string
        album_art_path: Path to album art image (optional)
        profile_pic_path: Path to user profile pic (optional)

    Returns:
        Path to generated thumbnail image
    """
    # Parse duration for progress calculation
    try:
        parts = duration.split(":")
        if len(parts) == 2:
            total_seconds = int(parts[0]) * 60 + int(parts[1])
        else:
            total_seconds = 225  # default 3:45
    except Exception:
        total_seconds = 225

    # Simulate current time at ~35% progress
    current_seconds = int(total_seconds * 0.35)
    current_min = current_seconds // 60
    current_sec = current_seconds % 60
    current_time = f"{current_min:02d}:{current_sec:02d}"
    progress = 0.35

    # ============ LOAD FONTS ============
    font_title = _load_font(FONT_TITLE, 44)
    font_subtitle = _load_font(FONT_NORMAL, 22)
    font_time = _load_font(FONT_NORMAL, 20)
    font_button_label = _load_font(FONT_NORMAL, 17)
    font_button_icon = _load_font(FONT_NORMAL, 26)
    font_heart = _load_font(FONT_NORMAL, 30)

    # ============ CREATE BACKGROUND ============
    bg = _create_greenery_background()
    bg = _add_light_beam(bg)

    # ============ CREATE CARD ============
    card = _create_card_base()
    draw = ImageDraw.Draw(card)

    # ---- TOP SECTION ----
    # Album art thumbnail
    thumb_size = 110
    thumb_x, thumb_y = 45, 45

    if album_art_path and os.path.exists(album_art_path):
        album_img = Image.open(album_art_path).resize((thumb_size, thumb_size)).convert("RGBA")
    else:
        # Default album art - green nature scene
        album_img = Image.new("RGBA", (thumb_size, thumb_size), (60, 130, 60, 255))
        aa_draw = ImageDraw.Draw(album_img)
        # Draw simple landscape
        aa_draw.rectangle([0, 60, thumb_size, thumb_size], fill=(40, 100, 40))
        aa_draw.ellipse([20, 20, 90, 70], fill=(80, 160, 80))
        aa_text = _load_font(FONT_NORMAL, 14)
        aa_draw.text((15, 80), "Axiom", fill=WHITE, font=aa_text)
        aa_draw.text((15, 95), "Music", fill=WHITE, font=aa_text)

    album_img = _create_rounded_image(album_img, 18)
    card.paste(album_img, (thumb_x, thumb_y), album_img)

    # Profile picture (top-right, replaces 3 dots)
    profile_size = 70
    profile_x = CARD_W - profile_size - 45
    profile_y = 55

    if profile_pic_path and os.path.exists(profile_pic_path):
        profile_img = Image.open(profile_pic_path).resize((profile_size, profile_size)).convert("RGBA")
    else:
        # Default profile - simple avatar
        profile_img = Image.new("RGBA", (profile_size, profile_size), (100, 100, 100, 255))
        pp_draw = ImageDraw.Draw(profile_img)
        pp_draw.ellipse([15, 10, 55, 50], fill=(180, 180, 180, 255))  # head
        pp_draw.ellipse([10, 45, 60, 75], fill=(180, 180, 180, 255))  # body

    profile_img = _create_rounded_image(profile_img, profile_size // 2)
    card.paste(profile_img, (profile_x, profile_y), profile_img)

    # Title text
    title_x = thumb_x + thumb_size + 25
    title_y = 55
    draw.text((title_x, title_y), title, fill=WHITE, font=font_title)

    # Green heart after title
    title_bbox = draw.textbbox((title_x, title_y), title, font=font_title)
    heart_x = title_bbox[2] + 12
    draw.text((heart_x, title_y + 2), "💚", fill=GREEN_PRIMARY, font=font_heart)

    # Channel name and views
    subtitle_y = title_y + 52
    draw.text((title_x, subtitle_y), channel, fill=(230, 230, 230, 255), font=font_subtitle)
    channel_bbox = draw.textbbox((title_x, subtitle_y), channel, font=font_subtitle)
    views_x = channel_bbox[2] + 30
    draw.text((views_x, subtitle_y), views, fill=(200, 200, 200, 255), font=font_subtitle)

    # ---- WAVEFORM ----
    wave_y = 195
    wave_x = 45
    wave_w = CARD_W - 90
    wave_h = 55
    _draw_waveform(draw, wave_x, wave_y, wave_w, wave_h, GREEN_WAVEFORM, progress=progress)

    # ---- PROGRESS BAR ----
    prog_y = 280
    prog_x = 45
    prog_w = CARD_W - 90
    _draw_progress_bar(draw, prog_x, prog_y, prog_w, progress, GREEN_PRIMARY, GREEN_LIGHT)

    # Time labels
    draw.text((prog_x, prog_y + 18), current_time, fill=WHITE, font=font_time)
    dur_bbox = draw.textbbox((0, 0), duration, font=font_time)
    dur_w = dur_bbox[2] - dur_bbox[0]
    draw.text((prog_x + prog_w - dur_w, prog_y + 18), duration, fill=WHITE, font=font_time)

    # ---- CONTROL BUTTONS ----
    ctrl_y = 355
    center_x = CARD_W // 2

    # Shuffle (far left) - green outline style
    shuffle_x = 90
    _draw_shuffle_icon(draw, shuffle_x, ctrl_y, 50, GREEN_PRIMARY)

    # Previous (black)
    prev_x = center_x - 170
    _draw_skip_triangle(draw, prev_x, ctrl_y, 45, BLACK, direction=-1)

    # Play button (large green circle)
    play_x = center_x
    play_y = ctrl_y + 5
    play_r = 48
    # Outer glow
    draw.ellipse([play_x - play_r - 4, play_y - play_r - 4, play_x + play_r + 4, play_y + play_r + 4],
                 fill=(76, 175, 80, 80))
    # Main circle
    draw.ellipse([play_x - play_r, play_y - play_r, play_x + play_r, play_y + play_r],
                 fill=GREEN_DARK, outline=GREEN_LIGHT, width=2)
    # Inner highlight
    draw.ellipse([play_x - play_r + 8, play_y - play_r + 8, play_x + play_r - 8, play_y - 10],
                 fill=(100, 200, 100, 60))
    # Play triangle
    _draw_play_triangle(draw, play_x + 3, play_y, 30, WHITE)

    # Next (black)
    next_x = center_x + 170
    _draw_skip_triangle(draw, next_x, ctrl_y, 45, BLACK, direction=1)

    # Repeat (far right) - green outline style
    repeat_x = CARD_W - 90
    _draw_repeat_icon(draw, repeat_x, ctrl_y, 50, GREEN_PRIMARY)

    # ---- BOTTOM BUTTONS (Queue, Autoplay, Speed, Settings) ----
    btn_y = 445
    btn_w = 195
    btn_h = 52
    btn_r = 26
    btn_gap = 25
    total_btn_w = 4 * btn_w + 3 * btn_gap
    btn_start_x = (CARD_W - total_btn_w) // 2

    buttons = [
        ("", "QUEUE"),
        ("▶", "AUTOPLAY"),
        ("⚡", "SPEED"),
        ("⚙", "SETTINGS"),
    ]

    btn_bg = (80, 160, 80, 120)  # Green translucent
    btn_text = WHITE

    for i, (icon, label) in enumerate(buttons):
        bx = btn_start_x + i * (btn_w + btn_gap)
        _draw_button_pill(draw, bx, btn_y, btn_w, btn_h, btn_r, icon, label,
                          font_button_icon, font_button_label, btn_bg, btn_text)

    # ---- VOLUME BAR ----
    vol_y = 545
    vol_x = 70
    vol_w = CARD_W - 140
    _draw_volume_bar(draw, vol_x, vol_y, vol_w, 0.55, GREEN_PRIMARY)

    # Volume icons
    vol_icon_font = _load_font(FONT_NORMAL, 24)
    draw.text((25, vol_y - 12), "🔈", fill=WHITE, font=vol_icon_font)
    draw.text((CARD_W - 50, vol_y - 12), "🔊", fill=WHITE, font=vol_icon_font)

    # ============ COMPOSE FINAL ============
    # Add card shadow to background
    bg = _add_card_shadow(bg, CARD_X, CARD_Y, CARD_W, CARD_H, CARD_RADIUS)

    # Paste card onto background
    bg.paste(card, (CARD_X, CARD_Y), card)

    # Add subtle vignette
    vignette = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for i in range(50):
        alpha = int(40 * (i / 50))
        vdraw.rectangle([i, i, THUMB_WIDTH - i - 1, THUMB_HEIGHT - i - 1], outline=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, vignette)

    # ============ SAVE ============
    output_dir = os.path.join(BASE_DIR, "AxiomMusic", "assets", "cache")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"thumb_{videoid}.png")

    final = bg.convert("RGB")
    final.save(output_path, "PNG", quality=95)

    return output_path


# For testing
if __name__ == "__main__":
    result = get_thumb(
        videoid="test123",
        title="Axiom X Music",
        duration="03:45",
        channel="OwnerAxiom",
        views="1.2M views",
    )
    print(f"Generated: {result}")
