from database.confdb import db
class Viaje(db.Model):
    __tablename__ = 'viaje'
    id_viaje = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_ruta = db.Column(db.Integer, db.ForeignKey('ruta.id_ruta'), nullable=False)
    id_bus = db.Column(db.String(20), db.ForeignKey('bus.placa'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    def __init__(self, id_usuario, id_ruta, id_bus, fecha):
        self.id_usuario = id_usuario
        self.id_ruta = id_ruta
        self.id_bus = id_bus
        self.fecha = fecha