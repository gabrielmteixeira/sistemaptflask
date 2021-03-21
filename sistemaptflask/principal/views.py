from flask import render_template, Blueprint
from sistemaptflask.usuario.models import Usuario
from sistemaptflask.tarefa.models import Tarefa
from sistemaptflask.principal.utils import get_ejs_destaque
from sistemaptflask import db
from flask_login import current_user

principal = Blueprint('principal', __name__, template_folder='templates')

@principal.route('/')
def index():
    tarefas = Tarefa.query.all()
    for tarefa in tarefas:
        tarefa.is_prazo_perto = tarefa.isPrazoApertado()
    
    ejs_destaque = get_ejs_destaque()

    return render_template('tela_principal.html', tarefas=tarefas, ejs_destaque=ejs_destaque)
