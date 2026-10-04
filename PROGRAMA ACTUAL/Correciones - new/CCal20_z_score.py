# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal20_z_score.py                                                                       #
# DESCRIPCIÓN: Aplica corrección de z-score a los datos de precipitación                           #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal20_z_score(df)                                                                             #
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
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from matplotlib import use

from Funciones.instrumentar import Instrumentar
use('Agg')

# CONTROL DE CALIDAD ============================================================================= #
def CCal20_z_score(df):

    ZScore = Instrumentar('Aplica corrección de Z-Score')
    eliminados = []
    columnas_consideradas = [c for c in df.columns if c in ['Nivel','Temperatura']]
    umbral = 6  # similar a ±4 desviaciones estándar

    for var in columnas_consideradas:
        df_temp = df[var].dropna()
        if len(df_temp) == 0:
            continue

        idx = pd.to_datetime([])

        for h in range(24):
            df_temp_h = df_temp.between_time(f"{h}:00", f"{h}:59").dropna()
            if len(df_temp_h) < 10:
                continue

            mediana = df_temp_h.median()
            mad     = np.median(np.abs(df_temp_h - mediana))

            if mad == 0:  # evitar división por cero
                continue

            z_score_robusto = 0.6745 * (df_temp_h - mediana) / mad
            idx_h = df_temp_h[np.abs(z_score_robusto) > umbral].index
            idx   = idx.union(idx_h)

        if len(idx) > 0:
            eliminados.append(df.loc[idx, var].copy())

        df.loc[idx, var] = np.nan

    if len(eliminados) > 0:
        eliminados = pd.concat(eliminados, axis=1, sort=True)

    ZScore.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal20_z_score.variables   = ['Nivel'] # Variables requeridas para funcionar
CCal20_z_score.nombre      = 'Z-Score'  # Nombre visible
CCal20_z_score.obligatorio = False
CCal20_z_score.visible     = True