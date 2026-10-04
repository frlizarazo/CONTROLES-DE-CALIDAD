import tkinter as tk

import Correciones as c

from Estilos.colores  import *
from Estilos.margenes import MARGEN_ESTRECHA

from Funciones.cargar_icono import cargar_icono

class Filtros(tk.Toplevel):
    def __init__(self,  _modulo, _ventana_principal):
        super().__init__(_ventana_principal)

        self.title('Seleccione los filtros a aplicar')
        self.config(bg = COLOR_FONDO)
        cargar_icono(self)
        self.grab_set()

        self.geometry("450x450")
        self.resizable(True, True)

        self.modulo   = _modulo
        self.variables = self.modulo.variables

        self.variables_filtros = [tk.IntVar() for i in range(len(c.FILTROS))]
        
        INDICE_HOMOGENIZACION = 10
        if len(c.FILTROS) > INDICE_HOMOGENIZACION:
            self.variables_filtros[INDICE_HOMOGENIZACION].set(1) # Activa por defecto si se desea

        # --- CONTENEDOR CON SCROLL ---
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill='both', expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(container, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_FONDO)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- CREACIÓN DE TODOS LOS CHECKBUTTONS EN ORDEN ---
        self.todas_las_opciones = []
        for i in range(len(c.FILTROS)):
            cmd = self.actualizar_estado_filtros if i == INDICE_HOMOGENIZACION else None
            
            chk = tk.Checkbutton(
                self.scrollable_frame, 
                variable = self.variables_filtros[i],
                text     = c.FILTROS[i].nombre,
                bg       = COLOR_FONDO,
                activebackground = COLOR_FONDO,
                command  = cmd
            )
            chk.pack(anchor = 'w', **MARGEN_ESTRECHA)
            self.todas_las_opciones.append((chk, self.variables_filtros[i], i))

        # --- BOTONES FIJOS EN LA PARTE INFERIOR ---
        botones = tk.Frame(self, bg = COLOR_FONDO)
        botones.pack(side='bottom', fill='x', padx=5, pady=5)

        boton_selec_todo = tk.Button(
            botones, 
            text    = 'Seleccionar todo',
            command = self.seleccionar_todo,
            bg      = COLOR_PRINCIPAL,
            fg      = COLOR_FUENTE_PRINCIPAL,
            relief  = 'flat'
        )
        boton_selec_todo.grid(row = 0, column = 0, sticky = 'ew', **MARGEN_ESTRECHA)
        
        boton_limpiar = tk.Button(
            botones, 
            text    = 'Limpiar', 
            command = self.limpiar_seleccion,
            bg      = COLOR_PRINCIPAL,
            fg      = COLOR_FUENTE_PRINCIPAL,
            relief  = 'flat'
        )
        boton_limpiar.grid(row = 0, column = 1, sticky = 'ew', **MARGEN_ESTRECHA)
        
        boton_listo = tk.Button(
            botones, 
            text    = 'Listo',
            command = self.listo_filtros,
            bg      = COLOR_SECUNDARIO,
            fg      = COLOR_FUENTE_SECUNDARIA,
            relief  = 'flat'
        )
        boton_listo.grid(row = 0, column = 2, sticky = 'ew', columnspan=2, **MARGEN_ESTRECHA)

        botones.grid_columnconfigure(0, weight=1)
        botones.grid_columnconfigure(1, weight=1)
        botones.grid_columnconfigure(2, weight=1)

        # Aplicar estados iniciales correctos
        self.actualizar_estado_filtros()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def actualizar_estado_filtros(self):
        INDICE_HOMOGENIZACION = 10
        homo_activo = False
        if len(c.FILTROS) > INDICE_HOMOGENIZACION:
            homo_activo = self.variables_filtros[INDICE_HOMOGENIZACION].get() == 1
        
        for chk, var, i in self.todas_las_opciones:
            compatible = not any(var_req not in list(self.variables.values()) for var_req in c.FILTROS[i].variables)
            
            if i < INDICE_HOMOGENIZACION:
                if compatible:
                    chk.config(state='normal')
                else:
                    chk.config(state='disabled')
                    var.set(0)
                    
            elif i == INDICE_HOMOGENIZACION:
                if compatible:
                    chk.config(state='normal')
                else:
                    chk.config(state='disabled')
                    var.set(0)
                    
            else:
                if homo_activo and compatible:
                    chk.config(state='normal')
                else:
                    chk.config(state='disabled')
                    var.set(0)

    def seleccionar_todo(self):
        INDICE_HOMOGENIZACION = 10
        
        # Si homogeneización es compatible, la marcamos primero para que los posteriores puedan habilitarse
        if len(c.FILTROS) > INDICE_HOMOGENIZACION:
            compat_homo = not any(var_req not in list(self.variables.values()) for var_req in c.FILTROS[INDICE_HOMOGENIZACION].variables)
            if compat_homo:
                self.variables_filtros[INDICE_HOMOGENIZACION].set(1)

        # Actualizamos estados para habilitar los filtros posteriores en base a la homogeneización activa
        self.actualizar_estado_filtros()

        # Marcamos todos los que hayan quedado habilitados (en estado 'normal')
        for chk, var, i in self.todas_las_opciones:
            if str(chk.cget("state")) == 'normal':
                var.set(1)

    def limpiar_seleccion(self):
        # Desmarcamos todas las variables
        for chk, var, i in self.todas_las_opciones:
            var.set(0)
        
        # Forzamos la actualización para que se deshabiliten y limpien los posteriores al apagarse la homogeneización
        self.actualizar_estado_filtros()

    def listo_filtros(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.modulo.filtros = [filtro for i, filtro in enumerate(c.FILTROS) if self.variables_filtros[i].get() == 1]
        self.destroy()
        self.modulo.boton_ejecutar.habilitar()