from interfaces.registro import Registrarse
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt

class VentanaPrincipal(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle('Menú Principal')  
        self.resize(600, 400)  

        # vertical 
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Titulo
        titulo = QLabel("Menú Principal", self)
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setWordWrap(True)  # salto de línea
        
        fuente = titulo.font()
        fuente.setPointSize(16)
        fuente.setBold(True)
        titulo.setFont(fuente)

        # Botones 
        self.cuentas = QPushButton("Ver cuentas")
        self.depositar = QPushButton("Depositar")
        self.transferir = QPushButton("Transferir")
        self.retirar = QPushButton("Retirar")
        self.salir = QPushButton("Salir")
        
        self.cuentas.setMinimumHeight(40)
        self.depositar.setMinimumHeight(40)
        self.transferir.setMinimumHeight(40)
        self.retirar.setMinimumHeight(40)
        self.salir.setMinimumHeight(40)


        # Agregamos widgets al layout
        layout.addWidget(titulo)
        
        layout.addWidget(self.cuentas)
        #self.inicio.clicked.connect(self.)
        
        layout.addWidget(self.depositar)
        #self.registro.clicked.connect(self.)

        layout.addWidget(self.transferir)
        #self.registro.clicked.connect(self.)

        layout.addWidget(self.retirar)
        #self.registro.clicked.connect(self.)

        
        
        layout.addWidget(self.salir)
        self.salir.clicked.connect(self.close) #Agregar: QMessageBox.


        
        self.show()

        