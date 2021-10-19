class Card:
    def __init__(self):
        self.data = []
    def __init__(self, Name, Desc, Color, ID, Armor = 0, Draw= 0, Dmg = 0, ExtraA= 0, Heal = 0, PowerA = False, PowerB = False, PowerC = False):
        self.name = Name
        self.desc = Desc
        self.id = ID
        self.damage= Dmg
        self.defese= Armor
        self.draw = Draw
        self.action= ExtraA
        self.healing= Heal
        self.powerA,self.powerB,self.powerC = PowerA, PowerB, PowerC
        self.color= Color