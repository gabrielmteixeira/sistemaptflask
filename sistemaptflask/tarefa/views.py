import os
import re
import time
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from sistemaptflask.tarefa.models import Tarefa, TarefaTrainee
from sistemaptflask.usuario.models import Usuario, usuario_urole_roles
from sistemaptflask.ej.models import Ej
from sistemaptflask import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user
from sistemaptflask.tarefa.utils import data_format_in, data_format_out, define_solo_in, define_solo_out, confere_prazo_tarefa
import copy


tarefa = Blueprint('tarefa', __name__, template_folder='templates')

@tarefa.route('/cadastrar_tarefa', methods=['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def cadastra_tarefa():
    if request.method == 'POST':
        form = request.form

        titulo = form['titulo']
        descricao = form['descricao']
        icone = form['icone']
        prazo = form['data']
        solo = form['ehSolo']

        #tratando data 
        prazo = data_format_in(prazo)

        #tratando ehSolo
        ehSolo = define_solo_in(solo)

        tarefa = Tarefa(titulo, descricao, icone, prazo, ehSolo)

        db.session.add(tarefa)
        db.session.commit() 
    
        flash("Tarefa cadastrada!")

        return redirect(url_for('principal.index'))

    return render_template('cadastro_tarefa.html')


@tarefa.route('/listar_tarefas_admin')
@login_required(role=[usuario_urole_roles['ADMIN']])
def lista_tarefas():
    tarefas = Tarefa.query.all()
    
    return render_template('listar_tarefas.html', tarefas=tarefas)

@tarefa.route('/deletar_tarefa/<id>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def deleta_tarefa(id):
    tarefa = Tarefa.query.filter_by(id=id).first_or_404()
    related = TarefaTrainee.query.filter_by(id_tarefa=id).all()

    db.session.delete(tarefa)
    for i in related:
        db.session.delete(i)
    db.session.commit()

    return redirect(url_for('tarefa.lista_tarefas'))

@tarefa.route('/editar_tarefa/<id>', methods=['GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def pagina_edicao_tarefa(id):
    tarefa = Tarefa.query.filter_by(id=id).first_or_404()

    #tratando data
    prazo = data_format_out(tarefa.prazo)

    #tratando ehSolo
    solo = define_solo_out(tarefa.ehSolo)

    return render_template('edicao_tarefa.html', titulo=tarefa.titulo, descricao=tarefa.descricao, prazo=prazo, solo=solo, id=tarefa.id)

@tarefa.route('/editar_tarefa', methods=['POST'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def edita_tarefa():
    form = request.form

    _id = form['id']
    tarefa = Tarefa.query.filter_by(id=_id).first_or_404()

    titulo = form['titulo']
    descricao = form['descricao']
    prazo = form['data']
    solo = form['ehSolo']
    icone = form['icone']

    #tratando data 
    prazo = data_format_in(prazo)

    #tratando ehSolo
    ehSolo = define_solo_in(solo)
    
    tarefa.icone = icone
    tarefa.titulo = titulo
    tarefa.descricao = descricao
    tarefa.prazo = prazo
    tarefa.ehSolo = ehSolo

    db.session.commit()

    return redirect(url_for('tarefa.lista_tarefas'))
@tarefa.route('/listar_tarefas', methods=['POST', 'GET'])
@login_required()
def lista_tarefas_users():
    tarefas = Tarefa.query.all()
    
    if not tarefas:
        flash("Não há tarefas cadastradas no sistema.")
        return redirect(url_for('principal.index'))
    
    if request.method == 'POST':
        id_tarefa = request.form['id_tarefa']
        tarefa_entregue = Tarefa.query.get_or_404(id_tarefa)
        trainee = Usuario.query.get_or_404(current_user.id)
        
        if(tarefa_entregue.ehSolo):
            tarefa_trainee = TarefaTrainee(tarefa_entregue, trainee)
            confere_prazo_tarefa(tarefa_trainee)
            db.session.add(tarefa_trainee)
        elif(not trainee.ej_id):
            flash("É preciso estar em uma EJ para entregar tarefas coletivas!")
            return redirect(url_for('tarefa.lista_tarefas_users'))
        elif(not tarefa_entregue.ehSolo and trainee.ej_id):
            ej = Ej.query.filter_by(id=trainee.ej_id).first_or_404()
            
            for membro in ej.usuarios:
                tarefa_ej = TarefaTrainee(tarefa_entregue, membro)
                confere_prazo_tarefa(tarefa_ej)
                db.session.add(tarefa_ej)        
            
        db.session.commit()

        return redirect(url_for('tarefa.lista_tarefas_users'))
    

    return render_template('listar_tarefas_users.html', tarefas=tarefas)

@tarefa.route('/visualizar_tarefa/<_id>')
def visualizar_tarefa(_id):
    tarefa = Tarefa.query.get_or_404(_id)
    tarefa_trainee = TarefaTrainee.query.filter_by(id_tarefa=_id)
    usuarios = Usuario.query.all()

    # Retorna True se todos os trainees fizeram a tarefa
    def todosFizeram():
        trainees = Usuario.query.filter(Usuario.urole != 'admin').all()
        todosQueFizeram = tarefa.get_trainees()
        return todosQueFizeram == trainees

    # Retorna uma lista de quem não fez as tarefas
    def traineesQueNaoFizeram():
        trainees = Usuario.query.filter(Usuario.urole != 'admin').all()
        todosQueFizeram = tarefa.get_trainees()
        listaTraineesQueNaoFizeram = trainees
        for trainee in trainees[:]:
            if trainee in todosQueFizeram:
                listaTraineesQueNaoFizeram.remove(trainee)
        return listaTraineesQueNaoFizeram

    return render_template('visualizar_tarefa.html', usuarios = usuarios, 
                                                    tarefa_trainee = tarefa_trainee, 
                                                    tarefa=tarefa, 
                                                    traineesQueNaoFizeram=traineesQueNaoFizeram(),
                                                    todosFizeram=todosFizeram())

@tarefa.route('/desfazer_tarefa/<id>/<traineeId>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def desfazer_tarefa(id, traineeId):
    
    tarefa_a_desfazer = Tarefa.query.get_or_404(id)    

    if tarefa_a_desfazer.ehSolo:
        instancia = TarefaTrainee.query.filter_by(id_tarefa=id, id_trainee = traineeId).first_or_404()
        db.session.delete(instancia)
    else:
        trainee = Usuario.query.get_or_404(traineeId)
        ej = Ej.query.filter_by(id=trainee.ej_id).first_or_404()
        for membro in ej.usuarios:
            instancia = TarefaTrainee.query.filter_by(id_tarefa=id, id_trainee = membro.id).first_or_404()
            db.session.delete(instancia)

    db.session.commit()

    return redirect(url_for('tarefa.visualizar_tarefa', _id = id))