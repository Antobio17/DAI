#./app/app.py
from ejercicios import ejercicio1, ejercicio2, ejercicio3, ejercicio4, ejercicio5, ejercicio6
import model
from flask import Flask, flash, render_template, url_for, session, request, redirect
import logging, random, os
from werkzeug.exceptions import HTTPException
from time import time

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Variable global para el numero de documentos a filtrar
global n_documentos_filtrado
n_documentos_filtrado = 8

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
        return render_template('index.html', classAlert="alert alert-warning", mensaje_login=", regístrate o inicia sesión.", enlaces=getEnlacesRecientes()), 404


# Metodo para mostrar la coleccion
@app.route('/<name_collection>')
def mostrar_collection(name_collection):
    global n_documentos_filtrado                          # Usamos la variable declarada como global al principio para el numero de documentos a mostrar
    n_pagina = 1                                          # Pagina inicial de la tabla

    return calcular_render("", name_collection, n_pagina, n_documentos_filtrado, "")


# Metodo para el filtrado de la coleccion
@app.route('/<name_collection>', methods=['POST'])
def filtrar(name_collection):
    global n_documentos_filtrado
    n_documentos_filtrado = int(request.form['n_elementos'])   # Vemos sin ha cambiado el numero de documentos a mostrar en nuestro filtro
    n_pagina = 1                                               # Volvemos a poner a 1 la página por haber aplicado un filtro

    busqueda = request.form['busqueda']                        # Almacenamos en una variable lo que se haya mandado en el formulario para buscar
                                                               # si no se ha escrito nada obtendremos ""
    return calcular_render(busqueda, name_collection, n_pagina, n_documentos_filtrado, "")


# Metodo para gestionar la paginación en las tablas mostradas
@app.route('/<name_collection>/<int:pagina>', methods=['POST'])
def pagina(name_collection, pagina):
    global n_documentos_filtrado

    busqueda = request.form['busqueda']        # Guardamos si hay alguna búsqueda activa con un input de tipo hidden en el formulario usado para la paginacion

    return calcular_render(busqueda, name_collection, pagina, n_documentos_filtrado, "")


# Metodo para editar entrada
@app.route('/editar/<name_collection>/<document_id>', methods=['POST'])
def editar(name_collection, document_id):
    list_collection = model.select_documento_by_id(document_id, name_collection)

    template = 'editar_' + name_collection + '.html'           # Calcular el template que se va a utilizar
    return render_template(template, collection=list_collection)


# Metodo para editar entrada
@app.route('/editado/<name_collection>/<document_id>', methods=['POST'])
def editado(name_collection, document_id):
    if name_collection == "usuarios":
        usuario = request.form['usuario']
        nuevo_usuario = request.form['nuevo_usuario']
        password = request.form['password']
        list_collection = model.editar_usuario(document_id, usuario, nuevo_usuario, password)

    elif name_collection == "friends":
        titulo = request.form['titulo']
        nuevo_titulo = request.form['nuevo_titulo']
        temporada = request.form['temporada']
        numero = request.form['numero']
        fecha = request.form['fecha']
        resumen = '<p>'+request.form['resumen']+'</p>'
        list_collection = model.editar_capitulo(document_id, titulo, nuevo_titulo, temporada, numero, fecha, resumen)

    flash('Editado correctamente')
    template = 'editar_' + name_collection + '.html'           # Calcular el template que se va a utilizar
    return render_template(template, collection=list_collection, classAlert="alert alert-success")


# Metodo para eliminar entrada
@app.route('/eliminar/<name_collection>/<document_id>', methods=['POST'])
def eliminar(name_collection, document_id):
    return render_template('eliminar_documento.html', name_collec=name_collection, document_id=document_id)


# Metodo para confirmar eliminacion
@app.route('/eliminado/<name_collection>', methods=['POST'])
def eliminado(name_collection):
    global n_documentos_filtrado                          # Usamos la variable declarada como global al principio para el numero de documentos a mostrar

    _id = request.form['document_id']
    model.eliminar_documento(name_collection, _id)
    flash('Borrado correctamente.')
    return calcular_render("", name_collection, 1, n_documentos_filtrado, "alert alert-success")


# Metodo para cancelar la eliminacion
@app.route('/cancelado/<name_collection>', methods=['POST'])
def cancelado(name_collection):
    global n_documentos_filtrado

    flash('Borrado cancelado.')
    return calcular_render("", name_collection, 1, n_documentos_filtrado, "alert alert-warning")


# Metodo muestra el formulario para añadir un capitulo
@app.route('/nuevo/friends')
def aniadir_capitulo():
    return render_template('aniadir_capitulo.html')


@app.route('/aniadido/friends', methods=['POST'])
def aniadir_capitulo_bd():
    global n_documentos_filtrado                          # Usamos la variable declarada como global al principio para el numero de documentos a mostrar

    titulo = request.form['titulo']
    temporada = request.form['temporada']
    numero = request.form['numero']
    fecha = request.form['fecha']
    resumen = '<p>'+request.form['resumen']+'</p>'
    model.aniadir_capitulo(titulo, temporada, numero, fecha, resumen)

    n_pagina = 1                                          # Pagina inicial de la tabla

    flash('Capitulo añadido con exito.')
    return calcular_render("", "friends", n_pagina, n_documentos_filtrado, "alert alert-success")


# Metodo para calcular el render junto a todas sus variables y mostrar la pagina
def calcular_render(busqueda, collection, n_pag, n_docs_f, flash_alert):
    inicio = (n_pag-1) * n_docs_f                         # Calcular el primer documento a mostrar en el numero de pagina actual
    fin = inicio + n_docs_f                               # Calcular el ultimo documento a mostrar el numero de la pagina actual

    lista_collection = model.busqueda(busqueda, collection)    # Realizamos el query (sin filtro porque es la pagina principal)
    template = 'collection_' + collection + '.html'            # Calcular el template que se va a utilizar
    is_empty = (len(lista_collection) == 0)                    # Variable usada para saber si la lista esta vacia y mostrar un mensaje en el HTML

    if fin >= len(lista_collection):                       # Calcular si es el final de la lista para que no haya desbordamiento
        fin = len(lista_collection)                        # Recalcular el ultimo documento a mostrar el numero de la pagina actual                         
        final_lista = True
    else:
        final_lista = False
    
    if flash_alert == "":
        return render_template(template, collection=lista_collection, n_documentos_filtrados=n_docs_f, inicio=inicio, fin=fin, pagina=n_pag, is_empty=is_empty, final_lista=final_lista, busqueda=busqueda)
    else:
        return render_template(template, collection=lista_collection, n_documentos_filtrados=n_docs_f, inicio=inicio, fin=fin, pagina=n_pag, is_empty=is_empty, final_lista=final_lista, busqueda=busqueda, classAlert=flash_alert)


@app.route('/')
def index():
    # Enlace reciente
    enlaces = EnlacesRecientes(url_for('index'), "Inicio")
    if 'nombre' in session:
        nombre = session['nombre']
        return render_template('index.html', mensaje_login=f" {nombre}", enlaces=enlaces)
    else:
        return render_template('index.html', mensaje_login=", regístrate o inicia sesión.", enlaces=enlaces)

@app.route('/register')
def register():
    enlaces = EnlacesRecientes(url_for('register'), "Registrarse")
    return render_template('register.html', enlaces=enlaces)

@app.route('/registered', methods=['POST'])
def registered():
    nombre = request.form['nombre']
    if model.usuario_existente(nombre):
        flash('El nombre de usuario ya existe.')
        return render_template('register.html', classAlert="alert alert-danger")
    else:
        password = request.form['password']
        model.aniadir_usuario(nombre, password)
        flash('Te has registrado correctamente. Ahora puedes iniciar sesión.')
        # Actualizamos los enlaces recientes ya que cambiaremos al index
        enlaces = EnlacesRecientes(url_for('index'), "Inicio")
        return render_template('index.html', classAlert="alert alert-success", mensaje_login=", regístrate o inicia sesión.", enlaces=enlaces)

@app.route('/login')
def login():
    enlaces = EnlacesRecientes(url_for('login'), "Iniciar Sesión")
    return render_template('login.html', enlaces=enlaces)

@app.route('/logged', methods=['POST'])
def logged():
    nombre = request.form['nombre']
    password = request.form['password']
    if model.usuario_existente(nombre):
        if model.password_correcta(nombre, password):
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
    return render_template('index.html', classAlert="alert alert-success", mensaje_login=", regístrate o inicia sesión.", enlaces=enlaces)

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

