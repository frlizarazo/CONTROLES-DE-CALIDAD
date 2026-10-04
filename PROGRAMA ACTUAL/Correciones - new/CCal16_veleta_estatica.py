# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal16_veleta_estatica.py                                                               #
# DESCRIPCIÓN: Aplica corrección de veleta estática a los datos de precipitación                   #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal16_veleta_estatica(df)                                                                     #
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
def CCal16_veleta_estatica(df):

    Veleta_Estatica = Instrumentar('Aplica corrección de veleta estática')
    idx = df[df['Velocidad del Viento'] == 0].index

    if len(idx) > 0:
        eliminados = df.loc[idx, 'Dirección del Viento'].copy()

        df.loc[idx, 'Dirección del Viento'] = np.nan
        df.loc[idx, 'Dirección de la Rosa']   = ''

    else:
        eliminados = pd.Series(dtype='float64')  

    Veleta_Estatica.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal16_veleta_estatica.variables   = ['Velocidad del Viento', 'Dirección del Viento'] # Variables requeridas para funcionar
CCal16_veleta_estatica.nombre      = 'Veleta Estática'  # Nombre visible
CCal16_veleta_estatica.obligatorio = False
CCal16_veleta_estatica.visible     = True