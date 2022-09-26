from flask import Flask, request, jsonify


def create(collection):
    try:
        id = request.json['id']
        
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