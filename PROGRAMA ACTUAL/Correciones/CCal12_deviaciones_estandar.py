import os 
import numpy             as np
import pandas            as pd
import matplotlib.pyplot as plt

from matplotlib import use

use('Agg')

def CCal12_desviaciones_estandar(df):
    """
    Genera un histograma para cada hora, y elimina los datos que se alejan 
    4 desviaciones estándar de la media en cada hora

    df, eliminados = percentil_horario(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : DataFrame
        Contiene los datos eliminados por el filtro. Cuando en una hora solo se
        eliminan datos de algunas variables, en las demás se pone `nan`.
    """
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

            #Tukey
            #IQR
            #Q25-3*IQR
            #Q75+3*IQR

            #PETTITT (despues-hacer pruebas)
            #Diario

            #T-studen
            #Diario

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

    #print('percentil done')


    return df, eliminados

CCal12_desviaciones_estandar.variables = ['Temperatura']
CCal12_desviaciones_estandar.nombre = 'Percentiles horarios'