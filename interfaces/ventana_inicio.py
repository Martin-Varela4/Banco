import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt

class Ventana(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bienvenida al Banco')  
        self.resize(600, 400)  

        # Layout vertical (texto arriba, botones abajo)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Texto principal
        titulo = QLabel("Bienvenido/a, ¿qué desea realizar?", self)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)  # salto de línea
        
        fuente = titulo.font()
        fuente.setPointSize(16)
        fuente.setBold(True)
        titulo.setFont(fuente)

        # Botones (opcional, para probar)
        boton_login = QPushButton("Iniciar sesión")
        boton_registro = QPushButton("Registrarse")
        boton_salir = QPushButton("Salir")
        
        boton_login.setMinimumHeight(50)
        boton_registro.setMinimumHeight(50)
        boton_salir.setMinimumHeight(50)

        # Agregamos widgets al layout
        layout.addWidget(titulo)
        layout.addWidget(boton_login)
        layout.addWidget(boton_registro)
        layout.addWidget(boton_salir)
        

        # Mostramos
        self.show()
        
        self.establecer_conexiones(self)
        
        
    def establecer_conexiones(self):
        self.boton_salir.clicked.connect(self.close)
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ventana()
    sys.exit(app.exec())