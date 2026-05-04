from flask import Flask, jsonify
from extensions import db, migrate, ma, cors
from api import api_bp
from flask_cors import CORS  # importamos CORS directamente para configurarlo bien
from api.inventario import inventario_bp
from api.auth import auth_bp


app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
# 🔹 CONFIGURACIÓN DE BASE DE DATOS (MySQL 9.5)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:200514@localhost:3306/modaclic'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# 🔹 INICIALIZACIÓN DE EXTENSIONES
db.init_app(app)
migrate.init_app(app, db)
ma.init_app(app)

# 🔹 CONFIGURACIÓN CORRECTA DE CORS PARA PUT, DELETE, POST
CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)

# 🔹 RESPONDER CORRECTAMENTE A PRE-FLIGHT REQUESTS
@app.before_request
def handle_options_request():
    from flask import request, make_response
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        return response

# 🔹 REGISTRO DE BLUEPRINT API
app.register_blueprint(api_bp, url_prefix='/api')
from api.inventario import inventario_bp
app.register_blueprint(inventario_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/auth")
# 🔹 RUTA PRINCIPAL (PÁGINA DE INICIO)
@app.route('/')
def index():
    return jsonify({
        "titulo": "Aplicación de Moda",
        "nombre": "ModaClic",
        "descripcion": "Backend ERP Multi-Taller para gestión de moda",
        "estado": "Servidor en ejecución correctamente",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

