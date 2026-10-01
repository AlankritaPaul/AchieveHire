import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_subtagline():
    print("Generating stylish subtagline badge (Prepare for the opportunity you’ve been waiting for)...")
    SCALE = 4
    
    font = ImageFont.truetype('assets/fonts/hatton/Hatton1.otf', int(38 * SCALE))
    
    part1 = "Prepare for the opportunity you"
    apo = "'"
    part2 = "ve been waiting for"
    
    w1 = font.getlength(part1)
    w_apo = font.getlength(apo)
    w2 = font.getlength(part2)
    
    total_w = int(w1 + w_apo + w2 + 8 * SCALE)
    
    bb = font.getbbox("Prepare for the opportunity you've been waiting for")
    txt_h = bb[3] - bb[1]
    
    pad_x = int(36 * SCALE)
    pad_y = int(24 * SCALE)
    
    W = total_w + pad_x * 2
    H = txt_h + pad_y * 2
    
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    
    base_x = pad_x
    base_y = pad_y - bb[1]
    
    def draw_text_parts(draw_target, offset_x, offset_y, fill_color):
        # part 1
        draw_target.text((base_x + offset_x, base_y + offset_y), part1, font=font, fill=fill_color)
        # apostrophe lifted slightly to natural shoulder height in Hatton font
        draw_target.text((base_x + offset_x + w1 + int(1 * SCALE), base_y + offset_y - int(12 * SCALE)), apo, font=font, fill=fill_color)
        # part 2
        draw_target.text((base_x + offset_x + w1 + w_apo + int(2 * SCALE), base_y + offset_y), part2, font=font, fill=fill_color)
    
    # 1. Soft Dark Drop Shadow for clean contrast across light and dark modes
    shd = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shd)
    draw_text_parts(sdraw, int(1.5 * SCALE), int(2.5 * SCALE), (0, 0, 0, 115))
    shd = shd.filter(ImageFilter.GaussianBlur(int(2.8 * SCALE)))
    img.alpha_composite(shd)
    
    # 2. Warm Golden Halo / Ambient Bloom
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    draw_text_parts(gdraw, 0, 0, (245, 175, 45, 145))
    glow = glow.filter(ImageFilter.GaussianBlur(int(7 * SCALE)))
    img.alpha_composite(glow)
    
    # 3. Rich Champagne Gold Text with Specular Edge
    txt_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(txt_layer)
    # Base warm gold
    draw_text_parts(tdraw, 0, 0, (255, 225, 135, 255))
    # Top specular highlight for depth
    draw_text_parts(tdraw, 0, -int(0.6 * SCALE), (255, 250, 225, 200))
    img.alpha_composite(txt_layer)
    
    # 4. Downscale for super-sampled anti-aliasing
    retina = img.resize((W // 2, H // 2), Image.Resampling.LANCZOS)
    retina.save('assets/subtagline.png')
    print("Saved assets/subtagline.png successfully! Size:", retina.size)

if __name__ == '__main__':
    create_subtagline()
