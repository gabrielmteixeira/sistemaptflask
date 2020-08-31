from datetime import datetime

def data_format_in(data):
    data_format = data.split('-')
    data_format.reverse()
    prazo = '/'.join(data_format)

    return prazo

def data_format_out(data):
    data_format = data.split('/')
    data_format.reverse()
    prazo = '-'.join(data_format)

    return prazo

def define_solo_in(solo):
    ehSolo = False
    if(solo == 'sim'):
        ehSolo = True
    
    return ehSolo

def define_solo_out(ehSolo):
    solo = ''
    if(ehSolo == 0):
        solo = 'não'
    else: 
        solo = 'sim'

    return solo

def confere_prazo_tarefa(tarefaTrainee):
    d1 = datetime.today()
    d2 = datetime.strptime(tarefaTrainee.tarefa.prazo, '%d/%m/%Y')
    
    delta = (d1 - d2)
    
    if delta.days > 0:
        tarefaTrainee.atrasada = True
    else:
        tarefaTrainee.atrasada = False