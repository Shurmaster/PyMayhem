import sqlite3
from random import shuffle as shuff

class Card:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) # lil bit of spicy python magic
        self.power_1 = self.power_1 == "TRUE"
        self.power_2 = self.power_2 == "TRUE"
        self.power_3 = self.power_3 == "TRUE"
        self.requires_shield_select = self.requires_shield_select == "TRUE"

    def get_image_path(self):
        return f"images/{self.deck}/{self.id}.jpg"
        
    def __str__(self):
        s = f"{self.name}: "
        attrs = []
        for k, v in self.__dict__.items():
            if k not in ['quantity', 'id', 'deck', 'name'] and v:
                if type(v) == bool:
                    attrs.append(k)
                else:
                    attrs.append(f"{v} {k}")
        return s + ", ".join(attrs)


    def __repr__(self):
        """Returns all card data for debug purposes."""
        attrs = ", ".join([f"{k}: {v}" for k, v in self.__dict__.items()])
        return f"{self.deck.title()} Card({attrs})"

class Deck:
    def __init__(self, color):
        self.color = color
        self.cards = []
        self.load()
        self.shuffle()

    def draw(self, n=1):
        """Removes n cards from the deck and returns them."""
        if n == 1:
            return self.cards.pop(0)
        else:
            return [self.cards.pop(0) for i in range(n)]

    def add_card(self, card):
        """Adds the provided card to the back of the deck."""
        self.cards.append(card)

    def shuffle(self):
        """Rearrange the order of the deck's cards randomly."""
        shuff(self.cards)

    def load(self):
        """Fill the deck with all cards of the correct color by loading from the database."""
        self.cards.clear()
        con = sqlite3.connect('cards.db')
        con.row_factory = sqlite3.Row # need this to get row as dict
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM cards WHERE deck=?', (self.color,))
            rows = cur.fetchall()
            for row in rows:
                row_dict = dict(row)
                # need to insert multiples of cards with quantity > 1
                for _ in range(row_dict['quantity']):
                    self.cards.append(Card(**row_dict))