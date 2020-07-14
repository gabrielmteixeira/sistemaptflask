from flask import render_template, Blueprint

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route('/')
def index():

    return render_template('tela_principal.html')

@principal.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')
