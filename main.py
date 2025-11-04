import os, sys
from clientes import ClienteEmpresa, ClientePersona
from cuentas import CajaAhorro, CuentaCorriente, CuentaPlazoFijo, CuentaBase
from banco import Banco
from datetime import date
from menus import MenuBanco
from interfaces.ventana_inicio import VentanaInicial
from PySide6.QtWidgets import QApplication

def clear():
    if os.name == "nt":
        os.system("cls")
        
def main():  
    
    app = QApplication(sys.argv)

    # 🔹 Elegí qué ventana querés probar:
    ventana = VentanaInicial()
    # ventana = VentanaLogin()
    # ventana = VentanaRegistro()

    ventana.show()
    sys.exit(app.exec())
    # Creación de tipo de clientes, sus cuentas y banco
    banco = Banco("Macro")

    # Clientes
    cliente1 = ClientePersona("Carlos", 34567934)
    cliente2 = ClienteEmpresa("EmpresaX", 12345678)
    cliente3 = ClientePersona("María", 32765923)
    cliente4 = ClientePersona("Marcos", 327244423)
    cliente5 = ClientePersona("Claudia", 32743125)
    cliente6 = ClientePersona("Juancho", 27947924)
    
    #alta d clientes
    banco.alta_cliente(cliente1)
    banco.alta_cliente(cliente2)
    banco.alta_cliente(cliente3)
    banco.alta_cliente(cliente4)
    banco.alta_cliente(cliente5)
    banco.alta_cliente(cliente6)

    # Cuentas
    cc = CuentaCorriente(1, cliente1, 5000, banco, limite_descubierto=1000)
    cc2 = CuentaCorriente(2, cliente3, -1000, banco, limite_descubierto=10000)
    ca = CajaAhorro(3, cliente3, 3000, banco) #->> segunda cuenta de María
    pf = CuentaPlazoFijo(4, cliente1, 10000, date(2025, 12, 24), banco) #->> segunda cuenta de Carlos
    emp = CuentaCorriente(5, cliente2, 80000, banco, limite_descubierto=20000)
    ca2 = CajaAhorro(6, cliente4, 17500, banco) 
    ca3 = CajaAhorro(7, cliente5, 8200, banco) 
    ca4 = CajaAhorro(8, cliente6, 24000, banco) 

    banco.alta_cuenta(cc)
    banco.alta_cuenta(cc2)
    banco.alta_cuenta(ca)
    banco.alta_cuenta(pf)
    banco.alta_cuenta(emp)
    banco.alta_cuenta(ca2)
    banco.alta_cuenta(ca3)
    banco.alta_cuenta(ca4)
    
    #menu operaciones
    menu = MenuBanco(banco)
    menu.menu_operaciones()

                
if __name__ == "__main__":
    main()