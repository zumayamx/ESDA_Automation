from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QPoint

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.measure_mode = False
        self.measuring = False
        self.start_point = None
        self.current_point = None
        self.measure_callback = None
        self.setFocusPolicy(Qt.StrongFocus)

    def set_measure_mode(self, mode: bool):
        self.measure_mode = mode
        if mode:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        self.measuring = False
        self.start_point = None
        self.current_point = None
        self.update()

    def mousePressEvent(self, event):
        if self.measure_mode:
            self.measuring = True
            self.start_point = event.pos()
            self.current_point = event.pos()
            self.update()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.measure_mode and self.measuring:
            self.current_point = event.pos()
            self.update()  # Redraw to update the line
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.measure_mode and self.measuring:
            self.measuring = False
            end_point = self.current_point
            # Call the callback to process the measurement.
            if self.measure_callback:
                self.measure_callback(self.start_point, end_point)
            # Exit measure mode.
            self.set_measure_mode(False)
            self.update()
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if self.measure_mode and self.measuring and self.start_point:
            key = event.key()
            if key == Qt.Key_Space:
                # Snap to nearest axis: horizontal if dx > dy, otherwise vertical.
                dx = abs(self.current_point.x() - self.start_point.x())
                dy = abs(self.current_point.y() - self.start_point.y())
                if dx > dy:
                    self.current_point = QPoint(self.current_point.x(), self.start_point.y())
                else:
                    self.current_point = QPoint(self.start_point.x(), self.current_point.y())
                self.update()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.measure_mode and self.measuring and self.start_point and self.current_point:
            painter = QPainter(self)
            pen = QPen(Qt.black, 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawLine(self.start_point, self.current_point)
