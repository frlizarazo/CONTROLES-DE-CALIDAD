# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal5_duplicidad_entradas.py                                                            #
# DESCRIPCIÓN: Elimina las entradas duplicadas en el DataFrame                                     #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal5_duplicidad_entradas(df)                                                                  #
#                                                                                                  #
# PARAMETROS DE ENTRADA:                                                                           #
#   df: DataFrame con los datos de la serie temporal                                               #
#                                                                                                  #
# PARAMETROS DE SALIDA:                                                                            #
#   df         : DataFrame con los datos corregidos                                                #
#   eliminados : DataFrame con las entradas duplicadas eliminadas                                  #
#                                                                                                  #
# ================================================================================================ #

# LIBRERÍAS DE PYTHON ============================================================================ #
import numpy as np
import pandas as pd
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal6_duplicidad_entradas(df):

    Entradas_Duplicadas   = Instrumentar('Seleccionar datos de entradas duplicadas')
    mask_todas_duplicadas = df.index.duplicated(keep=False)
    idx_inicio_dups       = np.where(mask_todas_duplicadas & ~df.index.duplicated(keep='first'))[0]
    
    no_corrige = [] # Se crea esta variable para almacenar las entradas duplicadas que se 
                    # encuentran desfasadas por más de una hora, ya que esto probablemente sea por
                    # un error de formato en la fecha
        
    if len(idx_inicio_dups) > 0:

        # Se usa la columna 1 (normalmente temperatura) para decidir cual entrada permanece
        vals    = df.iloc[:, 0].values.copy()
        tiempos = df.index

        # Se itera y se corrigen los duplicados de 2 en 2
        # NOTA: Funciona bien si solo hay 2 entradas para el mismo periodo, si hay más entradas    
        #       estas por más que se leen, no pasan la comparación por lo que solo se tienen en 
        #       cuenta las primeras 2.
        for idx in idx_inicio_dups:
            hora_prev = tiempos[idx-1]  # Fecha y hora del dato anterior
            hora      = tiempos[idx]    # Fecha y hora del dato que se esta comparando

            val_prev  = vals[idx-1]     # Valor previo (referencia de consistencia)
            val1      = vals[idx]       # Valor de la entrada
            val2      = vals[idx+1]     # Valor de la repetición
            
            if (hora - hora_prev < pd.Timedelta('1h')) or np.isnan(val_prev):
                dif1 = abs(val1 - val_prev)
                dif2 = abs(val2 - val_prev)
                
                # Se compara cual de los repetidos es más coherente y se fuerza a que toda la fila sea igual al seleccionado en el df original
                if dif1 <= dif2:
                    df.iloc[idx+1, :] = df.iloc[idx, :]
                else:
                    df.iloc[idx, :] = df.iloc[idx+1, :]

            else:
                no_corrige.append(hora)

    if len(no_corrige) > 0:
        print(f"No corregibles: {no_corrige}")
        raise Exception('Fechas duplicadas: revisar serie')

    idx_eliminados = df.index.duplicated(keep='first')
    
    if idx_eliminados.any():
        eliminados = df.loc[idx_eliminados].copy()
    else:
        eliminados = pd.DataFrame(columns=df.columns, dtype='float64')

    # Aplicamos la limpieza definitiva en el DataFrame
    df = df[~idx_eliminados] 
    
    Entradas_Duplicadas.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal6_duplicidad_entradas.variables   = [] # Variables requeridas para funcionar
CCal6_duplicidad_entradas.nombre      = 'Duplicidad de Entradas'  # Nombre visible
CCal6_duplicidad_entradas.obligatorio = True
CCal6_duplicidad_entradas.visible     = True