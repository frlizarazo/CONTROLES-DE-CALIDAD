from tkinter import ttk
from Estilos.margenes import EXPANDIR_HORIZONTAL, MARGEN_NORMAL
from Estilos.colores import COLOR_CLARO

class barra_de_carga(ttk.Progressbar):
    def __init__(self, _contenedor):
        super().__init__(_contenedor)
        self.config(
            orient  = 'horizontal',
            length  = 200,
            maximum = 100,
            mode    = 'determinate'
        )
        self.style_name = f"Custom.Horizontal.TProgressbar_{id(self)}"
        style = ttk.Style()
        style.configure(
            self.style_name,
            background='#eb6828',         # Relleno sólido naranja
            troughcolor=COLOR_CLARO,      # Color de fondo del canal
            borderwidth=0,                # Sin bordes
            relief='flat'
        )

    def iniciar(self, max_valor=100):
        # Forzamos la ejecución en el hilo principal de Tkinter
        self.after(0, lambda: self._iniciar_ui(max_valor))

    def _iniciar_ui(self, max_valor):
        self['value'] = 0
        self['maximum'] = max_valor
        self.pack(**MARGEN_NORMAL, **EXPANDIR_HORIZONTAL)
        self.update_idletasks()
    
    def avanzar(self, paso=1):
        self.after(0, lambda: self._avanzar_ui(paso))

    def _avanzar_ui(self, paso):
        self['value'] += paso
        self.update_idletasks()
    
    def finalizar(self):
        self.after(0, self._finalizar_ui)

    def _finalizar_ui(self):
        self['value'] = self['maximum']
        self.update_idletasks()
        self.pack_forget()