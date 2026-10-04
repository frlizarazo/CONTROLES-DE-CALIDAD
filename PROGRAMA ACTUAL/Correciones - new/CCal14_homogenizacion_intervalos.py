# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal14_homogenización_intervalos.py                                                     #
# DESCRIPCIÓN: Homogeniza los intervalos de tiempo                                                 #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal14_homogenización_intervalos(df)                                                           #
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
import datetime as dt
from Funciones.instrumentar import Instrumentar

# CONTROL DE CALIDAD ============================================================================= #
def CCal14_homogenizacion_intervalos(df):

    Homogenización_Intervalos   = Instrumentar('Homogeniza los intervalos de tiempo de los datos de precipitación')

    with open('.config', 'r', encoding='utf-8') as f:
        res = int(f.readlines()[6].split('=')[-1].strip().replace("'",''))

    # la función crear_filtro es para que cuando se interpole no se consideren
    # los valores interpolados cuando haya más de 1 nan entre datos válidos
    
    def crear_filtro(df, max_nan=1):
        mask        = df.copy()
        grp         = ((mask.notnull() != mask.shift().notnull()).cumsum())
        grp['ones'] = 1
        
        for col in df:
            mask[col] = (grp.groupby(col)['ones'].transform('count') <= max_nan) | df[col].notnull()
            
        return mask
    
    # se define la función para interpolar los valores cuando solo haya un valor
    def arrastrar_cerca(serie, delta=pd.Timedelta(f'{res/2}min')):
        r                  = serie.reset_index()
        es_nan             = r.iloc[:,1].isna()
        siguiente_cerca    = (r['index'] - r.shift()['index'] <= delta) & es_nan
        anterior_cerca     = (r.shift(-1)['index'] - r['index'] <= delta) & es_nan
        r[siguiente_cerca] = r.shift()[siguiente_cerca]
        r[anterior_cerca]  = r.shift(-1)[anterior_cerca]
        
        return r.set_index(serie.index).iloc[:,1]
    
    def crear_df_cincomin(df):
        "crea un dataframe con índices exactos y las mismas columnas de df"
        delta  = dt.timedelta(minutes=res)

        # cálculo hora inicio
        ajuste1 = (dt.datetime.min - df.index[0]) % delta

        if ajuste1 == dt.timedelta(0):
            hora_inicio = df.index[0]

        else:
            hora_inicio = df.index[0] + ajuste1 - delta

        # cálculo hora fin
        ajuste2 = (dt.datetime.min - df.index[-1]) % delta

        if ajuste2 == dt.timedelta(0):
            hora_fin = df.index[-1]

        else:
            hora_fin = df.index[-1] + ajuste2

        idx = pd.date_range(hora_inicio, hora_fin, freq=f'{res}min')

        return pd.DataFrame(index=idx, columns=df.columns)
    
    # se crea un df vacío con la forma del original, con índices cada 5 min
    cincomin = crear_df_cincomin(df)
    cincomin_index = list(df.index) + list(cincomin[~np.isin(cincomin.index.values, df.index.values)].index)
    
    df_2 = df.reindex(pd.to_datetime(cincomin_index,
                                format  = '%d/%m/%Y %H:%M:%S', 
                                cache   = False)).sort_index()

    # se realizan las interpolaciones
    try:
        Observaciones = df_2['Observaciones']
        df_2 = df_2.drop(columns='Observaciones')
        df_2.drop(columns=['Dirección de la Rosa'], inplace=True)
        df_2 = df_2.interpolate(method='index', limit=1)[crear_filtro(df_2)]
        df_2['Observaciones'] = Observaciones
        df_2 = df_2.apply(arrastrar_cerca).loc[cincomin.index]
    except KeyError:
        pass

    # se asigna la dirección de la rosa de acuerdo a la dirección del viento    
    if 'Dirección del Viento' in df.columns:
        vals = np.array([  0, 11, 33, 55, 78, 100, 123, 145, 168, 190,
                         213, 235, 258, 280, 303, 325, 348, 360])
        
        bins = pd.IntervalIndex.from_arrays(vals[:-1], vals[1:], closed='left')

        dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S',
                'SSO','SO','OSO','O','ONO','NO','NNO','N']
    
        try:
            df_2['Dirección de la Rosa'] = np.array(dirs)[pd.cut(df_2['Dirección del Viento'],
                                                         bins = bins).cat.codes]
            df_2.loc[df_2['Dirección del Viento'].isna(), 'Dirección de la Rosa'] = np.nan
        
        except KeyError:
            pass

    eliminados = pd.Series(dtype='float64')
    Homogenización_Intervalos.fin()

    return df_2, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal14_homogenizacion_intervalos.variables   = [] # Variables requeridas para funcionar
CCal14_homogenizacion_intervalos.nombre      = 'Homogenización de Intervalos'  # Nombre visible
CCal14_homogenizacion_intervalos.obligatorio = False
CCal14_homogenizacion_intervalos.visible     = True