from projeto_base import db
import projeto_base.usuario.models

class Ej(db.Model):

    __tablename__ = 'ej'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    imagem = db.Column(db.String)
    cnpj = db.Column(db.String, unique=True)
    projetos_meta = db.Column(db.Integer)
    faturamento_meta = db.Column(db.Integer)
    projetos_atual = db.Column(db.Integer)
    faturamento_atual = db.Column(db.Integer)
    usuarios = db.relationship('Usuario', lazy=True)

    def __init__(self, nome, cnpj, projetos_meta, projetos_atual, faturamento_atual, faturamento_meta, imagem):
        self.nome = nome
        self.cnpj = cnpj
        self.projetos_meta = projetos_meta
        self.projetos_atual = projetos_atual
        self.faturamento_atual = faturamento_atual
        self.faturamento_meta = faturamento_meta
        self.imagem = imagem

    def __repr__(self):
        return f'EJ: {self.nome}'

    def tem_membros(self):
        return len(self.usuarios) > 0