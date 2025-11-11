from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from interfaces.clientes import VentanaClientes
from interfaces.cuentas import VentanaCuentas
from interfaces.deposito import VentanaDeposito
from interfaces.extraccion import VentanaExtraccion
from interfaces.transferencia import VentanaTransferencia
from interfaces.informes import VentanaInformes

import sys


class VentanaPrincipal(QMainWindow):
    def __init__(self, nombre_empleado,rol, parent=None):
        super().__init__(parent)
        self.nombre_empleado = nombre_empleado
        self.rol_empleado = rol
        
        
        self.setWindowTitle(f"Sistema Bancario | {self.rol_empleado}: {self.nombre_empleado}")
        self.setGeometry(250, 100, 800, 500)
        self.apply_stylesheet()
        
        self.init_ui()

    def init_ui(self):
        # barra de Menú
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Menús: "Gestión" / "Movimientos / "Informe"
        gestion_menu = menu_bar.addMenu("Gestión")
        
        movimientos_menu = menu_bar.addMenu("Movimientos")
        
        informes_menu = menu_bar.addMenu("Informes")

        
        # opcion clientes
        act_clientes = gestion_menu.addAction("Clientes")
        act_clientes.triggered.connect(self.abrir_clientes)
        
        # opcion Cuentas
        act_cuentas = gestion_menu.addAction("Cuentas")
        act_cuentas.triggered.connect(self.abrir_cuentas)
        
        #movimientos 
        
        act_movimientos = movimientos_menu.addAction("Depósito")
        act_movimientos.triggered.connect(self.abrir_deposito)
        
        act_movimientos = movimientos_menu.addAction("Extracción")
        act_movimientos.triggered.connect(self.abrir_extraccion)
        
        act_movimientos= movimientos_menu.addAction("Transferencia")
        act_movimientos.triggered.connect(self.abrir_transferencia)
        
        act_movimientos = movimientos_menu.addAction("Plazo fijo")
        #act_cuentas.triggered.connect(self.abrir_plazo_fijo)
        
        
        
        #informes
        
        act_informes = informes_menu.addAction("Informes de movimientos")
        act_informes.triggered.connect(self.abrir_informe_movimientos)
        
        act_informes = informes_menu.addAction("Informes de plazo fijo")
        #act_cuentas.triggered.connect(self.abrir_informe_plazo_fijo)

        
    
        gestion_menu.addSeparator()
        act_salir = gestion_menu.addAction("Salir")
        act_salir.triggered.connect(self.confirmar_salida)

        # 4. Contenido Central de la Ventana Principal
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        titulo = QLabel(f"<h1>Sistema de Gestión Bancaria</h1>") #faltaría: Bienvenida a {nombre_empleado} al terminar login
        titulo.setAlignment(Qt.AlignCenter)
        
        
        #fuente
        fuente = titulo.font()
        fuente.setPointSize(13)
        fuente.setBold(True)
        titulo.setFont(fuente)
        layout.addWidget(titulo)
        
        
        subtitulo = QLabel("Utilice la barra superior para acceder a las opciones.")
        subtitulo.setAlignment(Qt.AlignCenter)
        
        #decoracion tipografia
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #004080;")
        subtitulo.setStyleSheet("font-size: 16px; color: #555;")
        
        self.setCentralWidget(central_widget)
        layout.addWidget(subtitulo)
        
    def confirmar_salida(self):
        respuesta = QMessageBox.question(
            self,
            "Salir",
            "¿Desea salir?",
            QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            QMessageBox.information(self, "Salir", "¡Hasta luego!")
            self.close()
      
            
    def apply_stylesheet(self):   #metodo para aumentar tamaño de menu
        style_sheet = """
            QMenuBar {
                font-size: 16px 
            }
            QMenu {
                font-size: 14px; 
            }
        """
        self.setStyleSheet(style_sheet)
        
        

    def abrir_clientes(self):
        self.ventana_clientes = VentanaClientes(self)
        self.ventana_clientes.exec()
        
    def abrir_cuentas(self):
        self.ventana_cuentas = VentanaCuentas(self)
        self.ventana_cuentas.exec() 


    def abrir_deposito(self):
        self.ventana_deposito = VentanaDeposito(self)
        self.ventana_deposito.exec() 
        
    
    def abrir_extraccion(self):
        self.ventana_extr = VentanaExtraccion(self)
        self.ventana_extr.exec() 

    
    def abrir_transferencia(self):
        self.ventana_transf = VentanaTransferencia(self)
        self.ventana_transf.exec() 

    
    def abrir_plazo_fijo(self):
        #self.ventana_movimientos = VentanaMovimientos(self)
        #self.ventana_movimientos.exec() 
        pass

    
    def abrir_informe_movimientos(self):
        self.ventana_informes = VentanaInformes(self)
        self.ventana_informes.exec() 
        pass
    
    
    def abrir_informe_plazo_fijo(self):
        #self.ventana_informes = VentanaInformes(self)
        #self.ventana_informes.exec() 
        pass



