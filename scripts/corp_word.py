import os
from PIL import Image

def extract_characters(image_folder, label_folder, output_folder, image_prefix="img_", label_prefix="img_", num_images=100, img_ext=".png", label_ext=".txt"):
    # 创建保存字符的主目录
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i in range(num_images):
        # 构造图片和标注文件的名称
        image_filename = f"{image_prefix}{i:04d}{img_ext}"
        label_filename = f"{label_prefix}{i:04d}{label_ext}"

        image_path = os.path.join(image_folder, image_filename)
        label_path = os.path.join(label_folder, label_filename)

        # 打开图片
        if not os.path.exists(image_path) or not os.path.exists(label_path):
            print(f"Skipping {image_filename} as it or its label does not exist.")
            continue

        image = Image.open(image_path)
        img_width, img_height = image.size

        # 读取标签文件并裁剪图片
        with open(label_path, 'r') as f:
            lines = f.readlines()

            for idx, line in enumerate(lines):
                # YOLO 格式: <class> <x_center> <y_center> <width> <height>
                parts = line.strip().split()
                class_id = parts[0]
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])

                # 计算边界框的坐标（左上角和右下角）
                x_min = int((x_center - width / 2) * img_width)
                y_min = int((y_center - height / 2) * img_height)
                x_max = int((x_center + width / 2) * img_width)
                y_max = int((y_center + height / 2) * img_height)

                # 裁剪图片
                cropped_image = image.crop((x_min, y_min, x_max, y_max))

                # 创建保存该字符的目录
                char_folder = os.path.join(output_folder, f"character{str(i // 5).zfill(3)}")
                if not os.path.exists(char_folder):
                    os.makedirs(char_folder)

                # 保存裁剪的图片
                cropped_image_filename = f"img{str(i // 5).zfill(3)}_{str(5 + (i % 5) * 4 + idx).zfill(3)}.png"
                cropped_image_path = os.path.join(char_folder, cropped_image_filename)
                cropped_image.save(cropped_image_path)

                print(f"Saved cropped image to {cropped_image_path}")

# 示例调用
extract_characters(
    image_folder='./captcha-gen', 
    label_folder='./captcha-gen', 
    output_folder='./characters', 
    num_images=2435
)
