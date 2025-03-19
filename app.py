from flask import Flask, request, jsonify 
from database.confdb import db
from database.confdb import inicializar
from modelos.usuario import usuario

app = Flask(__name__)
inicializar(app)

@app.route('/usuarios', methods = ['GET'])
def obtener_usuarios():
    usuarios = usuario.query.all() 
    resultado = [
        {
            "id_usuario": u.id_usuario,
            "nombre": u.nombre,
            "email": u.email,
            "tipousuario": u.tipousuario,
            "licencia": u.licencia
        }
        for u in usuarios
    ]
    return jsonify(resultado)

@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = usuario.query.get(id)
    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    return jsonify({"ID_Usuario": usuario.id_usuario, "Nombre": usuario.nombre, 
                    "Email": usuario.email, "TipoUsuario": usuario.tipousuario, 
                    "Licencia": usuario.licencia})

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = usuario(
        nombre=data.get('nombre'),
        email=data.get('email'),
        tipo_usuario=data.get('tipousuario'),
        licencia=data.get('licencia')
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)  