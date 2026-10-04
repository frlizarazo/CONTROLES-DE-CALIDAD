# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal5_orden_de_datos.py                                                                 #
# DESCRIPCIÓN: Ordena los datos en el DataFrame                                                      #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#   Este control se aplica siempre y no sale dentro del apartado de filtros                        #
#                                                                                                  #
# USO:                                                                                             #
#   CCal5_orden_de_datos(df)                                                                      #
#                                                                                                  #
# PARAMETROS DE ENTRADA:                                                                           #
#   df: DataFrame con los datos de la serie temporal                                               #
#                                                                                                  #
# PARAMETROS DE SALIDA:                                                                            #
#   df         : DataFrame con los datos corregidos                                                #
#   eliminados : DataFrame con las filas duplicadas eliminadas                                     #
#                                                                                                  #
# ================================================================================================ #

# LIBRERÍAS DE PYTHON ============================================================================ #
import pandas as pd
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal5_orden_de_datos(df):

    Ordenar_Datos = Instrumentar('Ordenar datos', 1)
    df            = df.sort_index()
    eliminados    = pd.DataFrame(dtype='float64')
    Ordenar_Datos.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal5_orden_de_datos.variables   = [] # Variables requeridas para funcionar
CCal5_orden_de_datos.nombre      = 'Orden de Datos'  # Nombre visible
CCal5_orden_de_datos.obligatorio = True
CCal5_orden_de_datos.visible     = True