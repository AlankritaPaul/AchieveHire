import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_banner():
    print("Initializing Refined Banner & Logo Generator...")
    
    # 1. Load and prepare logo components
    logo = Image.open('assets/logo.png').convert('RGBA')
    arr = np.array(logo)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    cx, cy = 557.0, 128.0
    y_ind, x_ind = np.indices(arr.shape[:2])
    dist_target = np.sqrt((x_ind - cx)**2 + (y_ind - cy)**2)

    # Gold arrow segmentation
    is_gold = (a > 50) & (r > 130) & (g > 80) & (b < 120) & (r > b + 25)
    arrow_mask = (is_gold & (dist_target > 25)) | ((dist_target <= 25) & (dist_target > 2) & (x_ind < 560) & (y_ind > 115) & (r > 130) & (b < 100))

    # Dilate mask slightly for cleaning open-air flight path
    mask_img = Image.fromarray((arrow_mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    dilated_arrow_mask = np.array(mask_img) > 128

    # Spine tracing
    spine = []
    for y in range(623, 80, -1):
        xs = np.where(arrow_mask[y, :])[0]
        if len(xs) > 0:
            spine.append((float(np.mean(xs)), float(y)))

    dists = [0.0]
    for i in range(1, len(spine)):
        dx = spine[i][0] - spine[i-1][0]
        dy = spine[i][1] - spine[i-1][1]
        dists.append(dists[-1] + np.sqrt(dx**2 + dy**2))

    total_len = dists[-1]
    y_to_s = {}
    for i, pt in enumerate(spine):
        y_to_s[int(pt[1])] = dists[i] / total_len

    s_map = np.zeros(arr.shape[:2], dtype=float)
    for y, s_val in y_to_s.items():
        s_map[y, arrow_mask[y, :]] = s_val

    # Clean target layer with perfect concentric circles
    target_layer = Image.new('RGBA', logo.size, (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(target_layer)
    tdraw.ellipse((cx - 92, cy - 92, cx + 92, cy + 92), fill=(36, 44, 53, 255))
    tdraw.ellipse((cx - 71, cy - 71, cx + 71, cy + 71), fill=(48, 146, 198, 255))
    tdraw.ellipse((cx - 47, cy - 47, cx + 47, cy + 47), fill=(230, 70, 40, 255))
    tdraw.ellipse((cx - 25, cy - 25, cx + 25, cy + 25), fill=(250, 220, 15, 255))

    # Base ribbon with clean open-air flight path and dark groove inside ribbon body
    base_arr = arr.copy()
    base_arr[arrow_mask, 3] = 0
    in_flight = dilated_arrow_mask & (y_ind < 340) & (dist_target > 90)
    base_arr[in_flight, 3] = 0
    in_groove = arrow_mask & (y_ind >= 340) & (dist_target > 100)
    base_arr[in_groove] = [16, 55, 82, 220]
    base_img = Image.fromarray(base_arr)

    # 2. Canvas parameters (2x supersampling)
    SCALE = 2
    W_ORIG, H_ORIG = 1200, 380
    W, H = W_ORIG * SCALE, H_ORIG * SCALE

    # Fonts
    font_title = ImageFont.truetype('assets/fonts/glitten/Glitten-Regular.otf', int(64 * SCALE))
    font_tagline = ImageFont.truetype('assets/fonts/Kerry Halton.ttf', int(46 * SCALE))
    font_mono = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', int(15 * SCALE))

    # Right side text coordinates
    start_x = int(395 * SCALE)
    base_y = int(98 * SCALE)

    # Pre-render Title layer (Completely STATIC, NO animation)
    title_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(title_layer)

    # 'AscendCareer' text in Glitten luxury serif
    t_draw.text((start_x, base_y), 'AscendCareer', font=font_title, fill=(248, 250, 252, 255))
    bbox_all = t_draw.textbbox((start_x, base_y), 'AscendCareer', font=font_title)
    bbox_A = t_draw.textbbox((start_x, base_y), 'A', font=font_title)
    ax_mid = (bbox_A[0] + bbox_A[2]) / 2.0

    # Orange 'A' left leg matching Ascend style
    a_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(a_layer)
    a_draw.text((start_x, base_y), 'A', font=font_title, fill=(255, 122, 0, 255))
    a_arr = np.array(a_layer)
    y_ia, x_ia = np.indices(a_arr.shape[:2])
    is_right_leg = (x_ia > ax_mid + int(6 * SCALE))
    a_arr[is_right_leg, 3] = 0

    # Bold angled orange left stroke
    peak = (bbox_A[0] + int(19 * SCALE), bbox_A[1] + int(5 * SCALE))
    foot = (bbox_A[0] + int(2 * SCALE), bbox_A[3] - int(4 * SCALE))
    leg_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(leg_layer)
    ldraw.line([foot, peak], fill=(255, 122, 0, 255), width=int(12 * SCALE))
    ldraw.line([foot, peak], fill=(255, 180, 50, 255), width=int(3 * SCALE))

    title_layer.alpha_composite(Image.fromarray(a_arr))
    title_layer.alpha_composite(leg_layer)

    # Static swoosh curve points
    p0 = (bbox_A[0] + int(8 * SCALE), base_y + int(42 * SCALE))
    p1 = (start_x + int(110 * SCALE), base_y - int(34 * SCALE))
    p2 = (start_x + int(370 * SCALE), base_y - int(40 * SCALE))
    p3 = (bbox_all[2] + int(16 * SCALE), base_y - int(10 * SCALE))

    curve_pts = []
    for t_val in np.linspace(0, 1, 90):
        bx = (1-t_val)**3 * p0[0] + 3*(1-t_val)**2 * t_val * p1[0] + 3*(1-t_val) * t_val**2 * p2[0] + t_val**3 * p3[0]
        by = (1-t_val)**3 * p0[1] + 3*(1-t_val)**2 * t_val * p1[1] + 3*(1-t_val) * t_val**2 * p2[1] + t_val**3 * p3[1]
        curve_pts.append((bx, by))

    pt_last = curve_pts[-1]
    pt_prev = curve_pts[-4]
    curve_ang = math.atan2(pt_last[1] - pt_prev[1], pt_last[0] - pt_prev[0])
    head_len = 22 * SCALE
    head_w = 14 * SCALE
    head_tip = (pt_last[0] + head_len * 0.5 * math.cos(curve_ang), pt_last[1] + head_len * 0.5 * math.sin(curve_ang))
    head_left = (pt_last[0] - head_len * 0.5 * math.cos(curve_ang) + head_w * 0.5 * math.sin(curve_ang),
                 pt_last[1] - head_len * 0.5 * math.sin(curve_ang) - head_w * 0.5 * math.cos(curve_ang))
    head_right = (pt_last[0] - head_len * 0.5 * math.cos(curve_ang) - head_w * 0.5 * math.sin(curve_ang),
                  pt_last[1] - head_len * 0.5 * math.sin(curve_ang) + head_w * 0.5 * math.cos(curve_ang))

    curve_static = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(curve_static)
    for i in range(len(curve_pts) - 1):
        t_c = i / float(len(curve_pts))
        th = (3.2 + 5.2 * math.sin(t_c * math.pi * 0.9)) * SCALE
        pt1 = curve_pts[i]
        pt2 = curve_pts[i+1]
        cdraw.line([pt1, pt2], fill=(255, 122, 0, 255), width=max(int(2 * SCALE), int(th)))
        cdraw.line([pt1, pt2], fill=(255, 210, 70, 255), width=max(int(1 * SCALE), int(th * 0.4)))

    cdraw.polygon([head_tip, head_left, head_right], fill=(255, 122, 0, 255))
    cdraw.polygon([(head_tip[0], head_tip[1]), 
                   (head_left[0] + int(2 * SCALE) * math.cos(curve_ang), head_left[1] + int(2 * SCALE) * math.sin(curve_ang)),
                   (head_right[0] + int(2 * SCALE) * math.cos(curve_ang), head_right[1] + int(2 * SCALE) * math.sin(curve_ang))], 
                  fill=(255, 210, 70, 255))

    title_layer.alpha_composite(curve_static)

    # 3. Tagline (Generous breathing room below title)
    tagline_text = "Where Preparation Meets Opportunity."
    tag_y = base_y + int(94 * SCALE)
    tag_bbox = t_draw.textbbox((start_x, tag_y), tagline_text, font=font_tagline)

    # Static golden text layer
    tag_halo_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    th_draw = ImageDraw.Draw(tag_halo_layer)
    th_draw.text((start_x + int(4 * SCALE), tag_y), tagline_text, font=font_tagline, fill=(245, 158, 11, 200))
    tag_halo_layer = tag_halo_layer.filter(ImageFilter.GaussianBlur(int(4 * SCALE)))

    tag_core = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tc_draw = ImageDraw.Draw(tag_core)
    tc_draw.text((start_x + int(4 * SCALE), tag_y), tagline_text, font=font_tagline, fill=(255, 215, 0, 255))
    tc_draw.text((start_x + int(4 * SCALE), tag_y - int(1 * SCALE)), tagline_text, font=font_tagline, fill=(255, 248, 180, 180))

    sparkle_bases = [
        (start_x + int(30 * SCALE), tag_y + int(18 * SCALE), 0.0),
        (start_x + int(115 * SCALE), tag_y + int(12 * SCALE), 0.35),
        (start_x + int(220 * SCALE), tag_y + int(25 * SCALE), 0.7),
        (start_x + int(340 * SCALE), tag_y + int(10 * SCALE), 0.15),
        (start_x + int(460 * SCALE), tag_y + int(28 * SCALE), 0.55),
        (start_x + int(560 * SCALE), tag_y + int(14 * SCALE), 0.85),
        (start_x + int(660 * SCALE), tag_y + int(22 * SCALE), 0.25),
        (start_x + int(720 * SCALE), tag_y + int(12 * SCALE), 0.65),
    ]

    # 4. Monospace Pills Functions & Setup
    pill_y = tag_y + int(80 * SCALE)
    pill_h = int(28 * SCALE)

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

    # Pre-render static monospace pills
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

    NUM_FRAMES = 32
    banner_frames = []
    logo_only_frames = []

    logo_display_w = int(300 * SCALE)
    logo_display_h = int(300 * SCALE)
    logo_pos_x = int(45 * SCALE)
    logo_pos_y = int(40 * SCALE)

    print("Rendering 32 high-resolution animation frames...")

    for f_idx in range(NUM_FRAMES):
        t = f_idx / float(NUM_FRAMES)
        
        # --- LOGO ANIMATION (at native logo resolution) ---
        logo_canvas = Image.new('RGBA', logo.size, (0, 0, 0, 0))
        logo_canvas.alpha_composite(target_layer)
        logo_canvas.alpha_composite(base_img)

        # Timeline:
        # 0.00 to 0.42: Golden arrow emerges from below, curves through ribbon, flies to target
        # 0.42: Direct Hit! Impact explosion at bullseye
        # 0.42 to 0.68: Concentric shockwaves ripple through bullseye circles
        # 0.60 to 0.88: Specular shimmer sweeps along full golden arrow
        # 0.88 to 1.00: Full glory hold before looping
        if t < 0.42:
            s_front = t / 0.42
        else:
            s_front = 1.0

        arrow_frame = arr.copy()
        unrevealed = arrow_mask & (s_map > s_front)
        arrow_frame[unrevealed, 3] = 0
        logo_canvas.alpha_composite(Image.fromarray(arrow_frame))

        # Dynamic leading arrowhead when arrow is in flight
        if t < 0.42:
            spine_idx = min(int(s_front * (len(spine) - 1)), len(spine) - 1)
            fx, fy = spine[spine_idx]
            if spine_idx > 0:
                dx = fx - spine[spine_idx - 1][0]
                dy = fy - spine[spine_idx - 1][1]
            else:
                dx, dy = 1, -1
            ang = math.atan2(dy, dx)

            glow = Image.new('RGBA', logo.size, (0, 0, 0, 0))
            gdraw = ImageDraw.Draw(glow)
            for r_g in [26, 16, 8]:
                gdraw.ellipse((fx - r_g, fy - r_g, fx + r_g, fy + r_g), fill=(255, 220, 80, 130))

            hl = 34
            hw = 20
            p_tip = (fx + hl * 0.45 * math.cos(ang), fy + hl * 0.45 * math.sin(ang))
            p_left = (fx - hl * 0.55 * math.cos(ang) + hw * 0.5 * math.sin(ang),
                      fy - hl * 0.55 * math.sin(ang) - hw * 0.5 * math.cos(ang))
            p_right = (fx - hl * 0.55 * math.cos(ang) - hw * 0.5 * math.sin(ang),
                       fy - hl * 0.55 * math.sin(ang) + hw * 0.5 * math.cos(ang))
            gdraw.polygon([p_tip, p_left, p_right], fill=(255, 225, 90, 255))
            glow = glow.filter(ImageFilter.GaussianBlur(1.0))
            logo_canvas.alpha_composite(glow)

        # Bullseye impact & shockwave rings (t: 0.42 to 0.70)
        if 0.42 <= t < 0.70:
            t_imp = (t - 0.42) / 0.28
            imp_layer = Image.new('RGBA', logo.size, (0, 0, 0, 0))
            idraw = ImageDraw.Draw(imp_layer)

            # Expanding concentric shockwave rings
            shock_r = int(14 + 88 * t_imp)
            shock_alpha = int(255 * (1.0 - t_imp))
            idraw.ellipse((cx - shock_r, cy - shock_r, cx + shock_r, cy + shock_r), outline=(255, 235, 120, shock_alpha), width=3)
            if shock_r > 20:
                idraw.ellipse((cx - shock_r + 14, cy - shock_r + 14, cx + shock_r - 14, cy + shock_r - 14), outline=(255, 255, 255, int(shock_alpha * 0.75)), width=2)

            # Starburst flash
            flash_alpha = int(255 * max(0.0, 1.0 - t_imp * 1.6))
            if flash_alpha > 0:
                burst_len = int(48 * (1.0 - t_imp * 0.5))
                for rot in [0, 45, 90, 135]:
                    rad = math.radians(rot)
                    cos_r, sin_r = math.cos(rad), math.sin(rad)
                    idraw.line((cx - burst_len * cos_r, cy - burst_len * sin_r, cx + burst_len * cos_r, cy + burst_len * sin_r), fill=(255, 255, 255, flash_alpha), width=3)
                idraw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=(255, 240, 150, flash_alpha))

            imp_layer = imp_layer.filter(ImageFilter.GaussianBlur(1.2))
            logo_canvas.alpha_composite(imp_layer)

        # Specular shimmer traveling along the arrow (t: 0.58 to 0.90)
        if 0.58 <= t < 0.90:
            t_shim = (t - 0.58) / 0.32
            shim_layer = Image.new('RGBA', logo.size, (0, 0, 0, 0))
            shdraw = ImageDraw.Draw(shim_layer)
            shim_idx = int(t_shim * (len(spine) - 1))
            sx, sy = spine[shim_idx]
            shdraw.ellipse((sx - 22, sy - 22, sx + 22, sy + 22), fill=(255, 255, 255, 200))
            shdraw.ellipse((sx - 38, sy - 38, sx + 38, sy + 38), fill=(255, 230, 120, 130))

            shim_arr = np.array(shim_layer)
            shim_arr[~arrow_mask] = 0
            logo_canvas.alpha_composite(Image.fromarray(shim_arr))

        # Store standalone logo frame (scaled to 400x400)
        logo_only_frame = logo_canvas.resize((400, 400), Image.Resampling.LANCZOS)
        logo_only_frames.append(logo_only_frame)

        # --- BANNER FRAME COMPOSITION ---
        banner = Image.new('RGBA', (W, H), (11, 17, 32, 255))
        bdraw = ImageDraw.Draw(banner)

        # Subtle dark gradient & border
        bdraw.rounded_rectangle(
            (int(6 * SCALE), int(6 * SCALE), W - int(6 * SCALE), H - int(6 * SCALE)),
            radius=int(18 * SCALE),
            fill=(14, 22, 40, 255),
            outline=(30, 41, 59, 255),
            width=int(2 * SCALE)
        )

        # Subtle radial glow behind the logo
        glow_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        gldraw = ImageDraw.Draw(glow_layer)
        gl_cx = logo_pos_x + logo_display_w // 2
        gl_cy = logo_pos_y + logo_display_h // 2
        gldraw.ellipse((gl_cx - int(160 * SCALE), gl_cy - int(160 * SCALE), gl_cx + int(160 * SCALE), gl_cy + int(160 * SCALE)), fill=(14, 165, 233, 20))
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(int(40 * SCALE)))
        banner.alpha_composite(glow_layer)

        # Composite animated logo onto banner
        scaled_logo = logo_canvas.resize((logo_display_w, logo_display_h), Image.Resampling.LANCZOS)
        banner.alpha_composite(scaled_logo, (logo_pos_x, logo_pos_y))

        # 1. Composite STATIC Title (AscendCareer + Orange 'A' + Swoosh) - NO ANIMATION
        banner.alpha_composite(title_layer)

        # 2. Tagline with soft halo and gentle glittering sparkles
        banner.alpha_composite(tag_halo_layer)
        banner.alpha_composite(tag_core)

        # Animated Glitter Sparkles (twinkling starbursts across tagline)
        glitter_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        glt_draw = ImageDraw.Draw(glitter_layer)
        for sx, sy, phase in sparkle_bases:
            twinkle = math.sin((t + phase) * 2 * math.pi)
            if twinkle > 0.1:
                brt = int(255 * (twinkle - 0.1) / 0.9)
                s_size = int((8 + 6 * twinkle) * SCALE)
                glt_draw.line((sx - s_size, sy, sx + s_size, sy), fill=(255, 255, 255, brt), width=max(1, int(1.4 * SCALE)))
                glt_draw.line((sx, sy - s_size, sx, sy + s_size), fill=(255, 255, 255, brt), width=max(1, int(1.4 * SCALE)))
                glt_draw.ellipse((sx - int(3 * SCALE), sy - int(3 * SCALE), sx + int(3 * SCALE), sy + int(3 * SCALE)), fill=(255, 230, 100, brt))
        glitter_layer = glitter_layer.filter(ImageFilter.GaussianBlur(int(1 * SCALE)))
        banner.alpha_composite(glitter_layer)

        # 3. Monospace Feature Pills (Smart Resume • Realistic Interviews • Detailed Feedback)
        banner.alpha_composite(pills_layer)

        # Downsample with Lanczos for crystal-clear anti-aliasing
        frame_final = banner.resize((W_ORIG, H_ORIG), Image.Resampling.LANCZOS)
        banner_frames.append(frame_final.convert('RGB'))

    # Save animated GIF banner
    print("Saving assets/ascendcareer_banner.gif...")
    banner_frames[0].save(
        'assets/ascendcareer_banner.gif',
        save_all=True,
        append_images=banner_frames[1:],
        duration=65,
        loop=0,
        optimize=True
    )
    print("Banner saved! Size:", os.path.getsize('assets/ascendcareer_banner.gif'))

    # Save animated standalone logo
    print("Saving assets/logo_animated.gif...")
    logo_only_frames[0].save(
        'assets/logo_animated.gif',
        save_all=True,
        append_images=logo_only_frames[1:],
        duration=65,
        loop=0,
        disposal=2
    )
    print("Animated logo saved! Size:", os.path.getsize('assets/logo_animated.gif'))

    # Save sample frames for inspection
    banner_frames[5].save('assets/sample_banner_f5.png')
    banner_frames[14].save('assets/sample_banner_f14.png')
    banner_frames[22].save('assets/sample_banner_f22.png')
    print("Sample frames saved successfully!")

if __name__ == '__main__':
    create_banner()
