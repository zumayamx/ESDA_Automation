import os
from PySide6.QtWidgets import QFileDialog

class FileHandler:
    def __init__(self):
        # Default global directory
        self.output_dir = os.path.join(os.path.dirname(__file__), "../images")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_folder(self):
        """Open a file dialog to select a folder"""
        folder_path = QFileDialog.getExistingDirectory(None, "Seleccionar carpeta")
        if folder_path:
            self.output_dir = folder_path
            return folder_path
        return None
    
    def load_image_list(self):
        """Returns a list of only .jpg images in the output directory"""
        return [os.path.join(self.output_dir, f) for f in os.listdir(self.output_dir) if f.lower().endswith(".jpg")]
    
    def save_image(self, image, filename):
        save_path = os.path.join(self.output_dir, filename)
        image.save(save_path)
        print(f"Imagen guardada en {save_path}")
        return save_path