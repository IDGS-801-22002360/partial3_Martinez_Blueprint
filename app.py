from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()                    # este es un query a la tabla alumnos
    return render_template("index.html", form=create_form, alumnos=alumno)

@app.route("/detalles", methods=["GET", "POST"])
def detalles():
    if request.method == "GET":
        id = request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        
        nombre = alum1.nombre
        apaterno = alum1.apaterno
        email = alum1.email
        
        return render_template("detalles.html", id=id, nombre=nombre, apaterno=apaterno, email=email)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run()


