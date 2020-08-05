import os
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from projeto_base.ej.models import Ej
from projeto_base.usuario.models import Usuario, usuario_urole_roles
from projeto_base import db, login_required
from flask_login import LoginManager, current_user, login_user, logout_user

ej = Blueprint('ej', __name__, template_folder='templates')

@ej.route('/perfil/<id>')
def perfil_ej(id):
    def renderizaTemplate(entidade_ej):
        return render_template('perfil_ej.html',
                               entidade_ej = entidade_ej)
    
    entidade_ej = Ej.query.get_or_404(id)

    return renderizaTemplate(entidade_ej)

@ej.route('/cadastrar_ej', methods = ['POST', 'GET'])
@login_required(role=[usuario_urole_roles['ADMIN']])
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
@login_required(role=[usuario_urole_roles['ADMIN']])
def listar_ejs():
    lista = Ej.query.all()
    return render_template('listar_ejs.html', lista=lista)


@ej.route('/editar_ej/<id>', methods = ['GET', 'POST'])
@login_required(role=[usuario_urole_roles['ADMIN']])
def editar_ej(id):
    ej = Ej.query.filter_by(id=id).first_or_404()

    if request.method == 'POST':
        form = request.form

        _id = id
        ej = Ej.query.filter_by(id=_id).first_or_404()

        ej.nome = form['nome']             
        ej.projetos_meta = form['metaProj']             
        ej.faturamento_meta = form['metaFat']             
        ej.projetos_atual = form['atualProj']             
        ej.faturamento_atual = form['atualFat']

        foto = request.files['foto_ej']
        if foto.content_type != 'application/octet-stream':
            filename = foto.filename
            print("++++++++++++++++" + filename)
            filepath_novo = os.path.join(current_app.root_path, 'static', 'fotos_ej', filename)
            foto.save(filepath_novo)
            
            filepath_antigo = os.path.join(current_app.root_path, 'static', 'fotos_ej', )
            os.remove(filepath_antigo)        
            
            ej.imagem = filename

        db.session.commit()

        return redirect(url_for('ej.perfil_ej', id=id))

    return render_template('editar_ej.html', id=id, nome=ej.nome, metaProj=ej.projetos_meta, metaFat=ej.faturamento_meta, 
                                                            atualProj=ej.projetos_atual, atualFat=ej.faturamento_atual)


