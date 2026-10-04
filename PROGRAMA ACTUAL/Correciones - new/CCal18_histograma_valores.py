# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: CCal18_histograma_valores.py                                                               #
# DESCRIPCIÓN: Aplica corrección de veleta estática a los datos de precipitación                   #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# USO:                                                                                             #
#   CCal18_histograma_valores(df)                                                                     #
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

import os
import pandas            as pd
import matplotlib.pyplot as plt

from Datos.columnas import UNIDADES

def graficar_histograma(barras, frecuencia_relativa, guardar, limites, titulo):
    try:
        ancho_barra = np.diff(barras)[0]

    except IndexError:
        return
    
    plt.bar(barras, frecuencia_relativa, ancho_barra, edgecolor='black')

    plt.axvline(x=limites[0], c='r', label='Límite inferior')
    plt.axvline(x=limites[1], c='r', label='Límite superior')

    plt.text(
        limites[0], 
        0.6, 
        f'{limites[0]:.2f}', 
        color     = 'k', 
        ha        = 'right',     
        va        = 'top', 
        rotation  = 90, 
        transform = plt.gca().get_xaxis_transform()
    )
    
    plt.text(
        limites[1], 
        0.6, 
        f'{limites[1]:.2f}', 
        color     = 'k', 
        ha        = 'left',     
        va        = 'top', 
        rotation  = 90, 
        transform = plt.gca().get_xaxis_transform()
    )
    
    plt.xlabel(f'Valores de la variable')
    plt.ylabel('Frecuencia relativa (%)')
    plt.title (titulo)
    plt.yscale('log')
    plt.rc    ('axes', axisbelow=True)
    plt.grid  (True, which="both", color='0.8', linestyle='dotted')
    plt.legend()

    plt.savefig(guardar, bbox_inches='tight')
    plt.close()


# CONTROL DE CALIDAD ============================================================================= #
def CCal18_histograma_valores(df, _estacion, _graficar, _ruta_graficas,_tipo='valores'):

    Histograma_Valores = Instrumentar('Aplica corrección de Histograma de Valores')

    # columnas para las que se puede hacer esta corrección
    columnas_posibles = ['Temperatura',
                         'Temperatura del Agua',
                         'Velocidad del Viento',
                         'Presión Barométrica', 
                         'Humedad Relativa',
                         'Precipitación',
                         'Radiación Solar', 
                         'Evapotranspiración', 
                         'Nivel']

    mascara               = [c in columnas_posibles for c in df.columns]
    columnas_consideradas = [c for c, m in zip(df.columns, mascara) if m]

    if _tipo == 'valores':
        diferencias = df[columnas_consideradas]

    elif _tipo == 'diferencias_consecutivas':
        diferencias = df[columnas_consideradas].diff()

    eliminados = []

    if _graficar: os.makedirs(_ruta_graficas, exist_ok=True)

    for variable in columnas_consideradas:
        valores          = diferencias[variable]
        columna_variable = valores[valores.notnull()]

        # Divisiones del histograma
        n_datos = len(columna_variable)

        if n_datos == 0:
            continue

        n_barras = int(round(1+3.322*np.log10(n_datos)))

        # Elementos del gráfico
        frecuencia, barras = np.histogram(columna_variable, bins=n_barras)
        mitad_ancho_barra  = (barras[1] - barras[0])/2
        barras             = barras[:-1] + mitad_ancho_barra

        # Análisis extra para los limites
        frecuencia_relativa = frecuencia*100/n_datos
        
        # Se analiza la continuidad del histograma de diferencias
        # Se encuentran los valores cero del hietogrma que marcan sus limites
        id_cero_negativo = (np.where((frecuencia_relativa == 0) & 
                                     (barras < columna_variable.median())))[0]

        id_cero_positivo = (np.where((frecuencia_relativa == 0) & 
                                     (barras > columna_variable.median())))[0]
        
        # Barras negativas y que no tengan datos  y barras positivas que si tengan datos 
        if len(id_cero_negativo)==0 and len(id_cero_positivo)!=0:
            id_cero_positivo = id_cero_positivo[0]
            lim_inf          = barras[0] 
            lim_sup          = barras[id_cero_positivo-1]
            
        # Barras negativas con datos y positivas sin datos      
        elif len(id_cero_negativo)!=0 and len(id_cero_positivo)==0:
            id_cero_negativo = id_cero_negativo[-1]
            lim_inf          = barras[id_cero_negativo+1]
            lim_sup          = barras[-1]
            
        # No hay datos      
        elif len(id_cero_negativo)==0 and len(id_cero_positivo)==0:
            lim_inf = barras[0]
            lim_sup = barras[-1]
        
        # Barras postivas y negativas con datos
        else:
            id_cero_negativo = id_cero_negativo[-1]
            id_cero_positivo = id_cero_positivo[0]
            lim_inf          = barras[id_cero_negativo+1]
            lim_sup          = barras[id_cero_positivo-1]
        
        # Se agregan a una lista para cada variable sus limites superior e inferior
        # teniendo en cuenta el método de diferencias aplicado y la continuación 
        # del histograma
        
        lim_inf -= mitad_ancho_barra
        lim_sup += mitad_ancho_barra

        if _graficar:
            if _tipo == 'valores':
                titulo  = f'Valores de {UNIDADES[variable]} \n Estación {_estacion}'
                guardar = os.path.join(_ruta_graficas, f'{_estacion}_valores_{variable}.png')

            elif _tipo == 'diferencias_consecutivas':
                titulo  = f'Diferencias consecutivas de {UNIDADES[variable]} \n Estación {_estacion}'
                guardar = os.path.join(_ruta_graficas, f'{_estacion}_diferencias_{variable}.png')

            graficar_histograma(barras, frecuencia_relativa, guardar, (lim_inf, lim_sup), titulo)

        # Para los datos que se encuentren por fuera de los limites calculados por la
        # metodología de diferencias, se vuelven NaNs 
        # OJO: SE PUEDE AGREGAR LOS DATOS SOSPECHOSOS ENCONTRADOS Y DARLE AL
        # INVESTIGADOR LA DECISIÓN DE ELIMINAR O NO LOS DATOS.
        
        idx = diferencias[(diferencias[variable] < lim_inf) | 
                          (diferencias[variable] > lim_sup)].index
        
        if len(idx) > 0:
            eliminados.append(df.loc[idx, variable].copy())

        df.loc[idx, variable] = np.nan  # Se vuelven NaN

    if len(eliminados) > 0:
        eliminados = pd.concat(eliminados, axis=1, sort=True)

    Histograma_Valores.fin()

    return df, eliminados

# ATRIBUTOS DEL CONTROL DE CALIDAD =============================================================== #
CCal18_histograma_valores.variables   = [] # Variables requeridas para funcionar
CCal18_histograma_valores.nombre      = 'Histograma de Valores'  # Nombre visible
CCal18_histograma_valores.obligatorio = False
CCal18_histograma_valores.visible     = True