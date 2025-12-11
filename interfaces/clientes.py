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

       
        self.estado_actualizacion = "BUSCAR" 

        layout_principal = QVBoxLayout(self)
        
    
        titulo = QLabel("Gestión de Clientes")
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #004D40;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(15)

        
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("<b>Seleccione Operación:</b>"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Agregar cliente", "Actualizar cliente", "Baja de cliente"])
        self.combo_tipo.currentIndexChanged.connect(self.cambiar_operacion)
        combo_layout.addWidget(self.combo_tipo)
        layout_principal.addLayout(combo_layout)
        layout_principal.addSpacing(20) 

        # formulario
        
        self.form_layout = QGridLayout()
        layout_principal.addLayout(self.form_layout)

      
        self.form_layout.addWidget(QLabel("DNI:"), 0, 0)
        
        dni_layout = QHBoxLayout()
        self.dni = QLineEdit()
        self.dni.setPlaceholderText("Ingrese DNI")
        
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setStyleSheet("background-color: #FFB300; color: #333333; font-weight: bold;")
        self.btn_buscar.clicked.connect(self.buscar_cliente_para_actualizar)
        self.btn_buscar.setVisible(False) 
        
        dni_layout.addWidget(self.dni)
        dni_layout.addWidget(self.btn_buscar)
        self.form_layout.addLayout(dni_layout, 0, 1)

        # Resto de campos
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

       
        self.campos_secundarios = [self.nombre, self.apellido, self.contrasena, self.telefono, self.direccion]
        
        
        self.dni.editingFinished.connect(self.validar_dni_existente)

        self.cambiar_operacion(0) 


    def cambiar_operacion(self, index):
        self.limpiar_campos()
        self.btn_buscar.setVisible(False) 
        self.btn_aceptar.setText("Aceptar")
        self.estado_actualizacion = "BUSCAR" 

        if index == 0:  # alta
            self.btn_aceptar.setText("Agregar")
            self.dni.setEnabled(True)
            self.dni.setReadOnly(False)
            self.contrasena.setEchoMode(QLineEdit.Password)
            
           
            self.btn_aceptar.setEnabled(False)
            for campo in self.campos_secundarios:
                campo.setEnabled(False)
                campo.clear()
        
        elif index == 1:  #actualizar 
            self.btn_buscar.setVisible(True)
            self.dni.setEnabled(True)
            self.dni.setReadOnly(False)
            self.btn_aceptar.setEnabled(False) # Deshabilitado hasta encontrar
            
            for campo in self.campos_secundarios:
                campo.setEnabled(False)
                campo.clear()
        
        elif index == 2:  # Baja de cliente
            self.btn_aceptar.setText("Dar Baja")
            self.btn_aceptar.setEnabled(True)
            self.dni.setEnabled(True)
            self.dni.setReadOnly(False)
            self.contrasena.setEchoMode(QLineEdit.Normal)
            
            for campo in self.campos_secundarios:
                campo.setEnabled(False)
                campo.clear()

        self.dni.setFocus()

    
    def validar_dni_existente(self):
    
        if self.combo_tipo.currentIndex() != 0:
            return 
            
        dni = self.dni.text().strip()
        
        
        if not dni:
            return

        
        self.btn_aceptar.setEnabled(False)
        for campo in self.campos_secundarios:
            campo.setEnabled(False)

        if not dni.isdigit() or len(dni) < 8:
            QMessageBox.critical(self, "Error de DNI", "El DNI debe tener 8 dígitos y ser numérico.")
            self.dni.setFocus()
            return

        try:
            #vonsultar bd
            existe = bd.verificar_existencia_dni(dni)
            
            if existe:
                QMessageBox.critical(self, "DNI Duplicado", 
                                     f"El DNI {dni} ya pertenece a un cliente existente.\nNo se puede agregar.")
                self.dni.setFocus()
                self.dni.selectAll()
            else:
                
                for campo in self.campos_secundarios:
                    campo.setEnabled(True)
                self.btn_aceptar.setEnabled(True)
                self.nombre.setFocus() # mover al campo nombre 
        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Error al validar DNI: {e}")


    def buscar_cliente_para_actualizar(self):
        dni = self.dni.text().strip()
        
        if not dni:
            QMessageBox.warning(self, "Error", "Ingrese un DNI para buscar.")
            return

        try:
            datos = bd.obtener_cliente_por_dni(dni)
            
            if datos:
                nombre, apellido, contrasena, telefono, direccion = datos
                
                self.nombre.setText(nombre)
                self.apellido.setText(apellido)
                self.contrasena.setText(contrasena)
                self.telefono.setText(telefono or "")
                self.direccion.setText(direccion or "")
                
              
                for campo in self.campos_secundarios:
                    campo.setEnabled(True)
                
                self.estado_actualizacion = "GUARDAR"
                self.btn_aceptar.setText("Guardar Cambios")
                self.btn_aceptar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
                self.btn_aceptar.setEnabled(True)
                
                self.dni.setEnabled(False) # dni blqueado
                self.nombre.setFocus()
            else:
                QMessageBox.warning(self, "No Encontrado", "Cliente no encontrado.")
                self.dni.setFocus()
                
        except Exception as e:
            QMessageBox.critical(self, "Error DB", f"Error en búsqueda: {e}")


    def realizar_operacion(self):
        operacion = self.combo_tipo.currentText()
        
        if operacion == "Agregar cliente":
            self.agregar_cliente()
        elif operacion == "Actualizar cliente":
            if self.estado_actualizacion == "GUARDAR":
                self.guardar_actualizacion()
            else:
                QMessageBox.warning(self, "Atención", "Debe buscar un cliente.")
        elif operacion == "Baja de cliente":
            self.baja_cliente()



    def agregar_cliente(self):
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text().strip()
        dni = self.dni.text().strip()
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()

        if not (nombre and apellido and dni and contrasena):
            QMessageBox.warning(self, "Faltan Datos", "Complete los campos obligatorios.")
            return

        try:
            bd.agregar_cliente(dni, nombre, apellido, contrasena, telefono, direccion)
            
            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
            self.limpiar_campos()
            self.cambiar_operacion(0) # resetea  estado

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error Fatal", f"No se pudo agregar: {e}")


    def guardar_actualizacion(self):
        dni = self.dni.text().strip()
        nombre = self.nombre.text().strip()
        apellido = self.apellido.text().strip()
        contrasena = self.contrasena.text().strip()
        telefono = self.telefono.text().strip()
        direccion = self.direccion.text().strip()

        if not (nombre and apellido and contrasena):
            QMessageBox.warning(self, "Error", "Campos obligatorios vacíos.")
            return

        try:
            bd.actualizar_cliente(dni, nombre, apellido, contrasena, telefono, direccion)
            QMessageBox.information(self, "Éxito", "Cliente actualizado.")
            
            self.limpiar_campos()
            self.cambiar_operacion(1)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar: {e}")


    def baja_cliente(self):
        dni = self.dni.text().strip()

        if not dni:
            QMessageBox.warning(self, "Error", "Ingrese DNI.")
            return

        try:
            datos_cliente = bd.obtener_cliente_por_dni(dni) 

            if datos_cliente is None:
                raise ValueError(f"Error: El DNI '{dni}' no se encuentra registrado.")

            nombre = datos_cliente[0]
            apellido = datos_cliente[1]
            nombre_completo = f"{nombre} {apellido}"

            confirm = QMessageBox.question(
                self, 
                "Confirmar Baja", 
                f"¿Está seguro de dar de baja al cliente: {nombre_completo} (DNI: {dni})?", 
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                nombre_eliminado = bd.eliminar_cliente(dni) 

                QMessageBox.information(self, "Éxito", f"Cliente {nombre_eliminado} dado de baja correctamente.")
                self.limpiar_campos()
                self.cambiar_operacion(2)

        except ValueError as e:
            # Captura DNI no encontrado o error de lógica de negocio
            QMessageBox.critical(self, "Error", str(e))
        except RuntimeError as e:
            # Captura errores de base de datos (RuntimeError re-lanzado desde bd.py)
            QMessageBox.critical(self, "Error de DB", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al dar de baja: {e}")


    def limpiar_campos(self):
        self.dni.clear()
        self.nombre.clear()
        self.apellido.clear()
        self.contrasena.clear()
        self.telefono.clear()
        self.direccion.clear()