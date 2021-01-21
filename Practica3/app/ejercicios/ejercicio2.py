def Burbuja(lista):
    copia_lista = [int(x) for x in lista]
    for i in range(len(copia_lista)):
        for j in range(len(copia_lista)-i-1):
            if copia_lista[j] > copia_lista[j+1]:
                aux = copia_lista[j]
                copia_lista[j] = copia_lista[j+1]
                copia_lista[j+1] = aux
    lista = [str(x) for x in copia_lista]
    return lista


def QuickSort(lista):
    izquierda = []
    centro = []
    derecha = []
    if len(lista) > 1:
        pivote = lista[0]
        for i in lista:
            if i < pivote:
                izquierda.append(i)
            elif i == pivote:
                centro.append(i)
            elif i > pivote:
                derecha.append(i)
        return QuickSort(izquierda) + centro + QuickSort(derecha)
    else:
        return lista

        