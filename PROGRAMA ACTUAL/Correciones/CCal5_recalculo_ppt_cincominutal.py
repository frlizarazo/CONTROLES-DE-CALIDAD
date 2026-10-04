import pandas as pd

from Funciones.recalculo_cincominutales import recalculo_cincominutales

def CCal5_recalculo_ppt_cincominutal(df):
    """
    Recalcula los valores de precipitación Cincominutal a partir de la
    precipitación acumulada.

    df, eliminados = recalculo_ppt_cincominutal(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos. No incluye los valores de
        precipitación acumulada.
    eliminados : Serie
        Serie vacía (se retorna por consistencia con las demás correcciones).
    """
    df = recalculo_cincominutales(df, 'Precipitación Acumulada', 'Precipitación')

    df.drop('Precipitación Acumulada', axis = 1, inplace=True)

    eliminados = pd.Series(dtype='float64') # ?? No se estan retornando los valores eliminados

    #print('Recalculo ppt done')

    return df, eliminados

CCal5_recalculo_ppt_cincominutal.variables = ['Precipitación Acumulada']
CCal5_recalculo_ppt_cincominutal.nombre    = 'Recálculo Precipitación'
