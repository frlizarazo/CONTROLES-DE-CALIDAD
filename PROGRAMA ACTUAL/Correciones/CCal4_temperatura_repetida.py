import numpy  as np
import pandas as pd

def CCal4_temperatura_repetida(df):
    """
    Elimina valores de temperatura que se repiten más de 2 veces consecutivas.

    df, eliminados = temperatura_repetida(df)
    
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
    
    idx = df[(df['Temperatura'] == df['Temperatura'].shift(1)) &
             (df['Temperatura'] == df['Temperatura'].shift(2))].index
    
    if len(idx) > 0:
        eliminados = df.loc[idx, 'Temperatura'].copy()
        df.loc[idx, 'Temperatura'] = np.nan

    else:
        eliminados = pd.Series(dtype='float64')

    if 'Temperatura del Agua' in df.columns:
        idx_agua = df[(df['Temperatura del Agua'] == df['Temperatura del Agua'].shift(1)) &
                      (df['Temperatura del Agua'] == df['Temperatura del Agua'].shift(2))].index
        
        if len(idx_agua) > 0:
            eliminados_agua = df.loc[idx_agua, 'Temperatura del Agua'].copy()
            df.loc[idx_agua, 'Temperatura del Agua'] = np.nan
        else:
            eliminados_agua = pd.Series(dtype='float64')
        
        eliminados = pd.concat([eliminados, eliminados_agua], axis=0)

    #print('temperatura repetidas done')
    
    return df, eliminados

CCal4_temperatura_repetida.variables = ['Temperatura']
CCal4_temperatura_repetida.nombre = 'Temperatura repetida'