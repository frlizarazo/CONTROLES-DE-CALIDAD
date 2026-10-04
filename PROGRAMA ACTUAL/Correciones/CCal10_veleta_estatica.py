import numpy  as np
import pandas as pd

def CCal10_veleta_estatica(df):
    """
    Elimina los datos de dirrección del viento si la velocidad del viento
    es cero.

    df, eliminados = veleta_estatica(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : Serie
        Contiene los datos eliminados.
    """
    idx = df[df['Velocidad del Viento'] == 0].index

    if len(idx) > 0:
        eliminados = df.loc[idx, 'Dirección del Viento'].copy()

        df.loc[idx, 'Dirección del Viento'] = np.nan
        df.loc[idx, 'Dirección de la Rosa']   = ''

    else:
        eliminados = pd.Series(dtype='float64')     

    #print('Veleta ppt done')

    return df, eliminados

CCal10_veleta_estatica.variables = ['Velocidad del Viento', 'Dirección del Viento']
CCal10_veleta_estatica.nombre    = 'Veleta estática'