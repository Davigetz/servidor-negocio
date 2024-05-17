from flask import Blueprint, request, jsonify
from database import get_db_connection

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/', methods=['POST'])
def create_usuario():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuarios (nombre, apellido, telefono, email, contrasena, localidad)
        VALUES (%s, %s, %s, %s, %s, POINT(%s, %s))
        RETURNING id
    """, (data['nombre'], data['apellido'], data['telefono'], data['email'], data['contrasena'], data['localidad']['lon'], data['localidad']['lat']))
    usuario_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuario creado", "id": usuario_id}), 201

@usuario_bp.route('/', methods=['GET'])
def get_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, apellido, telefono, email, localidad
        FROM usuarios
    """)
    usuarios = cur.fetchall()
    results = [
        {
            "id": usuario[0],
            "nombre": usuario[1],
            "apellido": usuario[2],
            "telefono": usuario[3],
            "email": usuario[4],
            "localidad": usuario[5]
        } for usuario in usuarios]
    cur.close()
    conn.close()
    return jsonify(results), 200

@usuario_bp.route('/<uuid:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nombre, apellido, telefono, email, localidad
        FROM usuarios
        WHERE id = %s
    """, (str(usuario_id),))
    usuario = cur.fetchone()
    if usuario is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    result = {
        "id": usuario[0],
        "nombre": usuario[1],
        "apellido": usuario[2],
        "telefono": usuario[3],
        "email": usuario[4],
        "localidad": usuario[5]
    }
    cur.close()
    conn.close()
    return jsonify(result), 200

@usuario_bp.route('/<uuid:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuarios
        SET nombre = %s,
            apellido = %s,
            telefono = %s,
            email = %s,
            contrasena = %s,
            localidad = POINT(%s, %s)
        WHERE id = %s
    """, (data['nombre'], data['apellido'], data['telefono'], data['email'], data['contrasena'], data['localidad']['lon'], data['localidad']['lat'], str(usuario_id)))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuario actualizado"}), 200

@usuario_bp.route('/<uuid:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM usuarios
        WHERE id = %s
    """, (str(usuario_id),))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Usuario eliminado"}), 200