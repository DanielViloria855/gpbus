from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def inicializar(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpbus_0o6h_user:YgIdrwLwd5qbMG5OkiwGxVNmKZrEAZcp@dpg-d0lu0u0gjchc739bes5g-a.oregon-postgres.render.com/gpbus_0o6h'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  
