# Ejercicio 1
# Programe un mini-juego de "adivinar" un número (entre 1 y 100) que el ordenador establezca al azar. 
# El usuario puede ir introduciendo números y el ordenador le responderá con mensajes del estilo 
# "El número buscado el mayor / menor". El programa debe finalizar cuando el usuario adivine 
# el número (con su correspondiente mensaje de felicitación) o bien cuando el usuario haya realizado 
# 10 intentos incorrectos de adivinación.

def Adivina(numero_a_adivinar, entrada):
    if numero_a_adivinar == entrada:
        mensaje = f"Has dicho {entrada} y... Acertaste!!"
        alerta = "alert alert-success"
    elif numero_a_adivinar < entrada:
        mensaje = f"Has dicho {entrada} y... Mi número es menor!!"
        alerta = "alert alert-danger"
    elif numero_a_adivinar > entrada:
        mensaje = f"Has dicho {entrada} y... Mi número es mayor!!"
        alerta = "alert alert-danger"
    return mensaje, alerta