import tkinter as tk
from tkinter import ttk

from Modulos.Correccion_de_Series.Correccion_de_Series import Correccion_Series
from Modulos.Complementos.Complementos                 import Complementos

from Estilos.margenes import MARGEN_NORMAL

class Barra_de_Herramientas(ttk.Notebook):
    def __init__(self, _ventana_principal):
        super().__init__(_ventana_principal)
        self.ventana_principal = _ventana_principal

        self.insertar_modulo(Correccion_Series)
        self.insertar_modulo(Complementos)

        self.hide(1)

        self.pack(**MARGEN_NORMAL)
    
    def insertar_modulo(self, Tab):

        Tab = Tab(self, self.ventana_principal)
        self.add(Tab, text = Tab.title)

    def quitar_enfoque(self, event = None):
        event.widget.master.focus_set()
    
    def vincular_funciones(self):
        self.bind('<<NotebookTabChanged>>', self.quitar_enfoque)