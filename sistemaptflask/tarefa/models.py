from sistemaptflask import db
import sistemaptflask.usuario.models

class TarefaTrainee(db.Model):
    __tablename__ = 'tarefaTrainee'
    id_trainee = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    id_tarefa = db.Column(db.Integer, db.ForeignKey('tarefa.id'), primary_key=True)
    atrasada = db.Column(db.Boolean)
    trainee = db.relationship("Usuario", back_populates="tarefas")
    tarefa = db.relationship("Tarefa", back_populates="trainees")
    
    def __init__(self, tarefa, trainee):
        self.tarefa = tarefa
        self.trainee = trainee

    def __repr__(self):
        return f'TarefaTrainee: {self.id_tarefa}/{self.id_trainee}' 

class Tarefa(db.Model): 

    __tablename__ = 'tarefa'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), unique=True, nullable=False)
    descricao = db.Column(db.Text(), nullable=False)
    icone = db.Column(db.String(255))
    prazo = db.Column(db.String(100))
    ehSolo = db.Column(db.Boolean)
    trainees = db.relationship("TarefaTrainee", back_populates="tarefa")

    def __init__(self, titulo, descricao, icone, prazo, ehSolo):
        self.titulo = titulo
        self.descricao = descricao 
        self.icone = icone 
        self.prazo = prazo
        self.ehSolo = ehSolo

    def __repr__(self):
        return f'Tarefa: {self.titulo}' 
    
    def get_trainees(self):
        trainees_list = []
        for assoc in self.trainees:
            trainees_list.append(assoc.trainee)
        return trainees_list


