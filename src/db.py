import sys
import mysql.connector
from configuracion import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB

def conectar():
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            database=MYSQL_DB
        )
    except Exception as e:
        print(f"ERROR: No se pudo conectar a MySQL. Detalle: {e}")
        sys.exit(1)

# -----------------------------
#   Verificación si cambió el tipo de cambio (tabla tipocambio)
# -----------------------------
def obtener_tipo_cambio_actual():
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        SELECT InicioVigencia, compra, venta
        FROM tipocambio
        WHERE Estado = 'A'
    """
    cursor.execute(sql)
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    return resultado

def existen_cambios(fecha, compra, venta):
    conn = conectar()
    cursor = conn.cursor()
    sql = """
        SELECT compra, venta
        FROM tipocambio
        WHERE InicioVigencia = %s and Estado = 'A'
    """
    cursor.execute(sql, (fecha,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    # Si no existe registro → hay cambios por grabar
    if resultado is None:
        return True

    compra_bd, venta_bd = resultado

    # Si existe registro, comparar valores
    if compra_bd != compra or venta_bd != venta:
        return True  # hubo variación

    return False  # no hubo variación


# -----------------------------
#   Tabla Tipo de Cambio (tipocambio)
# -----------------------------

def desactivar_activos():
    sql = """
        UPDATE tipocambio
        SET Estado = 'I', FinVigencia = NOW()
        WHERE Estado = 'A'
    """
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print(f"ERROR: No se pudo desactivar los registros. Sentencia: {sql}. Detalle: {e}")
        sys.exit(1)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def insertar_tipocambio(compra, venta, fecha, api):
    sql = """
        INSERT INTO tipocambio (Compra, Venta, InicioVigencia, API)
        VALUES (%s, %s, %s, %s)
    """
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (compra, venta, fecha, api))
        conn.commit()
    except Exception as e:
        print(f"ERROR: No se pudo insertar el registro de tipo de cambio. Sentencia: {sql}. Detalle: {e}")
        sys.exit(1)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

# -----------------------------
#   Tabla log (logapi)
# -----------------------------

def insertar_log(fecha, url, resultado, mensaje):
    sql = """
        INSERT INTO logapi (Fecha, URL, Resultado, Mensaje)
        VALUES (%s, %s, %s, %s)
    """
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (fecha, url, resultado, mensaje))
        conn.commit()
    except Exception as e:
        print(f"ERROR: No se pudo insertar el registro de log. Sentencia: {sql}. Detalle: {e}")
        sys.exit(1)
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
