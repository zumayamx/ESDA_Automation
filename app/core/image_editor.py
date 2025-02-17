
import rembg
import numpy as np
from PIL import Image
# from segment_anything import SamPredictor, sam_model_registry
# import matplotlib.pyplot as plt

class ImageEditor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.MAX_BOUNDING_BOX_SIZE = 1000
        if not self.image:
            raise FileNotFoundError
    
    # This function is used to segment the image and get the object mask
    # it's beta function, we need to figure out if it worth to implement it
    # def sement_image(self):
    #     sam = sam_model_registry["vit_h"](checkpoint="../utils/sam_vit_h_4b8939.pth")
    #     predictor = SamPredictor(sam)
        
    #     # Convert PIL image to NumPy array
    #     image_array = np.array(self.image)

    #     # Define point coordinates and labels
    #     width, height = self.image.size
    #     point_coords = np.array([[width / 2, height / 2], [860, height / 2], [2330, height / 2]])
        
    #     # Example label, 1 for foreground, 0 for background
    #     point_labels = np.array([1, 1, 1])

    #     predictor.set_image(image_array)
    #     masks, _, _ = predictor.predict(point_coords=point_coords, point_labels=point_labels)

    #     # Mostrar la máscara generada
    #     plt.figure(figsize=(10, 6))
    #     plt.imshow(image_array)
    #     plt.imshow(masks[0], cmap="jet", alpha=0.5)
    #     plt.title("Máscara generada por Segment Anything")
    #     plt.axis("off")
    #     plt.show()

    def add_white_background_1(self):
        # Cargar imagen y eliminar fondo
        input_data = np.array(self.image)
        object_array = rembg.remove(input_data)
        object_image = Image.fromarray(object_array)

        # Convertir a numpy para trabajar con el canal alfa
        object_np = np.array(object_image)

        # Encontrar bounding box usando el canal alfa
        alpha_channel = object_np[:, :, 3]
        non_zero_pixels = np.where(alpha_channel > 0)

        # Calcular bounding box
        if len(non_zero_pixels[0]) > 0:
            y_min, y_max = non_zero_pixels[0].min(), non_zero_pixels[0].max()
            x_min, x_max = non_zero_pixels[1].min(), non_zero_pixels[1].max()

            # Recortar la imagen
            cropped_image = object_image.crop((x_min, y_min, x_max, y_max))
            cropped_image.save("object_cropped.png")

            # Agregar fondo blanco
            white_bg = Image.open("../assets/white_bg.png")
            white_bg.paste(cropped_image, ((white_bg.width - cropped_image.width) // 2, (white_bg.height - cropped_image.height) // 2), cropped_image)
            white_bg.convert("RGB").save("object_with_white_bg.png")

        else:
            print("No se detectó ningún objeto en la imagen.")
 
        
if __name__ == '__main__':
    editor = ImageEditor('../images/IMG_2028.jpg')
    # editor.sement_image()
    editor.add_white_background_1()