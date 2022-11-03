# python-junta-prop

Aplicación para la administracion de las juntas directivas de las unidades residenciales, el primer modulo y el cual intentamos desarrollar, es la creacion de las actas de las juntas directivas, la toma de decisiones en cada una de las juntas y el resultado de esas votaciones. Actualmente alcanzamos a desarrollar la creacion de propietarios con su front, la consulta de propietarios con su front, el login con el front.

De los endpoints alcanzamos a desarrolar el resto del crud de propietarios, el crud de las actas y el logaout.

PENDIENTE:

Desarrollar el crud para los temas que se van a tratar en cada acta

Desarrollar el crud para la activacion, votacion y resultados de cada tema.

Opciones de la aplicacion (Front):

Administracion de propietarios

StartFragment

Registrar acta

Registrar temas

Activar temas y votacion

votacion

resultados

EndFragment

## Instalacion

### Crear un environment python

```
python -m venv C:\Users\egroj\Documents\www\python\01_BD\mongo\mongoEnviroment
cd script activate
python -m pip install pymongo
```

python -m pip install Flask
python -m pip freeze > requirements.txt
python -m pip install gunicorn
python -m pip freeze > requirements.txt
pip install "fastapi[all]"
python -m pip install motor

pip install -r requirements.txt

export MONGODB_URL="mongodb://localhost:27017/testCV?retryWrites=true&w=majority"

$env:MONGODB_URL="mongodb://localhost:27017/testCV?retryWrites=true&w=majority"

python -m pip install Flask gunicorn firebase_admin pyrebase4

python -m pip install Flask datetime uuid pyjwt
