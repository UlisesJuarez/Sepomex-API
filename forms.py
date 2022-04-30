from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired



class EstadoForm(FlaskForm):
    c_estado = IntegerField("Código estado", validators=[DataRequired()])
    estado = StringField("Estado", validators=[DataRequired()])
    submit = SubmitField("Agregar estado")

class MunicipioForm(FlaskForm):
    c_municipio=IntegerField("Código municipio", validators=[DataRequired()])
    municipio=StringField("Municipio",validators=[DataRequired()])
    c_estado=IntegerField("Código estado", validators=[DataRequired()])
    c_cve_ciudad=IntegerField("Código clave ciudad", validators=[DataRequired()])
    submit=SubmitField("Agrega municipio")

class ColoniaForm(FlaskForm):
    id_asenta_cpconst=IntegerField("Id asentamiento",validators=[DataRequired()])
    colonia=StringField("Colonia",validators=[DataRequired()])
    tipo_asentamiento=StringField("Tipo asentamiento",validators=[DataRequired()])
    codigop=IntegerField("Código postal",validators=[DataRequired()])
    c_tipo_asenta=IntegerField("Código tipo asentamiento",validators=[DataRequired()])
    d_zona=StringField("Descripción zona",validators=[DataRequired()])
    c_municipio=IntegerField("Código municipio",validators=[DataRequired()])
    submit=SubmitField("Agrega colonia")

