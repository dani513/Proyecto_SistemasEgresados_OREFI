from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session, send_file
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
import datetime
from app.utils import convertir_fecha_a_texto


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
        info.director = data['director']
        info.decano = data['decano']
        db.session.commit()
        return jsonify({'message': 'Información actualizada con éxito'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()
##*********************************************************************************************************


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

    # Obtener el grupo de promoción
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
    
    # Número total de integrantes en la promoción
    total_integrantes = len(promocion)
    
    # Calcular el promedio de pa
    promedio_pa = total_pa / total_integrantes if total_integrantes > 0 else 0
    
    # Obtener la fecha actual en formato texto
    fecha_actual = datetime.datetime.now()
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
        ponderadoaprobatorio=egresado.pa,
        frecha_grado=egresado.fecha_grado,
        cod_periodo=f"{periodo.periodo} del año {periodo.ano}",  # Usar el año y el período
        cod_carrera=carrera.nombre,  # Usar el nombre de la carrera
        posicion=posicion,  # Posición en la promoción
        total_integrantes=total_integrantes,  # Total de integrantes en la promoción
        promedio_pa=promedio_pa,  # Promedio de pa en la promoción
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
            Paragraph(f"<b>{info.decano}</b>", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=10, fontName='Times-Roman')),
            Paragraph(f"<b>{info.director}</b>", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=10, fontName='Times-Roman'))
        ],
        [
            Paragraph("Decano - Facultad de Ingeniería", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=8, fontName='Times-Roman')),
            Paragraph("Director - OREFI", ParagraphStyle('Centered', alignment=TA_CENTER, fontSize=8, fontName='Times-Roman'))
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


@bp.route('/api/listado-promocion', methods=['GET'])
@login_required
def listado_promocion():
    codigo_carrera = request.args.get('codigo_carrera')
    codigo_periodo = request.args.get('codigo_periodo')

    if not codigo_carrera or not codigo_periodo:
        return jsonify({'error': 'Faltan datos'}), 400

    egresados = RegistroEgresado.query.filter_by(cod_carrera=codigo_carrera, cod_periodo=codigo_periodo).order_by(RegistroEgresado.rendimiento.desc()).all()

    if not egresados:
        return jsonify({'error': 'No se encontraron egresados'}), 404

    return jsonify([e.to_dict() for e in egresados])

@bp.route('/api/generar-listado-promocion', methods=['GET'])
@login_required
def generar_listado_promocion():
    codigo_carrera = request.args.get('codigo_carrera')
    codigo_periodo = request.args.get('codigo_periodo')

    if not codigo_carrera or not codigo_periodo:
        return jsonify({'error': 'Faltan datos'}), 400

    egresados = RegistroEgresado.query.filter_by(cod_carrera=codigo_carrera, cod_periodo=codigo_periodo).order_by(RegistroEgresado.rendimiento.desc()).all()
    info = db.session.query(Informacion).first()

    if not egresados:
        return jsonify({'error': 'No se encontraron egresados'}), 404

    # Calcular el promedio general
    total_rendimiento = sum(egresado.rendimiento for egresado in egresados)
    promedio_general = total_rendimiento / len(egresados) if egresados else 0

    # Crear el PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Cargar el membrete utilizando ruta absoluta
    base_path = os.path.dirname(os.path.abspath(__file__))
    membrete_path = os.path.join(base_path, 'static', 'img', 'membrete.png')

    # Ajustar el tamaño del membrete
    membrete_height = 85  # Ajusta la altura del membrete según sea necesario
    membrete_width = width - 30  # Aumenta el ancho del membrete para ocupar casi todo el ancho de la página

    # Verificar si el archivo existe y es accesible
    try:
        img_membrete = Image.open(membrete_path)
    except Exception as e:
        return jsonify({'error': f'Error al abrir la imagen del membrete: {str(e)}'}), 500

    try:
        c.drawImage(membrete_path, 15, height - 100, width=membrete_width, height=membrete_height, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        return jsonify({'error': f'Error al cargar la imagen del membrete en el PDF: {str(e)}'}), 500

    # Configurar el encabezado del listado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 150, f"Listado de Egresados - Carrera: {codigo_carrera} - Período: {codigo_periodo}")

    # Configurar la tabla con los datos
    y = height - 180  # Posición inicial
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, y, "SECUENCIA")
    c.drawString(100, y, "CÉDULA")
    c.drawString(200, y, "APELLIDO Y NOMBRE")
    c.drawString(400, y, "PROMEDIO")
    c.drawString(480, y, "LUGAR")
    y -= 20

    c.setFont("Helvetica", 12)
    for idx, egresado in enumerate(egresados, start=1):
        c.drawString(50, y, str(idx))
        c.drawString(100, y, egresado.cedula)
        c.drawString(200, y, egresado.nombre)
        c.drawString(400, y, str(egresado.rendimiento))
        c.drawString(480, y, str(idx))
        y -= 20
        if y < 50:  # Salto de página si se llena
            c.showPage()
            y = height - 50

    # Añadir el promedio general, nombres del decano y director
    c.setFont("Helvetica", 12)
    c.drawString(100, y - 20, f"PROMEDIO GENERAL: {promedio_general:.3f}")
    y -= 40
    c.drawString(100, y - 20, f"{info.director}")
    c.drawString(100, y - 40, "Director(a) - OREFI")
    y -= 60
    c.drawString(100, y - 20, f"{info.decano}")
    c.drawString(100, y - 40, "Decano - Facultad de Ingeniería")
    y -= 60
    c.drawString(100, y - 20, "Cuadro de Promoción por el Promedio Ponderado")

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, mimetype='application/pdf', download_name="Listado_Promocion.pdf")