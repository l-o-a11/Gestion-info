# Operaciones de persistencia para archivos JSON

import json
import os
from typing import Any, List


def load_data(filename: str) -> List[Dict[str, Any]]:
    """Carga los datos desde un archivo JSON.

    Si el archivo no existe, devuelve una lista vacía.
    Maneja JSON inválido mostrando mensaje pero no deteniendo la ejecución.

    Args:
        filename: Ruta al archivo JSON.

    Returns:
        Lista de registros (diccionarios). Lista vacía si hay error.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"  Advertencia: El archivo '{filename}' está dañado o contiene JSON inválido.")
        print("   Se iniciará con una lista vacía.")
        return []
    except Exception as e:
        print(f" Error al leer el archivo '{filename}': {e}")
        return []


def save_data(filename: str, data: List[Dict[str, Any]]) -> None:
    """Guarda los datos en un archivo JSON.

    Crea el directorio si no existe.

    Args:
        filename: Ruta al archivo JSON.
        data: Lista de registros a guardar.
    """
    try:
        directorio = os.path.dirname(filename)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f" Error al guardar el archivo '{filename}': {e}")