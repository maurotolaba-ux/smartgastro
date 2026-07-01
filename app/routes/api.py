from flask import Blueprint, jsonify, request

from app import db, login_required_api
from app.models import Producto

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/productos", methods=["POST"])
@login_required_api
def crear_producto():
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()

    try:
        precio = float(data.get("precio", 0))
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Precio o stock invalido."}), 400

    if not nombre or precio <= 0 or stock < 0:
        return jsonify({"error": "Datos invalidos."}), 400

    existente = Producto.query.filter_by(nombre=nombre).first()
    if existente:
        existente.stock += stock
        try:
            db.session.commit()
            return jsonify(
                {
                    "mensaje": "Producto existente, se sumo stock.",
                    "producto": _producto_dict(existente),
                }
            ), 200
        except Exception:
            db.session.rollback()
            return jsonify({"error": "Error al actualizar stock."}), 500

    producto = Producto(nombre=nombre, precio=precio, stock=stock)
    try:
        db.session.add(producto)
        db.session.commit()
        return jsonify(
            {"mensaje": "Producto creado.", "producto": _producto_dict(producto)}
        ), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al crear el producto."}), 500


@bp.route("/productos/<int:producto_id>", methods=["DELETE"])
@login_required_api
def eliminar_producto(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404

    try:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"mensaje": "Producto eliminado."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar el producto."}), 500


@bp.route("/clima", methods=["GET"])
@login_required_api
def clima():
    from app.services.weather import obtener_clima

    resultado = obtener_clima()
    if not resultado.get("ok"):
        return jsonify(resultado), 502
    return jsonify(resultado), 200


def _producto_dict(producto):
    return {
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": producto.precio,
        "stock": producto.stock,
    }
