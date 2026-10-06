# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal9_datos_nivel_constantes.py                                                         #
# DESCRIPCIÓN: Identifica y corrige niveles que reportan valores constantes                        #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal9_datos_nivel_constantes(df)                                                               #
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
import numpy as np
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal9_datos_nivel_constantes(df):

    Datos_Nivel_Constantes   = Instrumentar('Eliminar datos de niveles que reportan valores constantes',0)

    grupo = (df['Nivel'] != df['Nivel'].shift()).cumsum()
    tamano_grupo = df.groupby(grupo)['Nivel'].transform('size')

    mascara_eliminados = tamano_grupo > 5
    eliminados = df.loc[mascara_eliminados, ['Nivel']].copy()

    df.loc[mascara_eliminados, 'Nivel'] = np.nan

    Datos_Nivel_Constantes.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal9_datos_nivel_constantes.variables   = ['Nivel'] # Variables requeridas para funcionar
CCal9_datos_nivel_constantes.nombre      = 'CCal9 - Datos Nivel Constantes'  # Nombre visible
CCal9_datos_nivel_constantes.obligatorio = False
CCal9_datos_nivel_constantes.visible     = True
CCal9_datos_nivel_constantes.descripcion = 'Identifica y corrige niveles que reportan valores constantes'
CCal9_datos_nivel_constantes.depende     = None