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

async def get_thumb(videoid: str, user_name: str = "AxiomUser", user_pfp_url: str = None) -> str:
    output = f"cache/{videoid}.png"
    os.makedirs("cache", exist_ok=True)
    
    # Load template
    try:
        template = Image.open(TEMPLATE_PATH).convert("RGBA")
    except:
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    
    draw = ImageDraw.Draw(template)
    
    # Fetch YouTube metadata
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
    
    # Download album art
    album_img = Image.new("RGBA", (110, 110), (76, 175, 80))
    if thumb_url:
        try:
            cache_file = f"cache/album_{videoid}.jpg"
            async with aiohttp.ClientSession() as sess:
                async with sess.get(thumb_url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    async with aiofiles.open(cache_file, "wb") as f:
                        await f.write(await r.read())
            album_img = Image.open(cache_file).resize((110, 110), Image.LANCZOS).convert("RGBA")
            album_img = _create_rounded_image(album_img, 18)
            if os.path.exists(cache_file):
                os.remove(cache_file)
        except Exception as e:
            print(f"[ERROR] Album art: {e}")
    
    # Download user profile picture (if provided)
    profile_size = 70
    profile_img = Image.new("RGBA", (profile_size, profile_size), (100, 100, 100, 255))
    pp_draw = ImageDraw.Draw(profile_img)
    pp_draw.ellipse([15, 10, 55, 50], fill=(180, 180, 180))
    pp_draw.ellipse([10, 45, 60, 75], fill=(180, 180, 180))
    
    if user_pfp_url:
        try:
            pfp_cache = f"cache/pfp_{videoid}.jpg"
            async with aiohttp.ClientSession() as sess:
                async with sess.get(user_pfp_url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    async with aiofiles.open(pfp_cache, "wb") as f:
                        await f.write(await r.read())
            profile_img = Image.open(pfp_cache).resize((profile_size, profile_size), Image.LANCZOS).convert("RGBA")
            profile_img = _create_rounded_image(profile_img, profile_size // 2)
            if os.path.exists(pfp_cache):
                os.remove(pfp_cache)
        except Exception as e:
            print(f"[ERROR] Profile pic: {e}")
    
    # Paste album art (top-left)
    template.paste(album_img, (115, 60), album_img)
    
    # Paste profile pic (top-right)
    template.paste(profile_img, (880, 70), profile_img)
    
    # Load fonts
    font_title = _get_font(FONT_TITLE, 42)
    font_subtitle = _get_font(FONT_NORMAL, 22)
    font_time = _get_font(FONT_NORMAL, 20)
    
    # Truncate title if too long
    max_title_width = 680
    title_text = title
    while draw.textlength(title_text, font=font_title) > max_title_width and len(title_text) > 3:
        title_text = title_text[:-1]
    if len(title_text) < len(title):
        title_text = title_text[:-3] + "…"
    
    # Draw title (white with subtle shadow)
    title_x = 240
    title_y = 75
    draw.text((title_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 100), font=font_title)
    draw.text((title_x, title_y), title_text, fill=(255, 255, 255), font=font_title)
    
    # Draw channel and views
    subtitle_y = 120
    draw.text((title_x, subtitle_y), channel, fill=(230, 230, 230), font=font_subtitle)
    channel_width = draw.textlength(channel, font=font_subtitle)
    views_x = title_x + channel_width + 25
    draw.text((views_x, subtitle_y), views, fill=(200, 200, 200), font=font_subtitle)
    
    # Draw time (current time at 1:07 or calculated)
    try:
        parts = duration.split(":")
        total_seconds = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 225
    except:
        total_seconds = 225
    
    current_seconds = int(total_seconds * 0.30)  # ~30% progress
    current_min = current_seconds // 60
    current_sec = current_seconds % 60
    current_time = f"{current_min}:{current_sec:02d}"
    
    # Draw current time (left side)
    draw.text((115, 330), current_time, fill=(255, 255, 255), font=font_time)
    
    # Draw total duration (right side)
    dur_width = draw.textlength(duration, font=font_time)
    draw.text((820 - dur_width, 330), duration, fill=(255, 255, 255), font=font_time)
    
    # Save
    final = template.convert("RGB")
    final.save(output, "PNG", quality=95)
    
    return output
