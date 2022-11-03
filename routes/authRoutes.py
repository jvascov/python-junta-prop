from flask import request, jsonify, session
import pyrebase
import config.fbConfig as fbConfig

firebase = pyrebase.initialize_app(fbConfig.config)
auth = firebase.auth()


def signin(email, password, collection):
    if ('user' in session):
        print('session', session)
        return session['user']

    try:
        user = auth.sign_in_with_email_and_password(email, password)

        userData = collection.where('email', '==', email).get()

        datos = [doc.to_dict() for doc in userData]

        session['user'] = datos[0]

        print('session2', session)

        return jsonify({'user': user,
                        'datos': datos}), 200
    except Exception as e:
        print('session3', session)
        return f'Error en logueo {e}'


def signout():
    session.pop('user')
    return jsonify({'success': True}), 200
