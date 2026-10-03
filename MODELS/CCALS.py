from abc import ABC, abstractmethod
import pandas as pd
from typing import Tuple, List, Any, Dict

class ControlCalidad(ABC):
    """
    Clase abstracta base para procesos de control de calidad sobre DataFrames.
    """
    def __init__(self, df: pd.DataFrame, **kwargs: Any):
        self.df_original: pd.DataFrame = df.copy()
        self.kwargs: Dict[str, Any] = kwargs
        
        # Resultados estándar del proceso
        self.df_procesado: pd.DataFrame = pd.DataFrame()
        self.eliminados: pd.DataFrame = pd.DataFrame()
        self.observaciones: List[str] = []

    @abstractmethod
    def procesar(self) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """
        Ejecuta las reglas de validación y limpieza.
        Debe actualizar y retornar: (df_procesado, eliminados, observaciones).
        """
        pass

    @abstractmethod
    def graficar(self) -> None:
        """
        Genera gráficos descriptivos o de diagnóstico del control de calidad.
        """
        pass

    @abstractmethod
    def escribir_archivos(self, ruta_destino: str) -> None:
        """
        Exporta los resultados (datos limpios, eliminados y bitácora) a archivos.
        """
        pass