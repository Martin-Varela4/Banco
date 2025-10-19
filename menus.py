import os
from banco import Banco
from clientes import ClienteEmpresa, ClientePersona
from cuentas import CajaAhorro, CuentaCorriente, CuentaPlazoFijo, CuentaBase
from informes import InformeBanco

def clear():
    if os.name == "nt":
        os.system("cls")



class MenuBanco():
    def __init__(self, banco):
        self.banco = banco

    def menu_inicio(self):
        menu = {"1." : "Gestión de clientes",
                "2." : "Operaciones",
                "3." : "Saldo total del banco"}
                
        while True:
           print(f"\n=== INICIO - BANCO: {self.banco}===")
           for i,j in menu.items():
               print(i,j)
    
    
    def menu_operaciones(self):

        menu = {
                    "1." : "Ver saldos",
                    "2." : "Depositar",
                    "3." : "Extraer",
                    "4." : "Transferir",
                    "5." : "Acreditar intereses (solo Plazo Fijo)",
                    "6." : "Saldo total del banco",
                    "7." : "Ver informes",
                    "8." : "Editar Parametros",
                    "9." : "Aplicar costo de mantenimiento",
                    "10." : "Salir"}   

        while True:
            print("\n=== MENÚ BANCO ===")
            for i,j in menu.items():
                print(i,j)

            opcion = input("Elija una opción: ")

            if opcion == "1":
                clear()
                print("\n Saldos: \n")
                for cuenta in self.banco.cuentas:
                    print(f"Cuenta N°: {cuenta.numero} - Titular: '{cuenta.titular.nombre}' --> Saldo: ${cuenta.saldo}")

            elif opcion == "2":
                clear()
                print("\n---Depósito---\n")
                while True:
                    nro = int(input("Número de cuenta: "))
                    cuenta = self.banco.buscar_cuenta(nro)
                    
                    if cuenta:
                        break
                    else:
                        print("Cuenta no encontrada. Ingrese otra: ")
                
                while True:
                    monto = float(input("Monto a depositar: "))
                    print(cuenta.depositar(monto))
                    break
    
            elif opcion == "3":
                clear()
                print("\n---Extracción---\n")
                while True:
                    nro = int(input("Ingrese el número de cuenta: N°"))
                    cuenta = self.banco.buscar_cuenta(nro)

                    if cuenta:
                        break
                    else:
                        print("Cuenta no encontrada. Ingrese otra: ")

                while True:
                    monto = float(input("Monto a extraer: $"))
                    print(cuenta.extraer(monto))
                    break
                    
                    
            elif opcion == "4": 
                clear()
                print("\n------TRANSFERENCIA------")
                while True:
                    origen = int(input("Cuenta origen: "))
                    destino = int(input("Cuenta destino: "))
                    monto = float(input("Monto a transferir: $"))

                    cuenta_origen = self.banco.buscar_cuenta(origen)
                    cuenta_destino = self.banco.buscar_cuenta(destino)

                    if not cuenta_origen or not cuenta_destino:
                        print("Una de las cuentas no existe, ingrese nuevamente\n") #REAJUSTAR
                        continue
                    
                    nombre_origen = cuenta_origen.titular.nombre
                    nombre_destino = cuenta_destino.titular.nombre

                    print("\nPor favor, confirme la siguiente operación:")
                    confirmacion = input(
                        f"¿Desea transferir ${monto} desde la cuenta N°{origen} "
                        f"de '{nombre_origen}' hacia la cuenta N°{destino} "
                        f"de '{nombre_destino}'? (s/n): ").lower()

                    if confirmacion == "n":
                        print("Transferencia cancelada...")
                        break
                    else:
                        print(f"\n{self.banco.transferir(origen, destino, monto)}") #metodo transferir recien de la clase banco
                        break
                    
            elif opcion == "5":
                clear()
                print("---Areditar Interés----")
                while True:
                    try:
                        nro = int(input("Número de cuenta (Plazo Fijo): "))
                    except ValueError:
                        print("Debe ingresar un número válido.")
                        continue
                    
                    cuenta = self.banco.buscar_cuenta(nro)

                    if not cuenta:
                        print("Cuenta no encontrada. Intente nuevamente.")
                        continue
                    
                    if not isinstance(cuenta, CuentaPlazoFijo):
                        print("Esa cuenta no es de Plazo Fijo. Ingrese otra.")
                        continue

                    print(cuenta.acreditar_interes())
                    break

            elif opcion == "6":
                print(f"Saldo total en el banco: ${self.banco.saldo_total()}")


            elif opcion == "7":
                informe = InformeBanco(self.banco)
                print(informe.informe_totales())

                while True:
                    opcion = input("Desea guardar el informe? s/n: ").lower()

                    if opcion == 's':
                        informe.guardar_informe()
                        break

                    elif opcion == 'n':
                        break
                    
                    else:
                        print("Opción inválida")
                        continue
                    
            elif opcion == "8":
                clear()
                self.banco.ajustar_parametros()

            elif opcion == "9":
                clear()
                print("-------Aplicar costo de Mantenimiento---------")
                while True:
                    nro = int(input("Ingrese número de cuenta: "))
                    cuenta = self.banco.buscar_cuenta(nro)

                    if  isinstance(cuenta, CuentaCorriente):
                        if isinstance(cuenta.titular, ClientePersona):
                            costo = cuenta.costo_mantenimiento()
                            cuenta._saldo -= costo
                            print(f"Se descontó el costo de mantenimiento de ${costo}. Nuevo saldo de '{cuenta.titular.nombre}': ${cuenta._saldo}")
                            break

                        else:
                            costo = cuenta.costo_mantenimiento()
                            costo_descuento = cuenta.titular.descuento_mantenimiento(costo)
                            cuenta._saldo -= costo_descuento
                            print("10% de descuento aplicado")
                            print(f"Se descontó el costo de mantenimiento de ${costo_descuento}. Nuevo saldo de '{cuenta.titular.nombre}': ${cuenta._saldo}")
                            break

                    else:
                        print("No se aplica costo de mantenimiento a esta cuenta, intente de nuevo...")
                        continue
                    
            elif opcion == "10":
                clear()
                while True:
                    salida= input("Está seguro que desea salir? (s/n): ").lower()

                    if salida == 's':
                        exit('Hasta pronto!')

                    elif salida == 'n':
                        break

                    else:
                        print("Letra incorrecta, pulse de nuevo")

            else:
                clear()
                print("Opción inválida, intente nuevamente")
                continue