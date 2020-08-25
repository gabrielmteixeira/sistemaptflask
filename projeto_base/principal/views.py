from flask import render_template, Blueprint
from projeto_base.usuario.models import Usuario
from projeto_base.tarefa.models import Tarefa
from projeto_base import db
from flask_login import current_user

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route('/')
def index():
    tarefas = Tarefa.query.all()
    
    return render_template('tela_principal.html', tarefas=tarefas)

@principal.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')