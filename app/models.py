from peewee import *

db = SqliteDatabase('my_database.db')

class Kid(Model):
    name = CharField(unique=True)
    balance = FloatField()

    class Meta:
        database = db

class Transaction(Model):
    kid = ForeignKeyField(Kid, backref='transactions')
    amount = FloatField()
    description = CharField()

    class Meta:
        database = db

db.create_tables([Kid, Transaction])
