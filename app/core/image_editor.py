
import rembg
import numpy as np
from PIL import Image
from core.file_handler import FileHandler
import os

class ImageEditor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        if not self.image:
            raise FileNotFoundError("No se encontró la imagen.")
        self.file_handler = FileHandler()
        self.assets_dir = os.path.join(os.path.dirname(__file__), "../assets")

    def add_white_background(self):
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
            # cropped_path = self.file_handler.save_image(cropped_image, "object_cropped.png")

            # Agregar fondo blanco
            white_bg_path = os.path.join(self.assets_dir, "white_bg.png")
            if os.path.exists(white_bg_path):
                white_bg = Image.open(white_bg_path)
            else:
                print("Fondo blanco no encontrado, generando uno nuevo...")
                white_bg = Image.new("RGBA", (3024, 3024), (255, 255, 255, 255))

            white_bg.paste(cropped_image, ((white_bg.width - cropped_image.width) // 2, (white_bg.height - cropped_image.height) // 2), cropped_image)
            final_path = self.file_handler.save_image(white_bg.convert("RGB"), "object_with_white_bg.png")
            print(f"Imagen guardada en {final_path}")
                
        else:
            print("No se detectó ningún objeto en la imagen.")