import logging
import rembg
import numpy as np
from PIL import Image, ImageDraw
from PIL.ImageQt import ImageQt
from core.file_handler import FileHandler
import os

# Set up a logger for this module.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ImageEditor:
    """
    A class for editing images and applying transformations in-memory.
    
    Attributes:
        image_path (str): Path to the original image.
        original_image (PIL.Image.Image): The loaded original image.
        current_image (PIL.Image.Image): The current image after transformations.
        image_qt (QImage): The QImage version for UI display.
        GENERAL_SIZE (int): Base size for layout calculations.
        OBJECT_SPACE (int): Derived space for the image object.
        MEASURE_SPACE (int): Derived space reserved for measurements.
        MARGIN_SPACE (int): Derived margin space for additional UI elements.
        file_handler (FileHandler): Helper for file operations.
        assets_dir (str): Directory where asset files are stored.
        history (list): Stack holding versions of the image for undo/redo.
    """
    
    def __init__(self, image_path: str, general_size: int = 3024, object_space_factor: float = 0.5,
                 measure_space_factor: float = 0.3, margin_space_factor: int = 0.2) -> None:
        """
        Initialize the ImageEditor with the image at image_path.
        
        Args:
            image_path (str): The path to the image file.
            general_size (int, optional): Base size for layout calculations. Defaults to 3024.
        """
        self.image_path = image_path
        
        # Load the original image from disk.
        self.original_image = Image.open(image_path)
        # Create a copy so we don't modify the original.
        self.current_image = self.original_image.copy()
        # Create a QImage for UI display.
        self.image_qt = ImageQt(self.current_image)
        
        # Parameters for layout and transformation.
        self.GENERAL_SIZE = general_size
        self.OBJECT_SPACE = int(self.GENERAL_SIZE * object_space_factor)
        self.MEASURE_SPACE = int(self.GENERAL_SIZE * measure_space_factor)
        self.MARGIN_SPACE = int(self.GENERAL_SIZE *  margin_space_factor)
        
        # Initialize the file handler and assets directory.
        self.file_handler = FileHandler()
        
        # Maintain a history stack for undo functionality.
        self.history = [self.current_image.copy()]
    
    def apply_white_background(self) -> None:
        """
        Applies a white background to the current image after removing its background.
        Updates self.current_image and self.image_qt with the transformation result.
        """
        try:
            # Convert the current image to a numpy array.
            input_data = np.array(self.current_image)
            # Remove the background using rembg.
            object_array = rembg.remove(input_data)
            object_image = Image.fromarray(object_array)
            
            # Convert to numpy array to work with the alpha channel.
            object_np = np.array(object_image)
            alpha_channel = object_np[:, :, 3]
            non_zero_pixels = np.where(alpha_channel > 0)
            
            if len(non_zero_pixels[0]) > 0:
                y_min, y_max = non_zero_pixels[0].min(), non_zero_pixels[0].max()
                x_min, x_max = non_zero_pixels[1].min(), non_zero_pixels[1].max()
                
                # Crop the image to the bounding box.
                cropped_image = object_image.crop((x_min, y_min, x_max, y_max))
                
                # Create a new white background image.
                white_bg = Image.new("RGB", (self.OBJECT_SPACE + self.MEASURE_SPACE, self.OBJECT_SPACE + self.MEASURE_SPACE), (255, 255, 255))
                
                # Scale the cropped image if its size is larger than the object space.
                if cropped_image.width > self.OBJECT_SPACE or cropped_image.height > self.OBJECT_SPACE:
                    print("Scaling image")
                    cropped_image.thumbnail((self.OBJECT_SPACE, self.OBJECT_SPACE), Image.Resampling.LANCZOS)
                
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
                print("Current imge size: ", self.current_image.size)
                self.history.append(self.current_image.copy())
                self.image_qt = ImageQt(self.current_image)
                logger.info("White background transformation applied successfully.")
            else:
                logger.info("No object detected in the image.")
        except Exception as e:
            logger.error("Error applying white background: %s", e)
            raise e

    def apply_measure_line(self, start_point: tuple, end_point: tuple) -> None:
        """
        Draws a measurement line on the current image between start_point and end_point.
        The line is drawn in red with small rectangular markers at both endpoints.
        
        Args:
            start_point (tuple): (x, y) coordinates of the starting point.
            end_point (tuple): (x, y) coordinates of the ending point.
        """
        try:
            # Create a drawing context on the current image.
            draw = ImageDraw.Draw(self.current_image)
            
            # Define properties for the line and markers, dymanic in the future.
            line_color = (0, 0, 0)  # Black color for the measurement line.
            line_width = 20
            marker_size = 40
            
            # Draw the measurement line.
            draw.line([start_point, end_point], fill=line_color, width=line_width)
            
            # Draw rectangular markers at both endpoints.
            draw.rectangle(
                [ (start_point[0] - marker_size // 2, start_point[1] - marker_size // 2),
                  (start_point[0] + marker_size // 2, start_point[1] + marker_size // 2) ],
                fill=line_color
            )
            draw.rectangle(
                [ (end_point[0] - marker_size // 2, end_point[1] - marker_size // 2),
                  (end_point[0] + marker_size // 2, end_point[1] + marker_size // 2) ],
                fill=line_color
            )
            
            # Update the QImage for UI display.
            self.image_qt = ImageQt(self.current_image)

            # print("Current imge size: ", self.current_image.size)
            # Append the new state to the history stack.
            self.history.append(self.current_image.copy())
            logger.info("Measurement line applied successfully.")
        except Exception as e:
            logger.error("Error applying measure line: %s", e)
            raise e
        
        def apply_zoom(self):
            pass