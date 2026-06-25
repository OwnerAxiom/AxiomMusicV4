import os
import re
import aiohttp
import aiofiles
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE_DIR, "..", "assets")
FONT_TITLE = os.path.join(ASSETS, "f.ttf")
FONT_NORMAL = os.path.join(ASSETS, "cfont.ttf")
TEMPLATE_PATH = os.path.join(ASSETS, "thumb1.png")

@lru_cache(maxsize=4)
def _get_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def _create_rounded_image(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], radius=radius, fill=255)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result

async def get_thumb(videoid: str, user_name: str = "AxiomUser") -> str:
    output = f"cache/{videoid}.png"
    os.makedirs("cache", exist_ok=True)
    
    try:
        template = Image.open(TEMPLATE_PATH).convert("RGBA")
    except:
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    
    draw = ImageDraw.Draw(template)
    
    # Fetch metadata
    url = f"https://www.youtube.com/watch?v={videoid}"
    title = "Unknown Song"
    duration = "00:00"
    views = "0 views"
    channel = "Unknown"
    thumb_url = ""
    
    try:
        from py_yt import VideosSearch
        data = (await VideosSearch(url, limit=1).next())["result"][0]
        title = re.sub(r"[\x00-\x1f\x7f]", "", data.get("title", "Unknown")).strip()
        duration = data.get("duration", "00:00") or "00:00"
        thumb_url = data.get("thumbnails", [{}])[-1].get("url", "").split("?")[0]
        v_raw = str(data.get("viewCount", {}).get("short", "N/A"))
        vc = re.sub(r'\s*views?\s*', '', v_raw, flags=re.IGNORECASE).strip()
        views = f"{vc} views"
        channel = data.get("channel", {}).get("name", "Unknown")
    except Exception as e:
        print(f"[ERROR] Metadata: {e}")
    
    # Download album art - size 200x200
    album_size = 310
    album_img = Image.new("RGBA", (album_size, album_size), (76, 175, 80))
    if thumb_url:
        try:
            cache_file = f"cache/album_{videoid}.jpg"
            async with aiohttp.ClientSession() as sess:
                async with sess.get(thumb_url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    async with aiofiles.open(cache_file, "wb") as f:
                        await f.write(await r.read())
            album_img = Image.open(cache_file).resize((album_size, album_size), Image.LANCZOS).convert("RGBA")
            album_img = _create_rounded_image(album_img, 35)
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except Exception as e:
            print(f"[ERROR] Album art: {e}")
    
    # Album art INSIDE glowing box
    # Glowing box is at approximately x=75-320, y=180-400
    template.paste(album_img, (131, 134), album_img)
    
    # Fonts
    font_title = _get_font(FONT_TITLE, 60)
    font_subtitle = _get_font(FONT_NORMAL, 35)
    font_time = _get_font(FONT_NORMAL, 30)
    
    # Truncate title
    max_title_width = 830
    title_text = title
    while draw.textlength(title_text, font=font_title) > max_title_width and len(title_text) > 3:
        title_text = title_text[:-1]
    if len(title_text) < len(title):
        title_text = title_text[:-3] + "…"
    
    # Title - right of album art, aligned with top of album art
    title_x = 500
    title_y = 150
    
    # Green glow layers (3 layers for soft glow)
    for i in range(3, 0, -1):
        draw.text((title_x + i, title_y + i), title_text, 
                  fill=(50, 180, 50, 80), font=font_title)
    
    # Main title - pure white
    draw.text((title_x, title_y), title_text, fill=(220, 255, 100), font=font_title)
    
    # Channel - light gray-green (different from white)
    subtitle_y = 235
    draw.text((title_x, subtitle_y), channel, fill=(160, 200, 160), font=font_subtitle)
    
    # Pipe + Views
    channel_width = draw.textlength(channel, font=font_subtitle)
    draw.text((title_x + channel_width + 12, subtitle_y), "|", fill=(140, 180, 140), font=font_subtitle)
    draw.text((title_x + channel_width + 32, subtitle_y), views, fill=(210, 220, 210), font=font_subtitle)
    
    # Calculate current time
    try:
        parts = duration.split(":")
        total_seconds = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 225
    except:
        total_seconds = 225
    
    current_seconds = int(total_seconds * 0.30)
    current_min = current_seconds // 60
    current_sec = current_seconds % 60
    current_time = f"{current_min}:{current_sec:02d}"
    
    # Progress bar is at approximately y=375
    # Time text should be JUST ABOVE progress bar
    time_y = 345
    
    # Current time - LEFT side
    draw.text((100, time_y), current_time, fill=(255, 255, 255), font=font_time)
    
    # Duration - RIGHT side
    dur_width = draw.textlength(duration, font=font_time)
    draw.text((1250 - dur_width, time_y), duration, fill=(255, 255, 255), font=font_time)
    
    # Save
    final = template.convert("RGB")
    final.save(output, "PNG", quality=95)
    
    return output
    
