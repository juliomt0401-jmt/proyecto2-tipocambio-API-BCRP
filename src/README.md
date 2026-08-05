# API BCRP – Sistema de Registro de Tipo de Cambio con Vigencias

Este proyecto implementa un sistema confiable para consultar el tipo de cambio oficial del BCRP y registrar cada variación en una base de datos MySQL.  
Está diseñado para escenarios reales de alta volatilidad económica, donde el tipo de cambio puede cambiar varias veces durante el día y donde es crítico mantener un histórico preciso y ordenado.

## Finalidad del proyecto

Quienes hemos vivido épocas de crisis sabemos lo que significa ver el dólar cambiar:

- varias veces en una mañana,
- subir y bajar sin aviso,
- generar incertidumbre en operaciones financieras.

En esos contextos, los sistemas deben ser capaces de:

- consultar el tipo de cambio más de una vez al día,
- detectar variaciones intradía,
- registrar cada cambio con su vigencia,
- evitar reescritura de días pasados,
- mantener un histórico limpio y confiable.

Este proyecto resuelve exactamente ese problema.

## ¿Qué hace el sistema?

1. Consulta el tipo de cambio oficial del BCRP mediante API pública.
2. Verifica si existe variación respecto al valor vigente.
3. Si hay cambios:
   - cierra la vigencia anterior,
   - registra un nuevo tipo de cambio con fecha y fuente.
4. Permite ejecutar el proceso varias veces al día.
5. Ignora automáticamente fechas antiguas para proteger el histórico.
6. Detiene el programa si MySQL no está disponible.
7. Registra errores del API y del sistema.

## Arquitectura del proyecto

### API-BCRP-TipoCambio-main.py
- Obtiene la fecha del parámetro o del sistema.
- Valida si la fecha es procesable.
- Ejecuta el flujo principal.

### db.py
- Conexión a MySQL con manejo de errores.
- Lectura del tipo de cambio vigente.
- Verificación de cambios intradía.
- Inserción de nuevos registros.
- Actualización de vigencias.

### logica.py
- Consulta del tipo de cambio vía API.
- Validación de variación.
- Flujo de actualización de vigencias.

### api.py
- Llamado seguro a la API del BCRP.
- Manejo de errores y registro en log.

## Política de integridad temporal

Si la fecha argumento es menor a la fecha vigente, no se procesa.  
Esto evita:

- reabrir días pasados,
- alterar el histórico,
- generar vigencias inconsistentes,
- registrar datos fuera de orden.

## Escenarios soportados

- Variación intradía.
- Primer registro del día.
- Día nuevo.
- Fechas antiguas ignoradas.

## Uso

### Ejecutar con fecha específica:
python src/API-BCRP-TipoCambio-main.py 2026-07-25

### Ejecutar confecha del sistema:
python src/API-BCRP-TipoCambio-main.py

### Requisitos
- Python 3.10+
- MySQL 8+
- Librerías:
    mysql-connector-python
    requests
    decimal