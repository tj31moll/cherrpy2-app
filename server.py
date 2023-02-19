import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
from models import db, Kid, Activity

# Set up Jinja2 template engine
env = Environment(loader=FileSystemLoader(os.path.abspath('templates')))

# Set up the application
class App:

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('home.html')
        return tmpl.render()

    @cherrypy.expose
    def add_kid(self, name=None, balance=None, id=None):
        if name and balance:
            kid = Kid.create(name=name, balance=float(balance))
            tmpl = env.get_template('view_kid.html')
            return tmpl.render(kid=kid)
        else:
            tmpl = env.get_template('add_kid.html')
            return tmpl.render()

    @cherrypy.expose
    def view_kid(self, id=None):
        if id is None:
            return "Error: No kid ID provided"
        else:
            try:
                kid = Kid.get(id=id)
                tmpl = env.get_template('view_kid.html')
                return tmpl.render(kid=kid)
            except Kid.DoesNotExist:
                return "Error: Kid not found"

    @cherrypy.expose
    def all_kids(self):
        kids = Kid.select()
        tmpl = env.get_template('all_kids.html')
        return tmpl.render(kids=kids)

    @cherrypy.expose
    def add_activity(self, kid_id=None, name=None, cost=None, id=None):
        if kid_id and name and cost:
            kid = Kid.get(id=kid_id)
            activity = Activity.create(kid=kid, name=name, cost=float(cost), )
            activity.save()
            kid.balance -= activity.cost
            kid.save()
            tmpl = env.get_template('view_activity.html')
            return tmpl.render(activity=activity, kid=kid)
        else:
            kids = Kid.select()
            tmpl = env.get_template('add_activity.html')
            return tmpl.render(kids=kids)

    @cherrypy.expose
    def view_activity(self, id=None):
        if id is None:
            return "Error: No activity ID provided"
        else:
            try:
                activity = Activity.get(id=id)
                tmpl = env.get_template('view_activity.html')
                return tmpl.render(activity=activity)
            except Activity.DoesNotExist:
                return "Error: Activity not found"
            
    @cherrypy.expose
    def all_activities_for_kid(self, kid_id=None):
        if kid_id is None:
            return "Error: No kid ID provided"
        else:
            try:
                kid = Kid.get(id=kid_id)
                activities = Activity.select().where(Activity.kid == kid)
                tmpl = env.get_template('all_activities_for_kid.html')
                return tmpl.render(kid=kid, activities=activities)
            except Kid.DoesNotExist:
                return "Error: Kid not found"

    def create_tables():
        with db:
            db.create_tables([Kid, Activity])

App.create_tables()

if __name__ == '__main__':
    # Set up CherryPy server
    conf = {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath('./static'),
        },
    }
    cherrypy.tree.mount(App(), '/', config=conf)
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
