import tkinter as tk
import base64
import io

from PIL import Image, ImageTk

from Estilos.colores  import COLOR_FONDO, COLOR_FUENTE_SECUNDARIA
from Estilos.fuentes  import FUENTE_NORMAL, FUENTE_NEGRITA
from Estilos.margenes import MARGEN_SOLO_HORIZONTAL, LEFT, MARGEN_VERTICAL
from Estilos.tamaños  import TAMAÑO_PEQUEÑO

from Elementos.boton_grafico import boton_grafico

from Funciones.cargar_ajustes import guardar_ajustes
from Funciones.cargar_icono   import cargar_icono

from Recursos.imagenes import imagenes

class boton_interruptor():
    def __init__(
            self, 
            _contenedor, 
            _ventana_principal, 
            _incluir_texto_1 = True,
            _incluir_texto_2 = True,
            _incluir_boton_2 = False,
            _texto_1         = 'opcion 1',
            _texto_2         = 'opcion 2',
            _color_de_fondo  = COLOR_FONDO,
            _color_de_texto  = COLOR_FUENTE_SECUNDARIA,
            _nombre_ajuste   = '', 
            _opciones_ajuste = ['opcion 1','opcion 2'],
            _row             = 0
        ):

        self.incluir_boton_2 = _incluir_boton_2

        self.estado_del_boton = (True 
                                 if getattr(
                                     _ventana_principal, _nombre_ajuste) == _opciones_ajuste[1] 
                                 else 
                                 False)

        imagen       = base64.b64decode(imagenes['interruptor1'])
        imagen       = Image.open(io.BytesIO(imagen))
        imagen       = imagen.resize((50, 50))
        self.apagado = ImageTk.PhotoImage(imagen)

        imagen       = base64.b64decode(imagenes['interruptor2'])
        imagen         = Image.open(io.BytesIO(imagen))
        imagen         = imagen.resize((50, 50))
        self.encendido = ImageTk.PhotoImage(imagen)

        imagen       = base64.b64decode(imagenes['mas'])
        imagen         = Image.open(io.BytesIO(imagen))
        imagen         = imagen.resize((25, 25))
        self.mas = ImageTk.PhotoImage(imagen)

        if _incluir_texto_1:
            self.texto_1 = tk.Label(
                _contenedor, 
                text               = _texto_1, 
                bg                 = _color_de_fondo, 
                fg                 = _color_de_texto,
                disabledforeground = '#f0f0f0',
                **FUENTE_NORMAL
            )
            self.texto_1.grid(row = _row, column = 0, **MARGEN_SOLO_HORIZONTAL)

        self.boton = tk.Button(
            _contenedor,
            image              = self.apagado,
            bg                 = COLOR_FONDO,
            activebackground   = COLOR_FONDO,
            relief             = 'sunken',
            borderwidth        = 0,
            highlightthickness = 0,
            command            = lambda : self.switch(
                                                _ventana_principal, 
                                                _nombre_ajuste,
                                                _opciones_ajuste
                                          )
        )
        self.boton.grid(row = _row, column = 1)

        if _incluir_texto_2:
            self.texto_2 = tk.Label(
                _contenedor, 
                text               = _texto_2, 
                bg                 = _color_de_fondo, 
                fg                 = _color_de_texto,
                disabledforeground = '#f0f0f0',
                **FUENTE_NORMAL
            )
            self.texto_2.grid(row = _row, column = 2, **MARGEN_SOLO_HORIZONTAL)
        
        if self.incluir_boton_2:
            self.boton2 = tk.Button(
                _contenedor,
                image              = self.mas,
                bg                 = COLOR_FONDO,
                activebackground   = COLOR_FONDO,
                borderwidth        = 0,
                highlightthickness = 0,
                command            = lambda: ventana_mas(_contenedor, _ventana_principal)
            )
            self.boton2.grid(row = _row, column = 3)

        self.switch(_ventana_principal, _nombre_ajuste, _opciones_ajuste)

    def switch(self, _ventana_principal, _nombre_ajuste, _opciones_ajustes):
        
        if self.estado_del_boton:
            self.boton.configure(image = self.encendido)
            ajuste = _opciones_ajustes[1]

            if self.incluir_boton_2: self.boton2.config(state = 'normal')

        else:
            self.boton.configure(image = self.apagado)
            ajuste = _opciones_ajustes[0]

            if self.incluir_boton_2: self.boton2.config(state = 'disabled')
        
        self.estado_del_boton = not self.estado_del_boton
        
        guardar_ajustes(ajuste, _nombre_ajuste)
        _ventana_principal.cargar_ajustes()

class ventana_mas(tk.Toplevel):
    def __init__(self, _ventana_madre, _ventana_principal):
        super().__init__(_ventana_madre)
        self.config(bg = COLOR_FONDO)
        self.title('Patron de selección')
        _ventana_principal.cargar_ajustes()
        cargar_icono(self)
        self.grab_set()

        tk.Label(
            self, 
            text               = 'Patron de selección:', 
            bg                 = COLOR_FONDO, 
            fg                 = COLOR_FUENTE_SECUNDARIA,
            **FUENTE_NEGRITA
        ).pack(**LEFT, **MARGEN_VERTICAL)

        self.patron = tk.Entry(
            self,
            width = 10
        )
        self.patron.pack(**LEFT, **MARGEN_VERTICAL)

        self.patron.insert(0, _ventana_principal.patron_de_seleccion)

        tk.Label(
            self, 
            text               = '.csv', 
            bg                 = COLOR_FONDO, 
            fg                 = COLOR_FUENTE_SECUNDARIA,
            **FUENTE_NORMAL
        ).pack(**LEFT, **MARGEN_VERTICAL)

        boton_grafico(
            _contenedor     = self,
            _imagen         = 'guardar',
            _incluir_texto  = False,
            _desabilitado   = False,
            _alineacion     = 'left',
            _color_de_fondo = COLOR_FONDO,
            _color_de_texto = COLOR_FUENTE_SECUNDARIA,
            _funcion        = lambda: self.guardar(self.patron.get()),
            **TAMAÑO_PEQUEÑO
        )
    
    def guardar(self, _valor):
        guardar_ajustes(_valor, configuracion = 'patron_de_seleccion')
        self.destroy()