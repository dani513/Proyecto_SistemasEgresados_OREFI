from app import create_app, db
from app.models import CambioNumerico, Carrera, EstadoPeriodo, Informacion, IP, Periodo, RegistroEgresado, Usuario
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
