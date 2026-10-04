import pandas as pd
import numpy as np

def saltos_y_separador(ruta):
    
    with open(ruta,'r') as file:
        for saltos, lina in enumerate(file):
            pcoma = lina.count(';')
            coma  = lina.count(',')

            separador = ',' if coma > pcoma else ';' if pcoma > 0 else False
            
            if separador:
                break

    return saltos, separador

# %%
def leer_datos(ruta):
    """
    Se lee la serie de datos del archivo.

    df = leer_datos(archivo, columnas)

    Parámetros de entrada
    ---------------------
    archivo : cadena
        Ubicación del archivo, incluyendo la extensión '.csv'
    columnas : lista
        Lista con los nombres de las columnas.
    
    Parámetros de salida
    --------------------
    df : DataFrame
        Serie con los datos.
    """
    # Se establece el tipo de separador del archivo (,|;) y el numero de lineas a saltar de encabezado
    saltos, separador = saltos_y_separador(ruta)
    print(f"Se detectó el separador '{separador}' y se saltaron {saltos} líneas de encabezado.")

    # Se leen los datos
    df = pd.read_csv(
        ruta, 
        sep          = separador, 
        skiprows     = saltos,
        encoding     = 'utf-8', 
        header       = 0, 
        na_values    = ['-', 'X', 'NA', '.', 'ND'],
        on_bad_lines = 'skip',
        engine       ='c',
        index_col    = False,
        low_memory   = False
    )

    df.columns = [columna.strip() for columna in df.columns]
 
    return df
# %%
