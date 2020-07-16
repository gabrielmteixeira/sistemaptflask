import os
from functools import wraps
from flask import Flask, render_template, current_app
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flask_mail import Mail     --> Quando usar e-mail, precisa dessa biblioteca

login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

############################################################
################## BANCO DE DADOS ##########################
############################################################

app.config['SQLALCHEMY_DATABASE_URI'] =  "mysql+pymysql://projeto_base:pierre@lindo1@projeto_base.mysql.dbaas.com.br/projeto_base"
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
from projeto_base.usuario.models import usuario_urole_roles
@app.context_processor
def insere_usuario_urole_roles():
    return dict(usuario_urole_roles=usuario_urole_roles)

############################################################
######################## EMAIL #############################
############################################################

# EMAIL DEVE SER CONFIGURADO ANTES DE USAR (apague este comentário depois de configurar)
''' 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME'] = 'cudolarrypage@gmail.com'
app.config['MAIL_PASSWORD'] = 'daniel2019'
'''

#############################################################
################## CONFIGURA LOGIN ##########################
#############################################################

#Conferir se não tem que mudar nada antes de descomentar o trecho abaixo (apague este comentário depois de conferir)

login_manager.init_app(app)
login_manager.login_view = "principal.index"
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

from projeto_base.usuario.models import Usuario

#############################################################
####################### BLUEPRINTS ##########################
#############################################################

from projeto_base.principal.views import principal
from projeto_base.usuario.views import usuario
from projeto_base.usuario.admin_views import admin

app.register_blueprint(principal)
app.register_blueprint(usuario, url_prefix='/usuario')
app.register_blueprint(admin, url_prefix='/admin')