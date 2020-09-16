from flask import render_template, Blueprint
from projeto_base.usuario.models import Usuario
from projeto_base.tarefa.models import Tarefa
from projeto_base.principal.utils import get_ejs_destaque
from projeto_base import db
from flask_login import current_user

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route('/')
def index():
    tarefas = Tarefa.query.all()
    
    ejs_destaque = get_ejs_destaque()

    return render_template('tela_principal.html', tarefas=tarefas, ejs_destaque=ejs_destaque)
