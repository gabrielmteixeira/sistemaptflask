from flask import render_template, Blueprint, request, redirect, url_for, flash
from projeto_base.usuario.models import Usuario, usuario_urole_roles
from projeto_base import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

usuario = Blueprint('usuario', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "principal.index"

@usuario.route('/editar_usuario/', methods=['POST', 'GET']) 
@login_required()
def editar_usuario():

    def renderizaTemplate(entidade_usuario, permissao_usuario):
        return render_template('editar_usuario.html',
                               login_usuario = entidade_usuario.login,
                               email_usuario = entidade_usuario.email,
                               permissao_usuario = permissao_usuario)

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

            db.session.commit()
        elif entidade_usuario_permissao == usuario_urole_roles['ADMIN']:

            entidade_usuario.login = form["login"]
            entidade_usuario.email = form["email"]

            status = form["ativo"]

            if status == "ativo":
                entidade_usuario.active = True
            if status == "desativado":
                entidade_usuario.active = False

            db.session.commit()

        flash("Usuário alterado com sucesso!")
        return redirect(url_for('principal.index'))

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
        else:
            if request.method == 'POST':
                form = request.form

                login = form["login"]
                senha = form["senha"]
                email = form["email"]
                confirmacao = form["confirmacao"]

                emailRepetido = Usuario.query.filter_by(email= email).first()
                loginRepetido = Usuario.query.filter_by(login= login).first()

                if (confirmacao != senha ):
                    flash("Confirmação de senha e senha estão diferentes.")
                elif (emailRepetido):
                    flash("Este email já está em uso.")
                elif not(emailRepetido or loginRepetido):

                    entidade_usuario = Usuario(login,senha,email)

                    db.session.add(entidade_usuario)
                    db.session.commit()
                    flash("Usuário cadastrado!")

                return redirect(url_for('principal.index'))
    else:
        if request.method == 'POST':
            form = request.form

            login = form["login"]
            senha = form["senha"]
            email = form["email"]
            confirmacao = form["confirmacao"]

            emailRepetido = Usuario.query.filter_by(email= email).first()
            loginRepetido = Usuario.query.filter_by(login= login).first()

            if (confirmacao != senha ):
                flash("Confirmação de senha e senha estão diferentes.")
            elif (emailRepetido):
                flash("Este email já está em uso.")
            elif not(emailRepetido or loginRepetido):

                entidade_usuario = Usuario(login,senha,email)

                db.session.add(entidade_usuario)
                db.session.commit()
                flash("Usuário cadastrado!")

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

@usuario.route('/admin_excluir_usuario_lista/',methods=['POST', 'GET'])
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

        db.session.delete(entidade_usuario)
        db.session.commit()
    lista = Usuario.query.all()
    return render_template('listar_usuarios.html', lista = lista)

@usuario.route('/admin_desativar_usuario/',methods=['POST', 'GET'])
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

@usuario.route('/admin_ativar_usuario/',methods=['POST', 'GET'])
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

@usuario.route('/admin_editar_usuario/<id_user>', methods = ['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def admin_editar_usuario(id_user):
    entidade_usuario_atual = Usuario.query.filter_by(id = id_user).first()

    if request.method == 'POST':
        form = request.form

        nome = form ["login"]
        email = form["email"]
        senha = form["senha"]
        confirmar_senha = form["confirmar_senha"]
        ativo = None
        funcao = form["funcao"]

        if(form["ativo"].lower() == "ativo"):
            ativo = True
        elif(form["ativo"].lower() == "desativado"):
            ativo = False

        if (senha != confirmar_senha):
            flash('As senhas inseridas são diferentes')
            return redirect(url_for('principal.index'))

        entidade_usuario_atual.login = nome
        entidade_usuario_atual.email = email
        entidade_usuario_atual.setSenha(senha)
        entidade_usuario_atual.active = ativo
        entidade_usuario_atual.urole = funcao
        db.session.commit()
        flash('Usuario editado com sucesso!')
        return redirect(url_for('principal.index'))

    return render_template('editar_usuario_adm.html', entidade_usuario = entidade_usuario_atual)

@usuario.route('/excluir_usuario_by_adm/<id_user>')
@login_required(role=[usuario_urole_roles['ADMIN']])
def excluir_usuario_by_adm(id_user):

    entidade_usuario = Usuario.query.filter_by(id = id_user).first()
    db.session.delete(entidade_usuario)
    db.session.commit()

    flash('Usuario excluido com sucesso')

    return redirect(url_for('principal.index'))
