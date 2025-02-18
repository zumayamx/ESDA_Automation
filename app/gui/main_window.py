from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.setGeometry(300, 200, 800, 600)

        layout = QVBoxLayout()
        label = QLabel("Bienvenido al editor de fotos de productos")
        label.setStyleSheet("font-size: 20px; padding: 20px")
        layout.addWidget(label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()