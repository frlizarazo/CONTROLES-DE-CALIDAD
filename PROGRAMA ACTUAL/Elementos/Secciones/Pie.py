import io
import base64
import os
import tempfile
import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from Estilos.colores  import COLOR_FONDO, COLOR_FUENTE_SECUNDARIA
from Estilos.fuentes  import FUENTE_PEQUEÑA
from Estilos.margenes import MARGEN_NORMAL, EXPANDIR_HORIZONTAL, LEFT, RIGHT, MARGEN_SOLO_HORIZONTAL
from Recursos.imagenes import imagenes

from Elementos.barra_de_carga import barra_de_carga
from Datos.textos import CITA

class Pie(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(bg = COLOR_FONDO)

        # Contenedor principal para la cita y los botones
        contenedor_cita = tk.Frame(self, bg = COLOR_FONDO)
        contenedor_cita.pack(fill = 'x', pady = (0, 5))

        # Texto de la cita
        lbl_cita = tk.Label(
            contenedor_cita, 
            text = CITA, 
            justify = 'left', 
            background = COLOR_FONDO,
            **FUENTE_PEQUEÑA
        )
        lbl_cita.pack(**LEFT, fill = 'x', expand = True)

        # Contenedor para alinear los botones a la derecha
        frame_botones = tk.Frame(contenedor_cita, bg = COLOR_FONDO)
        frame_botones.pack(**RIGHT, padx = (5, 0))

        # Botón Copiar
        btn_copiar = tk.Button(
            frame_botones,
            text = "Copiar",
            command = self.copiar_cita,
            cursor = "hand2",
            relief = "flat",
            bd = 1
        )
        btn_copiar.pack(**LEFT, padx = 2)

        # Contenedor inferior de logos
        contenedor_logos = tk.Frame(self, bg = COLOR_FONDO)
        contenedor_logos.pack(side = 'top')

        imagen = imagenes['logos']
        imagen = base64.b64decode(imagen)
        imagen = Image.open(io.BytesIO(imagen))
        imagen = imagen.resize((520, 50))

        self.logos = ImageTk.PhotoImage(imagen)

        tk.Label(
            contenedor_logos,
            image = self.logos,
            bg    = COLOR_FONDO,
            fg    = COLOR_FUENTE_SECUNDARIA,
            **FUENTE_PEQUEÑA
        ).pack(**LEFT, **EXPANDIR_HORIZONTAL)

        self.pack(**EXPANDIR_HORIZONTAL, **MARGEN_NORMAL)

    def copiar_cita(self):
        """Copia el contenido de CITA al portapapeles del sistema."""
        self.clipboard_clear()
        self.clipboard_append(CITA)
        self.update()
        messagebox.showinfo("Copia exitosa", "La cita se ha copiado al portapapeles.")