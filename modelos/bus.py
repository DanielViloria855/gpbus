from database.confdb import db
class Bus(db.Model):
    __tablename__ = 'bus'
    placa = db.Column(db.String(20), primary_key=True)
    capacidad = db.Column(db.Integer, nullable=False)
    flota = db.Column(db.String(50), nullable=False)

    def __init__(self, placa, capacidad, flota):
        self.placa = placa
        self.capacidad = capacidad
        self.flota = flota
