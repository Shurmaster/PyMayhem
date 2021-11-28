class Card:
    def __init__(self):
        self.data = []
    #def __init__(self, Name, Desc, Color, ID, Armor = 0, Draw= 0, Dmg = 0, ExtraA= 0, Heal = 0, PowerA = False, PowerB = False, PowerC = False):
    def __init__(self, Name, Desc, Color, ID, Dmg = 0, Draw= 0, Heal = 0, Armor = 0, ExtraA= 0, PowerA = False, PowerB = False, PowerC = False):
        self.name = Name
        self.desc = Desc
        self.id = ID
        self.damage= Dmg
        self.defense= Armor
        self.draw = Draw
        self.action= ExtraA
        self.healing= Heal
        self.powerA,self.powerB,self.powerC = PowerA, PowerB, PowerC
        self.color= Color
        #print("ID: {} Damage: {}, Draw: {}, Action: {}, Armor: {}, Healing: {}".format(self.id, self.damage, self.draw, self.action, self.defense, self.healing))
    def __str__(self):
        return self.name
    def getList(self):
        return [self.name, self.desc, self.damage, self.draw, self.healing, self.action, self.defense]
        #To get data easily to program
        #Name, Description, Damage, Draw, Healing, Action, Armor
