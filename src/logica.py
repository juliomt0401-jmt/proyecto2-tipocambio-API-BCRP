from decimal import Decimal
from api import obtener_compra, obtener_venta
from db import insertar_tipocambio, desactivar_activos, existen_cambios
from configuracion import FUENTE

def procesar_tipo_cambio(fecha):
    # --- Obtener valores ---
    compra = obtener_compra(fecha)
    venta = obtener_venta(fecha)

    compra = Decimal(str(compra)).quantize(Decimal('0.0001'))
    venta  = Decimal(str(venta)).quantize(Decimal('0.0001'))

    # Si no hay valores válidos, no grabamos nada
    if compra is None and venta is None:
        return

    # Verifica si existen cambios por grabar
    if not existen_cambios(fecha, compra, venta):
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
