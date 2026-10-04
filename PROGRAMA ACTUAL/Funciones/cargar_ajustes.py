import os
import re

def cargar_ajustes():
    try: 
        with open('.config', 'r', encoding = 'utf-8') as f:
            datos = f.readlines()
            datos = [eval(conf.strip().split(' = ')[1]) for conf in datos]

        directorio_inicial     = datos[0] if datos[0] != '' else os.getcwd().replace('\\','/')
        directorio_de_salida   = datos[1] if datos[1] != '' else os.getcwd().replace('\\','/') + '/Salida'
        protocolo_de_seleccion = datos[2]
        patron_de_seleccion    = datos[3]
        exportar_eliminados    = datos[4]
        exportar_graficas      = datos[5]
        resolucion             = int(datos[6])
        formato_fecha          = datos[7]

    except:
        directorio_inicial     = os.getcwd().replace('\\','/')
        directorio_de_salida   = os.getcwd().replace('\\','/') + '/Salida'
        protocolo_de_seleccion = 'por archivos'
        patron_de_seleccion    = '*'
        exportar_eliminados    = 'no'
        exportar_graficas      = 'no'
        resolucion             = '5'
        formato_fecha          = '%d/%m/%Y %H:%M:%S'

        datos = f"""directorio_inicial     = '{directorio_inicial}'
directorio_de_salida   = '{directorio_de_salida}'
protocolo_de_seleccion = {protocolo_de_seleccion}
patron_de_seleccion    = '{patron_de_seleccion}'
exportar_eliminados    = {exportar_eliminados}
exportar_graficas      = {exportar_graficas}
resolucion             = {resolucion}
formato_fecha          = {formato_fecha}'"""

        guardar_ajustes(datos = datos)


    return (directorio_inicial, 
            directorio_de_salida, 
            protocolo_de_seleccion, 
            patron_de_seleccion,
            exportar_eliminados,
            exportar_graficas,
            resolucion,
            formato_fecha)

def guardar_ajustes(valor = '0', configuracion = 'Ninguna', datos = ''):

    try:

        with open('.config', 'r', encoding = 'utf-8') as f:

            datos = f.readlines()

            for i,linea in enumerate(datos):
                datos[i] = re.sub(r'= .*',"= '" + valor + "'", linea) if configuracion in linea else linea
    
    except:
        pass
    
    with open('.config', 'w', encoding = 'utf-8') as f:
        f.writelines(datos)