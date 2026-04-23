# # print ("Sistema listo")  
from colorama import init, Fore, Style, Back
import os

# init(autoreset=True)

# # Crear adgoritmo de almacenamiento de datos en lista y tiene, manejo de funciones, orden de mayor a menor, listas, menu interactivo y manejo de errores

# print (Fore.CYAN +"===================================================================================")
# print( Back.BLUE +"======================Manejo de listas y errores====================================")
# print (Style.BRIGHT + Fore.WHITE +"===================================================================================")
# try: 
#     print("Bienvenido al sistema de gestión de información")
# except ValueError:
#     print("Error: Valor no válido. Por favor, ingrese un número.")

from service import GestorRegistros
from file import load_data, save_data

init(autoreset=True)

# Ruta del archivo JSON
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'records.json')

def mostrar_menu():
    """Muestra el menú principal"""
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + "SISTEMA DE GESTIÓN DE INFORMACIÓN")
    print(Fore.CYAN + "=" * 70)
    print(Fore.GREEN + "1. Crear nuevo registro")
    print(Fore.GREEN + "2. Listar todos los registros")
    print(Fore.GREEN + "3. Buscar registro por ID")
    print(Fore.GREEN + "4. Ver estadísticas")
    print(Fore.GREEN + "5. Salir")
    print(Fore.CYAN + "=" * 70)


def crear_registro_interactivo(gestor):
    """Permite crear un registro interactivamente"""
    print("\n" + Fore.YELLOW + "--- CREAR NUEVO REGISTRO ---")
    
    try:
        id_persona = input("Ingrese ID (número): ").strip()
        nombre = input("Ingrese nombre: ").strip()
        email = input("Ingrese email: ").strip()
        edad = input("Ingrese edad: ").strip()
        
        exito, mensaje, registro = gestor.crear_registro(id_persona, nombre, email, edad)
        
        if exito:
            print(Fore.GREEN + f" {mensaje}")
            print(f"  ID: {registro['id']}")
            print(f"  Nombre: {registro['nombre']}")
            print(f"  Email: {registro['email']}")
            print(f"  Edad: {registro['edad']} años")
            
            # Guardar datos en archivo JSON
            save_data(DATA_FILE, gestor.listar_registros())
        else:
            print(Fore.RED + f" {mensaje}")
    
    except Exception as e:
        print(Fore.RED + f" Error inesperado: {e}")


def listar_registros_interactivo(gestor):
    """Muestra todos los registros registrados"""
    registros = gestor.listar_registros()
    
    if not registros:
        print(Fore.YELLOW + "No hay registros registrados aún.")
        return
    
    print(" " + Fore.YELLOW + "LISTA DE REGISTROS")
    print("-" * 70)
    print(f"{'ID':<5} {'Nombre':<20} {'Email':<25} {'Edad':<5}")
    print("-" * 70)
    
    for registro in registros:
        print(f"{registro['id']:<5} {registro['nombre']:<20} {registro['email']:<25} {registro['edad']:<5}")
    
    print("-" * 70)
    print(Fore.CYAN + f"Total de registros: {gestor.obtener_total_registros()}")
    print("=" * 70)


def buscar_registro_interactivo(gestor):
    """Busca un registro por ID"""
    try:
        id_buscar = int(input("\nIngrese ID a buscar: ").strip())
        registro = gestor.obtener_registro_por_id(id_buscar)
        
        if registro:
            print(Fore.GREEN + " Registro encontrado:")
            print(f"  ID: {registro['id']}")
            print(f"  Nombre: {registro['nombre']}")
            print(f"  Email: {registro['email']}")
            print(f"  Edad: {registro['edad']} años")
        else:
            print(Fore.RED + f" No se encontró registro con ID {id_buscar}")
    
    except ValueError:
        print(Fore.RED + " El ID debe ser un número")
    except Exception as e:
        print(Fore.RED + f" Error: {e}")


def mostrar_estadisticas(gestor):
    """Muestra estadísticas del sistema"""
    total = gestor.obtener_total_registros()
    registros = gestor.listar_registros()
    
    print("" + Fore.CYAN + "ESTADÍSTICAS DEL SISTEMA")
    print("-" * 70)
    print(Fore.GREEN + f"Total de registros: {total}")
    
    if total > 0:
        edades = [r['edad'] for r in registros]
        promedio_edad = sum(edades) / len(edades)
        print(f"Edad promedio: {promedio_edad:.1f} años")
        print(f"Edad mínima: {min(edades)} años")
        print(f"Edad máxima: {max(edades)} años")
    
    print("=" * 70)


def main():
    """Función principal del programa"""
    print(Fore.MAGENTA + Style.BRIGHT + "\n¡Bienvenido al Sistema de Gestión de Información!\n")
    
    gestor = GestorRegistros()
    
    # Cargar datos desde archivo JSON
    print(Fore.CYAN + " Cargando datos desde el archivo...")
    registros_cargados = load_data(DATA_FILE)
    
    if registros_cargados:
        print(Fore.GREEN + f" Se cargaron {len(registros_cargados)} registros desde el archivo.\n")
        # Restaurar registros en el gestor
        for registro in registros_cargados:
            gestor.registros.append(registro)
            gestor.ids_unicos.add(registro['id'])
            gestor.emails_unicos.add(registro['email'])
    else:
        print(Fore.YELLOW + "  No hay registros previos. Se inicia con lista vacía.\n")
    
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            crear_registro_interactivo(gestor)
        
        elif opcion == "2":
            listar_registros_interactivo(gestor)
        
        elif opcion == "3":
            buscar_registro_interactivo(gestor)
        
        elif opcion == "4":
            mostrar_estadisticas(gestor)
        
        elif opcion == "5":
            print(Fore.MAGENTA + Style.BRIGHT + "\n¡Hasta luego!\n")
            break
        
        else:
            print(Fore.RED + " Opción no válida. Por favor, seleccione entre 1 y 5")
        
        input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()
