from database.confdb import db

class DetalleTiempo(db.Model):
    __tablename__ = 'detalle_tiempo'
    id_tiempo = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    def __init__(self, id_usuario, hora_inicio, hora_fin):
        self.id_usuario = id_usuario
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin