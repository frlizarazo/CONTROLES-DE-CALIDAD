import tkinter as tk

from Estilos.tamaños import ancho_pequeño, alto_pequeño
from Estilos.colores import COLOR_PRINCIPAL

class espacio(tk.Frame):
    def __init__(
            self,
            _contenedor,
            _ancho      = ancho_pequeño,
            _alto       = alto_pequeño,
            _fondo      = COLOR_PRINCIPAL,
            _alineacion = 'left'
        ):

        super().__init__(_contenedor)

        self.config(
            bg     = _fondo,
            width  = _ancho, 
            height = _alto
        )

        self.pack(side = _alineacion)