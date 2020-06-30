import os
from flask import Flask, request, abort, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json


  # create and configure the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://aaltwaim@localhost:5432/estate'
CORS(app)
from models import Building, Unit

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)