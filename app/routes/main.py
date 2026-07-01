from flask import Blueprint, render_template

from app import STOCK_BAJO_UMBRAL, login_required
from app.models import Producto
from app.services.weather import obtener_clima

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def dashboard():
    productos = Producto.query.order_by(Producto.nombre).all()
    stock_bajo = [p for p in productos if p.stock <= STOCK_BAJO_UMBRAL]
    clima = obtener_clima()
    return render_template(
        "dashboard.html",
        productos=productos,
        stock_bajo=stock_bajo,
        clima=clima,
        umbral=STOCK_BAJO_UMBRAL,
    )
