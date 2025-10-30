import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton


def iniciar_app():
    app = QApplication(sys.argv)
    
    ventana = QMainWindow()
    ventana.setWindowTitle("Ventana Principal")
    ventana.setGeometry(200, 200, 1000,700) #x,y, ancho y alto
    
    # etiqueta = QLabel("!Bienvenidos al banco", ventana)
    # etiqueta.move(20,10)
    
    entrada = QLineEdit(ventana)
    entrada.move(50,100)
    entrada.resize(300, 30)
    entrada.setPlaceholderText("Escriba el nombre aquí...")
    
    ventana.show()
    
    sys.exit(app.exec())
    
 
def obtener_texto():
    pass   
    
    
    

if __name__ == "__main__":
    iniciar_app()
    
    
#QDialog  = son ventanas secundarias o temporales
# Barra de Menú (QMenuBar)
#Barras de Herramientas (QToolBar)
#Barra de Estado (QStatusBar)
#Área Central (QCentralWidget): Aquí es donde se coloca el contenido
#principal de la aplicación.
    