
import pygame as pg
import sqlite3
import random
from Card import *
from Player import *

# initializations
pg.init()

bg = pg.image.load("images/start_saver_1200x600.jpg")
help_screen = pg.image.load("images/help_screen.png")

SCREENWIDTH = 1200
SCREENHEIGHT = 600


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pg.display.set_caption("Py Mayhem")
        self.gameRunning = True
        self.gameState = 'start'
        self.selectedCard = [None, None]
        self.selectedShield = [None, None]
        self.selectedGY = 0

        # info for each player
        self.P1 = random_player_color("Player 1")
        self.P2 = random_player_color("Player 2")
        self.players = [self.P1, self.P2]

        # info pertaining to the game
        self.turn = 0
        self.attacker = self.P1 # switch attacker/defender during hotseat
        self.defender = self.P2
        self.action_strings = []
        self.msg_cooldown = 2000
        self.msg_time_total = 0
        self.last = pg.time.get_ticks()
        self.ctr = 0

    # starting up the screen
    def start(self):
        self.setup() # run setup only once

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
                self.shield_draw()
            elif self.gameState == 'select gy':
                self.gy_select_events()
                self.gy_select_draw()
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
        message = font.render(text, True, color)
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
        self.screen.blit(help_screen, (0, 0))
        pg.display.update()

    ###################################### GAME PLAY HELPER FUNCTIONS #####################################
    # select the card from your hand you want to play
    def card_select_events(self):
        self.msg_time_total = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
                #If a player were to start their turn with no cards in hand; They can draw 2.

            if event.type == pg.KEYDOWN and (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]):
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
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)

        # attacker hand
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        # drawing attacker shield
        for i in range(0, len(self.attacker.shield)):
            for j in range(0, self.attacker.shield[i]):
                img = pg.image.load("images/shield_a.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (100+(170*i)+(42*j), 315)
                self.screen.blit(img, rect)

        pg.display.update()


    def confirm_card_events(self):
        # change your card selection or confirm it with ENTER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]):
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

                active_card = self.attacker.hand[int(self.selectedCard[0]) - 1]

                if len(self.defender.shield) > 1 and (active_card.damage > 0 or active_card.requires_shield_select):
                    # if there are shields, you need to select a shield now
                    self.gameState = 'select shield'

                elif (active_card.deck == "red" and active_card.power_1) and len(self.attacker.graveyard) > 0:
                    self.gameState = 'select gy'

                else:
                    print("Its not either of the if statements")
                    print(f"ID: {active_card.deck} P1: {active_card.power_1} P2: {active_card.power_2} P3: {active_card.power_3}")
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
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)



        # attacker hand
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            if i == int(self.selectedCard[0])-1:
                rect.topleft = (100+(170*i),330)
            else:
                rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        # drawing attacker shield
        for i in range(0, len(self.attacker.shield)):
            for j in range(0, self.attacker.shield[i]):
                img = pg.image.load("images/shield_a.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (100+(170*i)+(42*j), 315)
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
            if event.type == pg.KEYDOWN and (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]):
                if int(pg.key.name(event.key)) in range(1, len(self.defender.shield)+1):
                    print ("you selected key {}\n".format(pg.key.name(event.key)))
                    # change the selected key
                    self.selectedShield[0] = pg.key.name(event.key)
                    self.selectedShield[1] = event.key
                    self.gameState = 'confirm shield'
                    print(f"**** SELECTED SHIELD: {self.selectedShield}****")
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
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)


        # attacker hand
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load(j.get_image_path()).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)


        # drawing attacker shield
        for i in range(0, len(self.attacker.shield)):
            for j in range(0, self.attacker.shield[i]):
                img = pg.image.load("images/shield_a.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (100+(170*i)+(42*j), 315)
                self.screen.blit(img, rect)

        #self.draw_text("You selected card {}".format(self.selectedCard[0]), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Now it's time to select an opponent shield.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()

    def confirm_shield_events(self):
        # change your shield selection or confirm it with ENTER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9]):
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
                self.action_strings = self.attacker.take_turn_game(opponent=self.defender, hand_choice=(int(self.selectedCard[0])), opp_choice=int(self.selectedShield[0])-1)

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
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)

        # attacker hand
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)
            self.screen.blit(img, rect)

        # drawing attacker shield
        for i in range(0, len(self.attacker.shield)):
            for j in range(0, self.attacker.shield[i]):
                img = pg.image.load("images/shield_a.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (100+(170*i)+(42*j), 315)
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

                if len(self.attacker.hand) == 0:
                    self.attacker.hand.extend(self.attacker.deck.draw(2))
                if self.attacker.turns == 0:
                    # swap the players
                    self.attacker.hand.append(self.attacker.deck.draw())
                    self.turn += 1
                    self.attacker = self.players[self.turn % 2]
                    self.defender = self.players[(self.turn + 1) % 2]
                    self.attacker.turns = 1
                    # drawing a card for the prev player each round
                    # Player should only be drawing cards at the beginning of turn
                    # If they have no cards in hand; they will draw 2

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
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))

        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)


        # attacker hand
        for i, j in enumerate(self.attacker.hand):
            img = pg.image.load(j.get_image_path()).convert()
            rect = img.get_rect()
            rect.topleft = (100+(170*i),350)

            self.screen.blit(img, rect)


        # drawing attacker hand and shield shield
        if self.attacker.turns == 0:
            for i, j in enumerate(self.attacker.hand):
                pg.draw.rect(self.screen, [32, 40, 69], pg.Rect(100+(170*i), 350, 150, 249))
        else:
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


        self.draw_text("Now your turn is over, executing actions.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()

    def gy_select_events(self):
        self.msg_time_total = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
                #If a player were to start their turn with no cards in hand; They can draw 2.
            if event.type == pg.KEYDOWN and (event.key in [pg.K_a, pg.K_d]):
                if event.key == pg.K_d:
                    self.selectedGY += 1
                else:
                    self.selectedGY -= 1
                if self.selectedGY <= 0:
                    self.selectedGY = 0
                if self.selectedGY >= len(self.attacker.graveyard) - 1:
                    self.selectedGY = len(self.attacker.graveyard) - 1
                print(self.selectedGY, len(self.attacker.graveyard) - 1, sep='\\')
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                print(1)
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                if self.attacker.turns == 0:
                    self.attacker = self.players[self.turn % 2]
                    self.defender = self.players[(self.turn + 1) % 2]
                    self.attacker.turns = 1
                self.action_strings = self.attacker.take_turn_game(opponent=self.defender, hand_choice=(int(self.selectedCard[0])) , opp_choice=self.selectedGY)
                self.selectedGY = 0
                self.gameState = 'end turn'


            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
    def gy_select_draw(self):
        self.screen.fill(pg.Color("white"))
        # HP
        self.draw_text(self.attacker.name, self.screen, [15, 475], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.attacker.hp}/10", self.screen, [15, 500], 24, pg.Color("blue"), pg.font.get_default_font(), False)
        self.draw_text(f"Turns: {self.attacker.turns}", self.screen, [15, 525], 24, pg.Color("green"), pg.font.get_default_font(), False)
        self.draw_text(self.defender.name, self.screen, [15, 25], 24, pg.Color("red"), pg.font.get_default_font(), False)
        self.draw_text(f"HP: {self.defender.hp}/10", self.screen, [15, 50], 24, pg.Color("red"), pg.font.get_default_font(), False)
        # opponent's hand
        for i, j in enumerate(self.defender.hand):
            pg.draw.rect(self.screen, [92, 92, 92], pg.Rect(150+(150*i), 0, 100, 133))
        # drawing groups of shields
        for i in range(0, len(self.defender.shield)):
            for j in range(0, self.defender.shield[i]):
                img = pg.image.load("images/shield_d.png").convert_alpha()
                rect = img.get_rect()
                rect.topleft = (150+(150*i)+(22*j), 145)
                self.screen.blit(img, rect)


        # TODO: if card has shield, draw shield
        """for i, j in enumerate(self.attacker.hand):
            img = pg.image.load("images/{}/{}.jpg".format(j.deck, j.id)).convert()
            rect = img.get_rect()
            rect.topleft = (100+(200),350)
            self.screen.blit(img, rect)"""
        # GY Rectangle
        pg.draw.rect(self.screen, "gray", pg.Rect(60, 60, 1080, 480))
        pg.draw.rect(self.screen, "yellow", pg.Rect(450, 130, 315, 350))


        self.draw_text(f"Select Card in GY:", self.screen, [int(SCREENWIDTH * 0.45), int(SCREENHEIGHT * 0.25)], 24, pg.Color("Black"), pg.font.get_default_font(), False)
        self.draw_text(f"GY: {self.selectedGY + 1}/{len(self.attacker.graveyard)}", self.screen, [int(SCREENWIDTH * 0.49), int(SCREENHEIGHT * 0.75)], 24, pg.Color("Black"), pg.font.get_default_font(), False)

        myCard = self.attacker.graveyard[self.selectedGY]
        img = pg.image.load("images/{}/{}.jpg".format(myCard.deck, myCard.id)).convert()

        rect = img.get_rect()
        rect.topleft = (535,int(SCREENHEIGHT * 0.3))
        self.screen.blit(img, rect)
        if self.selectedGY > 0:
            img2 = pg.image.load("images/{}/{}.jpg".format(self.attacker.graveyard[self.selectedGY - 1].deck, self.attacker.graveyard[self.selectedGY - 1].id)).convert()
            rect2 = img2.get_rect()
            self.draw_text("< [A]", self.screen, [400,int(SCREENHEIGHT * 0.3)], 24, pg.Color("black"), pg.font.get_default_font(), False)
            rect2.topleft = (235,int(SCREENHEIGHT * 0.3))
            self.screen.blit(img2, rect2)
        if self.selectedGY < len(self.attacker.graveyard) - 1:
            img3 = pg.image.load("images/{}/{}.jpg".format(self.attacker.graveyard[self.selectedGY + 1].deck, self.attacker.graveyard[self.selectedGY + 1].id)).convert()
            rect3 = img3.get_rect()
            self.draw_text("[D] >", self.screen, [785,int(SCREENHEIGHT * 0.3)], 24, pg.Color("black"), pg.font.get_default_font(), False)
            rect3.topleft = (835,int(SCREENHEIGHT * 0.3))
            self.screen.blit(img3, rect3)

        self.screen.blit(img, rect)
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
        self.draw_text("You can close the game now.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.65], 28, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()

# randomize a deck for each player
def random_player_color(playerStr):
    #current decks: Red, Yellow, Green
    #arbitrarily: Red=1, Yellow=2, Green=3
    rand = random.randint(1,3)
    if rand == 1:
        return RedPlayer(playerStr)
    elif rand == 2:
        return YellowPlayer(playerStr)
    elif rand == 3:
        return GreenPlayer(playerStr)



######################################## MAIN ##############################################
if __name__ == "__main__":
    game = Game()
    game.start()
