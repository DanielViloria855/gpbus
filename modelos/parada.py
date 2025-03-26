from database.confdb import db
class Parada(db.Model):
    __tablename__ = 'parada'
    id_parada = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_ruta = db.Column(db.Integer, db.ForeignKey('ruta.id_ruta'), nullable=False)

    def __init__(self, nombre, id_ruta):
        self.nombre = nombre
        self.id_ruta = id_ruta