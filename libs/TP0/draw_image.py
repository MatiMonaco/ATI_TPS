from PIL import Image, ImageDraw

im = Image.new('RGB', (200, 200), (0, 0, 0))

draw = ImageDraw.Draw(im)
draw.rectangle((50, 50, 150, 150), fill=(255, 255, 255), outline=(255, 255, 255))
im.save('square.pgm', quality=95) 

circle = Image.new('RGB', (200, 200), (0, 0, 0))
draw_circle = ImageDraw.Draw(circle)
draw_circle.ellipse((50, 50, 150, 150), fill=(255, 255,255), outline=(255, 255, 255))
circle.save('circle.pgm', quality=95) 