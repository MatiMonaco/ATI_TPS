from PIL import Image, ImageDraw
import os
import shutil

def draw_rect_iterative(it: int = 20):
    if os.path.isdir("rects"):
        shutil.rmtree("rects")
    try:
        os.mkdir("rects")
    except FileExistsError:
        print("delete rects file in current folder")
        exit(-1)
    top_left = 250
    bottom_right = 350
    draw_percentage = 0.8
    max_draw = int(600 * draw_percentage)
    step = (max_draw - bottom_right) / it
    print(f"step: {step}")
    for i in range(it):
        print(f"top_left: {top_left}, bottom_right: {bottom_right}")
        im = Image.new('RGB', (600, 600), (0, 0, 0))
        draw = ImageDraw.Draw(im)
        draw.rectangle((top_left, top_left, bottom_right, bottom_right), fill=(255, 255, 255), outline=(255, 255, 255))
        im.save(f'rects/rect_{i}.pgm', quality=95) 
        top_left -= step
        bottom_right += step

im = Image.new('RGB', (200, 200), (0, 0, 0))

draw = ImageDraw.Draw(im)
draw.rectangle((50, 50, 150, 150), fill=(255, 255, 255), outline=(255, 255, 255))
im.save('square.pgm', quality=95) 

circle = Image.new('RGB', (200, 200), (0, 0, 0))
draw_circle = ImageDraw.Draw(circle)
draw_circle.ellipse((50, 50, 150, 150), fill=(255, 255,255), outline=(255, 255, 255))
circle.save('circle.pgm', quality=95) 

draw_rect_iterative()