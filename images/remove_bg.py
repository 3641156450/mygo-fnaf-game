from PIL import Image
import os

img_dir = r"C:\Users\36411\Doubao\chats\2026-09-11\new-chat-2\fnaf1-game\images"

def remove_white_bg(src, dst, threshold=240):
    img = Image.open(src).convert("RGBA")
    datas = img.getdata()
    new_data = []
    for item in datas:
        r, g, b, a = item
        # near-white pixel -> transparent
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    img.save(dst, "PNG")
    print(f"saved {dst} ({img.size})")

# 1. Tomori idle
remove_white_bg(os.path.join(img_dir, "tomori-idle.png"),
                os.path.join(img_dir, "tomori-idle.png"))

# 2. Soyo idle (use new image)
remove_white_bg(os.path.join(img_dir, "soyo-new.jpg"),
                os.path.join(img_dir, "soyo-idle.png"))
