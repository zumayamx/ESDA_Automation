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
        self.setWindowTitle("Image Editor")
        self._init_ui()
        self.file_handler = FileHandler()
        self._setup_window_size()

    def _init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._create_topbar(), 1)
        main_layout.addLayout(self._create_content_layout(), 6)
        
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_topbar(self):
        topbar_layout = QHBoxLayout()
        topbar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_add_image = QPushButton("Agregar Imagen")
        self.btn_add_image.setFixedSize(150, 150)
        self.btn_add_image.setStyleSheet("border: 2px solid red;")
        self.btn_add_image.clicked.connect(self.toggle_sidebar)
        topbar_layout.addWidget(self.btn_add_image)
        
        self.btn_other = QPushButton("Otra función")
        self.btn_other.setFixedSize(150, 150)
        self.btn_other.setStyleSheet("border: 2px solid red;")
        self.btn_other.setEnabled(False)
        topbar_layout.addWidget(self.btn_other)
        
        topbar_widget = QWidget()
        topbar_widget.setLayout(topbar_layout)
        topbar_widget.setStyleSheet("border: 1px solid red;")
        return topbar_widget

    def _create_content_layout(self):
        content_layout = QHBoxLayout()
        
        # Create and style sidebar
        self.sidebar_widget = self._create_sidebar()
        content_layout.addWidget(self.sidebar_widget, 1)
        
        # Create central content widget
        self.content_central_widget = self._create_central_content()
        content_layout.addWidget(self.content_central_widget, 6)
        
        # Create right sidebar
        self.right_sidebar_widget = self._create_right_sidebar()
        content_layout.addWidget(self.right_sidebar_widget, 1)
        
        return content_layout

    def _create_sidebar(self):
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        self.sidebar_label = QLabel("Texto del sidebar")
        self.sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sidebar_label)
        sidebar.setStyleSheet("border: 1px solid blue;")
        return sidebar

    def _create_central_content(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        
        # Image display widget
        self.image_widget = QWidget()
        image_layout = QVBoxLayout(self.image_widget)
        image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel("Aquí se mostrará la imagen procesada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; padding: 10px")
        image_layout.addWidget(self.image_label)
        self.image_widget.setStyleSheet("border: 1px solid green;")
        layout.addWidget(self.image_widget, 6)
        
        # Image array widget
        self.image_array_widget = QWidget()
        array_layout = QVBoxLayout(self.image_array_widget)
        array_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_array_label = QLabel("Aquí se mostrará la lista de imágenes cargadas")
        self.image_array_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        array_layout.addWidget(self.image_array_label)
        self.image_array_widget.setStyleSheet("border: 1px solid green;")
        layout.addWidget(self.image_array_widget, 1)
        
        central.setStyleSheet("border: 1px solid red;")
        return central

    def _create_right_sidebar(self):
        right_sidebar = QWidget()
        layout = QVBoxLayout(right_sidebar)
        self.right_sidebar_label = QLabel("Datos generales de la imagen")
        self.right_sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.right_sidebar_label)
        right_sidebar.setStyleSheet("border: 1px solid yellow;")
        return right_sidebar

    def _setup_window_size(self):
        screen = QApplication.primaryScreen().geometry()
        self.resize(screen.width() * 0.6, screen.height() * 0.6)
        self.move(
            screen.center().x() - self.width() / 2,
            screen.center().y() - self.height() / 2
        )

    def toggle_sidebar(self):
        self.sidebar_widget.setVisible(not self.sidebar_widget.isVisible())

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
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setScaledContents(True)
