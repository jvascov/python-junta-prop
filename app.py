import os
from flask import Flask, request

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from routes.propietariosRoutes import create as createProp, read as readProp, update as updateProp

app = Flask(__name__)

cred = credentials.Certificate('./config/gKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()



@app.route('/propietarios', methods=['POST'])
def crearPropietario():
    collection_propietarios = db.collection('propietarios')
    return createProp(collection_propietarios)

@app.route('/propietarios', methods=['GET'])
def leerPropietarios():
    collection_propietarios = db.collection('propietarios')
    return readProp(collection_propietarios)

@app.route('/propietarios/<string:id>', methods=['GET', 'PUT'])
def leerPropietario(id):
    collection_propietarios = db.collection('propietarios')

    if request.method == 'GET':
        return readProp(collection_propietarios, id)
    else:
        return updateProp(collection_propietarios, id)

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)