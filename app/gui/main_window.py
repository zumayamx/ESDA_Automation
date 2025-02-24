from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QMessageBox, QApplication, QListWidget, QListWidgetItem,
    QSizePolicy
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.image_editor import ImageEditor
from core.file_handler import FileHandler
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_handler = FileHandler()
        self.setWindowTitle("Image Editor")
        self._init_ui()
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
        
        # Button Labels
        button_labels = [
            "Cargar directorio de imágenes",
            "Agregar fondo blanco y centrar",
            "Agregar medida",
            "Agregar zoom",
            "Deshacer",
            "Guardar imagen"
        ]

        # Button References (for access later if needed)
        self.buttons = []

        for label in button_labels:
            button = QPushButton(label)
            button.setStyleSheet("border: 2px solid red;")

            # Set expanding policy
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            button.setFixedSize(225, 150)
            
            topbar_layout.addWidget(button)
            self.buttons.append(button)  # Store buttons in a list

        # Ensure each button gets an equal portion of the width
        for i in range(len(self.buttons)):
            topbar_layout.setStretch(i, 1)
        
        self.buttons[0].clicked.connect(self.load_folder)
        # self.buttons[1].clicked.connect(self.load_image)

        # Wrap layout in a widget
        topbar_widget = QWidget()
        topbar_widget.setLayout(topbar_layout)
        topbar_widget.setStyleSheet("border: 1px solid red;")
        
        return topbar_widget

    def _create_content_layout(self):
        content_layout = QHBoxLayout()
        
        # Create and style left_sidebar
        self.sidebar_widget = self._create_left_sidebar()
        content_layout.addWidget(self.sidebar_widget, 1)
        
        # Create central content widget
        self.content_central_widget = self._create_central_content()
        content_layout.addWidget(self.content_central_widget, 6)
        
        # Create right left_sidebar
        self.right_sidebar_widget = self._create_right_sidebar()
        content_layout.addWidget(self.right_sidebar_widget, 1)
        
        return content_layout

    def _create_left_sidebar(self):
        left_sidebar = QWidget()
        layout = QVBoxLayout(left_sidebar)
        self.sidebar_label = QLabel("Lista de imágenes en el directorio")
        self.sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sidebar_label)

        self.image_list = QListWidget()
        self.image_list.setStyleSheet("border: 1px solid gray;")
        self.image_list.itemClicked.connect(lambda item: self.display_image(item.data(Qt.ItemDataRole.UserRole)))
        layout.addWidget(self.image_list)
        self.load_image_list()

        left_sidebar.setStyleSheet("border: 1px solid blue;")
        return left_sidebar
    
    def load_image_list(self):
        """Load all .jpg images from the FileHandler"""
        self.image_list.clear()
        images = self.file_handler.load_image_list()
        if images:
            for image_path in images:
                item = QListWidgetItem(os.path.basename(image_path))
                item.setData(Qt.ItemDataRole.UserRole, image_path)
                self.image_list.addItem(item)
        else:
            self.image_list.addItem("No hay imágenes cargadas")

    def _create_central_content(self):
        image_widget = QWidget()
        layout = QVBoxLayout(image_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel("Aquí se mostrará la imagen seleccionada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed gray; padding: 10px")
        layout.addWidget(self.image_label)
        image_widget.setStyleSheet("border: 1px solid green;")
        return image_widget

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

    def load_folder(self):
        folder_path = self.file_handler.load_folder()
        if folder_path:
            try:
                QMessageBox.information(self, "Éxito", f"Directorio cargado: {folder_path}")
                self.load_image_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el directorio: {str(e)}")

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label.setScaledContents(True)

    # def _create_topbar(self):
    #     topbar_layout = QHBoxLayout()
    #     topbar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    #     self.btn_add_image = QPushButton("Cargar directorio de imágenes")
    #     self.btn_add_image.setFixedSize(150, 150)
    #     self.btn_add_image.setStyleSheet("border: 2px solid red;")
    #     self.btn_add_image.clicked.connect(self.toggle_sidebar)
    #     topbar_layout.addWidget(self.btn_add_image)
        
    #     self.btn_remove_bg_center = QPushButton("Agregar fondo blanco y centrar")
    #     self.btn_remove_bg_center.setFixedSize(150, 150)
    #     self.btn_remove_bg_center.setStyleSheet("border: 2px solid red;")
    #     self.btn_remove_bg_center.setEnabled(False)
    #     topbar_layout.addWidget(self.btn_remove_bg_center)

    #     self.btn_add_measurement = QPushButton("Agregar medida")
    #     self.btn_add_measurement.setFixedSize(150, 150)
    #     self.btn_add_measurement.setStyleSheet("border: 2px solid red;")
    #     self.btn_add_measurement.setEnabled(False)
    #     topbar_layout.addWidget(self.btn_add_measurement)

    #     self.btn_add_zoom = QPushButton("Agregar zoom")
    #     self.btn_add_zoom.setFixedSize(150, 150)
    #     self.btn_add_zoom.setStyleSheet("border: 2px solid red;")
    #     self.btn_add_zoom.setEnabled(False)
    #     topbar_layout.addWidget(self.btn_add_zoom)

    #     self.btn_save_image = QPushButton("Guardar imagen")
    #     self.btn_save_image.setFixedSize(150, 150)
    #     self.btn_save_image.setStyleSheet("border: 2px solid red;")
    #     self.btn_save_image.setEnabled(False)
    #     topbar_layout.addWidget(self.btn_save_image)
        
    #     topbar_widget = QWidget()
    #     topbar_widget.setLayout(topbar_layout)
    #     topbar_widget.setStyleSheet("border: 1px solid red;")
    #     return topbar_widget

        # def load_image(self):
    #     """ Cargar imagen y procesarla """
    #     file_path = self.file_handler.select_image(self)
    #     if file_path:
    #         try:
    #             editor = ImageEditor(file_path)
    #             editor.add_white_background()
    #             QMessageBox.information(self, "Éxito", "Imagen procesada y guardada en /images/")

    #             # Mostrar la imagen procesada
    #             processed_image_path = os.path.join(self.file_handler.output_dir, "object_with_white_bg.png")
    #             if os.path.exists(processed_image_path):
    #                 self.display_image(processed_image_path)
    #             else:
    #                 QMessageBox.warning(self, "Advertencia", "La imagen procesada no se encontró.")
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", f"No se pudo procesar la imagen: {str(e)}")