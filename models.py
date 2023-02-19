import datetime
import os

import peewee

db = peewee.SqliteDatabase(os.path.join(os.path.dirname(__file__), 'database.db'))


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Kid(BaseModel):
    name = peewee.CharField(unique=True)
    balance = peewee.DecimalField(default=0.00, decimal_places=2)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'balance': float(self.balance),
            'created_at': self.created_at.isoformat(),
        }
    
    def get_all(cls):
        kids = Kid.select()
        return [kid.to_dict() for kid in kids]


class Activity(BaseModel):
    kid = peewee.ForeignKeyField(Kid, backref='activities')
    name = peewee.CharField()
    cost = peewee.DecimalField(decimal_places=2)

    def to_dict(self):
        return {
            'id2': self.id2,
            'name': self.name,
            'cost': float(self.cost),
            'kid': self.kid.to_dict(),
        }
