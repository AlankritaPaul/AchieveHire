import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_cursive_tagline():
    print("Generating cursive tagline badge (Better Preparation. Stronger Presentation.)...")
    SCALE = 4
    font = ImageFont.truetype('assets/fonts/GreatVibes.ttf', int(64 * SCALE))

    tag1 = "Better Preparation."
    tag2 = " Stronger Presentation."
    w1 = font.getlength(tag1)
    w2 = font.getlength(tag2)
    total_w = int(w1 + w2)

    bbox = font.getbbox(tag1 + tag2)
    pad_x = int(40 * SCALE)
    pad_y = int(28 * SCALE)
    txt_h = bbox[3] - bbox[1]

    W = total_w + pad_x * 2
    H = txt_h + pad_y * 2
    tag_x = pad_x
    tag_y = pad_y - bbox[1]

    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))

    # Subtle drop shadow for cross-theme contrast (works on light & dark)
    shd = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shd)
    sdraw.text((tag_x + int(1.5 * SCALE), tag_y + int(2.5 * SCALE)), tag1, font=font, fill=(0, 0, 0, 95))
    sdraw.text((tag_x + w1 + int(1.5 * SCALE), tag_y + int(2.5 * SCALE)), tag2, font=font, fill=(0, 0, 0, 95))
    shd = shd.filter(ImageFilter.GaussianBlur(int(2.8 * SCALE)))
    img.alpha_composite(shd)

    # Luminous glow (light pink behind Better Preparation., sky blue behind Stronger Presentation.)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.text((tag_x, tag_y), tag1, font=font, fill=(244, 114, 182, 160))
    gdraw.text((tag_x + w1, tag_y), tag2, font=font, fill=(56, 189, 248, 160))
    glow = glow.filter(ImageFilter.GaussianBlur(int(8 * SCALE)))
    img.alpha_composite(glow)

    # Core rich text
    txt_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tldraw = ImageDraw.Draw(txt_layer)
    # Light pink with specular accent
    tldraw.text((tag_x, tag_y), tag1, font=font, fill=(244, 114, 182, 255))
    tldraw.text((tag_x, tag_y - int(0.5 * SCALE)), tag1, font=font, fill=(255, 205, 230, 220))
    # Sky blue with specular accent
    tldraw.text((tag_x + w1, tag_y), tag2, font=font, fill=(56, 189, 248, 255))
    tldraw.text((tag_x + w1, tag_y - int(0.5 * SCALE)), tag2, font=font, fill=(186, 235, 255, 220))

    img.alpha_composite(txt_layer)

    # Downscale for super-sampled anti-aliasing
    retina = img.resize((W // 2, H // 2), Image.Resampling.LANCZOS)
    retina.save('assets/tagline.png')
    print("Saved assets/tagline.png successfully! Size:", retina.size)

if __name__ == '__main__':
    create_cursive_tagline()
