from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave secreta real

# Inicializando el administrador de inicio de sesión
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Simulando una base de datos de usuarios
users = {
    "freddy": "password123"  # Usuario de ejemplo: freddy con contraseña password123
}

class User(UserMixin):
    def __init__(self, username):
        self.username = username
    
    def get_id(self):
        return self.username  # Devuelve el nombre de usuario como el identificador

@login_manager.user_loader
def load_user(username):
    return User(username) if username in users else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Usar get para evitar KeyError
        password = request.form.get('password')
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('welcome'))
        flash('Credenciales incorrectas.')
    return render_template('login.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)