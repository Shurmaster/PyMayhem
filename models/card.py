class Card:
    def __init__(self, card_data):
        for attribute, data in card_data.items():
            setattr(self, attribute, data)

    def __repr__(self):
        return "Card<" + ', '.join(['{}: {}'.format(k,v) for k,v in self.__dict__.items()]) + ">"
