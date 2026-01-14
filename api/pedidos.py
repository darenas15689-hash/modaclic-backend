from flask_restful import Resource
from flask import request
from models import Pedido
from extensions import db
from datetime import datetime

class PedidoResource(Resource):

    # GET /api/pedidos
    # GET /api/pedidos/<id>
    def get(self, id=None):
        if id:
            pedido = Pedido.query.get(id)
            if not pedido:
                return {"error": "Pedido no encontrado"}, 404

            return {
                "id": pedido.id,
                "cliente": pedido.cliente,
                "estado": pedido.estado,
                "total": pedido.total,
                "producto": pedido.producto,
                "tipo_prenda": pedido.tipo_prenda,
                "talla": pedido.talla,
                "color": pedido.color,
                "medidas_personalizadas": pedido.medidas_personalizadas,
                "taller_id": pedido.taller_id,
                "fecha": pedido.fecha.strftime("%Y-%m-%d %H:%M:%S") if pedido.fecha else None
            }, 200

        pedidos = Pedido.query.all()
        return [{
            "id": p.id,
            "cliente": p.cliente,
            "estado": p.estado,
            "total": p.total,
            "producto": p.producto,
            "tipo_prenda": p.tipo_prenda,
            "talla": p.talla,
            "color": p.color,
            "medidas_personalizadas": p.medidas_personalizadas,
            "taller_id": p.taller_id,
            "fecha": p.fecha.strftime("%Y-%m-%d %H:%M:%S") if p.fecha else None
        } for p in pedidos], 200

    # POST /api/pedidos
    def post(self):
        data = request.json

        nuevo_pedido = Pedido(
            cliente=data["cliente"],
            estado=data.get("estado", "Pendiente"),
            total=data["total"],
            producto=data.get("producto"),
            tipo_prenda=data.get("tipo_prenda"),
            talla=data.get("talla"),
            color=data.get("color"),
            medidas_personalizadas=data.get("medidas_personalizadas"),
            taller_id=data.get("taller_id"),
            fecha=datetime.now()
        )

        db.session.add(nuevo_pedido)
        db.session.commit()

        return {"mensaje": "Pedido creado correctamente"}, 201

    # PUT /api/pedidos/<id>
    def put(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            return {"error": "Pedido no encontrado"}, 404

        data = request.json

        pedido.cliente = data.get("cliente", pedido.cliente)
        pedido.estado = data.get("estado", pedido.estado)
        pedido.total = data.get("total", pedido.total)
        pedido.producto = data.get("producto", pedido.producto)
        pedido.tipo_prenda = data.get("tipo_prenda", pedido.tipo_prenda)
        pedido.talla = data.get("talla", pedido.talla)
        pedido.color = data.get("color", pedido.color)
        pedido.medidas_personalizadas = data.get(
            "medidas_personalizadas",
            pedido.medidas_personalizadas
        )

        db.session.commit()

        return {"mensaje": "Pedido actualizado correctamente"}, 200

    # DELETE /api/pedidos/<id>
    def delete(self, id):
        pedido = Pedido.query.get(id)
        if not pedido:
            return {"error": "Pedido no encontrado"}, 404

        db.session.delete(pedido)
        db.session.commit()
        return {"mensaje": "Pedido eliminado"}, 200
