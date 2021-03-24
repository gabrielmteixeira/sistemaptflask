import os
from functools import wraps
from flask import Flask, render_template, current_app
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail   

login_manager = LoginManager()

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

############################################################
################## BANCO DE DADOS ##########################
############################################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                                            "pool_recycle": 10
                                          }
#app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db, compare_type = True)

#############################################################
########### VARIÁVEIS/FUNÇÕES DO TEMPLATE ###################
#############################################################
from sistemaptflask.usuario.models import usuario_urole_roles
@app.context_processor
def insere_usuario_urole_roles():
    return dict(usuario_urole_roles=usuario_urole_roles)

############################################################
######################## EMAIL #############################
############################################################


app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS']= os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)


#############################################################
################## CONFIGURA LOGIN ##########################
#############################################################

#Conferir se não tem que mudar nada antes de descomentar o trecho abaixo (apague este comentário depois de conferir)

login_manager.init_app(app)
login_manager.login_view = "usuario.login"
login_manager.login_message = "Não foi possível acessar esta página ou executar esta ação. Por favor confira se o login foi feito ou se você tem a devida permissão."

def login_required(role=["ANY"]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
               return current_app.login_manager.unauthorized()
            urole = current_user.urole
            if ( (urole not in role) and (role != ["ANY"])):
                return current_app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

#############################################################
####################### MODELS ##############################
#############################################################

from sistemaptflask.usuario.models import Usuario
from sistemaptflask.ej.models import Ej

#############################################################
####################### BLUEPRINTS ##########################
#############################################################

from sistemaptflask.principal.views import principal
from sistemaptflask.usuario.views import usuario
from sistemaptflask.usuario.admin_views import admin
from sistemaptflask.ej.views import ej
from sistemaptflask.tarefa.views import tarefa

app.register_blueprint(principal)
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(ej, url_prefix='/ej')
app.register_blueprint(tarefa, url_prefix='/tarefa')