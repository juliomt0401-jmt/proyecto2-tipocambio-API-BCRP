from api import obtener_compra, obtener_venta
from db import insertar_tipocambio, desactivar_activos
from configuracion import FUENTE

def procesar_tipo_cambio(fecha):
    # --- Obtener valores ---
    compra = obtener_compra(fecha)
    venta = obtener_venta(fecha)

    # Si no hay valores válidos, no grabamos nada
    if compra is None and venta is None:
        return

    # Desactivar el registro activo anterior
    desactivar_activos()

    # Insertar nuevo tipo de cambio
    insertar_tipocambio(
        compra,
        venta,
        fecha,
        FUENTE
    )
