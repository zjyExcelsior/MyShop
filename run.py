# coding: utf-8
from myapp import create_app, db
from flask_script import Server, Manager

def create_all_tables(app):
    with app.app_context():
        db.create_all()

def drop_all_tables(app):
    with app.app_context():
        db.drop_all()

if __name__ == '__main__':
    app = create_app('config')
    # drop_all_tables(app)
    create_all_tables(app)
    manager = Manager(app)
    server = Server(host="0.0.0.0", port=5000, use_debugger=True, threaded=True)
    manager.add_command("runserver", server)
    manager.run()
