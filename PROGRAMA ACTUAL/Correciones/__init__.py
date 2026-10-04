from .CCal0_controles_de_lectura        import CCal0_controles_de_lectura
from .CCal1_extracción_de_observaciones import CCal1_extracción_de_observaciones
from .CCal1_sensores_constantes         import CCal1_sensores_constantes
from .CCal2_Datos_de_nivel_constantes   import CCal2_Datos_de_nivel_constantes
from .CCal2_filas_nulas                 import CCal2_filas_nulas
from .CCal3_fallo_sensor                import CCal3_fallo_sensor
from .CCal4_temperatura_repetida        import CCal4_temperatura_repetida
from .CCal5_recalculo_ppt_cincominutal  import CCal5_recalculo_ppt_cincominutal
from .CCal6_recalculo_evt_cincominutal  import CCal6_recalculo_evt_cincominutal
from .CCal7_limites_fisicos             import CCal7_limites_fisicos
from .CCal8_homogenizacion_intervalos   import CCal8_homogenizacion_intervalos
from .CCal9_redondeo_p2                 import CCal9_redondeo_p2
from .CCal10_veleta_estatica            import CCal10_veleta_estatica
from .CCal11_histograma_valores         import CCal11_histograma_valores
from .CCal12_deviaciones_estandar       import CCal12_desviaciones_estandar
from .CCal16_z_score                    import CCal16_ZScoreRobusto

# filtros habilitados en el programa
FILTROS = (
    CCal0_controles_de_lectura,
    CCal1_extracción_de_observaciones,
    CCal1_sensores_constantes,
    CCal2_Datos_de_nivel_constantes,
    CCal2_filas_nulas,
    CCal3_fallo_sensor,
    CCal4_temperatura_repetida,
    CCal5_recalculo_ppt_cincominutal,
    CCal6_recalculo_evt_cincominutal,
    CCal7_limites_fisicos,
    CCal8_homogenizacion_intervalos,
    CCal9_redondeo_p2,
    CCal10_veleta_estatica,
    CCal11_histograma_valores,
    CCal12_desviaciones_estandar,
    CCal16_ZScoreRobusto,
)

__all__ = [FILTROS]

# Quitar los ND que faltan