# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal8_sensores_constantes.py                                                            #
# DESCRIPCIÓN: Identifica y corrige sensores que reportan valores constantes                       #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal8_sensores_constantes(df)                                                                  #
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
def CCal8_sensores_constantes(df):

    Sensores_Constantes   = Instrumentar('Eliminar datos de sensores que reportan valores constantes',0)

    df_notna = df.dropna(how = 'all')
    idx      = df_notna[(df_notna == df_notna.shift()).all(axis=1)].index

    if len(idx) > 0:
        eliminados  = df.loc[idx].copy()
        df.loc[idx] = np.nan
    else:
        eliminados = pd.DataFrame(dtype='float64')

    Sensores_Constantes.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal8_sensores_constantes.variables   = [] # Variables requeridas para funcionar
CCal8_sensores_constantes.nombre      = 'CCal8 - Sensores Constantes'  # Nombre visible
CCal8_sensores_constantes.obligatorio = False
CCal8_sensores_constantes.visible     = True
CCal8_sensores_constantes.descripcion = 'Identifica y corrige sensores que reportan valores constantes'