import tkinter as tk
from tkinter import ttk
from unidecode import unidecode

from tkinter.messagebox import showerror

from Estilos.colores import *
from Estilos.margenes import *
from Estilos.fuentes import FUENTE_NEGRITA

from Funciones.cargar_icono import cargar_icono
from Elementos.Secciones.Encabezado import Encabezado
from Datos.columnas import NOMBRES_DE_COLUMNAS

class Variables(tk.Toplevel):
    def __init__(self, _modulo, _ventana_principal):
        super().__init__(_ventana_principal)
        self.title('Seleccione las variables de las series')
        self.config(bg = COLOR_FONDO)
        cargar_icono(self)
        self.grab_set()

        # Fijamos el tamaño de la ventana y evitamos que se redimensione
        self.geometry("550x550")
        self.resizable(True, True)

        self.modulo = _modulo

        self.leer_encabezados()

        # Encabezado superior fijo
        Encabezado(self, 'Variables', _descripcion = '''Debido a la gran variedad de nombres que puede recibir una misma
variable, a continuación se muestran las variables detectadas en
los archivos leídos y se pide que se seleccione para cada una a
que tipo de dato corresponde.''')

        # --- BOTONES FIJOS EN LA PARTE INFERIOR ---
        botones = tk.Frame(self, bg = COLOR_FONDO)
        botones.pack(side = 'bottom', fill = 'x', padx = 5, pady = 5)

        tk.Button(
            botones, 
            text    = 'Seleccionar todo',
            command = self.seleccionar_todo,
            bg      = COLOR_PRINCIPAL,
            fg      = COLOR_FUENTE_PRINCIPAL,
            relief  = 'flat'
        ).grid(row = 0, column = 0, sticky = 'ew', **MARGEN_ESTRECHA)
        
        tk.Button(
            botones, 
            text    = 'Limpiar',
            command = self.limpiar_seleccion,
            bg      = COLOR_PRINCIPAL,
            fg      = COLOR_FUENTE_PRINCIPAL,
            relief  = 'flat'
        ).grid(row = 0, column = 1, sticky = 'ew', **MARGEN_ESTRECHA)

        tk.Button(
            botones, 
            text    = 'Listo',
            command = self.listo_columnas,
            bg      = COLOR_SECUNDARIO,
            fg      = COLOR_FUENTE_SECUNDARIA,
            relief  = 'flat'
        ).grid(row = 0, column = 2, columnspan = 2, sticky = 'ew', **MARGEN_ESTRECHA)

        botones.grid_columnconfigure(0, weight=1)
        botones.grid_columnconfigure(1, weight=1)
        botones.grid_columnconfigure(2, weight=1)

        # --- CONTENEDOR PRINCIPAL CON SCROLL ---
        container = tk.Frame(self, bg=COLOR_FONDO)
        container.pack(fill='both', expand=True, padx=10, pady=5)

        # Títulos de las columnas usando grid para alinear perfectamente con las filas
        frame_titulos = tk.Frame(container, bg = COLOR_FONDO)
        frame_titulos.pack(fill = 'x', side = 'top', pady=(0, 5))
        
        tk.Label(frame_titulos, text = 'Variables leídas', font = FUENTE_NEGRITA, bg = COLOR_FONDO).grid(row = 0, column = 0, sticky = 'w', padx=5)
        tk.Label(frame_titulos, text = 'Tipo de variable', font = FUENTE_NEGRITA, bg = COLOR_FONDO).grid(row = 0, column = 1, sticky = 'e', padx=5)
        
        frame_titulos.grid_columnconfigure(0, weight=1)
        frame_titulos.grid_columnconfigure(1, weight=0)

        # Sub-contenedor para canvas y scrollbar
        canvas_container = tk.Frame(container, bg=COLOR_FONDO)
        canvas_container.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(canvas_container, bg=COLOR_FONDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLOR_FONDO)

        # Ventana dentro del canvas y ajuste automático de ancho
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Forzar que el frame interno ocupe todo el ancho del canvas
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Habilitar scroll con la rueda del ratón
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.variables_columnas = [tk.IntVar() for i in range(len(self.encabezados))]

        self.opciones = []
        self.tipos    = []

        for i, variable in enumerate(self.variables_columnas):
            row_frame = tk.Frame(self.scrollable_frame, bg = COLOR_FONDO)
            row_frame.pack(expand=True, fill='x', pady=2)

            opc = tk.Checkbutton(
                row_frame, 
                text     = self.encabezados[i],
                variable = variable,
                bg       = COLOR_FONDO,
                activebackground = COLOR_FONDO
            )
            opc.grid(row = 0, column = 0, sticky = 'w', **MARGEN_ESTRECHA)
            self.opciones.append(opc)

            tipo_cb = ttk.Combobox(row_frame, values=['Fecha', 'Hora'] + NOMBRES_DE_COLUMNAS, width=25)
            tipo_cb.grid(row = 0, column = 1, sticky = 'e', **MARGEN_ESTRECHA)
            
            # Detectar cambios en el combobox para bloquear/desbloquear el checkbutton
            tipo_cb.bind("<<ComboboxSelected>>", lambda event, idx=i: self.actualizar_estado_check(idx))
            
            self.tipos.append(tipo_cb)

            row_frame.grid_columnconfigure(0, weight=1)
            row_frame.grid_columnconfigure(1, weight=0)

            encabezado = unidecode(self.encabezados[i].lower())
            self.tipos_por_defecto(encabezado, tipo_cb)
            
            # Evaluar estado inicial por defecto
            self.actualizar_estado_check(i)

        [variable.set(1) for variable in self.variables_columnas]

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def saltos_y_separador(self, ruta):
        with open(ruta, 'r', encoding='utf-8') as file:
            for saltos, lina in enumerate(file):
                pcoma = lina.count(';')
                coma  = lina.count(',')

                separador = ',' if coma > pcoma else ';' if pcoma > 0 else False
                
                if separador:
                    break

        return saltos, separador

    def leer_encabezados(self):
        encabezados = []

        for ruta in self.modulo.rutas.rutas:
            saltos, separador = self.saltos_y_separador(ruta)
            
            if not separador:
                showerror(
                    parent  = self,
                    title   = 'Error de formato',
                    message = f'No se pudo detectar un separador válido en el archivo:\n{ruta}'
                )
                self.destroy()
                return

            with open(ruta, 'r', encoding='utf-8') as r:
                lineas = r.readlines()
                encabezados.append(lineas[saltos].split(separador))

        encabezados  = [
            [encabezado.strip() for encabezado in encabezados0] 
            for encabezados0 in encabezados
        ]

        encabezados_para_chequeo = set([','.join(encabezado) for encabezado in encabezados])

        if len(encabezados_para_chequeo) > 1:
            showerror(
                parent  = self, 
                title   = 'Revisar los encabezados', 
                message = 'Una o más series presentan encabezados diferentes\n{}'.format(
                    encabezados_para_chequeo
                )
            )
            self.destroy()

        self.encabezados = encabezados[0]

    def actualizar_estado_check(self, index):
        tipo_seleccionado = self.tipos[index].get()
        if tipo_seleccionado in ['Fecha', 'Hora']:
            self.variables_columnas[index].set(1)  # Forzar a seleccionado
            self.opciones[index].config(state='disabled')  # Bloquear checkbutton
        else:
            self.opciones[index].config(state='normal')  # Desbloquear checkbutton

    def seleccionar_todo(self):
        for variable in self.variables_columnas:
            variable.set(1)

    def limpiar_seleccion(self):
        for i, variable in enumerate(self.variables_columnas):
            tipo_seleccionado = self.tipos[i].get()
            # No desmarcar si es Fecha u Hora
            if tipo_seleccionado not in ['Fecha', 'Hora']:
                variable.set(0)

    def listo_columnas(self):
        tipos = [tipo.get() for tipo in self.tipos]

        if ('Fecha' in tipos) and ('Hora' in tipos):
            self.canvas.unbind_all("<MouseWheel>") # Limpiar evento global al cerrar
            self.modulo.boton_filtros.habilitar()
            self.modulo.variables = {
                variable : tipo 
                for i, (variable, tipo) in 
                enumerate(zip(self.encabezados, tipos))
                if self.variables_columnas[i].get() == 1
            }
            self.destroy()
        else:
            showerror(
                parent  = self,
                title   = 'Error de fecha y hora',
                message = 'Tienen que haber datos del tipo fecha y hora'
            )

    def tipos_por_defecto(self, encabezado, tipo):
        if 'fecha' in encabezado:
            tipo.set('Fecha')
        elif 'hora' in encabezado:
            tipo.set('Hora')
        elif 'temperatura' in encabezado:
            if 'agua' in encabezado:
                tipo.set('Temperatura del Agua')
            else:
                tipo.set('Temperatura')
        elif 'viento' in encabezado:
            if 'vel' in encabezado:
                tipo.set('Velocidad del Viento')
            else:
                tipo.set('Dirección del Viento')
        elif 'rosa' in encabezado:
            tipo.set('Dirección de la Rosa')
        elif 'presion' in encabezado:
            tipo.set('Presión Barométrica')
        elif 'humedad' in encabezado:
            tipo.set('Humedad Relativa')
        elif 'precipitacion' in encabezado:
            if 'acum' in encabezado:
                tipo.set('Precipitación Acumulada')
            else:
                tipo.set('Precipitación')
        elif 'radiacion' in encabezado:
            tipo.set('Radiación Solar')
        elif any(term in encabezado for term in ['evapotranspiracion', 'evt', 'e.t.']):
            if 'acum' in encabezado:
                tipo.set('Evapotranspiración Acumulada')
            else:
                tipo.set('Evapotranspiración')
        elif 'nivel' in encabezado:
            tipo.set('Nivel')
        elif 'observacion' in encabezado:
            tipo.set('Observaciones')
        else:
            tipo.set('--')