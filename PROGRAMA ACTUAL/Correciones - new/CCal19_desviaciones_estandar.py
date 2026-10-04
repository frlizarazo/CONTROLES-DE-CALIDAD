# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal19_desviaciones_estandar.py                                                               #
# DESCRIPCIÓN: Aplica corrección de desviaciones estándar a los datos de precipitación                   #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal19_desviaciones_estandar(df)                                                                     #
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
import os 
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from matplotlib import use

from Funciones.instrumentar import Instrumentar
use('Agg')

# CONTROL DE CALIDAD ============================================================================= #
def CCal19_desviaciones_estandar(df):

    Desviaciones_Estandar = Instrumentar('Aplica corrección de Desviaciones Estándar')
    n = 4           # número de desviaciones estándar a considerar

    eliminados = []
    columnas_consideradas = [c for c in df.columns if c in ['Temperatura', 'Presión Barométrica']] 

    for var in columnas_consideradas:
        df_temp = df[var].dropna()

        if len(df_temp) == 0:
            continue

        idx      = pd.to_datetime([])
        _, axs = plt.subplots(ncols=4, nrows=6, figsize=(20, 16))
        axs      = axs.flatten()

        for h in range(24):
            df_temp_h = df_temp.between_time(f"{h}:00", f"{h}:59")
            if len(df_temp_h) == 0:
                continue
            n_bins    = int(round( 1 + 3.322*np.log10( len(df_temp_h) )))
            ax        = df_temp_h.hist(bins=n_bins, ax=axs[h])
            media     = df_temp_h.median()                            # MEDIANA
            desv      = df_temp_h.std()
            media_mas = media + n*desv
            media_men = media - n*desv

            ax.axvline(media_mas, c='r')
            ax.axvline(media_men, c='r')

            ax.text(
                media_mas,
                0.99,
                f'{media_mas:.2f}',
                color     = 'k', 
                ha        = 'right', 
                va        = 'top', 
                rotation  = 90, 
                transform = ax.get_xaxis_transform()
            )

            ax.text(
                media_men, 
                0.99, 
                f'{media_men:.2f}', 
                color     = 'k', 
                ha        = 'left', 
                va        = 'top', 
                rotation  = 90, 
                transform = ax.get_xaxis_transform()
            )

            ax.get_yaxis ().set_visible(False)
            ax.set_yscale('log')
            ax.set_title (f'{var} de {h}:00 a {h}:59')

            idx_h = df_temp_h[(df_temp_h < media_men) | (df_temp_h > media_mas)].index
            idx   = idx.union(idx_h)

        plt.tight_layout()
        plt.close()

        if len(idx) > 0:
            eliminados.append(df.loc[idx, var].copy())

        df.loc[idx, var] = np.nan  # Se vuelven NaN

    if len(eliminados) > 0:
        eliminados = pd.concat(eliminados, axis=1, sort=True)

    Desviaciones_Estandar.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal19_desviaciones_estandar.variables   = ['Temperatura'] # Variables requeridas para funcionar
CCal19_desviaciones_estandar.nombre      = 'Desviaciones Estándar'  # Nombre visible
CCal19_desviaciones_estandar.obligatorio = False
CCal19_desviaciones_estandar.visible     = True