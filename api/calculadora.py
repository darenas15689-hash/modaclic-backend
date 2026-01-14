from flask import Blueprint, request, jsonify
from extensions import db
from sqlalchemy import text

calculadora_bp = Blueprint("calculadora", __name__)

@calculadora_bp.route("/calculadora/precio", methods=["POST"])
def calcular_precio():
    data = request.json

    result = db.session.execute(
        text("""
            SELECT mano_obra, urgencia
            FROM precios_base
            WHERE tipo_prenda=:tipo AND tela=:tela
        """),
        {
            "tipo": data["tipo_prenda"],
            "tela": data["tela"]
        }
    ).fetchone()

    if not result:
        return {"error": "No hay precio base"}, 404

    total = (result.mano_obra + result.urgencia) * data["cantidad"]

    return jsonify({
        "precio_estimado": total
    })
