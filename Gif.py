import os
import re
from PIL import Image

def remove_white_background_and_crop(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")

    datas = image.getdata()
    new_data = []
    for item in datas:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)
    
    # 保存为PNG格式确保透明度兼容性
    output_path = output_path.replace(".tiff", ".png")
    image.save(output_path, "PNG")

def create_gif(image_folder, output_gif, duration=100, loop=0):
    # 获取所有PNG文件并按数字序号排序
    filenames = [
        f for f in os.listdir(image_folder) 
        if f.lower().endswith(('.png', '.tif', '.tiff'))
    ]
    
    # 提取文件名中的四位数序号进行排序
    def sort_key(filename):
        match = re.search(r'\.(\d{4})\.', filename)
        return int(match.group(1)) if match else 0
    
    filenames.sort(key=sort_key)

    frames = []
    for filename in filenames:
        img_path = os.path.join(image_folder, filename)
        img = Image.open(img_path)
        
        # 确保处理透明背景（转换为P模式+调色板优化）
        if img.mode in ('RGBA', 'LA'):
            img = img.convert("RGBA")
            alpha = img.split()[3]
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            img = img.convert("RGB").convert("P", palette=Image.ADAPTIVE, colors=255)
            img.paste(255, mask)
        else:
            img = img.convert("P")
        
        frames.append(img)

    # 保存GIF（首帧作为基准）
    if frames:
        frames[0].save(
            output_gif,
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=duration,
            loop=loop,
            transparency=255,
            disposal=2
        )
        print(f"GIF saved to {output_gif}")
    else:
        print("No images found for GIF creation")

def batch_process_images(input_folder, output_folder, gif_output):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 处理所有图片
    processed_files = []
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.tif', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            remove_white_background_and_crop(input_path, output_path)
            processed_files.append(output_path.replace(".tiff", ".png"))
            print(f"Processed {filename}")

    # 生成GIF
    create_gif(output_folder, gif_output)

# 使用示例
input_folder = r"/mnt/g/PaperWork/run/1/singleArcbag/Animiation"
output_folder = r"/mnt/g/PaperWork/run/1/singleArcbag/Animiation_post"
gif_output = r"/mnt/g/PaperWork/run/1/singleArcbag/Animation.gif"

batch_process_images(input_folder, output_folder, gif_output)
