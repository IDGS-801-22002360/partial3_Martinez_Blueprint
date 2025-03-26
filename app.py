from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
from models import db, Cliente, Orden
from forms import OrdenForm, LoginForm
from pizza import pizza_bp
from proovedores import proovedores_bp

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a la página de inicio de sesión si no está autenticado

@app.context_processor
def inject_user():
    return dict(user=current_user)

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
            return redirect(url_for('pizza.index'))  # Redirige al Blueprint de pizza
        else:
            flash('Credenciales inválidas.', 'error')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitoso.', 'success')
    return redirect(url_for('login'))

app.register_blueprint(pizza_bp, url_prefix='/pizza')

app.register_blueprint(proovedores_bp, url_prefix='/proovedores')

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run()