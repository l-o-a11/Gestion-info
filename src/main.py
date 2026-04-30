from colorama import Fore, Style, init
import os
import sys
from pathlib import Path

from menu import (
    mostrar_menu,
    new_register_interactivo,
    list_records_interactivo,
    buscar_registro_interactivo,
    update_record_interactivo,
    delete_record_interactivo,
    exportar_a_csv_interactivo,
    filtrar_registros_interactivo,
)
from service import GestorRegistros
from integration import ManagerReportes
from file import load_data, save_data

init(autoreset=True)

# Ruta del archivo JSON
DATA_FILE: str = str(Path(__file__).parent / '..' / 'data' / 'records.json')


def main() -> None:
    """Función principal del programa."""
    print(Fore.MAGENTA + Style.BRIGHT + "\n¡Bienvenido al Sistema de Gestión de Información!\n")

    gestor = GestorRegistros()
    manager_reportes = ManagerReportes()

    # Cargar datos desde archivo JSON
    print(Fore.CYAN + " Cargando datos desde el archivo...")
    registros_cargados = load_data(DATA_FILE)

    if registros_cargados:
        print(Fore.GREEN + f" Se cargaron {len(registros_cargados)} registros desde el archivo.\n")
        # Restaurar registros en el gestor
        for registro in registros_cargados:
            try:
                gestor.new_register(
                    str(registro['id']),
                    registro['nombre'],
                    registro['email'],
                    str(registro['edad'])
                )
            except Exception:
                pass
    else:
        print(Fore.YELLOW + "  No hay registros previos. Se inicia con lista vacía.\n")

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-8): ").strip()

        if opcion == "1":
            new_register_interactivo(gestor, DATA_FILE)

        elif opcion == "2":
            list_records_interactivo(gestor)

        elif opcion == "3":
            buscar_registro_interactivo(gestor)

        elif opcion == "4":
            update_record_interactivo(gestor, DATA_FILE)

        elif opcion == "5":
            delete_record_interactivo(gestor, DATA_FILE)

        elif opcion == "6":
            exportar_a_csv_interactivo(gestor, manager_reportes)

        elif opcion == "7":
            filtrar_registros_interactivo(gestor, manager_reportes)

        elif opcion == "8":
            print(Fore.MAGENTA + Style.BRIGHT + "\n¡Hasta luego!\n")
            sys.exit(0)

        else:
            print(Fore.RED + " Opción no válida. Por favor, seleccione entre 1 y 8")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
