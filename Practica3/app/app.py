#./app/app.py
from ejercicios import ejercicio1, ejercicio2, ejercicio3, ejercicio4, ejercicio5, ejercicio6
import model
from flask import Flask, flash, render_template, url_for, session, request, redirect
import logging, random, os
from werkzeug.exceptions import HTTPException
from time import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.before_request
def session_management():
  session.permanent = True

@app.errorhandler(HTTPException)
def handle_exception(e):
    flash('Ha intentado acceder a una URL que no existe.')
    if 'nombre' in session:
        nombre = session['nombre']
        return render_template('index.html', classAlert="alert alert-warning", mensaje_login=f" {nombre}", enlaces=getEnlacesRecientes()), 404
    else:
        return render_template('index.html', classAlert="alert alert-warning", mensaje_login=", registrate o inicia sesión.", enlaces=getEnlacesRecientes()), 404


@app.route('/')
def index():
    # Enlace reciente
    enlaces = EnlacesRecientes(url_for('index'), "Inicio")
    if 'nombre' in session:
        nombre = session['nombre']
        return render_template('index.html', mensaje_login=f" {nombre}", enlaces=enlaces)
    else:
        return render_template('index.html', mensaje_login=", registrate o inicia sesión.", enlaces=enlaces)

@app.route('/register')
def register():
    enlaces = EnlacesRecientes(url_for('register'), "Registrarse")
    return render_template('register.html', enlaces=enlaces)

@app.route('/registered', methods=['POST'])
def registered():
    nombre = request.form['nombre']
    if model.UsuarioExistente(nombre):
        flash('El nombre de usuario ya existe.')
        return render_template('register.html', classAlert="alert alert-danger")
    else:
        password = request.form['password']
        model.AniadirUsuario(nombre, password)
        flash('Te has registrado correctamente. Ahora puedes iniciar sesión.')
        # Actualizamos los enlaces recientes ya que cambiaremos al index
        enlaces = EnlacesRecientes(url_for('index'), "Inicio")
        return render_template('index.html', classAlert="alert alert-success", mensaje_login=", registrate o inicia sesión.", enlaces=enlaces)

@app.route('/login')
def login():
    enlaces = EnlacesRecientes(url_for('login'), "Iniciar Sesión")
    return render_template('login.html', enlaces=enlaces)

@app.route('/logged', methods=['POST'])
def logged():
    nombre = request.form['nombre']
    password = request.form['password']
    if model.UsuarioExistente(nombre):
        if model.PasswordCorrecta(nombre, password):
            flash('Has iniciado sesión correctamente.')
            session['nombre'] = nombre
            session['password'] = password
            # Actualizamos los enlaces recientes ya que cambiaremos al index
            enlaces = EnlacesRecientes(url_for('index'), "Inicio")
            return render_template('index.html', classAlert="alert alert-success", mensaje_login=f" {nombre}", enlaces=enlaces)
        else:
            flash('La contraseña no es correcta.')
            return render_template('login.html', classAlert="alert alert-danger")
    else:
        flash('El usuario no existe.')
        return render_template('login.html', classAlert="alert alert-danger")

@app.route('/logout')
def logout():
    session.pop('nombre',None)
    session.pop('password',None)
    session.clear()
    flash('Tu sesión se ha cerrado correctamente.')
    # Actualizamos los enlaces recientes ya que cambiaremos al index
    enlaces = EnlacesRecientes(url_for('index'), "Inicio")
    return render_template('index.html', classAlert="alert alert-success", mensaje_login=", registrate o inicia sesión.", enlaces=enlaces)

# Creamos los enlaces recientes de la sesion con una lista de diccionarios para guardar el mensaje
# que se mostrará y la url generada por el url_for()
def EnlacesRecientes(href, mensaje):
    if  not 'ultima_visita_href' in session:
        session['ultima_visita_href'] = href
        session['ultima_visita_mensaje'] = mensaje
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']} ]
        return enlaces
    elif not 'penultima_visita_href' in session:
        session['penultima_visita_href'] = session['ultima_visita_href']
        session['penultima_visita_mensaje'] = session['ultima_visita_mensaje']
        session['ultima_visita_href'] = href
        session['ultima_visita_mensaje'] = mensaje
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']}, 
                    { 'href': session['penultima_visita_href'], 'mensaje': session['penultima_visita_mensaje']}
                  ]
        return enlaces
    else:
        session['antepenultima_visita_href'] = session['penultima_visita_href']
        session['antepenultima_visita_mensaje'] = session['penultima_visita_mensaje']
        session['penultima_visita_href'] = session['ultima_visita_href']
        session['penultima_visita_mensaje'] = session['ultima_visita_mensaje']
        session['ultima_visita_href'] = href
        session['ultima_visita_mensaje'] = mensaje
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']}, 
                    { 'href': session['penultima_visita_href'], 'mensaje': session['penultima_visita_mensaje']},
                    { 'href': session['antepenultima_visita_href'], 'mensaje': session['antepenultima_visita_mensaje']}
                  ]
    return enlaces

def getEnlacesRecientes():
    if  not 'ultima_visita_href' in session:
        enlaces = [ ]
        return enlaces
    elif not 'penultima_visita_href' in session:
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']} ]
        return enlaces
    elif not 'antepenultima_visita_href' in session:
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']}, 
                    { 'href': session['penultima_visita_href'], 'mensaje': session['penultima_visita_mensaje']}
                  ]
        return enlaces
    else:
        enlaces = [ { 'href': session['ultima_visita_href'], 'mensaje': session['ultima_visita_mensaje']}, 
                    { 'href': session['penultima_visita_href'], 'mensaje': session['penultima_visita_mensaje']},
                    { 'href': session['antepenultima_visita_href'], 'mensaje': session['antepenultima_visita_mensaje']}
                  ]
    return enlaces
    
#########################################
######### EJERCICIOS PRACTICA 1 #########
#########################################

@app.route('/adivina')
def Adivina():
    enlaces = EnlacesRecientes(url_for('Adivina'), "Ejercicio 1")
    return render_template('ejercicio1.html', ejercicio="Ejercicio 1. Adivine el número", enlaces=enlaces)

@app.route('/adivina', methods=['POST'])  
def PruebaAdivina():
    enlaces = EnlacesRecientes(url_for('Adivina'), "Ejercicio 1")
    if  not 'numero_a_adivinar' in session:
        session['numero_a_adivinar'] = random.randint(0, 100)

    entrada = int(request.form['numero'])
    mensaje, alerta = ejercicio1.Adivina(session['numero_a_adivinar'],entrada)
    flash(mensaje)
    # Si hemos acertado el numero se deja de ejecutar por lo que generamos otro numero
    if alerta == "alert alert-success":
        session.pop('numero_a_adivinar',None)

    return render_template('ejercicio1.html', ejercicio="Ejercicio 1. Adivine el número", classAlert=alerta, enlaces=enlaces)

@app.route('/ordena/<lista>')
def Ordena(lista):
    enlaces = EnlacesRecientes(url_for('Ordena', lista='6,4,9,1,2,5,3'), "Ejercicio 2")
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

    return render_template('ejercicios.html', ejercicio="Ejercicio 2. Ordena una lista de números", resultado=f"La lista ordenada por burbuja es {lista}. El algoritmo burbuja ha tardado {tiempo_ejecucion_burbuja} segundos y el algoritmo quicksort ha tardado {tiempo_ejecucion_quicksort} segundos.", enlaces=enlaces)

@app.route('/criba/<numero>')
def Criba(numero):
    enlaces = EnlacesRecientes(url_for('Criba', numero=78), "Ejercicio 3")
    resultado = ejercicio3.CribaEratostenes(int(numero))
    return render_template('ejercicios.html', ejercicio="Ejercicio 3. La Criba de Eratóstenes", resultado=f"Los numeros primos de 1 a {numero} son {resultado}", enlaces=enlaces)

@app.route('/fibonacci/<numero>')
def Fibonacci(numero):
    numero = random.randint(1, 50)
    enlaces = EnlacesRecientes(url_for('Fibonacci', numero=12), "Ejercicio 4")
    resultado = ejercicio4.Fibonacci(int(numero))
    return render_template('ejercicios.html', ejercicio="Ejercicio 4. La sucesión de Fibonacci", resultado=f"El termino {numero} de fibonacci es {resultado}", enlaces=enlaces)

@app.route('/balanceada')
def EsBalanceadaAleatorio():
    enlaces = EnlacesRecientes(url_for('EsBalanceadaAleatorio'), "Ejercicio 5")
    secuencia = ejercicio5.secuenciaAleatoria()
    es_Balanceada = ejercicio5.esBalanceada(secuencia)
    if es_Balanceada:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada", resultado=f"Nuestra secuencia es: {secuencia} y está balanceada", enlaces=enlaces)
    else:
        return render_template('ejercicios.html', ejercicio="Ejercicio 5. Cadena balanceada", resultado=f"Nuestra secuencia es: {secuencia} y no está balanceada", enlaces=enlaces)

@app.route('/expresionRegular/<cadena>')
def ExpresionesRegulares(cadena):
    enlaces = EnlacesRecientes(url_for('ExpresionesRegulares', cadena='antonio@gmail.com'), "Ejercicio 6")
    mensaje = ejercicio6.ExpresionesRegulares(cadena)
    return render_template('ejercicios.html', ejercicio="Ejercicio 6. Expresiones regulares", resultado=mensaje, enlaces=enlaces)

