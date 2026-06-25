import os
import re
import random
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Tuple
from functools import lru_cache

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ASSETS      = os.path.join(BASE_DIR, "..", "assets")
FONT_TITLE  = os.path.join(ASSETS, "f.ttf")
FONT_NORMAL = os.path.join(ASSETS, "cfont.ttf")

W, H = 1280, 720

# ============ COLORS (Green Theme) ============
GREEN_PRIMARY   = (76, 175, 80)
GREEN_LIGHT     = (129, 199, 132)
GREEN_DARK      = (56, 142, 60)
GREEN_ACCENT    = (102, 187, 106)
GREEN_WAVEFORM  = (60, 160, 65)
WHITE           = (255, 255, 255)
BLACK           = (30, 30, 30)
GRAY            = (180, 180, 180)
TRANSPARENT     = (0, 0, 0, 0)

# ============ CARD DIMENSIONS ============
CARD_X, CARD_Y = 140, 60
CARD_W, CARD_H = 1000, 600
CARD_RADIUS = 40

@lru_cache(maxsize=4)
def _get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def _draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def _create_rounded_image(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=radius, fill=255)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result

def _draw_waveform(draw, x, y, width, height, color, progress=0.35):
    num_bars = 80
    bar_w = max(2, (width - num_bars * 2) // num_bars)
    gap = 2
    random.seed(42)
    
    for i in range(num_bars):
        bx = x + i * (bar_w + gap)
        center_factor = 1.0 - abs(i - num_bars/2) / (num_bars/2)
        base_h = random.randint(8, height)
        bar_h = int(base_h * (0.3 + 0.7 * center_factor))
        by = y + (height - bar_h) // 2
        
        if i / num_bars <= progress:
            draw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=color)
        else:
            faded = tuple(max(0, c - 100) for c in color)
            draw.rectangle([bx, by, bx + bar_w, by + bar_h], fill=faded)

def _draw_progress_bar(draw, x, y, width, progress, color, handle_color):
    track_h = 6
    track_y = y - track_h // 2
    draw.rounded_rectangle([x, track_y, x + width, track_y + track_h], radius=3, fill=(200, 200, 200))
    pw = int(width * progress)
    if pw > 0:
        draw.rounded_rectangle([x, track_y, x + pw, track_y + track_h], radius=3, fill=color)
    hx = x + pw
    draw.ellipse([hx - 11, y - 11, hx + 11, y + 11], fill=handle_color, outline=WHITE, width=2)

def _draw_volume_bar(draw, x, y, width, volume, color):
    track_h = 6
    track_y = y - track_h // 2
    draw.rounded_rectangle([x, track_y, x + width, track_y + track_h], radius=3, fill=(200, 200, 200))
    vw = int(width * volume)
    if vw > 0:
        draw.rounded_rectangle([x, track_y, x + vw, track_y + track_h], radius=3, fill=color)
    hx = x + vw
    draw.ellipse([hx - 10, y - 10, hx + 10, y + 10], fill=WHITE, outline=GREEN_LIGHT, width=2)

def _draw_play_triangle(draw, cx, cy, size, color):
    h = size * 0.866
    pts = [(cx - size*0.4, cy - h*0.5), (cx - size*0.4, cy + h*0.5), (cx + size*0.5, cy)]
    draw.polygon(pts, fill=color)

def _draw_skip_triangle(draw, cx, cy, size, color, direction=1):
    h = size * 0.7
    if direction == 1:
        pts = [(cx - h*0.4, cy - h*0.5), (cx - h*0.4, cy + h*0.5), (cx + h*0.5, cy)]
    else:
        pts = [(cx + h*0.4, cy - h*0.5), (cx + h*0.4, cy + h*0.5), (cx - h*0.5, cy)]
    draw.polygon(pts, fill=color)
    bar_x = cx + h*0.55 if direction == 1 else cx - h*0.55 - 4
    draw.rectangle([bar_x, cy - h*0.5, bar_x + 4, cy + h*0.5], fill=color)

def _draw_shuffle_icon(draw, cx, cy, size, color):
    s = size * 0.4
    draw.line([cx-s, cy-s, cx+s, cy+s], fill=color, width=3)
    draw.line([cx-s, cy+s, cx+s, cy-s], fill=color, width=3)
    draw.polygon([(cx+s, cy+s), (cx+s-6, cy+s-2), (cx+s-2, cy+s-6)], fill=color)
    draw.polygon([(cx-s, cy-s), (cx-s+6, cy-s+2), (cx-s+2, cy-s+6)], fill=color)

def _draw_repeat_icon(draw, cx, cy, size, color):
    r = size * 0.35
    draw.arc([cx-r, cy-r, cx+r, cy+r], start=30, end=150, fill=color, width=3)
    draw.arc([cx-r, cy-r, cx+r, cy+r], start=210, end=330, fill=color, width=3)
    draw.polygon([(cx+r*0.5, cy-r*0.86), (cx+r*0.3, cy-r*0.7), (cx+r*0.7, cy-r*0.6)], fill=color)
    draw.polygon([(cx-r*0.5, cy+r*0.86), (cx-r*0.3, cy+r*0.7), (cx-r*0.7, cy+r*0.6)], fill=color)

def _create_greenery_background():
    img = Image.new("RGB", (W, H), (34, 139, 34))
    draw = ImageDraw.Draw(img)
    
    for y in range(H):
        ratio = y / H
        shade = int(40 + 30 * (1 - ratio))
        draw.line([(0, y), (W, y)], fill=(shade, 100 + int(60*ratio), shade))
    
    random.seed(42)
    for _ in range(2000):
        x = random.randint(0, W)
        y = random.randint(0, H)
        shade = random.randint(40, 120)
        draw.point((x, y), fill=(shade, shade+60, shade))
    
    return img.filter(ImageFilter.GaussianBlur(radius=8)).convert("RGBA")

def _add_light_beam(base_img):
    overlay = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx = W // 2
    
    for y in range(0, 350):
        alpha = int(50 * (1 - y/350) ** 2)
        beam_w = int(80 + y * 1.2)
        draw.line([(cx - beam_w, y), (cx + beam_w, y)], fill=(255, 255, 240, alpha))
    
    return Image.alpha_composite(base_img, overlay)

def _add_card_shadow(base_img, card_x, card_y, card_w, card_h, radius):
    shadow = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    
    for offset in range(15, 0, -1):
        alpha = int(60 * (1 - offset/15))
        draw.rounded_rectangle(
            [card_x + offset, card_y + offset + 5, card_x + card_w + offset, card_y + card_h + offset + 5],
            radius=radius, fill=(0, 0, 0, alpha)
        )
    
    return Image.alpha_composite(base_img, shadow)

def _truncate(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"

async def get_thumb(videoid: str, user_name: str = "AxiomUser") -> str:
    output = f"cache/{videoid}.png"
    cache = f"cache/thumb_{videoid}.jpg"
    os.makedirs("cache", exist_ok=True)

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
        title, duration, views, channel = "Unknown Song", "00:00", "0 views", "Unknown"
        thumb_url = ""

    # Download thumbnail
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(thumb_url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                async with aiofiles.open(cache, "wb") as f:
                    await f.write(await r.read())
        song_img = Image.open(cache).resize((110, 110)).convert("RGBA")
    except Exception:
        song_img = Image.new("RGBA", (110, 110), (76, 175, 80))
        aa_draw = ImageDraw.Draw(song_img)
        aa_draw.text((15, 40), "Music", fill=WHITE, font=_get_font(FONT_NORMAL, 14))

    song_img = _create_rounded_image(song_img, 18)

    # Parse duration
    try:
        parts = duration.split(":")
        total_seconds = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 225
    except:
        total_seconds = 225

    current_seconds = int(total_seconds * 0.35)
    current_time = f"{current_seconds // 60:02d}:{current_seconds % 60:02d}"
    progress = 0.35

    # Create background
    bg = _create_greenery_background()
    bg = _add_light_beam(bg)

    # Create card
    card = Image.new("RGBA", (CARD_W, CARD_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    
    # Card background
    card_bg = (220, 235, 220, 200)
    draw.rounded_rectangle([0, 0, CARD_W-1, CARD_H-1], radius=CARD_RADIUS, fill=card_bg)
    
    # Top light effect
    for y in range(0, 150):
        alpha = int(60 * (1 - y/150))
        draw.line([(10, y), (CARD_W-10, y)], fill=(255, 255, 255, alpha))
    
    # Border
    draw.rounded_rectangle([2, 2, CARD_W-3, CARD_H-3], radius=CARD_RADIUS-2, 
                          outline=(255, 255, 255, 80), width=2)

    # Album art (top-left)
    thumb_x, thumb_y = 45, 45
    card.paste(song_img, (thumb_x, thumb_y), song_img)

    # Profile pic placeholder (top-right)
    profile_size = 70
    profile_x = CARD_W - profile_size - 45
    profile_y = 55
    profile_img = Image.new("RGBA", (profile_size, profile_size), (100, 100, 100, 255))
    pp_draw = ImageDraw.Draw(profile_img)
    pp_draw.ellipse([15, 10, 55, 50], fill=(180, 180, 180))
    pp_draw.ellipse([10, 45, 60, 75], fill=(180, 180, 180))
    profile_img = _create_rounded_image(profile_img, profile_size // 2)
    card.paste(profile_img, (profile_x, profile_y), profile_img)

    # Title
    title_x = thumb_x + 110 + 25
    title_y = 55
    font_title = _get_font(FONT_TITLE, 44)
    card.text((title_x, title_y), title, fill=WHITE, font=font_title)
    
    # Green heart
    title_bbox = card.textbbox((title_x, title_y), title, font=font_title)
    heart_x = title_bbox[2] + 12
    card.text((heart_x, title_y + 2), "💚", fill=GREEN_PRIMARY, font=_get_font(FONT_NORMAL, 30))

    # Channel and views
    subtitle_y = title_y + 52
    font_subtitle = _get_font(FONT_NORMAL, 22)
    card.text((title_x, subtitle_y), channel, fill=(230, 230, 230), font=font_subtitle)
    channel_bbox = card.textbbox((title_x, subtitle_y), channel, font=font_subtitle)
    views_x = channel_bbox[2] + 30
    card.text((views_x, subtitle_y), views, fill=(200, 200, 200), font=font_subtitle)

    # Waveform
    wave_y = 195
    wave_x = 45
    wave_w = CARD_W - 90
    wave_h = 55
    _draw_waveform(card, wave_x, wave_y, wave_w, wave_h, GREEN_WAVEFORM, progress)

    # Progress bar
    prog_y = 280
    prog_x = 45
    prog_w = CARD_W - 90
    _draw_progress_bar(card, prog_x, prog_y, prog_w, progress, GREEN_PRIMARY, GREEN_LIGHT)
    
    font_time = _get_font(FONT_NORMAL, 20)
    card.text((prog_x, prog_y + 18), current_time, fill=WHITE, font=font_time)
    dur_bbox = card.textbbox((0, 0), duration, font=font_time)
    dur_w = dur_bbox[2] - dur_bbox[0]
    card.text((prog_x + prog_w - dur_w, prog_y + 18), duration, fill=WHITE, font=font_time)

    # Control buttons
    ctrl_y = 355
    center_x = CARD_W // 2
    
    shuffle_x = 90
    _draw_shuffle_icon(card, shuffle_x, ctrl_y, 50, GREEN_PRIMARY)
    
    prev_x = center_x - 170
    _draw_skip_triangle(card, prev_x, ctrl_y, 45, BLACK, direction=-1)
    
    play_x = center_x
    play_y = ctrl_y + 5
    play_r = 48
    card.ellipse([play_x-play_r-4, play_y-play_r-4, play_x+play_r+4, play_y+play_r+4], fill=(76, 175, 80, 80))
    card.ellipse([play_x-play_r, play_y-play_r, play_x+play_r, play_y+play_r], 
                fill=GREEN_DARK, outline=GREEN_LIGHT, width=2)
    card.ellipse([play_x-play_r+8, play_y-play_r+8, play_x+play_r-8, play_y-10], fill=(100, 200, 100, 60))
    _draw_play_triangle(card, play_x+3, play_y, 30, WHITE)
    
    next_x = center_x + 170
    _draw_skip_triangle(card, next_x, ctrl_y, 45, BLACK, direction=1)
    
    repeat_x = CARD_W - 90
    _draw_repeat_icon(card, repeat_x, ctrl_y, 50, GREEN_PRIMARY)

    # Bottom buttons (Queue, Autoplay, Speed, Settings)
    btn_y = 445
    btn_w = 195
    btn_h = 52
    btn_r = 26
    btn_gap = 25
    total_btn_w = 4 * btn_w + 3 * btn_gap
    btn_start_x = (CARD_W - total_btn_w) // 2
    
    buttons = [("≡", "QUEUE"), ("▶", "AUTOPLAY"), ("⚡", "SPEED"), ("⚙", "SETTINGS")]
    btn_bg = (80, 160, 80, 120)
    font_btn_label = _get_font(FONT_NORMAL, 17)
    font_btn_icon = _get_font(FONT_NORMAL, 26)
    
    for i, (icon, label) in enumerate(buttons):
        bx = btn_start_x + i * (btn_w + btn_gap)
        card.rounded_rectangle([bx, btn_y, bx+btn_w, btn_y+btn_h], radius=btn_r, fill=btn_bg)
        card.text((bx+20, btn_y+10), icon, fill=WHITE, font=font_btn_icon)
        card.text((bx+55, btn_y+13), label, fill=WHITE, font=font_btn_label)

    # Volume bar
    vol_y = 545
    vol_x = 70
    vol_w = CARD_W - 140
    _draw_volume_bar(card, vol_x, vol_y, vol_w, 0.55, GREEN_PRIMARY)
    
    vol_icon_font = _get_font(FONT_NORMAL, 24)
    card.text((25, vol_y-12), "🔈", fill=WHITE, font=vol_icon_font)
    card.text((CARD_W-50, vol_y-12), "🔊", fill=WHITE, font=vol_icon_font)

    # Compose final image
    bg = _add_card_shadow(bg, CARD_X, CARD_Y, CARD_W, CARD_H, CARD_RADIUS)
    bg.paste(card, (CARD_X, CARD_Y), card)
    
    # Vignette
    vignette = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for i in range(50):
        alpha = int(40 * (i/50))
        vdraw.rectangle([i, i, W-i-1, H-i-1], outline=(0, 0, 0, alpha))
    bg = Image.alpha_composite(bg, vignette)

    # Save
    final = bg.convert("RGB")
    final.save(output, "PNG", quality=95)
    
    try:
        if os.path.exists(cache):
            os.remove(cache)
    except:
        pass

    return output
