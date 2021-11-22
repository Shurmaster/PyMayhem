import csv
import sqlite3
from Card import Card

if __name__ == "__main__":
    con = sqlite3.connect('cards.db')
    with con:
        cur = con.cursor()

        # check if cards table already exists, and drop it if so
        cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='cards' ''')
        if cur.fetchone()[0]:
            cur.execute("DROP TABLE cards")
            print("Dropped table cards.")

        # create cards table
        sql = '''CREATE TABLE cards (
            quantity   INT NOT NULL,
            id         TEXT PRIMARY KEY,
            deck       TEXT NOT NULL,
            armor      INT NOT NULL,
            draw       INT NOT NULL,
            damage     INT NOT NULL,
            extra_turn INT NOT NULL,
            heal       INT NOT NULL,
            power_1    INT NOT NULL,
            power_2    INT NOT NULL,
            power_3    INT NOT NULL,
            name       TEXT NOT NULL
        )'''
        cur.execute(sql)
        print("Created table cards.")

        # insert data from csv into db
        cards = []
        print("Loading table cards...", end=' ')
        with open('data/cards.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile);
            for row in reader:
                row['name'] = row['id'].title().replace('-', ' ').replace(' 2', '') # format names from
                cards.append(tuple(row.values()))
        cur.executemany('INSERT INTO cards VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', cards)
        print("Done.")
