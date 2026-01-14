from flask_restful import Resource
from flask import request
from models import Producto
from schemas import ProductoSchema
from extensions import db

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

class ProductoResource(Resource):

    # GET: todos o por id
    def get(self, id=None):
        if id:
            producto = Producto.query.get(id)
            if not producto:
                return {"error": "Producto no encontrado"}, 404
            return producto_schema.dump(producto), 200
        else:
            taller_id = request.args.get('taller_id')
            if not taller_id:
                return {"error": "taller_id requerido"}, 400
            productos = Producto.query.filter_by(taller_id=taller_id).all()
            return productos_schema.dump(productos), 200

    # POST: crear nuevo producto
    def post(self):
        data = request.get_json()
        if not data.get("nombre") or not data.get("taller_id"):
            return {"error": "Datos incompletos"}, 400

        producto = Producto(
            nombre=data["nombre"],
            precio=data.get("precio", 0),
            taller_id=data["taller_id"],
            activo=True
        )
        db.session.add(producto)
        db.session.commit()
        return producto_schema.dump(producto), 201

    # PUT: actualizar producto por id
    def put(self, id):
        producto = Producto.query.get(id)
        if not producto:
            return {"error": "Producto no encontrado"}, 404

        data = request.get_json()
        producto.nombre = data.get("nombre", producto.nombre)
        producto.precio = data.get("precio", producto.precio)
        producto.activo = data.get("activo", producto.activo)

        db.session.commit()
        return producto_schema.dump(producto), 200

    # DELETE: eliminar producto por id
    def delete(self, id):
        producto = Producto.query.get(id)
        if not producto:
            return {"error": "Producto no encontrado"}, 404

        db.session.delete(producto)
        db.session.commit()
        return {"mensaje": f"Producto {id} eliminado"}, 200
