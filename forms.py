from wtforms import Form, StringField, validators, RadioField, SelectMultipleField, widgets, PasswordField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectMultipleField, widgets, validators

class OrdenForm(FlaskForm):  # Asegúrate de heredar de FlaskForm
    nombre = StringField('Nombre', [
        validators.DataRequired(message='Este campo es requerido'),
    ])
    direccion = StringField('Dirección', [
        validators.DataRequired(message='Este campo es requerido'),
    ])
    telefono = StringField('Teléfono', [
        validators.DataRequired(message='Este campo es requerido'),
        validators.Length(max=10, message='El teléfono debe tener máximo 10 caracteres'),
        validators.Regexp(r'^\d+$', message='El teléfono debe contener solo números')
    ])
    tamanio = RadioField('Tamaño', choices=[('chica', 'Chica'), ('mediana', 'Mediana'), ('grande', 'Grande')], default='mediana')
    ingredientes = SelectMultipleField('Ingredientes', choices=[('jamon', 'Jamón'), ('pina', 'Piña'), ('champiñones', 'Champiñones')], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))
    numero = StringField('Número', [
        validators.DataRequired(message="Este campo es requerido"),
        validators.Regexp(r'^\d+$', message='El número debe contener solo números')
    ])
    
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class ProovedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    contacto = StringField('Contacto', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    submit = SubmitField('Guardar')