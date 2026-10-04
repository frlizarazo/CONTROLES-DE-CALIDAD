# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal2_entradas_repetidas.py                                                             #
# DESCRIPCIÓN: Elimina las entradas repetidas en el DataFrame                                      #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal2_entradas_repetidas(df)                                                                   #
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
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal2_entradas_repetidas(df):

    Filas_Duplicadas = Instrumentar('Eliminar filas completas duplicadas', 1)
    duplicated_mask  = df.duplicated()
    eliminados       = df.iloc[duplicated_mask.values]
    df               = df.drop_duplicates().set_index('index')
    Filas_Duplicadas.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal2_entradas_repetidas.variables   = [] # Variables requeridas para funcionar
CCal2_entradas_repetidas.nombre      = 'Entradas Repetidas'  # Nombre visible
CCal2_entradas_repetidas.obligatorio = True
CCal2_entradas_repetidas.visible     = True