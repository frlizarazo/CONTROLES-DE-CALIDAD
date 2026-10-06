# ================================================================================================ #
#                                                                                                  #
#                               dP"Y8 88 8b    d8    db     dP""b8                                 #
#                               Ybo   88 88b  d88   dPYb   dP                                      #
#                                 Y8b 88 88YbdP88  dP__Yb  Yb                                      #
#                              8bodP  88 88 YY 88 dP    Yb  YboodP                                 #
#                                                                                                  #
# ================================================================================================ #
#                                                                                                  #
# ARCHIVO: main.py                                                                                 #
# DESCRIPCIÓN: Script principal del programa                                                       #
#                                                                                                  #
# AUTOR: Franklin Andrés Lizarazo Muñoz                                                            #
#                                                                                                  #
# VERSION DEL SCRIPT: 1                                                                            #
#                                                                                                  #
# NOTAS:                                                                                           #
#                                                                                                  #
# ================================================================================================ #


# LIBRERÍAS DE PYTHON ============================================================================ #
import os
import tkinter as tk

# MÓDULOS ======================================================================================== #

## ESTILOS Y PERSONALIZACIÓN -------------------------------------------------------------------- ##
from Estilos.colores import *
from Estilos.tema    import apply_style

## OBJETOS Y SECCIONES -------------------------------------------------------------------------- ##
from Elementos.Secciones.Encabezado            import Encabezado
from Elementos.Secciones.Barra_de_Herramientas import Barra_de_Herramientas
from Elementos.Secciones.Consola               import Consola
from Elementos.Secciones.Pie                   import Pie

from Elementos.barra_de_carga import barra_de_carga

## FUNCIONES ------------------------------------------------------------------------------------ ##
from Funciones.cargar_ajustes import cargar_ajustes
from Funciones.cargar_icono   import cargar_icono

# VENTANA PRINCIPAL ============================================================================== #

class Ventana_principal(tk.Tk):
    '''
    Objeto de ventana principal con los métodos:

    .iniciar_programa(): envía la ventana principal al loop principal y da mensaje de bienvenida
    .cerrar_programa(): cierra el programa eliminando todos los hilos abiertos 
    .cargar_ajustes(): carga las variables almacenadas en el archivo .config
    '''

    def __init__(self):

        # Inicialización de la ventana
        super().__init__()

        self.title('Análisis de Series V1.0')
        self.config(bg = COLOR_FONDO)

        apply_style()
        cargar_icono(self)
        self.cargar_ajustes()

        # Inicialización de las secciones y objetos de la ventana
        self.encabezado            = Encabezado(self)
        self.barra_de_herramientas = Barra_de_Herramientas(self)
        self.consola               = Consola(self)
        self.pie                   = Pie(self)

        self.barra_de_carga        = barra_de_carga(self)

        # Captura y redirección del método de cierre de la ventana de windows
        self.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

    def iniciar_programa(self):

        # Enviar ventana al bucle principal
        self.mainloop()

        # Escribir mensaje de bienvenida
        self.consola.escribir('Bienvenido, por favor realiza alguna acción para comenzar')
    
    def cerrar_programa(self):

        # Métodos de cierre del programa
        self.quit()
        self.destroy()
        os._exit(0)

    def cargar_ajustes(self):

        # Variables cargadas del archivo .config
        (self.directorio_inicial, 
         self.directorio_de_salida,
         self.protocolo_de_seleccion,
         self.patron_de_seleccion,
         self.exportar_eliminados,
         self.exportar_graficas,
         self.resolucion,
         self.formato_fecha,
         self.resolucion_pluviometro) = cargar_ajustes()

# INICIALIZACIÓN ================================================================================= #

if __name__ == '__main__':

    Programa = Ventana_principal()
    Programa.iniciar_programa()

# FIN ============================================================================================ #