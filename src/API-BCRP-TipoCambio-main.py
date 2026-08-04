from datetime import datetime
import sys
from logica import procesar_tipo_cambio

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
    procesar_tipo_cambio(fecha_parametro)

if __name__ == "__main__":
    main()
