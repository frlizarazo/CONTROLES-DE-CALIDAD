
class serie:
    def __init__(self, _ruta):
        _ruta = _ruta.replace('\\','/')

        self.ruta = _ruta

        (
         self.directorio,
         self.nombre
        ) = _ruta.rsplit('/',1)

        self.nombre = self.nombre.replace('.csv','')


class series:
    def __init__(self, _rutas):
        self.series  = [serie(ruta) for ruta in _rutas]

        self.directorio = self.series[0].directorio
    
        self.nombres = [serie_.nombre for serie_ in self.series]
        self.rutas   = [serie_.ruta   for serie_ in self.series]

        self.numero = len(self.series)