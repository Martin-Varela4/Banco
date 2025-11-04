from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QLineEdit, QDialog, QGridLayout, QHBoxLayout
from banco import Banco

class Registrarse(QDialog): #del boton registrarse
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Registrar")
        self.resize(400, 300)
        self.setModal(True)
        # self.banco = banco
        
        
        layout_principal = QVBoxLayout(self)
        self.setLayout(layout_principal)

        titulo = QLabel("Registrarse")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout_principal.addWidget(titulo)    
        
    
        form_layout = QGridLayout()
        
        
        form_layout.addWidget(QLabel("<b>Nombre:</b>"), 1, 0)
        form_layout.addWidget(QLineEdit(), 1, 1)


        form_layout.addWidget(QLabel("<b>Apellido:</b>"), 2, 0)
        form_layout.addWidget(QLineEdit(), 2, 1)
        
        form_layout.addWidget(QLabel("<b>Contraseña:</b>"), 3, 0)
        form_layout.addWidget(QLineEdit(), 3, 1)
    

        form_layout.addWidget(QLabel("<b>DNI/ID:</b>"), 4, 0)
        form_layout.addWidget(QLineEdit(), 4, 1)
        
        
        layout_principal.addLayout(form_layout)
        
        botones_layout = QHBoxLayout()
        btn_registrar = QPushButton("Registrar")
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.close)
        
        botones_layout.addWidget(btn_registrar)
        botones_layout.addWidget(btn_cancelar)

        # Agregar botones al layout principal
        layout_principal.addStretch()
        layout_principal.addLayout(botones_layout)
        
        
    def registrar(self, nombre, apellido, contraseña, dni):
        pass
        
     
