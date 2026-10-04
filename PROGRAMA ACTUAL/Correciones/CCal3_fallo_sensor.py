import numpy  as np
import pandas as pd

# que se pueda con cualquiera de los casos

def CCal3_fallo_sensor(df):
    """
    Elimina datos de humedad cuando no se tienen datos de otras variables.

    df, eliminados = fallo_sensor(df)
    
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

    # Caso 1 -----------------------------------------------------------------

    # Temperatura: NaN
    # Velocidad del viento: NaN 
    # Dirección del viento: NaN
    # Humedad: not NaN

    idx_1 = df[np.isnan(df['Temperatura']) & np.isnan(df['Velocidad del Viento']) &
               np.isnan(df['Dirección del Viento']) & ~np.isnan(df['Humedad Relativa'])]
    
    # Caso 2 -----------------------------------------------------------------

    # Temperatura: NaN
    # Radiación Solar: NaN 
    # Humedad: not NaN

    idx_2 = df[np.isnan(df['Temperatura']) & np.isnan(df['Radiación Solar']) &
                ~np.isnan(df['Humedad Relativa'])]
    
    # Caso 3 -----------------------------------------------------------------
    # REVISAR ESTA
    # Velocidad del viento: NaN 
    # Dirección del viento: NaN
    # Radiación Solar: NaN 
    # Humedad: not NaN

    idx_3 = df[np.isnan(df['Velocidad del Viento']) & np.isnan(df['Dirección del Viento']) & 
               np.isnan(df['Radiación Solar']) & ~np.isnan(df['Humedad Relativa'])]
    
    idx = pd.concat([idx_1, idx_2, idx_3]).index

    # Se elimina la humedad para cualquiera de los casos mencionados
    if len(idx) > 0:
        eliminados               = df.loc[idx, ['Humedad Relativa']].copy()
        df.loc[idx, ['Humedad Relativa']] = np.nan

    else:
        eliminados = pd.Series(dtype='float64')

    #print('Fallo sensor done')

    return df, eliminados

CCal3_fallo_sensor.variables = ['Temperatura',
                                'Velocidad del Viento',
                                'Dirección del Viento', 
                                'Humedad Relativa']

CCal3_fallo_sensor.nombre = 'Fallo sensor'