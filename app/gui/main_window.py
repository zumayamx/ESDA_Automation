from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QMessageBox, QApplication, QListWidget, QListWidgetItem,
    QSizePolicy, QProgressDialog
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint
import os

from core.image_editor import ImageEditor
from core.file_handler import FileHandler
from core.image_label import ImageLabel
from core.zoom_selector import ZoomSelector

class MainWindow(QMainWindow):
    def __init__(self, general_size: int = 3024, scaled_size: int = 550):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.file_handler = FileHandler()
        self.image_editors = {}
        self.current_image_path = None
        self.original_image_size = general_size
        self.scaled_image_size = scaled_size
        self.object_space_factor = 0.5
        self.measure_space_factor = 0.3
        self.margin_space_factor = 0.2
        self.image_label = None
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
        
        # Button Labels for the top bar
        button_labels = [
            "Cargar directorio de imágenes",
            "Agregar fondo blanco y centrar",
            "Agregar medida",
            "Agregar zoom",
            "Deshacer",
            "Guardar imagen"
        ]

        self.buttons = []

        for label in button_labels:
            button = QPushButton(label)
            button.setStyleSheet("border: 2px solid red;")
            # Set expanding policy
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setFixedSize(225, 150)
            topbar_layout.addWidget(button)
            self.buttons.append(button)  # Store each button

        # Distribute space evenly among the buttons
        for i in range(len(self.buttons)):
            topbar_layout.setStretch(i, 1)
        
        # Connect the first two buttons to their actions.
        self.buttons[0].clicked.connect(self.load_folder)
        self.buttons[1].clicked.connect(self.apply_white_background)
        self.buttons[2].clicked.connect(self.activate_measure_mode)
        self.buttons[3].clicked.connect(self.activate_zoom_mode)
        self.buttons[4].clicked.connect(self.undo)
        self.buttons[5].clicked.connect(self.save_image)
        
        topbar_widget = QWidget()
        topbar_widget.setLayout(topbar_layout)
        topbar_widget.setStyleSheet("border: 1px solid red;")
        return topbar_widget

    def _create_content_layout(self):
        content_layout = QHBoxLayout()
        
        # Left Sidebar: List of images
        self.sidebar_widget = self._create_left_sidebar()
        content_layout.addWidget(self.sidebar_widget, 1)
        
        # Central Content: Display selected image
        self.content_central_widget = self._create_central_content()
        content_layout.addWidget(self.content_central_widget, 6)
        
        # Right Sidebar: Image details or additional data
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
        # When an image is clicked, display it.
        self.image_list.itemClicked.connect(lambda item: self.display_image(item.data(Qt.ItemDataRole.UserRole)))
        layout.addWidget(self.image_list)
        self.load_image_list()

        left_sidebar.setStyleSheet("border: 1px solid blue;")
        return left_sidebar
    
    def load_image_list(self):
        """Load all .jpg images from the FileHandler."""
        self.image_list.clear()
        self.image_editors.clear()

        images = self.file_handler.load_image_list()
        if images:
            for image_path in images:
                item = QListWidgetItem(os.path.basename(image_path))
                item.setData(Qt.ItemDataRole.UserRole, image_path)
                self.image_list.addItem(item)
                # Create and store an ImageEditor instance for each image.
                self.image_editors[image_path] = ImageEditor(image_path, self.original_image_size, self.object_space_factor, self.measure_space_factor, self.margin_space_factor)
        else:
            self.image_list.addItem("No hay imágenes cargadas")

    def _create_central_content(self):
        """
        Crea y devuelve el panel central que muestra la imagen seleccionada.
        """
        # Panel principal para la imagen
        imagePanel = QWidget()
        imagePanel.setStyleSheet("border: 1px solid red;")
        
        # Un solo layout para organizar el contenido
        panelLayout = QVBoxLayout(imagePanel)
        panelLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Crear y configurar la etiqueta de imagen
        self.image_label = ImageLabel("Aquí se muestra la imagen seleccionada")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(self.scaled_image_size, self.scaled_image_size)
        
        # Añadir la etiqueta directamente al layout
        panelLayout.addWidget(self.image_label)
        
        return imagePanel

    def _create_right_sidebar(self):
        right_sidebar = QWidget()
        layout = QVBoxLayout(right_sidebar)
        self.right_sidebar_label = QLabel("Datos generales de la imagen")
        self.right_sidebar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.right_sidebar_label)
        right_sidebar.setStyleSheet("border: 1px solid yellow;")
        return right_sidebar

    def _setup_window_size(self):
        self.showMaximized()

    def load_folder(self):
        folder_path = self.file_handler.load_folder()
        if folder_path:
            try:
                QMessageBox.information(self, "Éxito", f"Directorio cargado: {folder_path}")
                self.load_image_list()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el directorio: {str(e)}")
    
    def apply_white_background(self):
        """Apply white background transformation and update UI."""
        if not self.current_image_path:
            QMessageBox.warning(self, "Sin selección", "Selecciona una imagen primero.")
            return
        
        editor = self.image_editors.get(self.current_image_path)
        if editor:
            progress_dialog = QProgressDialog("Aplicando fondo blanco...", None, 0, 0, self)
            progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            progress_dialog.setCancelButton(None)
            progress_dialog.show()
            QApplication.processEvents()
            editor.apply_white_background()
            progress_dialog.close()
            # Update the display immediately after transformation.
            self.display_image(self.current_image_path)
        else:
            QMessageBox.warning(self, "Error", "No se encontró un editor para la imagen seleccionada.")
    
    def activate_measure_mode(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Sin selección", "Selecciona una imagen primero.")
            return
        self.image_label.set_measure_mode(True)
        self.image_label.measure_callback = self.measure_line_callback
    
    def measure_line_callback(self, start_point, end_point):

        scale_factor = (self.original_image_size * self.object_space_factor + self.original_image_size * self.measure_space_factor) / self.scaled_image_size
        print("Scale factor:", scale_factor)

        # Calculate the poitns in the image with the scale factor
        start_point = (start_point.x() * scale_factor, start_point.y() * scale_factor)
        end_point = (end_point.x() * scale_factor, end_point.y() * scale_factor)

        print("Scaled start point:", start_point)
        print("Scaled end point:", end_point)

        editor = self.image_editors.get(self.current_image_path)
        if editor:
            editor.apply_measure_line(start_point, end_point)
            self.display_image(self.current_image_path)
        else:
            QMessageBox.warning(self, "Error", "No se encontró un editor para la imagen seleccion")
    
    def activate_zoom_mode(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Sin selección", "Selecciona una imagen primero.")
            return
        
        print("Setting cursor to cross")
        self.image_label.setCursor(Qt.CrossCursor)
        self.zoom_selector = ZoomSelector(self.image_label)
        self.zoom_selector.zoomSelected.connect(self.zoom_area_callback)
        self.zoom_selector.show()
    
    def zoom_area_callback(self, center: tuple, radius: int):

        scale_factor = (self.original_image_size * self.object_space_factor + self.original_image_size * self.measure_space_factor) / self.scaled_image_size
        print("Scale factor:", scale_factor)
        self.zoom_center = (int(center.x() * scale_factor), int(center.y() * scale_factor))
        self.zoom_radius = int(radius * scale_factor)

        QMessageBox.information(self, "Zoom", f"Area de zoom definida en el centro {center} y radio {radius}")

        self.image_label.setCursor(Qt.CrossCursor)
        self.reference = self.image_label.mousePressEvent
        self.image_label.mousePressEvent = self.zoom_target_mousePressEvent
    
    def zoom_target_mousePressEvent(self, event):
        scale_factor = (self.original_image_size * self.object_space_factor + self.original_image_size * self.measure_space_factor) / self.scaled_image_size
        print("Scale factor:", scale_factor)
        target_point = (int(event.pos().x() * scale_factor), int(event.pos().y() * scale_factor))
        print("Target point:", target_point)

        editor = self.image_editors.get(self.current_image_path)
        if editor:
            print("Arguments for apply_zoom:", self.zoom_center, self.zoom_radius, target_point)
            editor.apply_zoom(self.zoom_center, self.zoom_radius, target_point)
            self.display_image(self.current_image_path)
            print("Zoom applied")
        else:
            QMessageBox.warning(self, "Error", "No se encontró un editor para la imagen seleccionada.")
        
        # Reset the mousePressEvent to the default behavior.
        self.image_label.mousePressEvent = self.reference
        self.image_label.setCursor(Qt.ArrowCursor)
        

    def display_image(self, image_path):
        # Set the active image path.
        self.current_image_path = image_path

        editor = self.image_editors.get(image_path, None)
        if not editor:
            QMessageBox.critical(self, "Error", "Debe cargar un directorio de imágenes primero.")
            return
        
        pixmap = QPixmap(editor.image_qt)
        scaled_pixmap = pixmap.scaled(
            self.scaled_image_size, 
            self.scaled_image_size,
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled_pixmap)

    def undo(self):
        editor = self.image_editors.get(self.current_image_path)
        if editor:
            editor.undo()
            self.display_image(self.current_image_path)
        else:
            QMessageBox.warning(self, "Error", "No se encontró un editor para la imagen seleccionada.")
    
    def save_image(self):
        editor = self.image_editors.get(self.current_image_path)
        if editor:
            editor.save(self.file_handler.output_dir)
            QMessageBox.information(self, "Éxito", "Imagen guardada correctamente.")
        else:
            QMessageBox.warning(self, "Error", "No se encontró un editor para la imagen seleccionada.")