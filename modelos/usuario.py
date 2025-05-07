from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database.confdb import db

class Usuario(db.Model, UserMixin):  
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)
    licencia = db.Column(db.String(50), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, email, tipo_usuario, password=None, licencia=None):
        self.nombre = nombre
        self.email = email
        self.tipo_usuario = tipo_usuario
        self.licencia = licencia
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id_usuario  