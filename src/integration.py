"""Módulo de integración con pandas para exportación y filtrado de registros.

Proporciona funcionalidades avanzadas de reportes, exportación a CSV y filtrado de datos.
"""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd  # type: ignore


class ManagerReportes:
    """Gestor de reportes y exportación de datos con pandas."""

    def __init__(self, data_dir: Optional[str] = None) -> None:
        """Inicializa el gestor de reportes.

        Args:
            data_dir: Directorio donde se almacenarán los reportes.
                      Si no se especifica, usa la carpeta 'data' del proyecto.

        Raises:
            ValueError: Si la carpeta de datos no existe.
        """
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

        if not os.path.exists(data_dir):
            raise ValueError(f"La carpeta de datos no existe: {data_dir}")

        self.data_dir = data_dir

    def exportar_a_csv(self, registros: List[Dict[str, Any]], *args: Any, nombre_archivo: Optional[str] = None, **kwargs: Any) -> Tuple[bool, str, Optional[str]]:
        """Exporta registros a archivo CSV con opciones configurables.

        Args:
            registros: Lista de registros (diccionarios).
            *args: Argumentos posicionales adicionales (para extensibilidad).
            nombre_archivo: Nombre personalizado del archivo.
            **kwargs: Argumentos adicionales:
                - incluir_timestamp (bool): Incluir timestamp (default: True).
                - separador (str): Separador CSV (default: ',').
                - encoding (str): Codificación (default: 'utf-8').

        Returns:
            Tupla (éxito, mensaje, ruta_archivo).
        """
        if not registros:
            return False, "Error: No hay registros para exportar", None

        try:
            incluir_timestamp = kwargs.get('incluir_timestamp', True)
            separador = kwargs.get('separador', ',')
            encoding = kwargs.get('encoding', 'utf-8')

            df = pd.DataFrame(registros)

            if nombre_archivo is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") if incluir_timestamp else ""
                nombre_archivo = f"reporte_registros_{timestamp}.csv" if timestamp else "reporte_registros.csv"
            elif not nombre_archivo.endswith('.csv'):
                nombre_archivo += '.csv'

            ruta_completa = os.path.join(self.data_dir, nombre_archivo)
            df.to_csv(ruta_completa, sep=separador, encoding=encoding, index=False)

            mensaje = f"Reporte exportado exitosamente: {ruta_completa}"
            return True, mensaje, ruta_completa

        except Exception as e:
            return False, f"Error al exportar CSV: {str(e)}", None

    def filtrar_registros(self, registros: List[Dict[str, Any]], *args: Any, **kwargs: Any) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """Filtra y ordena registros usando pandas DataFrame.

        Args:
            registros: Lista de registros.
            *args: Argumentos posicionales (para extensibilidad).
            **kwargs: Criterios de filtro:
                - edad_min (int): Edad mínima.
                - edad_max (int): Edad máxima.
                - nombre (str): Búsqueda en nombre (substring).
                - email (str): Búsqueda en email (substring).
                - ordenar_por (str): Campo para ordenar (default: 'id').
                - orden_asc (bool): Ascendente (default: True).

        Returns:
            Tupla (éxito, mensaje, registros_filtrados).
        """
        if not registros:
            return False, "No hay registros para filtrar", []

        try:
            df = pd.DataFrame(registros)
            df_filtrado = df.copy()

            if 'edad_min' in kwargs:
                edad_min = kwargs['edad_min']
                df_filtrado = df_filtrado[df_filtrado['edad'] >= edad_min]

            if 'edad_max' in kwargs:
                edad_max = kwargs['edad_max']
                df_filtrado = df_filtrado[df_filtrado['edad'] <= edad_max]

            if 'nombre' in kwargs:
                nombre_busqueda = kwargs['nombre'].lower()
                df_filtrado = df_filtrado[df_filtrado['nombre'].str.lower().str.contains(nombre_busqueda)]

            if 'email' in kwargs:
                email_busqueda = kwargs['email'].lower()
                df_filtrado = df_filtrado[df_filtrado['email'].str.lower().str.contains(email_busqueda)]

            ordenar_por = kwargs.get('ordenar_por', 'id')
            orden_asc = kwargs.get('orden_asc', True)

            if ordenar_por in df_filtrado.columns:
                df_filtrado = df_filtrado.sort_values(by=ordenar_por, ascending=orden_asc)

            registros_resultado = df_filtrado.to_dict(orient='records')
            mensaje = f"Filtrado exitoso: {len(registros_resultado)} registros encontrados"
            return True, mensaje, registros_resultado

        except Exception as e:
            return False, f"Error al filtrar: {str(e)}", []

    def generar_reporte_estadistico(self, registros: List[Dict[str, Any]], *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Genera un reporte estadístico de los registros.

        Args:
            registros: Lista de registros.
            *args: Argumentos posicionales (para extensibilidad).
            **kwargs: Opciones adicionales.

        Returns:
            Diccionario con estadísticas del dataset.
        """
        if not registros:
            return {
                'total_registros': 0,
                'total_personas_unicas': 0,
                'edad_promedio': 0,
                'edad_minima': 0,
                'edad_maxima': 0,
                'edad_mediana': 0,
                'desv_std_edad': 0,
            }

        try:
            df = pd.DataFrame(registros)

            estadisticas = {
                'total_registros': len(df),
                'total_personas_unicas': len(df['id'].unique()),
                'edad_promedio': round(df['edad'].mean(), 2),
                'edad_minima': int(df['edad'].min()),
                'edad_maxima': int(df['edad'].max()),
                'edad_mediana': int(df['edad'].median()),
                'desv_std_edad': round(df['edad'].std(), 2),
            }

            return estadisticas

        except Exception as e:
            return {'error': str(e)}
