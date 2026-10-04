import tkinter as tk

from Estilos.colores import *

from Elementos.boton_grafico import boton_grafico
from Elementos.espacio       import espacio
from Elementos.separador     import separador

import Modulos.Correccion_de_Series.sub_ventanas as sub

class Complementos(tk.Frame):
    def __init__(self, _contenedor, _ventana_principal):
        super().__init__(_contenedor)
        self.title = 'Complementos'
        self.config(bg = COLOR_PRINCIPAL, width = 600, height = 100)

        espacio(self)

        self.boton_examinar = boton_grafico(
            _contenedor   = self,
            _id           = 0,
            _imagen       = 'abrir',
            _texto        = 'Seleccionar\nSeries',
            _desabilitado = False,
            _funcion      = ...
        )

        separador(self)

        self.boton_variables = boton_grafico(
            _contenedor   = self,
            _id           = 1,
            _imagen       = 'graficar',
            _texto        = 'Graficar\nVariables',
            _funcion      = ...
        )

        self.boton_filtros = boton_grafico(
            _contenedor   = self,
            _id           = 2,
            _imagen       = 'fechas',
            _texto        = 'Separar\npor Fechas',
            _funcion      = ...
        )

        self.boton_ejecutar = boton_grafico(
            _contenedor   = self,
            _id           = 3,
            _imagen       = 'estadisticos',
            _texto        = 'Calcular\nEstadísticos',
            _funcion      = ...
        )
        
        separador(self)

        self.boton_ajustes = boton_grafico(
            _contenedor   = self,
            _id           = 4,
            _imagen       = 'ajustes',
            _texto        = 'Ajustes',
            _desabilitado = False,
            _funcion      = ...
        )

        espacio(self)

        self.pack()