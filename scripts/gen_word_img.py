import os
from PIL import Image, ImageDraw, ImageFont

def generate_character_image(character, font_path = 'WenQuanZhengHei.ttf', size=(32, 32), font_size=25):

    image = Image.new('RGB', size, (255, 255, 255))
    
    draw = ImageDraw.Draw(image)
    
    font = ImageFont.truetype(font_path, font_size)
    
    bbox = draw.textbbox((0, 0), character, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2 - 3)

    draw.text(position, character, font=font, fill=(0, 0, 0))

    return image




if __name__ == '__main__':
    import json

    # 从文件读取 JSON 数据
    with open('words.json', 'r', encoding='utf-8') as f:
        data = json.load(f)


    for i in range(len(data)):
        item = data[i]
        words = item.get("words", [])
        # for j in range(len(words)):
        #     word = words[j]
        #     generate_character_image(word, 'WenQuanZhengHei.ttf', f"./characters/character{str(i // 5).zfill(3)}/img{str(i // 5).zfill(3)}_{(i % 5) * 4 + j}.png")

        word = words[0]
        image = generate_character_image(word, 'WenQuanZhengHei.ttf')

        output_path = f"./characters/character{str(i // 5).zfill(3)}/img{str(i // 5).zfill(3)}_{str((i % 5)).zfill(3)}.png"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 保存图像
        image.save(output_path)

