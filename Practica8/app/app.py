#http -v http://0.0.0.0:5000/api/friends        GET
#http -f POST http://0.0.0.0:5000/api/friends name=prueba season=89.0 number=100.0 airdate=2020/12/01 summary="El resumen es este"       POST
#http -v http://0.0.0.0:5000/api/friends/5fc58a5ffdbbb3a2679d40ce      GET
#http -f PUT http://0.0.0.0:5000/api/friends/5fc58a5ffdbbb3a2679d40ce name=prueba_editado season=90.0 number=110.0 airdate=2020/12/02 summary="El resumen es este editado"
#http DELETE http://0.0.0.0:5000/api/friends/5fc58a5ffdbbb3a2679d40ce

#./app/app.py
from flask import Flask, request, jsonify, render_template
import logging, os, re
from werkzeug.exceptions import HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
# Variables MongoDB
client = MongoClient("mongo", 27017)  # Conectar al servicio (docker) "mongo" en su puerto estandar
db = client.SampleCollections         # Elegimos la base de datos de ejemplo

@app.route('/')
def index():
    # Enlace reciente
    return render_template('index.html')


@app.route('/api/friends', methods=['GET', 'POST'])
def api_1():
    if request.method == 'GET':
        lista = []
        if request.args.get('name') != None:
            value = str(request.args.get('name'))
            episodios = db.samples_friends.find({'name': value})
        elif request.args.get('season') != None:
            value = float(request.args.get('season'))
            episodios = db.samples_friends.find({'season': value})
        elif request.args.get('number') != None:
            value = float(request.args.get('number'))
            episodios = db.samples_friends.find({'number': value})
        elif request.args.get('airdate') != None:
            value = request.args.get('airdate')
            episodios = db.samples_friends.find({'airdate': value})
        elif request.args.get('summary') != None:
            value = str(request.args.get('summary'))
            episodios = db.samples_friends.find({'summary': value})
        else:
            episodios = db.samples_friends.find({})

        for episodio in episodios:
            lista.append({
                'id':     str(episodio.get('_id')),
                'name':       episodio.get('name'),
                'season':   episodio.get('season'),
                'number':   episodio.get('number'),
                'airdate': episodio.get('airdate'),
                'summary': episodio.get('summary')
            })
        return jsonify(lista)

    if request.method == 'POST':
        try:
            episodio = {
                'name':       request.form['name'],
                'season':   request.form['season'],
                'number':   request.form['number'],
                'airdate': request.form['airdate'],
                'summary': request.form['summary']
            }

            db.samples_friends.insert_one(episodio)

            return jsonify({'id': str(episodio['_id'])})
        except Exception:
            return jsonify({'error': 'Fallo al añadir episodio'}), 400


@app.route('/api/friends/<value>', methods=['GET', 'PUT', 'DELETE'])
def api_2(value):
    if request.method == 'GET':
        try:
            xreg = re.compile(f'([0-9A-Za-z]*){value}([0-9A-Za-z]*)')
            episodios = db.samples_friends.find({'name': xreg})
            lista = []
            for episodio in episodios:
                lista.append({
                    'id':     str(episodio.get('_id')),
                    'name':       episodio.get('name'),
                    'season':   episodio.get('season'),
                    'number':   episodio.get('number'),
                    'airdate': episodio.get('airdate'),
                    'summary': episodio.get('summary')
                })
            return jsonify(lista)
        except Exception:
            return jsonify({'error': 'Episodio no encontrado'}), 404

    if request.method == 'PUT':
        try:
            db.samples_friends.find_and_modify(query={'_id':ObjectId(value)}, 
            update={"$set": {
                'name':       request.form['name'],
                'season':   request.form['season'],
                'number':   request.form['number'],
                'airdate': request.form['airdate'],
                'summary': request.form['summary']
            }}, upsert=False, full_response= True)
            
            return jsonify({'editado': id})
        except Exception:
            return jsonify({'error': 'Episodio no encontrado'}), 404

    if request.method == 'DELETE':
        try:
            db.samples_friends.delete_one({'_id': ObjectId(value)})
            return jsonify({'borrado': value})
        except Exception:
            return jsonify({'error': 'Fallo al eliminar episodio'}), 400