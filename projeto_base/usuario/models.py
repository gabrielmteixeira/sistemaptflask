from projeto_base import db, login_manager
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import expression
from flask_login import UserMixin
from flask import session
from enum import Enum

import projeto_base.ej.models

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
    login = db.Column(db.String(255), unique=True)
    senha = db.Column(db.String(255),nullable = False)
    urole = db.Column(db.String(50), server_default="user", nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    active = db.Column(db.Boolean, server_default= expression.true())
    ej_id = db.Column(db.Integer, db.ForeignKey('ej.id'))
    ej = db.relationship('Ej')

    def __init__(self, login, senha, email):
        self.login = login
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')
        self.email = email

    def checa_senha(self, senha):
        return self.bcrypt.check_password_hash(self.senha,senha)

    def setSenha(self, senha):
        self.senha = self.bcrypt.generate_password_hash(senha).decode('utf-8')

    def __repr__(self):
        return f"Login:{self.login}, Senha:{self.senha}"
