import sys
from datetime import datetime
from db import obtener_tipo_cambio_actual
from logica import procesar_tipo_cambio

def ignorar_fecha_antigua(fecha_parametro):
    vigente = obtener_tipo_cambio_actual()

    # Si no hay registro vigente → primera ejecución del sistema
    if vigente is None:
        return

    fecha_vigente, compra_vigente, venta_vigente = vigente
    if isinstance(fecha_vigente, datetime):
        fecha_vigente = fecha_vigente.date()

    # Política definida por ti:
    # Si la fecha argumento es menor a la vigente → ignorar
    if fecha_parametro < fecha_vigente:
        print(f"Fecha {fecha_parametro} ignorada: No se puede grabar valores de tipo de cambio de fechas antiguas. La fecha vigente es {fecha_vigente}.")
        sys.exit(1)

    return

def obtener_fecha_parametro():
    # ¿Se pasó parámetro?
    if len(sys.argv) > 1:
        fecha_str = sys.argv[1]
        try:
            # Validar formato AAAA-MM-DD
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            return fecha
        except ValueError:
            print("ERROR: La fecha debe tener formato AAAA-MM-DD y ser válida.")
            sys.exit(1)

    # Si no hay parámetro → fecha del sistema
    return datetime.now().date()

def main():
    fecha_parametro = obtener_fecha_parametro()
    ignorar_fecha_antigua(fecha_parametro)
    procesar_tipo_cambio(fecha_parametro)

if __name__ == "__main__":
    main()
