import os
from clientes import ClienteEmpresa, ClientePersona
from cuentas import CajaAhorro, CuentaCorriente, CuentaPlazoFijo, CuentaBase
from banco import Banco
from datetime import date
from informes import InformeBanco

def clear():
    if os.name == "nt":
        os.system("cls")
        
def main():  
    
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
    cc2 = CuentaCorriente(2, cliente3, -7400, banco, limite_descubierto=10000)
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
    
    

    # menú principal
    menu = {"1." : "Ver saldos",
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
            for cuenta in banco.cuentas:
                print(f"Cuenta N°: {cuenta.numero} - Titular: '{cuenta.titular.nombre}' --> Saldo: ${cuenta.saldo}")

        elif opcion == "2":
            nro = int(input("Número de cuenta: "))
            monto = float(input("Monto a depositar: "))
            cuenta = banco.buscar_cuenta(nro)
            if cuenta:
                print(cuenta.depositar(monto))
            else:
                print("Cuenta no encontrada.")

        elif opcion == "3":
            clear()
            print("---Extracción---")
            while True:
                nro = int(input("Ingrese el número de cuenta: N°"))
                cuenta = banco.buscar_cuenta(nro)

                if cuenta:
                    break
                else:
                    print("Cuenta no encontrada. Ingrese otra: ")
            
            while True:
                monto = float(input("Monto a extraer: $"))

                if monto <= 0:
                    print("El monto deber ser positivo, ingrese de nuevo")

                else:
                    print(cuenta.extraer(monto))
                    break

        elif opcion == "4": 
            clear()
            print("\n------TRANSFERENCIA------")
            while True:
                origen = int(input("Cuenta origen: "))
                destino = int(input("Cuenta destino: "))
                monto = float(input("Monto a transferir: $"))

                if monto <= 0:
                    print("Debe ingresar un monto válido mayor a 0.")
                    continue
               
                cuenta_origen = banco.buscar_cuenta(origen)
                cuenta_destino = banco.buscar_cuenta(destino)

                if not cuenta_origen or not cuenta_destino:
                    print("Una de las cuentas no existe, ingrese nuevamente\n")
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
                    print(f"\n{banco.transferir(origen, destino, monto)}") #metodo transferir recien de la clase banco
                    break

        elif opcion == "5":
            clear()
            print("---Areditar Interés----")
            while True:
                nro = int(input("Número de cuenta (Plazo Fijo): "))
                cuenta = banco.buscar_cuenta(nro)

                if cuenta:
                    break
                else:
                    print("Cuenta no encontrada. Ingrese otra: ")
                    
            if isinstance(cuenta, CuentaPlazoFijo):
                print(cuenta.acreditar_interes())
            else:
                print("Esa cuenta no es de Plazo Fijo.")

        elif opcion == "6":
            print(f"Saldo total en el banco: ${banco.saldo_total()}")


        elif opcion == "7":
            informe = InformeBanco(banco)
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
            banco.ajustar_parametros()
            
        elif opcion == "9":
            clear()
            print("-------Aplicar costo de Mantenimiento---------")
            while True:
                nro = int(input("Ingrese número de cuenta: "))
                cuenta = banco.buscar_cuenta(nro)

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
               
                            
if __name__ == "__main__":
    main()