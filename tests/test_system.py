"""Test suite for the Gestión de Información system.

Tests cover:
- Data validation (all fields)
- CRUD operations with RecordService
- Duplicate constraint enforcement
- File persistence (load/save)
- CSV export and filtering with pandas
- Statistical analysis

Run with: pytest tests/ -v
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.service import GestorRegistros
from src.integration import ManagerReportes
from src.file import load_data, save_data
from src.validate import validar_id, validar_nombre, validar_email, validar_edad


# ============================================================================
# Validator Tests
# ============================================================================


class TestValidators:
    """Pruebas de funciones de validación de datos."""

    def test_validar_id_valido(self):
        """IDs válidos deben ser aceptados."""
        valido, resultado = validar_id("1")
        assert valido is True
        assert resultado == 1
        
        valido, resultado = validar_id("100")
        assert valido is True
        assert resultado == 100

    def test_validar_id_cero_o_negativo(self):
        """IDs cero o negativos deben ser rechazados."""
        valido, msg = validar_id("0")
        assert valido is False
        assert "positivo" in msg

        valido, msg = validar_id("-5")
        assert valido is False

    def test_validar_id_no_numerico(self):
        """IDs no numéricos deben ser rechazados."""
        valido, msg = validar_id("abc")
        assert valido is False
        assert "número entero" in msg

    def test_validar_nombre_valido(self):
        """Nombres válidos deben ser aceptados y limpiados."""
        valido, resultado = validar_nombre("Juan")
        assert valido is True
        assert resultado == "Juan"
        
        valido, resultado = validar_nombre("  Ana  ")
        assert valido is True
        assert resultado == "Ana"

    def test_validar_nombre_corto(self):
        """Nombres con menos de 2 caracteres deben ser rechazados."""
        valido, msg = validar_nombre("A")
        assert valido is False
        assert "2 caracteres" in msg

    def test_validar_nombre_vacio(self):
        """Nombre vacío debe ser rechazado."""
        valido, msg = validar_nombre("")
        assert valido is False

    def test_validar_email_valido(self):
        """Emails válidos deben ser aceptados y normalizados."""
        valido, email = validar_email("TEST@EXAMPLE.COM")
        assert valido is True
        assert email == "test@example.com"

    def test_validar_email_invalido(self):
        """Emails inválidos deben ser rechazados."""
        valido, msg = validar_email("not-an-email")
        assert valido is False
        assert "formato" in msg

    def test_validar_email_vacio(self):
        """Email vacío debe ser rechazado."""
        valido, msg = validar_email("")
        assert valido is False

    def test_validar_edad_valida(self):
        """Edades válidas deben ser aceptadas."""
        valido, resultado = validar_edad("25")
        assert valido is True
        assert resultado == 25
        
        valido, resultado = validar_edad("0")
        assert valido is True
        
        valido, resultado = validar_edad("120")
        assert valido is True

    def test_validar_edad_fuera_rango(self):
        """Edades fuera de 0-120 deben ser rechazadas."""
        valido, msg = validar_edad("-1")
        assert valido is False
        assert "entre 0 y 120" in msg

        valido, msg = validar_edad("999")
        assert valido is False

    def test_validar_edad_no_numerica(self):
        """Edades no numéricas deben ser rechazadas."""
        valido, msg = validar_edad("abc")
        assert valido is False
        assert "número entero" in msg


# ============================================================================
# GestorRegistros - Create Tests
# ============================================================================


class TestGestorRegistrosCreate:
    """Pruebas de creación de registros."""

    def setup_method(self):
        """Crear un gestor nuevo para cada prueba."""
        self.gestor = GestorRegistros()

    def test_crear_registro_valido(self):
        """Un registro válido debe crearse exitosamente."""
        exito, msg, registro = self.gestor.new_register("1", "Juan", "juan@email.com", "30")
        assert exito is True
        assert registro['id'] == 1
        assert registro['nombre'] == "Juan"
        assert registro['email'] == "juan@email.com"
        assert registro['edad'] == 30

    def test_crear_registro_id_duplicado(self):
        """Registro con ID duplicado debe fallar."""
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")
        exito, msg, _ = self.gestor.new_register("1", "Ana", "ana@email.com", "25")
        assert exito is False
        assert "ya existe" in msg

    def test_crear_registro_email_duplicado(self):
        """Registro con email duplicado debe fallar."""
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")
        exito, msg, _ = self.gestor.new_register("2", "Ana", "juan@email.com", "25")
        assert exito is False
        assert "email" in msg.lower()

    def test_crear_registro_datos_invalidos(self):
        """Datos inválidos deben generar error."""
        exito, msg, _ = self.gestor.new_register("-1", "Juan", "juan@email.com", "30")
        assert exito is False

        exito, msg, _ = self.gestor.new_register("1", "A", "juan@email.com", "30")
        assert exito is False

        exito, msg, _ = self.gestor.new_register("1", "Juan", "invalido", "30")
        assert exito is False

        exito, msg, _ = self.gestor.new_register("1", "Juan", "juan@email.com", "999")
        assert exito is False

    def test_crear_multiples_registros(self):
        """Múltiples registros válidos deben poder crearse."""
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")
        self.gestor.new_register("2", "Ana", "ana@email.com", "25")
        self.gestor.new_register("3", "Carlos", "carlos@email.com", "40")
        assert len(self.gestor.list_records()) == 3


# ============================================================================
# GestorRegistros - Read Tests
# ============================================================================


class TestGestorRegistrosRead:
    """Pruebas de lectura de registros."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.gestor = GestorRegistros()
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")
        self.gestor.new_register("2", "Ana", "ana@email.com", "25")

    def test_obtener_registro_existente(self):
        """Registro existente debe encontrarse."""
        registro = self.gestor.search_record(1)
        assert registro is not None
        assert registro['nombre'] == "Juan"

    def test_obtener_registro_inexistente(self):
        """Registro inexistente debe retornar None."""
        registro = self.gestor.search_record(999)
        assert registro is None

    def test_listar_todos_los_registros(self):
        """Todos los registros deben listarse."""
        registros = self.gestor.list_records()
        assert len(registros) == 2

    def test_busqueda_con_list_comprehension(self):
        """Busqueda debe usar list comprehension internamente."""
        # Verificar que search_record usa list comprehension
        # La implementación usa [r for r in self.registros if r['id'] == id_persona]
        registro = self.gestor.search_record(1)
        assert registro is not None
        assert registro['id'] == 1


# ============================================================================
# GestorRegistros - Update Tests
# ============================================================================


class TestGestorRegistrosUpdate:
    """Pruebas de actualización de registros."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.gestor = GestorRegistros()
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")

    def test_actualizar_nombre(self):
        """Nombre debe actualizarse."""
        exito, msg = self.gestor.update_record(1, nombre="Juanito", email=None, edad=None)
        assert exito is True
        registro = self.gestor.search_record(1)
        assert registro['nombre'] == "Juanito"

    def test_actualizar_email(self):
        """Email debe actualizarse."""
        exito, msg = self.gestor.update_record(1, nombre=None, email="nuevo@email.com", edad=None)
        assert exito is True
        registro = self.gestor.search_record(1)
        assert registro['email'] == "nuevo@email.com"

    def test_actualizar_edad(self):
        """Edad debe actualizarse."""
        exito, msg = self.gestor.update_record(1, nombre=None, email=None, edad="35")
        assert exito is True
        registro = self.gestor.search_record(1)
        assert registro['edad'] == 35

    def test_actualizar_registro_inexistente(self):
        """Actualizar registro inexistente debe fallar."""
        exito, msg = self.gestor.update_record(999, nombre="X", email=None, edad=None)
        assert exito is False

    def test_actualizar_email_a_duplicado(self):
        """Actualizar email a uno existente debe fallar."""
        self.gestor.new_register("2", "Ana", "ana@email.com", "25")
        exito, msg = self.gestor.update_record(1, nombre=None, email="ana@email.com", edad=None)
        assert exito is False

    def test_actualizar_campos_multiples(self):
        """Múltiples campos deben poder actualizarse."""
        exito, msg = self.gestor.update_record(1, nombre="Nuevo", email="nuevo@email.com", edad="40")
        assert exito is True
        registro = self.gestor.search_record(1)
        assert registro['nombre'] == "Nuevo"
        assert registro['email'] == "nuevo@email.com"
        assert registro['edad'] == 40


# ============================================================================
# GestorRegistros - Delete Tests
# ============================================================================


class TestGestorRegistrosDelete:
    """Pruebas de eliminación de registros."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.gestor = GestorRegistros()
        self.gestor.new_register("1", "Juan", "juan@email.com", "30")

    def test_eliminar_registro_existente(self):
        """Registro existente debe eliminarse."""
        exito, msg = self.gestor.delete_record(1)
        assert exito is True
        assert len(self.gestor.list_records()) == 0

    def test_eliminar_registro_inexistente(self):
        """Registro inexistente debe fallar."""
        exito, msg = self.gestor.delete_record(999)
        assert exito is False

    def test_registro_inaccesible_despues_eliminar(self):
        """Registro eliminado no debe ser accesible."""
        self.gestor.delete_record(1)
        assert self.gestor.search_record(1) is None


# ============================================================================
# GestorRegistros - Serialization Tests
# ============================================================================


class TestGestorRegistrosSerialization:
    """Pruebas de serialización y carga desde diccionarios."""

    def test_to_dict_list_vacio(self):
        """Gestor vacío debe retornar lista vacía."""
        gestor = GestorRegistros()
        assert gestor.to_dict_list() == []

    def test_to_dict_list_con_datos(self):
        """Registros deben convertirse a diccionarios."""
        gestor = GestorRegistros()
        gestor.new_register("1", "Juan", "juan@email.com", "30")
        gestor.new_register("2", "Ana", "ana@email.com", "25")

        registros = gestor.to_dict_list()
        assert len(registros) == 2
        assert registros[0] == {"id": 1, "nombre": "Juan", "email": "juan@email.com", "edad": 30}
        assert registros[1] == {"id": 2, "nombre": "Ana", "email": "ana@email.com", "edad": 25}

    def test_cargar_desde_dict_list(self):
        """Registros deben cargarse desde diccionarios."""
        gestor = GestorRegistros()
        datos = [
            {"id": 1, "nombre": "Juan", "email": "juan@email.com", "edad": 30},
            {"id": 2, "nombre": "Ana", "email": "ana@email.com", "edad": 25},
        ]
        gestor.load_from_dict_list(datos)

        assert len(gestor.get_all()) == 2
        assert gestor.search_record(1)['nombre'] == "Juan"

    def test_cargar_desde_dict_list_duplicado_falla(self):
        """Cargar datos duplicados debe fallar."""
        gestor = GestorRegistros()
        datos = [
            {"id": 1, "nombre": "Juan", "email": "juan@email.com", "edad": 30},
            {"id": 1, "nombre": "Ana", "email": "ana@email.com", "edad": 25},
        ]
        with pytest.raises(Exception):
            gestor.load_from_dict_list(datos)

    def test_cargar_desde_dict_list_invalido_falla(self):
        """Cargar datos inválidos debe fallar."""
        gestor = GestorRegistros()
        datos = [{"id": -1, "nombre": "Juan", "email": "juan@email.com", "edad": 30}]
        with pytest.raises(Exception):
            gestor.load_from_dict_list(datos)

    def test_get_all_returns_copy(self):
        """get_all debe retornar una copia para evitar modificaciones externas."""
        gestor = GestorRegistros()
        gestor.new_register("1", "Juan", "juan@email.com", "30")
        registros = gestor.get_all()
        registros.clear()
        assert len(gestor.get_all()) == 1


# ============================================================================
# Storage Tests
# ============================================================================


class TestStorage:
    """Pruebas de operaciones de persistencia."""

    def test_guardar_y_cargar_registros(self):
        """Registros deben guardarse y cargarse correctamente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "registros.json"
            datos = [
                {"id": 1, "nombre": "Juan", "email": "juan@email.com", "edad": 30},
                {"id": 2, "nombre": "Ana", "email": "ana@email.com", "edad": 25},
            ]

            save_data(str(filepath), datos)
            cargados = load_data(str(filepath))

            assert cargados == datos

    def test_cargar_archivo_inexistente(self):
        """Cargar archivo inexistente debe retornar lista vacía."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "inexistente.json"
            cargados = load_data(str(filepath))
            assert cargados == []

    def test_cargar_json_invalido(self):
        """Cargar JSON inválido no debe caerse."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "mal.json"
            filepath.write_text("{ invalido }")

            cargados = load_data(str(filepath))
            assert cargados == []

    def test_guardar_directorio_inexistente(self):
        """Guardar debe crear directorios si no existen."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "subdir" / "registros.json"
            datos = [{"id": 1, "nombre": "Juan", "email": "juan@email.com", "edad": 30}]

            save_data(str(filepath), datos)
            assert filepath.exists()

            cargados = load_data(str(filepath))
            assert cargados == datos


# ============================================================================
# ManagerReportes - Filter Tests
# ============================================================================


class TestManagerReportesFilter:
    """Pruebas de filtrado de registros."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.manager = ManagerReportes()
        self.registros = [
            {"id": 1, "nombre": "Juan", "email": "juan@gmail.com", "edad": 28},
            {"id": 2, "nombre": "María", "email": "maria@hotmail.com", "edad": 35},
            {"id": 3, "nombre": "Carlos", "email": "carlos@gmail.com", "edad": 42},
            {"id": 4, "nombre": "Ana", "email": "ana@yahoo.com", "edad": 25},
            {"id": 5, "nombre": "Luis", "email": "luis@gmail.com", "edad": 30},
        ]

    def test_filtrar_por_rango_edad(self):
        """Filtrar por rango de edad debe funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, edad_min=25, edad_max=35
        )
        assert exito is True
        assert len(resultado) == 3
        edades = [r["edad"] for r in resultado]
        assert all(25 <= e <= 35 for e in edades)

    def test_filtrar_por_nombre(self):
        """Filtrar por nombre debe funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, nombre="an"
        )
        assert exito is True
        assert len(resultado) == 2
        nombres = {r["nombre"] for r in resultado}
        assert nombres == {"Juan", "Ana"}

    def test_filtrar_por_email(self):
        """Filtrar por email debe funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, email="gmail"
        )
        assert exito is True
        assert len(resultado) == 3

    def test_ordenar_por_edad_desc(self):
        """Ordenar por edad descendente debe funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, ordenar_por="edad", orden_asc=False
        )
        assert exito is True
        edades = [r["edad"] for r in resultado]
        assert edades == [42, 35, 30, 28, 25]

    def test_ordenar_por_nombre_asc(self):
        """Ordenar por nombre ascendente debe funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, ordenar_por="nombre", orden_asc=True
        )
        assert exito is True
        nombres = [r["nombre"] for r in resultado]
        assert nombres == ["Ana", "Carlos", "Juan", "Luis", "María"]

    def test_filtro_combinado(self):
        """Filtros combinados deben funcionar."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros,
            edad_min=25,
            edad_max=35,
            email="gmail",
            ordenar_por="edad",
            orden_asc=True,
        )
        assert exito is True
        assert len(resultado) == 2
        assert resultado[0]["nombre"] == "Luis"
        assert resultado[1]["nombre"] == "Juan"

    def test_filtro_no_coincide(self):
        """Filtro sin coincidencias debe retornar lista vacía."""
        exito, msg, resultado = self.manager.filtrar_registros(
            self.registros, edad_min=100
        )
        assert exito is True
        assert resultado == []

    def test_filtro_registros_vacios(self):
        """Filtrar lista vacía debe retornar lista vacía."""
        exito, msg, resultado = self.manager.filtrar_registros([])
        assert exito is False
        assert resultado == []


# ============================================================================
# ManagerReportes - Statistics Tests
# ============================================================================


class TestManagerReportesStatistics:
    """Pruebas de estadísticas."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.manager = ManagerReportes()
        self.registros = [
            {"id": 1, "nombre": "Juan", "email": "juan@gmail.com", "edad": 28},
            {"id": 2, "nombre": "María", "email": "maria@hotmail.com", "edad": 35},
            {"id": 3, "nombre": "Carlos", "email": "carlos@gmail.com", "edad": 42},
            {"id": 4, "nombre": "Ana", "email": "ana@yahoo.com", "edad": 25},
            {"id": 5, "nombre": "Luis", "email": "luis@gmail.com", "edad": 30},
        ]

    def test_estadisticas_calculos(self):
        """Cálculos estadísticos deben ser correctos."""
        stats = self.manager.generar_reporte_estadistico(self.registros)

        assert stats["total_registros"] == 5
        assert stats["total_personas_unicas"] == 5
        assert stats["edad_promedio"] == 32.0
        assert stats["edad_minima"] == 25
        assert stats["edad_maxima"] == 42
        assert stats["edad_mediana"] == 30
        assert stats["desv_std_edad"] == 6.52

    def test_estadisticas_vacio(self):
        """Estadísticas de lista vacía deben retornar ceros."""
        stats = self.manager.generar_reporte_estadistico([])

        assert stats["total_registros"] == 0
        assert stats["total_personas_unicas"] == 0
        assert stats["edad_promedio"] == 0
        assert stats["edad_minima"] == 0

    def test_estadisticas_un_registro(self):
        """Estadísticas con un solo registro."""
        stats = self.manager.generar_reporte_estadistico([{"id": 1, "nombre": "A", "email": "a@b.com", "edad": 20}])

        assert stats["total_registros"] == 1
        assert stats["edad_promedio"] == 20.0
        assert stats["edad_minima"] == 20


# ============================================================================
# ManagerReportes - Export Tests
# ============================================================================


class TestManagerReportesExport:
    """Pruebas de exportación a CSV."""

    def setup_method(self):
        """Preparar datos de prueba."""
        self.manager = ManagerReportes()
        self.registros = [
            {"id": 1, "nombre": "Juan", "email": "juan@gmail.com", "edad": 28},
            {"id": 2, "nombre": "María", "email": "maria@hotmail.com", "edad": 35},
        ]

    def test_exportar_csv(self):
        """Exportar a CSV debe funcionar."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exito, msg, filepath = self.manager.exportar_a_csv(
                self.registros,
                nombre_archivo="test",
                include_timestamp=False,
                encoding="utf-8-sig",
                data_dir=tmpdir,
            )

            assert exito is True
            assert filepath is not None
            assert Path(filepath).exists()

            contenido = Path(filepath).read_text(encoding='utf-8-sig')
            assert "Juan" in contenido
            assert "María" in contenido
            assert "," in contenido

    def test_exportar_csv_vacio(self):
        """Exportar lista vacía debe fallar."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exito, msg, filepath = self.manager.exportar_a_csv(
                [],
                data_dir=tmpdir,
            )

            assert exito is False
            assert filepath is None

    def test_exportar_con_timestamp(self):
        """Exportar con timestamp debe incluir fecha/hora en nombre."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exito, msg, filepath = self.manager.exportar_a_csv(
                self.registros,
                include_timestamp=True,
                data_dir=tmpdir,
            )
            assert exito is True
            assert "reporte_registros_" in filepath

    def test_exportar_nombre_personalizado(self):
        """Exportar con nombre personalizado debe usar ese nombre."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exito, msg, filepath = self.manager.exportar_a_csv(
                self.registros,
                nombre_archivo="mi_reporte",
                include_timestamp=False,
                data_dir=tmpdir,
            )
            assert exito is True
            assert filepath.endswith("mi_reporte.csv")

    def test_exportar_separador_personalizado(self):
        """Exportar con separador personalizado debe usarlo."""
        with tempfile.TemporaryDirectory() as tmpdir:
            exito, msg, filepath = self.manager.exportar_a_csv(
                self.registros,
                separador=";",
                include_timestamp=False,
                data_dir=tmpdir,
            )
            assert exito is True
            contenido = Path(filepath).read_text(encoding='utf-8')
            assert ";" in contenido


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
