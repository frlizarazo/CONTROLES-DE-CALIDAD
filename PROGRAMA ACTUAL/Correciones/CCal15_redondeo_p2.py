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
import numpy as np
import pandas as pd

def CCal15_redondeo_p2(df, resolucion = 0.2):

    Redondeo_P2 = Instrumentar('Redondea los valores de precipitación menores a la resolución', 0)

    # Máscara para identificar valores estrictamente menores que la resolución
    mask = df['Precipitación'] < resolucion

    # Arrastrar a la resolución mínima o a cero según el punto medio (resolucion / 2)
    df.loc[mask, 'Precipitación'] = np.where(
        df.loc[mask, 'Precipitación'] >= (resolucion / 2), 
        resolucion, 
        0.0
    )

    eliminados = pd.Series(dtype='float64')

    Redondeo_P2.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal15_redondeo_p2.variables   = ['Precipitación'] # Variables requeridas para funcionar
CCal15_redondeo_p2.nombre      = 'CCal15 - Redondeo de Precipitación'  # Nombre visible
CCal15_redondeo_p2.obligatorio = False
CCal15_redondeo_p2.visible     = True
CCal15_redondeo_p2.descripcion = 'Redondea los valores inferiores a la resolución de medición del pluviometro'
CCal15_redondeo_p2.depende     = ['CCal14 - Homogenización de Intervalos']
