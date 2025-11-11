from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import base_datos as bd
import sqlite3

class VentanaDeposito(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Realizar Depósito")
        self.resize(350, 200)
        self.setModal(True) 
        

        layout_principal = QVBoxLayout(self)
        
       
        titulo = QLabel("Depósito en Cuenta")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(10)

   
        form_layout = QGridLayout()
        
    
        form_layout.addWidget(QLabel("<b>N° Cuenta Destino:</b>"), 0, 0)
        self.txt_cuenta = QLineEdit()
        form_layout.addWidget(self.txt_cuenta, 0, 1)

   
        form_layout.addWidget(QLabel("<b>Monto a Depositar:</b>"), 1, 0)
        self.txt_monto = QLineEdit()
        form_layout.addWidget(self.txt_monto, 1, 1)
        
        layout_principal.addLayout(form_layout)
        layout_principal.addStretch() # espaciador para centrar 


        botones_layout = QHBoxLayout()
        
        btn_depositar = QPushButton("Confirmar Depósito")
        btn_depositar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
        btn_depositar.clicked.connect(self.procesar_deposito)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #CC0000; color: white;")
        btn_cancelar.clicked.connect(self.reject) 
        
        botones_layout.addWidget(btn_depositar)
        botones_layout.addWidget(btn_cancelar)
        layout_principal.addLayout(botones_layout)


    
    def procesar_deposito(self):
        cuenta = self.txt_cuenta.text().strip()
        monto_str = self.txt_monto.text().replace(',', '.').strip()

   
        if not cuenta or not monto_str:
            QMessageBox.warning(self, "Error", "Debe ingresar el número de cuenta y el monto.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error de Monto", "El monto debe ser un número positivo válido.")
            return

        try:
 
            bd.ejecutar_deposito(cuenta, monto)

            QMessageBox.information(self, "Éxito", f"Se depositaron ${monto:.2f} en la cuenta {cuenta}.")

            self.accept() 
            
        except ValueError as e:
            QMessageBox.critical(self, "Error de Operación", str(e))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error de DB", f"Fallo de la base de datos: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error Fatal", f"Ocurrió un error inesperado: {e}")
        


