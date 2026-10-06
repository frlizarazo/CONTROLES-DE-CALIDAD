# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal17_limites_fisicos.py                                                               #
# DESCRIPCIÓN: Aplica corrección de veleta estática a los datos de precipitación                   #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal17_limites_fisicos(df)                                                                     #
#                                                                                                  #
# PARAMETROS DE ENTRADA:                                                                           #
#   df: DataFrame con los datos de la serie temporal                                               #
#                                                                                                  #
# PARAMETROS DE SALIDA:                                                                            #
#   df         : DataFrame con los datos corregidos                                                #
#   eliminados : DataFrame vacío                                                                   #
#                                                                                                  #
# ================================================================================================ #

# LIBRERÍAS DE PYTHON ============================================================================ #
import pandas as pd
import numpy as np
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal17_limites_fisicos(df):

    Limites_Fisicos = Instrumentar('Aplica corrección de limites fisicos',0)

    limites = {'Temperatura':                     (-np.inf,      100), # permitir valores negativos solo para las altitudes de las P.N.N.N
               'Temperatura del Agua':            (-np.inf,      100),
               'Velocidad del Viento':            (      0,       50), #antes 28.4 - evaluar aumento
               'Dirección del Viento':            (      0,      360),
               'Presión Barométrica':             (   0.01,     1500), # proponer un filtro de rango variable (con histogramas o percentiles)
               'Humedad Relativa':                (   0.01,      100), # proponer un filtro de rango variable (con histogramas o percentiles)
               'Radiación Solar':                 (      0,     1367),
               'Precipitación':                   (      0,      155),
               'Evapotranspiración':              (      0,      160), # Eliminar esto de todo
               'Nivel':                           (      0,   np.inf), # revisar
               'Nivel (1)':                       (      0,   np.inf)} # revisar

    # se crea el filtro de los datos que se salen de los rangos establecidos 
    filtro_limites = pd.DataFrame(False, columns = df.columns, index = df.index)
    eliminados     = pd.DataFrame(columns = df.columns, index = df.index)
    
    for var in limites.keys():
        if var in df.columns:
            filtro_limites[var] = ((df[var] < limites[var][0]) | 
                                   (df[var] > limites[var][1]))

    # se elimina la fila completa si más de 3 columnas tienen datos fuera de los
    # límites
    filas_completas = df[filtro_limites.sum(axis=1) >= 3].index

    if len(filas_completas) > 0:
        eliminados.loc[filas_completas] = df.loc[filas_completas].copy()

    df.loc[filas_completas]             = np.nan
    filtro_limites.loc[filas_completas] = False

    for var in filtro_limites.columns:
        CorVar = df[filtro_limites[var]].index

        if len(CorVar) > 0:
            eliminados.loc[CorVar, [var]] = df.loc[CorVar, [var]].copy()
            df.loc[CorVar, var]           = np.nan

    eliminados = eliminados[eliminados.any(axis=1)]

    eliminados.replace(False, np.nan, inplace=True)
    eliminados.dropna(axis=1, how='all', inplace=True)


    Limites_Fisicos.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal17_limites_fisicos.variables   = [] # Variables requeridas para funcionar
CCal17_limites_fisicos.nombre      = 'CCal17 - Límites Físicos'  # Nombre visible
CCal17_limites_fisicos.obligatorio = False
CCal17_limites_fisicos.visible     = True
CCal17_limites_fisicos.descripcion = 'Aplica corrección de límites físicos'
CCal17_limites_fisicos.depende     = ['CCal14 - Homogenización de Intervalos']