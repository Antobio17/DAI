def CribaEratostenes(numero):
    criba = []
    for i in range(numero+1):
        criba.append(i)
    criba.remove(0)
    
    contador = 0
    total = len(criba)
    esprimo = True

    while contador <= total:
        aux = 2
        esprimo = True
        while aux <= contador/2 and esprimo != False :
            esprimo = contador%aux
            if esprimo == False:
                criba.remove(contador)
            aux = aux+1
        contador = contador+1

    return criba