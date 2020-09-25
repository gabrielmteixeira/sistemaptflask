from flask import render_template, Blueprint, request, redirect, url_for, flash
from sistemaptflask.usuario.models import Usuario, usuario_urole_roles
from sistemaptflask import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

admin = Blueprint('admin', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "principal.index"


@admin.route('/excluir_usuario_lista/',methods=['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def admin_excluir_usuario_lista():

    entidade_usuario_atual = Usuario.query.filter_by(id = current_user.get_id()).first()

    if request.method == 'POST':
        form = request.form
        id = form["id"]
        entidade_usuario = Usuario.query.filter_by(id = id).first()

        if entidade_usuario_atual == entidade_usuario:
            flash("Você não tem permissão para executar esta ação.")
            return redirect(url_for('principal.index'))
        
        for assoc in entidade_usuario.tarefas:
            db.session.delete(assoc) 

        db.session.delete(entidade_usuario)
        db.session.commit()
    lista = Usuario.query.all()
    return render_template('listar_usuarios.html', lista = lista)

@admin.route('/desativar_usuario/',methods=['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def admin_desativar_usuario():
    if request.method == 'POST':
        form = request.form
        id = form["id"]
        entidade_usuario = Usuario.query.filter_by(id = id).first()

        if entidade_usuario.active == False:
            flash("O usuario já está desativado")
            return redirect(url_for('principal.index'))

        entidade_usuario.active = False
        db.session.commit()
    lista = Usuario.query.all()
    return render_template('listar_usuarios.html', lista = lista)

@admin.route('/ativar_usuario/',methods=['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def admin_ativar_usuario():
    if request.method == 'POST':
        form = request.form
        id = form["id"]
        entidade_usuario = Usuario.query.filter_by(id = id).first()

        if entidade_usuario.active == True:
            flash("O usuario já está ativo")
            return redirect(url_for('principal.index'))

        entidade_usuario.active = True
        db.session.commit()
    lista = Usuario.query.all()
    return render_template('listar_usuarios.html', lista = lista)

@admin.route('/editar_usuario/<id_user>', methods = ['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def admin_editar_usuario(id_user):
    entidade_usuario_atual = Usuario.query.filter_by(id = id_user).first()

    if request.method == 'POST':
        form = request.form

        nome = form ["login"]
        email = form["email"]
        
        ativo = None
        funcao = form["funcao"]

        if(form["ativo"].lower() == "ativo"):
            ativo = True
        elif(form["ativo"].lower() == "desativado"):
            ativo = False

        

        entidade_usuario_atual.login = nome
        entidade_usuario_atual.email = email
        entidade_usuario_atual.active = ativo
        entidade_usuario_atual.urole = funcao
        db.session.commit()
        flash('Usuario editado com sucesso!')
        return redirect(url_for('principal.index'))

    return render_template('editar_usuario_adm.html', entidade_usuario = entidade_usuario_atual)

@admin.route('/excluir_usuario/<id_user>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def excluir_usuario_by_adm(id_user):
    
    entidade_usuario = Usuario.query.filter_by(id = id_user).first()
    db.session.delete(entidade_usuario)
    db.session.commit()

    flash('Usuario excluido com sucesso')

    return redirect(url_for('principal.index'))

