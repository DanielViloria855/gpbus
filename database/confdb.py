from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def inicializar(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gp_kti2_user:qRxyas6WatnSfV2naWsWMQZR7y6ZYoEV@dpg-cvd4cmqn91rc73dco7d0-a.oregon-postgres.render.com/gp_kti2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  
