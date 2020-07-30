import os
import re
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from projeto_base.tarefa.models import Tarefa, TarefaTrainee
from projeto_base.usuario.models import Usuario, usuario_urole_roles
from projeto_base import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

tarefa = Blueprint('tarefa', __name__, template_folder='templates')

@tarefa.route('/cadastrar_tarefa', methods=['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def cadastra_tarefa():
    if request.method == 'POST':
        form = request.form

        titulo = form['titulo']
        descricao = form['descricao']
        icone = request.files['icone']
        prazo = form['data']
        solo = form['ehSolo']

        #tratando data 
        lista_data = prazo.split('-')
        lista_data.reverse()
        prazo = '/'.join(lista_data)

        #tratando ehSolo
        ehSolo = False
        if(solo == 'sim'):
            ehSolo = True

        filename = icone.filename
        print("++++++++++++++++" + filename)
        filepath = os.path.join(current_app.root_path, 'static', 'fotos_tarefa', filename)
        icone.save(filepath)

        tarefa = Tarefa(titulo, descricao, filename, prazo, ehSolo)

        db.session.add(tarefa)
        db.session.commit() 
    
        flash("Tarefa cadastrada!")

        return redirect(url_for('principal.index'))

    return render_template('cadastro_tarefa.html')


@tarefa.route('/listar_tarefas')
@login_required(role=[usuario_urole_roles['ADMIN']])
def lista_tarefas():
    tarefas = Tarefa.query.all()
    if not tarefas:
        flash("Não há tarefas cadastradas no sistema.")
        return redirect(url_for('principal.index'))
    
    return render_template('listar_tarefas.html', tarefas=tarefas)

@tarefa.route('/deletar_tarefa/<id>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def deleta_tarefa(id):
    tarefa = Tarefa.query.filter_by(id=id).first_or_404()
    
    filepath = os.path.join(current_app.root_path, 'static', 'fotos_tarefa', tarefa.icone)
    os.remove(filepath)

    db.session.delete(tarefa)
    db.session.commit()

    return redirect(url_for('tarefa.lista_tarefas'))