from database.confdb import db

class Ruta(db.Model):
    __tablename__ = 'ruta'
    id_ruta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False) 
    origen = db.Column(db.String(100), nullable=False) 
    descripcion = db.Column(db.String(255), nullable=True) 
    destino = db.Column(db.String(100), nullable = False)
    latitud_origen = db.Column(db.Float, nullable = False)
    longitud_origen = db.Column(db.Float, nullable = False)
    latitud_destino = db.Column(db.Float, nullable=False)
    longitud_destino = db.Column(db.Float, nullable=False)

    def __init__(self, nombre, precio, descripcion, origen, 
                 destino, latitud_origen, longitud_origen, latitud_destino, longitud_destino
                 ):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.destino = destino
        self.latitud_destino = latitud_destino
        self.longitud_destino = longitud_destino
        self.latitud_origen = latitud_origen
        self.longitud_origen = longitud_origen
        self.origen = origen