# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal15_redondeo_p2.py                                                                 #
# DESCRIPCIÓN: Redondea los valores de precipitación                                                #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal15_redondeo_p2(df)                                                                         #
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
import datetime as dt
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal15_redondeo_p2(df):

    Redondeo_P2   = Instrumentar('Redondea los valores de precipitación')

    redondear_p2        = lambda x: 0.2 * np.round(x/0.2)
    df['Precipitación'] = df['Precipitación'].apply(redondear_p2)
    eliminados          = pd.Series(dtype='float64')

    Redondeo_P2.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal15_redondeo_p2.variables   = ['Precipitación'] # Variables requeridas para funcionar
CCal15_redondeo_p2.nombre      = 'Redondeo de Precipitación'  # Nombre visible
CCal15_redondeo_p2.obligatorio = False
CCal15_redondeo_p2.visible     = True