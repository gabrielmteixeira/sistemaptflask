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