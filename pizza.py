from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required  # Importa login_required
from models import db, Orden, Cliente
from forms import OrdenForm

pizza_bp = Blueprint('pizza', __name__)  # Inicializa el Blueprint

def leer_ordenes_desde_archivo():
    """Lee las órdenes desde el archivo de texto."""
    ordenes = []
    try:
        with open("registros.txt", "r") as f:
            for line in f:
                # Dividir la línea en partes
                parts = line.strip().split(",")
                
                # Asegurarnos de que hay al menos 7 campos
                if len(parts) < 7:
                    continue
                
                # Reconstruir los ingredientes (pueden contener comas)
                idOrden = int(parts[0])
                tam = parts[1]
                ing = ",".join(parts[2:-4])  # Agrupar los ingredientes
                num = int(parts[-4])
                total = float(parts[-3])
                idClient = int(parts[-2])
                status = int(parts[-1])

                # Agregar la orden a la lista si está activa
                if status == 1:
                    orden = {
                        "idOrden": idOrden,
                        "tam": tam,
                        "ing": ing,
                        "num": num,
                        "total": total,
                        "idClient": idClient,
                        "status": status,
                    }
                    ordenes.append(orden)
    except FileNotFoundError:
        pass  # Si el archivo no existe, simplemente devuelve una lista vacía
    return ordenes

def calcular_total(tamanio, numero, ingredientes):
    precios = {
        'chica': 40,
        'mediana': 80,
        'grande': 120
    }
    precio_base = precios[tamanio]
    precio_ingredientes = len(ingredientes) * 10
    return (precio_base + precio_ingredientes) * numero

@pizza_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = OrdenForm(request.form)
    if request.method == "POST" and form.validate():
        ingredientes = form.ingredientes.data
        nueva_orden = Orden(
            tam=form.tamanio.data,
            ing=','.join(ingredientes),
            num=int(form.numero.data),
            total=calcular_total(form.tamanio.data, int(form.numero.data), ingredientes),
            idClient=1,
            status=1,
        )
        db.session.add(nueva_orden)
        db.session.commit()

        with open('registros.txt', 'a') as f:
            f.write(f"{nueva_orden.idOrden},{nueva_orden.tam},{nueva_orden.ing},{nueva_orden.num},{nueva_orden.total},{nueva_orden.idClient},{nueva_orden.status}\n")

    cliente = Cliente.query.all()
    orden = leer_ordenes_desde_archivo()
    return render_template("orden.html", cliente=cliente, orden=orden, form=form)

@pizza_bp.route("/deleteOrden/<int:id>", methods=["POST"])
def delete_orden(id):
    orden = Orden.query.get(id)
    if orden:
        orden.status = 0
        db.session.commit()

        ordenes = leer_ordenes_desde_archivo()
        with open('registros.txt', 'w') as f:
            for o in ordenes:
                if o['idOrden'] == id:
                    o['status'] = 0
                f.write(f"{o['idOrden']},{o['tam']},{o['ing']},{o['num']},{o['total']},{o['idClient']},{o['status']}\n")

        return jsonify({"success": True})
    return jsonify({"success": False})

@pizza_bp.route("/calcularTotal", methods=["POST"])
def calcular_total_pedido():
    ordenes = leer_ordenes_desde_archivo()
    total_por_cliente = {}

    for orden in ordenes:
        if orden['status'] == 1:
            idClient = orden['idClient']
            if idClient not in total_por_cliente:
                total_por_cliente[idClient] = 0
            total_por_cliente[idClient] += orden['total']

    total = sum(total_por_cliente.values())
    return jsonify({"success": True, "total": total})