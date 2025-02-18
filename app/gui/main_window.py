from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QPushButton, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.image_editor import ImageEditor
from core.file_handler import FileHandler
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.setGeometry(300, 200, 800, 600)

        main_layout = QHBoxLayout()

        # Barra lateral (sidebar)
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignmentFlag.AlignTop)  # Asegurar alineación superior

        self.select_image_button = QPushButton("Seleccionar Imagen")
        self.select_image_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.select_image_button.clicked.connect(self.load_image)
        sidebar.addWidget(self.select_image_button)

        self.other_button = QPushButton("Otra acción (Futuro)")
        self.other_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.other_button.setEnabled(False)
        sidebar.addWidget(self.other_button)

        # Agregar un espacio al final para empujar los botones hacia arriba
        sidebar.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Contenido principal (donde se muestra la imagen)
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel("Aquí se mostrará la imagen procesada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; padding: 10px")
        content_layout.addWidget(self.image_label)

        # Agregar layouts al layout principal
        main_layout.addLayout(sidebar, 1)  # Sidebar ocupa 1 parte del espacio
        main_layout.addLayout(content_layout, 3)  # Área de imagen ocupa 3 partes

        # Configurar widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.file_handler = FileHandler()

    def load_image(self):
        file_path = self.file_handler.select_image(self)
        if file_path:
            try:
                editor = ImageEditor(file_path)
                editor.add_white_background()
                QMessageBox.information(self, "Éxito", "Imagen procesada y guardada en /images/")

                # Mostrar la imagen procesada
                processed_image_path = os.path.join(self.file_handler.output_dir, "object_with_white_bg.png")
                if os.path.exists(processed_image_path):
                    self.display_image(processed_image_path)
                else:
                    QMessageBox.warning(self, "Advertencia", "La imagen procesada no se encontró.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo procesar la imagen: {str(e)}")
    
    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setScaledContents(True)