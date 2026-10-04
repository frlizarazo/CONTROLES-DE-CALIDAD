import numpy  as np
import pandas as pd

def CCal9_redondeo_p2(df):
    ## Revisar con el acumulado para que no se incremente
    """
    Modifica los datos de precipitación menores a 0.2 mm, que aparecen con la
    interpolación, aumentándolos a 0.2 mm.

    df, eliminados = redondeo_p2(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : Serie
        Serie vacía, por consistencia con las demás correcciones.
    """
    redondear_p2              = lambda x: 0.2 * np.round(x/0.2)
    df['Precipitación'] = df['Precipitación'].apply(redondear_p2)

    #print('Redondeo done')

    return df, pd.Series(dtype='float64')

CCal9_redondeo_p2.variables = ['Precipitación']
CCal9_redondeo_p2.nombre = 'Redondear precipitación a 0.2 mm'