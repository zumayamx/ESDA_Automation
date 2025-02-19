from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QMessageBox, QSizePolicy, QApplication, QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QRect
from core.image_editor import ImageEditor
from core.file_handler import FileHandler
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")

        # Layout Principal
        main_layout = QVBoxLayout()

        # Barra Superior con Botones Centrados
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_add_image = QPushButton("🖼 Agregar Imagen")
        self.btn_add_image.setFixedSize(150, 50)
        self.btn_add_image.setStyleSheet("border: 2px solid red;")
        self.btn_add_image.clicked.connect(self.toggle_sidebar)
        top_bar.addWidget(self.btn_add_image)

        self.btn_other = QPushButton("🛠 Otra Herramienta")
        self.btn_other.setFixedSize(150, 50)
        self.btn_other.setStyleSheet("border: 2px solid red;")
        self.btn_other.setEnabled(False)
        top_bar.addWidget(self.btn_other)

        # 🖼 Contenido Principal (Imagen Procesada)
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel("Aquí se mostrará la imagen procesada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; padding: 10px; font-size: 16px;")
        content_layout.addWidget(self.image_label)

        # Sidebar (Deslizable)
        self.sidebar = QFrame(self)
        self.sidebar.setStyleSheet("border: 2px solid blue;")
        self.sidebar.setGeometry(-250, 50, 250, self.height())  # Inicialmente oculto
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        self.sidebar_label = QLabel("Directorio de imágenes")
        self.sidebar_label.setStyleSheet("border: 2px solid blue; padding: 10px;")
        self.sidebar_layout.addWidget(self.sidebar_label)

        # Configuración de animación
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"geometry")
        self.sidebar_animation.setDuration(300)  # Duración en milisegundos

        # Agregar layouts al Principal
        main_layout.addLayout(top_bar, 1)  # Barra superior
        main_layout.addLayout(content_layout, 9)  # Contenido principal

        # Configurar Widget Central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Manejador de Archivos
        self.file_handler = FileHandler()

        # Ajustar Tamaño de la Ventana
        screen = QApplication.primaryScreen().geometry()
        self.resize(screen.width(), screen.height())
        self.move(0, 0)

        self.sidebar_visible = False  # Estado del sidebar

    def toggle_sidebar(self):
        """ Desliza el sidebar sin afectar la imagen central """
        if self.sidebar_visible:
            self.sidebar_animation.setStartValue(QRect(0, 50, 250, self.height()))  # Posición actual
            self.sidebar_animation.setEndValue(QRect(-250, 50, 250, self.height()))  # Ocultar
        else:
            self.sidebar_animation.setStartValue(QRect(-250, 50, 250, self.height()))  # Posición oculta
            self.sidebar_animation.setEndValue(QRect(0, 50, 250, self.height()))  # Mostrar

        self.sidebar_animation.start()
        self.sidebar_visible = not self.sidebar_visible

    def load_image(self):
        """ Cargar imagen y procesarla """
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
        """ Muestra la imagen procesada en pantalla """
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setScaledContents(True)