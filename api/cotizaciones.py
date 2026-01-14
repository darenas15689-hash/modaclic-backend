from flask import Blueprint, request, jsonify
from extensions import db
from sqlalchemy import text

cotizaciones_bp = Blueprint("cotizaciones", __name__)

@cotizaciones_bp.route("/cotizaciones", methods=["GET"])
def listar():
    result = db.session.execute(text("SELECT * FROM cotizaciones"))
    return jsonify([dict(r._mapping) for r in result])

@cotizaciones_bp.route("/cotizaciones", methods=["POST"])
def crear():
    data = request.json
    db.session.execute(
        text("""
            INSERT INTO cotizaciones
            (cliente, tipo_prenda, tela, cantidad, precio_estimado, tiempo_estimado)
            VALUES (:cliente, :tipo, :tela, :cantidad, :precio, :tiempo)
        """),
        {
            "cliente": data["cliente"],
            "tipo": data["tipo_prenda"],
            "tela": data["tela"],
            "cantidad": data["cantidad"],
            "precio": data["precio_estimado"],
            "tiempo": data["tiempo_estimado"]
        }
    )
    db.session.commit()
    return {"mensaje": "Cotización creada"}, 201

@cotizaciones_bp.route("/cotizaciones/<int:id>/aprobar", methods=["PUT"])
def aprobar(id):
    db.session.execute(
        text("UPDATE cotizaciones SET estado='Aprobado' WHERE id=:id"),
        {"id": id}
    )
    db.session.commit()
    return {"mensaje": "Cotización aprobada"}
