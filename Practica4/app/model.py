from datetime import datetime
from pymongo import MongoClient
import logging
import re
from bson.objectid import ObjectId


# Variables MongoDB
client = MongoClient("mongo", 27017)  # Conectar al servicio (docker) "mongo" en su puerto estandar
db = client.SampleCollections         # Elegimos la base de datos de ejemplo
collection_usuarios = db['Usuarios']  # Creamos la coleccion de usuarios registrados de la web


def usuario_existente(nombre):
    if collection_usuarios.find_one({"usuario": nombre}) == None:
        return False
    else:
        return True


def aniadir_usuario(nombre, password):
    now = datetime.now()
    nuevo_usuario = {                              # Creamos un documento de ejemplo
        'usuario': nombre,
        'password': password,
        'fecha_registro': now
    }
    collection_usuarios.insert_one(nuevo_usuario)   # Insertamos el documento
    return None


def password_correcta(nombre, password):
    return password == collection_usuarios.find_one({"usuario": nombre})['password']


def select_documento_by_id(document_id, name_collection):
    _id = ObjectId(document_id)
    if name_collection == "usuarios":
        result = db.Usuarios.find({'_id': ObjectId(_id)})
    elif name_collection == "friends":
        result = db.samples_friends.find({'_id': ObjectId(_id)})

    lista_collection = []     # Devuelve la consulta en formato lista
    for document in result:
        lista_collection.append(document)

    return lista_collection


def busqueda(busqueda, name_collection):
    xreg = re.compile(f'([0-9A-Za-z]*){busqueda}([0-9A-Za-z]*)')
    if name_collection == "usuarios":
        result = db.Usuarios.find({'usuario': xreg})
    elif name_collection == "friends":
        result = db.samples_friends.find({'name': xreg})

    lista_collection = []     # Devuelve la consulta en formato lista
    for document in result:
        lista_collection.append(document)

    return lista_collection

def editar_usuario(document_id, usuario, nuevo_usuario, password):
    _id = ObjectId(document_id)
    db.Usuarios.find_and_modify(query={'_id':ObjectId(_id)}, update={"$set": {'usuario': nuevo_usuario, 'password': password}}, upsert=False, full_response= True)
    result = select_documento_by_id(document_id, "usuarios")
    lista_collection = []     # Devuelve la consulta en formato lista
    for document in result:
        lista_collection.append(document)

    return lista_collection

def editar_capitulo(document_id, titulo, nuevo_titulo, temporada, numero, fecha, resumen):
    _id = ObjectId(document_id)
    db.samples_friends.find_and_modify(query={'_id':ObjectId(_id)}, update={"$set": {'name': nuevo_titulo, 'season': temporada, 'number': numero, 'airdate': fecha, 'summary': resumen}}, upsert=False, full_response= True)
    result = select_documento_by_id(document_id, "friends")
    lista_collection = []     # Devuelve la consulta en formato lista
    for document in result:
        lista_collection.append(document)
    return lista_collection 

def aniadir_capitulo(titulo, temporada, numero, fecha, resumen):
    capitulo = {
        'name': titulo,
        'season': temporada,
        'number': numero,
        'airdate': fecha,
        'summary': resumen
    }
    db.samples_friends.insert_one(capitulo)
    result = busqueda("", "friends")
    lista_collection = []     # Devuelve la consulta en formato lista
    for document in result:
        lista_collection.append(document)
    return lista_collection


def eliminar_documento(name_collection, document_id):
    _id = ObjectId(document_id)
    if name_collection == "usuarios":
        db.Usuarios.delete_one({'_id': _id})
    elif name_collection == "friends":
        db.samples_friends.delete_one({'_id': _id})
        
    return None
