from pickleshare import *

db = PickleShareDB('~/testpickleshare')
db.clear()

def UsuarioExistente(nombre):
    return nombre in db.keys()

def AniadirUsuario(nombre, password):
    db[nombre] = password
    return None

def PasswordCorrecta(nombre, password):
    return password == db[nombre]