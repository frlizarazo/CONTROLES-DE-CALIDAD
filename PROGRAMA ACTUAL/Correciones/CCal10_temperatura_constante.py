# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal10_temperatura_repetida.py                                                           #
# DESCRIPCIÓN: Detecta y elimina las filas en las que la temperatura se repite                     #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal10_temperatura_repetida(df)                                                                 #
#                                                                                                  #
# PARAMETROS DE ENTRADA:                                                                           #
#   df: DataFrame con los datos de la serie temporal                                               #
#                                                                                                  #
# PARAMETROS DE SALIDA:                                                                            #
#   df         : DataFrame con los datos corregidos                                                #
#   eliminados : DataFrame vacío                                                                   #
#                                                                                                  #
# ================================================================================================ #

# LIBRERÍAS DE PYTHON ============================================================================ #
import pandas as pd
import numpy as np
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal10_temperatura_constante(df):

    Temperatura_Repetida   = Instrumentar('Detectar temperatura repetida',0)

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

    Temperatura_Repetida.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal10_temperatura_constante.variables   = ['Temperatura'] # Variables requeridas para funcionar
CCal10_temperatura_constante.nombre      = 'CCal10 - Temperatura constante'  # Nombre visible
CCal10_temperatura_constante.obligatorio = False
CCal10_temperatura_constante.visible     = True
CCal10_temperatura_constante.descripcion = 'Detecta y elimina las filas en las que la temperatura se repite'