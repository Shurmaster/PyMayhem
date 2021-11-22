import sqlite3
from models.card import Card

db = sqlite3.connect('cards.db')
db.row_factory = sqlite3.Row
c = db.cursor()

all_cards = []

for row in c.execute("SELECT * FROM Cards").fetchall():
    row = dict(row)
    n = int(row.pop('quantity')) # we don't need this as instance data
    for i in range(n):
        all_cards.append(Card(row))

for item in all_cards:
    print(item)

db.close()
