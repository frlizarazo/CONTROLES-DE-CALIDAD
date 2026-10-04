# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal1_tipos_de_datos.py                                                                 #
# DESCRIPCIÓN:Convierte los datos a los tipos de datos adecuados (numéricos)                       #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal1_tipos_de_datos(df)                                                                       #
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
def CCal1_tipos_de_datos(df):

    Convertir_Numerico = Instrumentar('Convertir a numérico', 1)
    cols_excluir       = ['Fecha', 'Hora', 'Dirección de la Rosa', 'Observaciones']
    cols_convertir     = [col for col in df.columns if col not in cols_excluir]
    df[cols_convertir] = df[cols_convertir].apply(pd.to_numeric, errors='coerce', downcast='float')
    eliminados         = pd.DataFrame(dtype='float64')
    Convertir_Numerico.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal1_tipos_de_datos.variables   = [] # Variables requeridas para funcionar
CCal1_tipos_de_datos.nombre      = 'Tipos de Datos'  # Nombre visible
CCal1_tipos_de_datos.obligatorio = True
CCal1_tipos_de_datos.visible     = True