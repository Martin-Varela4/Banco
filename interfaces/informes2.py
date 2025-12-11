import csv
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFileDialog, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

# 🟢 IMPORTACIONES NECESARIAS PARA EL GRÁFICO (Matplotlib)
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np 

import base_datos as bd

class VentanaInformes(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informe y Exportación de Movimientos")
        self.resize(1200, 600) # Aumentamos el tamaño para el gráfico
        self.setModal(True)

        layout_principal = QVBoxLayout(self)
        
        # 1. Título
        titulo = QLabel("Informe de Movimientos Bancarios")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo)
        
        # 2. Área de Filtros
        self.setup_filtros(layout_principal)

        # 🟢 3. Área de Contenido Principal (Tabla y Gráfico)
        contenido_layout = QHBoxLayout()
        
        # Tabla de Resultados
        self.tabla_movimientos = QTableWidget()
        self.tabla_movimientos.setColumnCount(6)
        self.tabla_movimientos.setHorizontalHeaderLabels([
            "ID Cuenta", "Tipo Movimiento", "Monto", "Fecha y Hora", 
            "Cuenta Relacionada", "ID Movimiento"
        ])
        self.tabla_movimientos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla_movimientos.horizontalHeader().setStretchLastSection(True)
        # La tabla ocupa 2/3 del espacio horizontal
        contenido_layout.addWidget(self.tabla_movimientos, 2) 

        # 🟢 Contenedor del Gráfico (ocupa 1/3 del espacio horizontal)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        contenido_layout.addWidget(self.canvas, 1)

        layout_principal.addLayout(contenido_layout)
        # -----------------------------------------------------------------------

        # 4. Área de Botones
        self.setup_botones(layout_principal)
        
        # Cargar datos iniciales
        self.consultar_movimientos()

    def setup_filtros(self, layout_principal):
        filtro_layout = QHBoxLayout()
        filtro_layout.setAlignment(Qt.AlignLeft)
        
 
        filtro_layout.addWidget(QLabel("<b>Tipo:</b>"))
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItem("TODOS")
        self.combo_tipo.addItems([
            "DEPOSITO", "EXTRACCION", "TRANSFERENCIA_ENTRADA", "TRANSFERENCIA_SALIDA"
        ])
        self.combo_tipo.setFixedWidth(150)
        filtro_layout.addWidget(self.combo_tipo)
        
        # desde
        filtro_layout.addWidget(QLabel("<b>Desde:</b>"))
        self.fecha_desde = QDateEdit()
        self.fecha_desde.setCalendarPopup(True)
        self.fecha_desde.setDisplayFormat("yyyy-MM-dd")
        self.fecha_desde.setDate(QDate.currentDate().addMonths(-3))
        filtro_layout.addWidget(self.fecha_desde)

        # hasta
        filtro_layout.addWidget(QLabel("<b>Hasta:</b>"))
        self.fecha_hasta = QDateEdit()
        self.fecha_hasta.setCalendarPopup(True)
        self.fecha_hasta.setDisplayFormat("yyyy-MM-dd")
        self.fecha_hasta.setDate(QDate.currentDate())
        filtro_layout.addWidget(self.fecha_hasta)
        

        btn_consultar = QPushButton("Consultar")
        btn_consultar.setStyleSheet("background-color: #2196F3; color: white;")
        btn_consultar.setFixedWidth(120)
        btn_consultar.clicked.connect(self.consultar_movimientos)
        filtro_layout.addWidget(btn_consultar)
        
        layout_principal.addLayout(filtro_layout)

    def setup_botones(self, layout_principal):
        
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        
        btn_exportar = QPushButton("Exportar a CSV")
        btn_exportar.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_exportar.setFixedWidth(150)
        btn_exportar.clicked.connect(self.exportar_a_csv)
        
        botones_layout.addWidget(btn_exportar)
        layout_principal.addLayout(botones_layout)

    def consultar_movimientos(self):
        
        tipo_seleccionado = self.combo_tipo.currentText()
        fecha_desde = self.fecha_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.fecha_hasta.date().addDays(1).toString("yyyy-MM-dd") 

        if tipo_seleccionado in ["TRANSFERENCIA_ENTRADA", "TRANSFERENCIA_SALIDA"]:
            tipo_movimiento_db = "TRANSFERENCIA"
        else:
            tipo_movimiento_db = tipo_seleccionado
        
        try:
            movimientos = bd.obtener_movimientos_filtrados(
                tipo_movimiento_db, 
                fecha_desde, 
                fecha_hasta
            )
            
            self.mostrar_en_tabla(movimientos, tipo_seleccionado) 
            self.generar_grafico(movimientos)
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Consulta", f"No se pudieron obtener los movimientos: {str(e)}")

    def mostrar_en_tabla(self, movimientos, filtro_tipo_ui="TODOS"):
       
        
        self.tabla_movimientos.setRowCount(0)
        
        movimientos_filtrados_ui = []
        
        for movimiento in movimientos:
             id_cuenta_origen = movimiento[0]
             tipo_db = movimiento[1]
             
             
             if tipo_db == "TRANSFERENCIA":
        
                 if filtro_tipo_ui == "TRANSFERENCIA_SALIDA" and movimiento[2] > 0:
                     continue 
                 elif filtro_tipo_ui == "TRANSFERENCIA_ENTRADA" and movimiento[2] < 0:
                     continue 
             
             movimientos_filtrados_ui.append(movimiento)
        
        self.tabla_movimientos.setRowCount(len(movimientos_filtrados_ui))
        
        for fila, movimiento in enumerate(movimientos_filtrados_ui):
           
            
            monto_formateado = f"{movimiento[2]:.2f}"
            
            cuenta_relacionada_valor = movimiento[4]
            cuenta_relacionada_str = str(cuenta_relacionada_valor)
            
          
            if cuenta_relacionada_valor is None:
                cuenta_relacionada_str = "N/A"
            
            for columna, valor in enumerate(movimiento):
                item_valor = str(valor)
                
                if columna == 2: 
                    item_valor = monto_formateado
                    
                elif columna == 4: 
                    item_valor = cuenta_relacionada_str 
                    
                item = QTableWidgetItem(item_valor)
                
                if columna == 2:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                self.tabla_movimientos.setItem(fila, columna, item)
        
        if not movimientos_filtrados_ui:
             QMessageBox.information(self, "Sin Resultados", "No se encontraron movimientos con los filtros aplicados.")

    def generar_grafico(self, movimientos):
        
        resumen = {}
        
        for movimiento in movimientos:
            tipo_db = movimiento[1]
            monto_real = movimiento[2]
            
            
            monto_abs = abs(monto_real)
            
            etiqueta = tipo_db
            resumen[etiqueta] = resumen.get(etiqueta, 0) + monto_abs

       
        labels = list(resumen.keys())
        sizes = list(resumen.values())
        

        self.figure.clear()
        if not sizes or sum(sizes) == 0:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, "No hay movimientos para graficar", ha='center', va='center')
            self.canvas.draw()
            return

       
        ax = self.figure.add_subplot(111)
        
       
        colors = ['#4CAF50', '#F44336', '#2196F3', '#FFC107'] 
        
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors[:len(labels)],
            wedgeprops={'edgecolor': 'black'}
        )
        
        ax.axis('equal')  
        ax.set_title("Porcentaje de movimientos", fontsize=12)
        
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_weight('bold')

        self.canvas.draw()

    def exportar_a_csv(self):
        """Guarda el contenido actual de la tabla en un archivo CSV."""

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
                
                encabezados = [self.tabla_movimientos.horizontalHeaderItem(i).text() for i in range(self.tabla_movimientos.columnCount())]
                writer.writerow(encabezados)
                
                for fila in range(self.tabla_movimientos.rowCount()):
                    fila_datos = []
                    for columna in range(self.tabla_movimientos.columnCount()):
                        item = self.tabla_movimientos.item(fila, columna)
                        fila_datos.append(item.text() if item is not None else "")
                    writer.writerow(fila_datos)
                    
            QMessageBox.information(self, "Éxito", f"Datos exportados con éxito a:\n{nombre_archivo}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error de Exportación", f"Fallo al escribir el archivo CSV: {str(e)}")