from flask import Flask, jsonify, render_template,redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from forms import ColoniaForm, EstadoForm, MunicipioForm

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sepomex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "mysecretapikey56789"

Bootstrap(app)
db = SQLAlchemy(app)


class Estado(db.Model):
    __tablename__ = "estados"
    c_estado = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
    estado = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Municipio(db.Model):
    __tablename__ = "municipios"
    c_municipio = db.Column(db.Integer, primary_key=True,unique=True, nullable=False)
    municipio = db.Column(db.String(200), nullable=False)
    c_cve_ciudad = db.Column(db.Integer, nullable=False)
    c_estado = db.Column(db.Integer, db.ForeignKey("estados.c_estado"))

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Colonia(db.Model):
    __tablename__ = "colonias"
    id_asenta_cpconst = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    colonia = db.Column(db.String(200), nullable=False)
    tipo_asentamiento = db.Column(db.String(200), nullable=False)
    codigop = db.Column(db.Integer, nullable=False)
    c_tipo_asenta = db.Column(db.Integer, nullable=False)
    d_zona = db.Column(db.String(100), nullable=False)
    c_municipio = db.Column(db.Integer, db.ForeignKey("municipios.c_municipio"))

    def to_dict(self):
        dictionary = {}
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


""" solo se ejecuta db.create_all() la primera vez que se corre el programa, esto para
    crear la base de datos con sqlite, por eso lo he comentado
"""
# db.create_all()

""" agregamos un estado de manera inicial """
# nuevo_estado = Estado(
#     c_estado=1,
#     estado="Aguascalientes"
# )
# db.session.add(nuevo_estado)
# db.session.commit()


@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")



@app.route("/estados", methods=["GET"])
def estados():
    query_estado=request.args.get("estado")

    #sí se ingresa un criterio de busqueda, se realiza la consulta en base a ese criterio
    if query_estado:
        estados=db.session.query(Estado).filter_by(estado=query_estado).all()
        if estados:
            return jsonify(estados=[estado.to_dict() for estado in estados])
        else:
            return jsonify(response={"Not found": "No hay resultados para ese estado."})
    else:
        #sí no, se muestran todos los datos de los estados
        estados = db.session.query(Estado).all()
        if estados:
            return jsonify(estados=[estado.to_dict() for estado in estados])
        else:
            return jsonify(response={"Not found": "Aún no hay estados registrados."})


@app.route("/municipios", methods=["GET"])
def municipios():
    query_municipio=request.args.get("municipio")
    
    #sí se ingresa un criterio de búsqueda, se realiza la consulta en base a ese criterio
    if query_municipio:
        municipios=db.session.query(Municipio).filter_by(municipio=query_municipio).all()
        if municipios:
            return jsonify(municipios=[municipio.to_dict() for municipio in municipios])
        else:
            return jsonify(response={"Not found": "No hay resultados para ese municipio"})  
    else:
        #sí no, se muestran todos los datos de todos los municipio
        municipios = db.session.query(Municipio).all()
        if municipios:
            return jsonify(municipios=[municipio.to_dict() for municipio in municipios])
        else:
            return jsonify(response={"Not found": "Aún no hay municipios registrados."}) 
    

#para obtener los datos generales de las colonias
@app.route("/colonias", methods=["GET"])
def colonias():
    cp_col=request.args.get("codigop")
    query_colonia=request.args.get("colonia")

    if cp_col:
        colonias=db.session.query(Colonia).filter_by(codigop=cp_col).all()
        if colonias:
            return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
        else:
            return jsonify(response={"Not found": "No hay resultados para ese código postal."})
    elif query_colonia:
        colonias=db.session.query(Colonia).filter_by(colonia=query_colonia).all()
        if colonias:
            return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
        else:
            return jsonify(response={"Not found": "No hay resultados para esa colonia."})
    else:
        colonias = db.session.query(Colonia).all()
        if colonias:
            return jsonify(colonias=[colonia.to_dict() for colonia in colonias])
        else:
            return jsonify(response={"Not found": "Aún no hay colonias registradas."})


#función para agregar un nuevo estado mediante una petición POST
@app.route("/estado_post", methods=["POST"])
def estado_post():
    try:
        nuevo_edo = Estado(
            c_estado=request.args.get("c_estado"),
            estado=request.args.get("estado")
        )
        db.session.add(nuevo_edo)
        db.session.commit()
        return jsonify(response={"success": "Estado agregado con éxito."})
    except:
        return jsonify(response={"error": "Ha ocurrido un error al agregar el estado."})

#función para agregar un nuevo municipio mediante una petición POST
@app.route("/municipio_post", methods=["POST"])
def municipio_post():
    try:
        nuevo_municipio = Municipio(
            c_municipio=request.args.get("c_municipio"),
            municipio=request.args.get("municipio"),
            c_cve_ciudad=request.args.get("c_cve_ciudad"),
            c_estado= request.args.get("c_estado")
        )
        db.session.add(nuevo_municipio)
        db.session.commit()
        return jsonify(response={"success": "Municipio agregado con éxito."})
    except:
        return jsonify(response={"error": "Ha ocurrido un error al agregar el municipio."})

#función para agregar una nueva colonia mediante una petición POST
@app.route("/colonia_post", methods=["POST"])
def colonia_post():
    try:
        nueva_colonia = Colonia(
            id_asenta_cpconst=request.args.get("id_asenta_cpconst"),
            colonia=request.args.get("colonia"),
            tipo_asentamiento=request.args.get("tipo_asentamiento"),
            codigop= request.args.get("codigop"),
            c_tipo_asenta= request.args.get("c_tipo_asenta"),
            d_zona= request.args.get("d_zona"),
            c_municipio= request.args.get("c_municipio")
        )
        db.session.add(nueva_colonia)
        db.session.commit()
        return jsonify(response={"success": "Colonia agregada con éxito."})
    except:
        return jsonify(response={"error": "Ha ocurrido un error al agregar la colonia."})

@app.route("/borra_colonia/<int:id_asenta_cpconst>", methods=["DELETE"])
def borra_colonia(id_asenta_cpconst):
    api_key = request.args.get("api-key")
    if api_key == "sepomexApiKey23":
        colonia= db.session.query(Colonia).get(id_asenta_cpconst)
        if colonia:
            db.session.delete(colonia)
            db.session.commit()
            return jsonify(response={"Success": "Se ha borrado esa colonia de la API."}), 200
        else:
            return jsonify(error={"Not Found": "No se ha encontrado una colonia con ese identificador"}), 404
    else:
        return jsonify(error={"Forbidden": "No esta autorizado para realizar esta operación, verifique la api-key"}), 403


#################################################################################
######## Estos son las funciones para añadir datos mediante formularios #########
@app.route('/nuevo_estado',methods=["GET","POST"])
def nuevo_estado():
    form=EstadoForm()

    if form.validate_on_submit():
        if Estado.query.filter_by(c_estado=form.c_estado.data).first():
            return jsonify(error={"Error": "El estado con ese código ya esta registrado"})
        
        nuevo_estado=Estado(
            c_estado=form.c_estado.data,
            estado=form.estado.data,
        )

        db.session.add(nuevo_estado)
        db.session.commit()
        return redirect(url_for('estados'))
    return render_template("nuevo_estado.html",form=form)

@app.route('/nuevo_municipio',methods=["GET","POST"])
def nuevo_municipio():
    form=MunicipioForm()

    if form.validate_on_submit():
        if Municipio.query.filter_by(c_municipio=form.c_municipio.data).first():
            return jsonify(error={"Error": "El municipio con ese código ya esta registrado"})
        
        nuevo_municipio = Municipio(
            c_municipio=form.c_municipio.data,
            municipio=form.municipio.data,
            c_cve_ciudad=form.c_cve_ciudad.data,
            c_estado= form.c_estado.data
        )
        db.session.add(nuevo_municipio)
        db.session.commit()
        return redirect(url_for('municipios'))
    return render_template("nuevo_municipio.html",form=form)

@app.route('/nueva_colonia',methods=["GET","POST"])
def nueva_colonia():
    form=ColoniaForm()

    if form.validate_on_submit():
        if Colonia.query.filter_by(id_asenta_cpconst=form.id_asenta_cpconst.data).first():
            return jsonify(error={"Error": "La colonia con ese código ya esta registrada"})
        
        nueva_colonia = Colonia(
            id_asenta_cpconst=form.id_asenta_cpconst.data,
            colonia=form.colonia.data,
            tipo_asentamiento=form.tipo_asentamiento.data,
            codigop=form.codigop.data,
            c_tipo_asenta=form.c_tipo_asenta.data,
            d_zona=form.d_zona.data,
            c_municipio=form.c_municipio.data
        )
        db.session.add(nueva_colonia)
        db.session.commit()
        return redirect(url_for('colonias'))
    return render_template("nueva_colonia.html",form=form)


if __name__ == '__main__':
    app.run(debug=True)