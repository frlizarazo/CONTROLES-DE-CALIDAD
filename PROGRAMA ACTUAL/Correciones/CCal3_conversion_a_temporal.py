# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal3_conversion_a_temporal.py                                                          #
# DESCRIPCIÓN: Convierte los datos a formato temporal                                              #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal3_conversion_a_temporal(df)                                                                #
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
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal3_conversion_a_temporal(df, formato_fecha):

    Extraccion_Observaciones   = Instrumentar('Extraer datos enviados a observaciones',0)
    # Para que el indice no tenga fila a parte con el nombre
    df.index.names = [None]
    
    # Se deja como indice una columna con fecha y hora con formato m/d/y h:m:s
    df.set_index(pd.to_datetime(df['Fecha'] + ' ' + df['Hora'],
                                format  = formato_fecha, 
                                cache   = False), 
                                inplace = True)
    eliminados = pd.DataFrame(dtype='float64')
    df.drop(df.columns[[0, 1]], axis = 1, inplace = True)   

    Extraccion_Observaciones.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal3_conversion_a_temporal.variables   = [] # Variables requeridas para funcionar
CCal3_conversion_a_temporal.nombre      = 'CCal3 - Conversión a Temporal'  # Nombre visible
CCal3_conversion_a_temporal.obligatorio = True
CCal3_conversion_a_temporal.visible     = True
CCal3_conversion_a_temporal.descripcion = 'Convierte la fecha y hora a un índice temporal'
