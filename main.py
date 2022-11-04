import os
from flask import Flask, request, session, jsonify, render_template
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import wraps
from flask_cors import CORS, cross_origin
import jwt
import config.fbConfig as fbConfig

from routes.authRoutes import signin, signout, getNewToken
from routes.propietariosRoutes import create as createProp, read as readProp, update as updateProp
from routes.actasRoutes import create as createAct, read as readAct, update as updateAct
from routes.temasRoutes import crearTema, leerTemas, updateTema

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = 'ClaveSecreta'
cred = credentials.Certificate('./config/gKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

upload_folder = os.path.join('static')


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
        token = None
        bearer =''
        if 'Authorization' in request.headers:
            bearer = request.headers['Authorization'].split(' ')
            token = bearer[1]

        if not token:
            return jsonify({'error': 'No hay token de autenticacion'}), 400
        
        try:
            data = jwt.decode(token, fbConfig.secretKey, algorithms=["HS256"])
            request.uuid = data['public_id']
            request.role = data['role']

            
            
        except:
            return jsonify({'error': 'Usuario no autenticado!'}), 400

        return f(*args, **kargs)
    return _validarAutenticacion


''' PROPIETARIOS '''


@app.route('/propietarios', methods=['POST'])
@cross_origin()
@validarAutenticacion
# @validarRole
def crearPropietario():
    collection_propietarios = db.collection('propietarios')
    return createProp(collection_propietarios)


@app.route('/propietarios', methods=['GET'])
@cross_origin()
@validarAutenticacion
# @validarRole
def leerPropietarios():
    collection_propietarios = db.collection('propietarios')
    return readProp(collection_propietarios)


@app.route('/propietarios/<string:id>', methods=['GET', 'PUT'])
@cross_origin()
@validarAutenticacion
# @validarRole
def leerPropietario(id):
    collection_propietarios = db.collection('propietarios')
    print('id:', id)
    if request.method == 'GET':
        return readProp(collection_propietarios, id)
    else:
        return updateProp(collection_propietarios, id)


'''ACTAS'''


@app.route('/actas', methods=['POST'])
@cross_origin()
@validarAutenticacion
# @validarRole
def crearActa():
    collection_actas = db.collection('actas')
    return createAct(collection_actas)


@app.route('/actas', methods=['GET'])
@cross_origin()
@validarAutenticacion
# @validarRole
def leerActas():
    collection_actas = db.collection('actas')
    
    return readAct(collection_actas)


@app.route('/actas/<string:id>', methods=['GET', 'PUT'])
@cross_origin()
@validarAutenticacion
# @validarRole
def leerActa(id):
    collection_actas = db.collection('actas')

    if request.method == 'GET':
        return readAct(collection_actas, id)
    else:
        return updateAct(collection_actas, id)


'''TEMAS'''


@app.route('/temas', methods=['POST'])
@validarAutenticacion
# @validarRole
def crearTema():
    collection_temas = db.collection('temas')
    return crearTema(collection_temas)


@app.route('/actas', methods=['GET'])
@validarAutenticacion
# @validarRole
def leerTemas():
    collection_temas = db.collection('temas')
    return leerTemas(collection_temas)


@app.route('/temas/<string:id>', methods=['GET', 'PUT'])
@validarAutenticacion
# @validarRole
def leerTema(id):
    collection_temas = db.collection('temas')

    if request.method == 'GET':
        return readAct(collection_temas, id)
    else:
        return updateTema(collection_temas, id)


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.json['email']
    password = request.json['password']
    collection_propietarios = db.collection('propietarios')
    propietarios = signin(email, password, collection_propietarios)
    return propietarios    

@app.route('/renew', methods=['GET'])
@cross_origin()
@validarAutenticacion
def newToken():
    return getNewToken()


@app.route('/logout', methods=['POST'])
@cross_origin()
@validarAutenticacion
def logout():
    return signout()


port = int(os.environ.get('PORT', 8080))


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/opciones/')
def opciones():
    return render_template('opciones.html')


@app.route('/propietarios/')
def propietarios():
    return render_template('propietarios.html')


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
