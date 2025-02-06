from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, send_file, current_app
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import Usuario, RegistroEgresado, Informacion, Carrera, Periodo
from app.forms import LoginForm, EgresadoForm, ConsultaForm
from werkzeug.security import check_password_hash
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PlatypusImage, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from PIL import Image
import io
import os
from app.utils import convertir_fecha_a_texto, numero_a_ordinal, numero_a_texto
import jwt
import datetime
from datetime import timedelta, datetime
from functools import wraps


bp = Blueprint('main', __name__)

# decorador para verificar token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 403
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
            current_user = Usuario.query.get(current_user_id)
            if not current_user:
                return jsonify({'error': 'Usuario no encontrado'}), 403
        except Exception as e:
            return jsonify({'error': str(e)}), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated


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

        # Generar el token JWT
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expira en 1 hora
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Usuario o contraseña incorrectos o acceso no permitido'}), 401

@bp.route('/api/protegido', methods=['GET'])
@token_required
def protegido(current_user):
    return jsonify({'message': 'Acceso permitido', 'user_id': current_user.id}), 200

@bp.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': 'Sesión cerrada'}), 200


@bp.route('/api/agregar', methods=['POST'])
@token_required
def agregar_egresado(current_user):
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
@token_required
def consultar_egresados(current_user):
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
@token_required
def get_username(current_user):
    return jsonify({'username': current_user.nombre}), 200


@bp.route('/api/eliminar/<int:id>', methods=['POST'])
@token_required
def eliminar(current_user, id):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    egresado = RegistroEgresado.query.get_or_404(id)
    db.session.delete(egresado)
    db.session.commit()
    return jsonify({'message': 'Egresado eliminado con éxito'}), 200


@bp.route('/api/consultar/<int:id>', methods=['GET'])
@token_required
def consultar_egresado(current_user, id):
    egresado = RegistroEgresado.query.get_or_404(id)
    return jsonify(egresado.to_dict())


@bp.route('/api/editar/<int:id>', methods=['POST'])
@token_required
def editar(current_user, id):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    egresado = RegistroEgresado.query.get_or_404(id)
    data = request.get_json()
    try:
        egresado.nombre = data['nombre']
        egresado.cedula = data['cedula']
        egresado.cod_carrera = data['cod_carrera']
        egresado.cod_periodo = data['cod_periodo']
        egresado.num_periodo = data['num_periodo']
        egresado.ag = data['ag']
        egresado.aa = data['aa']
        egresado.pg = data['pg']
        egresado.pa = data['pa']
        egresado.rendimiento = data['rendimiento']
        egresado.fecha_grado = data['fecha_grado']
        
        # Añade más campos según sea necesario
        db.session.commit()
        return jsonify({'message': 'Egresado editado con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# director y decano 

@bp.route('/api/informacion', methods=['GET'])
@token_required
def obtener_informacion(current_user):
    info = db.session.query(Informacion).first()
    data = {
        'director': info.director,
        'decano': info.decano,
        'can_edit': current_user.p_acesso == 1
    }
    return jsonify(data)


@bp.route('/api/actualizar_informacion', methods=['POST'])
@token_required
def actualizar_informacion(current_user):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    data = request.get_json()
    try:
        info = db.session.query(Informacion).first()
        info.director = data['director']
        info.decano = data['decano']
        db.session.commit()
        return jsonify({'message': 'Información actualizada con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/api/agregar_periodo', methods=['POST'])
@token_required
def agregar_periodo(current_user):
    if current_user.p_acesso != 1:
        return jsonify({'error': 'No tienes permiso para realizar esta acción.'}), 403
    data = request.get_json()
    try:
        cod_periodo = data['periodo'] + str(data['ano'])
        nuevo_periodo = Periodo(cod_periodo=cod_periodo, ano=data['ano'], periodo=data['periodo'])
        db.session.add(nuevo_periodo)
        db.session.commit()
        return jsonify({'message': 'Período agregado con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

##*********************************************************************************************************

#(listo) carta tipo 1: promedio PONDERADO APROBATORIO, posicion respecto a la promocion (puesto ponderado aprobatorio)
#(listo) carta tipo 2: promedio ARITMETICO APROBATORIO, posicion respecto a la promocion (puesto aritmetico aprobatorio)

#() carta tipo 3: promedio PONDERADO APROBATORIO, posicion respecto a la promocion, con rendimiento (puesto ponderado con eficiencia)
#() carta tipo 4: promedio ARITMETICO APROBATORIO, posicion respecto a la promocion, con rendimiento (puesto aritmetico con eficiencia)

#() carta tipo 5: promedio ARITMETICO GENERAL, posicion respecto a todos los graduados de la ESCUELA (puesto aritmetico general por escuela)
#() carta tipo 6: promedio ARITMETICO GENERAL, posicion respecto a todos los graduados en la FACULTAD (puesto aritmetico general en la facultad)


@bp.route('/api/generar-carta', methods=['GET'])
@login_required
def generar_carta():
    cedula = request.args.get('cedula')
    tipo_carta = request.args.get('tipoCarta')
    
    egresado = RegistroEgresado.query.filter_by(cedula=cedula).first()
    info = db.session.query(Informacion).first()
    carrera = db.session.query(Carrera).filter_by(cod_carrera=egresado.cod_carrera).first()
    periodo = db.session.query(Periodo).filter_by(cod_periodo=egresado.cod_periodo).first()
    usuario = current_user.nombre  # Obtener el nombre de usuario del usuario que imprimió la carta

    if not egresado or not info or not carrera or not periodo:
        return jsonify({'error': 'Datos no encontrados'}), 404

    # Obtener el grupo de promoción, escuela o facultad sengun la carta selecionada
    
    if tipo_carta == "carta_tipo_1": # trabaja con pa
        
        promocion = RegistroEgresado.query.filter_by(cod_carrera=egresado.cod_carrera, cod_periodo=egresado.cod_periodo).order_by(RegistroEgresado.pa.desc()).all()
        # Calcular las posiciones y el promedio de pa
        posiciones = {}
        posicion_actual = 1
        
        total_pa = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(promocion):
            pa_val = float(estudiante.pa)  # Convertir pa a número
            total_pa += pa_val
            if pa_val not in posiciones:
                posiciones[pa_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo pa
            posicion_actual += 1
        
        # Obtener la posición del egresado en la promoción
        posicion = posiciones.get(float(egresado.pa), None)  # Convertir pa a número
        pos_escrita = numero_a_ordinal(posicion) #escribir de forma ordinal
        # Número total de integrantes en la promoción
        total_integrantes = len(promocion)

        # Calcular el promedio de pa
        promedio_promo = total_pa / total_integrantes if total_integrantes > 0 else 0
            
    
    elif tipo_carta == "carta_tipo_2": # trabaja con aa
        promocion = RegistroEgresado.query.filter_by(cod_carrera=egresado.cod_carrera, cod_periodo=egresado.cod_periodo).order_by(RegistroEgresado.aa.desc()).all()
        # Calcular las posiciones y el promedio de aa
        posiciones = {}
        posicion_actual = 1
        
        total_aa = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(promocion):
            aa_val = float(estudiante.aa)  # Convertir pa a número
            total_aa += aa_val
            if aa_val not in posiciones:
                posiciones[aa_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo pa
            posicion_actual += 1
        
        # Obtener la posición del egresado en la promoción
        posicion = posiciones.get(float(egresado.aa), None)  # Convertir pa a número
        pos_escrita = numero_a_ordinal(posicion)

        # Número total de integrantes en la promoción
        total_integrantes = len(promocion)
        
        # Calcular el promedio de aa
        promedio_promo = total_aa / total_integrantes if total_integrantes > 0 else 0
        
        
    elif tipo_carta == "carta_tipo_3": #trabaja con pa y rendimiento 
        
        promocion = RegistroEgresado.query.filter_by(cod_carrera=egresado.cod_carrera, cod_periodo=egresado.cod_periodo).order_by(RegistroEgresado.pa.desc()).all()
        # Calcular las posiciones y el promedio de pa
        posiciones = {}
        posicion_actual = 1
        
        total_pa = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(promocion):
            pa_val = float(estudiante.pa)  # Convertir pa a número
            total_pa += pa_val
            if pa_val not in posiciones:
                posiciones[pa_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo pa
            posicion_actual += 1
        
        # Obtener la posición del egresado en la promoción
        posicion = posiciones.get(float(egresado.pa), None)  # Convertir pa a número
        pos_escrita = numero_a_ordinal(posicion)

        # Número total de integrantes en la promoción
        total_integrantes = len(promocion)

        # Calcular el promedio de pa
        promedio_promo = total_pa / total_integrantes if total_integrantes > 0 else 0
        
        
    elif tipo_carta == "carta_tipo_4":
        
        promocion = RegistroEgresado.query.filter_by(cod_carrera=egresado.cod_carrera, cod_periodo=egresado.cod_periodo).order_by(RegistroEgresado.aa.desc()).all()
        # Calcular las posiciones y el promedio de aa
        posiciones = {}
        posicion_actual = 1
        
        total_aa = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(promocion):
            aa_val = float(estudiante.aa)  # Convertir pa a número
            total_aa += aa_val
            if aa_val not in posiciones:
                posiciones[aa_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo pa
            posicion_actual += 1
        
        # Obtener la posición del egresado en la promoción
        posicion = posiciones.get(float(egresado.aa), None)  # Convertir pa a número
        pos_escrita = numero_a_ordinal(posicion)

        # Número total de integrantes en la promoción
        total_integrantes = len(promocion)
        
        # Calcular el promedio de aa
        promedio_promo = total_aa / total_integrantes if total_integrantes > 0 else 0

    elif tipo_carta == "carta_tipo_5":  # trabaja con ag y cod_carrera
        egresados_carrera = RegistroEgresado.query.filter_by(cod_carrera=egresado.cod_carrera).order_by(RegistroEgresado.ag.desc()).all()
        # Calcular las posiciones y el promedio de ag
        posiciones = {}
        posicion_actual = 1
            
        total_ag = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(egresados_carrera):
            ag_val = float(estudiante.ag)  # Convertir pa a número
            total_ag += ag_val
            if ag_val not in posiciones:
                posiciones[ag_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo pa
            posicion_actual += 1
            
        # Obtener la posición del egresado en la carrera
        posicion = posiciones.get(float(egresado.ag), None)  # Convertir pa a número
        pos_escrita = numero_a_texto(posicion)
        
        # Número total de integrantes en la carrera
        total_integrantes = len(egresados_carrera)

        # Calcular el promedio de pa
        promedio_promo = total_ag / total_integrantes if total_integrantes > 0 else 0

    elif tipo_carta == "carta_tipo_6":  # trabaja con ag y todos los graduados en la facultad
        egresados_facultad = RegistroEgresado.query.order_by(RegistroEgresado.ag.desc()).all()
        # Calcular las posiciones y el promedio de aa
        posiciones = {}
        posicion_actual = 1

        total_ag = 0.0  # Asegurarnos de que el total es un número
        for index, estudiante in enumerate(egresados_facultad):
            ag_val = float(estudiante.aa)  # Convertir aa a número
            total_ag += ag_val
            if ag_val not in posiciones:
                posiciones[ag_val] = posicion_actual
            else:
                posicion_actual -= 1  # Mantener la misma posición para los estudiantes con el mismo aa
            posicion_actual += 1

        # Obtener la posición del egresado en la facultad
        posicion = posiciones.get(float(egresado.ag), None)  # Convertir aa a número
        pos_escrita = numero_a_texto(posicion)

        # Número total de integrantes en la facultad
        total_integrantes = len(egresados_facultad)

        # Calcular el promedio de aa
        promedio_promo = total_ag / total_integrantes if total_integrantes > 0 else 0

    # Obtener la fecha actual en formato texto
    fecha_actual = datetime.now()
    fecha_actual_texto = convertir_fecha_a_texto(fecha_actual)

    # Verificar que las claves existen en `egresado`
    required_keys = ['nombre', 'cedula', 'rendimiento', 'fecha_grado', 'ag', 'aa', 'pg', 'pa', 'cod_carrera', 'cod_periodo']
    if not all([getattr(egresado, key, None) for key in required_keys]):
        return jsonify({'error': 'Datos incompletos del egresado'}), 404

    # Leer la plantilla de la carta
    template_path = os.path.join('app', 'templates', 'letters', f'{tipo_carta}.txt')
    if not os.path.exists(template_path):
        return jsonify({'error': 'Tipo de carta no encontrado'}), 404

    content = read_template(template_path)
    content = content.format(
        nombre=egresado.nombre,
        cedula=egresado.cedula,
        rendimiento=egresado.rendimiento,
        aritmeticoaprobatorio=egresado.aa,
        aritmetico_general=egresado.ag,
        ponderadoaprobatorio=egresado.pa,
        frecha_grado=egresado.fecha_grado,
        cod_periodo=f"{periodo.periodo} del año {periodo.ano}",  # Usar el año y el período
        cod_carrera=carrera.nombre,  # Usar el nombre de la carrera
        posicion=posicion,  # Posición en la promoción, escuela o facultad
        pos_escrita=pos_escrita, #posicion escrita de forma ordinal
        total_integrantes=total_integrantes,  # Total de integrantes en la promoción
        promedio_promo=promedio_promo,  # Promedio de pa en la promoción
        director=info.director,
        decano=info.decano,
        fecha_actual_texto=fecha_actual_texto  # Fecha actual en texto
    )

    # Crear el PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=inch * 0.75, leftMargin=inch * 0.75,
                            topMargin=inch * 0.75, bottomMargin=inch * 0.75)
    elements = []

    # Estilos de párrafo
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=18, fontSize=14, fontName='Times-Roman'))
    styles.add(ParagraphStyle(name='Centered', alignment=TA_CENTER, fontSize=22, spaceAfter=20, fontName='Times-Roman'))

    # Membrete
    base_path = os.path.dirname(os.path.abspath(__file__))
    membrete_path = os.path.join(base_path, 'static', 'img', 'membrete.png')

    # Verificar si el archivo existe y es accesible
    if os.path.exists(membrete_path):
        elements.append(PlatypusImage(membrete_path, width=doc.width, height=85))
        elements.append(Spacer(1, 36))  # Aumentar el espacio entre el membrete y el título

    # Título
    elements.append(Paragraph("CONSTANCIA", styles['Centered']))

    # Contenido justificado
    for line in content.split('\n'):
        elements.append(Paragraph(line, styles['Justify']))
        elements.append(Spacer(1, 12))

    # Tabla para Decano y Director
    table_data = [
        [
            Paragraph(f"<b>{info.decano}</b>", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=12, fontName='Times-Roman')),
            Paragraph(f"<b>{info.director}</b>", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=12, fontName='Times-Roman'))
        ],
        [
            Paragraph("Decano - Facultad de Ingeniería", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=10, fontName='Times-Roman')),
            Paragraph("Director - OREFI", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=10, fontName='Times-Roman'))
        ]
    ]
    table = Table(table_data, colWidths=[doc.width / 2.0] * 2)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 36))  # Espacio antes del pie de página

    # Agregar el usuario que imprimió la carta
    elements.append(Paragraph(f"Impreso por: {usuario}", styles['Justify']))

    doc.build(elements)

    buffer.seek(0)
    return send_file(buffer, as_attachment=False, mimetype='application/pdf')

def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()

##****************************************************************************************************
# lista 1: Puestos de promocion por el promedio ponderado aprobatorio (pa) 
# lista 2: Puestos de promocion por el promedio aritmetico aprobatorio (aa)
# lista 3: Listado alfabetico


@bp.route('/api/carreras', methods=['GET'])
@login_required
def obtener_carreras():
    carreras = Carrera.query.all()
    return jsonify([carrera.to_dict() for carrera in carreras])

@bp.route('/api/periodos', methods=['GET'])
@login_required
def obtener_periodos():
    periodos_permitidos = ['A', 'B', 'U', 'E', 'I']
    periodos = Periodo.query.filter(Periodo.periodo.in_(periodos_permitidos)).all()
    return jsonify([periodo.to_dict() for periodo in periodos])

@bp.route('/api/listado-promocion', methods=['GET'])
@login_required
def listado_promocion():
    codigo_carrera = request.args.get('codigo_carrera')
    codigo_periodo = request.args.get('codigo_periodo')

    if not codigo_carrera or not codigo_periodo:
        return jsonify({'error': 'Faltan datos'}), 400

    egresados = RegistroEgresado.query.filter_by(cod_carrera=codigo_carrera, cod_periodo=codigo_periodo).order_by(RegistroEgresado.pa.desc()).all()

    if not egresados:
        return jsonify({'error': 'No se encontraron egresados'}), 404

    return jsonify([e.to_dict() for e in egresados])

@bp.route('/api/generar-listado-promocion', methods=['GET'])
@login_required
def generar_listado_promocion():
    codigo_carrera = request.args.get('codigo_carrera')
    codigo_periodo = request.args.get('codigo_periodo')
    tipo_lista = request.args.get('tipo_lista')  # Obtener el tipo de lista

    if not codigo_carrera or not codigo_periodo or not tipo_lista:
        return jsonify({'error': 'Faltan datos'}), 400

    if tipo_lista == "tipo1":
        orden = RegistroEgresado.pa.desc()
        campo = "pa"
        titulo = "Cuadro de Promoción por el Promedio Ponderado"
    elif tipo_lista == "tipo2":
        orden = RegistroEgresado.aa.desc()
        campo = "aa"
        titulo = "Cuadro de Promoción por el Promedio Aritmético"
    elif tipo_lista == "tipo3":
        orden = RegistroEgresado.nombre.asc()
        titulo = "Cuadro de Promoción en Orden Alfabético"
    else:
        return jsonify({'error': 'Tipo de lista no válido'}), 400

    egresados = RegistroEgresado.query.filter_by(cod_carrera=codigo_carrera, cod_periodo=codigo_periodo).order_by(orden).all()
    info = db.session.query(Informacion).first()
    carrera = db.session.query(Carrera).filter_by(cod_carrera=codigo_carrera).first()

    if not egresados:
        return jsonify({'error': 'No se encontraron egresados'}), 404

    # Calcular el promedio general
    if tipo_lista != "tipo3":
        total_campo = sum(float(getattr(egresado, campo)) for egresado in egresados)
        promedio_general = total_campo / len(egresados) if egresados else 0

    # Crear el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 50  # Margen para ambos lados

    # Cargar el membrete utilizando ruta absoluta
    base_path = os.path.dirname(os.path.abspath(__file__))
    membrete_path = os.path.join(base_path, 'static', 'img', 'membrete.png')

    # Ajustar el tamaño del membrete para ocupar todo el ancho
    membrete_height = 85  # Ajusta la altura del membrete según sea necesario
    membrete_width = width - 2 * margin  # Aumenta el ancho del membrete para ocupar casi todo el ancho de la página

    # Verificar si el archivo existe y es accesible
    try:
        img_membrete = Image.open(membrete_path)
    except Exception as e:
        return jsonify({'error': f'Error al abrir la imagen del membrete: {str(e)}'}), 500

    try:
        c.drawImage(membrete_path, margin, height - 100, width=membrete_width, height=membrete_height, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        return jsonify({'error': f'Error al cargar la imagen del membrete en el PDF: {str(e)}'}), 500

    # Configurar el encabezado del listado
    c.setFont("Helvetica-Bold", 14)
    # Título de la lista
    c.drawString(margin + 50, height - 150, f"EGRESADOS       {codigo_periodo}              {carrera.nombre}")

    # Líneas horizontales al principio de la lista
    c.line(margin, height - 180, width - margin, height - 180)

    # Configurar la tabla con los datos
    y = height - 200  # Posición inicial
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(margin + 25, y, "SECUENCIA")
    c.drawCentredString(margin + 85, y, "CÉDULA")
    c.drawString(margin + 160, y, "APELLIDO Y NOMBRE")
    if tipo_lista != "tipo3":
        c.drawCentredString(margin + 370, y, "PROMEDIO")
        c.drawCentredString(margin + 440, y, "LUGAR")
    y -= 15

    c.setFont("Helvetica", 10)

    if tipo_lista == "tipo3":
        # Lista ordenada alfabéticamente por nombre, sin promedio ni lugar
        for idx, egresado in enumerate(egresados, start=1):
            c.drawCentredString(margin + 25, y, str(idx))
            c.drawCentredString(margin + 85, y, egresado.cedula)
            c.drawString(margin + 160, y, egresado.nombre)
            y -= 15
            if y < 50:  # Salto de página si se llena
                c.showPage()
                y = height - 50
    else:
        # Calcular posiciones con empate y ajustar la secuencia correctamente
        posicion_actual = 1
        posiciones = {}
        for idx, egresado in enumerate(egresados):
            valor_campo = float(getattr(egresado, campo))
            if valor_campo not in posiciones:
                posiciones[valor_campo] = posicion_actual
                posicion_actual += 1

        secuencia_actual = 1
        for idx, egresado in enumerate(egresados):
            valor_campo = float(getattr(egresado, campo))
            if idx > 0 and valor_campo != float(getattr(egresados[idx-1], campo)):
                secuencia_actual += 1

            c.drawCentredString(margin + 25, y, str(secuencia_actual))
            c.drawCentredString(margin + 85, y, egresado.cedula)
            c.drawString(margin + 160, y, egresado.nombre)
            if tipo_lista != "tipo3":
                c.drawCentredString(margin + 370, y, str(valor_campo))
            c.drawCentredString(margin + 440, y, str(posiciones[valor_campo]))
            y -= 15
            if y < 50:  # Salto de página si se llena
                c.showPage()
                y = height - 50

    # Añadir un pequeño espacio después del último egresado
    y -= 10

    # Líneas horizontales al final de la lista
    c.line(margin, y, width - margin, y)

    # Añadir el promedio general, nombres del decano y director
    if tipo_lista != "tipo3":
        c.setFont("Helvetica", 10)
        c.drawString(width - margin - 200, y - 20, f"PROMEDIO GENERAL: {promedio_general:.3f}")

    c.drawString(margin + 10, y - 50, f"{info.director}")
    c.drawString(margin + 10, y - 70, "Director(a) - OREFI")
    c.drawString(margin + 10, y - 110, f"{info.decano}")
    c.drawString(margin + 10, y - 130, "Decano - Facultad de Ingeniería")
    c.drawString(margin + 10, y - 170, titulo)

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=False, mimetype='application/pdf', download_name="Listado_Promocion.pdf")
