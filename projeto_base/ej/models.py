from projeto_base import db
import projeto_base.usuario.models

class Ej(db.Model):

    __tablename__ = 'ej'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    imagem = db.Column(db.String, nullable=False)
    projetos_meta = db.Column(db.Integer)
    faturamento_meta = db.Column(db.Integer)
    projetos_atual = db.Column(db.Integer)
    faturamento_atual = db.Column(db.Integer)
    usuarios = db.relationship('Usuario', lazy=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f'EJ: {self.nome}'