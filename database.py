import peewee

# Define the database schema
db = peewee.SqliteDatabase('kids.db')

class Kid(peewee.Model):
    name = peewee.CharField()
    balance = peewee.DecimalField(decimal_places=2)

    class Meta:
        database = db

class Transaction(peewee.Model):
    kid = peewee.ForeignKeyField(Kid, backref='transactions')
    description = peewee.CharField()
    amount = peewee.DecimalField(decimal_places=2)

    class Meta:
        database = db

# Create the database tables
db.create_tables([Kid, Transaction])

# Functions to interact with the database
def get_kids():
    return Kid.select()

def add_kid(name, balance):
    kid = Kid(name=name, balance=balance)
    kid.save()

def get_kid(id):
    return Kid.get(Kid.id == id)

def update_kid_balance(id, new_balance):
    kid = Kid.get(Kid.id == id)
    kid.balance = new_balance
    kid.save()

def add_transaction(kid, description, amount):
    transaction = Transaction(kid=kid, description=description, amount=amount)
    transaction.save()

def get_transactions_for_kid(kid):
    return Transaction.select().where(Transaction.kid == kid)
