import glob
import shutil
import os
from PIL import Image, ImageOps, ImageEnhance


class Digitizer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.img = Image.open(filepath)

    def save(self, output_filepath):
        self.img.save(output_filepath)
        print("This has saved")

    def adjust_contrast(self, amount=1.5):
        enhancer = ImageEnhance.Contrast(self.img)
        self.img = enhancer.enhance(amount)

    def make_grayscale(self):
        self.img = ImageOps.grayscale(self.img)

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
    image.save(output)
