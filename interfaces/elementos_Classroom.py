import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QDialog, QGridLayout, QHBoxLayout, QLineEdit, QMenuBar, QMainWindow
from PySide6.QtCore import Qt

# Removed PyQt6 import as it is not needed


# =================================================================
# CLASES DE VENTANAS SECUNDARIAS
# =================================================================

class VentanaClientes(QDialog):
    """Ventana para la gestión de datos de Clientes."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(200, 200, 400, 300)
        self.setModal(True) # Hace la ventana modal (bloquea la principal)

        main_layout = QVBoxLayout(self)
        
        # 1. Layout de Formulario (Grid para pares Label-LineEdit)
        form_layout = QGridLayout()
        
        # Fila 0: Nombre
        form_layout.addWidget(QLabel("<b>Nombre:</b>"), 0, 0)
        form_layout.addWidget(QLineEdit(), 0, 1)
        
        # Fila 1: Apellido
        form_layout.addWidget(QLabel("<b>Apellido:</b>"), 1, 0)
        form_layout.addWidget(QLineEdit(), 1, 1)

        # Fila 2: DNI/Identificación
        form_layout.addWidget(QLabel("<b>DNI/ID:</b>"), 2, 0)
        form_layout.addWidget(QLineEdit(), 2, 1)
        
        # Fila 3: Email
        form_layout.addWidget(QLabel("<b>Email:</b>"), 3, 0)
        form_layout.addWidget(QLineEdit(), 3, 1)

        main_layout.addLayout(form_layout)
        main_layout.addStretch() # Espacio flexible para empujar el botón abajo

        # 2. Botón Cerrar
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.clicked.connect(self.close) # Conecta al método de cierre de la ventana
        
        # Layout para el botón (centrado o al final)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cerrar)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)


class VentanaCuentas(QDialog):
    """Ventana para la creación de Cuentas Bancarias."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Creación de Cuentas")
        self.setGeometry(200, 200, 400, 250)
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        
        # 1. Layout de Formulario (Grid)
        form_layout = QGridLayout()

        # Fila 0: Tipo de Cuenta
        form_layout.addWidget(QLabel("<b>Tipo de Cuenta:</b>"), 0, 0)
        form_layout.addWidget(QLabel("Caja de Ahorro"), 0, 1) # Podría ser un QComboBox
        
        # Fila 1: Moneda
        form_layout.addWidget(QLabel("<b>Moneda:</b>"), 1, 0)
        form_layout.addWidget(QLineEdit("$"), 1, 1) 

        # Fila 2: Saldo Inicial
        form_layout.addWidget(QLabel("<b>Saldo Inicial:</b>"), 2, 0)
        form_layout.addWidget(QLineEdit("0.00"), 2, 1)
        
        # Fila 3: Titular ID
        form_layout.addWidget(QLabel("<b>ID Titular:</b>"), 3, 0)
        form_layout.addWidget(QLineEdit(), 3, 1)

        main_layout.addLayout(form_layout)
        main_layout.addStretch() 

        # 2. Botón Cerrar
        btn_crear = QPushButton("💾 Crear Cuenta")
        btn_cerrar = QPushButton("❌ Cerrar")
        btn_cerrar.clicked.connect(self.close)
        
        # Layout para los botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_crear)
        btn_layout.addWidget(btn_cerrar)
        
        main_layout.addLayout(btn_layout)


# =================================================================
# CLASE DE VENTANA PRINCIPAL (MAIN WINDOW)
# =================================================================

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema Bancario - Menú Principal")
        self.setGeometry(100, 100, 600, 400)
        
        self.init_ui()

    def init_ui(self):
        # 1. Crear la Barra de Menú
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # 2. Crear un Menú "Gestión"
        gestion_menu = menu_bar.addMenu("Gestión")

        # 3. Crear Acciones y Conexiones
        
        # Opción Clientes
        act_clientes = gestion_menu.addAction("Clientes")
        act_clientes.triggered.connect(self.abrir_clientes)
        
        # Opción Cuentas
        act_cuentas = gestion_menu.addAction("Cuentas")
        act_cuentas.triggered.connect(self.abrir_cuentas)
        
        # Opción Salir (opcional)
        gestion_menu.addSeparator()
        act_salir = gestion_menu.addAction("Salir")
        act_salir.triggered.connect(self.close)

        # 4. Contenido Central de la Ventana Principal
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("<h1>Bienvenido al Sistema de Gestión Bancaria</h1>"))
        layout.addWidget(QLabel("Utilice el menú 'Gestión' para acceder a las opciones."))
        layout.addStretch()
        self.setCentralWidget(central_widget)

    # =======================================
    # SLOTS (Funciones que abren las ventanas)
    # =======================================

    def abrir_clientes(self):
        """Abre la ventana de Clientes."""
        self.ventana_clientes = VentanaClientes(self)
        self.ventana_clientes.exec() # Usamos exec() ya que es un QDialog (modal)

    def abrir_cuentas(self):
        """Abre la ventana de Cuentas."""
        self.ventana_cuentas = VentanaCuentas(self)
        self.ventana_cuentas.exec() # Usamos exec() ya que es un QDialog (modal)


# =================================================================
# ARRANQUE DE LA APLICACIÓN
# =================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Configuramos el estilo para una mejor visualización multiplataforma
    app.setStyle("Fusion") 
    
    main_window = VentanaPrincipal()
    main_window.show()
    sys.exit(app.exec())