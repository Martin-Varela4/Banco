import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PySide6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Login Form')

        # Crear un layout en cuadrícula
        layout = QGridLayout()
        self.setLayout(layout)

        # Campo de usuario
        layout.addWidget(QLabel('Username:'), 0, 0)
        layout.addWidget(QLineEdit(), 0, 1)

        # Campo de contraseña
        layout.addWidget(QLabel('Password:'), 1, 0)
        layout.addWidget(QLineEdit(echoMode=QLineEdit.EchoMode.Password), 1, 1)

        # Botones
        layout.addWidget(QPushButton('Log in'), 2, 0, alignment=Qt.AlignRight)
        layout.addWidget(QPushButton('Close'), 2, 1, alignment=Qt.AlignRight)

        # Mostrar ventana
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())