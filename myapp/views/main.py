# coding: utf-8
from flask import render_template, Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def hello_world():
    return render_template('index.html')

@main.route('/login/')
def login():
    return render_template('login.html')
