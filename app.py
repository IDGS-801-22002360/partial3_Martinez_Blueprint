from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'llave_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a esta vista si no está autenticado

# Clase de usuario (usando UserMixin para integrar con flask-login)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

#*  con el uso de una base de datos simulada vamos a poner a 2 usuarios
users = {
    'user1': User(id=1, username='marco', password='1234'),
    'user2': User(id=2, username='user2', password='1234')
}

# Cargar usuario por ID
@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users.values() if u.username == username and u.password == password), None)
        if user:
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales inválidas.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitoso.', 'success')
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)