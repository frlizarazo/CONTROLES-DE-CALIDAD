import pandas as pd

from Funciones.recalculo_cincominutales import recalculo_cincominutales

def CCal6_recalculo_evt_cincominutal(df):
    """
    Recalcula los valores de evapotranspiración Cincominutal a partir de la
    precipitación acumulada.

    df, eliminados = recalculo_evt_cincominutal(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos. No incluye los valores de
        evapotranspiración acumulada.
    eliminados : Serie
        Serie vacía (se retorna por consistencia con las demás correcciones).
    """
    df = recalculo_cincominutales(df, 'Evapotranspiración Acumulada', 'Evapotranspiración')

    df.drop('Evapotranspiración Acumulada', axis=1, inplace=True)
    
    eliminados = pd.Series(dtype='float64')

    #print('Recalculo evt done')

    return df, eliminados

CCal6_recalculo_evt_cincominutal.variables = ['Evapotranspiración Acumulada']
CCal6_recalculo_evt_cincominutal.nombre    = 'Recálculo Evapotranspiración'