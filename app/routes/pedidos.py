from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from app import db, login_required, login_required_api
from app.models import Cliente, Pedido, PedidoItem, Producto

bp = Blueprint("pedidos", __name__, url_prefix="/pedidos")


@bp.route("/")
@login_required
def listar():
    import json

    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template(
        "pedidos/listar.html",
        pedidos=pedidos,
        clientes_json=json.dumps([{"id": c.id, "nombre": c.nombre} for c in clientes]),
        productos_json=json.dumps(
            [{"id": p.id, "nombre": p.nombre, "stock": p.stock} for p in productos]
        ),
    )


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()

    if request.method == "POST":
        try:
            cliente_id = int(request.form.get("cliente_id"))
            producto_id = int(request.form.get("producto_id"))
            cantidad = int(request.form.get("cantidad"))
        except (TypeError, ValueError):
            flash("Datos invalidos.", "error")
            return render_template(
                "pedidos/form.html", clientes=clientes, productos=productos
            )

        if cantidad <= 0:
            flash("La cantidad debe ser mayor a cero.", "error")
            return render_template(
                "pedidos/form.html", clientes=clientes, productos=productos
            )

        cliente = Cliente.query.get(cliente_id)
        producto = Producto.query.get(producto_id)

        if not cliente or not producto:
            flash("Cliente o producto no encontrado.", "error")
            return render_template(
                "pedidos/form.html", clientes=clientes, productos=productos
            )

        if producto.stock < cantidad:
            flash("Stock insuficiente.", "error")
            return render_template(
                "pedidos/form.html", clientes=clientes, productos=productos
            )

        total = producto.precio * cantidad
        pedido = Pedido(cliente_id=cliente.id, total=total)
        item = PedidoItem(pedido=pedido, producto_id=producto.id, cantidad=cantidad)
        producto.stock -= cantidad

        try:
            db.session.add(pedido)
            db.session.add(item)
            db.session.commit()
            flash(f"Venta registrada. Total: ${total:.2f}", "success")
            return redirect(url_for("pedidos.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al registrar el pedido.", "error")

    return render_template("pedidos/form.html", clientes=clientes, productos=productos)


@bp.route("/<int:pedido_id>/eliminar", methods=["POST"])
@login_required
def eliminar(pedido_id):
    pedido = Pedido.query.get(pedido_id)
    if not pedido:
        flash("Pedido no encontrado.", "error")
        return redirect(url_for("pedidos.listar"))

    try:
        for item in pedido.items:
            if item.producto:
                item.producto.stock += item.cantidad
        db.session.delete(pedido)
        db.session.commit()
        flash("Pedido eliminado y stock restaurado.", "success")
    except Exception:
        db.session.rollback()
        flash("Error al eliminar el pedido.", "error")

    return redirect(url_for("pedidos.listar"))


@bp.route("/api/pedidos", methods=["POST"])
@login_required_api
def crear_async():
    data = request.get_json(silent=True) or {}

    try:
        cliente_id = int(data.get("cliente_id"))
        producto_id = int(data.get("producto_id"))
        cantidad = int(data.get("cantidad"))
    except (TypeError, ValueError):
        return jsonify({"error": "Datos invalidos."}), 400

    if cantidad <= 0:
        return jsonify({"error": "La cantidad debe ser mayor a cero."}), 400

    cliente = Cliente.query.get(cliente_id)
    producto = Producto.query.get(producto_id)

    if not cliente:
        return jsonify({"error": "Cliente no encontrado."}), 404
    if not producto:
        return jsonify({"error": "Producto no encontrado."}), 404
    if producto.stock < cantidad:
        return jsonify({"error": "Stock insuficiente."}), 400

    total = producto.precio * cantidad
    pedido = Pedido(cliente_id=cliente.id, total=total)
    item = PedidoItem(pedido=pedido, producto_id=producto.id, cantidad=cantidad)
    producto.stock -= cantidad

    try:
        db.session.add(pedido)
        db.session.add(item)
        db.session.commit()
        return jsonify(
            {
                "mensaje": "Pedido registrado.",
                "pedido": {
                    "id": pedido.id,
                    "total": pedido.total,
                    "cliente": cliente.nombre,
                    "producto": producto.nombre,
                    "cantidad": cantidad,
                    "stock_restante": producto.stock,
                },
            }
        ), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error al registrar el pedido."}), 500
