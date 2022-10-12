from flask import Flask, request, jsonify
import pyrebase
import config.fbConfig as fbConfig

firebase = pyrebase.initialize_app(fbConfig.config)
auth = firebase.auth()

def crearTema(collection):
    try:
        tema = request.json['tema']

        if len(tema) < 5:
            return {'message': 'Error en el nombre del tema'},400
        
        collection.add(request.json)

        return jsonify({'success': True})

    except Exception as e:
        return f'Error registrando tema: {e}'

def leerTemas(collection, id = None):
    try:
        if id:
            collTema = collection.document(id).get()
            return jsonify(collTema.to_dict())
        else:
            collTemas = [doc.to_idct() for doc in collection.stream()]
            return jsonify(collTemas)
    except Exception as e:
        return f'Error obteniendo temas: {e}'

def updateTema(collection, id):
    try:
        if id:
            collection.document(id).update(request.json)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'el tema no existe'}), 400
    except Exception as e:
        return f'Error actualizando tema: {e}'