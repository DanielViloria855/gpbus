import datetime
import re  # Para validar el email
from flask import Flask, flash, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from database.confdb import db, inicializar
from modelos.usuario import Usuario as UsuarioModel
from modelos.bus import Bus
from modelos.detalle_tiempo import DetalleTiempo
from modelos.ruta import Ruta as RutaModel
from modelos.viaje import Viaje
from modelos.parada import Parada

app = Flask(__name__)
inicializar(app)

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirigir a la vista de inicio de sesión
app.secret_key = 'daniel115valdes'
@login_manager.user_loader
def load_user(user_id):
    return UsuarioModel.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form  
        usuario = UsuarioModel.query.filter_by(email=data.get('email')).first()

        if usuario and usuario.check_password(data.get('password')):  # Usar el método check_password
            login_user(usuario)  # Iniciar sesión
            
            # Redirigir según el tipo de usuario
            if usuario.tipo_usuario == "pasajero":
                return redirect(url_for('pagina_pasajero'))  # Redirigir a la página de pasajero
            elif usuario.tipo_usuario == "conductor":
                return redirect(url_for('pagina_conductor'))  # Redirigir a la página de conductor
            elif usuario.tipo_usuario == "admin":
                return redirect(url_for('pagina_admin'))  # Redirigir a la página de administrador
            else:
                return redirect(url_for('index'))  # Redirigir a la página de inicio por defecto
        else: 
            flash("Credenciales incorrectas", "danger")
    
    return render_template('login.html')
@app.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        tipo_usuario = request.form.get("tipo_usuario")
        password = request.form.get("password")
        licencia = request.form.get("licencia", None)

        if not nombre or not email or not tipo_usuario or not password:
            return render_template("registro.html", mensaje="Todos los campos son obligatorios")

        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            return render_template("registro.html", mensaje="El email no es válido")

        tipos_permitidos = {"conductor", "cliente", "admin", "pasajero"}
        if tipo_usuario not in tipos_permitidos:
            return render_template("registro.html", mensaje="Tipo de usuario inválido")

        if tipo_usuario == "conductor" and not licencia:
            return render_template("registro.html", mensaje="El campo 'licencia' es obligatorio para conductores")

        if len(password) < 6:
            return render_template("registro.html", mensaje="La contraseña debe tener al menos 6 caracteres")

        usuario_existente = UsuarioModel.query.filter_by(email=email).first()
        if usuario_existente:
            return render_template("registro.html", mensaje="El email ya está registrado")

        nuevo_usuario = UsuarioModel(
        nombre=nombre,
        email=email,
        tipo_usuario=tipo_usuario,
        password=password,  # Esto llamará a set_password
        licencia=licencia if tipo_usuario == "conductor" else None
    )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return render_template("registro.html", mensaje=f"Error: {str(e)}")

    return render_template("registro.html")

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def pagina_admin():
    if request.method == 'POST':
        # Agregar nueva ruta
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")

        if not nombre or not precio:
            flash("Nombre y precio son obligatorios", "danger")
            return redirect(url_for('pagina_admin'))

        nueva_ruta = RutaModel(nombre=nombre, precio=float(precio), descripcion=descripcion)
        db.session.add(nueva_ruta)
        db.session.commit()
        flash("Ruta agregada con éxito", "success")
        return redirect(url_for('pagina_admin'))

    # Obtener todas las rutas existentes
    rutas = RutaModel.query.all()
    return render_template('admin.html', rutas=rutas)

@app.route('/')
@login_required
def index():
    return render_template('bienvenida.html')
@app.route('/pasajero')

def pagina_pasajero():
    return render_template('pasajero.html', usuario=current_user)

@app.route('/conductor')

def pagina_conductor():
    return render_template('conductor.html', usuario=current_user)


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)


