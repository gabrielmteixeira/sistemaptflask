from projeto_base import db
import projeto_base.usuario.models

class Ej(db.Model):

    __tablename__ = 'ej'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    imagem = db.Column(db.String, nullable=False)
    usuarios = db.relationship('Usuario', backref='ej', lazy=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return f'EJ: {self.nome}'