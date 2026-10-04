import numpy  as np
import pandas as pd


def CCal7_limites_fisicos(df, altitud = np.nan):
    """
    Elimina los datos que se salen de los límites físicos establecidos.

    df, eliminados = limites_fisicos(df, altitud=NaN)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.
    altitud : número
        Altitud de la estación.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : DataFrame
        Contiene los datos eliminados.
    """

    limites = {'Temperatura':                     (-np.inf,      100), # permitir valores negativos solo para las altitudes de las P.N.N.N
               'Temperatura del Agua':            (-np.inf,      100),
               'Velocidad del Viento':            (      0,       50), #antes 28.4 - evaluar aumento
               'Dirección del Viento':            (      0,      360),
               'Presión Barométrica':             (   0.01,     1500), # proponer un filtro de rango variable (con histogramas o percentiles)
               'Humedad Relativa':                (   0.01,      100), # proponer un filtro de rango variable (con histogramas o percentiles)
               'Radiación Solar':                 (      0,     1367),
               'Precipitación':                   (      0,      155),
               'Evapotranspiración':              (      0,      160), # Eliminar esto de todo
               'Nivel':                           (      0,   np.inf), # revisar
               'Nivel (1)':                       (      0,   np.inf)} # revisar

    # se crea el filtro de los datos que se salen de los rangos establecidos 
    filtro_limites = pd.DataFrame(False, columns = df.columns, index = df.index)
    eliminados     = pd.DataFrame(columns = df.columns, index = df.index)
    
    for var in limites.keys():
        if var in df.columns:
            filtro_limites[var] = ((df[var] < limites[var][0]) | 
                                   (df[var] > limites[var][1]))

    # se elimina la fila completa si más de 3 columnas tienen datos fuera de los
    # límites
    filas_completas = df[filtro_limites.sum(axis=1) >= 3].index

    if len(filas_completas) > 0:
        eliminados.loc[filas_completas] = df.loc[filas_completas].copy()

    df.loc[filas_completas]             = np.nan
    filtro_limites.loc[filas_completas] = False

    for var in filtro_limites.columns:
        CorVar = df[filtro_limites[var]].index

        if len(CorVar) > 0:
            eliminados.loc[CorVar, [var]] = df.loc[CorVar, [var]].copy()
            df.loc[CorVar, var]           = np.nan

    eliminados = eliminados[eliminados.any(axis=1)]

    eliminados.replace(False, np.nan, inplace=True)
    eliminados.dropna(axis=1, how='all', inplace=True)

    #print('Limites fisicos done')

    return df, eliminados

CCal7_limites_fisicos.variables = []
CCal7_limites_fisicos.nombre    = 'Límites físicos'