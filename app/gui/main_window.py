from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QMessageBox, QApplication
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.image_editor import ImageEditor
from core.file_handler import FileHandler
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de imágenes")

    def load_image(self):
        """ Cargar imagen y procesarla """
        file_path = self.file_handler.select_image(self)
        if file_path:
            try:
                editor = ImageEditor(file_path)
                editor.add_white_background()
                QMessageBox.information(self, "Éxito", "Imagen procesada y guardada en /images/")

                # Mostrar la imagen procesada
                processed_image_path = os.path.join(self.file_handler.output_dir, "object_with_white_bg.png")
                if os.path.exists(processed_image_path):
                    self.display_image(processed_image_path)
                else:
                    QMessageBox.warning(self, "Advertencia", "La imagen procesada no se encontró.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo procesar la imagen: {str(e)}")

    def display_image(self, image_path):
        """ Muestra la imagen procesada en pantalla """
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setScaledContents(True)