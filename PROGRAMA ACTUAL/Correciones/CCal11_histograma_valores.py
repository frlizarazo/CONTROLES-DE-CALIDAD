import os
import numpy             as np
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

def histogramas(df, _estacion, _graficar, _ruta_graficas,_tipo='valores'):
    """
    Genera histogramas de cada variable, y cuando hay un intervalo de valores
    sin datos elimina los de los intervalos que están más lejos de la mediana
    que dicho intervalo sin datos.

    df, eliminados = correccion_histogramas(df, ruta, estacion, graficar, tipo)
    
    Parámetros de entrada
    ---------------------
    df : DataFrame
        Serie de tiempo con los datos sin corregir.
    estacion : cadena
        Nombre de la estación.
    graficar : booleano
        Si se generan o no las gráficas.
    tipo : cadena
        Indica de qué son los histogramas, 'valores' corresponde a histogramas
        de los valores de cada variable, y 'diferencias_consecutivas' a
        histogramas de las diferencias consecutivas de los valores de cada
        variable.

    Parámetros de salida
    --------------------
    df : DataFrame
        Serie de  tiempo con los datos corregidos.
    eliminados : DataFrame
        Contiene los datos eliminados por el filtro. Cuando en una hora solo se
        eliminan datos de algunas variables, en las demás se pone `nan`.
    """

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

    return df, eliminados 

def CCal11_histograma_valores(df, estacion, graficar, _ruta_graficas):
    """
    correccion_histogramas con el parámetro tipo='valores'.
    """
    df, eliminados = histogramas(df, estacion, graficar, _ruta_graficas, _tipo='valores')

    #print('Histograma done')

    return df, eliminados

CCal11_histograma_valores.nombre = 'Histogramas valores'
CCal11_histograma_valores.variables = []