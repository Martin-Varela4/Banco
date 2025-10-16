class Cliente():
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni
        
    def descuento_mantenimiento(self, costo):
        return costo
    
class ClientePersona(Cliente):
    pass

class ClienteEmpresa(Cliente):
    pass

    def descuento_mantenimiento(self, costo):
        return costo * 0.9 