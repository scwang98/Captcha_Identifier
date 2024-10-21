import os
import requests
import base64
import json

# 创建保存图片和标注的文件夹
output_dir = "captcha-gen"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存words数据
words_data = []

# YOLO格式：x_center, y_center, width, height 都需要归一化，图片假设为宽高都是100
IMG_WIDTH = 310
IMG_HEIGHT = 155
BOX_WIDTH = 34
BOX_HEIGHT = 34

# 发送POST请求并处理数据
url = "http://localhost:8080/captcha/get"
headers = {'Content-Type': 'application/json'}
data = {"captchaType": "clickWord"}

for i in range(2435):
    # 发送POST请求获取JSON数据
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        rep_data = result.get("repData", {})

        # 1. 保存图片
        image_base64 = rep_data.get("originalImageBase64")
        if image_base64:
            # 解码Base64
            image_data = base64.b64decode(image_base64)
            # 生成图片文件名
            img_filename = os.path.join(output_dir, f"img_{i:04d}.png")
            with open(img_filename, "wb") as img_file:
                img_file.write(image_data)

        # 2. 处理并保存YOLO格式的标注数据
        point_list = rep_data.get("pointList", [])
        yolo_filename = os.path.join(output_dir, f"img_{i:04d}.txt")
        with open(yolo_filename, "w") as yolo_file:
            for point in point_list:
                x_center = (point["x"] + 13) / IMG_WIDTH
                y_center = (point["y"] - 8) / IMG_HEIGHT
                width = BOX_WIDTH / IMG_WIDTH
                height = BOX_HEIGHT / IMG_HEIGHT
                # YOLO标注格式：<class_id> <x_center> <y_center> <width> <height>
                yolo_file.write(f"15 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        # 3. 保存wordList到words.json
        word_list = rep_data.get("wordList", [])
        words_data.append({
            "image": f"img_{i:04d}.png",
            "words": word_list,
            "points": point_list
        })
        print(f"Succeeded to get data for img_{i:04d}, status code: {response.status_code}")
    else:
        print(f"Failed to get data for img_{i:04d}, status code: {response.status_code}")

# 保存所有wordList数据到words.json
with open("words.json", "w") as words_file:
    json.dump(words_data, words_file, indent=4, ensure_ascii=False)

print("Data processing completed.")
