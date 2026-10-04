import tkinter as tk

from Estilos.margenes import MARGEN_NORMAL, EXPANDIR_HORIZONTAL
from Estilos.fuentes  import FUENTE_PEQUEÑA
from Estilos.colores  import COLOR_CLARO, COLOR_OSCURO

class Consola(tk.Text):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(
            bg          = COLOR_CLARO,
            fg          = COLOR_OSCURO,
            height      = 10, 
            width       = 66,
            borderwidth = 0,
            **FUENTE_PEQUEÑA
        )

        self.pack(**MARGEN_NORMAL)
    
    def escribir(self, text):
        self.insert('end', ' >>>   ' + text + '\n')
        self.see('end')