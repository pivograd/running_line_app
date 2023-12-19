from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

text = 'ЖопкапОП 1'

width, height = 100, 100
font_size = 85

image = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", font_size)
draw.text((0, 0), text, font=font, fill='black')

temp_image_path = 'temp_image.png'
image.save(temp_image_path)

x_position = width

output_file = "running_line.mp4"
fps = 30
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

num_frames = 90
for frame in range(num_frames):
    draw.rectangle((0, 0, width, height), fill=(255, 255, 255))
    draw.text((x_position, 0), text, font=font, fill=(0, 0, 0))
    if len(text) > 7:
        x_position -= len(text)-(len(text)/3) + 1
    else:
        x_position -= 5

    frame_array = np.array(image)

    # Инвертирую цвета (OpenCV использует BGR, а не RGB)
    frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)

    video_writer.write(frame_array)

video_writer.release()

