import tkinter as tk
import Correciones as c

from Estilos.colores  import *
from Estilos.margenes import MARGEN_ESTRECHA
from Funciones.cargar_icono import cargar_icono

class ToolTip:
    """Clase auxiliar para mostrar información flotante (tooltip) al pasar el cursor."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(400, self.show_tip) # Retraso de 400ms antes de mostrar

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 2
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, 
            text=self.text, 
            justify=tk.LEFT,
            background="#ffffe0", 
            fg="#000000",
            relief=tk.SOLID, 
            borderwidth=1,
            font=("Arial", 9)
        )
        label.pack(ipadx=3, ipady=2)

    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class Filtros(tk.Toplevel):
    # Diccionario de clase para recordar estados y la última ruta de archivo por módulo
    _estado_memoria = {}
    _ultimo_archivo_memoria = {}

    def __init__(self, _modulo, _ventana_principal):
        super().__init__(_ventana_principal)

        self.window = _ventana_principal

        self.title('Seleccione los filtros a aplicar')
        self.config(bg = COLOR_FONDO)
        cargar_icono(self)
        self.grab_set()

        self.geometry("450x450")
        self.resizable(True, True)

        self.modulo = _modulo
        self.variables = self.modulo.variables

        # Detectar si se ha cargado un archivo nuevo para limpiar el estado guardado
        archivo_actual = getattr(self.modulo, 'archivo', None)
        ruta_actual = getattr(archivo_actual, 'ruta', str(archivo_actual)) if archivo_actual else None
        
        modulo_id = id(self.modulo)
        archivo_previo = Filtros._ultimo_archivo_memoria.get(modulo_id)

        if archivo_previo != ruta_actual:
            # Archivo nuevo detectado: limpiamos memoria de este módulo
            Filtros._estado_memoria.pop(modulo_id, None)
            Filtros._ultimo_archivo_memoria[modulo_id] = ruta_actual

        # Inicializar variables IntVar para cada filtro
        self.variables_filtros = [tk.IntVar() for _ in range(len(c.FILTROS))]

        # Restaurar estado anterior si existe en memoria, de lo contrario aplicar por defecto (.obligatorio)
        estado_guardado = Filtros._estado_memoria.get(modulo_id)
        
        for i, filtro in enumerate(c.FILTROS):
            es_obligatorio = getattr(filtro, 'obligatorio', False)
            if es_obligatorio:
                self.variables_filtros[i].set(1)
            elif estado_guardado and i < len(estado_guardado):
                self.variables_filtros[i].set(estado_guardado[i])
            else:
                self.variables_filtros[i].set(0)

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

        # --- CREACIÓN DE CHECKBUTTONS SEGÚN VISIBILIDAD ---
        self.todas_las_opciones = []
        for i, filtro in enumerate(c.FILTROS):
            visible = getattr(filtro, 'visible', True)
            
            if visible:
                chk = tk.Checkbutton(
                    self.scrollable_frame, 
                    variable = self.variables_filtros[i],
                    text     = getattr(filtro, 'nombre', f'Filtro {i}'),
                    bg       = COLOR_FONDO,
                    activebackground = COLOR_FONDO,
                    command  = self.actualizar_estado_filtros
                )
                chk.pack(anchor = 'w', **MARGEN_ESTRECHA)
                
                # Añadir tooltip si el filtro tiene el atributo .descripcion
                descripcion = getattr(filtro, 'descripcion', None)
                if descripcion:
                    ToolTip(chk, descripcion)

                self.todas_las_opciones.append((chk, self.variables_filtros[i], i))
            else:
                # Si no es visible, se registra sin widget visual pero con su variable controlada
                self.todas_las_opciones.append((None, self.variables_filtros[i], i))

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

        # Aplicar estados iniciales y dependencias
        self.actualizar_estado_filtros()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def actualizar_estado_filtros(self):
        filtros_activos_nombres = {
            getattr(c.FILTROS[j], 'nombre'): (self.variables_filtros[j].get() == 1)
            for j in range(len(c.FILTROS))
        }

        for chk, var, i in self.todas_las_opciones:
            filtro = c.FILTROS[i]
            es_obligatorio = getattr(filtro, 'obligatorio', False)
            
            # 1. Validar variables requeridas por el filtro
            variables_requeridas = getattr(filtro, 'variables', [])
            compatible = not any(req not in list(self.variables.values()) for req in variables_requeridas)

            # 2. Validar dependencia (.depende) soportando texto plano o lista/tupla de dependencias
            dependencia_cumplida = True
            depende_de = getattr(filtro, 'depende', None)
            if depende_de:
                if isinstance(depende_de, (list, tuple)):
                    dependencia_cumplida = all(filtros_activos_nombres.get(d, False) for d in depende_de)
                else:
                    dependencia_cumplida = filtros_activos_nombres.get(depende_de, False)

            if es_obligatorio:
                var.set(1)
                if chk:
                    chk.config(state='disabled') # Obligatorio: marcado y no seleccionable por el usuario
            else:
                if compatible and dependencia_cumplida:
                    if chk:
                        chk.config(state='normal')
                else:
                    if chk:
                        chk.config(state='disabled')
                    var.set(0)

    def seleccionar_todo(self):
        # Bucle iterativo para asegurar que los filtros dependientes en cadena se habiliten y seleccionen correctamente
        cambios = True
        while cambios:
            cambios = False
            self.actualizar_estado_filtros()
            
            for chk, var, i in self.todas_las_opciones:
                filtro = c.FILTROS[i]
                es_obligatorio = getattr(filtro, 'obligatorio', False)
                if not es_obligatorio and chk and str(chk.cget("state")) == 'normal' and var.get() == 0:
                    var.set(1)
                    cambios = True
                    
        self.actualizar_estado_filtros()

    def limpiar_seleccion(self):
        for chk, var, i in self.todas_las_opciones:
            filtro = c.FILTROS[i]
            es_obligatorio = getattr(filtro, 'obligatorio', False)
            if not es_obligatorio:
                var.set(0)
        
        self.actualizar_estado_filtros()

    def listo_filtros(self):
        self.canvas.unbind_all("<MouseWheel>")
        
        # Guardar estado actual en memoria antes de cerrar
        modulo_id = id(self.modulo)
        Filtros._estado_memoria[modulo_id] = [v.get() for v in self.variables_filtros]

        self.modulo.filtros = [filtro for i, filtro in enumerate(c.FILTROS) if self.variables_filtros[i].get() == 1]
        
        # Mensaje impreso por consola con la cantidad de filtros seleccionados
        self.window.consola.escribir(f"Se han seleccionado, {len(self.modulo.filtros)} filtros....")

        self.destroy()
        self.modulo.boton_ejecutar.habilitar()