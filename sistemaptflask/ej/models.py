from sistemaptflask import db
import sistemaptflask.usuario.models

class Ej(db.Model):

    __tablename__ = 'ej'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    imagem = db.Column(db.String(255))
    usuarios = db.relationship('Usuario', lazy=True)

    def __init__(self, nome, imagem):
        self.nome = nome
        self.imagem = imagem

    def __repr__(self):
        return f'EJ: {self.nome}'

    def tem_membros(self):
        return len(self.usuarios) > 0

    def getMembros(self):
        membros = list()
        for membro in self.usuarios:
            membros.append(membro)
        return membros