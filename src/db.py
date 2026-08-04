import mysql.connector
from configuracion import MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB

def conectar():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASS,
        database=MYSQL_DB
    )

# -----------------------------
#   Tabla Tipo de Cambio (tipocambio)
# -----------------------------

def desactivar_activos():
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        UPDATE tipocambio
        SET Estado = 'I', FinVigencia = NOW()
        WHERE Estado = 'A'
    """

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

def insertar_tipocambio(compra, venta, fecha, api):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO tipocambio (Compra, Venta, InicioVigencia, API)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (compra, venta, fecha, api))
    conn.commit()

    cursor.close()
    conn.close()

# -----------------------------
#   Tabla log (logapi)
# -----------------------------

def insertar_log(fecha, url, resultado, mensaje):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
        INSERT INTO logapi (Fecha, URL, Resultado, Mensaje)
        VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (fecha, url, resultado, mensaje))
    conn.commit()

    cursor.close()
    conn.close()
