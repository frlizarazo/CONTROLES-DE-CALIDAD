import tkinter as tk
import tkinter.ttk as ttk

from os import getcwd
from multiprocessing import cpu_count
from tkinter.filedialog import askdirectory

from Estilos.colores  import *
from Estilos.margenes import MARGEN_SOLO_HORIZONTAL, LEFT
from Estilos.tamaños  import TAMAÑO_PEQUEÑO
from Estilos.fuentes  import FUENTE_NEGRITA

from Datos.textos import NOMBRE_DEL_PROGRAMA, DESCRIPCION

from Funciones.cargar_icono    import cargar_icono
from Funciones.cargar_ajustes import guardar_ajustes

from Elementos.boton_interruptor import boton_interruptor
from Elementos.boton_grafico     import boton_grafico
from Elementos.espacio           import espacio

class Ajustes(tk.Toplevel):
    def __init__(self, _ventana_principal):
        super().__init__(_ventana_principal)
        self.title('Ajustes del Módulo de Correcciones')
        self.config(bg = COLOR_FONDO)
        cargar_icono(self)
        self.grab_set()

        self.ventana_principal = _ventana_principal

        tk.Label(self, text = NOMBRE_DEL_PROGRAMA, font = ('courier',5), justify = 'left', background = COLOR_FONDO).pack(**MARGEN_SOLO_HORIZONTAL)

        contenedor0 = tk.Frame(self, bg = COLOR_FONDO)
        contenedor0.pack()

        ruta = _ventana_principal.directorio_inicial.split('/')
        directorio_inicial_acortado = ruta[0] + '/.../' + ruta[-1]

        self.directorio_inicial = boton_grafico(
            _contenedor      = contenedor0,
            _id              = 0,
            _imagen          = 'abrir',
            _texto           = directorio_inicial_acortado,
            _desabilitado    = False,
            _texto_variable = True,
            _alineacion      = 'left',
            _sub_alineacion = 'right',
            _incluir_titulo = True,
            _titulo          = 'Ruta por Defecto: ',
            _color_de_fondo = COLOR_FONDO,
            _color_de_texto = COLOR_FUENTE_SECUNDARIA,
            _funcion         = lambda: self.seleccionar_directorio(_ventana_principal, 'directorio_inicial'),
            **TAMAÑO_PEQUEÑO
        )

        ruta = _ventana_principal.directorio_de_salida.split('/')
        directorio_salida_acortado = ruta[0] + '/.../' + ruta[-1]

        self.directorio_de_salida = boton_grafico(
            _contenedor      = contenedor0,
            _id              = 0,
            _imagen          = 'abrir',
            _texto           = directorio_salida_acortado,
            _desabilitado    = False,
            _texto_variable = True,
            _alineacion      = 'left',
            _sub_alineacion = 'right',
            _incluir_titulo = True,
            _titulo          = 'Ruta de Salida: ',
            _color_de_fondo = COLOR_FONDO,
            _color_de_texto = COLOR_FUENTE_SECUNDARIA,
            _funcion         = lambda: self.seleccionar_directorio(_ventana_principal, 'directorio_de_salida'),
            **TAMAÑO_PEQUEÑO
        )

        contenedor1 = tk.Frame(self, bg = COLOR_FONDO)
        contenedor1.pack()

        boton_interruptor(
            contenedor1,
            _ventana_principal = _ventana_principal,
            _texto_1           = 'Seleccionar por Archivo',
            _texto_2           = 'Seleccionar por Carpeta',
            _incluir_boton_2   = True,
            _nombre_ajuste     = 'protocolo_de_seleccion',
            _opciones_ajuste   = ['por archivos', 'por carpeta'],
            _row               = 0,
        )

        boton_interruptor(
            contenedor1,
            _ventana_principal = _ventana_principal,
            _texto_1           = 'Exportar Eliminados',
            _incluir_texto_2   = False,
            _nombre_ajuste     = 'exportar_eliminados',
            _opciones_ajuste   = ['no', 'si'],
            _row               = 1,
        )
        boton_interruptor(
            contenedor1,
            _ventana_principal = _ventana_principal,
            _texto_1           = 'Exportar Graficas',
            _incluir_texto_2   = False,
            _nombre_ajuste     = 'exportar_graficas',
            _opciones_ajuste   = ['no', 'si'],
            _row               = 2,
        )

        espacio(self, _fondo = COLOR_FONDO, _alineacion = 'top')

        contenedor2 = tk.Frame(self, bg = COLOR_FONDO)
        contenedor2.pack()

        tk.Label(
            contenedor2, 
            text               = 'Resolución de los datos: ', 
            bg                 = COLOR_FONDO, 
            fg                 = COLOR_FUENTE_SECUNDARIA, 
            disabledforeground = '#f0f0f0',
            **FUENTE_NEGRITA
        ).pack(LEFT, **MARGEN_SOLO_HORIZONTAL)

        self.spinbox = ttk.Spinbox(
            contenedor2, 
            from_      = 0, 
            to         = 1440, 
            increment = 5, 
            width      = 8, 
            format     = "%.0f min",
            command    = self.seleccionar_resolucion
        )
        self.spinbox.pack(LEFT)

        self.spinbox.insert(0, f'{self.ventana_principal.resolucion} min')

        espacio(self, _fondo = COLOR_FONDO, _alineacion = 'top')

        # --- NUEVO CONTENEDOR PARA FORMATO DE FECHA ---
        contenedor3 = tk.Frame(self, bg = COLOR_FONDO)
        contenedor3.pack()

        tk.Label(
            contenedor3, 
            text               = 'Formato de Fecha: ', 
            bg                 = COLOR_FONDO, 
            fg                 = COLOR_FUENTE_SECUNDARIA, 
            disabledforeground = '#f0f0f0',
            **FUENTE_NEGRITA
        ).pack(LEFT, **MARGEN_SOLO_HORIZONTAL)

        # Usamos un Combobox para permitir elegir o escribir formatos comunes de fecha/hora (strptime)
        formatos_disponibles = [
            '%d/%m/%Y %H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y %H:%M',
            '%Y/%m/%d %H:%M',
            '%d/%m/%Y',
            '%Y-%m-%d'
        ]

        self.combo_fecha = ttk.Combobox(
            contenedor3,
            values = formatos_disponibles,
            width  = 22
        )
        self.combo_fecha.pack(LEFT)
        self.combo_fecha.set(getattr(self.ventana_principal, 'formato_fecha', '%d/%m/%Y %H:%M:%S'))

        # Guardar cambios al seleccionar o presionar enter / salir del foco
        self.combo_fecha.bind("<<ComboboxSelected>>", self.seleccionar_formato_fecha)
        self.combo_fecha.bind("<Return>", self.seleccionar_formato_fecha)
        self.combo_fecha.bind("<FocusOut>", self.seleccionar_formato_fecha)

        espacio(self, _fondo = COLOR_FONDO, _alineacion = 'top')

        self.spinbox.bind("<Return>",           self.seleccionar_resolucion)
        self.spinbox.bind("<FocusOut>",         self.seleccionar_resolucion)
        self.spinbox.bind("<KeyRelease>",       self.seleccionar_resolucion)
    
    def seleccionar_resolucion(self, evento = None):
        guardar_ajustes(valor = self.spinbox.get().replace(' min', ''), configuracion = 'resolucion')
    
    def seleccionar_formato_fecha(self, evento = None):
        guardar_ajustes(valor = self.combo_fecha.get(), configuracion = 'formato_fecha')
        if hasattr(self.ventana_principal, 'cargar_ajustes'):
            self.ventana_principal.cargar_ajustes()

    def seleccionar_directorio(self, _ventana_principal, _ajuste):

        directorio_inicial = getattr(_ventana_principal, _ajuste)

        dir = askdirectory(
                parent     = self,
                initialdir = directorio_inicial, 
                title      = 'Selecciona el directorio'
            )
        
        guardar_ajustes(valor = dir, configuracion = _ajuste)
        _ventana_principal.cargar_ajustes()

        dir = dir if len(dir) > 0 else getcwd().replace('\\','/')
        dir = dir.split('/')
        dir = dir[0] + '/.../' + dir[-1]

        getattr(self, _ajuste).texto_variable.set(dir)