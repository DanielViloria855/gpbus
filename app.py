import datetime
import random
import re  # Para validar el email
from flask import Blueprint, Flask, flash, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from database.confdb import db, inicializar
from modelos import usuario
from modelos.usuario import Usuario as UsuarioModel
from modelos.bus import Bus
from modelos.detalle_tiempo import DetalleTiempo
from modelos.ruta import Ruta as RutaModel
from modelos.viaje import Viaje
from modelos.viaje import Viaje as ViajeModel
from modelos.parada import Parada

app = Flask(__name__)
inicializar(app)
buses = [
    Bus('ABC123', 50, 'Flota 1', 6.2777, -75.6358, 'en ruta'),
    Bus('XYZ456', 40, 'Flota 2', 6.4473, -75.5818, 'en espera'),
    Bus('MNO789', 55, 'Flota 3', 6.3959, -75.6471, 'en ruta'),
    Bus('JKL012', 45, 'Flota 4', 6.4595, -75.5597, 'en ruta')
]
gps = Blueprint('gps', __name__)

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.secret_key = 'daniel115valdes'

@login_manager.user_loader
def load_user(user_id):
    return UsuarioModel.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form  
        usuario = UsuarioModel.query.filter_by(email=data.get('email')).first()

        if usuario and usuario.check_password(data.get('password')):
            login_user(usuario)
            
            if usuario.tipo_usuario == "pasajero":
                return redirect(url_for('pagina_pasajero'))
            elif usuario.tipo_usuario == "conductor":
                return redirect(url_for('pagina_conductor'))
            elif usuario.tipo_usuario == "admin":
                return redirect(url_for('pagina_admin'))
            else:
                return redirect(url_for('index'))
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
        
        tipo_usuario = "pasajero"
        licencia = None
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
            password=password,
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
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        descripcion = request.form.get("descripcion")
        origen = request.form.get("origen")
        destino = request.form.get("destino")
        latitud_origen = request.form.get("latitud_origen")
        longitud_origen = request.form.get("longitud_origen")
        latitud_destino = request.form.get("latitud_destino")
        longitud_destino = request.form.get("longitud_destino")


        if not nombre or not precio or not origen or not destino or not latitud_destino or not longitud_destino or not latitud_origen or not longitud_origen or not descripcion:
            flash(" Datos obligatorios", "danger")
            return redirect(url_for('pagina_admin'))

        nueva_ruta = RutaModel(nombre=nombre, precio=float(precio), descripcion=descripcion, origen=origen, destino=destino, latitud_origen=float(latitud_origen), longitud_origen=float(longitud_origen),
                               latitud_destino=float(latitud_destino), longitud_destino=float(longitud_destino) )
        db.session.add(nueva_ruta)
        db.session.commit()
        flash("Ruta agregada con éxito", "success")
        return redirect(url_for('pagina_admin'))

    rutas = RutaModel.query.all()
    return render_template('admin.html', rutas=rutas)

@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ruta(id):
    ruta = RutaModel.query.get_or_404(id)  # Asegúrate de que el ID se maneje correctamente

    if request.method == 'POST':
        ruta.nombre = request.form.get("nombre")
        ruta.precio = float(request.form.get("precio"))
        ruta.descripcion = request.form.get("descripcion")
        origen = request.form.get("origen")
        destino = request.form.get("destino")
        latitud_origen = request.form.get("latitud_origen")
        longitud_origen = request.form.get("longitud_origen")
        latitud_destino = request.form.get("latitud_destino")
        longitud_destino = request.form.get("longitud_destino")
        db.session.commit()
        flash("Ruta actualizada con éxito", "success")
        return redirect(url_for('pagina_admin'))

    return render_template('editar_ruta.html', ruta=ruta)

@app.route('/admin/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_ruta(id):
    ruta = RutaModel.query.get_or_404(id)
    db.session.delete(ruta)
    db.session.commit()
    flash("Ruta eliminada con éxito", "success")
    return redirect(url_for('pagina_admin'))

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

@app.route('/rutas/<nombre>', methods=['GET'])
def obtener_ruta(nombre):
    ruta = RutaModel.query.filter_by(nombre=nombre).first()
    
    if ruta:
        return jsonify({
            "nombre": ruta.nombre,
            "descripcion": ruta.descripcion,
            "precio": ruta.precio
        })
    else:
        return jsonify({"error": "Ruta no encontrada"}), 404

@app.route('/admin/conductores', methods=['GET', 'POST'])
@login_required
def admin_conductores():
    if current_user.tipo_usuario != 'admin':
        flash("Acceso denegado", "danger")
        return redirect(url_for('pagina_admin'))

    if request.method == 'POST':
        nombre   = request.form.get("nombre")
        email    = request.form.get("email")
        licencia = request.form.get("licencia")
        password = request.form.get("password")

        if not nombre or not email or not licencia or not password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for('admin_conductores'))

        # Aquí usas la clase, no el módulo:
        if UsuarioModel.query.filter_by(email=email).first():
            flash("Ya existe un conductor con ese email", "danger")
            return redirect(url_for('admin_conductores'))

        nuevo = UsuarioModel(
            nombre=nombre,
            email=email,
            tipo_usuario='conductor',
            password=password,
            licencia=licencia
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Conductor agregado con éxito", "success")
        return redirect(url_for('admin_conductores'))

    conductores = UsuarioModel.query.filter_by(tipo_usuario='conductor').all()
    return render_template('conductores.html', conductores=conductores)


@app.route('/admin/conductores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_conductor(id):
    # Solo admins
    if current_user.tipo_usuario != 'admin':
        flash("Acceso denegado", "danger")
        return redirect(url_for('pagina_admin'))

    c = UsuarioModel.query.get_or_404(id)
    if c.tipo_usuario != 'conductor':
        flash("Usuario no es conductor válido", "danger")
        return redirect(url_for('admin_conductores'))

    if request.method == 'POST':
        c.nombre   = request.form.get("nombre")
        c.email    = request.form.get("email")
        c.licencia = request.form.get("licencia")
        pwd        = request.form.get("password")
        if pwd:
            c.set_password(pwd)
        db.session.commit()
        flash("Conductor actualizado con éxito", "success")
        return redirect(url_for('admin_conductores'))

    return render_template('editar_conductor.html', conductor=c)


@app.route('/admin/conductores/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_conductor(id):
    if current_user.tipo_usuario != 'admin':
        flash("Acceso denegado", "danger")
        return redirect(url_for('pagina_admin'))

    conductor = UsuarioModel.query.get_or_404(id)
    if conductor.tipo_usuario != 'conductor':
        flash("El usuario no es un conductor válido", "danger")
        return redirect(url_for('admin_conductores'))

    db.session.delete(conductor)
    db.session.commit()
    flash("Conductor eliminado con éxito", "success")
    return redirect(url_for('admin_conductores'))


@app.route('/get-destinos')
def get_destinos():
    rutas = RutaModel.query.all()

    destinos = []
    for ruta in rutas:
        destinos.append({
            "nombre": ruta.nombre,
            "destino": ruta.destino,
            "lat": ruta.latitud_destino,
            "lng": ruta.longitud_destino
        })

    return jsonify(destinos)
@app.route('/iniciar_simulacion', methods=['POST'])
@login_required
def iniciar_simulacion():
    # 1) ID del usuario autenticado
    id_usuario = current_user.get_id()

    # 2) Leer JSON de la petición
    data = request.get_json(silent=True) or {}
    id_ruta = data.get('id_ruta')
    if not id_ruta:
        return jsonify({ 'status': 'error', 'message': 'No se recibió id_ruta' }), 400

    # 3) Seleccionar un bus aleatorio
    placas = [bus.placa for bus in buses]  # usa tu lista estática o haz consulta a la BD
    if not placas:
        return jsonify({ 'status': 'error', 'message': 'No hay buses disponibles' }), 500
    id_bus_aleatorio = random.choice(placas)

    # 4) Fecha y hora actual
    fecha_actual = datetime.datetime.utcnow()

    # 5) Crear y guardar el viaje en la BD
    nuevo_viaje = ViajeModel(
        id_usuario=int(id_usuario),
        id_ruta=int(id_ruta),
        id_bus=id_bus_aleatorio,
        fecha=fecha_actual
    )
    try:
        db.session.add(nuevo_viaje)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({ 'status': 'error', 'message': f'Excepción al guardar: {str(e)}' }), 500

    # 6) Devolver JSON de éxito
    return jsonify({ 'status': 'ok', 'message': 'Viaje registrado correctamente' }), 200

from werkzeug.security import generate_password_hash

hash = generate_password_hash("1234567", method="pbkdf2:sha256")
print(hash)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    

