import random

def crearImagenSVG():
    # Creamos 2 listas para las posibles opciones de figuras y de colores
    imagenes = ['circle', 'rect', 'line']
    colores = ['red', 'green', 'blue', 'black', 'orange', 'violet', 'purple', 'yellow', 'fuchsia', 'snow', 'darkRed', 'coral', 'mediumPurple', 'orangeRed', 'navy', 'saddleBrown', 'cyan']

    imagen = random.choice(imagenes)          # Elegimos una figura aleatoriamente
    color = random.choice(colores)            # Elegimos un color de borde aleatorio
    color_relleno = random.choice(colores)    # Elegimos un color de relleno aleatorio

    aux_img = imagen
    nombre_imagen = {
        "rect": "Rectangulo",                 # Diccionario usado para el nombre del objeto creado
        "circle": "Círculo",                  # Será utilizado en el front-end
        "line": "Línea"
    }

    # Dependiendo de la figura elegida aleatoriamente se generarán puntos aleatorios y se compondrá el código HTML que generará la figura
    if imagen=='circle':
        cx = random.randint(50, 500)
        cy = random.randint(50, 200)
        r = random.randint(30, 80)
        imagen = imagen + ' cx=' + str(cx) + ' cy=' + str(cy) + ' r=' + str(r)
    elif imagen=='line':
        x1 = random.randint(10, 75)
        y1 = random.randint(10, 300)
        x2 = random.randint(76, 150)
        y2 = random.randint(10, 300)
        imagen = imagen + ' x1=' +  str(x1) + ' y1=' + str(y1) + ' x2=' + str(x2) + ' y2=' + str(y2)
    elif imagen=='rect':
        x = random.randint(10, 500)
        y = random.randint(10, 200)
        width = random.randint(50, 200)
        height = random.randint(50, 200)
        imagen = imagen + ' x=' + str(x) + ' y=' + str(y) + ' width=' + str(width) + ' height=' + str(height)
    imagen = imagen + ' stroke=' + color + ' stroke-width=4 fill=' + color_relleno

    return imagen, nombre_imagen[aux_img]