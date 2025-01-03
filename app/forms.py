from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class EgresadoForm(FlaskForm):
    ag = StringField('AG', validators=[DataRequired()])
    aa = StringField('AA', validators=[DataRequired()])
    pg = StringField('PG', validators=[DataRequired()])
    pa = StringField('PA', validators=[DataRequired()])
    rendimiento = FloatField('Rendimiento', validators=[DataRequired()])
    fecha_grado = DateField('Fecha de Grado', format='%Y-%m-%d', validators=[DataRequired()])
    cod_carrera = StringField('Código de Carrera', validators=[DataRequired()])
    cod_periodo = StringField('Código de Periodo', validators=[DataRequired()])
    num_periodo = StringField('Número de Periodo', validators=[DataRequired()])
    cedula = StringField('Cédula', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    submit = SubmitField('Guardar')



class ConsultaForm(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired()])
    submit = SubmitField('Consultar')
