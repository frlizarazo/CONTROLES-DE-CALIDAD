import numpy  as np
import pandas as pd


def CCal1_sensores_constantes(df):
    """
    Elimina filas de datos consecutivas que se repiten más de una vez.

    df, eliminados = filas_repetidas(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : DataFrame
        Contiene los datos eliminados.
    """
    
    df_notna = df.dropna(how = 'all')
    idx      = df_notna[(df_notna == df_notna.shift()).all(axis=1)].index

    if len(idx) > 0:
        eliminados  = df.loc[idx].copy()
        df.loc[idx] = np.nan

    else:
        eliminados = pd.DataFrame(dtype='float64')
    
    #print('Filas repetidas done')

    return df, eliminados

CCal1_sensores_constantes.variables = []
CCal1_sensores_constantes.nombre = 'Sensores constantes'