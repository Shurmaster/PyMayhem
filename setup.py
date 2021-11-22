import sqlite3
import csv

db = sqlite3.connect('cards.db')
c = db.cursor()

cards_table = """CREATE TABLE IF NOT EXISTS Cards (
                    quantity INTEGER NOT NULL,
                    id TEXT PRIMARY KEY,
                    deck TEXT NOT NULL,
                    armor INTEGER NOT NULL,
                    draw INTEGER NOT NULL,
                    damage INTEGER NOT NULL,
                    extra_turn INTEGER NOT NULL,
                    heal INTEGER NOT NULL
                );
             """
c.execute(cards_table);

with open('data/cards.csv', 'r') as infile:
    reader = csv.reader(infile)
    next(reader) # discard header
    card_insert = """INSERT INTO Cards(
                        quantity,
                        id,
                        deck,
                        armor,
                        draw,
                        damage,
                        extra_turn,
                        heal
                     ) VALUES (?,?,?,?,?,?,?,?);
                  """
    c.executemany(card_insert, reader)

db.commit()
db.close()
