from abc import ABC, abstractmethod
from datetime import date

class CuentaBase(ABC):
    @abstractmethod
    def __init__(self, numero, titular, saldo, banco):
        self.numero = numero
        self.titular = titular
        self._saldo = saldo
        self.banco = banco
        
    @abstractmethod
    def puede_extraer(self, monto):
        pass    

    @abstractmethod
    def costo_mantenimiento(self):
        pass    
        
    @property
    def saldo(self):
        return self._saldo 
           
    def depositar(self, monto):
        if monto <= 0:
             return 'Error: El monto a depositar debe ser mayor a 0'
        
        self._saldo += monto
        return f"Depósito exitoso de: ${monto}! El nuevo saldo de '{self.titular.nombre}' es de: ${self._saldo}"
    
    def extraer(self, monto):
        
        if monto <= 0:
            return "Error: El monto a retirar debe ser mayor que 0."
        
        puede = self.puede_extraer(monto)
        
        if puede:
            self._saldo -= monto
            return (f"Ha retirado: ${monto}! \n"
                    f"El nuevo saldo de '{self.titular.nombre}' -- Cuenta N°: {self.numero} -- es de: ${self._saldo}")
        
        
        elif not puede:
            if monto >= self._saldo:
                restante = self._saldo - monto
                return (f'Error: No cuenta con suficiente saldo. Le faltan: ${abs(restante)}...')

            return f"No se puede retirar dinero de la cuenta de '{self.titular.nombre}' por reglas del tipo de cuenta."
        
    
    def transferir(self, destino, monto):
        if monto <= 0:
             return 'Error: La transferencia debe ser mayor a 0'
        
        if monto > self._saldo:
            restante = self._saldo - monto
            return(f'Error de transferencia: No cuenta con suficiente saldo. Le faltan: ${abs(restante)}...')
        
        self._saldo -= monto
        destino._saldo += monto 
        
        return f'''Transferencia de ${monto} realizada con éxito!
                De '{self.titular.nombre}' hacia '{destino.titular.nombre}'
                Saldo actual: ${self._saldo}
                '''
                
class CajaAhorro(CuentaBase):
    def __init__(self, numero, titular, saldo, banco):
        super().__init__(numero, titular, saldo, banco)
        
    
    def puede_extraer(self, monto):
        #el saldo no puede ser negativo
        return monto <= self.saldo
    
    def costo_mantenimiento(self):
        return 0
          
class CuentaCorriente(CuentaBase):
    def __init__(self, numero, titular, saldo, banco, limite_descubierto):
        super().__init__(numero, titular, saldo, banco)
        self.limite_descubierto = limite_descubierto 
    
    def puede_extraer(self, monto):
        return monto <= self._saldo + self.limite_descubierto   #no se puede pasar el limite descubierto
        
    def costo_mantenimiento(self):
        return self.banco.costo_mantenimiento
    
class CuentaPlazoFijo(CuentaBase):
    def __init__(self, numero, titular, saldo, fecha_vencimiento, banco):
        super().__init__(numero, titular, saldo, banco)
        
        self.fecha_vencimiento = fecha_vencimiento
        
    def puede_extraer(self, monto):
        fecha_actual = date.today()
        return fecha_actual >= self.fecha_vencimiento and monto <= self._saldo  #fecha actual no puede superar a la del vencimiento
    
    def costo_mantenimiento(self):
        return 0  

    def acreditar_interes(self):
        interes = self._saldo * self.banco.tasa_interes #interes fijo del banco
        self._saldo += interes
        return f"Interés acreditado: ${interes}. Nuevo saldo de {self.titular.nombre}: ${self._saldo}"
    

