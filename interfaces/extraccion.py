from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import base_datos as bd 
import sqlite3

class VentanaExtraccion(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Realizar Extracción")
        self.setModal(True)
        self.resize(350, 150)

        layout_principal = QVBoxLayout(self)
        
     
        titulo = QLabel("Extracción")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(10)

        
        
        layout_cuenta = QHBoxLayout()
        layout_cuenta.addWidget(QLabel("<b>ID Cuenta:</b>"))
        self.txt_cuenta = QLineEdit()
        self.txt_cuenta.setPlaceholderText("Ingrese ID de Cuenta")
        layout_cuenta.addWidget(self.txt_cuenta)
        
       
        layout_monto = QHBoxLayout()
        layout_monto.addWidget(QLabel("<b>Monto (€/$/USD):</b>"))
        self.txt_monto = QLineEdit()
        self.txt_monto.setPlaceholderText("Monto a extraer")
        layout_monto.addWidget(self.txt_monto)

        layout_principal.addLayout(layout_cuenta)
        layout_principal.addLayout(layout_monto)
        layout_principal.addStretch() # Empuja los elementos hacia arriba

        
        btn_aceptar = QPushButton("Extraer")
        btn_aceptar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
        btn_aceptar.clicked.connect(self.procesar_extraccion)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #CC0000; color: white; font-weight: bold;")
        btn_cancelar.clicked.connect(self.reject)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(btn_aceptar)
        botones_layout.addWidget(btn_cancelar)
        layout_principal.addLayout(botones_layout)

    
    def procesar_extraccion(self):
        id_cuenta = self.txt_cuenta.text().strip()
        monto_str = self.txt_monto.text().replace(',', '.').strip()

    
        if not id_cuenta or not monto_str:
            QMessageBox.warning(self, "Error", "Debe ingresar el ID de cuenta y el monto.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error de Monto", "El monto debe ser un número positivo válido.")
            return

      
        try:
           
            nuevo_saldo, dni_cliente, nombre_cliente = bd.ejecutar_extraccion(id_cuenta, monto)
            
            QMessageBox.information(
                self, 
                "Extracción Exitosa", 
                f"Se extrajeron ${monto:.2f} de la cuenta {id_cuenta}.\n"
                f"Titular: {nombre_cliente} (DNI: {dni_cliente})\n"
                f"Nuevo Saldo: ${nuevo_saldo:.2f}"
            )
            self.accept()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error de Operación", str(e))
        except RuntimeError as e:
            QMessageBox.critical(self, "Error de Base de Datos", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")