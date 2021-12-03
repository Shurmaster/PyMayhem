
import pygame as pg
import sqlite3
import random
from Card import *
from Player import *

pg.init()

bg = pg.image.load("images/start_saver_600x600.jpg")
# images = load_images("images")

## Can have a separate file for globals if we want
SCREENWIDTH = 1200
SCREENHEIGHT = 600


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.gameRunning = True
        self.gameState = 'start'
        self.selectedCard = [None, None]
        self.selectedShield = [None, None]

        # info for each player
        self.P1 = YellowPlayer("Player 1") # deck ID 1 will be yellow
        self.P2 = RedPlayer("Player 2")
        self.players = [self.P1, self.P2]

        # info pertaining to the game
        self.turn = 0
        self.attacker = self.P1 # switch attacker/defender during hotseat
        self.defender = self.P2
        self.action_strings = []
        self.msg_cooldown = 3000
        self.msg_time_total = 0
        self.last = pg.time.get_ticks()
        self.ctr = 0

    # starting up the screen
    def start(self):
        self.setup() # run setup only once

        #DEBUG STUFF
        # for card in self.players[1].deck.cards:
        #     print(repr(card))

        while self.gameRunning:
            if self.gameState == 'start':
                self.start_events()
                self.start_draw()
            elif self.gameState == 'select card':
                self.card_select_events()
                self.card_select_draw()
            elif self.gameState == 'confirm card':
                self.confirm_card_events()
                self.confirm_card_draw()
            elif self.gameState == 'end turn':
                self.turn_end_events()
                self.turn_end_draw()
            elif self.gameState == 'select shield':
                self.shield_select_events()
                self.shield_select_draw()
            elif self.gameState == 'confirm shield':
                self.confirm_shield_events()
                self.confirm_shield_draw()
            elif self.gameState == 'game over':
                self.game_over_events()
                self.game_over_draw()
            elif self.gameState == 'help':
                self.help_events()
                self.help_draw()

    ######### GAME SETUP AND HANDLING ###########
    def setup(self):
        # add cards to each player's deck

        # connect to database first
        db = sqlite3.connect('cards.db')
        db.row_factory = sqlite3.Row
        c = db.cursor()

    ######### GENERAL HELPER FUNCTIONS ###########
    def draw_text(self, text, screen, pos, size, color, fontname, wantCentered = False):
        font = pg.font.SysFont(fontname, size)
        message = font.render(text, False, color)
        msg_sz = message.get_size()

        if wantCentered:
            pos[0] = pos[0] - msg_sz[0] // 2 # this is to make our text centered on the screen
            pos[1] = pos[1] - msg_sz[1] // 2 # this is to make our text centered on the screen

        screen.blit(message, pos)


    ###################################### START SCREEN HELPER FUNCTIONS ######################################
    def start_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: # user presses space bar to start playing the game
                self.gameState = 'select card'
            if event.type == pg.KEYDOWN and event.key == pg.K_TAB: # we'll have this to display options/help/about menu
                self.gameState = 'help'

    def start_draw(self):
        self.screen.blit(bg, (0, 0))
        self.draw_text('Dungeon Mayhem', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 32, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text('Push Space to start', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Push TAB for help!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.65], 28, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()

    ###################################### HELP SCREEN HELPER FUNCTIONS #####################################
    def help_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.gameState = 'start'
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def help_draw(self):
        self.screen.fill(pg.Color("black"))
        self.draw_text("Py Mayhem is an online version of the card game, Dungeon Mayhem", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Placeholder", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2.5], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Placeholder", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Placeholder", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Placeholder", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.6], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Placeholder", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.4], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Press SPACE to go back or Press ESCAPE to quit", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.2], 24, pg.Color("white"), pg.font.get_default_font(), True)
        pg.display.update()

    ###################################### GAME PLAY HELPER FUNCTIONS #####################################
    # select the card from your hand you want to play
    def card_select_events(self):
        self.msg_time_total = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if len(self.attacker.hand) <= 0:                 
                self.attacker.hand.extend(self.attacker.deck.draw(2))
                #If a player were to start their turn with no cards in hand; They can draw 2.

            if event.type == pg.KEYDOWN and (event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                if int(pg.key.name(event.key)) in range(1, len(self.attacker.hand)+1):
                    print ("you selected key {}\n".format(pg.key.name(event.key)))
                    # change the selected key
                    self.selectedCard[0] = pg.key.name(event.key)
                    self.selectedCard[1] = event.key
                    self.gameState = 'confirm card'
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def card_select_draw(self):
        self.screen.fill(pg.Color("white"))

        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)


        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                pg.draw.rect(self.screen, "orange", pg.Rect(120+(120*i)+(35*j), 0, 15, 15))

        # TODO: if card has shield, draw shield
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        pg.display.update()


    def confirm_card_events(self):
        # change your card selection or confirm it with ENTER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                if int(pg.key.name(event.key)) in range(1, len(self.attacker.hand)+1):
                    print ("you selected key {}\n".format(pg.key.name(event.key)))
                    # change the selected key
                    self.selectedCard[0] = pg.key.name(event.key)
                    self.selectedCard[1] = event.key
                    self.gameState = 'confirm card'
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                # check length of opponent's shield, and do a select shield if necessary

                self.attacker = self.players[self.turn % 2]
                self.defender = self.players[(self.turn + 1) % 2]

                if len(self.defender.shield) > 1:
                    # if there are shields, you need to select a shield now
                    self.gameState = 'select shield'

                else:
                    self.action_strings = self.attacker.take_turn_game(opponent=self.defender, hand_choice=(int(self.selectedCard[0])), opp_choice=-1)

                    # if someone's HP is zero
                    if (self.attacker.hp <= 0) or (self.defender.hp <= 0):
                        self.gameState = 'game over'
                    else:
                        self.last = pg.time.get_ticks()
                        self.gameState = 'end turn'

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def confirm_card_draw(self):
        self.screen.fill(pg.Color("white"))

        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)

        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                pg.draw.rect(self.screen, "orange", pg.Rect(120+(120*i)+(35*j), 0, 15, 15))

        # TODO: if card has shield, draw shield
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            if i == int(self.selectedCard[0])-1:
                rect.topleft = (100+(170*i),330)
            else:
                rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        try:
            self.draw_text("You selected card {}".format(self.attacker.hand[int(self.selectedCard[0])-1].id), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        except IndexError:
            pass

        self.draw_text("Press ENTER to confirm your selection, or a number to select another card.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()


    def shield_select_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                if int(pg.key.name(event.key)) in range(1, len(self.defender.shield)+1):
                    print ("you selected key {}\n".format(pg.key.name(event.key)))
                    # change the selected key
                    self.selectedShield[0] = pg.key.name(event.key)
                    self.selectedShield[1] = event.key
                    self.gameState = 'confirm shield'
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def shield_draw(self):
        self.screen.fill(pg.Color("white"))

        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)

        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                pg.draw.rect(self.screen, "orange", pg.Rect(120+(120*i)+(35*j), 0, 15, 15))

        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load(j.get_image_path()).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        #self.draw_text("You selected card {}".format(self.selectedCard[0]), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Now it's time to select an opponent shield.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()

    def confirm_shield_events(self):
        # change your shield selection or confirm it with ENTER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                if int(pg.key.name(event.key)) in range(1, len(self.defender.shield)+1):
                    print ("you selected key {}\n".format(pg.key.name(event.key)))
                    # change the selected key
                    self.selectedShield[0] = pg.key.name(event.key)
                    self.selectedShield[1] = event.key
                    self.gameState = 'confirm shield'
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if self.attacker.turns == 0:
                    self.attacker = self.players[self.turn % 2]
                    self.defender = self.players[(self.turn + 1) % 2]
                    self.attacker.turns = 1
                self.action_strings = self.attacker.take_turn_game(opponent=self.defender, hand_choice=(int(self.selectedCard[0])), opp_choice=int(self.selectedShield[1])+1)

                # if someone's HP is zero
                if (self.attacker.hp <= 0) or (self.defender.hp <= 0):
                    self.gameState = 'game over'
                else:
                    self.last = pg.time.get_ticks()
                    self.gameState = 'end turn'

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def confirm_shield_draw(self):
        self.screen.fill(pg.Color("white"))

        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)

        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                pg.draw.rect(self.screen, "orange", pg.Rect(120+(120*i)+(35*j), 0, 15, 15))

        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        self.draw_text("You selected shield {}".format(self.selectedShield[0]), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Press ENTER to confirm your selection, or a number to select another shield.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()


    def turn_end_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False

            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:

                self.action_strings.clear() # empty this list for the next round
                self.ctr = 0 # set the list index for action strings back to 0

                
                if self.attacker.turns == 0:
                    # swap the players
                    self.turn += 1
                    self.attacker = self.players[self.turn % 2]
                    self.defender = self.players[(self.turn + 1) % 2]
                    self.attacker.turns = 1
                    # drawing a card for the prev player each round
                    # Player should only be drawing cards at the beginning of turn
                    # If they have no cards in hand; they will draw 2
                    if len(self.attacker.hand) <= 0:                 
                        self.attacker.hand.extend(self.attacker.deck.draw(2))
                    self.attacker.hand.append(self.attacker.deck.draw())

                # start round over again
                self.gameState = 'select card'

            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def turn_end_draw(self):
        self.screen.fill(pg.Color("white"))

        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)

        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                pg.draw.rect(self.screen, "orange", pg.Rect(120+(120*i)+(35*j), 0, 15, 15))

        # TODO: if card has shield, draw shield
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load(j.get_image_path()).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)

            self.screen.blit(img, rect)


        # display actions of the card playeds
        if self.msg_time_total >= self.msg_cooldown*(len(self.action_strings)):
            if self.attacker.turns == 0:
                self.draw_text(f"Press ENTER to end your turn", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("red"), pg.font.get_default_font(), True)
            else:
                self.draw_text(f"Press ENTER to continue your turn ({self.attacker.turns} remaining)", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("red"), pg.font.get_default_font(), True)
        else:
            now = pg.time.get_ticks()
            if now-self.last >= self.msg_cooldown:
                self.last = now
                self.msg_time_total += self.msg_cooldown
                self.ctr+=1
                try:
                    self.draw_text(f"{self.action_strings[self.ctr]}", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("black"), pg.font.get_default_font(), True)
                except IndexError:
                    pass
            else:
                self.draw_text(f"{self.action_strings[self.ctr]}", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("black"), pg.font.get_default_font(), True)


        #self.draw_text("You selected card {}".format(self.selectedCard[0]), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Now your turn is over, executing actions.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()


    def game_over_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def game_over_draw(self):
        self.screen.fill(pg.Color("black"))
        self.draw_text('Game Over', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 32, pg.Color("white"), pg.font.get_default_font(), True)
        winner = None
        if self.attacker.hp > 0:
            winner = self.attacker
        else:
            winner = self.defender

        self.draw_text(f'{winner} has won the game!', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("You can close the game now", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.65], 28, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()




######################################## MAIN ##############################################
if __name__ == "__main__":
    game = Game()
    game.start()
