import pandas as pd
import numpy  as np
import os

import Correciones as c

from time import time

from Funciones.leer_datos     import leer_datos
from Funciones.exportar_datos import exportar, exportar_eliminados

def analisis(_archivo, _columnas, _filtros, _destino, _altitud = np.nan, _exportar_graficas = False, _exportar_eliminados = False, formato_fecha = '%d/%m/%Y %H:%M:%S'):
    """
    Interpola la serie del archivo, y aplica las correcciones indicadas. 
    Genera un archivo CSV con la serie tras aplicarle las correcciones.

    analisis(archivo, columnas, filtros, destino, altitud=np.nan, exportar_eliminados=False)

    Parámetros de entrada
    ---------------------
    archivo : cadena
        Ubicación del archivo.
    columnas : lista (cadenas)
        Contiene los nombres de las columnas de la serie
    filtros : lista (funciones)
        Contiene las correcciones que se van a aplicar
    destino: cadena
        Carpeta en la que se almacenan los archivos generados
    altitud : número
        Altitud de la estación correspondiente a la serie del archivo, en
        m.s.n.m.
    exportar_eliminados : booleano
        Opción para crear un archivo de Excel con el reporte de datos elminados
    """
    df = leer_datos(_archivo.ruta)
    df = df[list(_columnas.keys())]

    columnas_iniciales = list(_columnas.values())
    conteo             = {}
    columnas           = []

    for columna in columnas_iniciales:
        if columna in conteo:
            conteo[columna] += 1
            nuevo_nombre = f"{columna} ({conteo[columna]})"
        else:
            conteo[columna] = 0
            nuevo_nombre = columna
        columnas.append(nuevo_nombre)

    df.columns = list(columnas)

    _columnas = dict(zip(_columnas.keys(), columnas))

    # Para que el indice no tenga fila a parte con el nombre
    df.index.names = [None]
    
    # Se deja como indice una columna con fecha y hora con formato m/d/y h:m:s
    df.set_index(pd.to_datetime(df['Fecha'] + ' ' + df['Hora'],
                                format  = formato_fecha, 
                                cache   = False), 
                                inplace = True)
    
    # Se eliminan las columnas de fecha y hora
    df.drop(df.columns[[0, 1]], axis = 1, inplace = True)   

    estacion = _archivo.nombre

    ruta_de_salida = _destino + '/' + estacion
    os.makedirs(ruta_de_salida, exist_ok = True)

    ruta_graficas     = ruta_de_salida + '/Graficas'
    graficar          = True if _exportar_graficas == 'si' else False
    
    try:
        if c.CCal8_homogenizacion_intervalos in _filtros:
            homogenizacion_intervalos        = lambda df: c.CCal8_homogenizacion_intervalos(df, formato_fecha)
            homogenizacion_intervalos.nombre = c.CCal8_homogenizacion_intervalos.nombre

            _filtros[_filtros.index(c.CCal8_homogenizacion_intervalos)] = homogenizacion_intervalos
            
        if c.CCal11_histograma_valores in _filtros:
            histograma_valores        = lambda df: c.CCal11_histograma_valores(df, estacion, graficar, ruta_graficas)
            histograma_valores.nombre = c.CCal11_histograma_valores.nombre

            _filtros[_filtros.index(c.CCal11_histograma_valores)] = histograma_valores

        if c.CCal12_deviaciones_estandar in _filtros:
            percentil_horario        = lambda df: c.CCal12_deviaciones_estandar(df, ruta_graficas, graficar)
            percentil_horario.nombre = c.CCal12_deviaciones_estandar.nombre

            _filtros[_filtros.index(c.CCal12_deviaciones_estandar)] = percentil_horario
    except:
        pass

    datos_eliminados = {}

    for i,filtro in enumerate(_filtros):
        inicio    = time()
        resultado = filtro(df)
    
        if isinstance(resultado, tuple) and len(resultado) == 2:
            df, eliminados_filtro = resultado
        else:
            df = resultado
            eliminados_filtro = None

        if eliminados_filtro is not None and len(eliminados_filtro) > 0:
            datos_eliminados[filtro.nombre] = eliminados_filtro
        fin    = time()
        print(f'Filtro {filtro.nombre} ejecutado en {round(fin-inicio,2)}')

    encabezado = []
    palabras   = ['Fecha', 'Hora']

    try:
        if c.CCal5_recalculo_ppt_cincominutal in _filtros:
            palabras.append('Precipitación Acumulada')
        if c.CCal6_recalculo_evt_cincominutal in _filtros:
            palabras.append('Evapotranspiración Acumulada')
    except:
        pass

    _columnas = {v: k for k, v in _columnas.items()}
    columnas = list(_columnas.keys())
    columnas = [
        columna 
        for columna in columnas 
        if not any(
            palabra in columna
            for palabra in palabras
        )
    ]

    df       = df.reindex(columns=columnas)
    columnas = [_columnas[col] for col in columnas]
    df.columns = columnas

    os.makedirs(ruta_de_salida, exist_ok = True)
    exportar(df, ruta_de_salida + '/' + f'{estacion}_corregido.csv', encabezado)

    if _exportar_eliminados == 'si':
        exportar_eliminados(datos_eliminados, ruta_de_salida)