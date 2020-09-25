from sistemaptflask.tarefa.models import Tarefa, TarefaTrainee
from sistemaptflask.usuario.models import Usuario
from sistemaptflask.ej.models import Ej

def get_ejs_destaque():
    tarefas = Tarefa.query.filter_by(ehSolo=0).all()
    ejs = Ej.query.all()

    ejs_em_destaque = []
    for ej in ejs:
        fizeram_todas_as_tarefas = []
        
        if(ej.tem_membros()):
            for membro in ej.usuarios:
                if len(membro.get_tarefas_coletivas()) == len(tarefas):
                    fizeram_todas_as_tarefas.append(True)
                else:
                    fizeram_todas_as_tarefas.append(False)

            if all(fizeram_todas_as_tarefas):
                ejs_em_destaque.append(ej)

    return ejs_em_destaque

