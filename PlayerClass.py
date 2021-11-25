import random

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
    def myHand(self):
        myList = []
        for n in self.Hand:
            myList.append(str(n))
        return myList
    def myGY(self):
        myList = []
        for n in self.GY:
            myList.append(str(n))
        return myList
#For testing Purposes
##################################################################
#   Card Functions  (Currently in Player class as it seemed like it
#                   made the most sense as the actions in the game
#                   are made specifically to each player. Subject to changes.)
    def DrawCard(self, num=1):
        for i in range(0, num):
            if len(self.Hand) == 0:
                print("     There are 0 cards in hand; Shuffling")
                self.returnDeck()
            self.Deck2Hand() #
    def AttackOP(self, target, d): #Inflict {d} damage to Player {target}.
        if len(target.Shield) > 0:
            #print("     target's shields: {}".format(target.Shield))
            return False
        self.ChangeHP(-d, target)
        return True
    def HealingT(self, h): #Restores {h} points of life to self.
                           #(Without going over Player.MaxHP)
        self.ChangeHP(h, self)
    def GetAction(self, a): #Increase actions this turn by {a}.
        self.Actions+=a
    def getShield(self, n): #Adds a shield of {n}.
        self.Shield.append(n)

    def Whirlwind(self):
        return 0
        #Inflicts n damage to all opponents and restore n points of HP
        #Where n is the number of players
    def BattleRoar(self):
        return 0
        #All players discard their hand and draw 3 cards
    def DestroyShield(self):
        return 0
        #Destroy a Shield x from Player t.
    def DestroyAllShield(self):
        return 0
        #Calls DestroyShield for all players.
    def Fireball(self):
        return 0
        #Inflicts 3 damage to all players
    def StealShield(self):
        return 0
        #Take shield "s" from Player t and append it as your own.
    def SwapHP(self):
        return 0
        #Exchange HP with Player t.
    def DivInsp(self):
        return 0
        #Adds a card in your Discard Pile to your hand
    def Disguise(self):
        return 0
        #None of your opponent's cards affect you or your shields until your next turn.
    def PickPocket(self):
        return 0
        #Draw the top card of Player t's Deck

###################################################################
#   Alternative Functions
#   Basically other versions of above functions
#   In different scenarios, if needed.
    def AttackSh(self, target, d, st):
        target.Shield[st] -= d
        if target.Shield[st] == 0:
            target.Shield.pop(st)
            return d
        if target.Shield[st] < 0:
            return target.Shield.pop(st) * -1
        else:
            return 0
####################################################################
#   Helper Functions
#   Since so many actions will be repeated in one way or another with each effect
#   Of cards; I figured I'd made more sense to break down each part of the effects
#   In multiple pieces with the goal to avoid repetition in code writing.

    def Deck2Hand(self, card = 0):
        myCard = self.Deck.pop(card)
        self.Hand.append(myCard)
        return myCard
    def Hand2GY(self, card = 0):
        myCard = self.Hand.pop(card)
        self.GY.append(myCard)
        return myCard
    def Deck2GY(self, card= 0):
        myCard = self.Deck.pop(card)
        self.GY.append(myCard)
        return myCard
    def GY2Deck(self, card= 0):
        myCard = self.GY.pop(card)
        self.Deck.append(myCard)
        return myCard
    def ChangeHP(self, n, target):
        target.HP += n
        if (target.HP > target.MHP):
            target.HP = target.MHP
        if (target.HP < 0):
            target.HP = 0


#   Returns cards from the GY to the Deck, and proceeds to shuffle them
    def returnDeck(self):
        print("     Shuffling Deck!")
        while len(self.GY) > 0:
            #print("         {}".format(self.GY[0]))
            self.GY2Deck(0)
        print("GY: {}".format(self.GY))
        self.deckShuffle()
#   Moves around the order of the Deck List, randomizing it.
    def deckShuffle(self):
        random.shuffle(self.Deck)
        return 0
