from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import base_datos as bd


class FormularioCuentaCorriente(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        
       
        layout.addWidget(QLabel("<b>Saldo Inicial:</b>"), 0, 0)
        self.saldo_inicial = QLineEdit()
        layout.addWidget(self.saldo_inicial, 0, 1)

        
        layout.addWidget(QLabel("<b>Límite Descubierto:</b>"), 1, 0)
        self.limite_descubierto = QLineEdit()
        layout.addWidget(self.limite_descubierto, 1, 1)
        
        
        layout.setRowStretch(2, 1)

class FormularioPlazoFijo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        
        
        layout.addWidget(QLabel("<b>Saldo Inicial:</b>"), 0, 0)
        self.saldo_inicial = QLineEdit()
        layout.addWidget(self.saldo_inicial, 0, 1)

        layout.addWidget(QLabel("<b>Tasa de Interés (%):</b>"), 1, 0)
        self.tasa_interes = QLineEdit()
        layout.addWidget(self.tasa_interes, 1, 1)

        layout.addWidget(QLabel("<b>Fecha Vencimiento (AAAA-MM-DD):</b>"), 2, 0)
        self.fecha_vencimiento = QLineEdit()
        self.fecha_vencimiento.setPlaceholderText("Ej: 2026-12-31")
        layout.addWidget(self.fecha_vencimiento, 2, 1)

        layout.setRowStretch(3, 1)


class FormularioCajaAhorro(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        
       
        layout.addWidget(QLabel("<b>Saldo Inicial:</b>"), 0, 0)
        self.saldo_inicial = QLineEdit()
        layout.addWidget(self.saldo_inicial, 0, 1)
        
        layout.setRowStretch(2, 1)


class VentanaCuentas(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("CRUD de Cuentas")
        self.resize(550, 450)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)


        titulo = QLabel("Gestión de Cuentas")
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #004D40;")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        layout_principal.addSpacing(15)

     
        self.combo_operacion = self.crear_combo_box(["Agregar Cuenta", "Actualizar Parámetros", "Cerrar Cuenta"])
        self.combo_operacion.currentIndexChanged.connect(self.cambiar_operacion)
        
       
        self.combo_tipo_cuenta = self.crear_combo_box(["Cuenta Corriente", "Plazo Fijo", "Caja de Ahorro"])

        #cambia la pila del QStackedWidget interno
        self.combo_tipo_cuenta.currentIndexChanged.connect(self.cambiar_tipo_formulario)
        

        dni_layout = QGridLayout()
        dni_layout.addWidget(QLabel("<b>DNI Cliente:</b>"), 0, 0)
        self.cliente_dni = QLineEdit()
        dni_layout.addWidget(self.cliente_dni, 0, 1)
        
        layout_principal.addLayout(self._crear_horizontal_layout(QLabel("<b>Operación:</b>"), self.combo_operacion))
        layout_principal.addLayout(dni_layout)
        layout_principal.addLayout(self._crear_horizontal_layout(QLabel("<b>Tipo de Cuenta:</b>"), self.combo_tipo_cuenta))
    
        
        self.stacked_campos = QStackedWidget()
        self.layout_campos_fijos = QGridLayout() 
        
        #inicializar
        self.form_corriente = FormularioCuentaCorriente()
        self.form_plazo_fijo = FormularioPlazoFijo()
        self.form_caja_ahorro = FormularioCajaAhorro()
        
        # añadimos los formularios como "pilas"
        self.stacked_campos.addWidget(self.form_corriente)  
        self.stacked_campos.addWidget(self.form_plazo_fijo) 
        self.stacked_campos.addWidget(self.form_caja_ahorro)
        
        layout_principal.addLayout(self.layout_campos_fijos) # campos fijos (ID Cuenta)
        layout_principal.addWidget(self.stacked_campos)      
        

        layout_principal.addStretch()
        self.btn_aceptar = QPushButton("Aceptar")
        self.btn_aceptar.setStyleSheet("background-color: #008000; color: white; font-weight: bold;")
        self.btn_aceptar.clicked.connect(self.realizar_operacion)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("background-color: #CC0000; color: white; font-weight: bold;")
        btn_cancelar.clicked.connect(self.close)
        
        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.btn_aceptar)
        botones_layout.addWidget(btn_cancelar)
        layout_principal.addLayout(botones_layout)
 
        self.cambiar_operacion(0) 
        

    
    def crear_combo_box(self, items):
        combo = QComboBox()
        combo.addItems(items)
        combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return combo

    def _crear_horizontal_layout(self, label, widget):
        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(widget)
        return h_layout

    
    def cambiar_tipo_formulario(self, index):
        self.stacked_campos.setCurrentIndex(index)
        
    def cambiar_operacion(self, index):
        if index == 0: # Agregar Cuenta
            self.setWindowTitle("AGREGAR")
            self.btn_aceptar.setText("Abrir Cuenta")
            self.cliente_dni.setEnabled(True)
            self.combo_tipo_cuenta.show()
            self.stacked_campos.show()

        elif index == 1: 
            self.setWindowTitle("ACTUALIZAR")
            self.btn_aceptar.setText("Actualizar Parámetros")
            
            
            self.lbl_id_cuenta = QLabel("<b>ID de Cuenta:</b>")
            self.txt_id_cuenta = QLineEdit()
            self.layout_campos_fijos.addWidget(self.lbl_id_cuenta, 0, 0)
            self.layout_campos_fijos.addWidget(self.txt_id_cuenta, 0, 1)

            self.cliente_dni.setEnabled(True) 
            self.combo_tipo_cuenta.show() 
            self.stacked_campos.show()

        elif index == 2: 
            self.setWindowTitle("CERRAR")
            self.btn_aceptar.setText("Cerrar Cuenta")
            
            # Añadir campo de ID de Cuenta
            self.lbl_id_cuenta = QLabel("<b>ID de Cuenta:</b>")
            self.txt_id_cuenta = QLineEdit()
            self.layout_campos_fijos.addWidget(self.lbl_id_cuenta, 0, 0)
            self.layout_campos_fijos.addWidget(self.txt_id_cuenta, 0, 1)
            
            self.cliente_dni.setEnabled(True) 
            self.combo_tipo_cuenta.hide() 
            self.stacked_campos.hide()    

    def realizar_operacion(self):
        operacion = self.combo_operacion.currentText()
        if operacion == "Agregar Cuenta":
            self.abrir_cuenta()
        elif operacion == "Actualizar Parámetros":
            self.actualizar_parametros()
        elif operacion == "Cerrar Cuenta":
            self.cerrar_cuenta()

    def abrir_cuenta(self):
        dni = self.cliente_dni.text().strip()
        tipo_cuenta = self.combo_tipo_cuenta.currentText()

        if not dni:
            QMessageBox.warning(self, "Error", "Debe ingresar el DNI del cliente.")
            return

        formulario_activo = self.stacked_campos.currentWidget()
       
        saldo_inicial = formulario_activo.saldo_inicial.text().replace(',', '.') 

        parametro_especifico = None
        fecha_vencimiento_pf = None


        if tipo_cuenta == "Cuenta Corriente":
           
            parametro_especifico = formulario_activo.limite_descubierto.text().replace(',', '.')

        elif tipo_cuenta == "Plazo Fijo":
            
            parametro_especifico = formulario_activo.tasa_interes.text().replace(',', '.')

            
            fecha_vencimiento_pf = formulario_activo.fecha_vencimiento.text().strip()
        
  
        try:
            id_cuenta = bd.abrir_cuenta(
                dni, 
                tipo_cuenta, 
                saldo_inicial, 
                parametro_especifico,
                fecha_vencimiento_str=fecha_vencimiento_pf 
            )
            QMessageBox.information(
                self, "Éxito", 
                f"Cuenta {tipo_cuenta} abierta correctamente para el cliente {dni} con ID: {id_cuenta}."
            )
            self.close()

        except ValueError as e:
            QMessageBox.critical(self, "Error de Validación", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error Desconocido", f"Fallo al crear la cuenta: {str(e)}")

    def actualizar_parametros(self):
        id_cuenta = self.txt_id_cuenta.text().strip()
        tipo_cuenta = self.combo_tipo_cuenta.currentText()
        dni_cliente = self.cliente_dni.text().strip()
        
        if not dni_cliente:
            QMessageBox.warning(self, "Error", "Debe ingresar el DNI del cliente.")
            return
        
        if not id_cuenta:
            QMessageBox.warning(self, "Error", "Debe ingresar el ID de la cuenta a actualizar.")
            return

        formulario_activo = self.stacked_campos.currentWidget()
        saldo = formulario_activo.saldo_inicial.text().replace(',', '.') 
        
        parametro_especifico = None
        
  
        if tipo_cuenta == "Cuenta Corriente":
            parametro_especifico = formulario_activo.limite_descubierto.text().replace(',', '.')
            param_nombre = "limite_descubierto"
        elif tipo_cuenta == "Plazo Fijo":
            parametro_especifico = formulario_activo.tasa_interes.text().replace(',', '.')
            param_nombre = "tasa_interes"
        else:
            param_nombre = None
        

        try:
            bd.actualizar_cuenta_parametros(
                id_cuenta, 
                dni_cliente, 
                saldo, 
                param_nombre, 
                parametro_especifico
            )
            
            QMessageBox.information(self, "Éxito", f"Parámetros de Cuenta {id_cuenta} actualizados correctamente.")
            
        except ValueError as e:
        
            QMessageBox.critical(self, "Error de Validación", str(e))
        except RuntimeError as e:
            QMessageBox.critical(self, "Error de Base de Datos", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")

    def cerrar_cuenta(self):
        id_cuenta = self.txt_id_cuenta.text().strip()
        
        if not id_cuenta:
            QMessageBox.warning(self, "Error", "Debe ingresar el ID de la cuenta a cerrar.")
            return

        respuesta = QMessageBox.question(self, "Confirmar Cierre", 
                                        f"¿Está seguro de cerrar la cuenta ID: {id_cuenta}? El saldo debe ser cero.", 
                                        QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.No:
            return
            

        try:
            bd.cerrar_cuenta(id_cuenta)
            
            QMessageBox.information(self, "Éxito", f"Cuenta {id_cuenta} cerrada (estado actualizado).")
            
        except ValueError as e:
            QMessageBox.critical(self, "Error de Cierre", str(e)) # Captura "Saldo no es cero"
        except Exception as e:
            QMessageBox.critical(self, "Error de DB", f"Fallo al cerrar cuenta: {e}")


