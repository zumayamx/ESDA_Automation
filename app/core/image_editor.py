import cv2
import rembg
import numpy as np
from PIL import Image

class ImageEditor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        if not self.image:
            raise FileNotFoundError
    
    # This is the main function to prepare the image for be edited
    def add_white_background(self):
        image_array = np.array(self.image)
        object_array = rembg.remove(image_array)
        object_image = Image.fromarray(object_array)

        object_image = object_image.convert('RGBA')
        pixels = object_image.load()
        width, height = object_image.size

        first_pixel_of_object = None
        for x in range(width - 1, -1, -1):
            for y in range(height):
                if pixels[x, y][3] > 0:
                    first_pixel_of_object = (x, y)
                    break
            if first_pixel_of_object is not None:
                break
        
        print('First pixel cordinate of object:', first_pixel_of_object)

        white_background = Image.open("../assets/white_bg.png")

        object_image = object_image.resize(white_background.size)

        white_background.paste(object_image, (0, 0), object_image)

        white_background.convert("RGB")
        white_background.save("object.png")

        # if first_pixel_of_object is not None:
        #     for y in range(height):
        #         pixels[first_pixel_of_object[0] + 1, y] = (255, 0, 0, 255)

        # object_image.save('object.png')

        # object_image = Image.fromarray(object_array)
        # object_image.save('object.png')

if __name__ == '__main__':
    editor = ImageEditor('../images/IMG_1788.jpg')
    editor.add_white_background()



