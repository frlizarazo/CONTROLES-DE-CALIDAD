from .CCal1_tipos_de_datos import CCal1_tipos_de_datos
from .CCal2_entradas_repetidas import CCal2_entradas_repetidas
from .CCal3_conversion_a_temporal import CCal3_conversion_a_temporal
from .CCal4_coherencia_fecha import CCal4_coherencia_fecha
from .CCal5_orden_de_datos import CCal5_orden_de_datos
from .CCal6_duplicidad_entradas import CCal6_duplicidad_entradas
from .CCal7_extraccion_de_observaciones import CCal7_extraccion_de_observaciones
from .CCal8_sensores_constantes import CCal8_sensores_constantes
from .CCal9_datos_nivel_constantes import CCal9_datos_nivel_constantes
from .CCal10_temperatura_constante import CCal10_temperatura_constante
from .CCal11_filas_nulas import CCal11_filas_nulas
from .CCal12_fallo_sensor import CCal12_fallo_sensor
from .CCal13_recalculo_ppt import CCal13_recalculo_ppt
from .CCal14_homogenizacion_intervalos import CCal14_homogenizacion_intervalos
from .CCal15_redondeo_p2 import CCal15_redondeo_p2
from .CCal16_veleta_estatica import CCal16_veleta_estatica
from .CCal17_limites_fisicos import CCal17_limites_fisicos
from .CCal18_histograma_valores import CCal18_histograma_valores
from .CCal19_desviaciones_estandar import CCal19_desviaciones_estandar
from .CCal20_z_score import CCal20_z_score

# filtros habilitados en el programa
FILTROS = (
    CCal1_tipos_de_datos,
    CCal2_entradas_repetidas,
    CCal3_conversion_a_temporal,
    CCal4_coherencia_fecha,
    CCal5_orden_de_datos,
    CCal6_duplicidad_entradas,
    CCal7_extraccion_de_observaciones,
    CCal8_sensores_constantes,
    CCal9_datos_nivel_constantes,
    CCal10_temperatura_constante,
    CCal11_filas_nulas,
    CCal12_fallo_sensor,
    CCal13_recalculo_ppt,
    CCal14_homogenizacion_intervalos,
    CCal15_redondeo_p2,
    CCal16_veleta_estatica,
    CCal17_limites_fisicos,
    CCal18_histograma_valores,
    CCal19_desviaciones_estandar,
    CCal20_z_score
)

__all__ = [FILTROS]