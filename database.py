from models import db, Kid

def seed_data():
    db.connect()
    db.create_tables([Kid])

    kids = [
        {'name': 'Alice', 'balance': 50},
        {'name': 'Bob', 'balance': 100},
        {'name': 'Charlie', 'balance': 75},
    ]

    for kid in kids:
        Kid.create(**kid)

    db.close()
