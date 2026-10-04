from time import time

class Instrumentar():
    def __init__(self, process_name = 'Proceso', level = 0):
        self.inicio       = time()
        self.level        = level
        self.process_name = process_name
    
    def fin(self):
        print(self.level*'\t' + f'- {self.process_name} Finalizado en {round(time()-self.inicio,2)} segundos')