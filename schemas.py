from extensions import ma
from models import *

class TallerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Taller

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario

class ProductoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Producto

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido

class CitaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cita
from marshmallow import Schema, fields

class UsuarioSchema(Schema):
    id = fields.Int(dump_only=True)
    usuario = fields.Str(required=True)
    password = fields.Str(required=True)
    rol = fields.Str(required=True)
