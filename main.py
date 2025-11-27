import os, sys
from interfaces.inicio import InicioSesion
from PySide6.QtWidgets import QApplication


def clear():
    if os.name == "nt":
        os.system("cls")
        
def main():  
    
    app = QApplication(sys.argv)

    ventana = InicioSesion()
    
    ventana.show()
    sys.exit(app.exec())
                
if __name__ == "__main__":
    main()