from flask import Blueprint, request, jsonify
from extensions import db
from sqlalchemy import text

inventario_bp = Blueprint("inventario", __name__)

# ===============================
# MATERIA PRIMA
# ===============================

@inventario_bp.route("/inventario/materia-prima", methods=["GET"])
def listar_materia_prima():
    result = db.session.execute(
        text("SELECT * FROM inventario_materia_prima")
    )
    data = [dict(row._mapping) for row in result]
    return jsonify(data), 200


@inventario_bp.route("/inventario/materia-prima", methods=["POST"])
def crear_materia_prima():
    data = request.json

    db.session.execute(
        text("""
            INSERT INTO inventario_materia_prima (nombre, unidad, stock)
            VALUES (:nombre, :unidad, :stock)
        """),
        {
            "nombre": data["nombre"],
            "unidad": data["unidad"],
            "stock": data["stock"]
        }
    )

    db.session.commit()
    return {"mensaje": "Materia prima registrada"}, 201


@inventario_bp.route("/inventario/materia-prima/<int:id>", methods=["PUT"])
def editar_materia_prima(id):
    data = request.json

    db.session.execute(
        text("""
            UPDATE inventario_materia_prima
            SET nombre = :nombre,
                unidad = :unidad,
                stock = :stock
            WHERE id = :id
        """),
        {
            "id": id,
            "nombre": data["nombre"],
            "unidad": data["unidad"],
            "stock": data["stock"]
        }
    )

    db.session.commit()
    return {"mensaje": "Materia prima actualizada"}, 200


@inventario_bp.route("/inventario/materia-prima/<int:id>", methods=["DELETE"])
def eliminar_materia_prima(id):
    db.session.execute(
        text("DELETE FROM inventario_materia_prima WHERE id = :id"),
        {"id": id}
    )

    db.session.commit()
    return {"mensaje": "Materia prima eliminada"}, 200


# ===============================
# INVENTARIO PRODUCTOS
# ===============================

@inventario_bp.route("/inventario/productos", methods=["GET"])
def listar_productos():
    result = db.session.execute(
        text("SELECT * FROM inventario_productos")
    )
    data = [dict(row._mapping) for row in result]
    return jsonify(data), 200


@inventario_bp.route("/inventario/productos", methods=["POST"])
def crear_producto():
    data = request.json

    db.session.execute(
        text("""
            INSERT INTO inventario_productos
            (nombre, tipo, talla, color, stock)
            VALUES (:nombre, :tipo, :talla, :color, :stock)
        """),
        {
            "nombre": data["nombre"],
            "tipo": data["tipo"],
            "talla": data["talla"],
            "color": data["color"],
            "stock": data["stock"]
        }
    )

    db.session.commit()
    return {"mensaje": "Producto registrado"}, 201


@inventario_bp.route("/inventario/productos/<int:id>", methods=["PUT"])
def editar_producto(id):
    data = request.json

    db.session.execute(
        text("""
            UPDATE inventario_productos
            SET nombre = :nombre,
                tipo = :tipo,
                talla = :talla,
                color = :color,
                stock = :stock
            WHERE id = :id
        """),
        {
            "id": id,
            "nombre": data["nombre"],
            "tipo": data["tipo"],
            "talla": data["talla"],
            "color": data["color"],
            "stock": data["stock"]
        }
    )

    db.session.commit()
    return {"mensaje": "Producto actualizado"}, 200


@inventario_bp.route("/inventario/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    db.session.execute(
        text("DELETE FROM inventario_productos WHERE id = :id"),
        {"id": id}
    )

    db.session.commit()
    return {"mensaje": "Producto eliminado"}, 200


# ===============================
# CALCULADORA DE PRECIOS
# ===============================

@inventario_bp.route("/calculadora/precio", methods=["POST"])
def calcular_precio():
    data = request.json

    tipo_prenda = data.get("tipo_prenda")
    tela = data.get("tela")
    cantidad = int(data.get("cantidad", 1))

    base_prenda = {
        "Camisa": 20000,
        "Pantalón": 30000,
        "Chaqueta": 50000,
        "Vestido": 40000
    }

    costo_tela = {
        "Algodón": 8000,
        "Jean": 10000,
        "Seda": 15000,
        "Lino": 12000,
        "Cuero": 20000,
        "Poliéster": 7000,
        "Drill": 9000
    }

    precio_unitario = (
        base_prenda.get(tipo_prenda, 20000)
        + costo_tela.get(tela, 8000)
    )

    precio_estimado = precio_unitario * cantidad

    return jsonify({
        "precio_unitario": precio_unitario,
        "precio_estimado": precio_estimado
    }), 200


# ===============================
# COTIZACIONES
# ===============================

@inventario_bp.route("/cotizaciones", methods=["GET"])
def listar_cotizaciones():
    result = db.session.execute(
        text("SELECT * FROM cotizaciones ORDER BY fecha DESC")
    )
    data = [dict(row._mapping) for row in result]
    return jsonify(data), 200


@inventario_bp.route("/cotizaciones", methods=["POST"])
def crear_cotizacion():
    data = request.json

    db.session.execute(
        text("""
            INSERT INTO cotizaciones
            (cliente, tipo_prenda, tela, cantidad, precio_estimado, tiempo_estimado, estado)
            VALUES
            (:cliente, :tipo_prenda, :tela, :cantidad, :precio_estimado, :tiempo_estimado, :estado)
        """),
        {
            "cliente": data["cliente"],
            "tipo_prenda": data["tipo_prenda"],
            "tela": data["tela"],
            "cantidad": data["cantidad"],
            "precio_estimado": data["precio_estimado"],
            "tiempo_estimado": data["tiempo_estimado"],
            "estado": data.get("estado", "Cotizado")
        }
    )

    db.session.commit()
    return {"mensaje": "Cotización creada"}, 201


@inventario_bp.route("/cotizaciones/<int:id>", methods=["PUT"])
def editar_cotizacion(id):
    data = request.json

    db.session.execute(
        text("""
            UPDATE cotizaciones
            SET cliente = :cliente,
                tipo_prenda = :tipo_prenda,
                tela = :tela,
                cantidad = :cantidad,
                precio_estimado = :precio_estimado,
                tiempo_estimado = :tiempo_estimado,
                estado = :estado
            WHERE id = :id
        """),
        {
            "id": id,
            "cliente": data["cliente"],
            "tipo_prenda": data["tipo_prenda"],
            "tela": data["tela"],
            "cantidad": data["cantidad"],
            "precio_estimado": data["precio_estimado"],
            "tiempo_estimado": data["tiempo_estimado"],
            "estado": data["estado"]
        }
    )

    db.session.commit()
    return {"mensaje": "Cotización actualizada"}, 200


@inventario_bp.route("/cotizaciones/<int:id>", methods=["DELETE"])
def eliminar_cotizacion(id):
    db.session.execute(
        text("DELETE FROM cotizaciones WHERE id = :id"),
        {"id": id}
    )

    db.session.commit()
    return {"mensaje": "Cotización eliminada"}, 200
