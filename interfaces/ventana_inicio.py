import sys

from interfaces.inicio import InicioSesion
from interfaces.registro import Registrarse
from interfaces.principal import VentanaPrincipal
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class VentanaInicial(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

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
        self.boton_salir.clicked.connect(self.confirmar_salida)

        
        self.show()
        
        
    def abrir_login(self):
        self.ventana_login = InicioSesion()
        self.ventana_login.show()
        
    
    def abrir_registro(self):
        self.ventana_login = Registrarse()
        self.ventana_login.show()

    def confirmar_salida(self):
        
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "¿Desea salir?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            QMessageBox.information(self, "Salir", "Gracias por usar el banco. ¡Hasta luego!")
            self.close()

    def abrir_principal(self):
        self.ventana_principal = VentanaPrincipal()
        self.ventana_principal.show()
        
