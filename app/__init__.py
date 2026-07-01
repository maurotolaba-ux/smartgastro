import os
from functools import wraps

import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

STOCK_BAJO_UMBRAL = 5


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///smartgastro.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import api, auth, clientes, main, pedidos, productos

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(productos.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(pedidos.bp)
    app.register_blueprint(api.bp)

    with app.app_context():
        db.create_all()
        _seed_default_user()

    return app


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def login_required_api(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "No autorizado."}), 401
        return view(*args, **kwargs)

    return wrapped


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def _seed_default_user():
    from app.models import Usuario

    if Usuario.query.filter_by(username="admin").first() is None:
        admin = Usuario(
            username="admin",
            password_hash=hash_password("profe123"),
        )
        try:
            db.session.add(admin)
            db.session.commit()
        except Exception:
            db.session.rollback()
