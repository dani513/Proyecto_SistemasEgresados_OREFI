from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import Usuario, RegistroEgresado, Informacion
from app.forms import LoginForm, EgresadoForm, ConsultaForm
from werkzeug.security import check_password_hash
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
import io
import os


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = Usuario.query.filter_by(nombre=username).first()
    
    if user and user.check_password(password):
        login_user(user)  # Autenticar al usuario
        session['user_id'] = user.id
        return jsonify({'message': 'Inicio de sesión exitoso'}), 200
    else:
        return jsonify({'error': 'Usuario o contraseña incorrectos o acceso no permitido'}), 401


@bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': 'Sesión cerrada'}), 200


@bp.route('/api/agregar', methods=['POST'])
@login_required
def agregar_egresado():
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403

    data = request.get_json()
    print(data)  # Mensaje de depuración para ver los datos recibidos
    try:
        egresado = RegistroEgresado(
            ag=data['ag'],
            aa=data['aa'],
            pg=data['pg'],
            pa=data['pa'],
            rendimiento=data['rendimiento'],
            fecha_grado=data['fecha_grado'],
            cod_carrera=data['cod_carrera'],
            cod_periodo=data['cod_periodo'],
            num_periodo=data['num_periodo'],
            cedula=data['cedula'],
            nombre=data['nombre']
        )
        db.session.add(egresado)
        db.session.commit()
        return jsonify({'message': 'Egresado agregado con éxito'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/consultar', methods=['GET'])
@login_required
def consultar_egresados():
    codigo_carrera = request.args.get('codigo_carrera')
    cedula = request.args.get('cedula')
    nombre = request.args.get('nombre')
    codigo_periodo = request.args.get('codigo_periodo')

    query = RegistroEgresado.query

    if codigo_carrera:
        query = query.filter_by(cod_carrera=codigo_carrera)  # Asegurarse de usar 'cod_carrera'
    if cedula:
        query = query.filter_by(cedula=cedula)
    if nombre:
        query = query.filter(RegistroEgresado.nombre.ilike(f'%{nombre}%'))
    if codigo_periodo:
        query = query.filter_by(cod_periodo=codigo_periodo)  # Asegurarse de usar 'cod_periodo'

    egresados = query.all()

    return jsonify([e.to_dict() for e in egresados])

@bp.route('/api/get-username', methods=['GET'])
@login_required
def get_username():
    return jsonify({'username': current_user.nombre}), 200


@bp.route('/api/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    egresado = RegistroEgresado.query.get_or_404(id)
    db.session.delete(egresado)
    db.session.commit()
    return jsonify({'message': 'Egresado eliminado con éxito'}), 200

@bp.route('/api/consultar/<int:id>', methods=['GET'])
@login_required
def consultar_egresado(id):
    egresado = RegistroEgresado.query.get_or_404(id)
    return jsonify(egresado.to_dict())

@bp.route('/api/editar/<int:id>', methods=['POST'])
@login_required
def editar(id):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    egresado = RegistroEgresado.query.get_or_404(id)
    data = request.get_json()
    try:
        egresado.nombre = data['nombre']
        egresado.cedula = data['cedula']
        egresado.cod_carrera = data['cod_carrera']
        egresado.cod_periodo = data['cod_periodo']
        # Añade más campos según sea necesario
        db.session.commit()
        return jsonify({'message': 'Egresado editado con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
# director  y de decano 

@bp.route('/api/informacion', methods=['GET'])
@login_required
def obtener_informacion():
    info = db.session.query(Informacion).first()
    data = {
        'director': info.director,
        'decano': info.decano,
        'can_edit': current_user.p_acesso == 1
    }
    return jsonify(data)

@bp.route('/api/actualizar_informacion', methods=['POST'])
@login_required
def actualizar_informacion():
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    data = request.get_json()
    try:
        info = db.session.query(Informacion).first()
        info.director_ = data['director']
        info.decano = data['decano']
        db.session.commit()
        return jsonify({'message': 'Información actualizada con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

@bp.route('/api/generar-carta', methods=['GET'])
@login_required
def generar_carta():
    cedula = request.args.get('cedula')
    tipo_carta = request.args.get('tipoCarta')
    
    egresado = RegistroEgresado.query.filter_by(cedula=cedula).first()
    info = db.session.query(Informacion).first()

    if not egresado or not info:
        return jsonify({'error': 'Datos no encontrados'}), 404
    
    # Leer la plantilla de la carta
    template_path = f'templates/letters/{tipo_carta}.txt'
    if not os.path.exists(template_path):
        return jsonify({'error': 'Tipo de carta no encontrado'}), 404

    content = read_template(template_path)
    content = content.format(
        nombre=egresado.nombre,
        director=info.director,
        decano=info.decano
    )

    # Crear el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 100  # Ajustar la posición inicial

    for line in content.split('\n'):
        c.drawString(100, y, line)
        y -= 20

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=False, mimetype='application/pdf')
