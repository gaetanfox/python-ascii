import glob
import shutil
import os
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont


class Digitizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.img = Image.open(filepath).convert("RGBA")

    def save(self, output_filepath):
        print("This has saved")
        if self.filepath.endswith(".jpg"):
            self.img = self.img.convert("RGB")
        self.img.save(output_filepath)

    def adjust_contrast(self, amount=1.5):
        enhancer = ImageEnhance.Contrast(self.img)
        self.img = enhancer.enhance(amount)

    def make_grayscale(self):
        self.img = ImageOps.grayscale(self.img)
        self.img = self.img.convert("RGBA")

    def make_upside_down(self):
        self.img = self.img.rotate(180)

    def make_thumbnail_size(self, size=(128, 128)):
        self.img.thumbnail(size)

    def make_square(self, size=200):
        (w, h) = self.img.size
        if w > h:
            x = (w - h) * 0.5
            y = 0
            box = (x, y, h + x, y + h)
        else:
            x = 0
            y = (h - w) * 0.5
            box = (x, y, x + w, y + w)
        self.img = self.img.resize((size, size), box=box)

    def add_watermark(self):
        font = ImageFont.truetype("ibm-plex-mono.ttf", 16)
        drawer = ImageDraw.Draw(self.img)

        drawer.text((32, 32), "Fox watermark", font=font, fill=(255, 0, 0, 100))


inputs = glob.glob("inputs/*.jpg")

os.makedirs("outputs", exist_ok=True)

for filepath in inputs:
    output = filepath.replace("inputs", "outputs")

    image = Digitizer(filepath)
    # image.make_upside_down()
    # image.make_thumbnail_size((200, 200))
    image.make_square()
    image.make_grayscale()
    image.adjust_contrast()
    image.add_watermark()
    image.save(output)
