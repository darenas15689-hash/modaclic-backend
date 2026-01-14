from flask_restful import Resource
from flask import request
from models import Taller
from extensions import db
from schemas import TallerSchema

taller_schema = TallerSchema()
talleres_schema = TallerSchema(many=True)


class TallerResource(Resource):
    """
    Gestión de talleres (solo debería usarse por Administrador General)
    """

    def get(self):
        talleres = Taller.query.all()
        return talleres_schema.dump(talleres), 200

    def post(self):
        data = request.get_json()

        if not data or 'nombre' not in data:
            return {"error": "El nombre del taller es obligatorio"}, 400

        taller = Taller(
            nombre=data['nombre'],
            activo=True
        )
        db.session.add(taller)
        db.session.commit()

        return taller_schema.dump(taller), 201

    def put(self):
        data = request.get_json()

        if 'id' not in data:
            return {"error": "ID del taller requerido"}, 400

        taller = Taller.query.get_or_404(data['id'])

        taller.nombre = data.get('nombre', taller.nombre)
        taller.activo = data.get('activo', taller.activo)

        db.session.commit()
        return taller_schema.dump(taller), 200

    def delete(self):
        taller_id = request.args.get('id')

        if not taller_id:
            return {"error": "ID requerido"}, 400

        taller = Taller.query.get_or_404(taller_id)
        db.session.delete(taller)
        db.session.commit()

        return {"mensaje": "Taller eliminado correctamente"}, 200
