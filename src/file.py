# funciones de load_data y save_data para manejar archivos JSON

import json 
import os

def load_data(filename):
    """Carga los datos desde un archivo JSON. Si el archivo no existe, devuelve una lista vacía."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, devolver lista vacía
        return []
    except json.JSONDecodeError:
        # Si el archivo está dañado, mostrar mensaje y devolver lista vacía
        print(f"  Advertencia: El archivo '{filename}' está dañado o contiene JSON inválido.")
        print("   Se iniciará con una lista vacía.")
        return []
    except Exception as e:
        # Otros errores de lectura
        print(f" Error al leer el archivo '{filename}': {e}")
        return []

def save_data(filename, data):
    """Guarda los datos en un archivo JSON."""
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(filename)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Guardar datos en JSON
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f" Datos guardados correctamente en '{filename}'")
    except IOError as e:
        # Error de escritura
        print(f" Error al guardar en '{filename}': {e}")
    except Exception as e:
        # Otros errores
        print(f" Error inesperado al guardar: {e}")
        
