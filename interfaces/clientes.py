import sqlite3 
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

import base_datos as bd


class VentanaClientes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CRUD de Clientes")
        self.resize(550, 450)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)
        
        
        titulo = QLabel("Gestión de Clientes")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #004D40;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(15)

        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("<b>Seleccione Operación:</b>"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Agregar cliente", "Actualizar cliente", "Eliminar cliente"])
        self.combo_tipo.currentIndexChanged.connect(self.cambiar_operacion)
        combo_layout.addWidget(self.combo_tipo)
        layout_principal.addLayout(combo_layout)
        layout_principal.addSpacing(20) 

        
        self.form_layout = QGridLayout()
        layout_principal.addLayout(self.form_layout)

        
        self.form_layout.addWidget(QLabel("DNI:"), 0, 0)
        self.dni = QLineEdit()
        self.form_layout.addWidget(self.dni, 0, 1)

        self.form_layout.addWidget(QLabel("Nombre:"), 1, 0)
        self.nombre = QLineEdit()
        self.form_layout.addWidget(self.nombre, 1, 1)

        self.form_layout.addWidget(QLabel("Apellido:"), 2, 0)
        self.apellido = QLineEdit()
        self.form_layout.addWidget(self.apellido, 2, 1)
        
        self.form_layout.addWidget(QLabel("Contraseña:"), 3, 0)
        self.contrasena = QLineEdit()
        self.contrasena.setEchoMode(QLineEdit.Password)
        self.form_layout.addWidget(self.contrasena, 3, 1) 

        self.form_layout.addWidget(QLabel("Teléfono:"), 4, 0)
        self.telefono = QLineEdit()
        self.form_layout.addWidget(self.telefono, 4, 1)

        self.form_layout.addWidget(QLabel("Dirección:"), 5, 0)
        self.direccion = QLineEdit()
        self.form_layout.addWidget(self.direccion, 5, 1)

        layout_principal.addStretch() 
        
        
        
        botones_layout = QHBoxLayout()
        self.btn_aceptar = QPushButton("Aceptar")
        self.btn_aceptar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
        self.btn_aceptar.clicked.connect(self.realizar_operacion)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #CC0000; color: white; font-weight: bold;")
        btn_cancelar.clicked.connect(self.reject) 

        botones_layout.addWidget(self.btn_aceptar)
        botones_layout.addWidget(btn_cancelar)
        layout_principal.addLayout(botones_layout)

        self.cambiar_operacion(0) 

    
    def obtener_widgets_por_fila(self, fila_inicio, fila_fin):
        widgets = []
        for fila in range(fila_inicio, fila_fin + 1):
            label_item = self.form_layout.itemAtPosition(fila, 0)
            line_edit_item = self.form_layout.itemAtPosition(fila, 1)
            
            if label_item and line_edit_item:
                widgets.extend([label_item.widget(), line_edit_item.widget()])
        return widgets

    def cambiar_operacion(self, index):

        todos_los_campos = self.obtener_widgets_por_fila(1, 5) # fila 1 a 5
        for w in todos_los_campos:
             w.hide()
             
        # Limpiar todos los campos
        for w in [self.dni, self.nombre, self.apellido, self.contrasena, self.telefono, self.direccion]:
             w.clear()
             
        campos_completos = self.obtener_widgets_por_fila(1, 5)

        if index == 0:  
             self.setWindowTitle("AGREGAR")
             self.btn_aceptar.setText("Registrar")
             self.dni.setEnabled(True)
             for w in campos_completos: w.show()

        if index == 1:  # Actualizar
            self.setWindowTitle("ACTUALIZAR")
            self.btn_aceptar.setText("Buscar / Guardar") 
            self.dni.setEnabled(True) 
           
            campos_completos = self.obtener_widgets_por_fila(1, 5)
            for w in campos_completos: w.show()
        

            self.estado_actualizacion = "BUSCAR"
            self.btn_aceptar.setStyleSheet("background-color: #FFC107; color: black; font-weight: bold;") 

        elif index == 2:  #eliminar
             self.setWindowTitle("CRUD de Clientes - ELIMINAR")
             self.btn_aceptar.setText("Eliminar")
             self.dni.setEnabled(True) 
             
             

    def realizar_operacion(self):
        operacion = self.combo_tipo.currentText()
        if operacion == "Agregar cliente":
            self.agregar_cliente()
        elif operacion == "Actualizar cliente":
            if self.estado_actualizacion == "BUSCAR":
                self.buscar_cliente_para_actualizar()
            else: # estado = "GUARDAR"
                self.guardar_actualizacion()
                
        elif operacion == "Eliminar cliente":
            self.eliminar_cliente()

    
    def buscar_cliente_para_actualizar(self):
        dni = self.dni.text().strip()
        if not dni:
            QMessageBox.warning(self, "Error", "Ingrese el DNI del cliente a buscar.")
            return

        try:
            datos = bd.obtener_cliente_por_dni(dni)

            if datos:
                nombre, apellido, contrasena, telefono, direccion = datos

                # Llenar campos con datos existentes
                self.nombre.setText(nombre)
                self.apellido.setText(apellido)
                self.contrasena.setText(contrasena)
                self.telefono.setText(telefono or "")
                self.direccion.setText(direccion or "")

                
                self.estado_actualizacion = "GUARDAR"
                self.btn_aceptar.setText("Guardar Cambios")
                self.btn_aceptar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
                self.dni.setEnabled(False) 

            else:
                QMessageBox.warning(self, "No Encontrado", f"No existe un cliente con DNI: {dni}.")

        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Fallo en la búsqueda: {e}")


    def guardar_actualizacion(self):
        dni = self.dni.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text() 
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()

        if not nombre or not apellido or not contrasena:
            QMessageBox.warning(self, "Error", "Nombre, Apellido y Contraseña no pueden estar vacíos.")
            return

        try:
            bd.actualizar_cliente(dni, nombre, apellido, contrasena, telefono, direccion) 

            QMessageBox.information(self, "Éxito", f"Cliente {dni} actualizado.")

            self.cambiar_operacion(1) 

        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Fallo al guardar: {e}")

    
    
    def agregar_cliente(self):
        # 1. Recuperar datos
        dni = self.dni.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text() 
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()
        
        
        if not dni or not nombre or not apellido or not contrasena:
            QMessageBox.warning(self, "Error de Datos", "DNI, Nombre, Apellido y Contraseña son obligatorios.")
            return
        
        
        try:
            
            bd.agregar_cliente(dni, nombre, apellido, contrasena, telefono, direccion) 
            
            QMessageBox.information(self, "Éxito", f"Cliente '{nombre} {apellido}' (DNI: {dni}) agregado correctamente.")
            
            
            self.cambiar_operacion(0) 

        except sqlite3.IntegrityError:
             QMessageBox.critical(self, "Error de Registro", f"El DNI {dni} ya está registrado en la base de datos.")
        except Exception as e:
             QMessageBox.critical(self, "Error de DB", f"Fallo al registrar cliente: {e}")


    def actualizar_cliente(self):
        dni = self.dni.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text() 
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()
       
        
        if not dni:
            QMessageBox.warning(self, "Error de Datos", "Debe ingresar el DNI del cliente a actualizar.")
            return

        try:
             
            bd.actualizar_cliente(dni, nombre, apellido, contrasena, telefono, direccion) 
        
        
            QMessageBox.information(self, "Actualización Éxito", f"Cliente con DNI {dni} actualizado (Simulación).")

        except Exception as e:
             QMessageBox.critical(self, "Error de DB", f"Fallo al actualizar: {e}")


    def eliminar_cliente(self):
        dni = self.dni.text().strip()
        if not dni:
            QMessageBox.warning(self, "Error de Datos", "Debe ingresar el DNI del cliente a eliminar.")
            return

        
        respuesta = QMessageBox.question(self, "Confirmar Eliminación", 
                                        f"¿Está seguro de eliminar al cliente con DNI: {dni}?.", 
                                        QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.No:
            return

        
        try:
            bd.eliminar_cliente(dni) # Llama a la función de base_datos.py
            
            QMessageBox.information(self, "Éxito", f"Cliente con DNI {dni} eliminado.")
            

            self.cambiar_operacion(2) 

        except Exception as e:
             QMessageBox.critical(self, "Error de DB", f"Fallo al eliminar cliente: {e}")
    
    
    
    def agregar_cliente(self):
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text().strip()
        dni = self.dni.text().strip()
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()

        #no estar vacios
        if not (nombre and apellido and dni and contrasena):
            QMessageBox.warning(self, "Error", "Complete todos los campos obligatorios (Nombre, Apellido, DNI, Contraseña).")
            return

        if not dni.isdigit():
            QMessageBox.critical(self, "Error de DNI", "El DNI debe contener solo números.")
            return

        if len(dni) < 8:
            QMessageBox.critical(self, "Error de DNI", "El DNI debe tener un mínimo de 8 dígitos.")
            return
        # ------------------------------------------------------------------

        try:
            bd.agregar_cliente(dni, nombre, apellido, contrasena, telefono, direccion)

            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")

        except ValueError as e:
            QMessageBox.critical(self, "Error de Cliente", str(e))
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al registrar el cliente: {str(e)}")
    
    
    
    def eliminar_cliente(self):
        dni = self.dni.text().strip()

        if not dni:
            QMessageBox.warning(self, "Error de Datos", "Debe ingresar el DNI del cliente a eliminar.")
            return

        
        respuesta = QMessageBox.question(self, "Confirmar Eliminación", 
                                        f"¿Está seguro de eliminar al cliente con DNI: {dni}? Esta acción es irreversible.", 
                                        QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.No:
            return

    
        try:

            bd.eliminar_cliente(dni) 

            QMessageBox.information(self, "Éxito", f"Cliente con DNI {dni} eliminado correctamente.")
            self.dni.clear() #limpiar campo 

        except sqlite3.Error as e:
             QMessageBox.critical(self, "Error de DB", f"Fallo al eliminar cliente: {e}")
        except Exception as e:
             QMessageBox.critical(self, "Error Fatal", f"Ocurrió un error inesperado: {e}")
             
             
             
    def actualizar_cliente(self):
    # recuperar datos
        dni = self.dni.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text() 
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()

        if not dni or not nombre or not apellido or not contrasena:
            QMessageBox.warning(self, "Error de Datos", "DNI, Nombre, Apellido y Contraseña son obligatorios para la actualización.")
            return

       
        try:
            bd.actualizar_cliente(dni, nombre, apellido, contrasena, telefono, direccion) 

            QMessageBox.information(self, "Éxito", f"Cliente con DNI {dni} actualizado correctamente.")

        except sqlite3.Error as e:
             QMessageBox.critical(self, "Error de DB", f"Fallo al actualizar cliente: {e}")
        except Exception as e:
             QMessageBox.critical(self, "Error Fatal", f"Ocurrió un error inesperado: {e}")