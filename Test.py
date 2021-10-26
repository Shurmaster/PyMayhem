from PlayerClass import Player
from CardClass import Card
import random

def UseCard(ply, n):
    toRet = ply.Hand[n ]
    ply.Hand2GY(n)
    return toRet


if __name__ == "__main__":
    P1 = Player("Aldo", 2)
    P2 = Player("Not Aldo", 1)
    inGame = True
    myL = (P1, P2)
    ind = 0
    for i in myL:
        for n in range(0,27):
            myRand = random.randint(0, 30)                                                                            #Dmg = 0,             Draw= 0,              Heal = 0,             Armor = 0,            ExtraA= 0
            toAdd = Card("{}".format(myRand), "Is the {}th card.".format(myRand), i.deckID, random.randint(100, 200), random.randint(0, 4), random.randint(0, 1), random.randint(0, 1), random.randint(0, 2), int(random.randint(0, 50)/33) )
            i.Deck.append(toAdd)
    turn = 1
    for i in myL:
        i.DrawCard(3)

    while(inGame):
        for turnP in myL:
            if inGame == False:
                break
            turnP.Actions += 1
            print("==== Turn {} ======".format(turn))
            turnP.DrawCard(1)
            print("{} - HP:{} Deck:{}".format(turnP.player, turnP.HP, len(turnP.Deck)))
            Ptarget = myL[(myL.index(turnP) + 1) % len(myL)]
            print("Hand({}): {}".format(len(turnP.Hand), turnP.myHand()))
            print("GY({}): {}".format(len(turnP.GY), turnP.myGY()) )
            print("Armor: {}".format(turnP.Shield) )
            while turnP.Actions > 0:
                myUsed= UseCard(turnP, random.randint(0, len(turnP.Hand) - 1))
                print("Player {} used {} whichs deals {} Damage, Draws {} cards, Adds {} Armor, gives {} extra actions and Heals {} points.".format(turnP.player, myUsed, myUsed.damage, myUsed.draw, myUsed.defense, myUsed.action, myUsed.healing))
                if len(turnP.Hand) == 0:
                    turnP.DrawCard(2)
                    print("     empty Hand; Drawing 2 cards")
                    print("         Hand({}): {}".format(len(turnP.Hand), turnP.myHand()))
                myAttack = myUsed.damage
                while len(Ptarget.Shield) > 0:
                    myTargeto = random.randint(0, len(Ptarget.Shield)) - 1
                    print("     Opponent {}'s Shield: {}".format(Ptarget.player, Ptarget.Shield))
                    myAttack = turnP.AttackSh(Ptarget, myAttack, myTargeto)
                    print("     Damage remaining: {}".format(myAttack))
                    print("     Opponent {}'s Shield: {}".format(Ptarget.player, Ptarget.Shield))
                    if myAttack <= 0:
                        myAttack = 0
                        break
                turnP.AttackOP(Ptarget, myAttack)

                turnP.HealingT(myUsed.healing)
                turnP.DrawCard(myUsed.draw)
                turnP.GetAction(myUsed.action)
                if myUsed.defense > 0:
                    turnP.getShield(myUsed.defense)
                    print("{}'s Shield: {}".format(turnP.player, turnP.Shield))
                turnP.Actions -=1
                if Ptarget.HP <= 0 or turnP.HP <= 0:
                    inGame = False
                    print("\nBy turn {}: {}'s Health is {}; {} wins with {} HP!".format(turn, Ptarget.player, Ptarget.HP, turnP.player, turnP.HP))
                    break
            turn += 1
        

#    def __init__(self, Name, ID):

