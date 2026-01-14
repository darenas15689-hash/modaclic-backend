from extensions import db
from datetime import datetime

class Taller(db.Model):
    __tablename__ = 'talleres'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    taller_id = db.Column(db.Integer, db.ForeignKey('talleres.id'))

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    taller_id = db.Column(db.Integer)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Float)
    activo = db.Column(db.Boolean, default=True)
    categoria_id = db.Column(db.Integer)
    taller_id = db.Column(db.Integer)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    estado = db.Column(db.String(50))
    total = db.Column(db.Float)

    # ✅ NUEVOS CAMPOS NECESARIOS
    producto = db.Column(db.String(100))
    tipo_prenda = db.Column(db.String(20))
    talla = db.Column(db.String(10))
    color = db.Column(db.String(10))
    medidas_personalizadas = db.Column(db.Text)

    taller_id = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)


class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    responsable = db.Column(db.String(100))
    fecha_estimada = db.Column(db.Date)

class Servicio(db.Model):
    __tablename__ = 'servicios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    taller_id = db.Column(db.Integer)

class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100))
    fecha = db.Column(db.DateTime)
    servicio_id = db.Column(db.Integer)
    asesor = db.Column(db.String(100))
    taller_id = db.Column(db.Integer)
