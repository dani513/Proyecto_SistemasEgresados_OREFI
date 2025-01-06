from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import Usuario, RegistroEgresado
from app.forms import LoginForm, EgresadoForm, ConsultaForm
from werkzeug.security import check_password_hash


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



@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    if current_user.p_acesso != 1:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.index'))
    egresado = RegistroEgresado.query.get_or_404(id)
    form = EgresadoForm(obj=egresado)
    if form.validate_on_submit():
        form.populate_obj(egresado)
        db.session.commit()
        flash('Egresado editado con éxito')
        return redirect(url_for('main.editar', id=id))
    return render_template('editar.html', form=form, egresado=egresado)

@bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    if current_user.p_acesso != 1:
        flash('No tienes permiso para realizar esta acción.')
        return redirect(url_for('main.index'))
    egresado = RegistroEgresado.query.get_or_404(id)
    db.session.delete(egresado)
    db.session.commit()
    flash('Egresado eliminado con éxito')
    return redirect(url_for('main.index'))


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



