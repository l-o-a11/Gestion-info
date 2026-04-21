# Gestion Info

Sistema de gestión de información en Python.

## Requisitos

- Python 3.7+

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/l-o-a11/gestion-info.git
cd gestion-info
```

2. (Opcional) Crear un entorno virtual:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. Instalar dependencias (si las hay):

```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar el programa:

```bash
python src/main.py
```

## Estructura del Proyecto

- `src/` - Código fuente principal
  - `main.py` - Punto de entrada del programa
  - `menu.py` - Interfaz de menú
  - `service.py` - Servicios principales
  - `validate.py` - Validaciones
  - `integration.py` - Integraciones
  - `file.py` - Manejo de archivos

- `data/` - Datos del programa
  - `records.json` - Registros de datos

- `test/` - Pruebas unitarias
  - `tests.py` - Suite de pruebas

## Ejecución de Pruebas

```bash
python -m pytest test/tests.py
```

## Licencia

MIT
