def tarefasFeitas(tarefas, tarefaTrainee):
    listaTarefasFeitas = list()
    for tarefa in tarefas:
        for t in tarefaTrainee:
            if t.id_tarefa == tarefa.id:
                listaTarefasFeitas.append(tarefa)
    return listaTarefasFeitas