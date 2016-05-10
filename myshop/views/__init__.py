from .. import app
from flask import render_template

@app.route('/')
def hello_word():
    return render_template('index.html')