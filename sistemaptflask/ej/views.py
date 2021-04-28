import os
import time
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from sistemaptflask.ej.models import Ej
from sistemaptflask.ej.utils import calcula_chart_grid
from sistemaptflask.usuario.models import Usuario, usuario_urole_roles
from sistemaptflask.tarefa.models import Tarefa, TarefaTrainee
from sistemaptflask.tarefa.utils import confere_prazo_tarefa
from sistemaptflask import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user
from sqlalchemy.sql import or_, and_

ej = Blueprint('ej', __name__, template_folder='templates')

@ej.route('/listar_ejs', methods = ['GET'])
@login_required()
def listar_ejs():
    lista = Ej.query.all()
    return render_template('listar_ejs.html', lista=lista, usuario=current_user)

@ej.route('/perfil/<id>', methods = ['GET', 'POST'])
@login_required()
def perfil_ej(id):
    entidade_ej = Ej.query.get_or_404(id)
    
    if request.method == 'POST':  
        usuario_id = current_user.id
        usuario = Usuario.query.get_or_404(usuario_id)
        
        tarefas = Tarefa.query.filter_by(ehSolo=0).all()
        for tarefa in tarefas:
            if entidade_ej.usuarios and tarefa in entidade_ej.usuarios[0].get_tarefas():
                tarefa_trainee = TarefaTrainee(tarefa, usuario)
                confere_prazo_tarefa(tarefa_trainee)
                db.session.add(tarefa_trainee)

        usuario.ej_id = id
        db.session.commit()
    
    return render_template('perfil_ej.html', entidade_ej = entidade_ej, usuario = current_user)

@ej.route('/cadastrar_ej', methods = ['POST', 'GET'])
@login_required()
def cadastrar_ej():
    if (current_user.is_authenticated):
        if request.method == 'POST':
            form = request.form

            nome = form["nome"]
            foto_ej = request.files["foto_ej"]

            original_filename = foto_ej.filename
            filename = str(original_filename).split(".")
            filename[0] = str(time.time())
            filename.insert(1, ".")
            filename = "".join(filename)
            print("++++++++++++++++" + filename)
            filepath = os.path.join(current_app.root_path, 'static', 'fotos_ej', filename)
            foto_ej.save(filepath)

            entidade_ej = Ej(nome=nome, imagem=filename)

            db.session.add(entidade_ej)

            db.session.commit()
            flash("Empresa cadastrada!")

            if current_user.urole == usuario_urole_roles['USER']:
                usuario_id = current_user.id

                usuario = Usuario.query.get_or_404(usuario_id)
                
                usuario.ej_id = entidade_ej.id
                db.session.commit()

            return redirect(url_for('principal.index'))

    return render_template('cadastro_ej.html')


@ej.route('/editar_ej/<id>', methods = ['GET', 'POST'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def editar_ej(id):
    ej = Ej.query.filter_by(id=id).first_or_404()

    if request.method == 'POST':
        form = request.form

        _id = id
        ej = Ej.query.filter_by(id=_id).first_or_404()

        ej.nome = form['nome']

        foto = request.files['foto_ej']
        if foto.content_type != 'application/octet-stream':
            original_filename = foto.filename
            filename = str(original_filename).split(".")
            filename[0] = str(time.time())
            filename.insert(1, ".")
            filename = "".join(filename)
            print("++++++++++++++++" + filename)
            filepath_novo = os.path.join(current_app.root_path, 'static', 'fotos_ej', filename)
            foto.save(filepath_novo)
            
            filepath_antigo = os.path.join(current_app.root_path, 'static', 'fotos_ej', )
            os.remove(filepath_antigo)        
            
            ej.imagem = filename

        db.session.commit()

        return redirect(url_for('ej.perfil_ej', id=id))

    return render_template('editar_ej.html', id=id, nome=ej.nome, cnpj=ej.cnpj , metaProj=ej.projetos_meta, metaFat=ej.faturamento_meta, 
                                                            atualProj=ej.projetos_atual, atualFat=ej.faturamento_atual)



@ej.route('/deletar_ej/<_id>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def deleta_ej(_id):
    ej = Ej.query.get_or_404(_id)
    db.session.delete(ej)
    db.session.commit()

    return redirect(url_for('ej.listar_ejs'))


@ej.route('/relacionar_ej/<_id>', methods=['GET', 'POST'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def relacionar_ej(_id):

    ej = Ej.query.get_or_404(_id)
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        usuario_id = request.form['id']
    
        usuario = Usuario.query.get_or_404(usuario_id)
        
        ej_id = request.form['ej_id']

        tarefas = Tarefa.query.filter_by(ehSolo=0).all()
        for tarefa in tarefas:
            if ej.usuarios and tarefa in ej.usuarios[0].get_tarefas():
                tarefa_trainee = TarefaTrainee(tarefa, usuario)
                confere_prazo_tarefa(tarefa_trainee)
                db.session.add(tarefa_trainee)
    
        usuario.ej_id = ej_id
        db.session.commit()

        return redirect(url_for('ej.relacionar_ej', _id=ej.id))


    return render_template('relacionar_ej.html', ej=ej, usuario=usuarios)

@ej.route('/remover_trainee/<id_ej>/<id_trainee>')
@login_required()
def remover_trainee(id_ej, id_trainee):
    if current_user.urole != 'admin' and int(current_user.id) != int(id_trainee):
        flash('Você não possui permissão de remover outra pessoa de sua EJ.')
        return redirect(url_for('ej.perfil_ej', id=id_ej))
        
    trainee = Usuario.query.get_or_404(id_trainee)
    tarefas = trainee.get_tarefas_coletivas()

    tarefasColetivasEntregues = list()
    for tarefa in tarefas:
        tarefasColetivasEntregues.append(TarefaTrainee.query.join(Tarefa).filter(and_(TarefaTrainee.id_trainee == id_trainee, Tarefa.id == tarefa.id)).first())
    
    for tarefa in tarefasColetivasEntregues:
        db.session.delete(tarefa)
   
    trainee.ej_id = None
    
    db.session.commit()

    return redirect(url_for('ej.perfil_ej', id=id_ej))
