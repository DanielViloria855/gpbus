from database.confdb import db

class usuario(db.Model): 
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tipousuario = db.Column(db.String(20), nullable=False)
    licencia = db.Column(db.String(50))

    def __init__(self, nombre, email, tipo_usuario, licencia=None):
        self.Nombre = nombre
        self.Email = email
        self.TipoUsuario = tipo_usuario
        self.Licencia = licencia
