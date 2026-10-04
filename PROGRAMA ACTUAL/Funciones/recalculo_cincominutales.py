import numpy as np

def recalculo_cincominutales_old(df, variable_acum, variable_cincomin):
    """
    Recalcula variables cincominutales a partir de acumuladas.

    df = recalculo_cincominutales(df, variable_acum, variable_cincomin)

    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.
    variable_acum : cadena
        Nombre de la columna de la variable acumulada.
    variable_cincomin : cadena
        Nombre de la columna de la variable cincominutal.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    """
    # no se aplica la corrección si la variable acumulada no tiene datos
    if df[variable_acum].sum() > 0:
        # se localizan las entradas sin dato
        mask = df[variable_acum].isna().values

        # se calculan los cincominutales
        corregidos    = df[variable_acum].ffill().diff() # ffill - forward fill
        corregidos.iloc[0] = df[variable_acum].iloc[0]

        # se localizan los valores negativos (cuando se reinicia el valor acumulado)
        # y se dejan estos nuevos valores como los cincominutales
        mask2             = (corregidos < 0).values
        corregidos[mask2] = df.loc[mask2, variable_acum]

        # donde no había dato, no se pone
        corregidos[mask]             = np.nan
        df.loc[:, variable_cincomin] = corregidos
    
    return df

import numpy as np
import pandas as pd

def recalculo_cincominutales(df, variable_acum, variable_cincomin):
    """
    Recalcula variables cincominutales a partir de acumuladas.

    Usa el DatetimeIndex para separar por años.
    Solo recalcula en los años donde la variable acumulada tiene datos (>0).
    """

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("El DataFrame debe tener un DatetimeIndex.")

    anios = df.index.year

    for anio in pd.Series(anios).unique():

        idx_anio = (anios == anio)
        df_anio = df.loc[idx_anio]

        # Si ese año no tiene acumulados reales → no tocar
        if df_anio[variable_acum].sum(skipna=True) <= 0:
            continue

        # Máscara NaN originales
        mask = df_anio[variable_acum].isna().values

        # Diferencias
        corregidos = df_anio[variable_acum].ffill().diff()
        corregidos.iloc[0] = df_anio[variable_acum].iloc[0]

        # Reinicios del acumulador
        mask2 = (corregidos < 0).values
        corregidos.iloc[mask2] = df_anio.loc[df_anio.index[mask2], variable_acum].values

        # Respetar NaN
        corregidos.iloc[mask] = np.nan

        # Guardar resultados
        df.loc[df_anio.index, variable_cincomin] = corregidos.values

    return df

