from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QLineEdit, QDialog, QGridLayout, QHBoxLayout

class Registrarse(QDialog): #del boton registrarse
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Inicio de Sesión")
        self.resize(400, 300)
        self.setModal(True)
        
        
        layout_principal = QVBoxLayout(self)
        self.setLayout(layout_principal)
        

        titulo = QLabel("Registrarse")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout_principal.addWidget(titulo)    
        
        
        form_layout = QGridLayout()
        
    
        
        form_layout.addWidget(QLabel("<b>Nombre:</b>"), 0, 0)
        form_layout.addWidget(QLineEdit(), 0, 1)


        form_layout.addWidget(QLabel("<b>Apellido:</b>"), 1, 0)
        form_layout.addWidget(QLineEdit(), 1, 1)
        

        form_layout.addWidget(QLabel("<b>DNI/ID:</b>"), 2, 0)
        form_layout.addWidget(QLineEdit(), 2, 1)
        
        
        layout_principal.addLayout(form_layout)
        
        botones_layout = QHBoxLayout()
        btn_registrar = QPushButton("Registrar")
        btn_cancelar = QPushButton("Cancelar")
        botones_layout.addWidget(btn_registrar)
        botones_layout.addWidget(btn_cancelar)

        # Agregar botones al layout principal
        layout_principal.addStretch()
        layout_principal.addLayout(botones_layout)
     
