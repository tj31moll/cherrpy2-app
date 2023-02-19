import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
from models import db, Kid, Transaction

env = Environment(loader=FileSystemLoader(os.path.abspath('templates')))

class KidApp:

    @cherrypy.expose
    def index(self):
        kids = Kid.select()
        tmpl = env.get_template('index.html')
        return tmpl.render(kids=kids)

if __name__ == '__main__':
    db.connect()
    db.create_tables([Kid, Transaction])
    db.close()

    cherrypy.tree.mount(KidApp(), '/')
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
