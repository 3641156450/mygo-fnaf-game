from PIL import Image, ImageDraw, ImageFilter
import os, math, random

img_dir = r"C:\Users\36411\Doubao\chats\2026-09-11\new-chat-2\fnaf1-game\images"

# Load sprites directly
tomori = Image.open(os.path.join(img_dir, "tomori-idle.png")).convert("RGBA")
soyo = Image.open(os.path.join(img_dir, "soyo-idle.png")).convert("RGBA")

# Target canvas size (16:9) - higher res for clarity
W, H = 1280, 720

def scale_to_height(img, h):
    w = int(img.width * h / img.height)
    return img.resize((w, h), Image.LANCZOS)

# Scale characters to stand on stage
char_h = 520
tomori_s = scale_to_height(tomori, char_h)
soyo_s = scale_to_height(soyo, char_h)

# Dark stage background from image, enlarged for pan room
bg_img = Image.open(os.path.join(img_dir, "stage-bg.jpg")).convert("RGBA")
bg_img = bg_img.resize((int(W*1.2), int(H*1.2)), Image.LANCZOS)
# darken
bg_img = Image.eval(bg_img, lambda p: int(p * 0.5))

# Bake characters onto the enlarged background
floor_y = int(bg_img.height * 0.88)
tx = bg_img.width // 4 - tomori_s.width // 2
bg_img.alpha_composite(tomori_s, (tx, floor_y - tomori_s.height))
sx = int(bg_img.width * 3 // 4 - soyo_s.width // 2)
bg_img.alpha_composite(soyo_s, (sx, floor_y - soyo_s.height))

def make_bg(shift_x=0):
    ox = (bg_img.width - W) // 2 + shift_x
    oy = (bg_img.height - H) // 2
    return bg_img.crop((ox, oy, ox+W, oy+H))

frames = []
n_frames = 60
for i in range(n_frames):
    t = i / n_frames
    sway = int(math.sin(t * 2 * math.pi) * 120)
    bg = make_bg(sway)

    # Add noise / grain
    noise = Image.effect_noise((W, H), 18).convert("RGBA")
    noise = Image.eval(noise, lambda p: p // 4)
    bg = Image.blend(bg, noise, 0.15)

    # Scanlines
    draw = ImageDraw.Draw(bg)
    for y in range(0, H, 3):
        draw.line([(0, y), (W, y)], fill=(0, 0, 0, 40))

    frames.append(bg.convert("P", palette=Image.ADAPTIVE))

out = os.path.join(img_dir, "cam1a-idle.gif")
frames[0].save(out, save_all=True, append_images=frames[1:], duration=100, loop=0)
print(f"saved {out}, {len(frames)} frames, {os.path.getsize(out)} bytes")
