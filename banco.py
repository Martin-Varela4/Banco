class Banco():
    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = []
        self.cuentas = []
        self.tasa_interes = 0.05 #5%
        self.costo_mantenimiento = 500
        self.comision_transferencia = 50

    def crear_cuenta(self):
        pass


    def alta_cliente(self, cliente):
        self.clientes.append(cliente)

        return f'Alta de cliente exitoso: {cliente.nombre}'

    def alta_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

        return f'Alta de cuenta exitosa, numero: {cuenta.numero}'

    def buscar_cuenta(self, nro_cuenta):
        for cuenta in self.cuentas:
            if cuenta.numero == nro_cuenta:
                return cuenta
        return None

    def transferir(self, nro_origen, nro_destino, monto):
        cuenta_origen = self.buscar_cuenta(nro_origen)
        cuenta_destino = self.buscar_cuenta(nro_destino)

        #se usa elmétodo transferir de CuentaBase
        
        if cuenta_origen.titular != cuenta_destino.titular:
            print(f"Comisión fija de: ${self.comision_transferencia} aplicada")
            monto_total = monto + self.comision_transferencia
            return cuenta_origen.transferir(cuenta_destino, monto_total) #Con comisión
        
        return cuenta_origen.transferir(cuenta_destino, monto) #Sin comisión
    
    def saldo_total(self):
        saldo_total = 0
    
        for c in self.cuentas:
            saldo_total += c._saldo
            
        return saldo_total
    
    def ajustar_parametros(self):
        while True:
            
            print("\n--- Ajustar Parámetros del Banco ---")
            
            menu = {"1." : f"Ajustar tasa de interés anual actual: {self.tasa_interes * 100}%",
                    "2." : f"Ajustar costo de mantenimiento actual: ${self.costo_mantenimiento}",
                    "3." : f"Ajustar comisión por transferencia actual: {self.comision_transferencia}",
                    "4." : "Cancelar"}
            
            for i,j in menu.items():
                print(i,j)
            
            opcion = input("\nIngrese número de parámetro a cambiar (1-4): ")
            
            if opcion == "1":
                nueva_tasa = float(input("Ingrese nueva tasa (ej. 0.07 para 7%): "))
                self.tasa_interes = nueva_tasa
            elif opcion == "2":
                nuevo_costo = float(input("Ingrese nuevo costo de mantenimiento: "))
                self.costo_mantenimiento = nuevo_costo
            elif opcion == "3":
                nueva_comision = float(input("Ingrese nueva comisión por transferencia: "))
                self.comision_transferencia = nueva_comision
            elif opcion == "4":
                print("No se realizaron cambios.")
                break
                
            else:
                print("Opción inválida.")
                continue