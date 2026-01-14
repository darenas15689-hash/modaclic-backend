from flask import Blueprint
from flask_restful import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .talleres import TallerResource
from .usuarios import UsuarioResource
from .catalogo import ProductoResource
from .pedidos import PedidoResource
from .produccion import ProduccionResource
from .citas import CitaResource

api.add_resource(TallerResource, '/talleres')
api.add_resource(UsuarioResource, '/usuarios')
api.add_resource(ProductoResource, '/productos', '/productos/<int:id>')
api.add_resource(PedidoResource, '/pedidos', '/pedidos/<int:id>')
api.add_resource(ProduccionResource, '/produccion', '/produccion/<int:id>')
api.add_resource(CitaResource, '/citas', '/citas/<int:id>')

