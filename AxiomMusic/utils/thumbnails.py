from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random
import os

# ============ CONFIGURATION ============
BASE_WIDTH = 1280
BASE_HEIGHT = 720
CARD_X = 140
CARD_Y = 60
CARD_WIDTH = 1000
CARD_HEIGHT = 600
CARD_RADIUS = 40

# Font paths (tumhare repo ke hisab se adjust karo)
FONT_TITLE = "assets/f.ttf"      # Title ke liye
FONT_NORMAL = "assets/cfont.ttf"  # Baaki sab ke liye

# Colors
GREEN_PRIMARY = (76, 175, 80)
GREEN_LIGHT = (129, 199, 132)
GREEN_DARK = (56, 142, 60)
GREEN_ACCENT = (102, 187, 106)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GREEN_TRANSPARENT = (76, 175, 80, 180)

def create_rounded_rectangle(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle"""
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def draw_waveform(draw, x, y, width, height, color, progress=0.4):
    """Draw audio waveform"""
    num_bars = 80
    bar_width = width // num_bars
    gap = 2
    
    random.seed(42)  # Fixed seed for consistent waveform
    
    for i in range(num_bars):
        bar_x = x + i * (bar_width + gap)
        # Generate waveform height
        base_height = random.randint(8, height)
        # Make it look like a real waveform (higher in middle, lower at ends)
        center_factor = 1 - abs(i - num_bars/2) / (num_bars/2)
        bar_h = int(base_height * (0.3 + 0.7 * center_factor))
        bar_y = y + (height - bar_h) // 2
        
        if i / num_bars <= progress:
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_h], fill=color)
        else:
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_h], 
                         fill=(*color[:3], 80) if len(color) == 4 else (color[0]//3, color[1]//3, color[2]//3))

def draw_progress_bar(draw, x, y, width, height, progress, color, handle_color):
    """Draw progress bar with handle"""
    # Background track
    track_y = y + height // 2 - 3
    draw.rectangle([x, track_y, x + width, track_y + 6], fill=(200, 200, 200, 100))
    
    # Progress fill
    progress_width = int(width * progress)
    draw.rectangle([x, track_y, x + progress_width, track_y + 6], fill=color)
    
    # Handle
    handle_x = x + progress_width
    handle_y = y + height // 2
    draw.ellipse([handle_x - 10, handle_y - 10, handle_x + 10, handle_y + 10], fill=handle_color)

def draw_volume_bar(draw, x, y, width, height, volume=0.6, color=None):
    """Draw volume bar"""
    if color is None:
        color = GREEN_PRIMARY
    
    # Background track
    track_y = y + height // 2 - 3
    draw.rectangle([x, track_y, x + width, track_y + 6], fill=(200, 200, 200, 100))
    
    # Volume fill
    volume_width = int(width * volume)
    draw.rectangle([x, track_y, x + volume_width, track_y + 6], fill=color)
    
    # Handle
    handle_x = x + volume_width
    handle_y = y + height // 2
    draw.ellipse([handle_x - 10, handle_y - 10, handle_x + 10, handle_y + 10], fill=WHITE)

def draw_pill_button(draw, x, y, width, height, radius, icon_text, label, font_icon, font_label, bg_color, text_color):
    """Draw a pill-shaped button with icon and text"""
    # Button background
    draw.rounded_rectangle([x, y, x + width, y + height], radius=radius, fill=bg_color)
    
    # Icon
    icon_x = x + 20
    icon_y = y + height // 2
    draw.text((icon_x, icon_y - 12), icon_text, fill=text_color, font=font_icon)
    
    # Label
    label_x = icon_x + 30
    draw.text((label_x, icon_y - 10), label, fill=text_color, font=font_label)

def generate_thumbnail(title, channel_name, views, duration_str, current_time="01:24", 
                       album_art_path=None, profile_pic_path=None, output_path="thumbnail.png"):
    """Generate the music player thumbnail"""
    
    # Create base image with green nature background
    base = Image.new('RGBA', (BASE_WIDTH, BASE_HEIGHT), (34, 139, 34, 255))
    
    # Add blurred green background effect
    bg_draw = ImageDraw.Draw(base)
    for i in range(0, BASE_HEIGHT, 4):
        shade = int(40 + 30 * math.sin(i * 0.02))
        bg_draw.line([(0, i), (BASE_WIDTH, i)], fill=(shade, 100 + shade, shade, 255))
    
    # ============ CREATE CARD ============
    card = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card)
    
    # Card background with glassmorphism effect
    card_bg = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (200, 230, 200, 220))
    
    # Add light effect at top of card
    light_overlay = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    light_draw = ImageDraw.Draw(light_overlay)
    
    # Gradient light from top
    for y in range(0, 200):
        alpha = int(80 * (1 - y/200))
        light_draw.line([(0, y), (CARD_WIDTH, y)], fill=(255, 255, 255, alpha))
    
    card = Image.alpha_composite(card_bg, light_overlay)
    card_draw = ImageDraw.Draw(card)
    
    # Card border/glow
    create_rounded_rectangle(card_draw, (2, 2, CARD_WIDTH-2, CARD_HEIGHT-2), 
                            CARD_RADIUS, outline=(255, 255, 255, 100), width=2)
    
    # ============ LOAD FONTS ============
    try:
        font_title = ImageFont.truetype(FONT_TITLE, 42)
        font_subtitle = ImageFont.truetype(FONT_NORMAL, 22)
        font_time = ImageFont.truetype(FONT_NORMAL, 20)
        font_button = ImageFont.truetype(FONT_NORMAL, 18)
        font_icon = ImageFont.truetype(FONT_NORMAL, 24)
        font_small_icon = ImageFont.truetype(FONT_NORMAL, 28)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_time = ImageFont.load_default()
        font_button = ImageFont.load_default()
        font_icon = ImageFont.load_default()
        font_small_icon = ImageFont.load_default()
    
    # ============ TOP SECTION ============
    # Album art thumbnail (top-left)
    thumb_size = 100
    thumb_x, thumb_y = 40, 40
    
    if album_art_path and os.path.exists(album_art_path):
        album_art = Image.open(album_art_path).resize((thumb_size, thumb_size)).convert('RGBA')
    else:
        # Default green nature thumbnail
        album_art = Image.new('RGBA', (thumb_size, thumb_size), (76, 175, 80, 255))
        aa_draw = ImageDraw.Draw(album_art)
        aa_draw.text((10, 35), "Axiom\nMusic", fill=WHITE, font=font_button)
    
    # Round the album art corners
    album_mask = Image.new('L', (thumb_size, thumb_size), 0)
    mask_draw = ImageDraw.Draw(album_mask)
    mask_draw.rounded_rectangle([0, 0, thumb_size-1, thumb_size-1], radius=15, fill=255)
    album_art.putalpha(album_mask)
    
    card.paste(album_art, (thumb_x, thumb_y), album_art)
    
    # Profile picture (top-right) - replaces the 3 dots
    profile_size = 80
    profile_x = CARD_WIDTH - profile_size - 40
    profile_y = 50
    
    if profile_pic_path and os.path.exists(profile_pic_path):
        profile_pic = Image.open(profile_pic_path).resize((profile_size, profile_size)).convert('RGBA')
    else:
        # Default profile placeholder
        profile_pic = Image.new('RGBA', (profile_size, profile_size), (100, 100, 100, 255))
        pp_draw = ImageDraw.Draw(profile_pic)
        pp_draw.ellipse([20, 15, 60, 55], fill=(200, 200, 200, 255))
        pp_draw.ellipse([25, 50, 55, 75], fill=(200, 200, 200, 255))
    
    # Round profile pic
    profile_mask = Image.new('L', (profile_size, profile_size), 0)
    mask_draw = ImageDraw.Draw(profile_mask)
    mask_draw.ellipse([0, 0, profile_size-1, profile_size-1], fill=255)
    profile_pic.putalpha(profile_mask)
    
    card.paste(profile_pic, (profile_x, profile_y), profile_pic)
    
    # Title
    title_text = title
    title_bbox = card_draw.textbbox((0, 0), title_text, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = thumb_x + thumb_size + 30
    title_y = 55
    
    card_draw.text((title_x, title_y), title_text, fill=WHITE, font=font_title)
    
    # Green heart after title
    heart_x = title_x + title_width + 15
    card_draw.text((heart_x, title_y + 5), "💚", fill=GREEN_PRIMARY, font=font_small_icon)
    
    # Channel name and views
    subtitle_text = f"{channel_name}    {views}"
    card_draw.text((title_x, title_y + 50), subtitle_text, fill=(220, 220, 220, 255), font=font_subtitle)
    
    # ============ WAVEFORM ============
    waveform_y = 180
    waveform_x = 40
    waveform_width = CARD_WIDTH - 80
    waveform_height = 60
    
    # Create waveform on separate layer for transparency
    waveform_layer = Image.new('RGBA', (CARD_WIDTH, CARD_HEIGHT), (0, 0, 0, 0))
    waveform_draw = ImageDraw.Draw(waveform_layer)
    draw_waveform(waveform_draw, waveform_x, waveform_y, waveform_width, waveform_height, 
                  GREEN_PRIMARY, progress=0.35)
    card = Image.alpha_composite(card, waveform_layer)
    card_draw = ImageDraw.Draw(card)
    
    # ============ PROGRESS BAR ============
    progress_y = 270
    progress_x = 40
    progress_width = CARD_WIDTH - 80
    draw_progress_bar(card_draw, progress_x, progress_y, progress_width, 20, 0.35, GREEN_PRIMARY, GREEN_LIGHT)
    
    # Time labels
    card_draw.text((progress_x, progress_y + 25), current_time, fill=WHITE, font=font_time)
    
    duration_bbox = card_draw.textbbox((0, 0), duration_str, font=font_time)
    duration_width = duration_bbox[2] - duration_bbox[0]
    card_draw.text((progress_x + progress_width - duration_width, progress_y + 25), 
                   duration_str, fill=WHITE, font=font_time)
    
    # ============ CONTROL BUTTONS ============
    controls_y = 340
    center_x = CARD_WIDTH // 2
    
    # Shuffle button (far left) - green outline
    shuffle_x = 80
    card_draw.text((shuffle_x - 15, controls_y - 15), "⟳", fill=GREEN_PRIMARY, font=font_small_icon)
    
    # Previous button (black solid)
    prev_x = center_x - 180
    card_draw.polygon([(prev_x, controls_y - 20), (prev_x, controls_y + 20), 
                       (prev_x + 25, controls_y)], fill=BLACK)
    card_draw.rectangle([prev_x - 8, controls_y - 20, prev_x - 3, controls_y + 20], fill=BLACK)
    
    # Play button (large green circle)
    play_x = center_x
    play_y = controls_y + 10
    play_radius = 50
    card_draw.ellipse([play_x - play_radius, play_y - play_radius, 
                       play_x + play_radius, play_y + play_radius], fill=GREEN_DARK)
    # Play triangle
    card_draw.polygon([(play_x - 15, play_y - 25), (play_x - 15, play_y + 25), 
                       (play_x + 20, play_y)], fill=WHITE)
    
    # Next button (black solid)
    next_x = center_x + 155
    card_draw.polygon([(next_x, controls_y - 20), (next_x, controls_y + 20), 
                       (next_x + 25, controls_y)], fill=BLACK)
    card_draw.rectangle([next_x + 25, controls_y - 20, next_x + 30, controls_y + 20], fill=BLACK)
    
    # Repeat button (far right) - green outline
    repeat_x = CARD_WIDTH - 100
    card_draw.text((repeat_x - 15, controls_y - 15), "⟳", fill=GREEN_PRIMARY, font=font_small_icon)
    
    # ============ BOTTOM BUTTONS (Queue, Autoplay, Speed, Settings) ============
    buttons_y = 430
    button_width = 200
    button_height = 50
    button_radius = 25
    button_gap = 30
    total_buttons_width = 4 * button_width + 3 * button_gap
    buttons_start_x = (CARD_WIDTH - total_buttons_width) // 2
    
    buttons = [
        ("≡", "QUEUE"),
        ("▶", "AUTOPLAY"),
        ("⚡", "SPEED"),
        ("⚙", "SETTINGS")
    ]
    
    for i, (icon, label) in enumerate(buttons):
        btn_x = buttons_start_x + i * (button_width + button_gap)
        btn_bg = (76, 175, 80, 100)  # Green translucent
        card_draw.rounded_rectangle([btn_x, buttons_y, btn_x + button_width, buttons_y + button_height],
                                    radius=button_radius, fill=btn_bg)
        
        # Icon
        card_draw.text((btn_x + 20, buttons_y + 10), icon, fill=WHITE, font=font_icon)
        
        # Label
        card_draw.text((btn_x + 55, buttons_y + 13), label, fill=WHITE, font=font_button)
    
    # ============ VOLUME BAR ============
    volume_y = 520
    volume_x = 60
    volume_width = CARD_WIDTH - 140
    draw_volume_bar(card_draw, volume_x, volume_y, volume_width, 20, 0.5, GREEN_PRIMARY)
    
    # Volume icons
    card_draw.text((20, volume_y - 5), "🔈", fill=WHITE, font=font_icon)
    card_draw.text((CARD_WIDTH - 45, volume_y - 5), "🔊", fill=WHITE, font=font_icon)
    
    # ============ COMPOSE FINAL IMAGE ============
    # Paste card onto base
    base.paste(card, (CARD_X, CARD_Y), card)
    
    # Add 3D shadow effect
    shadow = Image.new('RGBA', (BASE_WIDTH, BASE_HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle([CARD_X + 10, CARD_Y + 15, 
                                    CARD_X + CARD_WIDTH + 10, CARD_Y + CARD_HEIGHT + 15],
                                   radius=CARD_RADIUS, fill=(0, 0, 0, 80))
    base = Image.alpha_composite(shadow, base)
    
    # Add light beam effect at top
    light_beam = Image.new('RGBA', (BASE_WIDTH, BASE_HEIGHT), (0, 0, 0, 0))
    light_draw = ImageDraw.Draw(light_beam)
    
    # Create light beam from top center
    for y in range(0, 300):
        alpha = int(40 * (1 - y/300))
        beam_width = int(100 + y * 0.5)
        light_draw.line([(BASE_WIDTH//2 - beam_width, y), (BASE_WIDTH//2 + beam_width, y)], 
                       fill=(255, 255, 255, alpha))
    
    base = Image.alpha_composite(base, light_beam)
    
    # Convert to RGB and save
    final = base.convert('RGB')
    final.save(output_path, quality=95)
    
    print(f"Thumbnail generated: {output_path}")
    return output_path

# ============ USAGE EXAMPLE ============
if __name__ == "__main__":
    generate_thumbnail(
        title="Axiom X Music",
        channel_name="OwnerAxiom",
        views="1.2M views",
        duration_str="03:45",
        current_time="01:24",
        album_art_path="assets/album_art.png",  # Song ka thumbnail
        profile_pic_path="assets/profile.png",   # User ka profile pic
        output_path="output_thumbnail.png"
    )
