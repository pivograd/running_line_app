from django.shortcuts import render, redirect
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from .forms import GenerateTextForm
from .models import GeneratedText

def generate(request):
    if request.method == 'POST':
        form = GenerateTextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            GeneratedText.objects.create(text=text)
            return redirect(f'http://127.0.0.1:8000/generate/{text}')
    else:
        form = GenerateTextForm()
    return render(request, 'running_line/generate_running_line.html', {'form': form})

def view_for_redirect(request):

    return redirect('http://127.0.0.1:8000/generate')

def generate_running_line(request, text):

    width, height = 100, 100
    font_size = 85
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text((100, 100), text, font=font, fill='black')
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
            x_position -= len(text) - (len(text) / 3) + 1
        else:
            x_position -= 5
        frame_array = np.array(image)
        # Инвертирую цвета (OpenCV использует BGR, а не RGB)
        frame_array = cv2.cvtColor(frame_array, cv2.COLOR_RGB2BGR)
        video_writer.write(frame_array)
    video_writer.release()
    # Отдаем видеофайл пользователю для скачивания
    with open(output_file, 'rb') as video_file:
        response = HttpResponse(video_file.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename={output_file}'
        return response
