import pandas as pd
import numpy as np

def CCal2_Datos_de_nivel_constantes(df):
    """
    Elimina valores de nivel de agua que son constantes durante más de 5 observaciones consecutivas.
    
    Parámetros:
    - df: DataFrame con una columna 'Nivel (cms)' que contiene los datos de nivel de agua.
    
    Retorna:
    - df: DataFrame modificado con los valores constantes reemplazados por NaN.
    """

    grupo = (df['Nivel'] != df['Nivel'].shift()).cumsum()
    tamano_grupo = df.groupby(grupo)['Nivel'].transform('size')

    mascara_eliminados = tamano_grupo > 5
    eliminados = df.loc[mascara_eliminados, ['Nivel']].copy()


    df.loc[mascara_eliminados, 'Nivel'] = np.nan

    return df, eliminados

CCal2_Datos_de_nivel_constantes.variables = ['Nivel']
CCal2_Datos_de_nivel_constantes.nombre    = 'Datos de nivel constantes'