from threading import Thread

def hilo_ejecucion(_ventana_principal, _funcion):

    def esta_ejecutando():
        if not hilo.is_alive():
            _ventana_principal.bell()
        else:
            _ventana_principal.after(100, esta_ejecutando)

    hilo = Thread(target = _funcion)
    hilo.start()
    esta_ejecutando()