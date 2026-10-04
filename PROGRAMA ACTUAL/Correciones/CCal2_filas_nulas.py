import numpy  as np
import pandas as pd


def CCal2_filas_nulas(df):

    """
    Elimina filas donde todos los datos numéricos son iguales a cero.

    df, eliminados = filas_nulas(df)

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
    
    idx = df[(df.select_dtypes('number') == 0).all(1)].index

    if len(idx) > 0:
        columnas_numericas = df.select_dtypes('number').columns
        eliminados         = df.loc[idx, columnas_numericas].copy()

        df.loc[idx, columnas_numericas] = np.nan
    else:
        eliminados = pd.DataFrame(dtype = 'float64')

    #print('Filas nulas done')
    
    return df, eliminados

CCal2_filas_nulas.nombre    = 'Filas nulas'
CCal2_filas_nulas.variables = []