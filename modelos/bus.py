from database.confdb import db

class Bus(db.Model):
    __tablename__ = 'bus'
    placa = db.Column(db.String(20), primary_key=True)
    capacidad = db.Column(db.Integer, nullable=False)
    flota = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='en espera')

    def __init__(self, placa, capacidad, flota, lat, lng, estado='en espera'):
        self.placa = placa
        self.capacidad = capacidad
        self.flota = flota
        self.lat = lat
        self.lng = lng
        self.estado = estado

    def to_dict(self):
        return {
            'placa': self.placa,
            'capacidad': self.capacidad,
            'flota': self.flota,
            'lat': self.lat,
            'lng': self.lng,
            'estado': self.estado
        }