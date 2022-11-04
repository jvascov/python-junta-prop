from flask import request, jsonify, session
import pyrebase
import config.fbConfig as fbConfig
import jwt
import datetime
# from config.fbConfig import config

firebase = pyrebase.initialize_app(fbConfig.config)
auth = firebase.auth()


def signin(email, password, collection):
    # if ('user' in session):
        # return session['user']

    try:
        userData = collection.where('email', '==', email).get()

        datos = [doc.to_dict() for doc in userData]
        # print('datos', datos[0]['id'])
        
        token = jwt.encode(
            {
            'public_id' : datos[0]['id'],
            'role': datos[0]['role'],
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
            }, fbConfig.secretKey, "HS256")
       
        
        return jsonify({'token': token,
                        'datos': datos}), 200
    except Exception as e:
        print('session3', session)
        return f'Error en logueo {e}'

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
