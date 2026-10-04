# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal12_fallo_sensor.py                                                                   #
# DESCRIPCIÓN: Detecta y elimina las filas en las que el sensor de humedad falla                   #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal12_fallo_sensor(df)                                                                         #
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
def CCal12_fallo_sensor(df):

    Fallo_Sensor   = Instrumentar('Detectar fallo en el sensor de humedad')

    # Caso 1 -----------------------------------------------------------------
    # Temperatura: NaN
    # Velocidad del viento: NaN 
    # Dirección del viento: NaN
    # Humedad: not NaN

    idx_1 = df[np.isnan(df['Temperatura']) & np.isnan(df['Velocidad del Viento']) &
               np.isnan(df['Dirección del Viento']) & ~np.isnan(df['Humedad Relativa'])]
    
    # Caso 2 -----------------------------------------------------------------
    # Temperatura: NaN
    # Radiación Solar: NaN 
    # Humedad: not NaN

    idx_2 = df[np.isnan(df['Temperatura']) & np.isnan(df['Radiación Solar']) &
                ~np.isnan(df['Humedad Relativa'])]
    
    # Caso 3 -----------------------------------------------------------------
    # Velocidad del viento: NaN 
    # Dirección del viento: NaN
    # Radiación Solar: NaN 
    # Humedad: not NaN

    idx_3 = df[np.isnan(df['Velocidad del Viento']) & np.isnan(df['Dirección del Viento']) & 
               np.isnan(df['Radiación Solar']) & ~np.isnan(df['Humedad Relativa'])]
    
    idx = pd.concat([idx_1, idx_2, idx_3]).index

    # Se elimina la humedad para cualquiera de los casos mencionados
    if len(idx) > 0:
        eliminados               = df.loc[idx, ['Humedad Relativa']].copy()
        df.loc[idx, ['Humedad Relativa']] = np.nan

    else:
        eliminados = pd.Series(dtype='float64')
        
    Fallo_Sensor.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal12_fallo_sensor.variables   = ['Temperatura',
                                'Velocidad del Viento',
                                'Dirección del Viento',
                                'Radiación Solar', 
                                'Humedad Relativa'] # Variables requeridas para funcionar
CCal12_fallo_sensor.nombre      = 'Fallo en el Sensor'  # Nombre visible
CCal12_fallo_sensor.obligatorio = False
CCal12_fallo_sensor.visible     = True