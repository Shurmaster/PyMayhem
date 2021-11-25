import pygame as pg
from CardClass import *
from PlayerClass import *

pg.init()

bg = pg.image.load("images/start_saver_600x600.jpg")

## Can have a separate file for globals if we want
SCREENWIDTH = 1200
SCREENHEIGHT = 600


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        #self.player1 = Player()
        #self.player2 = Player()
        self.gameRunning = True
        self.gameState = 'start'
        self.selectedCard = ['', pg.K_0]

    # starting up the screen
    def start(self):
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
            elif self.gameState == 'select opp card':
                self.select_opp_events()
                self.select_opp_draw()
            elif self.gameState == 'help':
                self.help_events()
                self.help_draw()

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                print ("you selected key {}\n".format(pg.key.name(event.key)))
                # hold the selected key in this list for reference in the next scene
                self.selectedCard[0] = pg.key.name(event.key)
                self.selectedCard[1] = event.key
                self.gameState = 'confirm card'
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def card_select_draw(self):
        self.screen.fill(pg.Color("white"))

        # TODO: for cards in opponent's hand
        for i in range(0, 6):
            # TODO: if card has shield, draw shield
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # TODO: for cards in players hand
        for i in range(0, 6):
            # TODO: if card has shield, draw shield
            pg.draw.rect(self.screen, "blue", pg.Rect(100+(170*i), 350, 150, 250))

        pg.display.update()


    def confirm_card_events(self):
        # change your card selection or confirm it with ENTER
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and (event.key in [pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6]):
                print ("you selected key {}\n".format(pg.key.name(event.key)))
                # change the selected key
                self.selectedCard[0] = pg.key.name(event.key)
                self.selectedCard[1] = event.key
                self.gameState = 'confirm card'
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                pass
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def confirm_card_draw(self):
        self.screen.fill(pg.Color("white"))

        # TODO: for cards in opponent's handl
        for i in range(0, 6):
            # TODO: if card has shield, draw shield
            pg.draw.rect(self.screen, "pink", pg.Rect(150+(150*i), 0, 100, 133))

        # TODO: for cards in player's hand
        for i in range(0, 6):
            # TODO: if card has shield, draw shield
            pg.draw.rect(self.screen, "blue", pg.Rect(100+(170*i), 350, 150, 250))

        self.draw_text("You selected card {}".format(self.selectedCard[0]), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Press ENTER to confirm your selection, or a number to select another card.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("red"), pg.font.get_default_font(), True)
        pg.display.update()




######################################## MAIN ##############################################
if __name__ == "__main__":
    game = Game()
    game.start()
