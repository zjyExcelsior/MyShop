# coding: utf-8
from myshop import create_app, db
from flask_script import Server, Manager

app = create_app('config')
manager = Manager(app)
server = Server(host="0.0.0.0", port=5000, use_debugger=True, threaded=True)
manager.add_command("runserver", server)

@manager.command
def create_all_tables():
    '''create all tables'''
    db.create_all()


@manager.command
def drop_all_tables():
    '''drop all tables'''
    db.drop_all()

if __name__ == '__main__':
    manager.run()
