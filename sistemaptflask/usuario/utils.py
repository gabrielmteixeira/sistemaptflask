from sistemaptflask.tarefa.models import Tarefa

def tarefasNaoEntregues(trainee):
    todasTarefas = Tarefa.query.all()
    tarefas = trainee.get_tarefas()
    tarefasNaoEntreguesLista = todasTarefas
    for tarefa in todasTarefas[:]:
        if tarefa in tarefas:
            tarefasNaoEntreguesLista.remove(tarefa)
    return tarefasNaoEntreguesLista

def getQuantidadeTarefasPendentes(trainee):
    tarefas = tarefasNaoEntregues(trainee)
    return len(tarefas)