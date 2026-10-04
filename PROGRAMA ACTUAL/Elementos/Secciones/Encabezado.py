import tkinter as tk

from Estilos.fuentes  import FUENTE_NEGRITA, FUENTE_PEQUEÑA
from Estilos.margenes import MARGEN_SOLO_HORIZONTAL, MARGEN_NORMAL
from Estilos.colores  import COLOR_FONDO, COLOR_FUENTE_SECUNDARIA
from Datos.textos     import DESCRIPCION

class Encabezado(tk.Frame):
    def __init__(self, parent, 
                 _texto        = 'CALIDAD SIMAC', 
                 _color_fondo  = COLOR_FONDO, 
                 _descripcion  = DESCRIPCION,
                 _color_fuente = COLOR_FUENTE_SECUNDARIA):
        
        super().__init__(parent)
        self.config(bg = _color_fondo)

        tk.Label(
            self,
            text = _texto,
            bg   = _color_fondo,
            fg   = _color_fuente,
            **FUENTE_NEGRITA
        ).pack()

        tk.Label(
            self, 
            text = _descripcion, 
            justify = 'left', 
            background = COLOR_FONDO,
            **FUENTE_PEQUEÑA
        ).pack()

        self.pack(**MARGEN_NORMAL)