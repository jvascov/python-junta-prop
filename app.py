import os
from flask import Flask

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)

port = int(os.environ.get('PORT', 8080))

if __name__ == '__main':
    app.run(threaded=True, host='0.0.0.0', port=port)