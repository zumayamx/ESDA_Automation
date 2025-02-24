import rembg
import numpy as np
from PIL import Image
from PIL.ImageQt import ImageQt
from core.file_handler import FileHandler
import os

class ImageEditor:
    def __init__(self, image_path):
        self.image_path = image_path
        # Load the original image from disk.
        self.original_image = Image.open(image_path)
        # Create a copy so we don't modify the original.
        self.current_image = self.original_image.copy()
        # Create a QImage for UI display (update this after each transformation)
        self.image_qt = ImageQt(self.current_image)
        # If the image failed to load, raise an exception.
        if self.original_image is None:
            raise FileNotFoundError("No se encontró la imagen.")
        self.file_handler = FileHandler()
        self.assets_dir = os.path.join(os.path.dirname(__file__), "../assets")
    
    def apply_white_background(self):
        # Convert the current image to a numpy array.
        input_data = np.array(self.current_image)
        # Remove the background using rembg.
        object_array = rembg.remove(input_data)
        object_image = Image.fromarray(object_array)
        
        # Convert to numpy array to work with the alpha channel.
        object_np = np.array(object_image)
        alpha_channel = object_np[:, :, 3]
        non_zero_pixels = np.where(alpha_channel > 0)

        # If there is any non-transparent area, process the transformation.
        if len(non_zero_pixels[0]) > 0:
            y_min, y_max = non_zero_pixels[0].min(), non_zero_pixels[0].max()
            x_min, x_max = non_zero_pixels[1].min(), non_zero_pixels[1].max()

            # Crop the image to the bounding box.
            cropped_image = object_image.crop((x_min, y_min, x_max, y_max))

            # Load a white background from assets, or create a new one if not found.
            white_bg_path = os.path.join(self.assets_dir, "white_bg.png")
            if os.path.exists(white_bg_path):
                white_bg = Image.open(white_bg_path)
            else:
                print("Fondo blanco no encontrado, generando uno nuevo...")
                white_bg = Image.new("RGBA", (3024, 3024), (255, 255, 255, 255))
            
            # Paste the cropped image onto the white background, centering it.
            white_bg.paste(
                cropped_image,
                (
                    (white_bg.width - cropped_image.width) // 2,
                    (white_bg.height - cropped_image.height) // 2
                ),
                cropped_image
            )
            # Update current_image with the transformed image.
            self.current_image = white_bg.convert("RGB")
            # Also update the QImage used for display.
            self.image_qt = ImageQt(self.current_image)
            print("Transformación aplicada: current_image actualizado.")
        else:
            print("No se detectó ningún objeto en la imagen.")