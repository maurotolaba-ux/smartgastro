# SmartGastro Web

Aplicacion web para gestion de foodtrucks. Evolucion del Trabajo Practico I (consola) a una app Flask con persistencia, autenticacion e integracion con API de clima.

**Integrante:** Mauro Jonathan Brian Tolaba  
**Comision:** ACN4AP

## Funcionalidades

- Login con sesiones y contrasenas hasheadas (bcrypt)
- CRUD de productos, clientes y pedidos/ventas
- Descuento automatico de stock al registrar ventas
- Alertas de stock bajo en el dashboard
- Integracion con OpenWeatherMap (alerta de lluvia en Buenos Aires)
- Operaciones async con `fetch()` (alta/eliminacion de productos y registro de ventas)

## Requisitos

- Python 3.10+
- Cuenta gratuita en [OpenWeatherMap](https://openweathermap.org/api) para la API key

## Instalacion

1. Clonar el repositorio y entrar a la carpeta:

```bash
git clone https://github.com/maurotolaba-ux/smartgastro.git
cd smartgastro
```

2. Crear entorno virtual e instalar dependencias:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. Copiar variables de entorno:

```bash
copy .env.example .env
```

4. Editar `.env` y colocar tu `OPENWEATHER_API_KEY` y una `SECRET_KEY` propia.

5. Ejecutar la aplicacion:

```bash
python run.py
```

6. Abrir en el navegador: `http://127.0.0.1:5000`

## Credenciales de prueba

| Usuario | Contrasena |
|---------|------------|
| admin   | profe123   |

## Endpoints API (requieren sesion activa)

| Metodo | URL | Descripcion |
|--------|-----|-------------|
| POST   | `/api/productos` | Crear producto |
| DELETE | `/api/productos/<id>` | Eliminar producto |
| POST   | `/pedidos/api/pedidos` | Registrar venta |
| GET    | `/api/clima` | Consultar clima |

## Estructura del proyecto

```
smartgastro/
├── app/
│   ├── models.py          # Usuario, Cliente, Producto, Pedido, PedidoItem
│   ├── routes/            # Blueprints web y API
│   ├── services/weather.py
│   ├── static/css/
│   └── templates/
├── legacy/smartgastro.py  # Version consola (TP I)
├── run.py
├── requirements.txt
└── .env.example
```

## Version consola (TP I)

```bash
python legacy/smartgastro.py
```
