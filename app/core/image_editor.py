import cv2
import rembg
import numpy as np
from PIL import Image

from segment_anything import SamPredictor, sam_model_registry
import matplotlib.pyplot as plt

settings = rembg.new_session(
    alpha_matting=True,
    alpha_matting_foreground_threshold=220,
    alpha_matting_background_threshold=30,
    alpha_matting_erode_size=5
)

class ImageEditor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        if not self.image:
            raise FileNotFoundError
        
    def sement_image(self):
        sam = sam_model_registry["vit_h"](checkpoint="../utils/sam_vit_h_4b8939.pth")
        predictor = SamPredictor(sam)
        
        # Convert PIL image to NumPy array
        image_array = np.array(self.image)

        # Define point coordinates and labels
        width, height = self.image.size
        point_coords = np.array([[width / 2, height / 2]])  # Example coordinates, you should adjust this
        point_labels = np.array([1])  # Example label, 1 for foreground
        
        predictor.set_image(image_array)
        masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)

            # Mostrar la máscara generada
        plt.figure(figsize=(10, 6))
        plt.imshow(image_array)
        plt.imshow(masks[0], cmap="jet", alpha=0.5)  # Superponer la máscara semitransparente
        plt.title("Máscara generada por Segment Anything")
        plt.axis("off")
        plt.show()
    
    # This is the main function to prepare the image for be edited
    def add_white_background(self):
        image_array = np.array(self.image)
        object_array = rembg.remove(image_array, session=settings)
        object_image = Image.fromarray(object_array)

        # object_image = object_image.convert('RGBA')
        # pixels = object_image.load()
        # width, height = object_image.size

        # first_pixel_of_object = None
        # for x in range(width - 1, -1, -1):
        #     for y in range(height):
        #         if pixels[x, y][3] > 0:
        #             first_pixel_of_object = (x, y)
        #             break
        #     if first_pixel_of_object is not None:
        #         break
        
        # print('First pixel cordinate of object:', first_pixel_of_object)

        white_background = Image.open("../assets/white_bg.png")

        # object_image = object_image.resize(white_background.size)

        white_background.paste(object_image, (0, 0), object_image)
        white_background.convert("RGBA")
        white_background.save("object.png")

if __name__ == '__main__':
    editor = ImageEditor('../images/IMG_1988.jpg')
    editor.sement_image()
    # editor.add_white_background()

