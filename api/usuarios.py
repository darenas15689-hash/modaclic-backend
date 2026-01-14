from flask_restful import Resource
from flask import request   # ✅ ESTA LÍNEA FALTABA
from models import Usuario
from schemas import UsuarioSchema
from extensions import db

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

class UsuarioResource(Resource):

    def get(self):
        usuarios = Usuario.query.all()
        return usuarios_schema.dump(usuarios), 200

    def post(self):
        data = request.json
        usuario = Usuario(**data)
        db.session.add(usuario)
        db.session.commit()
        return usuario_schema.dump(usuario), 201
