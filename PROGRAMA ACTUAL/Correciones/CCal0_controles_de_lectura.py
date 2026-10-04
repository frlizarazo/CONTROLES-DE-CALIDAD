# ============================================================================ #
#                                                                              #
#                   dP"Y8 88 8b    d8    db     dP""b8                         #
#                   Ybo   88 88b  d88   dPYb   dP                              #
#                     Y8b 88 88YbdP88  dP__Yb  Yb                              #
#                  8bodP  88 88 YY 88 dP    Yb  YboodP                         #
#                                                                              #
# ============================================================================ #
#                                                                              #
# ARCHIVO: CCal0_controles_de_lectura.py                                       #
# DESCRIPCIÓN: Correcciónes de formato para la correcta interpretación de los  #
#              datos como una serie temporal                                   #
#                                                                              #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                        #
#                                                                              #
# VERSION DEL SCRIPT: 2                                                        #
#   Se realizarón cambios de optimización pasando de bucles que iteraban sobre #
#   todas las filas repetidas a alternativas matriciales                       #
#                                                                              #
#   Se mejoró el algoritmo de corrección de multiples entradas para el mismo   #
#   periodo de tiempo                                                          #
#                                                                              #
# NOTAS:                                                                       #
#   Este control se aplica siempre y no sale dentro del apartado de filtros    #
#                                                                              #
# ============================================================================ #
# LIBRERÍAS DE PYTHON                                                          #
# ============================================================================ #

import pandas as pd
import numpy as np

# FUNCIONES ====================================================================================== #

from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #

def CCal0_controles_de_lectura(df):
    '''
    Son correcciones principalmente de formato que se aplican siempre para garantizar que los demás
    controles de calidad se puedan aplicar correctamente.

    df, eliminados = CCal0_controles_de_lectura(df)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
         Serie de tiempo con los datos sin corregir.

    Parámetros de salida
    --------------------
    df : DataFrame
         Serie de  tiempo con los datos corregidos.

    eliminados : DataFrame
                 Contiene los datos eliminados.
    '''

    ## CONVERSIÓN DE DATOS NUMÉRICOS ------------------------------------------------------------ ##
    Convertir_Numerico = Instrumentar('Convertir a numérico', 1)
    cols_excluir       = ['Fecha', 'Hora', 'Dirección de la Rosa', 'Observaciones']
    cols_convertir     = [col for col in df.columns if col not in cols_excluir]
    df[cols_convertir] = df[cols_convertir].apply(pd.to_numeric, errors='coerce', downcast='float')
    Convertir_Numerico.fin()

    ## ENTRADAS COMPLETAS DUPLICADAS ------------------------------------------------------------ ##
    Filas_Duplicadas = Instrumentar('Eliminar filas completas duplicadas', 1)
    duplicated_mask  = df.reset_index().duplicated()
    eliminados       = df.iloc[duplicated_mask.values]
    df               = df.reset_index().drop_duplicates().set_index('index').sort_index()
    Filas_Duplicadas.fin()

    ## MULTIPLES ENTRADAS PARA EL MISMO PERIODO ------------------------------------------------- ##
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

    df = df[~df.index.duplicated(keep='first')] 
    Entradas_Duplicadas.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal0_controles_de_lectura.variables = [] # Variables requeridas para funcionar
CCal0_controles_de_lectura.nombre    = 'Controles de Lectura'  # Nombre visible