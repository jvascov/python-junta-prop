from flask import request, jsonify, session
import pyrebase
import config.fbConfig as fbConfig
import jwt
import datetime
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

secretKey = os.getenv('secretKey') or fbConfig.secretKey
tokenTime = os.getenv('token_time') or fbConfig.token_time

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def signin(email, password, collection):
    # if ('user' in session):
        # return session['user']

    try:
        userData = collection.where('email', '==', email).get()

        datos = [doc.to_dict() for doc in userData]
        # print('datos', datos[0]['id'])
        if datos[0]['email'] == email and datos[0]['password'] == password:
        
            token = jwt.encode(
                {
                'public_id' : datos[0]['id'],
                'role': datos[0]['role'],
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                }, secretKey, "HS256")
        
            
            return jsonify({'token': token,
                            'datos': datos}), 200
        else:
            return jsonify({'message': 'Usuario o password inválido'}), 401
    except Exception as e:
        return jsonify({'message': 'Usuario o password inválido',
        'error': e}), 400

def getNewToken():
    id = request.uuid
    role = request.role

    try:
                        
        token = jwt.encode(
            {
            'public_id' : id,
            'role': role,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
            }, fbConfig.secretKey, "HS256")
       
        
        return jsonify({'token': token}), 200
    except Exception as e:
        print('session3', session)
        return f'Error en logueo {e}'

def signout():
    session.pop('user')
    return jsonify({'success': True}), 200
