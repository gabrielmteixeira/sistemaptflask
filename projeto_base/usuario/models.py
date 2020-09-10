from projeto_base import db, login_manager
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import expression
from flask_login import UserMixin
from flask import session
from enum import Enum

import projeto_base.ej.models
import projeto_base.tarefa.models

usuario_urole_roles = {
                'USER': 'user',
                'ADMIN': 'admin'
              }

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):

    bcrypt = Bcrypt()

    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Integer, unique=False, nullable=False)
    login = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255),nullable = False)
    urole = db.Column(db.String(50), server_default="user", nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, server_default= expression.true())
    foto_trainee = db.Column(db.String(120))
    ej_id = db.Column(db.Integer, db.ForeignKey('ej.id'))
    ej = db.relationship('Ej')
    tarefas = db.relationship("TarefaTrainee", back_populates="trainee")

    def __init__(self, nome, login, senha, email, foto_trainee):
        self.nome = nome
        self.login = login
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')
        self.email = email
        self.foto_trainee = foto_trainee

    def checa_senha(self, senha):
        return self.bcrypt.check_password_hash(self.senha,senha)

    def setSenha(self, senha):
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')

    def get_tarefas(self):
        tarefas_list = []
        for assoc in self.tarefas:
            tarefas_list.append(assoc.tarefa)
        return tarefas_list
    
    def get_tarefas_coletivas(self):
        tarefas_coletivas = []
        
        for assoc in self.tarefas:
            if not assoc.tarefa.ehSolo:
                tarefas_coletivas.append(assoc.tarefa)
        
        return tarefas_coletivas

    def __repr__(self):
        return f"Login:{self.login}, Senha:{self.senha}"
