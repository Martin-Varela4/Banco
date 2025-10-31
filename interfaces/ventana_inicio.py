import sys

from inicio import InicioSesion
from registro import Registrarse
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt

class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bienvenida al Banco')  
        self.resize(600, 400)  

        # vertical 
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Titulo
        titulo = QLabel("Bienvenido/a, ¿qué desea realizar?", self)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)  # salto de línea
        
        fuente = titulo.font()
        fuente.setPointSize(16)
        fuente.setBold(True)
        titulo.setFont(fuente)

        # Botones 
        self.inicio = QPushButton("Iniciar sesión")
        self.registro = QPushButton("Registrarse")
        self.boton_salir = QPushButton("Salir")
        
        self.inicio.setMinimumHeight(40)
        self.registro.setMinimumHeight(40)
        self.boton_salir.setMinimumHeight(40)


        # Agregamos widgets al layout
        layout.addWidget(titulo)
        

        
        layout.addWidget(self.inicio)
        self.inicio.clicked.connect(self.abrir_login)
        
        layout.addWidget(self.registro)
        self.registro.clicked.connect(self.abrir_registro)
        
        
        layout.addWidget(self.boton_salir)
        self.boton_salir.clicked.connect(self.close) #Agregar: QMessageBox.warning
        
        self.show()
        
        
    def abrir_login(self):
        self.ventana_login = InicioSesion()
        self.ventana_login.show()
        
    
    def abrir_registro(self):
        self.ventana_login = Registrarse()
        self.ventana_login.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VentanaInicial()
    sys.exit(app.exec())