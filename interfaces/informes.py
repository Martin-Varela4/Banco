import csv
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

import base_datos as bd 

class VentanaInformes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informe de Movimientos")
        self.resize(900, 600)
        self.setModal(True)

        layout_principal = QVBoxLayout(self)
        
        # titulo
        titulo = QLabel("Informe de Movimientos")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        
        # filtros
        self.setup_filtros(layout_principal)

        # tabla resultados
        self.tabla_movimientos = QTableWidget()
        self.tabla_movimientos.setColumnCount(6)
        self.tabla_movimientos.setHorizontalHeaderLabels([
            "ID Cuenta", "Tipo Movimiento", "Monto", "Fecha y Hora", 
            "Cuenta Relacionada", "ID Movimiento"
        ])
        
        self.tabla_movimientos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
     
        self.tabla_movimientos.horizontalHeader().setStretchLastSection(True)
        layout_principal.addWidget(self.tabla_movimientos)

  
        self.setup_botones(layout_principal)
        
        # datos iniciales al abrir la ventana
        self.consultar_movimientos()

    def setup_filtros(self, layout_principal):
        
        filtro_layout = QHBoxLayout()
        filtro_layout.setAlignment(Qt.AlignLeft)
        
        # Filtro Tipo de Movimiento
        filtro_layout.addWidget(QLabel("<b>Tipo:</b>"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItem("TODOS") # Opción para no filtrar
        self.combo_tipo.addItems([
            "DEPOSITO", "EXTRACCION", "TRANSFERENCIA_ENTRADA", "TRANSFERENCIA_SALIDA"
        ])
        self.combo_tipo.setFixedWidth(150)
        filtro_layout.addWidget(self.combo_tipo)
        
        # Filtro Fecha Desde
        filtro_layout.addWidget(QLabel("<b>Desde:</b>"))
        self.fecha_desde = QDateEdit()
        self.fecha_desde.setCalendarPopup(True)
        self.fecha_desde.setDisplayFormat("yyyy-MM-dd")
        filtro_layout.addWidget(self.fecha_desde)

        # Filtro Fecha Hasta
        filtro_layout.addWidget(QLabel("<b>Hasta:</b>"))
        self.fecha_hasta = QDateEdit()
        self.fecha_hasta.setCalendarPopup(True)
        self.fecha_hasta.setDisplayFormat("yyyy-MM-dd")
        self.fecha_hasta.setDate(QDate.currentDate()) # Fecha actual por defecto
        filtro_layout.addWidget(self.fecha_hasta)
        
        # Botón Consultar
        btn_consultar = QPushButton("Consultar")
        btn_consultar.setStyleSheet("background-color: #2196F3; color: white;")
        btn_consultar.setFixedWidth(120)
        btn_consultar.clicked.connect(self.consultar_movimientos)
        filtro_layout.addWidget(btn_consultar)
        
        layout_principal.addLayout(filtro_layout)

    def setup_botones(self, layout_principal):
        """Configura el botón de exportar."""
        
        botones_layout = QHBoxLayout()
        botones_layout.addStretch() # espacio flexible a la izquierda
        
        btn_exportar = QPushButton("Exportar a CSV")
        btn_exportar.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_exportar.setFixedWidth(150)
        btn_exportar.clicked.connect(self.exportar_a_csv)
        
        botones_layout.addWidget(btn_exportar)
        layout_principal.addLayout(botones_layout)

    def consultar_movimientos(self):
        """Recoge los filtros y llama a la DB para obtener y mostrar los movimientos."""
        
        tipo_movimiento = self.combo_tipo.currentText()
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        # sumar un día a la fecha 'hasta' para incluir todos los movimientos de ese día
        fecha_hasta = self.fecha_hasta.date().addDays(1).toString("yyyy-MM-dd") 
        
        try:
            movimientos = bd.obtener_movimientos_filtrados(
                tipo_movimiento, 
                fecha_desde, 
                fecha_hasta
            )
            self.mostrar_en_tabla(movimientos)
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Consulta", f"No se pudieron obtener los movimientos: {str(e)}")

    def mostrar_en_tabla(self, movimientos):
        """Rellena la tabla con los datos de los movimientos."""
        
        self.tabla_movimientos.setRowCount(0) # Limpiar tabla
        self.tabla_movimientos.setRowCount(len(movimientos))
        
        for fila, movimiento in enumerate(movimientos):
        
            monto_formateado = f"{movimiento[2]:.2f}"
            
            for columna, valor in enumerate(movimiento):
                item_valor = str(valor)
                if columna == 2: # Columna del Monto
                    item_valor = monto_formateado
                    
                item = QTableWidgetItem(item_valor)
                
                # Alinear el monto a la derecha para mejor legibilidad
                if columna == 2:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                self.tabla_movimientos.setItem(fila, columna, item)
        
        if not movimientos:
             QMessageBox.information(self, "Sin Resultados", "No se encontraron movimientos con los filtros aplicados.")

    def exportar_a_csv(self):
        
        nombre_archivo, _ = QFileDialog.getSaveFileName(
            self, 
            "Exportar a CSV", 
            f"informe_movimientos_{datetime.now().strftime('%Y%m%d')}.csv", 
            "Archivos CSV (*.csv)"
        )
        
        if not nombre_archivo:
            return 
            
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
                writer = csv.writer(archivo_csv)
                
                # encabezados
                encabezados = [self.tabla_movimientos.horizontalHeaderItem(i).text() for i in range(self.tabla_movimientos.columnCount())]
                writer.writerow(encabezados)
                
                # filas
                for fila in range(self.tabla_movimientos.rowCount()):
                    fila_datos = []
                    for columna in range(self.tabla_movimientos.columnCount()):
                        item = self.tabla_movimientos.item(fila, columna)
                        fila_datos.append(item.text() if item is not None else "")
                    writer.writerow(fila_datos)
                    
            QMessageBox.information(self, "Éxito", f"Datos exportados con éxito a:\n{nombre_archivo}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Exportación", f"Fallo al escribir el archivo CSV: {str(e)}")