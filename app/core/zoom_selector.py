from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainter, QPen
import math

class ZoomSelector(QWidget):
    # Signal emitted when the zoom area is selected:
    # Emits the center (QPoint) and the radius (int)
    zoomSelected = Signal(tuple, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.start_point = None
        self.current_point = None
        self.selecting = False
        # Ensure the widget covers its parent completely.
        self.resize(parent.size())
    
    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.current_point = event.pos()
        self.selecting = True
        self.update()
    
    def mouseMoveEvent(self, event):
        if self.selecting:
            self.current_point = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        if self.selecting:
            self.current_point = event.pos()
            self.selecting = False
            dx = self.current_point.x() - self.start_point.x()
            dy = self.current_point.y() - self.start_point.y()
            radius = int(math.hypot(dx, dy))
            self.zoomSelected.emit(self.start_point, radius)
            self.hide()  # Hide the overlay after selection.
            self.update()
    
    def paintEvent(self, event):
        if self.selecting and self.start_point and self.current_point:
            painter = QPainter(self)
            pen = QPen(Qt.blue, 2, Qt.DashLine)
            painter.setPen(pen)
            dx = self.current_point.x() - self.start_point.x()
            dy = self.current_point.y() - self.start_point.y()
            radius = int(math.hypot(dx, dy))
            painter.drawEllipse(self.start_point, radius, radius)