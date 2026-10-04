import tkinter as tk
import io
import base64

from PIL import Image, ImageTk

from Estilos.colores  import COLOR_PRINCIPAL, COLOR_FUENTE_PRINCIPAL
from Estilos.fuentes  import FUENTE_PEQUEÑA, FUENTE_NEGRITA
from Estilos.margenes import MARGEN_VERTICAL

from Estilos.tamaños  import alto_normal, ancho_normal

from Recursos.imagenes import imagenes


class boton_grafico(tk.Frame):
    def __init__(
            self, 
            _contenedor, 
            _id                = 0, 
            _alto              = alto_normal, 
            _ancho             = ancho_normal, 
            _imagen            = 'Recursos/sin_imagen.png', 
            _texto             = 'sin texto',
            _titulo            = 'sin texto',
            _alineacion        = 'left',
            _sub_alineacion    = 'top',
            _alineacion_titulo = 'left',
            _incluir_texto     = True,
            _incluir_titulo    = False,
            _texto_variable    = False,
            _desabilitado      = True,
            _funcion           = None, 
            _color_de_fondo    = COLOR_PRINCIPAL,
            _color_de_texto    = COLOR_FUENTE_PRINCIPAL,
            _fuente            = FUENTE_PEQUEÑA,
            _fuente_negrita    = FUENTE_NEGRITA,
            _margen            = MARGEN_VERTICAL
        ):
        
        super().__init__(_contenedor)
        self.config(bg = _color_de_fondo)

        self.incluir_texto = _incluir_texto

        imagen = imagenes[_imagen]
        imagen = base64.b64decode(imagen)
        imagen = Image.open(io.BytesIO(imagen))
        imagen = imagen.resize((_ancho,_alto))

        setattr(self, f'icono_{_id}', ImageTk.PhotoImage(imagen))

        if _incluir_titulo:

            self.titulo = tk.Label(
                self, 
                text               = _titulo, 
                bg                 = _color_de_fondo, 
                fg                 = _color_de_texto,
                disabledforeground = '#f0f0f0',
                **_fuente_negrita
            )
            self.titulo.pack(side = _alineacion_titulo)

        self.boton = tk.Button(
            self, 
            image              = getattr(self, f'icono_{_id}'), 
            bg                 = _color_de_fondo,
            activebackground   = _color_de_fondo,
            relief             = 'flat', 
            borderwidth        = 0,
            highlightthickness = 0, 
            command            = _funcion
        )
        self.boton.pack(side = _sub_alineacion)

        if self.incluir_texto:
            self.texto = tk.Label(
                self, 
                bg                 = _color_de_fondo, 
                fg                 = _color_de_texto,
                disabledforeground = '#f0f0f0',
                **_fuente
            )

            if _texto_variable:
                self.texto_variable = tk.StringVar(self)
                self.texto_variable.set(_texto)
                self.texto.config(textvariable = self.texto_variable)
            
            else:
                self.texto.config(text =  _texto)
            self.texto.pack(side = _sub_alineacion)
        
        if _desabilitado: self.desabilitar()

        self.pack(side = _alineacion, **_margen)

    def desabilitar(self):
        self.boton.config(state = 'disabled')
        if self.incluir_texto : self.texto.config(state = 'disabled')
        
    def habilitar(self):
        self.boton.config(state = 'normal')
        if self.incluir_texto : self.texto.config(state = 'normal')