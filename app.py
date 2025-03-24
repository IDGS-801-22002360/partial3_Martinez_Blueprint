from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db, Cliente, Orden
from forms import OrdenForm, LoginForm

app = Flask(__name__)  # Define el objeto app aquí
app.config.from_object(DevelopmentConfig)
app.secret_key = 'llave_secreta'
csrf = CSRFProtect()

<<<<<<< HEAD
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a la página de inicio de sesión si no está autenticado

@app.context_processor
def inject_user():
    return dict(user=current_user)

# Clase de usuario (usando UserMixin para integrar con flask-login)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = {
    'user1': User(id=1, username='marco', password='1234'),
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Valida el formulario y el CSRF token
        username = form.username.data
        password = form.password.data
        user = next((u for u in users.values() if u.username == username and u.password == password), None)
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))  # Redirige al HTML de index
        else:
            flash('Credenciales inválidas.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitoso.', 'success')
    return redirect(url_for('login'))



@app.route("/", methods=["GET", "POST"])
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

@app.route("/deleteOrden/<int:id>", methods=["POST"])
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

@app.route("/calcularTotal", methods=["POST"])
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
=======
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


>>>>>>> 891be2b (03/Mar/2025 - Detalles)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run()


