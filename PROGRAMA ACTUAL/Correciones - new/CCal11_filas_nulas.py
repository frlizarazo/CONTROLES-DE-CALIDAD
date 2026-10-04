# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal11_filas_nulas.py                                                                   #
# DESCRIPCIÓN: Elimina las filas en las que todas las variables son nulas                          #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal11_filas_nulas(df)                                                                         #
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
def CCal11_filas_nulas(df):

    Filas_Nulas   = Instrumentar('Eliminar filas en las que todas las variables son nulas')

    idx = df[(df.select_dtypes('number') == 0).all(1)].index

    if len(idx) > 0:
        columnas_numericas = df.select_dtypes('number').columns
        eliminados         = df.loc[idx, columnas_numericas].copy()

        df.loc[idx, columnas_numericas] = np.nan
    else:
        eliminados = pd.DataFrame(dtype = 'float64')

    Filas_Nulas.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal11_filas_nulas.variables   = [] # Variables requeridas para funcionar
CCal11_filas_nulas.nombre      = 'Filas Nulas'  # Nombre visible
CCal11_filas_nulas.obligatorio = False
CCal11_filas_nulas.visible     = True