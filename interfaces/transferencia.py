from PySide6.QtWidgets import *
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import base_datos as bd 
import sqlite3


class VentanaTransferencia(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Realizar Transferencia")
        self.setModal(True)
        self.resize(400, 200)

        layout_principal = QVBoxLayout(self)
        
        titulo = QLabel("Transferencia de Fondos")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(10)

        # form
    
        layout_origen = QHBoxLayout()
        layout_origen.addWidget(QLabel("<b>Cta. Origen (ID):</b>"))
        self.txt_origen = QLineEdit()
        self.txt_origen.setPlaceholderText("ID de la cuenta que envía")
        layout_origen.addWidget(self.txt_origen)
        
       
        layout_destino = QHBoxLayout()
        layout_destino.addWidget(QLabel("<b>Cta. Destino (ID):</b>"))
        self.txt_destino = QLineEdit()
        self.txt_destino.setPlaceholderText("ID de la cuenta que recibe")
        layout_destino.addWidget(self.txt_destino)
        
     
        layout_monto = QHBoxLayout()
        layout_monto.addWidget(QLabel("<b>Monto:</b>"))
        self.txt_monto = QLineEdit()
        self.txt_monto.setPlaceholderText("Monto a transferir")
        layout_monto.addWidget(self.txt_monto)

        layout_principal.addLayout(layout_origen)
        layout_principal.addLayout(layout_destino)
        layout_principal.addLayout(layout_monto)
        layout_principal.addStretch()

       
        btn_aceptar = QPushButton("Transferir")
        btn_aceptar.setStyleSheet("background-color: #004D40; color: white; font-weight: bold;")
        btn_aceptar.clicked.connect(self.procesar_transferencia)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #CC0000; color: white; font-weight: bold;")
        btn_cancelar.clicked.connect(self.reject)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(btn_aceptar)
        botones_layout.addWidget(btn_cancelar)
        layout_principal.addLayout(botones_layout)

    def procesar_transferencia(self):
        id_origen = self.txt_origen.text().strip()
        id_destino = self.txt_destino.text().strip()
        monto_str = self.txt_monto.text().replace(',', '.').strip()

    
        if not id_origen or not id_destino or not monto_str:
            QMessageBox.warning(self, "Error", "Debe completar todos los campos.")
            return

        if id_origen == id_destino:
            QMessageBox.critical(self, "Error", "La cuenta de origen y destino no pueden ser la misma.")
            return

        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Error de Monto", "El monto debe ser un número positivo válido.")
            return

        try:
            bd.ejecutar_transferencia(id_origen, id_destino, monto)
            
            QMessageBox.information(self, "Éxito", f"Transferencia de ${monto:.2f} realizada de {id_origen} a {id_destino}.")
            self.accept()
            
        except ValueError as e:
            QMessageBox.critical(self, "Error de Operación", str(e))
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error de DB", f"Fallo de la base de datos: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error Fatal", f"Ocurrió un error inesperado: {e}")