from PySide6.QtWidgets import *
from interfaces.principal import VentanaPrincipal
import sys
import base_datos as bd
import sqlite3
from PySide6.QtCore import Qt

#INICIO DE SESION DE 'EMPLEADO'  

class InicioSesion(QDialog):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle("Inicio de Sesión - Empleado")
        self.resize(400, 300)
        self.setModal(True)
        
        layout_principal = QVBoxLayout(self)
        
        titulo = QLabel("Iniciar sesión")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #007BFF;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo) 
        layout_principal.addSpacing(15)
        
    
        self.form_layout = QGridLayout()
        
        #
        self.form_layout.addWidget(QLabel("<b>Usuario:</b>"), 0, 0)
        self.usuario = QLineEdit() 
        self.usuario.setPlaceholderText("Ej: admin")
        self.form_layout.addWidget(self.usuario, 0, 1)

        self.form_layout.addWidget(QLabel("<b>Contraseña:</b>"), 1, 0)
        

        self.contrasena = QLineEdit() 
        self.contrasena.setEchoMode(QLineEdit.Password)
        self.contrasena.setPlaceholderText("Ingrese contraseña")
        self.form_layout.addWidget(self.contrasena, 1, 1)
        
        layout_principal.addLayout(self.form_layout)
        

        botones_layout = QHBoxLayout()
        
        btn_iniciar = QPushButton("Iniciar Sesión")
        btn_iniciar.setStyleSheet("background-color: #28A745; color: white; font-weight: bold;")
        btn_iniciar.clicked.connect(self.procesar_login)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #DC3545; color: white;")
        btn_cancelar.clicked.connect(self.reject) 
        
        botones_layout.addWidget(btn_iniciar)
        botones_layout.addWidget(btn_cancelar)

        layout_principal.addStretch()
        layout_principal.addLayout(botones_layout)
        

        self.usuario.setFocus()
        
        
    def procesar_login(self):
        user = self.usuario.text().strip()
        password = self.contrasena.text()

        if not user or not password:
            QMessageBox.warning(self, "Error", "Debe completar ambos campos.")
            return

        try:
    
            nombre_empleado, rol_empleado = bd.verificar_login(user, password) 
            
  
            QMessageBox.information(self, "Acceso", f"Bienvenido/a, {nombre_empleado} ({rol_empleado}).")
            
         
            self.abrir_menu_banco(nombre_empleado, rol_empleado)
            self.accept() 
            
        except ValueError as e:
            QMessageBox.critical(self, "Acceso Denegado", str(e))
            self.contrasena.clear() 
            self.contrasena.setFocus()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error de DB", f"Fallo la conexión o consulta: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")

    
    def abrir_menu_banco(self, nombre_empleado, rol_empleado):
        self.ventana_principal = VentanaPrincipal(nombre_empleado=nombre_empleado, rol=rol_empleado)
        self.ventana_principal.show()
            
        