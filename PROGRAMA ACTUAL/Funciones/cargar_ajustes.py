import os
import json
from tkinter import messagebox

# Ruta absoluta basada en la ubicación real de este archivo
CARPETA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(CARPETA_RAIZ, 'config.json')

# Configuración por defecto (incluyendo la resolución del pluviómetro)
AJUSTES_POR_DEFECTO = {
    "directorio_inicial": os.getcwd().replace('\\', '/'),
    "directorio_de_salida": os.getcwd().replace('\\', '/') + '/Salida',
    "protocolo_de_seleccion": "por archivos",
    "patron_de_seleccion": "*",
    "exportar_eliminados": "no",
    "exportar_graficas": "no",
    "resolucion": 5,
    "formato_fecha": "%d/%m/%Y %H:%M:%S",
    "resolucion_pluviometro": 0.2  # <-- Nueva variable añadida
}

def cargar_ajustes():
    """Carga los ajustes desde el archivo JSON. Si no existe o falla, usa los valores por defecto."""
    if not os.path.exists(CONFIG_PATH):
        guardar_todos_los_ajustes(AJUSTES_POR_DEFECTO)
        return tuple(AJUSTES_POR_DEFECTO.values())
    
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Asegurar que si agregas nuevas opciones, no falten claves en archivos viejos
        for clave, valor in AJUSTES_POR_DEFECTO.items():
            if clave not in datos:
                datos[clave] = valor
                
        return (
            datos.get("directorio_inicial"),
            datos.get("directorio_de_salida"),
            datos.get("protocolo_de_seleccion"),
            datos.get("patron_de_seleccion"),
            datos.get("exportar_eliminados"),
            datos.get("exportar_graficas"),
            int(datos.get("resolucion", 5)),
            datos.get("formato_fecha"),
            float(datos.get("resolucion_pluviometro", 0.2)) # <-- Devolviéndola como float
        )
    except Exception as e:
        messagebox.showerror(
            "Error de Configuración", 
            f"No se pudieron leer los ajustes anteriores.\nSe restaurarán los valores por defecto.\n\nDetalle: {e}"
        )
        return tuple(AJUSTES_POR_DEFECTO.values())

def guardar_ajustes(valor='0', configuracion='Ninguna', datos=''):
    """Guarda un ajuste específico actualizando el archivo JSON de forma segura."""
    config_actual = AJUSTES_POR_DEFECTO.copy()
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config_actual = json.load(f)
        except Exception:
            pass
            
    if configuracion != 'Ninguna':
        config_actual[configuracion] = valor
        
    guardar_todos_los_ajustes(config_actual)

def guardar_todos_los_ajustes(datos_dict):
    """Escribe el diccionario completo en el archivo JSON con manejo de errores."""
    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(datos_dict, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror(
            "Error al Guardar", 
            f"No se pudieron guardar los cambios.\nVerifica que tengas permisos de escritura en la carpeta del programa.\n\nDetalle: {e}"
        )