# Servicio de gestión de registros en memoria

from typing import Any, Dict, List, Optional, Tuple

from validate import validar_id, validar_nombre, validar_email, validar_edad


class GestorRegistros:
    """Gestiona registros de personas en memoria con validaciones.

    Mantiene listas de registros y sets para garantizar unicidad de IDs
    y direcciones de email únicas.
    """

    def __init__(self) -> None:
        self.registros: List[Dict[str, Any]] = []
        self.ids_unicos: set[int] = set()
        self.emails_unicos: set[str] = set()

    def new_register(self, id_persona: str, nombre: str, email: str, edad: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Crea un nuevo registro con validación completa.

        Valida todos los campos y verifica restricciones de unicidad
        antes de crear el registro.

        Args:
            id_persona: ID como string.
            nombre: Nombre de la persona.
            email: Email de la persona.
            edad: Edad como string.

        Returns:
            Tupla (éxito, mensaje, registro).
        """
        try:
            # Validar ID
            valido, resultado = validar_id(id_persona)
            if not valido:
                return False, f"Error en ID: {resultado}", None
            id_persona_int = resultado  # type: ignore

            if id_persona_int in self.ids_unicos:
                return False, f"Error: El ID {id_persona_int} ya existe", None

            # Validar nombre
            valido, resultado = validar_nombre(nombre)
            if not valido:
                return False, f"Error en nombre: {resultado}", None
            nombre = resultado  # type: ignore

            # Validar email
            valido, resultado = validar_email(email)
            if not valido:
                return False, f"Error en email: {resultado}", None
            email = resultado  # type: ignore

            if email in self.emails_unicos:
                return False, f"Error: El email '{email}' ya está registrado", None

            # Validar edad
            valido, resultado = validar_edad(edad)
            if not valido:
                return False, f"Error en edad: {resultado}", None
            edad_int = resultado  # type: ignore

            # Crear registro
            registro: Dict[str, Any] = {
                'id': id_persona_int,
                'nombre': nombre,
                'email': email,
                'edad': edad_int
            }

            self.registros.append(registro)
            self.ids_unicos.add(id_persona_int)
            self.emails_unicos.add(email)

            return True, "Registro creado exitosamente", registro

        except Exception as e:
            return False, f"Error inesperado: {e}", None

    def list_records(self) -> List[Dict[str, Any]]:
        """Retorna la lista completa de registros.

        Returns:
            Lista de diccionarios con todos los registros.
        """
        return list(self.registros)

    def search_record(self, id_persona: int) -> Optional[Dict[str, Any]]:
        """Busca un registro por ID.

        Args:
            id_persona: ID a buscar.

        Returns:
            Diccionario del registro o None si no se encuentra.
        """
        resultado = [r for r in self.registros if r['id'] == id_persona]
        resultado.sort(key=lambda x: x['id'])
        return resultado[0] if resultado else None

    def update_record(self, id_persona: int, nombre: Optional[str] = None, email: Optional[str] = None, edad: Optional[str] = None) -> Tuple[bool, str]:
        """Actualiza un registro existente por ID.

        Solo actualiza los campos proporcionados (no None).

        Args:
            id_persona: ID del registro a actualizar.
            nombre: Nuevo nombre (opcional).
            email: Nuevo email (opcional).
            edad: Nueva edad (opcional).

        Returns:
            Tupla (éxito, mensaje).
        """
        registro = self.search_record(id_persona)
        if registro is None:
            return False, f"No se encontró registro con ID {id_persona}"

        try:
            # Actualizar nombre
            if nombre is not None:
                valido, resultado = validar_nombre(nombre)
                if not valido:
                    return False, f"Error en nombre: {resultado}"
                registro['nombre'] = resultado  # type: ignore

            # Actualizar email
            if email is not None:
                valido, resultado = validar_email(email)
                if not valido:
                    return False, f"Error en email: {resultado}"
                nuevo_email = resultado  # type: ignore

                if nuevo_email != registro['email'] and nuevo_email in self.emails_unicos:
                    return False, f"Error: El email '{nuevo_email}' ya está registrado"

                self.emails_unicos.discard(registro['email'])
                registro['email'] = nuevo_email
                self.emails_unicos.add(nuevo_email)

            # Actualizar edad
            if edad is not None:
                valido, resultado = validar_edad(edad)
                if not valido:
                    return False, f"Error en edad: {resultado}"
                registro['edad'] = resultado  # type: ignore

            return True, "Registro actualizado exitosamente"

        except Exception as e:
            return False, f"Error inesperado: {e}"

    def delete_record(self, id_persona: int) -> Tuple[bool, str]:
        """Elimina un registro por ID.

        Args:
            id_persona: ID del registro a eliminar.

        Returns:
            Tupla (éxito, mensaje).
        """
        for i, registro in enumerate(self.registros):
            if registro['id'] == id_persona:
                self.ids_unicos.discard(registro['id'])
                self.emails_unicos.discard(registro['email'])
                del self.registros[i]
                return True, "Registro eliminado exitosamente"

        return False, f"No se encontró registro con ID {id_persona}"

    def limpiar_registros(self) -> None:
        """Limpia todos los registros y reinicia los índices."""
        self.registros = []
        self.ids_unicos = set()
        self.emails_unicos = set()