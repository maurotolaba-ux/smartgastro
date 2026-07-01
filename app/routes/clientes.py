from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db, login_required
from app.models import Cliente

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@bp.route("/")
@login_required
def listar():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    return render_template("clientes/listar.html", clientes=clientes)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()

        if not nombre or not telefono:
            flash("Nombre y telefono son obligatorios.", "error")
            return render_template("clientes/form.html", cliente=None)

        cliente = Cliente(nombre=nombre, telefono=telefono)
        try:
            db.session.add(cliente)
            db.session.commit()
            flash("Cliente creado correctamente.", "success")
            return redirect(url_for("clientes.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al crear el cliente.", "error")

    return render_template("clientes/form.html", cliente=None)


@bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente no encontrado.", "error")
        return redirect(url_for("clientes.listar"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()

        if not nombre or not telefono:
            flash("Nombre y telefono son obligatorios.", "error")
            return render_template("clientes/form.html", cliente=cliente)

        cliente.nombre = nombre
        cliente.telefono = telefono

        try:
            db.session.commit()
            flash("Cliente actualizado.", "success")
            return redirect(url_for("clientes.listar"))
        except Exception:
            db.session.rollback()
            flash("Error al actualizar el cliente.", "error")

    return render_template("clientes/form.html", cliente=cliente)


@bp.route("/<int:cliente_id>/eliminar", methods=["POST"])
@login_required
def eliminar(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        flash("Cliente no encontrado.", "error")
        return redirect(url_for("clientes.listar"))

    if cliente.pedidos:
        flash("No se puede eliminar: el cliente tiene pedidos asociados.", "error")
        return redirect(url_for("clientes.listar"))

    try:
        db.session.delete(cliente)
        db.session.commit()
        flash("Cliente eliminado.", "success")
    except Exception:
        db.session.rollback()
        flash("Error al eliminar el cliente.", "error")

    return redirect(url_for("clientes.listar"))
