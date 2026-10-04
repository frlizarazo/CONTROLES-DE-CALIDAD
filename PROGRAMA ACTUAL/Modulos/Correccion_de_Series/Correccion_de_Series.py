import tkinter as tk
import pandas  as pd
import numpy   as np

from time import time
from tkinter.filedialog import askdirectory, askopenfilenames

from glob    import glob

from Estilos.colores import *

from Elementos.boton_grafico import boton_grafico
from Elementos.espacio       import espacio
from Elementos.separador     import separador
from Elementos.series        import series

from Funciones.hilo_de_ejecución import hilo_ejecucion

import Modulos.Correccion_de_Series.sub_ventanas as sub

from Funciones.analisis import analisis

class Correccion_Series(tk.Frame):
    def __init__(self, _contenedor, _ventana_principal):
        super().__init__(_contenedor)
        self.title = 'Corregir Series'
        self.config(bg = COLOR_PRINCIPAL, width = 600, height = 100)

        espacio(self)

        self.boton_examinar = boton_grafico(
            _contenedor   = self,
            _id           = 0,
            _imagen       = 'abrir',
            _texto        = 'Seleccionar\nSeries',
            _desabilitado = False,
            _funcion      = lambda: self.seleccionar_archivos(_ventana_principal)
        )

        separador(self)

        self.boton_variables = boton_grafico(
            _contenedor   = self,
            _id           = 1,
            _imagen       = 'variables',
            _texto        = 'Variables/\nColumnas',
            _funcion      = lambda: sub.Variables(self, _ventana_principal)
        )

        self.boton_filtros = boton_grafico(
            _contenedor   = self,
            _id           = 2,
            _imagen       = 'correcciones',
            _texto        = 'Seleccionar\nFiltros',
            _funcion      = lambda: sub.Filtros(self, _ventana_principal)
        )

        self.boton_ejecutar = boton_grafico(
            _contenedor   = self,
            _id           = 3,
            _imagen       = 'ejecutar',
            _texto        = 'Aplicar\nFiltros',
            _funcion      = lambda : self.ejecutar(_ventana_principal)
        )
        
        separador(self)

        self.boton_ajustes = boton_grafico(
            _contenedor   = self,
            _id           = 4,
            _imagen       = 'ajustes',
            _texto        = 'Ajustes',
            _desabilitado = False,
            _funcion      = lambda: sub.Ajustes(_ventana_principal)
        )

        espacio(self)

        self.pack()
    
    def seleccionar_archivos(self, _ventana_principal):
        directorio_inicial  = _ventana_principal.directorio_inicial
        patron_de_seleccion = _ventana_principal.patron_de_seleccion

        if _ventana_principal.protocolo_de_seleccion == 'por carpeta':
            dir = askdirectory(
                parent     = self,
                initialdir = directorio_inicial, 
                title      = 'Selecciona el directorio'
            )
            rutas = glob(dir + '/' + patron_de_seleccion + '.csv')

        else: 
            rutas = askopenfilenames(
                parent     = self,
                initialdir = directorio_inicial,
                title      = 'Selecciona los archivos',
                filetypes  = (('Archivos CSV','*.csv'),)
            )

        if len(rutas) > 0:
            self.boton_variables.habilitar()

            rutas = series(rutas)

            _ventana_principal.consola.escribir(f'Se ha(n) seleccionado {rutas.numero} archivo(s)')
            self.rutas = rutas

            try:
                coordenadas = pd.read_csv('coordenadas.csv').set_index('Nombre de la Estación')

            except FileNotFoundError:
                pass

            for i,serie in enumerate(rutas.nombres):
                valor = '---'
                try:
                    valor = int(coordenadas.loc[serie, 'Elevación'])
                except:
                    pass
                
        else:
            _ventana_principal.consola.escribir('No se ha seleccionado ningún archivo')
    
    def ejecutar(self, _ventana_principal):
        hilo_ejecucion(_ventana_principal, lambda : self.ejecutar_analisis(_ventana_principal))

    def ejecutar_analisis(self, _ventana_principal):
        """
        Lee los parámetros de las distintas entradas, y ejecuta la función `analisis`
        """

        self.boton_examinar .desabilitar()
        self.boton_variables.desabilitar()
        self.boton_filtros  .desabilitar()
        self.boton_ejecutar .desabilitar()
        self.boton_ajustes  .desabilitar()

        tiempo_inicial = time()

        filtros  = self.filtros
        destino  = _ventana_principal.directorio_de_salida
        exportar_graficas = _ventana_principal.exportar_graficas
        exportar_eliminados = _ventana_principal.exportar_eliminados

        total_series = len(self.rutas.series)

        # Iniciamos pasando el total exacto de archivos
        _ventana_principal.barra_de_carga.iniciar(max_valor=total_series)
        formato_fecha = _ventana_principal.formato_fecha

        for i, ruta in enumerate(self.rutas.series):
            altitud = np.nan

            lista_argumentos = [
                ruta, 
                self.variables, 
                filtros, 
                destino, 
                altitud,
                exportar_graficas,
                exportar_eliminados,
                formato_fecha
            ]

            analisis(*lista_argumentos)
            
            # Avanzamos la barra 1 paso por cada archivo completado
            _ventana_principal.barra_de_carga.avanzar(1)

        tiempo_final = time()
        tiempo_de_ejecucion = round(tiempo_final - tiempo_inicial, 2)

        _ventana_principal.barra_de_carga.finalizar()
        _ventana_principal.consola.escribir(f'---- Ejecución Finalizada en {tiempo_de_ejecucion} segundos -----')

        self.boton_examinar .habilitar()
        self.boton_variables.habilitar()
        self.boton_filtros  .habilitar()
        self.boton_ejecutar .habilitar()
        self.boton_ajustes  .habilitar()