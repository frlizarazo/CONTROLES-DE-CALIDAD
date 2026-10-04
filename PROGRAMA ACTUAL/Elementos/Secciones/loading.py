import tkinter as tk
from PIL import Image, ImageTk

class VentanaGIF(tk.Tk):
    def __init__(self, gif_path):
        super().__init__()
        self.config(bg='#fff')
        self.title("GIF Animado en Tkinter")

        # Cargar el gif utilizando PIL
        self.gif = Image.open(gif_path)
        
        # Crear un label donde se mostrará el gif
        self.label_gif = tk.Label(self)
        self.label_gif.pack()

        # Contador de frames
        self.frame_index = 0
        
        # Actualizar la imagen cada cierto tiempo para crear la animación
        self.actualizar_gif()

    def actualizar_gif(self):
        try:
            # Seleccionar el frame actual del GIF
            self.gif.seek(self.frame_index)
            
            # Convertir el frame en una imagen que Tkinter puede mostrar
            frame = ImageTk.PhotoImage(self.gif)
            
            # Mostrar el frame en el label
            self.label_gif.config(image=frame)
            self.label_gif.image = frame
            
            # Avanzar al siguiente frame
            self.frame_index += 1
            
            # Si el índice sobrepasa el número de frames, reiniciar el índice
            if self.frame_index == self.gif.n_frames:
                self.frame_index = 0

            # Volver a actualizar después de 100 milisegundos (ajusta según la velocidad de tu GIF)
            self.after(20, self.actualizar_gif)

        except Exception as e:
            print("Error al cargar GIF:", e)

# Ruta del gif animado
gif_path = r"C:\Users\Franklin\Desktop\Programas\0. Código\Recursos\loading.gif"

# Crear la ventana y mostrar el gif
app = VentanaGIF(gif_path)
app.mainloop()
