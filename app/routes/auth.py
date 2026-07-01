from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import check_password, db, login_required
from app.models import Usuario

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and check_password(password, usuario.password_hash):
            session["user_id"] = usuario.id
            session["username"] = usuario.username
            flash("Sesion iniciada correctamente.", "success")
            return redirect(url_for("main.dashboard"))

        flash("Usuario o contrasena incorrectos.", "error")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Sesion cerrada.", "info")
    return redirect(url_for("auth.login"))
