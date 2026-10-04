# ================================================================================================ #
#                                                                                                  #
#                               dP"Y8 88 8b    d8    db     dP""b8                                 #
#                               Ybo   88 88b  d88   dPYb   dP                                      #
#                                 Y8b 88 88YbdP88  dP__Yb  Yb                                      #
#                              8bodP  88 88 YY 88 dP    Yb  YboodP                                 #
#                                                                                                  #
# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal1_extracción_de_observaciones.py                                                    #
# DESCRIPCIÓN: Recuperación de datos de variables que se enviaron erroneamente al campo de         #
#              observaciones                                                                       #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#   Por el momento el script solo extrae valores de nivel del campo de observaciones               #
#                                                                                                  #
# ================================================================================================ #

# CONTROL DE CALIDAD ============================================================================= #
 
def CCal1_extracción_de_observaciones(df):
    """
    Extrae el nivel de la columna 'Observaciones' y lo asigna a la columna 'Nivel'.

    Parámetros:
    - df: DataFrame que contiene las columnas 'Observaciones' y 'Nivel'.

    Retorna:
    - df: DataFrame modificado con los niveles extraídos.
    """

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

    return df

# Metadatos de la función
CCal1_extracción_de_observaciones.variables = ['Nivel', 'Observaciones']
CCal1_extracción_de_observaciones.nombre    = 'Extraer Nivel de Observaciones'