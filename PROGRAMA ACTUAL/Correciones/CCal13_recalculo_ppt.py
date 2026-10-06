# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal13_recalculo_ppt.py                                                                 #
# DESCRIPCIÓN: Recalcula los valores de precipitación cada 5 minutos                               #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal13_recalculo_ppt(df)                                                                       #
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
def CCal13_recalculo_ppt(df):

    Recalculo_PPT   = Instrumentar('Recalcula los valores de precipitación cada 5 minutos',0)
    
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("El DataFrame debe tener un DatetimeIndex.")

    años = df.index.year

    for año in pd.Series(años).unique():

        idx_año = (años == año)
        df_año = df.loc[idx_año]

        # Si ese año no tiene acumulados reales → no tocar
        if df_año['Precipitación Acumulada'].sum(skipna=True) <= 0:
            continue

        # Máscara NaN originales
        mask = df_año['Precipitación Acumulada'].isna().values

        # Diferencias
        corregidos = df_año['Precipitación Acumulada'].ffill().diff()
        corregidos.iloc[0] = df_año['Precipitación Acumulada'].iloc[0]

        # Reinicios del acumulador
        mask2 = (corregidos < 0).values
        corregidos.iloc[mask2] = df_año.loc[df_año.index[mask2], 'Precipitación Acumulada'].values

        # Respetar NaN
        corregidos.iloc[mask] = np.nan

        # Guardar resultados
        df.loc[df_año.index, 'Precipitación'] = corregidos.values

    df.drop('Precipitación Acumulada', axis = 1, inplace=True)
    eliminados = pd.Series(dtype='float64')
        
    Recalculo_PPT.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal13_recalculo_ppt.variables   = ['Precipitación Acumulada'] # Variables requeridas para funcionar
CCal13_recalculo_ppt.nombre      = 'CCal13 - Recalculo de PPT'  # Nombre visible
CCal13_recalculo_ppt.obligatorio = False
CCal13_recalculo_ppt.visible     = True
CCal13_recalculo_ppt.descripcion = 'Recalcula los valores de precipitación incremental a partir de los acumulados'