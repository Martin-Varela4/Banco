import sqlite3
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

NOMBRE_DB = "BD.db" 
RUTA_DB_COMPLETA = os.path.join(BASE_DIR, NOMBRE_DB) 

bd = RUTA_DB_COMPLETA 

def conectar_db():
    return sqlite3.connect(RUTA_DB_COMPLETA)



def tablas():
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS empleados (
            dni CHAR(8) PRIMARY KEY,
            usuario TEXT UNIQUE NOT NULL,
            contrasena TEXT NOT NULL,
            nombre TEXT NOT NULL,
            rol TEXT CHECK(rol IN ('admin', 'empleado')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clientes (
            dni CHAR(8) PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            telefono TEXT,
            direccion TEXT
        );

        CREATE TABLE IF NOT EXISTS cuentas (
            id INTEGER PRIMARY KEY,
            cliente_dni CHAR(8) NOT NULL,
            tipo TEXT CHECK(tipo IN ('Caja de Ahorro', 'Cuenta Corriente', 'Plazo Fijo')) NOT NULL,
            saldo REAL DEFAULT 0,
            estado TEXT DEFAULT 'ACTIVA', 
            FOREIGN KEY (cliente_dni) REFERENCES clientes(dni)
        );

        CREATE TABLE IF NOT EXISTS plazos_fijos (
            id INTEGER PRIMARY KEY,
            monto REAL NOT NULL,
            tasa_interes REAL NOT NULL,
            fecha_inicio TEXT NOT NULL,
            fecha_vencimiento TEXT NOT NULL,
            id_cuenta INTEGER NOT NULL,
            FOREIGN KEY(id_cuenta) REFERENCES cuentas(id)
        );
        
        
        CREATE TABLE IF NOT EXISTS cuentas_corrientes (
            id_cuenta INTEGER PRIMARY KEY,
            limite_descubierto REAL NOT NULL,
            FOREIGN KEY(id_cuenta) REFERENCES cuentas(id)
        );

        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY,
            id_cuenta INTEGER NOT NULL,
            tipo_movimiento TEXT NOT NULL, -- 'DEPOSITO', 'RETIRO', 'TRANSFERENCIA'
            cuenta_relacionada INTEGER,
            monto REAL NOT NULL,
            fecha_hora TEXT NOT NULL,
            FOREIGN KEY (id_cuenta) REFERENCES cuentas(id)
        );
    """)
    
    conn.commit()
    conn.close()


def verificar_login(usuario, contrasena):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE usuario=? AND contrasena=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()
    return resultado


# CRUD CLIENTES
def agregar_cliente(dni, nombre, apellido, contrasena, telefono, direccion):
    conn = conectar_db()
    cursor = conn.cursor()

    try:

        cursor.execute("SELECT COUNT(*) FROM clientes WHERE dni=?", (dni,))
        
        if cursor.fetchone()[0] > 0:
            raise ValueError(f"Ya existe un cliente registrado con el DNI: {dni}.")

        cursor.execute("""
        INSERT INTO clientes (dni, nombre, apellido, contrasena, telefono, direccion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (dni, nombre, apellido, contrasena, telefono, direccion))
        
        conn.commit()
        conn.close()

    except ValueError:
        raise
    

def eliminar_cliente(dni_cliente):
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM clientes WHERE dni=?", (dni_cliente,))
    count = cursor.fetchone()[0]
    
    
    try: 
        if count == 0:
                
                raise ValueError(f"Error: El DNI '{dni_cliente}' no se encuentra registrado.")

        
        cursor.execute("DELETE FROM clientes WHERE dni=?", (dni_cliente,))
        conn.commit()
        return True
    
    except ValueError:
        raise
    
    
    finally:
        conn.close()
    


def obtener_cliente_por_dni(dni):
    conn = conectar_db() 
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellido, contrasena, telefono, direccion FROM clientes WHERE dni=?", (dni,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado 

def actualizar_cliente(dni, nombre, apellido, contrasena, telefono, direccion):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes 
        SET nombre=?, apellido=?, contrasena=?, telefono=?, direccion=?
        WHERE dni=?
    """, (nombre, apellido, contrasena, telefono, direccion, dni))
    conn.commit()
    conn.close()



# CRUD CUENTAS
def agregar_cuenta(cliente_dni, tipo, saldo_inicial=0):
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cuentas (cliente_dni, tipo, saldo)
        VALUES (?, ?, ?)
    """, (cliente_dni, tipo, saldo_inicial))
    conn.commit()
    conn.close()

def obtener_cuentas():
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cuentas.id, clientes.nombre, clientes.apellido, cuentas.tipo, cuentas.saldo
        FROM cuentas
        JOIN clientes ON cuentas.cliente_dni = clientes.dni
    """)
    datos = cursor.fetchall()
    conn.close()
    return datos



def inicializar_empleado():
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM empleados")
    if cursor.fetchone()[0] == 0:
        try:
            cursor.execute("""
                INSERT INTO empleados VALUES (?, ?, ?, ?, ?)
            """, ('12345678', 'admin', '1234', 'Martín', 'admin'))
            conn.commit()
            print("Empleado 'admin' (pass: 1234) insertado.")
        except sqlite3.IntegrityError:
            pass
            
    conn.close()


def verificar_login(usuario, contrasena):
  
    conn = sqlite3.connect(bd)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, rol FROM empleados WHERE usuario=? AND contrasena=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        nombre, rol = resultado
        return nombre, rol 
    else:
        raise ValueError("Usuario o Contraseña incorrectos.")


#crud cuentas

def abrir_cuenta(cliente_dni, tipo_cuenta, saldo_inicial_str, parametro_especifico_str, fecha_vencimiento_str=None):
    
    from datetime import date, datetime
    
    try:
        saldo = float(saldo_inicial_str)
        param = float(parametro_especifico_str) if parametro_especifico_str and parametro_especifico_str.strip() else None
    except ValueError:
        raise ValueError("Saldo o parámetros deben ser números válidos.")
        
    conn = conectar_db() 
    cursor = conn.cursor()
    
    try:
        # verificar que el cliente exista
        cursor.execute("SELECT dni FROM clientes WHERE dni=?", (cliente_dni,))
        if cursor.fetchone() is None:
            raise ValueError(f"No existe un cliente con DNI: {cliente_dni}.")
            
        
        cursor.execute("""
            INSERT INTO cuentas (cliente_dni, tipo, saldo, estado)
            VALUES (?, ?, ?, 'ACTIVA')
        """, (cliente_dni, tipo_cuenta, saldo))
        
        id_cuenta = cursor.lastrowid
        

        if tipo_cuenta == "Cuenta Corriente" and param is not None:
            cursor.execute("""
                INSERT INTO cuentas_corrientes (id_cuenta, limite_descubierto)
                VALUES (?, ?)
            """, (id_cuenta, param))
            
        elif tipo_cuenta == "Plazo Fijo":
            
            if param is None:
                 raise ValueError("Se requiere la Tasa de Interés para el Plazo Fijo.")
            
           
            if not fecha_vencimiento_str or not fecha_vencimiento_str.strip():
                raise ValueError("Se requiere una fecha de vencimiento para el Plazo Fijo.")
                
            fecha_inicio = date.today().strftime('%Y-%m-%d')
            tasa_interes = param 
            
            try:
                fecha_vencimiento_obj = datetime.strptime(fecha_vencimiento_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("El formato de fecha de vencimiento es inválido (debe ser YYYY-MM-DD).")
                
            if fecha_vencimiento_obj <= date.today():
                raise ValueError("La fecha de vencimiento debe ser posterior al día de hoy.")
            
            # inserción en Plazo Fijo
            cursor.execute("""
                INSERT INTO plazos_fijos (id_cuenta, monto, tasa_interes, fecha_inicio, fecha_vencimiento)
                VALUES (?, ?, ?, ?, ?)
            """, (id_cuenta, saldo, tasa_interes, fecha_inicio, fecha_vencimiento_str))

        
        conn.commit()
        return id_cuenta
        
    finally:
        conn.close()


def actualizar_cuenta_parametros(id_cuenta, dni_cliente, nuevo_saldo_str, param_nombre, param_valor_str):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
       
        cursor.execute("SELECT id FROM cuentas WHERE id=? AND cliente_dni=?", (id_cuenta, dni_cliente))
        
        if cursor.fetchone() is None:
            
            cursor.execute("SELECT id FROM cuentas WHERE id=?", (id_cuenta,))
            if cursor.fetchone() is None:
                raise ValueError(f"Error: La cuenta con ID '{id_cuenta}' no existe en la base de datos.")
            else:
                raise ValueError(f"Error: La cuenta '{id_cuenta}' NO pertenece al cliente con DNI '{dni_cliente}'.")

      
        try:
            saldo = float(nuevo_saldo_str)
        except ValueError:
            raise ValueError("El saldo debe ser un número válido.")

       
        cursor.execute("UPDATE cuentas SET saldo=? WHERE id=?", (saldo, id_cuenta))
        
       
        if param_nombre and param_valor_str:
            try:
                param_valor = float(param_valor_str)
            except ValueError:
                raise ValueError("El parámetro (Límite/Tasa) debe ser un número válido.")

            if param_nombre == "limite_descubierto":
                cursor.execute("UPDATE cuentas_corrientes SET limite_descubierto=? WHERE id_cuenta=?", 
                               (param_valor, id_cuenta))
                
                if cursor.rowcount == 0:
                    raise ValueError(f"La cuenta {id_cuenta} no es una Cuenta Corriente.")

            elif param_nombre == "tasa_interes":
                cursor.execute("UPDATE plazos_fijos SET tasa_interes=? WHERE id_cuenta=?", 
                               (param_valor, id_cuenta))
                if cursor.rowcount == 0:
                    raise ValueError(f"La cuenta {id_cuenta} no es un Plazo Fijo.")
        
        conn.commit()
        
    except ValueError:
        raise 
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"Error de base de datos al actualizar: {e}")
    finally:
        conn.close()


def cerrar_cuenta(id_cuenta):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT saldo FROM cuentas WHERE id=?", (id_cuenta,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            raise ValueError(f"La cuenta ID {id_cuenta} no existe.")
            
        saldo_actual = resultado[0]
        
    
        if saldo_actual != 0.00: 
            raise ValueError(f"El saldo de la cuenta debe ser cero (${saldo_actual}) para poder cerrarla.")
            
   
        cursor.execute("UPDATE cuentas SET estado='CERRADA' WHERE id=?", (id_cuenta,))
        
        conn.commit()
        
    finally:
        conn.close()



def verificar_existencia_dni(dni):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT 1 FROM clientes WHERE dni=?", (dni,))
        # Si fetchone() devuelve algo, significa que el cliente existe.
        return cursor.fetchone() is not None 
        
    except Exception as e:
        raise Exception(f"Error de consulta de existencia: {e}")
        
    finally:
        conn.close()
# ----------------------------APARTADO DE MOVIMIENTOS--------------------------.

def ejecutar_deposito(id_cuenta, monto):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
    
        cursor.execute("SELECT saldo FROM cuentas WHERE id=? AND estado='ACTIVA'", (id_cuenta,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            raise ValueError(f"La cuenta ID {id_cuenta} no existe o no está activa.")
        
        saldo_actual = resultado[0]
        nuevo_saldo = saldo_actual + monto
        
        
        cursor.execute("UPDATE cuentas SET saldo=? WHERE id=?", 
                       (nuevo_saldo, id_cuenta))
        
        
        cursor.execute("""
            INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto, fecha_hora)
            VALUES (?, ?, ?, ?)
        """, (id_cuenta, 'DEPOSITO', monto, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        
        conn.commit()
        
    except ValueError:
        raise
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error en depósito: {e}")
    finally:
        conn.close()


def ejecutar_extraccion(id_cuenta, monto):
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
    
        cursor.execute("SELECT saldo, tipo, cliente_dni FROM cuentas WHERE id=? AND estado='ACTIVA'", (id_cuenta,))
        resultado_cuenta = cursor.fetchone()
        
        if resultado_cuenta is None:
            raise ValueError(f"La cuenta ID {id_cuenta} no existe o no está activa.")
        
        saldo_actual, tipo_cuenta, dni_cliente = resultado_cuenta
        nuevo_saldo = saldo_actual - monto
        
        
        cursor.execute("SELECT nombre FROM clientes WHERE dni=?", (dni_cliente,))
        resultado_cliente = cursor.fetchone()
        
        if resultado_cliente is None:

            raise RuntimeError(f"Error de integridad de datos: Cliente (DNI: {dni_cliente}) no encontrado.")
            
        nombre_cliente = resultado_cliente[0]
        
       
        if tipo_cuenta == 'Cuenta Corriente':
            cursor.execute("SELECT limite_descubierto FROM cuentas_corrientes WHERE id_cuenta=?", (id_cuenta,))
            limite = cursor.fetchone()
            
            limite_descubierto = 0.0
            if limite is not None:
                limite_descubierto = limite[0]
            
            saldo_minimo_permitido = -limite_descubierto 
            
            if nuevo_saldo < saldo_minimo_permitido:
                raise ValueError(f"Extracción rechazada. Supera el límite de descubierto de ${limite_descubierto:.2f}.")

        elif nuevo_saldo < 0:
            raise ValueError("Saldo insuficiente. El saldo no puede ser negativo.")

       
        cursor.execute("UPDATE cuentas SET saldo=? WHERE id=?", (nuevo_saldo, id_cuenta))
        
        cursor.execute("INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto, fecha_hora) VALUES (?, ?, ?, ?)", 
                       (id_cuenta, 'EXTRACCION', monto, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        conn.commit()
        
        
        return nuevo_saldo, dni_cliente, nombre_cliente
        
    except ValueError:
        conn.rollback()
        raise 
    except sqlite3.Error as e:
        print(f"error sqlite en extracción: {e}",)
        conn.rollback()
        raise RuntimeError(f"Error de base de datos al realizar la extracción: {e}")
    except Exception as e:

        conn.rollback()
        raise Exception(f"Fallo inesperado en la extracción: {e}")
    finally:
        conn.close()


def ejecutar_transferencia(id_origen, id_destino, monto):
    conn = conectar_db() 
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT saldo, tipo FROM cuentas WHERE id=? AND estado='ACTIVA'", (id_origen,))
        resultado_origen = cursor.fetchone()
        
        if resultado_origen is None:
            raise ValueError(f"La cuenta de origen ID {id_origen} no existe o no está activa.")
        
        saldo_actual_origen, tipo_origen = resultado_origen

        cursor.execute("SELECT saldo FROM cuentas WHERE id=? AND estado='ACTIVA'", (id_destino,))
        resultado_destino = cursor.fetchone()
        
        if resultado_destino is None:
            raise ValueError(f"La cuenta de destino ID {id_destino} no existe o no está activa.")
            
        saldo_actual_destino = resultado_destino[0]
        
        #saldo insuficiente
        
        nuevo_saldo_origen = saldo_actual_origen - monto
        
        if tipo_origen == 'Cuenta Corriente':
            cursor.execute("SELECT limite_descubierto FROM cuentas_corrientes WHERE id_cuenta=?", (id_origen,))
            limite = cursor.fetchone()
            limite_descubierto = limite[0] if limite else 0
            saldo_minimo_permitido = -limite_descubierto
            
            if nuevo_saldo_origen < saldo_minimo_permitido:
                raise ValueError(f"Transferencia rechazada. Supera el límite de descubierto de ${limite_descubierto:.2f} en la cuenta de origen.")
        
        elif nuevo_saldo_origen < 0:

            raise ValueError("Saldo insuficiente en la cuenta de origen.")
        

        cursor.execute("UPDATE cuentas SET saldo=? WHERE id=?", (nuevo_saldo_origen, id_origen))
        
        # actualiza suma de mont
        nuevo_saldo_destino = saldo_actual_destino + monto
        cursor.execute("UPDATE cuentas SET saldo=? WHERE id=?", (nuevo_saldo_destino, id_destino))
        
      
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        
        cursor.execute("""
            INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto, fecha_hora, cuenta_relacionada)
            VALUES (?, ?, ?, ?, ?)
        """, (id_origen, 'TRANSFERENCIA_SALIDA', monto, fecha_hora, id_destino))
        
    
        cursor.execute("""
            INSERT INTO movimientos (id_cuenta, tipo_movimiento, monto, fecha_hora, cuenta_relacionada)
            VALUES (?, ?, ?, ?, ?)
        """, (id_destino, 'TRANSFERENCIA_ENTRADA', monto, fecha_hora, id_origen))
        
        conn.commit()
        
    except ValueError:
        conn.rollback()
        raise
    except Exception as e:
        conn.rollback() 
        raise Exception(f"Error durante la transferencia: {e}")
    finally:
        conn.close()
        

def obtener_movimientos_filtrados(tipo_movimiento, fecha_desde, fecha_hasta):
 
    conn = conectar_db()
    cursor = conn.cursor()
    
    # consulta
    query = """
    SELECT 
        id_cuenta, 
        tipo_movimiento, 
        monto, 
        fecha_hora, 
        cuenta_relacionada, 
        id 
    FROM movimientos
    WHERE fecha_hora >= ? AND fecha_hora < ? 
    """
    parametros = [fecha_desde, fecha_hasta]
    
 
    if tipo_movimiento != "TODOS":
        query += " AND tipo_movimiento = ?"
        parametros.append(tipo_movimiento)
        
  
    query += " ORDER BY fecha_hora DESC"
    
    try:
        cursor.execute(query, tuple(parametros))
        movimientos = cursor.fetchall()
        return movimientos
        
    except sqlite3.Error as e:
        raise Exception(f"Error de SQL al consultar movimientos: {e}")
    finally:
        conn.close()


tablas()
inicializar_empleado()