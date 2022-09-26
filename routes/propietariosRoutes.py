from flask import Flask, request, jsonify
from firebase_admin import auth


def create(collection):
    try:
        id = request.json['id']
        email = request.json['email']
        password = request.json['password']

        if email is None or password is None:
            return {'message': 'Error capturando email o password'},400

        user = auth.create_user(email = email, password = password)
        
        col = collection.document(id).get()

        if not col:
            collection.document(id).set(request.json)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'el usuario ya existe'}), 400
    except Exception as e:
        return f'Error registrando propietario: {e}'


def read(collection, id = None):
    try:
        if id:
            coll = collection.document(id).get()
            return jsonify(coll.to_dict()), 200
        else:
            all_coll = [doc.to_dict() for doc in collection.stream()]
            return jsonify(all_coll), 200
    except Exception as e:
        return f'Error leyendo propietarios: {e}'

def update(collection, id):
    try:
        if id:
            collection.document(id).update(request.json)
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'el propietario no existe'}), 400
    except Exception as e:
        return f'Error actualizando propietarios: {e}'