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