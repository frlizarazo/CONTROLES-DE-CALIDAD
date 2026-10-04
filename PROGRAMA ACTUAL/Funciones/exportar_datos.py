import os
import pandas as pd

def exportar(df, nombre, comentarios=[]):
    """
    Exporta un DataFrame en un documento CSV.
    
    Parámetros de entrada
    ---------------------
        df : DataFrame
            DataFrame con los datos.
        nombre : cadena
            Ubicación del archivo a generar.
        comentarios : lista
            Texto a imprimir antes de los datos. Cada elemento de la lista
            va en una línea diferente del archivo.
    """
    
    # se escriben los comentarios, sobreescribiendo el archivo
    f     = open(nombre, 'w', encoding="utf-8")
    texto = ''

    for linea in comentarios:
        texto += linea + '\n' 
        
    f.write(texto)
    f.close()

    # se redondean los valores a imprimir, se separan la fecha y la hora, y se
    # exporta el archivo
    df_e          = df.round(2)
    df_e['Fecha'] = df_e.index.strftime('%d/%m/%Y')
    df_e['Hora']  = df_e.index.time
    cols          = list(df_e.columns)
    cols          = cols[-2:] + cols[:-2]
    df_e          = df_e[cols]
    
    df_e.to_csv(nombre, sep=',', index=False, mode='a', na_rep='')

def exportar_eliminados(datos_eliminados, ruta):
    """
    Exporta el diccionario con los datos eliminados a un documento de Excel, 
    donde cada hoja corresponde a los datos eliminados por una corrección.

    Parámetros de entrada
    ---------------------
        datos_eliminados : diccionario
            La llave de cada entrada es el nombre del filtro correspondiente,
            y el valor es la serie o DataFrame con los datos eliminados.
        ruta : cadena
            Ubicación donde se genera el archivo.
    
    """
    carpeta = os.path.join(ruta, 'datos_eliminados')
    os.makedirs(carpeta, exist_ok=True)

    for filtro in datos_eliminados:
        with pd.ExcelWriter(os.path.join(carpeta, f'{filtro}.xlsx')) as archivo:
            datos = datos_eliminados[filtro]

            if isinstance(datos, pd.Series):
                if len(datos.index) > 500000:
                    datos = datos.iloc[:500000]

                datos.to_excel(archivo, engine='xlsxwriter')

            else:
                if ('completas' in filtro) or (filtro == 'Valores nulos'):
                    if len(datos.index) > 500000:
                        datos = datos.head(500000)

                    datos.to_excel(archivo, engine='xlsxwriter')

                else:
                    for variable in datos.columns:
                        var = datos[variable].dropna()

                        if len(var.index) > 500000:
                            var = var.iloc[:500000]
                            
                        var.to_excel(archivo, sheet_name=variable, engine='xlsxwriter')