import requests
from datetime import datetime, timedelta
from configuracion import API_COMPRA, API_VENTA, DIAS_RANGO
from db import insertar_log

def construir_url(base_url, fecha):
    fecha_inicio = fecha - timedelta(days=DIAS_RANGO)
    fecha_fin = fecha
    return f"{base_url}/{fecha_inicio}/{fecha_fin}"

def llamar_api(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        insertar_log(
            datetime.now(),
            url,
            "ERROR",
            f"Error llamando API: {e}"
        )
        return None

def extraer_valor(json_data, url):
    try:
        for periodo in reversed(json_data["periods"]):
            valor = periodo["values"][0]
            if valor != "n.d.":
                insertar_log(
                    datetime.now(),
                    url,
                    "OK",
                    f"Valor obtenido: {valor}"
                )
                return float(valor)
        # API respondió, pero no hay valor
        insertar_log(
            datetime.now(),
            url,
            "OK",
            "API respondió pero no hay valor (n.d.)"
        )
        return None
    except (KeyError, IndexError, ValueError) as e:
        insertar_log(
            datetime.now(),
            url,
            "ERROR",
            f"Error extrayendo valor: {e}"
        )
        return None

def obtener_compra(fecha):
    url = construir_url(API_COMPRA, fecha)
    data = llamar_api(url)
    return extraer_valor(data, url) if data else None

def obtener_venta(fecha):
    url = construir_url(API_VENTA, fecha)
    data = llamar_api(url)
    return extraer_valor(data, url) if data else None
