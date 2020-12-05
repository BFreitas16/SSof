from flask import Flask
from flask_mysqldb import MySQL
import os, sys, time

from jinja2 import Environment

app = Flask(__name__)

app.config['SECRET_KEY'] = '\x83\xe1\xba%j\x0b\xe5Q\xdeiG\xde\\\xb1\x94\xe4\x0e\x1dk\x99\x1a\xda\xe8x'
app.config['MYSQL_HOST'] = 'db'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_USER'] = 'facefive'
app.config['MYSQL_PASSWORD'] = 'facefivepass'
app.config['MYSQL_DB'] = 'facefivedb'
app.config['photos_folder'] = './static/photos/'
app.config['default_photo'] = 'default-user.jpg'
app.config['MAX_CONTENT_PATH'] = 102400

mysql = MySQL(app)
current_user = None

@app.context_processor
def inject():
    return {'photos_folder' : app.config['photos_folder']}

from model import *
from views import * 

if __name__ == '__main__':
    ### enabled debug
    app.run(host='127.0.0.1', debug=True)

    ### # for mac you need a workaround and probably need to run it on 0.0.0.0
    ### # https://runnable.com/docker/python/docker-compose-with-flask-apps
    # app.run(host='0.0.0.0', debug=True)

    ### the program runs like this in the server
    # app.run(host='0.0.0.0', debug=False)