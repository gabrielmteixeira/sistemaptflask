from projeto_base import db
import projeto_base.usuario.models

TarefaTrainee = db.Table("tarefaTrainee",
                    db.Column('id_trainee', db.Integer, db.ForeignKey('usuario.id')),
                    db.Column('id_tarefa', db.Integer, db.ForeignKey('tarefa.id')),
                    db.Column('feita', db.Boolean))


                    

class Tarefa(db.Model): 

    __tablename__ = 'tarefa'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, unique=True, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    icone = db.Column(db.String)
    prazo = db.Column(db.String)
    ehSolo = db.Column(db.Boolean)
    trainees = db.relationship("Usuario", secondary=TarefaTrainee, back_populates="tarefas")

    def __init__(self, titulo, descricao, icone, prazo, ehSolo):
        self.titulo = titulo
        self.descricao = descricao 
        self.icone = icone 
        self.prazo = prazo
        self.ehSolo = ehSolo

    def __repr__(self):
        return f'Tarefa: {self.titulo}' 

