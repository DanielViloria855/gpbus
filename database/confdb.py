from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def inicializar(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpbus_user:EVMzvGQ3u8jpr41bZ6BJpRDguftJzdvP@dpg-d07ptj95pdvs73ad24gg-a.oregon-postgres.render.com/gpbus'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  
