from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class CambioNumerico(db.Model):
    numero = db.Column(db.Integer, primary_key=True, default=9)
    cadena = db.Column(db.String(255))

class Carrera(db.Model):
    cod_carrera = db.Column(db.Integer, primary_key=True, default=0)
    nombre = db.Column(db.String(50))

class EstadoPeriodo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_periodo = db.Column(db.String(5), nullable=False)
    cod_carrera = db.Column(db.String(50), nullable=False)
    cod_estado = db.Column(db.String(7), nullable=False)

class Informacion(db.Model):
    director = db.Column(db.String(50), primary_key=True, nullable=False)
    decano = db.Column(db.String(50), nullable=False)

class IP(db.Model):
    num_ip = db.Column(db.String(20), primary_key=True, nullable=False, default='')
    desc = db.Column(db.String(100))

class Periodo(db.Model):
    cod_periodo = db.Column(db.String(5), primary_key=True, nullable=False, default='')
    ano = db.Column(db.Integer)
    periodo = db.Column(db.String(1))

from app import db


class RegistroEgresado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ag = db.Column(db.String(10))
    aa = db.Column(db.String(10))
    pg = db.Column(db.String(10))
    pa = db.Column(db.String(10))
    rendimiento = db.Column(db.Float)
    fecha_grado = db.Column(db.Date)
    cod_carrera = db.Column(db.String(10))
    cod_periodo = db.Column(db.String(10))
    num_periodo = db.Column(db.String(10))
    cedula = db.Column(db.String(20))
    nombre = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'ag': self.ag,
            'aa': self.aa,
            'pg': self.pg,
            'pa': self.pa,
            'rendimiento': self.rendimiento,
            'fecha_grado': self.fecha_grado,
            'cod_carrera': self.cod_carrera,
            'cod_periodo': self.cod_periodo,
            'num_periodo': self.num_periodo,
            'cedula': self.cedula,
            'nombre': self.nombre
        }



class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(25), nullable=False, unique=True)
    clave = db.Column(db.String(128))
    p_acesso = db.Column(db.Integer)

    def set_password(self, password):
        self.clave = password

    def check_password(self, password):
        return self.clave == password

    # Métodos requeridos por Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

