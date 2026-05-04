from flask import Blueprint, request, jsonify
from extensions import db
from models import AuthUser
import jwt
import datetime

auth_bp = Blueprint('auth_bp', __name__)

SECRET_KEY = "modaclic_secret_key"


# =========================
# REGISTRO
# =========================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    rol = data.get('rol')

    if not nombre or not email or not password or not rol:
        return jsonify({"msg": "Faltan datos"}), 400

    if AuthUser.query.filter_by(email=email).first():
        return jsonify({"msg": "El usuario ya existe"}), 400

    nuevo = AuthUser(
        nombre=nombre,
        email=email,
        rol=rol
    )

    nuevo.set_password(password)

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"msg": "Usuario creado correctamente"}), 201


# =========================
# LOGIN
# =========================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Faltan datos"}), 400

    user = AuthUser.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"msg": "Credenciales incorrectas"}), 401

    token = jwt.encode({
        "id": user.id,
        "rol": user.rol,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "rol": user.rol,
        "nombre": user.nombre
    })