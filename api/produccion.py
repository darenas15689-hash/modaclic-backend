from flask_restful import Resource
from flask import request, jsonify
from models import OrdenProduccion
from extensions import db

class ProduccionResource(Resource):

    # GET /api/produccion o /api/produccion/<id>
    def get(self, id=None):
        if id:
            orden = OrdenProduccion.query.get(id)
            if not orden:
                return {"error": "Orden no encontrada"}, 404
            return {
                "id": orden.id,
                "pedido_id": orden.pedido_id,
                "estado": orden.estado,
                "responsable": orden.responsable,
                "fecha_estimada": str(orden.fecha_estimada)
            }, 200

        ordenes = OrdenProduccion.query.all()
        resultado = [{
            "id": o.id,
            "pedido_id": o.pedido_id,
            "estado": o.estado,
            "responsable": o.responsable,
            "fecha_estimada": str(o.fecha_estimada)
        } for o in ordenes]
        return jsonify(resultado)

    # POST /api/produccion
    def post(self):
        data = request.json
        orden = OrdenProduccion(
            pedido_id=data['pedido_id'],
            estado='pendiente',
            responsable=data['responsable'],
            fecha_estimada=data['fecha_estimada']
        )
        db.session.add(orden)
        db.session.commit()
        return {"mensaje": "Orden de producción creada"}, 201

    # PUT /api/produccion/<id>
    def put(self, id):
        orden = OrdenProduccion.query.get(id)
        if not orden:
            return {"error": "Orden no encontrada"}, 404

        data = request.json
        orden.estado = data.get('estado', orden.estado)
        orden.responsable = data.get('responsable', orden.responsable)

        db.session.commit()
        return {"mensaje": "Orden actualizada"}, 200

    # DELETE /api/produccion/<id>
    def delete(self, id):
        orden = OrdenProduccion.query.get(id)
        if not orden:
            return {"error": "Orden no encontrada"}, 404
        db.session.delete(orden)
        db.session.commit()
        return {"mensaje": "Orden eliminada"}, 200
