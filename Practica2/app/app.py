#./app/app.py
from ejercicios import ejercicio2, ejercicio3, ejercicio4, ejercicio5, ejercicio6, svg
from flask import Flask, render_template, url_for
import logging, random
from werkzeug.exceptions import HTTPException
from time import time

app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template('page_not_found.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ordena/<lista>')
def ordena(lista):
    lista = lista.split(',')
    #Calcular tiempo de ejecucion de la ordenación por burbuja
    tiempo_inicial = time()
    resultado_burbuja = ejercicio2.Burbuja(lista)
    tiempo_final = time()
    tiempo_ejecucion_burbuja = tiempo_final - tiempo_inicial
    #Calcular tiempo de ejecucion de la ordenación por quicksort
    tiempo_inicial = time()
    resultado_quickSort = ejercicio2.QuickSort(lista)
    tiempo_final = time()
    tiempo_ejecucion_quicksort = tiempo_final - tiempo_inicial
    lista = ','.join(resultado_quickSort)

    return render_template('ejercicios.html', ejercicio="Ejercicio 2. Ordena una lista de números:", resultado=f"La lista ordenada por burbuja es {lista}. El algoritmo burbuja ha tardado {tiempo_ejecucion_burbuja} segundos y el algoritmo quicksort ha tardado {tiempo_ejecucion_quicksort} segundos.")


@app.route('/criba/<numero>')
def criba(numero):
    resultado = ejercicio3.CribaEratostenes(int(numero))
    return render_template('ejercicios.html', ejercicio="Ejercicio 3. La Criba de Eratóstenes:", resultado=f"Los numeros primos de 1 a {numero} son {resultado}")


@app.route('/fibonacci/<numero>')
def Fibonacci(numero):
    resultado = ejercicio4.Fibonacci(int(numero))
    return render_template('ejercicios.html', ejercicio="Ejercicio 4. La sucesión de Fibonacci:", resultado=f"El termino {numero} de fibonacci es {resultado}")


# Comprobar es balanceada la cadena que le pasamos
@app.route('/balanceada/<secuencia>')
def EsBalanceada(secuencia):
    es_Balanceada = ejercicio5.esBalanceada(secuencia)
    if es_Balanceada:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada:", resultado=f"Nuestra secuencia es: {secuencia} y está balanceada")
    else:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada:", resultado=f"Nuestra secuencia es: {secuencia} y no está balanceada")


# Si no le pasamos ninguna cadena la generamos aleatoriamente
@app.route('/balanceada')
def EsBalanceadaAleatorio():
    secuencia = ejercicio5.secuenciaAleatoria()
    es_Balanceada = ejercicio5.esBalanceada(secuencia)
    if es_Balanceada:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada:", resultado=f"Nuestra secuencia es: {secuencia} y está balanceada")
    else:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada:", resultado=f"Nuestra secuencia es: {secuencia} y no está balanceada")


@app.route('/expresionRegular/<cadena>')
def ExpresionesRegulares(cadena):
    mensaje = ejercicio6.ExpresionesRegulares(cadena)
    return render_template('ejercicios.html', ejercicio="Ejercicio 6. Expresiones regulares:", resultado=mensaje)


@app.route('/svg')
def random_svg():
    imagen, nombre_imagen = svg.crearImagenSVG()
    return render_template('mostrar_svg.html', svg=f"Ejercicio Extra. SVG Dinámica: {nombre_imagen}", imagen=imagen)