from clientes import ClienteEmpresa, ClientePersona
from cuentas import CajaAhorro, CuentaCorriente, CuentaPlazoFijo
from banco import Banco
from datetime import date


class InformeBanco:
    def __init__(self, banco: Banco):
        self.banco = banco

    def informe_CC(self):
        total = 0
        texto = "Cuenta/s Corriente/s\n"
        for cuenta in self.banco.cuentas:
            if isinstance(cuenta, CuentaCorriente):
                total += cuenta.saldo
                texto += f"Nro Cuenta: {cuenta.numero} - Titular: {cuenta.titular.nombre} - Saldo: ${cuenta.saldo}\n"
        texto += f"Total de Cuentas Corrientes: ${total}\n\n"
        return texto, total

    def informe_CA(self):
        total = 0
        texto = "Cuenta/s Caja de Ahorro\n"
        for cuenta in self.banco.cuentas:
            if isinstance(cuenta, CajaAhorro):
                total += cuenta.saldo
                texto += f"Nro Cuenta: {cuenta.numero} - Titular: {cuenta.titular.nombre} - Saldo: ${cuenta.saldo}\n"
        texto += f"Total de Cajas de Ahorro: ${total}\n\n"
        return texto, total

    def informe_PF(self):
        total = 0
        fecha_actual = date.today()
        texto = "Cuenta/s Plazo Fijo\n"
        for cuenta in self.banco.cuentas:
            if isinstance(cuenta, CuentaPlazoFijo):
                total += cuenta.saldo
                interes = cuenta.saldo * cuenta.banco.tasa_interes
                total_acreditar = cuenta.saldo + interes
                texto += (
                    f"Nro Cuenta: {cuenta.numero}\n"
                    f"Cliente: {cuenta.titular.nombre}\n"
                    f"Fecha de creación: {fecha_actual}\n"
                    f"Fecha de vencimiento: {cuenta.fecha_vencimiento}\n"
                    f"Capital: ${cuenta.saldo}\n"
                    f"Tasa: {cuenta.banco.tasa_interes}\n"
                    f"Interés calculado: ${interes}\n"
                    f"Total a acreditar: ${total_acreditar}\n\n"
                )
        texto += f"Total de Plazos Fijos: ${total}\n\n"
        return texto, total

    def total_descubierto(self):
        total_descubierto = 0
        for c in self.banco.cuentas:
            if isinstance(c, CuentaCorriente) and c.saldo < 0:
                total_descubierto += abs(c.saldo)
        return f"Total descubierto: ${total_descubierto}\n", total_descubierto

    def clientes_personas(self):
        total_clientes = 0
        for c in self.banco.clientes:
            if isinstance(c, ClientePersona):
                total_clientes += 1
        return f"Total de clientes personas: {total_clientes}\n", total_clientes

    def clientes_empresas(self):
        total_empresas = 0
        for c in self.banco.clientes:
            if isinstance(c, ClienteEmpresa):
                total_empresas += 1
        return f"Total de clientes empresas: {total_empresas}\n", total_empresas


    def clientes_totales(self):
        empresa = 0
        personas = 0
   
        for e in self.banco.clientes:
            if isinstance(e, ClienteEmpresa):
                empresa += 1
        
        for c in self.banco.clientes:
            if isinstance(c, ClientePersona):
                personas += 1
                
        clientes_totales = empresa + personas
        
        return clientes_totales
                


    def saldo_total(self):
        saldo_total= 0 
        
        for c in self.banco.cuentas:
            saldo_total += c.saldo
        
        return saldo_total

    def informe_totales(self):
        secciones = [
            self.informe_CC(),
            self.informe_CA(),
            self.informe_PF(),
            self.total_descubierto(),
            self.clientes_personas(),
            self.clientes_empresas(),
        ]

        texto = "\n=== INFORME DE TOTALES ===\n\n"
        total_saldos = self.saldo_total()
  

        for contenido, total in secciones:
            texto += contenido + "\n"
        
        texto += (
            "---------------------------------\n"
            f"Total de clientes: {self.clientes_totales()}\n"
            f"Saldo total en el banco: ${total_saldos}\n"
        )
        return texto

    def guardar_informe(self):
        with open("c:\\Users\\Hijo Tigre\\Desktop\\Python\\CURSO-POO\\Banco\\informes.txt", "w", encoding="utf-8") as archivo:
            archivo.write(self.informe_totales())
        print(f"Informe guardado exitosamente!")
