from flask import Flask,current_app

app = Flask(__name__)

a = current_app
d = current_app.config['DEBUG']



