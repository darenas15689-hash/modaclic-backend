from flask_restful import Resource
from flask import request, jsonify
from models import Cita
from extensions import db
from datetime import datetime

class CitaResource(Resource):

    def get(self, id=None):
        if id:
            cita = Cita.query.get(id)
            if not cita:
                return {"error": "Cita no encontrada"}, 404
            return {
                "id": cita.id,
                "cliente": cita.cliente,
                "fecha": cita.fecha.strftime("%Y-%m-%d %H:%M:%S") if cita.fecha else None,
                "servicio_id": cita.servicio_id,
                "asesor": cita.asesor,
                "taller_id": cita.taller_id
            }, 200

        citas = Cita.query.all()
        resultado = [{
            "id": c.id,
            "cliente": c.cliente,
            "fecha": c.fecha.strftime("%Y-%m-%d %H:%M:%S") if c.fecha else None,
            "servicio_id": c.servicio_id,
            "asesor": c.asesor,
            "taller_id": c.taller_id
        } for c in citas]
        return jsonify(resultado)

    def post(self):
        data = request.json
        # Validar campos obligatorios
        for campo in ["cliente","fecha","taller_id"]:
            if campo not in data or not data[campo]:
                return {"error": f"Campo requerido faltante: {campo}"}, 400

        # Convertir fecha de "YYYY-MM-DDTHH:MM" a datetime
        try:
            fecha = datetime.strptime(data['fecha'], "%Y-%m-%dT%H:%M")
        except ValueError:
            return {"error": "Formato de fecha incorrecto. Use YYYY-MM-DDTHH:MM"}, 400

        cita = Cita(
            cliente=data['cliente'],
            fecha=fecha,
            servicio_id=data.get('servicio_id'),
            asesor=data.get('asesor'),
            taller_id=data['taller_id']
        )
        db.session.add(cita)
        db.session.commit()
        return {"mensaje": "Cita creada"}, 201

    # PUT /api/citas/<id>
    def put(self, id):
        cita = Cita.query.get(id)
        if not cita:
            return {"error": "Cita no encontrada"}, 404

        data = request.json
        if 'fecha' in data:
            try:
                cita.fecha = datetime.strptime(data['fecha'], "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                return {"error": f"Formato de fecha incorrecto: {str(e)}"}, 400
        if 'asesor' in data:
            cita.asesor = data['asesor']

        db.session.commit()
        return {"mensaje": "Cita actualizada"}, 200

    def delete(self, id):
        cita = Cita.query.get(id)
        if not cita:
            return {"error": "Cita no encontrada"}, 404
        db.session.delete(cita)
        db.session.commit()
        return {"mensaje": "Cita eliminada"}, 200
