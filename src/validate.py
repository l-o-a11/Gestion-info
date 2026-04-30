# Funciones de validación de campos

from typing import Tuple


def validar_id(id_valor: str) -> Tuple[bool, str | int]:
    """Valida que el ID sea un número entero positivo.

    Args:
        id_valor: Valor del ID a validar.

    Returns:
        Tupla (éxito, resultado) donde resultado es el ID entero
        si es válido o mensaje de error si no lo es.
    """
    try:
        id_int = int(id_valor)
        if id_int <= 0:
            return False, "El ID debe ser un número positivo"
        return True, id_int
    except ValueError:
        return False, "El ID debe ser un número entero"


def validar_nombre(nombre: str) -> Tuple[bool, str]:
    """Valida que el nombre no esté vacío y tenga al menos 2 caracteres.

    Args:
        nombre: Nombre a validar.

    Returns:
        Tupla (éxito, resultado) donde resultado es el nombre validado
        o mensaje de error si no es válido.
    """
    if not nombre or not isinstance(nombre, str):
        return False, "El nombre no puede estar vacío"
    if len(nombre.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    return True, nombre.strip()


def validar_email(email: str) -> Tuple[bool, str]:
    """Valida que el email tenga formato correcto.

    Args:
        email: Email a validar.

    Returns:
        Tupla (éxito, resultado) donde resultado es el email validado
        o mensaje de error si no es válido.
    """
    if not email or not isinstance(email, str):
        return False, "El email no puede estar vacío"
    email_clean = email.strip().lower()
    if '@' not in email_clean or '.' not in email_clean.split('@')[-1]:
        return False, "El email debe contener un formato válido"
    if len(email_clean) < 5:
        return False, "El email es demasiado corto"
    return True, email_clean


def validar_edad(edad: str) -> Tuple[bool, str | int]:
    """Valida que la edad sea un número entre 0 y 120.

    Args:
        edad: Edad a validar.

    Returns:
        Tupla (éxito, resultado) donde resultado es la edad entera
        si es válida o mensaje de error si no es válida.
    """
    try:
        edad_int = int(edad)
        if edad_int < 0 or edad_int > 120:
            return False, "La edad debe estar entre 0 y 120 años"
        return True, edad_int
    except ValueError:
        return False, "La edad debe ser un número entero"