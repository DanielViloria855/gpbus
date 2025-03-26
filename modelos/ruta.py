from database.confdb import db

class Ruta(db.Model):
    __tablename__ = 'ruta'
    id_ruta = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)  # Nuevo campo para el precio
    descripcion = db.Column(db.String(255), nullable=True)  # Nuevo campo para la descripción

    def __init__(self, nombre, precio, descripcion=None):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion