from flask import redirect, Flask, jsonify, abort, request, make_response, url_for, render_template, flash
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(__name__)

#client = MongoClient('mongodb://localhost:27017/')

@app.route('/')
def index():
    return render_template('index.html')
