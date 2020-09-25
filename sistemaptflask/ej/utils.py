def calcula_chart_grid(valorMeta):
    for i in range(3, 8):
        if(valorMeta % i == 0):
            return (valorMeta / i)