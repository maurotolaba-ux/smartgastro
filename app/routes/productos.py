from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db, login_required
from app.models import Producto

bp = Blueprint("productos", __name__, url_prefix="/productos")


@bp.route("/")
@login_required
def listar():
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template("productos/listar.html", productos=productos)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            precio = float(request.form.get("precio", 0))
            stock = int(request.form.get("stock", 0))
        except ValueError:
            flash("Precio o stock invalido.", "error")
            return render_template("productos/form.html", producto=None)

        if not nombre or precio <= 0 or stock < 0:
            flash("Datos invalidos.", "error")
            return render_template("productos/form.html", producto=None)

        existente = Producto.query.filter_by(nombre=nombre).first()
        if existente:
            existente.stock += stock
            try:
                db.session.commit()
                flash("Producto existente, se sumo stock.", "success")
                return redirect(url_for("productos.listar"))
            except Exception:
                db.session.rollback()
                flash("Error al actualizar stock.", "error")
                return render_template("productos/form.html", producto=None)

        producto = Producto(nombre=nombre, precio=precio, stock=stock)
        try:
            db.session.add(producto)
            db.session.commit()
            flash("Producto creado.", "success")
            return redirect(url_for("productos.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al crear el producto.", "error")

    return render_template("productos/form.html", producto=None)


@bp.route("/<int:producto_id>/editar", methods=["GET", "POST"])
@login_required
def editar(producto_id):
    producto = Producto.query.get(producto_id)
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos.listar"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        try:
            precio = float(request.form.get("precio", 0))
            stock = int(request.form.get("stock", 0))
        except ValueError:
            flash("Precio o stock invalido.", "error")
            return render_template("productos/form.html", producto=producto)

        if not nombre or precio <= 0 or stock < 0:
            flash("Datos invalidos.", "error")
            return render_template("productos/form.html", producto=producto)

        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock

        try:
            db.session.commit()
            flash("Producto actualizado.", "success")
            return redirect(url_for("productos.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al actualizar el producto.", "error")

    return render_template("productos/form.html", producto=producto)
