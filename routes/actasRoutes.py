from flask import request, jsonify
import pyrebase
import config.fbConfig as fbConfig
import os

config = {
    'apiKey' : os.getenv('apiKey') or fbConfig.apiKey,
    'authDomain' : os.getenv('authDomain') or fbConfig.authDomain,
    'projectId': os.getenv('projectId') or fbConfig.projectId,
    'storageBucket': os.getenv('storageBucket') or fbConfig.storageBucket,
    'messagingSenderId': os.getenv('messagingSenderId') or fbConfig.messagingSenderId,
    'appId': os.getenv('appId') or fbConfig.appId,
    'databaseURL': ""
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def create(collection):
    try:
        collection.add(request.json)
        return jsonify({'success': True}), 200
    except Exception as e:
        return f'Error registrando acta: {e}'


def read(collection, id = None):
    try:
        if id:
            coll = collection.document(id).get()
            return jsonify(coll.to_dict()), 200
        else:
            all_coll = []
            for doc in collection.stream():
                dictObj = {}
                dictObj = doc.to_dict()
                dictObj['id'] = doc.id
                all_coll.append(dictObj)
                

            return jsonify(all_coll), 200
                
    except Exception as e:
        return f'Error leyendo actas: {e}'

def update(collection, id):
    try:
        if id:
            collection.document(id).update(request.json)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Acta no existe'}), 400
    except Exception as e:
        return f'Error actualizando acta: {e}'