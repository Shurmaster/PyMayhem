class Player:
    def __init__(self, Name, ID):
        self.player =Name
        self.deckID = ID
        self.HP = 10
        self.MHP= 10
        self.Actions= 0
        self.Deck = []
        self.Hand = []
        self.GY   = []
        self.Shield= []
#
#   ID    : Used to determine what deck the Player chooses.
#           May be relevant for deck construction function
#           And certain Card Class Functions. 
#   Deck  : The deck of cards a Player will choose
#   Hand  : Cards the player should be able to see they have
#           And are able to use during their turn.
#   GY    : Discard Pile. This is where cards should go once
#           A player uses them.
#   Shield: Protects players from damage. Since each Shield is an 
#           individual item in the game, they are a list.
#           Compromises may be made if necessary.
#           (May be a List of Integers, and if the game detects
#           A player's len(Shield) is > 0, they may have to 
#           choose which shield to deal damage to.)

##################################################################
#   Card Functions  (Currently in Player class as it seemed like it 
#                   made the most sense as the actions in the game
#                   are made specifically to each player. Subject to changes.)
    def DrawCard(self, num=1):
        for i in range(0, num):
            if len(self.Deck) == 0:
                self.returnDeck()
            self.Deck2Hand() #
    def AttackOP(self, target, d): #Inflict {d} damage to Player {target}.
        return 0
    def HealingT(self, h): #Restores {h} points of life to self.
                           #(Without going over Player.MaxHP)
        return 0
    def GetAction(self, a): #Increase actions this turn by {a}.
        return 0
    def getShield(self, n): #Adds a shield of {n}.
        return 0
####################################################################
#   Helper Functions
#   Since so many actions will be repeated in one way or another with each effect
#   Of cards; I figured I'd made more sense to break down each part of the effects
#   In multiple pieces with the goal to avoid repetition in code writing.

    def Deck2Hand(self, card = 0): 
        self.Hand.append(self.Deck.pop(card))
    def Hand2GY(self, card = 0):  
        self.GY.append(self.Hand.pop[card])
    def Deck2GY(self, card= 0):
        self.GY.append(self.Deck.pop[card])
    def GY2Deck(self, card= 0):
        self.Deck.append(self.GY.pop[card])
    def ChangeHP(self, n, target = self):
        target.HP += n
        if (target.HP > target.MHP):
            target.HP = target.MHP
    

#   Returns cards from the GY to the Deck, and proceeds to shuffle them
    def returnDeck(self):
        while len(self.GY) > 0:
            self.GY2Deck()
        self.deckShuffle()
#   Moves around the order of the Deck List, randomizing it.
    def deckShuffle(self):
        return 0