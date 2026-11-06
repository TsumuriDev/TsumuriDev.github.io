import math
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def make_linear_gradient(width, height, color_start, color_end, angle_deg=125):
    # Create linear gradient image
    img = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(img)
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    
    # Calculate projection length
    diag = math.sqrt(width**2 + height**2)
    
    # Draw line by line for smooth gradient
    for y in range(height):
        for x in range(0, width, 2):
            proj = (x - width/2) * cos_a + (y - height/2) * sin_a
            t = (proj / (diag * 0.7)) + 0.5
            t = max(0.0, min(1.0, t))
            r = int(color_start[0] * (1 - t) + color_end[0] * t)
            g = int(color_start[1] * (1 - t) + color_end[1] * t)
            b = int(color_start[2] * (1 - t) + color_end[2] * t)
            img.putpixel((x, y), (r, g, b, 255))
            if x + 1 < width:
                img.putpixel((x + 1, y), (r, g, b, 255))
    return img

def create_radial_glow(width, height, cx, cy, radius, color, max_alpha=200):
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    # We can create a mask with multiple blurred concentric circles
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    steps = 40
    for i in range(steps, 0, -1):
        r = radius * (i / steps)
        t = i / steps
        alpha = int(max_alpha * ((1 - t) ** 1.8))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=alpha)
        
    mask = mask.filter(ImageFilter.GaussianBlur(radius * 0.15))
    glow_color = Image.new("RGBA", (width, height), (*color, 255))
    glow.paste(glow_color, (0, 0), mask)
    return glow

def apply_glow_to_logo(logo_img, glow_color=(234, 16, 222), blur_radius=30, alpha_factor=0.8):
    # Extract alpha mask of the logo
    r, g, b, a = logo_img.split()
    
    # Layer 1: Tight intense glow
    mask1 = a.filter(ImageFilter.GaussianBlur(12))
    glow1 = Image.new("RGBA", logo_img.size, (*glow_color, int(255 * alpha_factor * 0.9)))
    
    # Layer 2: Wide soft glow
    mask2 = a.filter(ImageFilter.GaussianBlur(blur_radius))
    glow2 = Image.new("RGBA", logo_img.size, (*glow_color, int(255 * alpha_factor * 0.6)))
    
    # Combined glow canvas
    canvas = Image.new("RGBA", logo_img.size, (0, 0, 0, 0))
    canvas.paste(glow2, (0, 0), mask2)
    canvas.paste(glow1, (0, 0), mask1)
    canvas.paste(logo_img, (0, 0), logo_img)
    return canvas

def generate_banner():
    # Width x Height matching the user's card screenshot
    W, H = 1600, 750
    base = Image.new("RGBA", (W, H), hex_to_rgb("#0c0a0e") + (255,))
    
    # Outer ambient glow in the whole canvas
    ambient = create_radial_glow(W, H, W//2, H//2, 500, (234, 16, 222), max_alpha=55)
    base = Image.alpha_composite(base, ambient)
    
    # Card dimensions
    card_w = 1420
    card_h = 580
    card_x = (W - card_w) // 2
    card_y = (H - card_h) // 2
    corner_r = 32
    
    # 1. Card drop shadow
    shadow_mask = Image.new("L", (W, H), 0)
    shadow_draw = ImageDraw.Draw(shadow_mask)
    shadow_draw.rounded_rectangle([card_x, card_y + 12, card_x + card_w, card_y + card_h + 12], radius=corner_r, fill=220)
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(25))
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    base.paste(shadow_layer, (0, 0), shadow_mask)
    
    # 2. Card background gradient
    card_bg = make_linear_gradient(card_w, card_h, hex_to_rgb("#27132b"), hex_to_rgb("#16111f"), angle_deg=125)
    
    # 3. Card inner radial glow behind logo
    card_glow = create_radial_glow(card_w, card_h, card_w//2, card_h//2, 380, (234, 16, 222), max_alpha=85)
    card_lime = create_radial_glow(card_w, card_h, card_w//2, card_h//2 + 80, 260, (68, 235, 126), max_alpha=35)
    card_bg = Image.alpha_composite(card_bg, card_glow)
    card_bg = Image.alpha_composite(card_bg, card_lime)
    
    # 4. Card rounded mask
    card_mask = Image.new("L", (card_w, card_h), 0)
    card_mask_draw = ImageDraw.Draw(card_mask)
    card_mask_draw.rounded_rectangle([0, 0, card_w, card_h], radius=corner_r, fill=255)
    
    # Paste card onto base
    base.paste(card_bg, (card_x, card_y), card_mask)
    
    # 5. Card Border with subtle glow
    border_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border_img)
    border_draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=corner_r, outline=hex_to_rgb("#542450") + (255,), width=2)
    base = Image.alpha_composite(base, border_img)
    
    # 6. Load and scale Logo
    logo = Image.open("assets/zoemc-logo.png").convert("RGBA")
    # Scale logo nicely inside the card (e.g. width ~1100 px)
    target_logo_w = 1120
    target_logo_h = int(logo.height * (target_logo_w / logo.width))
    logo_resized = logo.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)
    
    # Apply glowing effect
    logo_with_glow = apply_glow_to_logo(logo_resized, glow_color=(234, 16, 222), blur_radius=28, alpha_factor=0.85)
    
    # Center logo on card
    logo_x = (W - target_logo_w) // 2
    logo_y = (H - target_logo_h) // 2
    
    base.paste(logo_with_glow, (logo_x, logo_y), logo_with_glow)
    
    # Save output banner
    out_path = "zoemc-server-banner.png"
    base.save(out_path, "PNG")
    print(f"Generated banner: {out_path} ({W}x{H})")

def generate_square_logo():
    # 1024x1024 for Server Avatar, Discord Icon, Profile
    S = 1024
    base = Image.new("RGBA", (S, S), hex_to_rgb("#0c0a0e") + (255,))
    
    # Rounded card box inside square
    box_pad = 60
    box_w = S - box_pad * 2
    box_h = S - box_pad * 2
    corner_r = 48
    
    # Ambient radial aura
    ambient = create_radial_glow(S, S, S//2, S//2, 450, (234, 16, 222), max_alpha=120)
    ambient_lime = create_radial_glow(S, S, S//2, S//2 + 100, 300, (68, 235, 126), max_alpha=45)
    
    # Card background
    card_bg = make_linear_gradient(box_w, box_h, hex_to_rgb("#27132b"), hex_to_rgb("#140f1c"), angle_deg=130)
    card_glow = create_radial_glow(box_w, box_h, box_w//2, box_h//2, 340, (234, 16, 222), max_alpha=110)
    card_bg = Image.alpha_composite(card_bg, card_glow)
    
    card_mask = Image.new("L", (box_w, box_h), 0)
    ImageDraw.Draw(card_mask).rounded_rectangle([0, 0, box_w, box_h], radius=corner_r, fill=255)
    
    base.paste(card_bg, (box_pad, box_pad), card_mask)
    base = Image.alpha_composite(base, ambient)
    base = Image.alpha_composite(base, ambient_lime)
    
    # Border
    border_img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(border_img).rounded_rectangle([box_pad, box_pad, box_pad + box_w, box_pad + box_h], radius=corner_r, outline=hex_to_rgb("#662961") + (255,), width=3)
    base = Image.alpha_composite(base, border_img)
    
    # Logo
    logo = Image.open("assets/zoemc-logo.png").convert("RGBA")
    target_logo_w = 820
    target_logo_h = int(logo.height * (target_logo_w / logo.width))
    logo_resized = logo.resize((target_logo_w, target_logo_h), Image.Resampling.LANCZOS)
    
    logo_with_glow = apply_glow_to_logo(logo_resized, glow_color=(234, 16, 222), blur_radius=32, alpha_factor=0.9)
    
    logo_x = (S - target_logo_w) // 2
    logo_y = (S - target_logo_h) // 2
    base.paste(logo_with_glow, (logo_x, logo_y), logo_with_glow)
    
    out_path = "zoemc-server-logo-square.png"
    base.save(out_path, "PNG")
    print(f"Generated square logo: {out_path} ({S}x{S})")
    
    # Also generate Minecraft 64x64 server-icon.png
    icon64 = base.resize((64, 64), Image.Resampling.LANCZOS)
    icon64.save("server-icon.png", "PNG")
    print("Generated Minecraft standard server-icon.png (64x64)")

if __name__ == "__main__":
    generate_banner()
    generate_square_logo()
