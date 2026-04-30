from colorama import Fore, Style, init
import os
from typing import Optional

from file import save_data
from service import GestorRegistros
from integration import ManagerReportes

init(autoreset=True)


def mostrar_menu() -> None:
    """Muestra el menú principal."""
    print(Fore.CYAN + "=" * 70)
    print(Fore.CYAN + "SISTEMA DE GESTIÓN DE INFORMACIÓN")
    print(Fore.CYAN + "=" * 70)
    print(Fore.GREEN + "1. Crear nuevo registro")
    print(Fore.GREEN + "2. Listar todos los registros")
    print(Fore.GREEN + "3. Buscar registro por ID")
    print(Fore.GREEN + "4. Actualizar registro por ID")
    print(Fore.GREEN + "5. Eliminar registro por ID")
    print(Fore.GREEN + "6. Exportar registros a CSV")
    print(Fore.GREEN + "7. Filtrar y ordenar registros")
    print(Fore.GREEN + "8. Salir")
    print(Fore.CYAN + "=" * 70)


def new_register_interactivo(gestor: GestorRegistros, data_file: str) -> None:
    """Permite crear un registro interactivamente.

    Args:
        gestor: Instancia del gestor de registros.
        data_file: Ruta al archivo de datos para persistencia.
    """
    print("\n" + Fore.YELLOW + "--- CREAR NUEVO REGISTRO ---")

    try:
        id_persona = input("Ingrese ID (número): ").strip()
        nombre = input("Ingrese nombre: ").strip()
        email = input("Ingrese email: ").strip()
        edad = input("Ingrese edad: ").strip()

        exito, mensaje, registro = gestor.new_register(id_persona, nombre, email, edad)

        if exito:
            print(Fore.GREEN + f" {mensaje}")
            print(f"  ID: {registro['id']}")
            print(f"  Nombre: {registro['nombre']}")
            print(f"  Email: {registro['email']}")
            print(f"  Edad: {registro['edad']} años")

            save_data(data_file, gestor.list_records())
        else:
            print(Fore.RED + f" {mensaje}")

    except Exception as e:
        print(Fore.RED + f" Error inesperado: {e}")


def list_records_interactivo(gestor: GestorRegistros) -> None:
    """Muestra todos los registros registrados.

    Args:
        gestor: Instancia del gestor de registros.
    """
    registros = gestor.list_records()

    if not registros:
        print(Fore.YELLOW + "No hay registros registrados aún.")
        return

    print(" " + Fore.YELLOW + "LISTA DE REGISTROS")
    print("-" * 70)
    print(f"{'ID':<5} {'Nombre':<20} {'Email':<25} {'Edad':<5}")
    print("-" * 70)

    for registro in registros:
        print(f"{registro['id']:<5} {registro['nombre']:<20} {registro['email']:<25} {registro['edad']:<5}")


def buscar_registro_interactivo(gestor: GestorRegistros) -> None:
    """Busca un registro por ID.

    Args:
        gestor: Instancia del gestor de registros.
    """
    try:
        id_buscar = int(input("\nIngrese ID a buscar: ").strip())
        registro = gestor.search_record(id_buscar)

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


def update_record_interactivo(gestor: GestorRegistros, data_file: str) -> None:
    """Actualiza un registro por ID.

    Args:
        gestor: Instancia del gestor de registros.
        data_file: Ruta al archivo de datos para persistencia.
    """
    try:
        id_actualizar = int(input("\nIngrese ID a actualizar: ").strip())
        nombre = input("Ingrese nuevo nombre (dejar vacío para no cambiar): ").strip()
        email = input("Ingrese nuevo email (dejar vacío para no cambiar): ").strip()
        edad = input("Ingrese nueva edad (dejar vacío para no cambiar): ").strip()

        nombre = nombre if nombre else None
        email = email if email else None
        edad = edad if edad else None

        exito, mensaje = gestor.update_record(id_actualizar, nombre, email, edad)

        if exito:
            print(Fore.GREEN + f" {mensaje}")
            save_data(data_file, gestor.list_records())
        else:
            print(Fore.RED + f" {mensaje}")

    except ValueError:
        print(Fore.RED + " El ID debe ser un número")
    except Exception as e:
        print(Fore.RED + f" Error: {e}")


def delete_record_interactivo(gestor: GestorRegistros, data_file: str) -> None:
    """Elimina un registro por ID.

    Args:
        gestor: Instancia del gestor de registros.
        data_file: Ruta al archivo de datos para persistencia.
    """
    try:
        id_eliminar = int(input("\nIngrese ID a eliminar: ").strip())
        exito, mensaje = gestor.delete_record(id_eliminar)

        if exito:
            print(Fore.GREEN + f" {mensaje}")
            save_data(data_file, gestor.list_records())
        else:
            print(Fore.RED + f" {mensaje}")

    except ValueError:
        print(Fore.RED + " El ID debe ser un número")
    except Exception as e:
        print(Fore.RED + f" Error: {e}")


def exportar_a_csv_interactivo(gestor: GestorRegistros, manager_reportes: ManagerReportes) -> None:
    """Exporta registros a CSV de forma interactiva.

    Args:
        gestor: Instancia del gestor de registros.
        manager_reportes: Instancia del gestor de reportes.
    """
    print("\n" + Fore.YELLOW + "--- EXPORTAR A CSV ---")

    try:
        nombre = input("Ingrese nombre de archivo (sin .csv, dejar vacío para nombre automático): ").strip()
        nombre = nombre if nombre else None

        registros = gestor.list_records()
        exito, mensaje, ruta = manager_reportes.exportar_a_csv(
            registros,
            nombre_archivo=nombre,
            incluir_timestamp=True,
            encoding='utf-8-sig'
        )

        if exito:
            print(Fore.GREEN + f" {mensaje}")
        else:
            print(Fore.RED + f" {mensaje}")

    except Exception as e:
        print(Fore.RED + f" Error: {e}")


def filtrar_registros_interactivo(gestor: GestorRegistros, manager_reportes: ManagerReportes) -> None:
    """Filtra y ordena registros de forma interactiva.

    Args:
        gestor: Instancia del gestor de registros.
        manager_reportes: Instancia del gestor de reportes.
    """
    print("\n" + Fore.YELLOW + "--- FILTRAR Y ORDENAR REGISTROS ---")

    try:
        registros = gestor.list_records()

        if not registros:
            print(Fore.YELLOW + "No hay registros para filtrar")
            return

        print(Fore.CYAN + "\nOpciones de filtrado (dejar vacío para omitir):")

        edad_min_input = input("Edad mínima: ").strip()
        edad_max_input = input("Edad máxima: ").strip()
        nombre_busca = input("Buscar en nombre: ").strip()
        email_busca = input("Buscar en email: ").strip()

        print(Fore.CYAN + "\nOpciones de ordenamiento:")
        print("  - id (default)")
        print("  - nombre")
        print("  - email")
        print("  - edad")
        ordenar_por = input("Ordenar por (default: id): ").strip() or "id"

        orden_input = input("Orden (A=ascendente, D=descendente, default: A): ").strip().upper()
        orden_asc = orden_input != 'D'

        filtros = {}
        if edad_min_input:
            filtros['edad_min'] = int(edad_min_input)
        if edad_max_input:
            filtros['edad_max'] = int(edad_max_input)
        if nombre_busca:
            filtros['nombre'] = nombre_busca
        if email_busca:
            filtros['email'] = email_busca

        filtros['ordenar_por'] = ordenar_por
        filtros['orden_asc'] = orden_asc

        exito, mensaje, registros_filtrados = manager_reportes.filtrar_registros(registros, **filtros)

        if exito:
            print(Fore.GREEN + f"\n {mensaje}")

            if registros_filtrados:
                print("-" * 70)
                print(f"{'ID':<5} {'Nombre':<20} {'Email':<25} {'Edad':<5}")
                print("-" * 70)

                for registro in registros_filtrados:
                    print(f"{registro['id']:<5} {registro['nombre']:<20} {registro['email']:<25} {registro['edad']:<5}")
            else:
                print(Fore.YELLOW + "No hay registros que cumplan los criterios")
        else:
            print(Fore.RED + f" {mensaje}")

    except ValueError:
        print(Fore.RED + " Error: Debe ingresar valores numéricos en campos numéricos")
    except Exception as e:
        print(Fore.RED + f" Error: {e}")
