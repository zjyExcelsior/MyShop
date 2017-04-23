#!/bin/sh
export FLASK_APP=manage.py
export FLASK_DEBUG=true
flask run --port 5050
