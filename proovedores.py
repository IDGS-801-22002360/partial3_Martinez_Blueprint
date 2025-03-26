from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required
from forms import ProovedorForm
import os

proovedores_bp = Blueprint('proovedores', __name__, template_folder='templates')

PROOVEDORES_FILE = "proovedores.txt"

def leer_proovedores():
    if not os.path.exists(PROOVEDORES_FILE):
        return []
    with open(PROOVEDORES_FILE, "r") as f:
        lines = f.readlines()
    return [eval(line.strip()) for line in lines]

def guardar_proovedores(proovedores):
    with open(PROOVEDORES_FILE, "w") as f:
        for proovedor in proovedores:
            f.write(f"{proovedor}\n")

@proovedores_bp.route("/")
@login_required
def index():
    proovedores = leer_proovedores()
    form = ProovedorForm()
    return render_template("proovedores.html", proovedores=proovedores, form=form)

@proovedores_bp.route("/add", methods=["POST"])
@login_required
def add_proovedor():
    form = ProovedorForm()
    if form.validate_on_submit():
        proovedores = leer_proovedores()
        nuevo_proovedor = {
            "id": len(proovedores) + 1,
            "nombre": form.nombre.data,
            "contacto": form.contacto.data,
            "telefono": form.telefono.data
        }
        proovedores.append(nuevo_proovedor)
        guardar_proovedores(proovedores)
        return redirect(url_for("proovedores.index"))
    return redirect(url_for("proovedores.index"))

@proovedores_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_proovedor(id):
    proovedores = leer_proovedores()
    proovedores = [p for p in proovedores if p["id"] != id]
    guardar_proovedores(proovedores)
    return jsonify({"success": True})

@proovedores_bp.route("/edit/<int:id>", methods=["POST"])
@login_required
def edit_proovedor(id):
    form = ProovedorForm()
    if form.validate_on_submit():
        proovedores = leer_proovedores()
        for proovedor in proovedores:
            if proovedor["id"] == id:
                proovedor["nombre"] = form.nombre.data
                proovedor["contacto"] = form.contacto.data
                proovedor["telefono"] = form.telefono.data
                break
        guardar_proovedores(proovedores)
    return redirect(url_for("proovedores.index"))