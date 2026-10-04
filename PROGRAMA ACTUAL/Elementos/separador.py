from tkinter import ttk

from Estilos.margenes import MARGEN_VERTICAL, EXPANDIR_VERTICAL, LEFT, TOP

class separador(ttk.Separator):
    def __init__(
            self, 
            _contenedor,
            _orientacion = 'vertical'
        ):
        super().__init__(_contenedor)

        self.config(
            orient = _orientacion
        )

        alineacion = LEFT if _orientacion == 'vertical' else TOP

        self.pack(
            **alineacion,
            **EXPANDIR_VERTICAL,
            **MARGEN_VERTICAL
        )