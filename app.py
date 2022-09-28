import os
from flask import Flask, request, session, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import wraps


from routes.authRoutes import signin, signout
from routes.propietariosRoutes import create as createProp, read as readProp, update as updateProp
from routes.actasRoutes import create as createAct, read as readAct, update as updateAct

app = Flask(__name__)

app.secret_key = 'ClaveSecreta'
cred = credentials.Certificate('./config/gKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

""" 
register/login
https://parasmani300.medium.com/pyrebase-firebase-in-flask-d249a065e0df
https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login-es


Registrar propietarios - apartamentos

#modelo
#https://medium.com/@shivamkhandelwal555/a-proper-way-of-declaring-models-in-flask-9ce0bb0e42c1
Registrar acta
Registrar temas
Activar temas votacion
votacion
resultados

"""

""" 
    Middlewares
"""
def validarRole(f):
    @wraps(f)
    def _validarRole(*args, **kargs):
        if session['user']['role'] == 'admin':
            return f(*args, **kargs)
        else:
            return jsonify({'error': 'Usuario no autorizado'}), 400
    return _validarRole
    
def validarAutenticacion(f):
    @wraps(f)
    def _validarAutenticacion(*args, **kargs):
        if('user' in session):
            return f(*args, **kargs)
        else:
            return jsonify({'error': 'Usuario no autenticado'}), 400
    return _validarAutenticacion

''' PROPIETARIOS '''           

@app.route('/propietarios', methods=['POST'])
@validarAutenticacion
@validarRole
def crearPropietario():
    collection_propietarios = db.collection('propietarios')
    return createProp(collection_propietarios)

@app.route('/propietarios', methods=['GET'])
@validarAutenticacion
@validarRole
def leerPropietarios():
    collection_propietarios = db.collection('propietarios')
    return readProp(collection_propietarios)

@app.route('/propietarios/<string:id>', methods=['GET', 'PUT'])
@validarAutenticacion
@validarRole
def leerPropietario(id):
    collection_propietarios = db.collection('propietarios')

    if request.method == 'GET':
        return readProp(collection_propietarios, id)
    else:
        return updateProp(collection_propietarios, id)

'''ACTAS'''

@app.route('/actas', methods=['POST'])
@validarAutenticacion
@validarRole
def crearActa():
    collection_propietarios = db.collection('actas')
    return createAct(collection_propietarios)

@app.route('/actas', methods=['GET'])
@validarAutenticacion
@validarRole
def leerActas():
    collection_propietarios = db.collection('actas')
    return readAct(collection_propietarios)


@app.route('/actas/<string:id>', methods=['GET', 'PUT'])
@validarAutenticacion
@validarRole
def leerActa(id):
    print('id', id)
    collection_propietarios = db.collection('actas')

    if request.method == 'GET':
        return readAct(collection_propietarios, id)
    else:
        return updateAct(collection_propietarios, id)



@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    collection_propietarios = db.collection('propietarios')
    return signin(email, password, collection_propietarios)

@app.route('/logout', methods=['POST'])
@validarAutenticacion
def logout():
    return signout()

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)