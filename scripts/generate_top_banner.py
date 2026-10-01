import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_banner():
    print("Generating Clean Static Logo & Pure 2nd Font Banner...")

    # 1. Canvas parameters (2x supersampling)
    SCALE = 2
    W_ORIG, H_ORIG = 1200, 360
    W, H = W_ORIG * SCALE, H_ORIG * SCALE

    # Fonts
    font_title = ImageFont.truetype('assets/fonts/glitten/Glitten-Regular.otf', int(76 * SCALE))
    font_tagline = ImageFont.truetype('assets/fonts/GreatVibes.ttf', int(48 * SCALE))
    font_mono = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', int(15 * SCALE))

    # Base coordinates
    start_x = int(395 * SCALE)
    base_y = int(76 * SCALE)
    tag_y = base_y + int(108 * SCALE)
    pill_y = tag_y + int(74 * SCALE)
    pill_h = int(28 * SCALE)

    # 2. Static Logo on Left (NO animation!)
    logo = Image.open('assets/logo.png').convert('RGBA')
    logo_display_w = int(300 * SCALE)
    logo_display_h = int(300 * SCALE)
    scaled_logo = logo.resize((logo_display_w, logo_display_h), Image.Resampling.LANCZOS)
    logo_pos_x = int(45 * SCALE)
    logo_pos_y = int(30 * SCALE)

    # 3. Static Title 'AscendCareer' in stylish dual-tone luxury serif
    asc_w = font_title.getlength('Ascend')

    # Soft dark drop shadow for luxury depth and clean separation
    title_shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ts_draw = ImageDraw.Draw(title_shadow)
    ts_draw.text((start_x + int(2 * SCALE), base_y + int(3 * SCALE)), 'Ascend', font=font_title, fill=(0, 0, 0, 130))
    ts_draw.text((start_x + asc_w + int(2 * SCALE), base_y + int(3 * SCALE)), 'Career', font=font_title, fill=(0, 0, 0, 130))
    title_shadow = title_shadow.filter(ImageFilter.GaussianBlur(int(2.5 * SCALE)))

    # Soft warm ambient bloom behind Career
    title_glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tgldraw = ImageDraw.Draw(title_glow)
    tgldraw.text((start_x + asc_w, base_y), 'Career', font=font_title, fill=(245, 158, 11, 75))
    title_glow = title_glow.filter(ImageFilter.GaussianBlur(int(6 * SCALE)))

    # Pure crisp dual-tone title
    title_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(title_layer)
    # Ascend in pearl white
    tdraw.text((start_x, base_y), 'Ascend', font=font_title, fill=(255, 255, 255, 255))
    # Career in luminous champagne gold
    tdraw.text((start_x + asc_w, base_y), 'Career', font=font_title, fill=(250, 195, 60, 255))

    # 4. Tagline: 'Better Preparation. Stronger Presentation.' in cursive font with combination of light pink and sky blue
    tag1 = "Better Preparation."
    tag2 = " Stronger Presentation."
    w1 = font_tagline.getlength(tag1)
    w2 = font_tagline.getlength(tag2)

    # Soft glowing bloom (double-layer: broad ambient + rich inner neon)
    glow_broad = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gbdraw = ImageDraw.Draw(glow_broad)
    gbdraw.text((start_x, tag_y), tag1, font=font_tagline, fill=(244, 114, 182, 160))
    gbdraw.text((start_x + w1, tag_y), tag2, font=font_tagline, fill=(56, 189, 248, 160))
    glow_broad = glow_broad.filter(ImageFilter.GaussianBlur(int(10 * SCALE)))

    glow_inner = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gidraw = ImageDraw.Draw(glow_inner)
    gidraw.text((start_x, tag_y), tag1, font=font_tagline, fill=(251, 113, 133, 200))
    gidraw.text((start_x + w1, tag_y), tag2, font=font_tagline, fill=(14, 165, 233, 200))
    glow_inner = glow_inner.filter(ImageFilter.GaussianBlur(int(4 * SCALE)))

    # Crisp cursive text layer with luminous pastel tones & specular top pass
    tag_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tldraw = ImageDraw.Draw(tag_layer)
    # Better Preparation. in light pink
    tldraw.text((start_x, tag_y), tag1, font=font_tagline, fill=(255, 215, 238, 255))
    tldraw.text((start_x, tag_y - int(0.5 * SCALE)), tag1, font=font_tagline, fill=(255, 245, 252, 160))
    # Stronger Presentation. in sky blue
    tldraw.text((start_x + w1, tag_y), tag2, font=font_tagline, fill=(160, 235, 255, 255))
    tldraw.text((start_x + w1, tag_y - int(0.5 * SCALE)), tag2, font=font_tagline, fill=(240, 252, 255, 160))

    # Glitter twinkle positions across tagline with matching pink & sky-blue sparkles
    sparkle_bases = [
        (start_x + int(12 * SCALE), tag_y + int(12 * SCALE), 0.0, (255, 195, 225)),      # B in Better (pink)
        (start_x + int(115 * SCALE), tag_y + int(15 * SCALE), 0.35, (255, 195, 225)),    # P in Preparation (pink)
        (start_x + int(295 * SCALE), tag_y + int(24 * SCALE), 0.7, (255, 220, 240)),     # . after Prep (pink)
        (start_x + w1 + int(24 * SCALE), tag_y + int(14 * SCALE), 0.15, (147, 222, 255)),   # S in Stronger (sky blue)
        (start_x + w1 + int(170 * SCALE), tag_y + int(16 * SCALE), 0.55, (147, 222, 255)),  # P in Presentation (sky blue)
        (start_x + w1 + int(360 * SCALE), tag_y + int(24 * SCALE), 0.85, (210, 245, 255)),  # . at end (sky blue)
    ]

    # 5. Monospace Feature Pills (Smart Resume • Realistic Interviews • Detailed Feedback)
    def draw_doc_icon(d, cx, cy, s=int(10 * SCALE), color=(56, 189, 248)):
        x0, y0 = cx - s*0.6, cy - s*0.8
        x1, y1 = cx + s*0.6, cy + s*0.8
        fold = s*0.4
        pts = [(x0, y0), (x1 - fold, y0), (x1, y0 + fold), (x1, y1), (x0, y1)]
        d.polygon(pts, outline=color, fill=(15, 23, 42, 255), width=max(1, int(1.4 * SCALE)))
        d.line([(x1 - fold, y0), (x1 - fold, y0 + fold), (x1, y0 + fold)], fill=color, width=max(1, int(1.4 * SCALE)))
        d.line([(x0 + int(3*SCALE), cy - int(2*SCALE)), (x1 - int(3*SCALE), cy - int(2*SCALE))], fill=color, width=max(1, int(1.4 * SCALE)))
        d.line([(x0 + int(3*SCALE), cy + int(3*SCALE)), (x1 - int(3*SCALE), cy + int(3*SCALE))], fill=color, width=max(1, int(1.4 * SCALE)))

    def draw_mic_icon(d, cx, cy, s=int(10 * SCALE), color=(245, 158, 11)):
        w, h = s*0.38, s*0.7
        d.rounded_rectangle((cx - w, cy - h, cx + w, cy + h*0.2), radius=int(w), outline=color, fill=color, width=1)
        d.arc((cx - w*1.6, cy - h*0.4, cx + w*1.6, cy + h*0.6), start=0, end=180, fill=color, width=max(1, int(1.4 * SCALE)))
        d.line([(cx, cy + h*0.6), (cx, cy + h*0.95)], fill=color, width=max(1, int(1.4 * SCALE)))
        d.line([(cx - w*0.9, cy + h*0.95), (cx + w*0.9, cy + h*0.95)], fill=color, width=max(1, int(1.4 * SCALE)))

    def draw_chart_icon(d, cx, cy, s=int(10 * SCALE), color=(52, 211, 153)):
        x0, y0 = cx - s*0.7, cy - s*0.7
        x1, y1 = cx + s*0.7, cy + s*0.7
        d.line([(x0, y1), (x1, y1)], fill=color, width=max(1, int(1.4 * SCALE)))
        d.line([(cx - s*0.42, y1), (cx - s*0.42, cy + int(3*SCALE))], fill=color, width=int(2.2 * SCALE))
        d.line([(cx, y1), (cx, cy - int(2*SCALE))], fill=color, width=int(2.2 * SCALE))
        d.line([(cx + s*0.42, y1), (cx + s*0.42, cy - s*0.65)], fill=color, width=int(2.2 * SCALE))

    pills_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pills_layer)
    pills_data = [
        (draw_doc_icon, 'Smart Resume', (56, 189, 248)),
        (draw_mic_icon, 'Realistic Interviews', (245, 158, 11)),
        (draw_chart_icon, 'Detailed Feedback', (52, 211, 153))
    ]
    cur_bx = start_x + int(4 * SCALE)
    for icon_fn, label, color in pills_data:
        bbox = pdraw.textbbox((0, 0), label, font=font_mono)
        tw = bbox[2] - bbox[0]
        pw = tw + int(44 * SCALE)
        pdraw.rounded_rectangle(
            (cur_bx, pill_y, cur_bx + pw, pill_y + pill_h),
            radius=int(6 * SCALE),
            fill=(15, 23, 42, 255),
            outline=(30, 41, 59, 255),
            width=int(1 * SCALE)
        )
        icon_fn(pdraw, cur_bx + int(14 * SCALE), pill_y + pill_h // 2)
        pdraw.text((cur_bx + int(28 * SCALE), pill_y + int(6 * SCALE)), label, font=font_mono, fill=color)
        cur_bx += pw + int(12 * SCALE)

    # 6. Assemble Static Master Image
    base_banner = Image.new('RGBA', (W, H), (11, 17, 32, 255))
    bbdraw = ImageDraw.Draw(base_banner)
    bbdraw.rounded_rectangle(
        (int(6 * SCALE), int(6 * SCALE), W - int(6 * SCALE), H - int(6 * SCALE)),
        radius=int(18 * SCALE),
        fill=(14, 22, 40, 255),
        outline=(30, 41, 59, 255),
        width=int(2 * SCALE)
    )

    # Subtle ambient radial glow behind logo
    glow_bg = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow_bg)
    gl_cx = logo_pos_x + logo_display_w // 2
    gl_cy = logo_pos_y + logo_display_h // 2
    gdraw.ellipse((gl_cx - int(160 * SCALE), gl_cy - int(160 * SCALE), gl_cx + int(160 * SCALE), gl_cy + int(160 * SCALE)), fill=(14, 165, 233, 22))
    glow_bg = glow_bg.filter(ImageFilter.GaussianBlur(int(40 * SCALE)))
    base_banner.alpha_composite(glow_bg)

    # Composite static logo
    base_banner.alpha_composite(scaled_logo, (logo_pos_x, logo_pos_y))

    # Composite static title with soft shadow & warm glow
    base_banner.alpha_composite(title_shadow)
    base_banner.alpha_composite(title_glow)
    base_banner.alpha_composite(title_layer)

    # Composite tagline glow and text layer
    base_banner.alpha_composite(glow_broad)
    base_banner.alpha_composite(glow_inner)
    base_banner.alpha_composite(tag_layer)

    # Composite pills
    base_banner.alpha_composite(pills_layer)

    # 7. Render Animated Frames with gentle pink and sky-blue glitter twinkle on the tagline
    NUM_FRAMES = 24
    banner_frames = []

    print("Rendering frames with gentle pink & sky-blue glitter sparkle...")
    for f_idx in range(NUM_FRAMES):
        t = f_idx / float(NUM_FRAMES)
        frame = base_banner.copy()

        # Twinkling glitter starbursts across tagline
        glitter_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        glt_draw = ImageDraw.Draw(glitter_layer)
        for sx, sy, phase, spk_col in sparkle_bases:
            twinkle = math.sin((t + phase) * 2 * math.pi)
            if twinkle > 0.05:
                brt = int(255 * (twinkle - 0.05) / 0.95)
                s_size = int((7 + 5 * twinkle) * SCALE)
                glt_draw.line((sx - s_size, sy, sx + s_size, sy), fill=(255, 255, 255, brt), width=max(1, int(1.4 * SCALE)))
                glt_draw.line((sx, sy - s_size, sx, sy + s_size), fill=(255, 255, 255, brt), width=max(1, int(1.4 * SCALE)))
                glt_draw.ellipse((sx - int(2.5 * SCALE), sy - int(2.5 * SCALE), sx + int(2.5 * SCALE), sy + int(2.5 * SCALE)), fill=spk_col + (brt,))
        glitter_layer = glitter_layer.filter(ImageFilter.GaussianBlur(int(0.8 * SCALE)))
        frame.alpha_composite(glitter_layer)

        # Downsample with Lanczos for crystal-clear anti-aliasing
        frame_final = frame.resize((W_ORIG, H_ORIG), Image.Resampling.LANCZOS)
        banner_frames.append(frame_final.convert('RGB'))

    # Save animated GIF banner
    print("Saving assets/ascendcareer_banner.gif...")
    banner_frames[0].save(
        'assets/ascendcareer_banner.gif',
        save_all=True,
        append_images=banner_frames[1:],
        duration=70,
        loop=0,
        optimize=True
    )
    print("Banner GIF saved! Size:", os.path.getsize('assets/ascendcareer_banner.gif'))

    # Save static PNG banner
    print("Saving assets/ascendcareer_banner.png...")
    banner_frames[6].save('assets/ascendcareer_banner.png', optimize=True)
    print("Banner PNG saved! Size:", os.path.getsize('assets/ascendcareer_banner.png'))

    # Save sample frame for inspection
    banner_frames[6].save('assets/sample_clean_banner.png')
    print("Sample frame saved successfully!")

if __name__ == '__main__':
    create_banner()
