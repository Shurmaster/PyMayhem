import Card
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.hp = 10
        self.shield = [] # list of ints
        self.turns = 0

        self.deck = Card.Deck(color)
        self.deck.shuffle()

        self.hand = self.deck.draw(3)
        self.active_card = None
        self.graveyard = []
        self.disguised = False # for clever disguise

    def reload_deck(self):
        for card in self.graveyard:
            self.deck.add_card(card)
        self.graveyard.clear()
        self.deck.shuffle()

    @abstractmethod
    def mighty_power_1(self, opponent):
        ...

    @abstractmethod
    def mighty_power_2(self, opponent):
        ...

    @abstractmethod
    def mighty_power_3(self, opponent):
        ...

    def heal(self, points=None):
        if points is None: # provide the option to manually set points for mighty powers
            points = self.active_card.heal
        if points > 0 and self.hp < 10:
            self.hp += points
            if self.hp > 10: self.hp = 10
            print(f"- Healed for {points} points to {self.hp} HP!")

    def apply_shield(self):
        if self.active_card.armor:
            self.shield.append(self.active_card.armor)
            print(f"- Got {self.active_card.armor} armor!")

    def extra_turns(self):
        if self.active_card.extra_turn:
            self.turns += self.active_card.extra_turn
            print(f"- Got {self.active_card.extra_turn} extra turn{'s' if self.active_card.extra_turn > 1 else ''}!")

    def draw(self):
        if self.active_card.draw:
            if len(self.deck.cards) < self.active_card.draw:
                self.reload_deck()
            self.hand += self.deck.draw(self.active_card.draw)
            print(f"- Drew {self.active_card.draw} card{'s' if self.active_card.draw > 1 else ''}!")

    def attack(self, opponent, dmg=None, bypass_shields=False):
        if dmg is None: # provide the option to manually set damage for mighty powers
            dmg = self.active_card.damage
        if opponent.disguised:
            print(f"- {opponent.name} was disguised and couldn't be attacked!")
            return
        while dmg > 0 and opponent.hp > 0: # keep attacking until we've spent all our damage
            # attack shields first
            if opponent.shield and not bypass_shields:
                # choose shield if multiple are available
                if len(opponent.shield) > 1:
                    prompt =  "{self.name}, which shield will you attack?\n"
                    prompt += ", ".join([f"{i + 1}: {shield}" for i, shield in enumerate(opponent.shield)])
                    prompt += "\n> "
                    while (choice := input(prompt)) not in [str(i + 1) for i in range(len(opponent.shield))]:
                        print("Invalid choice, please try again.\n")
                    choice = int(choice) - 1
                    damage_dealt = min(opponent.shield[choice], dmg)
                    print(f"- Dealt {damage_dealt} damage to the opponent's shield!", end=' ')
                    opponent.shield[choice] -= dmg
                    dmg -= damage_dealt
                    if opponent.shield[choice] <= 0:
                        opponent.shield.pop(choice)
                        print("The shield broke!", end='')
                    print()
                else: # only one shield available
                    damage_dealt = min(opponent.shield[0], dmg)
                    print(f"- Dealt {damage_dealt} damage to the opponent's shield!", end=' ')
                    opponent.shield[0] -= dmg
                    dmg -= damage_dealt
                    if opponent.shield[0] == 0:
                        opponent.shield.pop()
                        print("The shield broke!", end='')
                    print()
            else:
                damage_dealt = min(opponent.hp, dmg)
                opponent.hp -= damage_dealt
                dmg -= damage_dealt
                print(f"- Dealt {damage_dealt} damage to {opponent.name}!")

    def take_turn(self, *, opponent):
        self.turns = 1
        if self.disguised:
            self.disguised = False
        while self.turns > 0:
            print(repr(self))
            # top up deck
            if len(self.hand) == 0:
                self.hand = self.deck.draw(2)

            # choose card
            prompt =  "Which card will you play?"
            for i, card in enumerate(self.hand):
                prompt += f"\n{i + 1}: {card}"
            prompt += "\n> "
            while (choice := input(prompt)) not in [str(i + 1) for i in range(len(self.hand))]:
                print("Invalid choice, try again.\n")
            self.active_card = self.hand.pop(int(choice) - 1)
            print(f"{self.name} played {self.active_card.name}!")

            # take card actions
            self.heal()
            self.apply_shield()
            self.extra_turns()
            self.draw()
            self.attack(opponent)
            self.mighty_power_1(opponent)
            self.mighty_power_2(opponent)
            self.mighty_power_3(opponent)
            self.turns -= 1
            self.graveyard.append(self.active_card)
            self.active_card = None
            print('-' * 20)

    def __str__(self):
        return f"{self.name} ( {self.color} deck)"

    def __repr__(self):
        s  = f"PLAYER {self.name}\n"
        s += f"HP: {self.hp}/10\n"
        s += f"Deck color: {self.color}\n"
        s += f"Shields: {self.shield if self.shield else 'none'}\n"
        s += f"Turns: {self.turns}\n"
        return s

class RedPlayer(Player):
    def __init__(self, name):
        super().__init__(name, "red")

    def mighty_power_1(self, opponent):
        """Choose any card from your graveyard and place it in your hand."""
        if not self.active_card.power_1:
            return
        prompt = f"- {self.name}, which card will you choose from the graveyard?"
        for i, card in enumerate(self.graveyard):
            prompt += f"\n{i + 1}: {card}"
        prompt += "\n> "
        while (choice := input(prompt)) not in [str(i + 1) for i in range(len(self.graveyard))]:
            print("Invalid choice, try again.\n")
        card = self.graveyard.pop(int(choice) - 1)
        self.hand.append(card)
        print(f"- {card.name} was added to your hand!")

    def mighty_power_2(self, opponent):
        """Destroy all shields on both sides."""
        if not self.active_card.power_2:
            return
        for player in [self, opponent]:
            if player.disguised:
                print(f"- {opponent.name} was disguised and couldn't be affected!")
            else:
                player.shield.clear()
                print(f"- All of {player.name}'s shields were destroyed!")

    def mighty_power_3(self, opponent):
        """Red player has no third mighty power."""
        pass

class YellowPlayer(Player):
    def __init__(self, name):
        super().__init__(name, "yellow")

    def mighty_power_1(self, opponent):
        if not self.active_card.power_1:
            return
        """Deal 3 damage to all players, bypassing shields."""
        self.attack(self, dmg=3, bypass_shields=True)
        self.attack(opponent, dmg=3, bypass_shields=True)

    def mighty_power_2(self, opponent):
        """Steal a shield from the opponent."""
        if not self.active_card.power_2:
            return
        if opponent.disguised:
            print(f"- {opponent.name} was disguised and couldn't be affected!")
            return
        if opponent.shield:
            # choose shield if multiple are available
            if len(opponent.shield) > 1:
                prompt =  "{self.name}, which shield will you steal?\n"
                prompt += ", ".join([f"{i + 1}: {shield}" for i, shield in enumerate(opponent.shield)])
                prompt += "\n> "
                while (choice := input(prompt)) not in [str(i + 1) for i in range(len(opponent.shield))]:
                    print("Invalid choice, please try again.\n")
                choice = int(choice) - 1
                print(f"- Stole the opponent's shield!")
                self.shield.append(opponent.shield.pop(int(choice) - 1))
            else: # only one shield available
                self.shield.append(opponent.shield.pop(0))
            print(f"- Stole the opponent's shield!")
        else:
            print("- The opponent had no shields to steal.")

    def mighty_power_3(self, opponent):
        """Swap HP with the opponent."""
        if not self.active_card.power_3:
            return
        self.hp, opponent.hp = opponent.hp, self.hp
        print(f"- {self.name} and {opponent.name} swapped HP!")

class GreenPlayer(Player):
    def __init__(self, name):
        super().__init__(name, "green")

    def mighty_power_1(self, opponent):
        """Heal once, then attack once."""
        if not self.active_card.power_1:
            return
        self.heal(points=1)
        self.attack(opponent, dmg=1)

    def mighty_power_2(self, opponent):
        """Each player replaces their hand."""
        if not self.active_card.power_2:
            return
        for player in [self, opponent]:
            for card in player.hand:
                player.graveyard.append(card)
            if len(player.deck) < 3: # make sure deck has enough cards to draw
                for card in player.graveyard:
                    player.deck.add_card(card)
                player.graveyard.clear()

            player.hand = player.deck.draw(3)
            print(f"- {player.name} discarded their hand!")
            print(f"- {player.name} drew 3 cards!")

    def mighty_power_3(self, opponent):
        """Destroy one of the opponent's shields."""
        if not self.active_card.power_3:
            return
        if opponent.disguised:
            print(f"- {opponent.name} was disguised and couldn't be affected!")
            return
        if opponent.shield:
            # choose shield if multiple are available
            if len(opponent.shield) > 1:
                prompt =  "{self.name}, which shield will you destroy?\n"
                prompt += ", ".join([f"{i + 1}: {shield}" for i, shield in enumerate(opponent.shield)])
                prompt += "\n> "
                while (choice := input(prompt)) not in [str(i + 1) for i in range(len(opponent.shield))]:
                    print("Invalid choice, please try again.\n")
                choice = int(choice) - 1
                print(f"- Destroyed the opponent's shield!")
                opponent.shield.pop(int(choice) - 1)
            else: # only one shield available
                print(f"- Destroyed the opponent's shield!")
                opponent.shield.pop(0)
        else:
            print("- The opponent had no shields to destroy.")
        

class PurplePlayer(Player):
    def __init__(self, name):
        super().__init__(name, "purple")

    def mighty_power_1(self, opponent):
        if not self.active_card.power_1:
            return
        self.disguised = True
        print(f"- {self.name} put on a clever disguise! Their HP and shields can't be affected until their next turn!")

    def mighty_power_2(self, opponent):
        """Destroy one of the opponent's shields."""
        if not self.active_card.power_2:
            return
        if opponent.disguised:
            print(f"- {opponent.name} was disguised and couldn't be affected!")
            return
        if opponent.shield:
            # choose shield if multiple are available
            if len(opponent.shield) > 1:
                prompt =  "{self.name}, which shield will you destroy?\n"
                prompt += ", ".join([f"{i + 1}: {shield}" for i, shield in enumerate(opponent.shield)])
                prompt += "\n> "
                while (choice := input(prompt)) not in [str(i + 1) for i in range(len(opponent.shield))]:
                    print("Invalid choice, please try again.\n")
                choice = int(choice) - 1
                print(f"- Destroyed the opponent's shield!")
                opponent.shield.pop(int(choice) - 1)
            else: # only one shield available
                print(f"- Destroyed the opponent's shield!")
                opponent.shield.pop(0)
        else:
            print("- The opponent had no shields to destroy.")

    def mighty_power_3(self, opponent):
        """Take the top card of the opponent's deck and play it."""
        ...

if __name__ == "__main__":
    players = [YellowPlayer("skylar"), RedPlayer("test dummy")]
    for card in players[0].deck.cards:
        print(card.power_1)
    turn = 0
    while all([player.hp > 0 for player in players]):
        attacker = players[turn % 2]
        defender = players[(turn + 1) % 2]
        attacker.take_turn(opponent=defender)
        turn += 1