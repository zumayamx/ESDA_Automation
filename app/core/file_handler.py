import os
from PySide6.QtWidgets import QFileDialog

class FileHandler:
    def __init__(self):
        self.output_dir = os.path.join(os.path.dirname(__file__), "../images")
        os.makedirs(self.output_dir, exist_ok=True)

    def select_image(self, parent):
        """Open a file dialog to select an image"""
        file_path, _ = QFileDialog.getOpenFileName(parent, "Seleccionar imagen", "", "Images (*.png *.jpg *.jpeg)")
        return file_path if file_path else None
    
    def save_image(self, image, filename):
        save_path = os.path.join(self.output_dir, filename)
        image.save(save_path)
        print(f"Imagen guardada en {save_path}")
        return save_path