# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal7_extraccion_de_observaciones.py                                                    #
# DESCRIPCIÓN: Extrae datos que se fueron enviados a observaciones                                 #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal7_extraccion_de_observaciones(df)                                                          #
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
def CCal7_extraccion_de_observaciones(df):

    Extraccion_Observaciones   = Instrumentar('Extraer datos enviados a observaciones')

    # Aseguramos que Observaciones sea string
    df['Observaciones'] = df['Observaciones'].astype(str)

    # Extraemos el valor numérico después de 'level:'
    df['Nivel_extraido'] = df['Observaciones'].str.extract(r'level:(\d+\.?\d*)')

    # Convertimos a float
    df['Nivel_extraido'] = df['Nivel_extraido'].astype(float)

    # Forzamos la columna 'Nivel' a float64 para evitar errores de asignación
    df['Nivel'] = df['Nivel'].astype('float64')

    # Asignamos los valores extraídos redondeados
    df.loc[df['Observaciones'].str.contains('level', na=False), 'Nivel'] = df['Nivel_extraido'].round(2)

    # Eliminamos la columna auxiliar
    df.drop(columns=['Nivel_extraido'], inplace=True, errors='ignore')

    eliminados = pd.DataFrame(dtype='float64')
    Extraccion_Observaciones.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal7_extraccion_de_observaciones.variables   = ['Nivel', 'Observaciones'] # Variables requeridas para funcionar
CCal7_extraccion_de_observaciones.nombre      = 'Extracción de Observaciones'  # Nombre visible
CCal7_extraccion_de_observaciones.obligatorio = False
CCal7_extraccion_de_observaciones.visible     = True