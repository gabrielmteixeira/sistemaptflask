import os
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from projeto_base.ej.models import Ej
from projeto_base.usuario.models import Usuario, usuario_urole_roles
from projeto_base import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

ej = Blueprint('ej', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "principal.index"

@ej.route('/cadastrar_ej', methods = ['POST', 'GET'])
def cadastrar_ej():
    if (current_user.is_authenticated):
        if current_user.urole == usuario_urole_roles['USER']:
            flash("Você não tem permissão para realizar esta ação.")
            return redirect(url_for("principal.index"))
        else:
            if request.method == 'POST':
                form = request.form

                nome = form["nome"]
                metaProj = form["metaProj"]
                metaFat = form["metaFat"]
                foto_ej = request.files["foto_ej"]

                filename = foto_ej.filename
                print("++++++++++++++++" + filename)
                filepath = os.path.join(current_app.root_path, 'static', 'fotos_ej', filename)
                foto_ej.save(filepath)

                entidade_ej = Ej(       nome=nome,
                                        imagem=filename,
                                        projetos_meta = metaProj,
                                        faturamento_meta = metaFat,
                                        projetos_atual = 0,
                                        faturamento_atual = 0)

                db.session.add(entidade_ej)
                db.session.commit()
                flash("Empresa cadastrada!")

                return redirect(url_for('principal.index'))

    return render_template('cadastro_ej.html')

@ej.route('/listar_ejs', methods = ['GET'])
def listar_ejs():
    lista = Ej.query.all()
    return render_template('listar_ejs.html', lista=lista)
