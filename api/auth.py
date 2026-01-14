from flask_restful import Resource
from flask import request
from models import Usuario

class LoginResource(Resource):
    def post(self):
        data = request.json

        usuario = Usuario.query.filter_by(
            usuario=data.get("usuario"),
            password=data.get("password")
        ).first()

        if not usuario:
            return {"mensaje": "Credenciales incorrectas"}, 401

        return {
            "id": usuario.id,
            "usuario": usuario.usuario,
            "rol": usuario.rol
        }, 200
