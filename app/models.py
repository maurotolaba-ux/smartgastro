from datetime import datetime, timezone

from app import db


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)

    pedidos = db.relationship("Pedido", back_populates="cliente", lazy=True)


class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    items = db.relationship("PedidoItem", back_populates="producto", lazy=True)


class Pedido(db.Model):
    __tablename__ = "pedidos"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    total = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.String(30), nullable=False, default="Pendiente")
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="pedidos")
    items = db.relationship(
        "PedidoItem", back_populates="pedido", lazy=True, cascade="all, delete-orphan"
    )


class PedidoItem(db.Model):
    __tablename__ = "pedido_items"

    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)

    pedido = db.relationship("Pedido", back_populates="items")
    producto = db.relationship("Producto", back_populates="items")
