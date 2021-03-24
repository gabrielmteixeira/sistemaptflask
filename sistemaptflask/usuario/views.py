import os
import time
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app, abort
from sistemaptflask.usuario.models import Usuario, usuario_urole_roles
from sistemaptflask.tarefa.models import Tarefa, TarefaTrainee
from sistemaptflask import db, login_required, mail, app
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_mail import Message
from secrets import token_urlsafe
from datetime import datetime, timedelta


usuario = Blueprint('usuario', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "principal.index"

@usuario.route('/perfil')
@login_required()
def perfil():
    def renderizaTemplate(entidade_usuario):
        return render_template('perfil.html',
                               entidade_usuario = entidade_usuario)
    
    entidade_usuario = Usuario.query.filter_by(id = current_user.get_id()).first()

    return renderizaTemplate(entidade_usuario)

@usuario.route('/visualizar_usuario/<_id>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def visualizar_usuario(_id):
    trainee = Usuario.query.get_or_404(_id)
    tarefasEntregues = (Tarefa.query.join(TarefaTrainee, TarefaTrainee.id_tarefa == Tarefa.id)
                        .add_columns((Tarefa.titulo), (TarefaTrainee.atrasada), (Tarefa.id))
                        .filter(TarefaTrainee.id_trainee == _id)
                        ).all()
    return render_template('visualizar_usuario.html', tarefasEntregues=tarefasEntregues, trainee=trainee)

@usuario.route('/editar_usuario/', methods=['POST', 'GET']) 
@login_required()
def editar_usuario():

    def renderizaTemplate(entidade_usuario, permissao_usuario):
        return render_template('editar_usuario.html',
                               login_usuario = entidade_usuario.login,
                               email_usuario = entidade_usuario.email,
                               permissao_usuario = permissao_usuario,
                               entidade_usuario = entidade_usuario)

    def validaDadosForm(login, email, loginAtual, emailAtual):
        emailRepetido = Usuario.query.filter_by(email= email).first()
        loginRepetido = Usuario.query.filter_by(login= login).first()

        if (emailAtual != email) and emailRepetido:
            flash("Este email já existe!")
            return False
        elif (loginAtual != login) and loginRepetido:
            flash("Este login já existe!")
            return False
        return True

    entidade_usuario = Usuario.query.filter_by(id = current_user.get_id()).first()

    if not entidade_usuario:
        flash("Usuário não encontrado.")
        return redirect(url_for('principal.index'))

    entidade_usuario_permissao = entidade_usuario.urole

    if request.method == "POST":
        form = request.form

        if not validaDadosForm(form["login"], form["email"], form["loginAtual"], form["emailAtual"]):
            return renderizaTemplate(entidade_usuario, entidade_usuario_permissao)

        if entidade_usuario_permissao == usuario_urole_roles['USER']:

            entidade_usuario.login = form["login"]
            entidade_usuario.email = form["email"]
            entidade_usuario.nome = form["nome"]
            foto_trainee = request.files["foto_trainee"]

            if foto_trainee:
                filename = foto_trainee.filename
                original_filename = str(original_filename).split(".")
                filename[0] = str(time.time())
                filename.insert(1, ".")
                filename = "".join(filename)
                filepath = os.path.join(current_app.root_path, 'static', 'fotos_trainees', filename)
                foto_trainee.save(filepath)
                entidade_usuario.foto_trainee = foto_trainee.filename
            db.session.commit()
        elif entidade_usuario_permissao == usuario_urole_roles['ADMIN']:

            entidade_usuario.login = form["login"]
            entidade_usuario.email = form["email"]
            entidade_usuario.nome = form["nome"]
            foto_trainee = request.files["foto_trainee"]

            if foto_trainee:
                original_filename = foto_trainee.filename
                filename = str(original_filename).split(".")
                filename[0] = str(time.time())
                filename.insert(1, ".")
                filename = "".join(filename)
                filepath = os.path.join(current_app.root_path, 'static', 'fotos_trainees', filename)
                foto_trainee.save(filepath)
                entidade_usuario.foto_trainee = foto_trainee.filename
            status = form["ativo"]

            if status == "ativo":
                entidade_usuario.active = True
            if status == "desativado":
                entidade_usuario.active = False

            db.session.commit()

        return redirect(url_for('usuario.perfil'))

    return renderizaTemplate(entidade_usuario, entidade_usuario_permissao)

@usuario.route('/editar_senha_usuario/', methods=['POST', 'GET'])
@login_required()
def editar_senha_usuario():

    if request.method == 'POST':
        entidade_usuario = Usuario.query.filter_by(id = current_user.get_id()).first()

        form = request.form
        confirmacao = form['confirmacao']
        senha = form['senha']

        if not entidade_usuario:
            flash("Usuário não encontrado.")
            return redirect(url_for('principal.index'))

        if (confirmacao == senha):
            entidade_usuario.setSenha(senha)

            db.session.commit()

            flash("Senha alterada com sucesso!")
        else:
            flash("Confirmação de senha e senha estão diferentes.")

        return redirect(url_for('principal.index'))

    return render_template('editar_senha_usuario.html')

@usuario.route('/cadastrar_usuario', methods = ['POST', 'GET'])
def cadastrar_usuario():
    if (current_user.is_authenticated):
        if current_user.urole == usuario_urole_roles['USER']:
            flash("Você não tem permissão para realizar esta ação.")
            return redirect(url_for("principal.index"))
    elif request.method == 'POST':
            form = request.form

            nome = form["nome"]
            login = form["login"]
            senha = form["senha"]
            email = form["email"]
            confirmacao = form["confirmacao"]
            foto_trainee = request.files["foto_trainee"]

            emailRepetido = Usuario.query.filter_by(email= email).first()
            loginRepetido = Usuario.query.filter_by(login= login).first()

            if (confirmacao != senha ):
                flash("Confirmação de senha e senha estão diferentes.")
                return redirect(url_for('usuario.cadastrar_usuario'))
            elif (emailRepetido):
                flash("Este email já está em uso.")
                return redirect(url_for('usuario.cadastrar_usuario'))
            elif loginRepetido:
                flash("Este username já está em uso.")
                return redirect(url_for('usuario.cadastrar_usuario'))
            elif not(emailRepetido or loginRepetido):

                original_filename = foto_trainee.filename
                filename = str(original_filename).split(".")
                filename[0] = str(time.time())
                filename.insert(1, ".")
                filename = "".join(filename)
                filepath = os.path.join(current_app.root_path, 'static', 'fotos_trainees', filename)
                foto_trainee.save(filepath)

                entidade_usuario = Usuario(nome=nome,
                                           login=login,
                                           senha=senha,
                                           email=email,
                                           foto_trainee=filename)

                db.session.add(entidade_usuario)
                db.session.commit()
                
                flash("Usuário cadastrado!")

                loginUsuario = Usuario.query.filter_by(email=email).first()
                login_user(loginUsuario)
                flash("Usuário logado com sucesso!")
            return redirect(url_for('principal.index'))

    return render_template('cadastro.html')
    
@usuario.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        form = request.form

        login = form["login"]
        senha = form["senha"]

        loginUsuario = Usuario.query.filter_by(login=login).first()

        if(loginUsuario):

            checaSenha = Usuario.checa_senha(loginUsuario, senha)
            if (checaSenha):
                if(loginUsuario.active == True):
                    login_user(loginUsuario)
                    flash("Usuário logado com sucesso!")
                    current_user.__name__=loginUsuario.login
                    return redirect(url_for('principal.index'))
                else:
                    flash("Este usuário foi desativado!")
                    return redirect(url_for('principal.index'))
            else:
                flash("Senha inválida")
        else:
            loginUsuario = Usuario.query.filter_by(email=login).first()
            if (loginUsuario):
                checaSenha = Usuario.checa_senha(loginUsuario, senha)
                if (checaSenha):
                    login_user(loginUsuario)
                    flash("Usuário logado com sucesso!")
                    return redirect(url_for('principal.index'))
                else:
                    flash("Senha inválida")
            else:
                flash("Usuário inválido")


    return render_template('login.html')

@usuario.route('/logout')
@login_required()
def logout():
    if (current_user):
        logout_user()
        flash("Logout feito com sucesso!")
    else:
        flash("Você precisa estar logado para continuar")
    return redirect(url_for('principal.index'))

@usuario.route('/listar_usuarios')
@login_required(role=[usuario_urole_roles['ADMIN']])
def listar_usuarios():
    lista = Usuario.query.all()
    if not lista:
        flash("Não há usuários cadastrados no sistema.")
        return redirect(url_for('principal.index'))

    return render_template('listar_usuarios.html', lista = lista)

@usuario.route('/excluir_usuario/')
@login_required()
def excluir_usuario():
    entidade_usuario = Usuario.query.filter_by(id = current_user.get_id()).first()
    if entidade_usuario.urole == usuario_urole_roles['ADMIN']:
        flash("O admin não pode ser excluído.")
        return redirect(url_for('principal.index'))

    db.session.delete(entidade_usuario)
    db.session.commit()
    return redirect(url_for('principal.index'))

@usuario.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        form = request.form
        email = form['email']
        confirmaEmail = form['confirmar']

        usuario = Usuario.query.filter_by(email=email).first()
        
        if email == confirmaEmail:
            if usuario:
                
                token = token_urlsafe(128)

                usuario.reset_token = token
                usuario.token_expiration = datetime.utcnow() + timedelta(hours=1)

                mensagem = Message("Recuperação de Senha",
                                    sender=('iJunior', 'emailautomatico1234@gmail.com'),
                                    recipients=[email])
                recover_url = url_for(
                    'usuario.recuperar_senha',
                    token=token,
                    _external=True)

                mensagem.html = render_template('email_de_resetar.html', usuario=usuario, recover_url = recover_url)

                mail.send(mensagem)

                db.session.commit()

                flash("Um e-mail para recuperar sua senha foi enviado no seu E-mail. Caso não encontre seu email, procure-o na caixa de spam")
                return redirect(url_for('usuario.forgot_password'))
            else:
                flash('Email incorreto!')
                return redirect(url_for('usuario.forgot_password'))
        else:
            flash("O E-mail e sua confirmação estão diferentes!")
            return redirect(url_for("usuario.forgot_password"))

    return render_template('forgot_password.html')
@usuario.route('/recuperar_senha', methods=['GET', 'POST'])
@usuario.route('/recuperar_senha/<token>', methods=['GET', 'POST'])
def recuperar_senha(token = None):
    if request.method == 'POST':
        form = request.form

        token = form['token']

        usuario = Usuario.query.filter(Usuario.reset_token == token).first()

        if not usuario:
            flash('Token informado expirou ou é inválido', 'error')
            return redirect(url_for('usuario.login'))

        if usuario.token_expiration <= datetime.utcnow():
            usuario.reset_token = None
            usuario.token_expiration = None
            db.session.commit()

            flash('Token informado expirou ou é inválido', 'error')
            return redirect(url_for('principal.login'))

        senha = form['senha']
        confirmar = form['confirmar']
        
        if confirmar == senha:
            usuario.setSenha(senha)
            usuario.reset_token = None
            usuario.token_expiration = None
            db.session.commit()
            flash("Senha alterada com sucesso!")
            return redirect(url_for('usuario.login'))
        elif confirmar != senha:
            flash("Confirmação de senha e senha estão diferentes.")
            return redirect(url_for('usuario.recuperar_senha', token=token))
    return render_template('password_reset.html', token=token)