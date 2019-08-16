from flask import Flask
import pusher
app = Flask(__name__)

app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes

