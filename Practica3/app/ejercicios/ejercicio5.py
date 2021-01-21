import math
import random

def esBalanceada(secuencia):
    abierto = 0
    if len(secuencia) % 2 == 0 and len(secuencia) > 0:
        if secuencia[0] == ']':
            return False
        else:
            for i in secuencia:
                if i == '[':
                    abierto += 1
                elif i == ']':
                    if abierto > 0:
                        abierto -= 1
                    else:
                        return False
            if abierto == 0:
                return True
            else:
                return False
    else:
        return False

def secuenciaAleatoria():
    tamanio_secuencia = random.randint(1, 10)
    opciones = ['[', ']']
    secuencia = ''

    for iter in range(tamanio_secuencia):
        secuencia += random.choice(opciones)
    
    return secuencia