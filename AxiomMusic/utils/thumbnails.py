import os
import re
import random
import aiohttp
import aiofiles
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from functools import lru_cache

# ═══════════════════════════════════════════════════════════════════
# PATHS & CONFIG
# ═══════════════════════════════════════════════════════════════════
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ASSETS      = os.path.join(BASE_DIR, "..", "assets")
FONT_TITLE  = os.path.join(ASSETS, "f.ttf")
FONT_NORMAL = os.path.join(ASSETS, "cfont.ttf")

# Thumbnail dimensions
W, H = 1280, 720

# Colors - Green theme
GREEN_PRIMARY   = (76, 175, 80)
GREEN_LIGHT     = (129, 199, 132)
GREEN_DARK      = (56, 142, 60)
GREEN_ACCENT    = (102, 187, 106)
GREEN_WAVEFORM  = (60, 160, 65)
WHITE           = (255, 255, 255)
BLACK           = (30, 30, 30)
GRAY            = (180, 180, 180)

# Card dimensions
CARD_X, CARD_Y = 140, 50
CARD_W, CARD_H = 1000, 620
CARD_RADIUS    = 45

# In-memory cache
_thumb_memory: dict = {}


@lru_cache(maxsize=4)
def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load font with fallback"""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            return ImageFont.load_default()


def _draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw rounded rectangle"""
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _create_rounded_image(img, radius):
    """Make image corners rounded"""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=radius, fill=255)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result


def _draw_waveform(draw, x, y, width, height, color, progress=0.35, num_bars=90):
    """Draw audio waveform"""
    bar_w = max(2, (width - num_bars * 2) // num_bars)
    gap = 2
    random.seed(123)
    
    for i in range(num_bars):
        bx = x + i * (bar_w + gap)
        center_factor = 1.0 - abs(i - num_bars/2) / (num_bars/2)
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
    
    # Background
    draw.rounded_rectangle([x, track_y, x + width, track_y + track_h], radius=3, fill=(200, 200, 200))
    
    # Progress
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


def _create_greenery_background():
    """Create lush green nature background"""
    img = Image.new("RGB", (W, H), (30, 80, 30))
    draw = ImageDraw.Draw(img)
    
    # Gradient
    for y in range(H):
        ratio = y / H
        r = int(20 + 40 * (1 - ratio))
        g = int(60 + 100 * (1 - ratio * 0.5))
        b = int(20 + 30 * (1 - ratio))
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    
    # Texture
    random.seed(42)
    for _ in range(3000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        shade = random.randint(40, 120)
        draw.point((x, y), fill=(shade, shade + 60, shade))
    
    return img.filter(ImageFilter.GaussianBlur(radius=8))


def _add_light_beam(base_img):
    """Add light beam from top"""
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    cx = W // 2
    for y in range(0, 400):
        alpha = int(50 * (1 - y/400) ** 2)
        beam_w = int(80 + y * 1.2)
        draw.line([(cx - beam_w, y), (cx + beam_w, y)], fill=(255, 255, 240, alpha))
    
    return Image.alpha_composite(base_img, overlay)


def _add_card_shadow(base_img, card_x, card_y, card_w, card_h, radius):
    """Add 3D drop shadow"""
    shadow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    for offset in range(15, 0, -1):
        alpha = int(60 * (1 - offset/15))
        draw.rounded_rectangle(
            [card_x + offset, card_y + offset + 5, card_x + card_w + offset, card_y + card_h + offset + 5],
            radius=radius, fill=(0, 0, 0, alpha)
        )
    
    return Image.alpha_composite(base_img, shadow)


def _create_card_base():
    """Create glassmorphism card"""
    card = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    
    # Background
    draw.rounded_rectangle([0, 0, CARD_W-1, CARD_H-1], radius=CARD_RADIUS, fill=(220, 235, 220, 200))
    
    # Top highlight
    for y in range(0, 150):
        alpha = int(60 * (1 - y/150))
        draw.line([(10, y), (CARD_W-10, y)], fill=(255, 255, 255, alpha))
    
    # Border
    draw.rounded_rectangle([2, 2, CARD_W-3, CARD_H-3], radius=CARD_RADIUS-2, 
                          outline=(255, 255, 255, 80), width=2)
    
    return card


def _truncate(draw, text, font, max_w):
    """Truncate text with ellipsis"""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


async def get_thumb(videoid: str, user_name: str = "AxiomUser") -> str:
    """Generate music player thumbnail"""
    output = f"cache/{videoid}.png"
    cache = f"cache/thumb_{videoid}.jpg"
    os.makedirs("cache", exist_ok=True)
    
    # Always regenerate
    if os.path.exists(output):
        try:
            os.remove(output)
        except:
            pass
    
    # Fetch metadata
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        from py_yt import VideosSearch
        data = (await VideosSearch(url, limit=1).next())["result"][0]
        title = re.sub(r"[\x00-\x1f\x7f]", "", data.get("title", "Unknown")).strip()
        duration = data.get("duration", "00:00") or "00:00"
        thumb_url = data.get("thumbnails", [{}])[-1].get("url", "").split("?")[0]
        v_raw = str(data.get("viewCount", {}).get("short", "N/A"))
        vc = re.sub(r'\s*views?\s*', '', v_raw, flags=re.IGNORECASE).strip()
        views, channel = f"{vc} views", data.get("channel", {}).get("name", "Unknown")
    except Exception:
        return "https://files.catbox.moe/alu3pu.jpg"
    
    # Download thumbnail
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(thumb_url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                async with aiofiles.open(cache, "wb") as f:
                    await f.write(await r.read())
        song_img = Image.open(cache).convert("RGBA")
    except Exception:
        song_img = Image.new("RGBA", (200, 200), (76, 175, 80, 255))
    
    # Parse duration
    try:
        parts = duration.split(":")
        total_seconds = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 225
    except:
        total_seconds = 225
    
    current_seconds = int(total_seconds * 0.35)
    current_time = f"{current_seconds // 60:02d}:{current_seconds % 60:02d}"
    progress = 0.35
    
    # ============ CREATE BACKGROUND ============
    bg = _create_greenery_background()
    bg = _add_light_beam(bg)
    
    # ============ CREATE CARD ============
    card = _create_card_base()
    draw = ImageDraw.Draw(card)
    
    # Load fonts
    font_title = _get_font(FONT_TITLE, 44)
    font_subtitle = _get_font(FONT_NORMAL, 22)
    font_time = _get_font(FONT_NORMAL, 20)
    font_button = _get_font(FONT_NORMAL, 17)
    font_icon = _get_font(FONT_NORMAL, 26)
    font_heart = _get_font(FONT_NORMAL, 30)
    
    # ---- ALBUM ART (top-left) ----
    thumb_size = 110
    thumb_x, thumb_y = 45, 45
    
    album_img = _create_rounded_image(song_img.resize((thumb_size, thumb_size)), 18)
    card.paste(album_img, (thumb_x, thumb_y), album_img)
    
    # ---- PROFILE PIC (top-right) ----
    profile_size = 70
    profile_x = CARD_W - profile_size - 45
    profile_y = 55
    
    # Default profile
    profile_img = Image.new("RGBA", (profile_size, profile_size), (100, 100, 100, 255))
    pp_draw = ImageDraw.Draw(profile_img)
    pp_draw.ellipse([15, 10, 55, 50], fill=(180, 180, 180, 255))
    pp_draw.ellipse([10, 45, 60, 75], fill=(180, 180, 180, 255))
    profile_img = _create_rounded_image(profile_img, profile_size // 2)
    card.paste(profile_img, (profile_x, profile_y), profile_img)
    
    # ---- TITLE ----
    title_x = thumb_x + thumb_size + 25
    title_y = 55
    draw.text((title_x, title_y), title, fill=WHITE, font=font_title)
    
    # Heart
    title_bbox = draw.textbbox((title_x, title_y), title, font=font_title)
    heart_x = title_bbox[2] + 12
    draw.text((heart_x, title_y + 2), "💚", fill=GREEN_PRIMARY, font=font_heart)
    
    # ---- CHANNEL & VIEWS ----
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
    _draw_waveform(draw, wave_x, wave_y, wave_w, wave_h, GREEN_WAVEFORM, progress)
    
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
    
    # ---- CONTROLS ----
    ctrl_y = 355
    center_x = CARD_W // 2
    
    # Shuffle
    shuffle_x = 90
    draw.text((shuffle_x - 12, ctrl_y - 14), "⟳", fill=GREEN_PRIMARY, font=font_icon)
    
    # Previous
    prev_x = center_x - 170
    draw.polygon([(prev_x, ctrl_y-20), (prev_x, ctrl_y+20), (prev_x+25, ctrl_y)], fill=BLACK)
    draw.rectangle([prev_x-8, ctrl_y-20, prev_x-3, ctrl_y+20], fill=BLACK)
    
    # Play button
    play_x = center_x
    play_y = ctrl_y + 5
    play_r = 48
    draw.ellipse([play_x-play_r, play_y-play_r, play_x+play_r, play_y+play_r], 
                fill=GREEN_DARK, outline=GREEN_LIGHT, width=2)
    draw.polygon([(play_x-15, play_y-25), (play_x-15, play_y+25), (play_x+20, play_y)], fill=WHITE)
    
    # Next
    next_x = center_x + 170
    draw.polygon([(next_x, ctrl_y-20), (next_x, ctrl_y+20), (next_x+25, ctrl_y)], fill=BLACK)
    draw.rectangle([next_x+25, ctrl_y-20, next_x+30, ctrl_y+20], fill=BLACK)
    
    # Repeat
    repeat_x = CARD_W - 90
    draw.text((repeat_x - 12, ctrl_y - 14), "⟳", fill=GREEN_PRIMARY, font=font_icon)
    
    # ---- BOTTOM BUTTONS ----
    btn_y = 445
    btn_w = 195
    btn_h = 52
    btn_r = 26
    btn_gap = 25
    total_btn_w = 4 * btn_w + 3 * btn_gap
    btn_start_x = (CARD_W - total_btn_w) // 2
    
    buttons = [("≡", "QUEUE"), ("▶", "AUTOPLAY"), ("⚡", "SPEED"), ("⚙", "SETTINGS")]
    btn_bg = (80, 160, 80, 120)
    
    for i, (icon, label) in enumerate(buttons):
        bx = btn_start_x + i * (btn_w + btn_gap)
        _draw_rounded_rect(draw, [bx, btn_y, bx+btn_w, btn_y+btn_h], btn_r, fill=btn_bg)
        draw.text((bx+20, btn_y+10), icon, fill=WHITE, font=font_icon)
        draw.text((bx+55, btn_y+13), label, fill=WHITE, font=font_button)
    
    # ---- VOLUME BAR ----
    vol_y = 545
    vol_x = 70
    vol_w = CARD_W - 140
    _draw_volume_bar(draw, vol_x, vol_y, vol_w, 0.55, GREEN_PRIMARY)
    
    vol_icon = _get_font(FONT_NORMAL, 24)
    draw.text((25, vol_y-12), "🔈", fill=WHITE, font=vol_icon)
    draw.text((CARD_W-50, vol_y-12), "🔊", fill=WHITE, font=vol_icon)
    
    # ============ COMPOSE FINAL ============
    bg = _add_card_shadow(bg, CARD_X, CARD_Y, CARD_W, CARD_H, CARD_RADIUS)
    bg.paste(card, (CARD_X, CARD_Y), card)
    
    # Vignette
    vignette = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for i in range(50):
        alpha = int(40 * (i/50))
        vd.rectangle([i, i, W-i-1, H-i-1], outline=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, vignette)
    
    # Save
    final = bg.convert("RGB")
    final.save(output, "PNG", quality=95)
    
    # Cleanup
    try:
        if os.path.exists(cache):
            os.remove(cache)
    except:
        pass
    
    _thumb_memory[videoid] = output
    return output


# Test
if __name__ == "__main__":
    import asyncio
    result = asyncio.run(get_thumb("test123", "OwnerAxiom"))
    print(f"Generated: {result}")
