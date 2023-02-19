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

    @cherrypy.expose
    def add_kid(self, name=None, balance=None):
        if name and balance:
            kid = Kid.create(name=name, balance=balance)
            tmpl = env.get_template('add_kid.html')
            return tmpl.render(kid=kid)
        else:
            tmpl = env.get_template('add_kid.html')
            return tmpl.render()

    @cherrypy.expose
    def add_transaction(self, kid_id=None, description=None, amount=None):
        if kid_id:
            kid = Kid.get(Kid.id == kid_id)
            if description and amount:
                transaction = Transaction(kid=kid, description=description, amount=amount)
                amount = float(amount)
                transaction.save()
                new_balance = kid.balance + amount
                kid.balance = new_balance
                kid.save()
            tmpl = env.get_template('add_transaction.html')
            return tmpl.render(kid=kid)
        else:
            kids = Kid.select()
            tmpl = env.get_template('add_transaction.html')
            return tmpl.render(kids=kids)

    @cherrypy.expose
    def transactions(self, kid_id=None):
        if kid_id:
            kid = Kid.get(Kid.id == kid_id)
            transactions = Transaction.select().where(Transaction.kid == kid)
            tmpl = env.get_template('transactions.html')
            return tmpl.render(kid=kid, transactions=transactions)
        else:
            kids = Kid.select()
            tmpl = env.get_template('transactions.html')
            return tmpl.render(kids=kids)

if __name__ == '__main__':
    db.close()
    db.connect()
    db.create_tables([Kid, Transaction])
    cherrypy.tree.mount(KidApp(), '/')
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.engine.start()
    cherrypy.engine.block()
